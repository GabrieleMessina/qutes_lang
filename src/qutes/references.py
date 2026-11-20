"""Construction-time locations and array identities, never quantum state copies."""

from dataclasses import dataclass
from qutes import ir


@dataclass(eq=False)
class Cell:
    value: ir.Expression


@dataclass(eq=False)
class ArrayObject:
    elements: list[ir.Expression]
    backing: ir.Expression | None = None


@dataclass(frozen=True)
class ArrayView:
    owner: ArrayObject
    positions: tuple[int, ...]
    readonly: bool = False

    @property
    def elements(self):
        return tuple(self.owner.elements[i] for i in self.positions)


@dataclass(eq=False)
class ElementCell:
    owner: ArrayObject
    index: int

    @property
    def value(self):
        return self.owner.elements[self.index]

    @value.setter
    def value(self, value):
        self.owner.elements[self.index] = value
