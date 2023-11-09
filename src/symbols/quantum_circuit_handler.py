from symbols.qutes_types import Qubit, Quint
from qiskit import QuantumCircuit, QuantumRegister as qr, ClassicalRegister as cr
from enum import Enum

class QuantumRegister(qr):
    pass

class ClassicalRegister(cr):
    pass

class QuantumGates(Enum):
    X = 0
    Y = 1
    Z = 2
    H = 3


class QuantumCircuitHandler():

    def __init__(self):
        self.quantum_registers : list[QuantumRegister] = []
        self.quantum_registers_values : dict[QuantumRegister, list[float] | None] = {}
        self.classic_registers : list[ClassicalRegister] = [] 
        self.operation_stack : list[(QuantumGates, list[QuantumRegister])] = [] 
        self.varname_to_register : dict[str, QuantumRegister] = {} 

    def declare_variable(self,  variable_name : str, quantum_variable : any) -> QuantumRegister:
        new_register = None
        initial_state = None,
        if(isinstance(quantum_variable, Qubit)):
            new_register = QuantumRegister(1, variable_name)
            initial_state = [quantum_variable.alpha, quantum_variable.beta]
        if(isinstance(quantum_variable, Quint)):
            new_register = QuantumRegister(quantum_variable.size, variable_name)
            initial_state = None #TODO: What goes here?

        if(new_register is None):
            raise SystemError("Error trying to declare a quantum variable of unsupported type")

        self.varname_to_register[variable_name] = new_register
        self.quantum_registers.append(new_register)
        self.quantum_registers_values[new_register] = initial_state
        return new_register
    
    def udpate_variable(self,  variable_name : str, quantum_variable : any) -> None:
        register_to_update = self.varname_to_register[variable_name]
        if(register_to_update is None):
            raise SystemError("Error trying to update an undeclared quantum variable")

        if(isinstance(quantum_variable, Qubit)):
            updated_state = [quantum_variable.alpha, quantum_variable.beta]
        if(isinstance(quantum_variable, Quint)):
            #TODO: handle quint update
            pass

        self.quantum_registers_values[register_to_update] = updated_state
    
    def print_circuit(self):
        circuit = QuantumCircuit(*self.quantum_registers, *self.classic_registers)
        for register in self.quantum_registers:
            circuit.initialize(self.quantum_registers_values[register], register, True)
        
        circuit.barrier()

        for (operation, registers) in self.operation_stack:
            if(operation == QuantumGates.X):
                circuit.x(*registers)
            if(operation == QuantumGates.Y):
                circuit.y(*registers)
            if(operation == QuantumGates.Z):
                circuit.z(*registers)
            if(operation == QuantumGates.H):
                circuit.h(*registers)
        
        circuit.barrier()
        
        print(circuit.draw())

    def push_not_operation(self, QuantumRegister) -> None:
        self.operation_stack.append((QuantumGates.X, [QuantumRegister]))

    def push_pauliy_operation(self, QuantumRegister) -> None:
        self.operation_stack.append((QuantumGates.Y, [QuantumRegister]))
    
    def push_pauliz_operation(self, QuantumRegister) -> None:
        self.operation_stack.append((QuantumGates.Z, [QuantumRegister]))
    
    def push_hadamard_operation(self, QuantumRegister) -> None:
        self.operation_stack.append((QuantumGates.H, [QuantumRegister]))
    