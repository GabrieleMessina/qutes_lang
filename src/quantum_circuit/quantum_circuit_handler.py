import math
import utils
from typing import Any, Callable, cast
from quantum_circuit.classical_register import ClassicalRegister
from quantum_circuit.quantum_circuit import QuantumCircuit
from quantum_circuit.quantum_register import QuantumRegister
from qiskit.circuit import Qubit as QiskitQubit, Instruction
from symbols.types import Qubit, Quint, Qustring, QutesDataType, QuantumArrayType
from qiskit import QiskitError
from qiskit_aer import AerSimulator
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_ibm_runtime import SamplerV2 as Sampler
from quantum_circuit.state_preparation import StatePreparation
from qiskit.circuit.quantumcircuit import CircuitInstruction
from qiskit.circuit.library import grover_operator as GroverOperator, MCMTGate as MCMT, ZGate, QFT, XGate, YGate, HGate, CXGate, MCXGate, PhaseGate, HalfAdderGate
from qiskit.circuit.gate import Gate


def unwrap(l:list[QuantumRegister|ClassicalRegister]) -> list:
    unwrapped = []
    for el in l:
        if not isinstance(el, QuantumRegister) and not isinstance(el, ClassicalRegister):
            unwrapped.append(el)
        else:
            unwrapped.extend(el)
    return unwrapped

