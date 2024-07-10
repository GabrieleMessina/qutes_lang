from typing import TypeVar
from symbols.types import QuantumType

T = TypeVar("T")

class QuantumArrayType(QuantumType[T]):
    def __init__(self) -> None:
        pass 