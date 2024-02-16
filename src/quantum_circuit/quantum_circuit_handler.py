from typing import Any, Callable, cast
from quantum_circuit.classical_register import ClassicalRegister
from quantum_circuit.quantum_circuit import QuantumCircuit
from quantum_circuit.quantum_register import QuantumRegister
from symbols.types import Qubit, Quint, Qustring
from qiskit import IBMQ, Aer, transpile

class QuantumCircuitHandler():
    def __init__(self):
        self._quantum_registers : list[QuantumRegister] = []
        self._registers_states : dict[QuantumRegister | ClassicalRegister, list[complex] | str | None] = {}
        self._classic_registers : list[ClassicalRegister] = []
        self._operation_stack : list[Callable[[QuantumCircuit], None]] = []
        self._varname_to_register : dict[str, QuantumRegister] = {}

    def declare_classical_register(self,  variable_name : str, bits_number : int) -> ClassicalRegister:
        new_register = ClassicalRegister(bits_number, variable_name)
        self._varname_to_register[variable_name] = new_register
        self._classic_registers.append(new_register)
        return new_register

    def delete_classical_register(self,  variable_name : str) -> None:
        register = self._varname_to_register[variable_name]
        self._classic_registers.remove(register)

    def declare_quantum_register(self,  variable_name : str, quantum_variable : any) -> QuantumRegister:
        new_register = None

        new_register = QuantumRegister(1, variable_name, quantum_variable)

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
        if(isinstance(quantum_variable, Qubit)):
            pass
        if(isinstance(quantum_variable, Quint) or isinstance(quantum_variable, Qustring)):
            #TODO-CRITICAL: this update actually change the reference, so all the old references around the code are still there. For now i hack this returning the new value and changing the name from update to replace.
            #Delete old quantum register and reference
            del self._registers_states[register_to_update]
            self._quantum_registers.remove(register_to_update)
            #Add new quantum register
            register_to_update = self._varname_to_register[variable_name] = QuantumRegister(quantum_variable.size, variable_name, quantum_variable)
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

        return register_to_update

    def create_circuit(self) -> QuantumCircuit:
        circuit = QuantumCircuit(*self._quantum_registers, *self._classic_registers)
        for register in self._quantum_registers:
            # circuit.initialize('01', register, True)
            # circuit.initialize([0, 1/np.sqrt(2), -1.j/np.sqrt(2), 0], register, True)
            circuit.initialize(self._registers_states[register], register, True)

        circuit.barrier()

        for operation in self._operation_stack:
            operation(circuit)

        circuit.barrier()
        return circuit

    def print_circuit(self, circuit:QuantumCircuit):
        print(circuit.draw())

    def __counts__(self, vec):
        for i in vec:
                print(" - " + str(i) +" : "+ str(vec[i]))

    def __revcounts__(self, vec):
        for i in vec:
                print(" - " + str(i)[::-1] +" : "+ str(vec[i]))

    # simulate the execution of a Quantum Circuit and get the results
    def __run__(self, circuit, shots):
        # Use Aer's qasm_simulator
        simulator = Aer.get_backend('aer_simulator')

        # compile the circuit down to low-level QASM instructions
        # supported by the backend (not needed for simple circuits)
        compiled_circuit = transpile(circuit, simulator)

        # Execute the circuit on the qasm simulator
        job = simulator.run(compiled_circuit, shots=shots)
        
        # Grab results from the job
        result = job.result()  
        cnt = result.get_counts(compiled_circuit)
        return cnt

    def run_circuit(self, circuit:QuantumCircuit, repetition:int = 1, max_results = 1) -> list[str]:
        try:
            cnt = self.__run__(circuit, repetition)
            self.__revcounts__(cnt)
            result_with_max_count = [key for key, value in cnt.items() if value == max(cnt.values())]
            return result_with_max_count[:max_results]
        except Exception as ex:
            print(ex)


    def push_not_operation(self, quantum_register : QuantumRegister) -> None:
        self._operation_stack.append(lambda circuit : cast(QuantumCircuit, circuit).x(quantum_register))
    
    def push_cnot_operation(self, quantum_register_control : QuantumRegister, quantum_register_target : QuantumRegister) -> None:
        self._operation_stack.append(lambda circuit : cast(QuantumCircuit, circuit).cx(quantum_register_control, quantum_register_target))

    def push_pauliy_operation(self, quantum_register : QuantumRegister) -> None:
        self._operation_stack.append(lambda circuit : cast(QuantumCircuit, circuit).y(quantum_register))

    def push_pauliz_operation(self, quantum_register : QuantumRegister) -> None:
        self._operation_stack.append(lambda circuit : cast(QuantumCircuit, circuit).z(quantum_register))

    def push_hadamard_operation(self, quantum_register : QuantumRegister) -> None:
        self._operation_stack.append(lambda circuit : cast(QuantumCircuit, circuit).h(quantum_register))

    def push_barrier_operation(self) -> None:
        self._operation_stack.append(lambda circuit : cast(QuantumCircuit, circuit).barrier())

    def push_swap_operation(self, quantum_register_a : QuantumRegister, quantum_register_b : QuantumRegister) -> None:
        self._operation_stack.append(lambda circuit : cast(QuantumCircuit, circuit).swap(quantum_register_a, quantum_register_b))

    def push_reset_operation(self, quantum_register : QuantumRegister) -> None:
        self._operation_stack.append(lambda circuit : cast(QuantumCircuit, circuit).reset(quantum_register))

    def push_compose_circuit_operation(self, circuit_to_compose : QuantumCircuit, quantum_registers : QuantumRegister, classical_registers : ClassicalRegister = None) -> None:
        self._operation_stack.append(lambda circuit: circuit.compose(circuit_to_compose, quantum_registers, classical_registers, inplace=True))

    def push_measure_operation(self, quantum_registers : QuantumRegister, classical_registers : ClassicalRegister = None) -> None:
        if(classical_registers != None):
            self._operation_stack.append(lambda circuit : cast(QuantumCircuit, circuit).measure(quantum_registers, classical_registers))
            return
        
        classic_register_name = "measured_"+quantum_registers.name
        classic_register = [reg for reg in self._classic_registers if reg.name == classic_register_name]
        if(not any(classic_register)):
            classic_register.append(self.declare_classical_register(classic_register_name, quantum_registers.size))
        self._operation_stack.append(lambda circuit : cast(QuantumCircuit, circuit).measure(quantum_registers, classic_register[0]))

    def run_and_measure(self, quantum_registers : QuantumRegister) -> str:        
        self.push_measure_operation(quantum_registers)
        result = self.run_circuit(self.create_circuit())[0].replace(' ', '')
        self._operation_stack.pop()
        return result
