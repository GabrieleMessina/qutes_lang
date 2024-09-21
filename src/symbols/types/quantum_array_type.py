from typing import TypeVar
from symbols.types import QuantumType
from symbols.types.qubit import Qubit

T = TypeVar("T")

class QuantumArrayType(QuantumType[T]):
    def __init__(self, unit_type: QuantumType[T], array:list['Symbol']):
        super().__init__(unit_type, sum([a.value.size for a in array]))
        self.unit_type = unit_type
        self.array = array
        self.size = sum([a.value.size for a in array])

    def get_default_value():
        return QuantumArrayType(Qubit, [Qubit.get_default_value()])
    
    def get_default_superposition_value():
        return QuantumArrayType(Qubit, [Qubit.get_default_superposition_value()])
    
    def get_default_size_in_qubit():
        return Qubit.get_default_size_in_qubit()

    def __to_printable__(self) -> str:
        return f"{self.unit_type.__name__}[{self.size}]"