"""Construction IR to verified circuit operations.

Current integration covers scalar qubit/quint arithmetic, scopes, inlined helpers,
expanded classical loops, and non-consuming measurement. Remaining source forms
produce an explicit diagnostic until their lowering is implemented.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from qutes import construction, ir
from qutes.cleanup import CleanupEvent, Scheduler, Storage
from qutes.config import CompilerConfig
from qutes.diagnostics import DiagnosticError, Span
from qutes.gates import Gate, Measurement
from qutes.values import SignedInteger


@dataclass(frozen=True)
class Result:
    type: ir.Type
    op: str
    arguments: tuple[Result, ...] = ()
    value: Any = None
    bits: tuple[int, ...] = ()

    def decode(self, memory: int):
        if self.op == "literal":
            return list(self.value) if self.type.array else self.value
        if self.op == "snapshot":
            encoded = sum(((memory >> bit) & 1) << index for index, bit in enumerate(self.bits))
            if self.type == ir.Type("bool"):
                return bool(encoded)
            if self.type == ir.Type("int"):
                return SignedInteger(len(self.bits)).decode(encoded)
            raise ValueError(f"unsupported snapshot type {self.type}")
        values = tuple(argument.decode(memory) for argument in self.arguments)
        if self.op == "array":
            return list(values)
        if self.op == "index":
            return values[0][values[1]]
        if self.op == "unary:!":
            return not values[0]
        if self.op.startswith("binary:"):
            a, b = values
            return {"==": lambda: a == b, "!=": lambda: a != b,
                    "<": lambda: a < b, "<=": lambda: a <= b,
                    ">": lambda: a > b, ">=": lambda: a >= b,
                    "&&": lambda: a and b, "||": lambda: a or b}[self.op[7:]]()
        raise ValueError(f"unsupported result operation {self.op}")


@dataclass(frozen=True)
class Allocation:
    id: int
    name: str
    bits: tuple[int, ...]
    released: bool
    span: Span


@dataclass(frozen=True)
class Program:
    config: CompilerConfig
    operations: tuple[Gate | Measurement, ...]
    qubit_count: int
    classical_bit_count: int
    allocations: tuple[Allocation, ...]
    cleanup_events: tuple[CleanupEvent, ...]
    result: Result
    cleanup_verified: bool = True

    def to_qiskit(self):
        from qutes.qiskit_backend import emit_operations
        return emit_operations(self.qubit_count, self.classical_bit_count, self.operations)


class Lowerer:
    def __init__(self, program: construction.Program):
        self.program = program
        self.config = program.typed.config
        self.scheduler = Scheduler(max_steps=self.config.max_evaluation_steps)
        self.bindings: dict[int, Storage | Result] = {}
        self.frames: list[set[int]] = [set()]

    def fail(self, node, message, code="Q2001"):
        raise DiagnosticError(code, message, node.span)

    def width(self, type_, node):
        if type_.array or type_.name not in {"qubit", "quint"}:
            self.fail(node, f"circuit lowering for {type_} is not implemented yet")
        return 1 if type_.name == "qubit" else self.config.quint_bits

    def reference(self, expression):
        if expression.op not in {"load", "move"}:
            self.fail(expression, f"circuit lowering for {expression.op} references is not implemented yet")
        value = self.bindings[expression.symbol.id]
        if not isinstance(value, Storage) or value.released:
            self.fail(expression, "quantum storage is unavailable", "Q3001")
        return value

    def constant(self, expression):
        if expression.op == "lift":
            return expression.arguments[0].value
        if expression.op == "literal":
            return expression.value
        return None

    def operand(self, expression):
        value = self.constant(expression)
        if value is not None:
            return int(value), ()
        if expression.op in {"load", "move"}:
            return self.reference(expression), ()
        value = self.create(expression, "$expression")
        return value, (value,)

    def copy_gates(self, target, source, span):
        if isinstance(source, int):
            selected = tuple(bit for index, bit in enumerate(target.bits) if (source >> index) & 1)
            return (Gate("x", selected, span=span),) if selected else ()
        return (Gate("copy", target.bits, source.bits, span=span),)

    def add_gates(self, target, source, span):
        if isinstance(source, int):
            return (Gate("add_constant", target.bits, amount=source, span=span),)
        if set(target.bits) & set(source.bits):
            raise DiagnosticError("Q3001", "addition operands overlap the updated variable; doubling cannot use an in-place adder", span)
        return (Gate("add", target.bits, source.bits, span=span),)

    def preparation(self, expression, target):
        op = expression.op
        constant = self.constant(expression)
        if constant is not None:
            return self.copy_gates(target, int(constant), expression.span), ()
        if op == "superposition":
            return (Gate("h", target.bits, span=expression.span),), ()
        if op in {"load", "move"}:
            return self.copy_gates(target, self.reference(expression), expression.span), ()
        if op == "binary:+":
            a, a_temps = self.operand(expression.arguments[0])
            b, b_temps = self.operand(expression.arguments[1])
            return (self.copy_gates(target, a, expression.span) + self.add_gates(target, b, expression.span),
                    a_temps + b_temps)
        if op in {"rotateLeft", "rotateRight", "unary:!"}:
            value, temporaries = self.operand(expression.arguments[0])
            gates = self.copy_gates(target, value, expression.span)
            if op == "unary:!":
                gates += (Gate("x", target.bits, span=expression.span),)
            else:
                amount = expression.arguments[1].value * (-1 if op == "rotateRight" else 1)
                gates += (Gate("rotate", target.bits, amount=amount, span=expression.span),)
            return gates, temporaries
        self.fail(expression, f"circuit lowering for {op} is not implemented yet")

    def create(self, expression, name):
        width = self.width(expression.type, expression)
        target = self.scheduler.allocate(width, name, expression.span)
        self.scheduler.tick(target, width)
        self.frames[-1].add(target.id)
        gates, temporaries = self.preparation(expression, target)
        self.scheduler.initialize(target, gates)
        self.release_temporaries(temporaries)
        return target

    def release_temporaries(self, temporaries):
        self.scheduler.release_scope({value.id for value in temporaries})

    def contains(self, expression, target):
        if expression.op in {"load", "move"} and expression.type.quantum:
            return self.reference(expression) is target
        return any(self.contains(argument, target) for argument in expression.arguments)

    def self_update(self, expression, target):
        op = expression.op
        if op in {"load", "move"} and self.reference(expression) is target:
            return (), ()
        if op == "binary:+":
            left, right = expression.arguments
            left_contains, right_contains = self.contains(left, target), self.contains(right, target)
            if left_contains != right_contains:
                inner, other = (left, right) if left_contains else (right, left)
                gates, temporaries = self.self_update(inner, target)
                source, more = self.operand(other)
                return gates + self.add_gates(target, source, expression.span), temporaries + more
        if op in {"rotateLeft", "rotateRight", "unary:!"}:
            gates, temporaries = self.self_update(expression.arguments[0], target)
            if op == "unary:!":
                return gates + (Gate("x", target.bits, span=expression.span),), temporaries
            amount = expression.arguments[1].value * (-1 if op == "rotateRight" else 1)
            return gates + (Gate("rotate", target.bits, amount=amount, span=expression.span),), temporaries
        self.fail(expression, "assignment overlaps its input and has no supported reversible update; use a distinct result variable", "Q3001")

    def runtime(self, expression):
        if expression is None:
            return Result(ir.Type("void"), "literal")
        if expression.op == "load":
            value = self.bindings[expression.symbol.id]
            if not isinstance(value, Result):
                self.fail(expression, "a quantum value requires explicit measurement")
            return value
        return Result(expression.type, expression.op,
                      tuple(self.runtime(argument) for argument in expression.arguments), expression.value)

    def block(self, block):
        for statement in block.statements:
            op = statement.op
            if op == "let":
                expression = statement.expressions[0]
                if expression.op == "measure":
                    source = self.reference(expression.arguments[0])
                    measurement = self.scheduler.measure(source)
                    value = Result(expression.type, "snapshot", bits=measurement.classical_bits)
                elif expression.op == "move":
                    value = self.reference(expression)
                elif expression.type.quantum:
                    value = self.create(expression, statement.symbol.name)
                else:
                    value = self.runtime(expression)
                self.bindings[statement.symbol.id] = value
            elif op == "assign":
                target_expression, expression = statement.expressions
                target = self.reference(target_expression)
                if self.contains(expression, target):
                    gates, temporaries = self.self_update(expression, target)
                    if gates:
                        self.scheduler.update(target, gates)
                else:
                    gates, temporaries = self.preparation(expression, target)
                    self.scheduler.overwrite(target, gates)
                self.release_temporaries(temporaries)
            elif op == "scope":
                self.frames.append(set())
                self.block(statement.blocks[0])
                escapes = set()
                for expression in statement.expressions:
                    # Nested return expressions can refer to more than one local.
                    for identifier in expression.dependencies:
                        value = self.bindings.get(identifier)
                        if isinstance(value, Storage):
                            escapes.add(value.id)
                owned = self.frames.pop()
                self.scheduler.release_scope(owned - escapes)
                self.frames[-1].update(owned & escapes)
            else:
                self.fail(statement, f"circuit lowering for {op} statements is not implemented yet")

    def run(self):
        self.block(self.program.body)
        result = self.runtime(self.program.result)
        scheduler = self.scheduler
        # Main's still-live values are circuit outputs; scope temporaries have all
        # been proven clean. End-of-shot disposal is not an in-program reset.
        allocations = tuple(Allocation(item.id, item.name, item.bits, item.released, item.span)
                            for item in scheduler.storages)
        return Program(self.config, tuple(scheduler.operations), scheduler.qubit_count,
                       scheduler.classical_bit_count, allocations, tuple(scheduler.events), result)


def lower(program: construction.Program) -> Program:
    return Lowerer(program).run()
