from typing import TypeVar, Type
from symbols.types.qutes_type import QutesType
from quantum_circuit.state_preparation import StatePreparation

T = TypeVar("T")

class QuantumType(QutesType[T]):
    def __init__(self, t_type: Type[T], size: int):
        super().__init__(t_type)
        self.size = size
        self.qubit_state = StatePreparation("")

    @staticmethod
    def get_default_superposition_value():
        raise NotImplementedError("get_default_superposition_value method must be implemented in derived class")

    @staticmethod
    def get_default_size_in_qubit():
        raise NotImplementedError("get_default_size_in_qubit method must be implemented in derived class")

    def __eq__(self, other):
        if isinstance(other, QuantumType):
            return self.qubit_state == other.qubit_state
        return False