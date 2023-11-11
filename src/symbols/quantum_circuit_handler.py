from symbols.qutes_types import Qubit, Quint
from qiskit import QuantumCircuit as qc, QuantumRegister as qr, ClassicalRegister as cr
from typing import cast, Callable
from utils.QiskitUtils import run, counts

class QuantumRegister(qr):
    def __init__(self, size, var_name, value):
        super().__init__(size, var_name)
        self.value = value

class ClassicalRegister(cr):
    pass

class QuantumCircuit(qc):
    pass

class QuantumCircuitHandler():

    def __init__(self):
        self._quantum_registers : list[QuantumRegister] = []
        self._registers_states : dict[QuantumRegister | ClassicalRegister, list[complex] | str | None] = {}
        self._classic_registers : list[ClassicalRegister] = [] 
        self._operation_stack : list[Callable[[QuantumCircuit], None]] = []
        self._varname_to_register : dict[str, QuantumRegister] = {} 

    def declare_quantum_register(self,  variable_name : str, quantum_variable : any) -> QuantumRegister:
        new_register = None

        if(isinstance(quantum_variable, Qubit)):
            new_register = QuantumRegister(1, variable_name, quantum_variable)
        if(isinstance(quantum_variable, Quint)):
            new_register = QuantumRegister(quantum_variable.size, variable_name, quantum_variable)

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

        if(isinstance(quantum_variable, Qubit)):
            pass
        if(isinstance(quantum_variable, Quint)):
            #TODO-CRITICAL: this update actually change the reference, so all the old references around the code are still there. For now i hack this returning the new value and changing the name from update to replace.
            #Delete old quantum register and reference
            del self._registers_states[register_to_update]
            self._quantum_registers.remove(register_to_update)
            #Add new quantum register
            register_to_update = self._varname_to_register[variable_name] = QuantumRegister(quantum_variable.size, variable_name, quantum_variable)
            self._quantum_registers.append(register_to_update)

        self._registers_states[register_to_update] = quantum_variable.get_quantum_state()
        return register_to_update

    # def declare_classical_register(self,  variable_name : str, classical_variable : any) -> QuantumRegister:
    #     new_value = int(classical_variable)
    #     new_register = ClassicalRegister(len(new_value))

    #     #TODO: check that the cast to int actually worked
    #     if(new_register is None):
    #         raise SystemError("Error trying to declare a quantum variable of unsupported type")

    #     self._varname_to_register[variable_name] = new_register
    #     self._classic_registers.append(new_register)
    #     self._registers_states[new_register] = bin(new_value).removeprefix("0b")
    #     return new_register
    

    # def udpate_quantum_register(self,  variable_name : str, classical_variable : any) -> None:
    #     new_value = int(classical_variable)
    #     new_register = ClassicalRegister(len(new_value))
    #     register_to_update = self._varname_to_register[variable_name]
    #     if(register_to_update is None):
    #         raise SystemError("Error trying to update an undeclared classical register")

    #     #Delete old register and reference
    #     del self._registers_states[register_to_update]
    #     self._classic_registers.remove(register_to_update)
    #     #Add new quantum register
    #     register_to_update = self._varname_to_register[variable_name] = new_register
    #     self._classic_registers.append(register_to_update)

    #     self._registers_states[register_to_update] = bin(new_value).removeprefix("0b")

    def print_circuit(self):
        circuit = QuantumCircuit(*self._quantum_registers, *self._classic_registers)
        for register in self._quantum_registers:
            # circuit.initialize('01', register, True)
            # circuit.initialize([0, 1/np.sqrt(2), -1.j/np.sqrt(2), 0], register, True)
            circuit.initialize(self._registers_states[register], register, True)
        
        circuit.barrier()

        for operation in self._operation_stack:
            operation(circuit)
        
        circuit.barrier()
        
        print(circuit.draw())

        # cnt = run(circuit,100)
        # counts(cnt)

    def push_not_operation(self, quantum_register : QuantumRegister) -> None:
        self._operation_stack.append(lambda circuit : cast(QuantumCircuit, circuit).x(quantum_register))

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

    def push_compose_circuit_operation(self, circuit_to_compose, quantum_registers, classical_registers = None) -> None:
        self._operation_stack.append(lambda circuit: circuit.compose(circuit_to_compose, quantum_registers, classical_registers, inplace=True))

    def push_measure_operation(self, quantum_registers, classical_register) -> None:
        self._operation_stack.append(lambda circuit : cast(QuantumCircuit, circuit).measure(quantum_registers, classical_register))