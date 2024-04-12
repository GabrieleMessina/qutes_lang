import math
from typing import Any, Callable, cast
from quantum_circuit.classical_register import ClassicalRegister
from quantum_circuit.quantum_circuit import QuantumCircuit
from quantum_circuit.quantum_register import QuantumRegister, QiskitQubit
from symbols.types import Qubit, Quint, Qustring, QutesDataType
from qiskit import IBMQ, Aer, QiskitError, transpile
from qiskit.primitives import Sampler
from qiskit.circuit.quantumcircuit import QubitSpecifier, CircuitInstruction
from qiskit.circuit.library import GroverOperator, MCMT, ZGate, QFT, XGate, YGate, HGate, CXGate, MCXGate, PhaseGate
from qiskit.circuit.gate import Gate

def unwrap(l:list[QuantumRegister|ClassicalRegister]) -> list:
    unwrapped = []
    for el in l:
        if(not isinstance(el, QuantumRegister) and not isinstance(el, ClassicalRegister)):
            unwrapped.append(el)
        else:
            unwrapped.extend(el)
    return unwrapped

class QuantumCircuitHandler():
    def __init__(self):
        self._quantum_registers : list[QuantumRegister] = []
        self._registers_states : dict[QuantumRegister | ClassicalRegister, list[complex] | str | None] = {}
        self._classic_registers : list[ClassicalRegister] = []
        self._operation_stacks :  list[list[Callable[[QuantumCircuit], None]]] = [[]]
        self._current_operation_stack :  list[Callable[[QuantumCircuit], None]] = self._operation_stacks[-1]
        self._varname_to_register : dict[str, QuantumRegister] = {}

    def declare_classical_register(self,  variable_name : str, bits_number : int) -> ClassicalRegister:
        new_register = ClassicalRegister(bits_number, variable_name)
        self._varname_to_register[variable_name] = new_register
        self._classic_registers.append(new_register)
        return new_register

    def delete_classical_register(self,  variable_name : str) -> None:
        register = self._varname_to_register[variable_name]
        self._classic_registers.remove(register)

    def declare_quantum_register(self, variable_name : str, quantum_variable : any) -> QuantumRegister:
        new_register = None

        new_register = QuantumRegister(quantum_variable.size, variable_name)

        if(new_register is None):
            raise SystemError("Error trying to declare a quantum variable of unsupported type")

        self._varname_to_register[variable_name] = new_register
        self._quantum_registers.append(new_register)
        self._registers_states[new_register] = quantum_variable.get_quantum_state()
        return new_register
    
    def replace_quantum_register(self,  variable_name : str, quantum_variable : any) -> QuantumRegister:
        register_to_update = self._varname_to_register[variable_name]
        if(register_to_update is None):
            raise SystemError("Error trying to update an undeclared quantum register")

        #TODO: can we handle qubit like quint and qustring?
        # if(isinstance(quantum_variable, Qubit)):
        #     pass
        if(isinstance(quantum_variable, Qubit) or isinstance(quantum_variable, Quint) or isinstance(quantum_variable, Qustring)):
            #TODO-CRITICAL: this update actually change the reference, so all the old references around the code are still there. For now i hack this returning the new value and changing the name from update to replace.
            #Delete old quantum register and reference
            del self._registers_states[register_to_update]
            self._quantum_registers.remove(register_to_update)
            #Add new quantum register
            register_to_update = self._varname_to_register[variable_name] = QuantumRegister(quantum_variable.size, variable_name)
            self._quantum_registers.append(register_to_update)

        self._registers_states[register_to_update] = quantum_variable.get_quantum_state()
        return register_to_update

    def assign_quantum_register_to_variable(self,  variable_name : str, quantum_register : QuantumRegister) -> QuantumRegister:
        register_to_update = self._varname_to_register[variable_name]
        if(register_to_update is None):
            raise SystemError("Error trying to update an undeclared quantum register")
        
        #TODO-CRITICAL(pasted from above, i don't know if this applies here too): this update actually change the reference, so all the old references around the code are still there. For now i hack this returning the new value and changing the name from update to replace.
        
        #TODO: check if we need to change the register size
        #TODO: i don't know why we don't save the new quantum_register to the internal data structures.
        if(register_to_update != quantum_register):
            #Delete old quantum register reference from the variable
            del self._registers_states[register_to_update]
            self._quantum_registers.remove(register_to_update)
            #Assign already created register reference to the variable
            self._varname_to_register[variable_name] = quantum_register
        return quantum_register
    
    def start_quantum_function(self):
        self._operation_stacks.append([])
        self._current_operation_stack = self._operation_stacks[-1]

    def end_quantum_function(self, *regs, gate_name:str, create_gate:bool = False) -> Gate:
        gate = self.create_circuit(*regs, do_initialization=False)
        if(create_gate):
            gate = gate.to_gate()
        gate.name = gate_name
        self._operation_stacks.pop()
        self._current_operation_stack = self._operation_stacks[-1]
        return gate

    def create_circuit(self, *regs, do_initialization:bool = True) -> QuantumCircuit:
        if(len(regs) == 0):
            circuit = QuantumCircuit(*self._quantum_registers, *self._classic_registers)
        else:
            circuit = QuantumCircuit(*regs)

        for register in self._quantum_registers:
            # circuit.initialize('01', register, True)
            # circuit.initialize([0, 1/np.sqrt(2), -1.j/np.sqrt(2), 0], register, True)
            # TODO: the following should be pushed as an operation because we don't want this to execute while creating gates.
            if(do_initialization):
                circuit.prepare_state(self._registers_states[register], register, "|0⟩-|1⟩/√2 ",normalize=True)
        for operation in self._current_operation_stack:
            operation(circuit)
        return circuit

    def print_circuit(self, circuit:QuantumCircuit, save_image:bool = False, print_circuit_to_console = True):
        if(save_image):
            import os 
            directory = "temp"
            file_name = "circuit.png"            
            file_path = os.path.join(directory, file_name)
            if not os.path.exists(directory):
                os.mkdir(directory)
            circuit.draw(output='mpl', filename=file_path)
            print(f"Circuit image printed at: {file_path}")
        if(print_circuit_to_console):
            print(circuit.draw())

    def __counts__(self, vec):
        for i in vec:
                print(" - " + str(i) +" : "+ str(vec[i]))

    def __revcounts__(self, vec):
        for i in vec:
                print(" - " + str(i)[::-1] +" : "+ str(vec[i]))

    # simulate the execution of a Quantum Circuit and get the results
    def __run__(self, circuit, shots, print_counts:bool = False):
        # Use Aer's qasm_simulator
        simulator = Aer.get_backend('aer_simulator')

        # compile the circuit down to low-level QASM instructions
        # supported by the backend (not needed for simple circuits)
        compiled_circuit = transpile(circuit, simulator)

        # Execute the circuit on the qasm simulator
        job = simulator.run(compiled_circuit, shots=shots)
        
        # Grab results from the job
        result = job.result()
        cnt = None
        try:
            cnt = result.get_counts(compiled_circuit)
        except QiskitError as er:
            if(er.message.startswith("No counts for experiment")):
                print(er.message)
            else: 
                raise er

        if(cnt != None):
            table = []
            for run in cnt:
                count = cnt[run]
                values = run.split(" ")[::-1]
                values.append(count)
                table.append(values)

            if(print_counts):
                from tabulate import tabulate
                print(tabulate(table, headers=[f"{creg[0]}[{creg[1]}]" for creg in cnt.creg_sizes] + ["count"]))

            measurement_for_runs = [res.split(" ")[::-1] for res in cnt.keys()]
            counts_for_runs = [res[1] for res in cnt.items()]
            for index in range(len(cnt.creg_sizes)):
                measurement_for_variable = [a[index] for a in measurement_for_runs]
                Classical_registers = [reg for reg in self._classic_registers if reg.name == cnt.creg_sizes[index][0]]
                Classical_registers[0].measured_values = measurement_for_variable
                Classical_registers[0].measured_counts = counts_for_runs
        return cnt

    def run_circuit(self, circuit:QuantumCircuit, repetition:int = 1, print_count:bool = False):
        self.__run__(circuit, repetition, print_count)
    
    def get_run_and_measure_results(self, quantum_registers : list[QuantumRegister] = None, classical_registers : list[ClassicalRegister] = None, repetition = 1, max_results = None, print_count:bool = False) -> tuple[list[str], list[ClassicalRegister]]:        
        quantum_registers = quantum_registers or self._quantum_registers
        classical_registers = self.push_measure_operation(quantum_registers, classical_registers)
        self.run_circuit(self.create_circuit(), repetition, print_count)
        # self._current_operation_stack.pop()

        for creg in classical_registers:
            [qreg for qreg in quantum_registers if qreg.name in creg.name][0].measured_classical_register = creg

        results = [reg.measured_values for reg in classical_registers]
        if(max_results is not None):
            results = results[:max_results]
        return (results, classical_registers)

    def run_and_measure(self, quantum_registers : list[QuantumRegister] = None, classical_registers : list[ClassicalRegister] = None, repetition = 1, max_results = 1, print_count:bool = False) -> list[ClassicalRegister]:        
        (_, classical_registers) = self.get_run_and_measure_results(quantum_registers, classical_registers, repetition, max_results, print_count)
        return classical_registers
    
    def get_run_and_measure_result_for_quantum_var(self, quantum_register : QuantumRegister, classical_register : ClassicalRegister = None, repetition = 1, max_results = 1, print_count:bool = False) -> tuple[str, ClassicalRegister]:        
        (_, classical_register) = self.get_run_and_measure_results([quantum_register], [classical_register] if classical_register != None else None, repetition, max_results, print_count)
        return (classical_register[0].measured_values[0], classical_register[0])

    def push_not_operation(self, quantum_register : QuantumRegister) -> None:
        self._current_operation_stack.append(lambda circuit : cast(QuantumCircuit, circuit).x(quantum_register))
    
    def push_cnot_operation(self, quantum_register_control : QuantumRegister, quantum_register_target : QuantumRegister) -> None:
        self._current_operation_stack.append(lambda circuit : cast(QuantumCircuit, circuit).cx(quantum_register_control, quantum_register_target))

    def push_pauliy_operation(self, quantum_register : QuantumRegister) -> None:
        self._current_operation_stack.append(lambda circuit : cast(QuantumCircuit, circuit).y(quantum_register))

    def push_pauliz_operation(self, quantum_register : QuantumRegister) -> None:
        self._current_operation_stack.append(lambda circuit : cast(QuantumCircuit, circuit).z(quantum_register))

    def push_MCZ_operation(self, quantum_registers : list[QuantumRegister] | list[QiskitQubit]) -> None:
        mcz_gate = MCMT(ZGate(), sum([1 if isinstance(q, QiskitQubit) else q.size for q in quantum_registers]) - 1, 1)
        self._current_operation_stack.append(lambda circuit : cast(QuantumCircuit, circuit).compose(mcz_gate, unwrap(quantum_registers), inplace=True))

    def push_MCX_operation(self, quantum_registers : list[QuantumRegister] | list[QiskitQubit]) -> None:
        mcx_gate = MCMT(XGate(), sum([1 if isinstance(q, QiskitQubit) else q.size for q in quantum_registers]) - 1, 1)        
        self._current_operation_stack.append(lambda circuit : cast(QuantumCircuit, circuit).compose(mcx_gate, unwrap(quantum_registers), inplace=True))

    def push_MCY_operation(self, quantum_registers : list[QuantumRegister] | list[QiskitQubit]) -> None:
        mcy_gate = MCMT(YGate(), sum([1 if isinstance(q, QiskitQubit) else q.size for q in quantum_registers]) - 1, 1)        
        self._current_operation_stack.append(lambda circuit : cast(QuantumCircuit, circuit).compose(mcy_gate, unwrap(quantum_registers), inplace=True))

    def push_MCP_operation(self, theta, quantum_registers : list[QuantumRegister] | list[QiskitQubit]) -> None:
        mcp_gate = MCMT(PhaseGate(theta), sum([1 if isinstance(q, QiskitQubit) else q.size for q in quantum_registers]) - 1, 1)        
        self._current_operation_stack.append(lambda circuit : cast(QuantumCircuit, circuit).compose(mcp_gate, unwrap(quantum_registers), inplace=True))

    def push_hadamard_operation(self, quantum_register : QuantumRegister) -> None:
        self._current_operation_stack.append(lambda circuit : cast(QuantumCircuit, circuit).h(quantum_register))

    def push_barrier_operation(self) -> None:
        self._current_operation_stack.append(lambda circuit : cast(QuantumCircuit, circuit).barrier())

    def push_swap_operation(self, quantum_register_a : QuantumRegister, quantum_register_b : QuantumRegister) -> None:
        self._current_operation_stack.append(lambda circuit : cast(QuantumCircuit, circuit).swap(quantum_register_a, quantum_register_b))

    def push_equals_operation(self, quantum_register_a : QuantumRegister, classical_value : Any) -> None:
        quantum_value : Qubit | Quint | Qustring = QutesDataType.promote_classical_to_quantum_value(classical_value)
        for index in range(len(quantum_register_a)):
            if(len(quantum_value.qubit_state) > index):
                qubit = quantum_value.qubit_state[-1-index]
                if(qubit.alpha == 1 and qubit.beta == 0):
                    self.push_not_operation(quantum_register_a[index])
            else:
                self.push_not_operation(quantum_register_a[index])

    def push_reset_operation(self, quantum_register : QuantumRegister) -> None:
        self._current_operation_stack.append(lambda circuit : cast(QuantumCircuit, circuit).reset(quantum_register))

    def push_compose_circuit_operation(self, circuit_to_compose : QuantumCircuit, quantum_registers : list[QuantumRegister] = None, classical_registers : list[ClassicalRegister] = []) -> None:
        if(quantum_registers == None):
            quantum_registers = self._quantum_registers
        self._current_operation_stack.append(lambda circuit: circuit.compose(circuit_to_compose, unwrap(quantum_registers), unwrap(classical_registers), inplace=True))

    def push_measure_operation(self, quantum_registers : list[QuantumRegister] = None, classical_registers : list[ClassicalRegister] = None) -> list[ClassicalRegister]:
        if(quantum_registers == None):
            quantum_registers = self._quantum_registers

        if(classical_registers == None):
            classical_registers = []
            for quantum_register in quantum_registers:
                classic_register_name = "measured_"+quantum_register.name
                search = [reg for reg in self._classic_registers if reg.name == classic_register_name]
                already_exists = any(search)
                if(not already_exists):
                    classic_register = self.declare_classical_register(classic_register_name, len(quantum_register))
                else:
                    classic_register = search[0]
                classical_registers.append(classic_register)
        
        self._current_operation_stack.append(lambda circuit : cast(QuantumCircuit, circuit).measure(unwrap(quantum_registers), unwrap(classical_registers)))
        return classical_registers
    
    def push_ESM_operation(self, input:QuantumRegister, rotation_register:QuantumRegister, to_match, phase_kickback_ancilla = None) -> None:
        array_len = len(input)
        to_match_len = len(to_match.qubit_state)
        block_size = Qustring.default_char_size
        logn = max(int(math.log2(array_len/block_size)),1)

        # rotate input array
        from quantum_circuit.qutes_gates import QutesGates
        for i in range(logn):
            self.push_compose_circuit_operation(QutesGates.crot(array_len, 2**i, block_size), [rotation_register[i], *input])

        # compare x and y[:m]
        self.push_equals_operation(input[:to_match_len], to_match)
        if(phase_kickback_ancilla == None):
            self.push_MCZ_operation([*input[:to_match_len]])
        else:
            self.push_MCZ_operation([*input[:to_match_len], phase_kickback_ancilla])

        self.push_equals_operation(input[:to_match_len], to_match)

        for i in range(logn)[::-1]:
            self.push_compose_circuit_operation(QutesGates.crot(array_len,2**i,Qustring.default_char_size).inverse(), [rotation_register[i], *input])
        
    grover_count = iter(range(1, 1000))
    # It expects the register to put the result into to be the last one in the list
    def push_grover_operation(self, *oracle_registers, quantum_function:QuantumCircuit, register_involved_indexes, dataset_size, n_results = 1, verbose:bool = False) -> QuantumRegister:
        current_grover_count = next(self.grover_count)
        grover_op = GroverOperator(quantum_function, reflection_qubits=register_involved_indexes, insert_barriers=True, name=f"Grover{current_grover_count}")

        if(verbose):
            self.print_circuit(quantum_function)
            self.print_circuit(grover_op.decompose())
        
        n_iteration = math.floor(
            (math.pi / 4) * math.sqrt(dataset_size / n_results)
        )
        if(verbose):
            print(f"Grover iterations: {n_iteration}")

        self.push_compose_circuit_operation(grover_op.power(n_iteration), oracle_registers)

        # Make the Z Controlled Oracle a X Controlled Oracle
        self.push_barrier_operation()
        boolean_quantum_function = quantum_function.copy()
        for index, instruction in enumerate(boolean_quantum_function.data):
            if(isinstance(instruction, CircuitInstruction)):
                name : str = instruction.operation.name
                op = instruction.operation
                if(name.startswith("c") and name.endswith("z")):
                    boolean_quantum_function.data[index] = CircuitInstruction(MCXGate(op.num_qubits), [*instruction.qubits,*oracle_registers[-1]], instruction.clbits)
        
        # check if the grover result is actually a hit.
        oracle_result = self.declare_quantum_register(f"oracle_phase_ancilla_{current_grover_count}", Qubit())
        self.push_compose_circuit_operation(boolean_quantum_function, [*oracle_registers[:-1],oracle_result])
        return oracle_result