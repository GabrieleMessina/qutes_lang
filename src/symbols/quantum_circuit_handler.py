from symbols.qutes_types import Qubit, Quint
from qiskit import QuantumCircuit, QuantumRegister as qr, ClassicalRegister as cr
from typing import cast, Callable
from utils.QiskitUtils import run, counts

class QuantumRegister(qr):
    pass

class ClassicalRegister(cr):
    pass

class QuantumCircuitHandler():

    def __init__(self):
        self.quantum_registers : list[QuantumRegister] = []
        self.quantum_registers_states : dict[QuantumRegister, list[complex] | str | None] = {}
        self.classic_registers : list[ClassicalRegister] = [] 
        self.operation_stack : list[Callable[[QuantumCircuit], None]] = []
        self.varname_to_register : dict[str, QuantumRegister] = {} 

    def declare_variable(self,  variable_name : str, quantum_variable : any) -> QuantumRegister:
        new_register = None
        if(isinstance(quantum_variable, Qubit)):
            new_register = QuantumRegister(1, variable_name)
        if(isinstance(quantum_variable, Quint)):
            new_register = QuantumRegister(quantum_variable.size, variable_name)

        if(new_register is None):
            raise SystemError("Error trying to declare a quantum variable of unsupported type")

        self.varname_to_register[variable_name] = new_register
        self.quantum_registers.append(new_register)
        self.quantum_registers_states[new_register] = quantum_variable.get_quantum_state()
        return new_register
    
    def udpate_variable(self,  variable_name : str, quantum_variable : any) -> None:
        register_to_update = self.varname_to_register[variable_name]
        if(register_to_update is None):
            raise SystemError("Error trying to update an undeclared quantum variable")

        if(isinstance(quantum_variable, Qubit)):
            pass
        if(isinstance(quantum_variable, Quint)):
            #Delete old quantum register and reference
            del self.quantum_registers_states[register_to_update]
            self.quantum_registers.remove(register_to_update)
            #Add new quantum register
            register_to_update = self.varname_to_register[variable_name] = QuantumRegister(quantum_variable.size, variable_name)
            self.quantum_registers.append(register_to_update)

        self.quantum_registers_states[register_to_update] = quantum_variable.get_quantum_state()

    def print_circuit(self):
        circuit = QuantumCircuit(*self.quantum_registers, *self.classic_registers)
        for register in self.quantum_registers:
            # circuit.initialize('01', register, True)
            # circuit.initialize([0, 1/np.sqrt(2), -1.j/np.sqrt(2), 0], register, True)
            circuit.initialize(self.quantum_registers_states[register], register, True)
        
        circuit.barrier()

        for operation in self.operation_stack:
            operation(circuit)
        
        circuit.barrier()
        
        print(circuit.draw())

        cnt = run(circuit,100)
        counts(cnt)

    def push_not_operation(self, quantum_register : QuantumRegister) -> None:
        self.operation_stack.append(lambda circuit : cast(QuantumCircuit, circuit).x(quantum_register))

    def push_pauliy_operation(self, quantum_register : QuantumRegister) -> None:
        self.operation_stack.append(lambda circuit : cast(QuantumCircuit, circuit).y(quantum_register))
    
    def push_pauliz_operation(self, quantum_register : QuantumRegister) -> None:
        self.operation_stack.append(lambda circuit : cast(QuantumCircuit, circuit).z(quantum_register))
    
    def push_hadamard_operation(self, quantum_register : QuantumRegister) -> None:
        self.operation_stack.append(lambda circuit : cast(QuantumCircuit, circuit).h(quantum_register))

    def push_barrier_operation(self) -> None:
        self.operation_stack.append(lambda circuit : cast(QuantumCircuit, circuit).barrier())

    def push_swap_operation(self, quantum_register_a : QuantumRegister, quantum_register_b : QuantumRegister) -> None:
        self.operation_stack.append(lambda circuit : cast(QuantumCircuit, circuit).swap(quantum_register_a, quantum_register_b))

    def push_reset_operation(self, quantum_register : QuantumRegister) -> None:
        self.operation_stack.append(lambda circuit : cast(QuantumCircuit, circuit).reset(quantum_register))

    def push_compose_circuit_operation(self, circuit_to_compose, quantum_registers, classical_registers = None) -> None:
        self.operation_stack.append(lambda circuit : cast(QuantumCircuit, circuit).compose(circuit_to_compose, quantum_registers, classical_registers))

    def push_measure_operation(self, quantum_registers, classical_register) -> None:
        self.operation_stack.append(lambda circuit : cast(QuantumCircuit, circuit).measure(quantum_registers, classical_register))
