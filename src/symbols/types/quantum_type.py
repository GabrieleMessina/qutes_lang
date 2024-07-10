from typing import Generic, TypeVar

T = TypeVar("T")

class QuantumType(Generic[T]):
    def __init__(self):
        pass

    def get_default_value():
        raise NotImplementedError("get_default_value method must be implemented in derived class")
    
    def get_default_superposition_value():
        raise NotImplementedError("get_default_superposition_value method must be implemented in derived class")
    
    def get_default_size_in_qubit():
        raise NotImplementedError("get_default_size_in_qubit method must be implemented in derived class")

    def __to_printable__(self) -> str:
        raise NotImplementedError("__to_printable__ method must be implemented in derived class")

    def __str__(self) -> str:
        return self.__to_printable__()

    def __repr__(self) -> str:
        return self.__to_printable__()