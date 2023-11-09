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
        self.classic_registers : list[ClassicalRegister] = [] 
        self.operation_stack : list[(QuantumGates, list[QuantumRegister])] = [] 
        self.varname_to_register : dict[str, QuantumRegister] = {} 

    def declare_variable(self,  variable_name : str, quantum_variable : any) -> QuantumRegister:
        new_register = None
        if(isinstance(quantum_variable, Qubit)):
            new_register = QuantumRegister(1, variable_name)
        if(isinstance(quantum_variable, Quint)):
            new_register = QuantumRegister(quantum_variable.size, variable_name)

        if(new_register is None):
            raise SystemError("Error trying to declare a quantum variable of unsupported type")

        #TODO: init with actual value

        self.varname_to_register[variable_name] = new_register
        self.quantum_registers.append(new_register)
        return new_register
    
    def udpate_variable(self,  variable_name : str, quantum_variable : any) -> None:
        register_to_update = self.varname_to_register[variable_name]
        if(register_to_update is None):
            raise SystemError("Error trying to update an undeclared quantum variable")

        #TODO: update with actual value
        if(isinstance(quantum_variable, Qubit)):
            pass
            #register_to_update = QuantumRegister(1, variable_name)
        if(isinstance(quantum_variable, Quint)):
            pass
            #register_to_update = QuantumRegister(quantum_variable.size, variable_name)

        return register_to_update
    
    def print_circuit(self):
        circuit = QuantumCircuit(*self.quantum_registers, *self.classic_registers)
        for (operation, registers) in self.operation_stack:
            if(operation == QuantumGates.X):
                circuit.x(*registers)
            if(operation == QuantumGates.Y):
                circuit.y(*registers)
            if(operation == QuantumGates.Z):
                circuit.z(*registers)
            if(operation == QuantumGates.H):
                circuit.h(*registers)
        print(circuit.draw())

    def push_not_operation(self, QuantumRegister) -> None:
        self.operation_stack.append((QuantumGates.X, [QuantumRegister]))

    def push_pauliy_operation(self, QuantumRegister) -> None:
        self.operation_stack.append((QuantumGates.Y, [QuantumRegister]))
    
    def push_pauliz_operation(self, QuantumRegister) -> None:
        self.operation_stack.append((QuantumGates.Z, [QuantumRegister]))
    
    def push_hadamard_operation(self, QuantumRegister) -> None:
        self.operation_stack.append((QuantumGates.H, [QuantumRegister]))
    