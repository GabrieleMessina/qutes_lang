from typing import TypeVar, Type
from symbols.types import QuantumType

T = TypeVar("T")

class QuantumArrayType(QuantumType[T]):
    def __init__(self, unit_type: Type[T]):
        super().__init__(unit_type)
        self.unit_type = unit_type