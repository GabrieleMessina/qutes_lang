from typing import TypeVar
from symbols.types import QuantumType

T = TypeVar("T")

class ClassicalArrayType(list[T]):
    def __init__(self, unit_type: QuantumType[T], array:list['Symbol']):
        super().__init__([a.value for a in array])
        self.unit_type = unit_type
        self.array = array
        self.size = len(array)

    def __to_printable__(self) -> str:
        return f"{self.unit_type.__name__}[{self.size}]"