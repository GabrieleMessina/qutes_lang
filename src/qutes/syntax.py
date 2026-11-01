"""Immutable, untyped syntax tree. Every node retains a source span."""

from __future__ import annotations

from dataclasses import dataclass, fields, is_dataclass
from typing import Any

from qutes.diagnostics import Span


@dataclass(frozen=True)
class Node:
    span: Span


@dataclass(frozen=True)
class TypeRef(Node):
    name: str
    array: bool = False


@dataclass(frozen=True)
class Parameter(Node):
    type: TypeRef
    name: str


@dataclass(frozen=True)
class Expr(Node):
    pass


@dataclass(frozen=True)
class Literal(Expr):
    kind: str
    value: int | bool | str


@dataclass(frozen=True)
class Name(Expr):
    identifier: str


@dataclass(frozen=True)
class Unary(Expr):
    operator: str
    operand: Expr


@dataclass(frozen=True)
class Binary(Expr):
    operator: str
    left: Expr
    right: Expr


@dataclass(frozen=True)
class Group(Expr):
    expression: Expr


@dataclass(frozen=True)
class Call(Expr):
    callee: Expr
    arguments: tuple[Expr, ...]


@dataclass(frozen=True)
class Index(Expr):
    collection: Expr
    index: Expr


@dataclass(frozen=True)
class Member(Expr):
    receiver: Expr
    name: str


@dataclass(frozen=True)
class ArrayLiteral(Expr):
    elements: tuple[Expr, ...]


@dataclass(frozen=True)
class NewArray(Expr):
    element_type: TypeRef
    length: Expr


@dataclass(frozen=True)
class Stmt(Node):
    pass


@dataclass(frozen=True)
class Block(Stmt):
    statements: tuple[Stmt, ...]


@dataclass(frozen=True)
class Declaration(Stmt):
    type: TypeRef
    name: str
    initializer: Expr


@dataclass(frozen=True)
class Input(Stmt):
    type: TypeRef
    name: str


@dataclass(frozen=True)
class Assignment(Stmt):
    target: Expr
    operator: str
    value: Expr


@dataclass(frozen=True)
class Update(Stmt):
    target: Expr
    operator: str


@dataclass(frozen=True)
class ExpressionStatement(Stmt):
    expression: Expr


@dataclass(frozen=True)
class Return(Stmt):
    value: Expr | None


@dataclass(frozen=True)
class If(Stmt):
    condition: Expr
    then_block: Block
    otherwise: Block | "If" | None


@dataclass(frozen=True)
class While(Stmt):
    condition: Expr
    body: Block


@dataclass(frozen=True)
class For(Stmt):
    initializer: Stmt | None
    condition: Expr | None
    update: Stmt | None
    body: Block


@dataclass(frozen=True)
class Foreach(Stmt):
    type: TypeRef
    name: str
    collection: Expr
    body: Block


@dataclass(frozen=True)
class Function(Node):
    return_type: TypeRef
    name: str
    parameters: tuple[Parameter, ...]
    body: Block


@dataclass(frozen=True)
class Program(Node):
    functions: tuple[Function, ...]
    statements: tuple[Stmt, ...] = ()


def to_dict(value: Any) -> Any:
    if is_dataclass(value):
        result = {field.name: to_dict(getattr(value, field.name)) for field in fields(value)}
        if isinstance(value, Node):
            result = {"node": type(value).__name__, **result}
        return result
    if isinstance(value, tuple):
        return [to_dict(item) for item in value]
    return value
