"""Structured typed IR, independent of syntax trees, storage allocation, and Qiskit."""

from __future__ import annotations

from dataclasses import dataclass, fields, is_dataclass
from enum import StrEnum
from typing import Any

from qutes.config import CompilerConfig
from qutes.diagnostics import Span


class Stage(StrEnum):
    STATIC = "construction"
    QUANTUM = "quantum"
    RUNTIME = "runtime-classical"


QUANTUM_TO_CLASSICAL = {"qubit": "bool", "quint": "int", "quchar": "char", "qustring": "string"}


@dataclass(frozen=True)
class Type:
    name: str
    array: bool = False

    @property
    def quantum(self) -> bool:
        return self.name in QUANTUM_TO_CLASSICAL

    @property
    def classical(self) -> Type:
        return Type(QUANTUM_TO_CLASSICAL.get(self.name, self.name), self.array)

    @property
    def element(self) -> Type:
        if self.array:
            return Type(self.name)
        if self.name in {"string", "qustring"}:
            return Type("quchar" if self.quantum else "char")
        raise ValueError("type is not indexable")

    def __str__(self) -> str:
        return self.name + ("[]" if self.array else "")


@dataclass(frozen=True)
class Symbol:
    id: int
    name: str
    type: Type
    readonly: bool
    span: Span


@dataclass(frozen=True)
class Expression:
    span: Span
    type: Type
    stage: Stage
    op: str
    arguments: tuple[Expression, ...] = ()
    value: Any = None
    symbol: Symbol | None = None
    known: bool = False
    shape: int | None = None
    dependencies: frozenset[int] = frozenset()
    effects: frozenset[str] = frozenset()
    presentation: str | None = None


@dataclass(frozen=True)
class Block:
    span: Span
    statements: tuple[Statement, ...]
    returns: bool = False


@dataclass(frozen=True)
class Statement:
    span: Span
    op: str
    expressions: tuple[Expression, ...] = ()
    blocks: tuple[Block, ...] = ()
    symbol: Symbol | None = None
    operator: str | None = None
    source_name: str | None = None
    aliases: tuple[tuple[str, Expression], ...] = ()


@dataclass(frozen=True)
class Function:
    span: Span
    key: str
    name: str
    parameters: tuple[Symbol, ...]
    return_type: Type
    return_stage: Stage
    return_shape: int | None
    body: Block
    effects: frozenset[str]


@dataclass(frozen=True)
class Program:
    span: Span
    config: CompilerConfig
    functions: tuple[Function, ...]
    entry: str
    validated: tuple[str, ...] = ("names", "types", "stages", "effects")
    cleanup_verified: bool = False
    globals: tuple[Symbol, ...] = ()
    inputs: tuple[Symbol, ...] = ()


def to_dict(value: Any) -> Any:
    if is_dataclass(value):
        return {field.name: to_dict(getattr(value, field.name)) for field in fields(value)}
    if isinstance(value, (tuple, frozenset)):
        sequence = sorted(value) if isinstance(value, frozenset) else value
        return [to_dict(item) for item in sequence]
    return value
