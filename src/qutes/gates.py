"""Backend-independent reversible operations with explicit bit ordering.

Bit tuples are least-significant first. Controls are (bit, required_value).
These operations never measure, reset, or discard quantum information.
"""

from __future__ import annotations

from dataclasses import dataclass, replace

from qutes.diagnostics import Span


@dataclass(frozen=True)
class Gate:
    kind: str
    targets: tuple[int, ...]
    inputs: tuple[int, ...] = ()
    amount: int = 0
    controls: tuple[tuple[int, bool], ...] = ()
    inverse: bool = False
    span: Span | None = None

    def __post_init__(self):
        if self.kind not in {"x", "h", "copy", "add", "add_constant", "rotate"}:
            raise ValueError(f"unknown reversible operation {self.kind}")
        if not self.targets or len(set(self.targets)) != len(self.targets):
            raise ValueError("operation needs distinct target bits")
        if len(set(self.inputs)) != len(self.inputs):
            raise ValueError("operation needs distinct input bits")
        if self.kind in {"copy", "add"}:
            if len(self.inputs) != len(self.targets):
                raise ValueError("input and target widths differ")
        elif self.inputs:
            raise ValueError("operation does not take input bits")
        control_bits = tuple(bit for bit, _ in self.controls)
        if len(set(control_bits)) != len(control_bits):
            raise ValueError("controls must be normalized")
        if set(self.targets) & (set(self.inputs) | set(control_bits)):
            raise ValueError("read operands overlap a mutation target")
        if any(type(bit) is not int or bit < 0 for bit in (*self.targets, *self.inputs, *control_bits)):
            raise ValueError("bit identifiers must be nonnegative integers")
        if any(type(value) is not bool for _, value in self.controls):
            raise ValueError("control values must be Boolean")
        if type(self.amount) is not int:
            raise ValueError("operation amount must be an integer")

    @property
    def reads(self) -> frozenset[int]:
        return frozenset(self.inputs) | frozenset(bit for bit, _ in self.controls)

    @property
    def bits(self) -> frozenset[int]:
        return self.reads | frozenset(self.targets)

    def adjoint(self) -> Gate:
        return replace(self, inverse=not self.inverse)


def inverse(gates: tuple[Gate, ...] | list[Gate]) -> tuple[Gate, ...]:
    return tuple(gate.adjoint() for gate in reversed(gates))


def controlled(gate: Gate, controls: tuple[tuple[int, bool], ...]) -> Gate | None:
    """Merge controls; a contradictory conjunction is an identity operation."""
    merged = dict(gate.controls)
    for bit, value in controls:
        if bit in merged and merged[bit] != value:
            return None
        merged[bit] = value
    return replace(gate, controls=tuple(sorted(merged.items())))
