from typing import Generic, TypeVar, Type
from quantum_circuit.state_preparation import StatePreparation

T = TypeVar("T")

class QuantumType(Generic[T]):
    def __init__(self, t_type: Type[T], size: int):
        self.t_type = t_type
        self.size = size
        self.qubit_state = StatePreparation("")

    def get_default_value():
        raise NotImplementedError("get_default_value method must be implemented in derived class")
    
    def get_default_superposition_value():
        raise NotImplementedError("get_default_superposition_value method must be implemented in derived class")
    
    def get_default_size_in_qubit():
        raise NotImplementedError("get_default_size_in_qubit method must be implemented in derived class")
    
    def __eq__(self, other):
        if isinstance(other, QuantumType):
            return self.qubit_state == other.qubit_state
        return False

    def __to_printable__(self) -> str:
        raise NotImplementedError("__to_printable__ method must be implemented in derived class")

    def __str__(self) -> str:
        return self.__to_printable__()

    def __repr__(self) -> str:
        return self.__to_printable__()