class QuantumCircuitHandler:
    anon_counter = iter(range(1000))
    anon_variable_name_prefix = "anon"
    def __init__(self):
        self._quantum_registers : list[QuantumRegister] = []
        self._registers_init_state : dict[QuantumRegister | ClassicalRegister, StatePreparation] = {}
        self._classic_registers : list[ClassicalRegister] = []
        self._nested_operations_stack :  list[list[Callable[[QuantumCircuit], None]]] = [[]]
        self._current_operations_queue :  list[Callable[[QuantumCircuit], None]] = self._nested_operations_stack[-1]
        self._varname_to_register : dict[str, QuantumRegister | ClassicalRegister] = {} # TODO: use symbol instead of str

    def declare_classical_register(self,  variable_name : str, bits_number : int) -> ClassicalRegister:
        new_register = ClassicalRegister(bits_number, variable_name)
        self._varname_to_register[variable_name] = new_register
        self._classic_registers.append(new_register)
        return new_register

    def declare_quantum_register(self, variable_name : str, quantum_variable : Qubit|Quint|Qustring|QuantumArrayType, is_anonymous = False) -> QuantumRegister:
        new_register = None
        if isinstance(quantum_variable, QuantumArrayType):
            bits = []
            for index, symbol in enumerate(quantum_variable.array):
                bits.extend(symbol.quantum_register._bits)
                # TODO: the following rename anon registers with another anon name, but we need to rename the anon register to the variable name
                # to achieve this we need to do the same in the assign_quantum_register_to_variable method
                # but there we don't have the QuantumArrayType we only have the QuantumRegister. How can we fix this?
                if symbol.quantum_register in self._registers_init_state and symbol.quantum_register.is_anonymous:
                    self.declare_quantum_register(f"{variable_name}_{index}", Qubit())
                    self.assign_quantum_register_to_variable(f"{variable_name}_{index}", symbol.quantum_register)
            new_register = QuantumRegister(None, variable_name, bits)
        else:
            new_register = QuantumRegister(quantum_variable.size, variable_name)
        new_register.is_anonymous = is_anonymous

        self._varname_to_register[variable_name] = new_register
        if new_register not in self._quantum_registers:
            self._quantum_registers.append(new_register)

        if not isinstance(quantum_variable, QuantumArrayType):
            self._registers_init_state[new_register] = quantum_variable.qubit_state
        return new_register

    # TODO: this should be a correlation operation, or a measure and then update,
    #       because we cannot rely on quantum_variable.qubit_state
    def create_and_assign_quantum_register(self,  variable_name : str, quantum_variable : Qubit|Quint|Qustring|QuantumArrayType, is_anonymous = False) -> QuantumRegister:
        if not QutesDataType.is_quantum_type(QutesDataType.type_of(quantum_variable)):
            raise SystemError("Error trying to update a quantum register with an unsupported type")

        quantum_register = self.declare_quantum_register(variable_name, quantum_variable, is_anonymous)
        self.assign_quantum_register_to_variable(variable_name, quantum_register)

        return quantum_register

    def assign_quantum_register_to_variable(self,  variable_name : str, new_quantum_register : QuantumRegister) -> QuantumRegister:
        #TODO: what about name collisions? maybe we should use symbol instead of name.
        if variable_name not in self._varname_to_register:
            raise SystemError("Error trying to update an undeclared quantum register")
        old_register = self._varname_to_register[variable_name]

        if old_register is new_quantum_register:
            return # the register is already assigned, nothing to do.

        old_register_has_other_ref = self.quantum_register_has_other_ref(old_register, variable_name)
        if new_quantum_register.is_anonymous: # this is the first time the anon is referenced by a variable so it can safely be recreated with a new name.
            anon_register = new_quantum_register
            new_name = f"{variable_name}_{next(QuantumCircuitHandler.anon_counter)}" if old_register_has_other_ref else variable_name
            new_quantum_register = QuantumRegister(None, new_name, bits=anon_register[:])
            if anon_register in self._registers_init_state:
                self._registers_init_state[new_quantum_register] = self._registers_init_state[anon_register]
            self._quantum_registers.append(new_quantum_register)
            self.remove_quantum_register(anon_register)

        self._varname_to_register[variable_name] = new_quantum_register

        if not old_register_has_other_ref:
            self.remove_quantum_register(old_register)

        return new_quantum_register

    def remove_quantum_register(self, quantum_register : QuantumRegister) -> None:
        if self._registers_init_state.get(quantum_register) is not None:
            del self._registers_init_state[quantum_register]
        if quantum_register in self._quantum_registers:
            self._quantum_registers.remove(quantum_register)

    def quantum_register_has_other_ref(self, quantum_register : QuantumRegister, variable_name:str) -> bool:
        """
        Check if there are other variables referencing the quantum register besides the one with the given variable name.
        """
        return any([quantum_register is reg and variable_name != name for name, reg in self._varname_to_register.items()])

    def _cleanup_orphan_registers(self):
        to_delete = [qreg for qreg in self._quantum_registers if not any([qreg is reg for reg in self._varname_to_register.values()])]
        for qreg in to_delete:
            self.remove_quantum_register(qreg)

    def _cleanup_anon_variables(self):
        to_delete = [var for var in self._varname_to_register.keys() if var.startswith(self.anon_variable_name_prefix)]
        for var in to_delete:
            self._varname_to_register.pop(var)

    def start_quantum_function(self):
        self._nested_operations_stack.append([])
        self._current_operations_queue = self._nested_operations_stack[-1]

    def end_quantum_function(self, *regs, name: str | None = None) -> QuantumCircuit | Gate:
        self._cleanup_orphan_registers()
        function_circuit = self._create_circuit(*regs)
        if name is not None:
            function_circuit.name = name
        self._nested_operations_stack.pop()
        self._current_operations_queue = self._nested_operations_stack[-1]
        return function_circuit

    def _create_circuit(self, *regs, compose_state_preparations:bool = False) -> QuantumCircuit:
        circuit = QuantumCircuit(*regs)

        if compose_state_preparations:
            for register in regs:
                if register in self._registers_init_state:
                    circuit.compose(self._registers_init_state[register], register, inplace=True)

        for operation in self._current_operations_queue:
            operation(circuit)
        return circuit

    def create_circuit(self) -> QuantumCircuit:
        self._cleanup_orphan_registers()
        return self._create_circuit(*self._quantum_registers, *self._classic_registers, compose_state_preparations=True)

    def print_circuit(self, circuit:QuantumCircuit, save_image:bool = False, print_circuit_to_console = True, image_file_prefix = ""):
        if save_image:
            import os
            # from PIL import Image
            from datetime import datetime
            directory = "circuit_images"
            timestamp = datetime.now().strftime("%Y_%m_%d-%H_%M_%S")
            file_name = f"{image_file_prefix}-{timestamp}.png"
            file_path = os.path.join(directory, file_name)
            if not os.path.exists(directory):
                os.mkdir(directory)
            circuit.draw(output='mpl', filename=file_path, style='iqp', fold=1000)
            # image = Image.open(file_path)
            # image.show()
            print(f"Circuit image printed at: {file_path}")

        if(print_circuit_to_console):
            print(circuit.draw())

    def get_counts_by_run(self, result) -> dict[str, int]:
        # {bitstring: count}
        return result[0].join_data().get_counts()

    def get_counts_by_register(self, result) -> dict[str, dict[str, int]]:
        # {reg_name: {bitstring: count}}
        cnt:dict[dict[int]] = {}
        for i, pub_res in enumerate(result): # For each circuit
            for reg_name in pub_res.data:
                reg_name = f'{reg_name}' if i == 0 else f'{reg_name}_circ_{i}'
                cnt[reg_name] = getattr(pub_res.data,reg_name).get_counts()
        return cnt

    def _run_circuit(self, circuit, shots, print_counts:bool = False):
        simulator = AerSimulator()
        pm = generate_preset_pass_manager(backend=simulator, optimization_level=1)

        isa_qc = pm.run(circuit)
        sampler = Sampler(mode=simulator)

        # Grab results from the job
        result = sampler.run([isa_qc], shots=shots).result()
        counts_by_registers = {}
        try:
            counts_by_registers = self.get_counts_by_register(result)
        except QiskitError:
            pass

        for reg_name, counts in counts_by_registers.items():
            for bitstring, count in counts.items():
                classical_registers = [reg for reg in self._classic_registers if reg.name == reg_name]
                classical_registers[0].measured_values.append(bitstring)
                classical_registers[0].measured_counts.append(count)

        if print_counts:
            self.print_result_table(result)


    def print_result_table(self, result):
        counts_by_run = {}
        counts_by_registers = {}
        try:
            counts_by_run = self.get_counts_by_run(result)
            counts_by_registers = self.get_counts_by_register(result)
        except (QiskitError, ValueError):
            pass

        from tabulate import tabulate
        table = []
        for index, (result, count) in enumerate(counts_by_run.items()):
            i = 0
            while i < len(result):
                row = []
                for reg_name in list(counts_by_registers.keys())[::-1]:
                    # reverse the regs list to match the qiskit ordering,
                    # measured variables from right to left based on measuring time
                    reg_size = self._varname_to_register[reg_name].size
                    bitstring = result[i:i+reg_size]
                    row.append(f"{bitstring}₂ | {int(bitstring, 2)}⏨")
                    i += reg_size
                row = row[::-1] # recover ordering to have first measured as first column
                row.append(count)
                row.append("Least Significant bit as rightmost") if(index == 0) else row.append("")
                table.append(row)

        if len(table) == 0:
            print("⚠️  ~ No results to show")
            return

        print("⚠️  ~ Following results only show the last execution of the circuit, in case of measurements in the middle of the circuit, like the ones needed for casts and Grover search, those results are not shown.")
        headers = [f"{reg_name}" for reg_name in counts_by_registers.keys()]
        headers.append("Counts")
        headers.append("Notes")
        maxcolwidths = [40] * len(headers)
        maxcolwidths[-1] = 40
        colalign = ["right"] * len(headers)
        colalign[-1] = "left"
        print(tabulate(table, headers=headers, stralign="right", tablefmt="fancy_grid", maxcolwidths=maxcolwidths, colalign=colalign))


    def run_circuit(self, circuit:QuantumCircuit, repetition:int = 1, print_count:bool = False):
        self._run_circuit(circuit, repetition, print_count)

    def get_run_and_measure_results(self, quantum_registers : list[QuantumRegister] = None, classical_registers : list[ClassicalRegister] = None, repetition = 1, max_results = None, print_count:bool = False) -> tuple[list[str], list[ClassicalRegister]]:
        quantum_registers = quantum_registers or self._quantum_registers
        classical_registers = self.push_measure_operation(quantum_registers, classical_registers)
        self.run_circuit(self.create_circuit(), repetition, print_count)
        # self._current_operation_stack.pop()

        for creg in classical_registers:
            [qreg for qreg in quantum_registers if qreg.name in creg.name][0].measured_classical_register = creg

        results = [reg.measured_values for reg in classical_registers]
        if max_results is not None:
            results = results[:max_results]
        return results, classical_registers

    def run_and_measure(self, quantum_registers : list[QuantumRegister] = None, classical_registers : list[ClassicalRegister] = None, repetition = 1, max_results = 1, print_count:bool = False) -> list[ClassicalRegister]:
        (_, classical_registers) = self.get_run_and_measure_results(quantum_registers, classical_registers, repetition, max_results, print_count)
        return classical_registers

    def get_run_and_measure_result_for_quantum_var(self, quantum_register : QuantumRegister, classical_register : ClassicalRegister = None, repetition = 1, max_results = 1, print_count:bool = False) -> list[str]:
        (_, classical_register) = self.get_run_and_measure_results([quantum_register], [classical_register] if classical_register is not None else None, repetition, max_results, print_count)
        return classical_register[0].measured_values[0]

    def push_not_operation(self, quantum_register : QuantumRegister) -> None:
        self._current_operations_queue.append(lambda circuit : cast(QuantumCircuit, circuit).x(quantum_register))

    def push_cnot_operation(self, quantum_register_control : QuantumRegister, quantum_register_target : QuantumRegister) -> None:
        self._current_operations_queue.append(lambda circuit : cast(QuantumCircuit, circuit).cx(quantum_register_control, quantum_register_target))

    def push_pauliy_operation(self, quantum_register : QuantumRegister) -> None:
        self._current_operations_queue.append(lambda circuit : cast(QuantumCircuit, circuit).y(quantum_register))

    def push_pauliz_operation(self, quantum_register : QuantumRegister) -> None:
        self._current_operations_queue.append(lambda circuit : cast(QuantumCircuit, circuit).z(quantum_register))

    def push_MCZ_operation(self, quantum_registers : list[QuantumRegister] | list[QiskitQubit]) -> None:
        mcz_gate = MCMT(ZGate(), sum([1 if isinstance(q, QiskitQubit) else q.size for q in quantum_registers]) - 1, 1)
        self._current_operations_queue.append(lambda circuit : cast(QuantumCircuit, circuit).compose(mcz_gate, unwrap(quantum_registers), inplace=True))

    def push_MCX_operation(self, quantum_registers : list[QuantumRegister] | list[QiskitQubit]) -> None:
        mcx_gate = MCMT(XGate(), sum([1 if isinstance(q, QiskitQubit) else q.size for q in quantum_registers]) - 1, 1)
        self._current_operations_queue.append(lambda circuit : cast(QuantumCircuit, circuit).compose(mcx_gate, unwrap(quantum_registers), inplace=True))

    def push_MCY_operation(self, quantum_registers : list[QuantumRegister] | list[QiskitQubit]) -> None:
        mcy_gate = MCMT(YGate(), sum([1 if isinstance(q, QiskitQubit) else q.size for q in quantum_registers]) - 1, 1)
        self._current_operations_queue.append(lambda circuit : cast(QuantumCircuit, circuit).compose(mcy_gate, unwrap(quantum_registers), inplace=True))

    def push_MCP_operation(self, theta, quantum_registers : list[QuantumRegister] | list[QiskitQubit]) -> None:
        mcp_gate = MCMT(PhaseGate(theta), sum([1 if isinstance(q, QiskitQubit) else q.size for q in quantum_registers]) - 1, 1)
        self._current_operations_queue.append(lambda circuit : cast(QuantumCircuit, circuit).compose(mcp_gate, unwrap(quantum_registers), inplace=True))

    def push_hadamard_operation(self, quantum_register : QuantumRegister) -> None:
        self._current_operations_queue.append(lambda circuit : cast(QuantumCircuit, circuit).h(quantum_register))

    def push_barrier_operation(self) -> None:
        self._current_operations_queue.append(lambda circuit : cast(QuantumCircuit, circuit).barrier())

    def push_swap_operation(self, quantum_register_a : QuantumRegister, quantum_register_b : QuantumRegister) -> None:
        self._current_operations_queue.append(lambda circuit : cast(QuantumCircuit, circuit).swap(quantum_register_a, quantum_register_b))

    def push_equals_operation(self, quantum_register_a : QuantumRegister, classical_value : Any) -> None:
        quantum_value : Qubit | Quint | Qustring = QutesDataType.promote_classical_to_quantum_value(classical_value)
        #find the only element in the statevector with prob == 1, and take its binary representation
        state_to_match = utils.binary(quantum_value.qubit_state.params.index(complex(1)), len(quantum_register_a))
        for index, state in enumerate(state_to_match):
            if state == "0":
                self.push_not_operation(quantum_register_a[index])

    def push_reset_operation(self, quantum_register : QuantumRegister) -> None:
        self._current_operations_queue.append(lambda circuit : cast(QuantumCircuit, circuit).reset(quantum_register))

    """
    Push sum operation for two quantum registers and a carry register.
    The sum is done using a half adder circuit.
    We expect symbol_b to have always one qubit more than symbol_a.
    The carry register is used to store the carry of the sum.
    The sum is done in place, so the symbol_b register is modified.
    """
    def push_sum_operation(self, symbol_a, symbol_b, symbol_carry):
        quantum_register_a:QuantumRegister = symbol_a.quantum_register
        quantum_register_b:QuantumRegister = symbol_b.quantum_register
        quantum_register_carry:QuantumRegister = symbol_carry.quantum_register
        numbers_len = min(quantum_register_a.size, quantum_register_b.size)

        adder = HalfAdderGate(numbers_len)
        quantum_registers = unwrap(quantum_register_a[:numbers_len] + quantum_register_b[:numbers_len] + quantum_register_carry[:])
        self.push_compose_circuit_operation(adder, quantum_registers)

    def push_compose_circuit_operation(self, circuit_to_compose : QuantumCircuit|Instruction, quantum_registers : list[QuantumRegister] = None, classical_registers=None) -> None:
        if classical_registers is None:
            classical_registers = []
        if quantum_registers is None:
            quantum_registers = self._quantum_registers
        self._current_operations_queue.append(lambda circuit: circuit.compose(circuit_to_compose, unwrap(quantum_registers), unwrap(classical_registers), inplace=True))

    def push_compose_controlled_circuit_operation(self, circuit_to_compose : QuantumCircuit, quantum_registers : list[QiskitQubit] = None, classical_registers=None, quantum_controller_registers : list[QiskitQubit] = None, controller_name: str|None = None) -> None:
        if classical_registers is None:
            classical_registers = []
        if quantum_registers is None:
            quantum_registers = []

        # TODO: add a global static class where to put all debug flags and use that class.
        self.print_circuit(circuit_to_compose, save_image=True, print_circuit_to_console=False, image_file_prefix=circuit_to_compose.name)

        # Make the gate controlled
        num_control_qubit = len(quantum_controller_registers)
        control_label = f"if {controller_name}" if controller_name is not None else None
        circuit_to_compose = circuit_to_compose.control(num_control_qubit, label=control_label)
        # Append compose operation
        qbits = quantum_controller_registers + quantum_registers
        qbits = list(dict.fromkeys(qbits)) #distinct preserving order
        self._current_operations_queue.append(lambda circuit: circuit.compose(circuit_to_compose, qbits, unwrap(classical_registers), inplace=True))

    def push_measure_operation(self, quantum_registers : list[QuantumRegister] = None, classical_registers : list[ClassicalRegister] = None) -> list[ClassicalRegister]:
        if quantum_registers == None:
            quantum_registers = self._quantum_registers

        if classical_registers == None:
            classical_registers = []

        for quantum_register in quantum_registers:
            classic_register_name = "measured_"+quantum_register.name
            search = [reg for reg in self._classic_registers if reg.name == classic_register_name]
            already_exists = any(search)
            if not already_exists:
                classic_register = self.declare_classical_register(classic_register_name, len(quantum_register))
            else:
                classic_register = search[0]
            classical_registers.append(classic_register)

        self._current_operations_queue.append(lambda circuit : cast(QuantumCircuit, circuit).measure(unwrap(quantum_registers), unwrap(classical_registers)))
        return classical_registers

    def push_ESM_operation(self, input:QuantumRegister, rotation_register:QuantumRegister, to_match:Qustring|Quint|Qubit, block_size, phase_kickback_ancilla = None) -> None:
        array_len = len(input)
        to_match_len = to_match.size

        # rotate input array
        from quantum_circuit.qutes_gates import QutesGates
        for i in range(len(rotation_register)):
            self.push_compose_circuit_operation(QutesGates.crot(array_len, 2**i, block_size), [rotation_register[i], *input])

        # compare x and y[:m]
        self.push_equals_operation(input[:to_match_len], to_match)
        if phase_kickback_ancilla is None:
            self.push_MCZ_operation([*input[:to_match_len]])
        else:
            self.push_MCZ_operation([*input[:to_match_len], phase_kickback_ancilla])

        self.push_equals_operation(input[:to_match_len], to_match)

        for i in range(len(rotation_register))[::-1]:
            self.push_compose_circuit_operation(QutesGates.crot(array_len, 2**i, block_size).inverse(), [rotation_register[i], *input])

    # It expects the register to put the result into to be the last one in the list
    grover_count = iter(range(1, 1000))
    def push_grover_operation(self, *oracle_registers, quantum_function:QuantumCircuit, register_involved_indexes, dataset_size, n_results = 1, verbose:bool = False) -> QuantumRegister:
        current_grover_count = next(self.grover_count)
        grover_op = GroverOperator(quantum_function, reflection_qubits=register_involved_indexes, insert_barriers=True, name=f"Grover{current_grover_count}")

        if verbose:
            self.print_circuit(quantum_function, save_image=True, image_file_prefix="quantum function")
            self.print_circuit(grover_op.decompose(), save_image=True, image_file_prefix="grover")

        n_iteration = math.floor(
            (math.pi / 4) * math.sqrt(dataset_size / n_results)
        )
        if verbose:
            print(f"Grover iterations: {n_iteration}")

        self.push_compose_circuit_operation(grover_op.power(n_iteration), oracle_registers)

        # Make the Z Controlled Oracle a X Controlled Oracle
        self.push_barrier_operation()
        boolean_quantum_function = quantum_function.copy()
        for index, instruction in enumerate(boolean_quantum_function.data):
            if isinstance(instruction, CircuitInstruction):
                name : str = instruction.operation.name
                op = instruction.operation
                if name == "mcmt" and op.base_gate.name == "z":
                    boolean_quantum_function.data[index] = CircuitInstruction(MCXGate(op.num_qubits), [*instruction.qubits,*oracle_registers[-1]], instruction.clbits)

        # check if the grover result is actually a hit.
        oracle_result = self.declare_quantum_register(f"oracle_phase_ancilla_{current_grover_count}", Qubit())
        self.push_compose_circuit_operation(boolean_quantum_function, [*oracle_registers[:-1],oracle_result])
        return oracle_result