from typing import TypeVar
from symbols.types import QuantumType
from symbols.types.qubit import Qubit

T = TypeVar("T")

class QuantumArrayType(QuantumType[T]):
    def __init__(self, unit_class_type: QuantumType[T], array:list['Symbol']):
        super().__init__(QuantumArrayType, sum([a.value.size for a in array]))
        self.unit_class_type = unit_class_type
        self.array:list['Symbol'] = array
        self.size = sum([a.value.size for a in array])

    @staticmethod
    def get_default_value():
        return QuantumArrayType(Qubit, [Qubit.get_default_value()])

    @staticmethod
    def get_default_superposition_value():
        return QuantumArrayType(Qubit, [Qubit.get_default_superposition_value()])

    @staticmethod
    def get_default_size_in_qubit():
        return Qubit.get_default_size_in_qubit()

    def __to_printable__(self) -> str:
        return f"{self.unit_class_type.__name__}[{self.size}]"