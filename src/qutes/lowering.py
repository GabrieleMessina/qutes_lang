"""Construction IR to verified circuit operations.

Integration covers quantum scalar/array/text storage, arithmetic, coherent
predicates and branches, scopes, helpers, loops, and non-consuming measurement.
Runtime-classical predicates use immutable measurement snapshots for feedforward.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Any

from qutes import construction, ir
from qutes.cleanup import CleanupEvent, Scheduler, Storage
from qutes.config import CompilerConfig
from qutes.diagnostics import DiagnosticError, Span
from qutes.feedforward import predicate as runtime_predicate
from qutes.gates import Gate, Measurement, conditioned, controlled, inverse
from qutes.search import schedule, uniform_index
from qutes.values import EncodedString, SignedInteger, TextEncoding


@dataclass(frozen=True)
class Result:
    type: ir.Type
    op: str
    arguments: tuple[Result, ...] = ()
    value: Any = None
    bits: tuple[int, ...] = ()
    alphabet: str | None = None
    length: int | None = None
    capacity: int | None = None

    def decode(self, memory: int):
        if self.op == "literal":
            return list(self.value) if self.type.array else self.value
        if self.op == "snapshot":
            encoded = sum(((memory >> bit) & 1) << index for index, bit in enumerate(self.bits))
            if self.type == ir.Type("bool"):
                return bool(encoded)
            if self.type == ir.Type("int"):
                return SignedInteger(len(self.bits)).decode(encoded)
            if self.type.name in {"char", "string"}:
                codec = TextEncoding(self.alphabet, self.capacity)
                if self.type.name == "char":
                    return codec.decode_character(encoded)
                width = codec.bits_per_character
                codes = tuple((encoded >> (index * width)) & ((1 << width) - 1)
                              for index in range(self.capacity))
                return codec.decode_string(EncodedString(codes, self.length))
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
    retained_index_bits: tuple[int, ...] = ()
    scratch_bits: tuple[int, ...] = ()


@dataclass(frozen=True)
class Collection:
    elements: tuple[Storage, ...]


@dataclass(frozen=True)
class View:
    storage: Storage
    bits: tuple[int, ...]

    @property
    def id(self):
        return self.storage.id


def storage_ids(value):
    if isinstance(value, Collection):
        return {item.id for item in value.elements}
    if isinstance(value, View):
        return {value.storage.id}
    return {value.id} if isinstance(value, Storage) else set()


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
    searches: tuple[dict, ...] = ()

    def to_qiskit(self):
        from qutes.qiskit_backend import emit_operations
        return emit_operations(self.qubit_count, self.classical_bit_count, self.operations)


class Lowerer:
    def __init__(self, program: construction.Program):
        self.program = program
        self.config = program.typed.config
        self.scheduler = Scheduler(max_steps=self.config.max_evaluation_steps)
        self.bindings: dict[int, Storage | Collection | Result] = {}
        self.frames: list[set[int]] = [set()]
        self.script_values: set[int] = set()
        self.controls: tuple[tuple[int, bool], ...] = ()
        self.conditions = ()
        self.lengths: dict[int, int] = {}
        self.searches = []
        self.search_layouts = {}

    def fail(self, node, message, code="Q2001"):
        raise DiagnosticError(code, message, node.span)

    def width(self, type_, node):
        if type_.array or not type_.quantum:
            self.fail(node, f"circuit lowering for {type_} is not implemented yet")
        return {"qubit": 1, "quint": self.config.quint_bits,
                "quchar": self.config.quchar_bits,
                "qustring": self.config.quchar_bits * self.config.qustring_capacity}[type_.name]

    def reference(self, expression):
        if expression.op == "index":
            collection = self.reference(expression.arguments[0])
            index = expression.arguments[1].value
            if isinstance(collection, Collection):
                return collection.elements[index]
            if isinstance(collection, (Storage, View)) and expression.arguments[0].type.name == "qustring":
                width = self.config.quchar_bits
                return View(collection.storage if isinstance(collection, View) else collection,
                            collection.bits[index * width:(index + 1) * width])
            self.fail(expression, "invalid quantum collection reference")
        if expression.op not in {"load", "move"}:
            self.fail(expression, f"circuit lowering for {expression.op} references is not implemented yet")
        value = self.bindings[expression.symbol.id]
        if not isinstance(value, (Storage, Collection, View)) or any(self.scheduler.storages[i].released for i in storage_ids(value)):
            self.fail(expression, "quantum storage is unavailable", "Q3001")
        return value

    def constant(self, expression):
        if expression.op == "lift":
            return expression.arguments[0].value
        if expression.op == "literal":
            return expression.value
        return None

    def encoded_constant(self, expression):
        value = self.constant(expression)
        if value is None:
            return None
        if expression.type.name in {"quchar", "qustring"}:
            codec = TextEncoding(self.config.alphabet, self.config.qustring_capacity)
            if expression.type.name == "quchar":
                return codec.encode_character(value)
            encoded = codec.encode_string(value)
            return sum(code << (index * codec.bits_per_character) for index, code in enumerate(encoded.codes))
        return int(value)

    def text_length(self, expression):
        value = self.constant(expression)
        if value is not None:
            return len(value)
        if expression.op in {"load", "move", "index"}:
            return self.lengths[self.reference(expression).id]
        if expression.shape is not None:
            return expression.shape
        self.fail(expression, "string length is not known during lowering", "Q2003")

    def operand(self, expression):
        value = self.encoded_constant(expression)
        if value is not None:
            return int(value), ()
        if expression.op in {"load", "move", "index"}:
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
        constant = self.encoded_constant(expression)
        if constant is not None:
            return self.copy_gates(target, int(constant), expression.span), ()
        if op == "superposition":
            return (Gate("h", target.bits, span=expression.span),), ()
        if op in {"load", "move", "index"}:
            return self.copy_gates(target, self.reference(expression), expression.span), ()
        if op == "binary:+":
            a, a_temps = self.operand(expression.arguments[0])
            b, b_temps = self.operand(expression.arguments[1])
            return (self.copy_gates(target, a, expression.span) + self.add_gates(target, b, expression.span),
                    a_temps + b_temps)
        if op in {"binary:==", "binary:!=", "binary:<", "binary:<=", "binary:>", "binary:>=",
                  "binary:&&", "binary:||"}:
            return self.predicate(expression, target)
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

    def gated(self, gates):
        result = []
        for gate in gates:
            try:
                operation = controlled(gate, self.controls)
            except ValueError:
                raise DiagnosticError("Q2004", "operation would change its quantum condition", gate.span)
            if operation is not None:
                operation = conditioned(operation, self.conditions)
                if operation is not None:
                    result.append(operation)
        return tuple(result)

    def predicate(self, expression, target):
        a, a_temps = self.operand(expression.arguments[0])
        b, b_temps = self.operand(expression.arguments[1])
        temporaries = a_temps + b_temps
        operator = expression.op[7:]
        gates = []

        if expression.arguments[0].type.name == "qustring" and (
                self.text_length(expression.arguments[0]) != self.text_length(expression.arguments[1])):
            return ((Gate("x", target.bits, span=expression.span),) if operator == "!=" else ()), temporaries

        def test_bit(value, index, expected):
            return bool((value >> index) & 1) == expected if isinstance(value, int) else (value.bits[index], expected)

        def toggle(tests):
            pairs = []
            for test in tests:
                if test is False:
                    return
                if test is not True:
                    pairs.append(test)
            operation = controlled(Gate("x", target.bits, span=expression.span), tuple(pairs))
            if operation is not None:
                gates.append(operation)

        if operator in {"&&", "||"}:
            if operator == "||":
                toggle((test_bit(a, 0, True),))
                toggle((test_bit(b, 0, True),))
            toggle((test_bit(a, 0, True), test_bit(b, 0, True)))
            return tuple(gates), temporaries

        width = self.width(expression.arguments[0].type, expression)
        difference = self.scheduler.allocate(width, "$comparison", expression.span)
        self.scheduler.tick(difference, width)
        self.frames[-1].add(difference.id)
        self.scheduler.initialize(difference, self.gated(self.copy_gates(difference, a, expression.span)
                                                       + self.copy_gates(difference, b, expression.span)))
        temporaries += (difference,)
        if operator in {"==", "!="}:
            toggle(tuple((bit, False) for bit in difference.bits))
            if operator == "!=":
                toggle(())
        else:
            if operator in {">", "<="}:
                a, b = b, a
            signed = expression.arguments[0].type.name == "quint"
            for index in range(width):
                sign = signed and index == width - 1
                toggle((*((bit, False) for bit in difference.bits[index + 1:]),
                        test_bit(a, index, sign), test_bit(b, index, not sign)))
            if operator in {"<=", ">="}:
                toggle(())
        return tuple(gates), temporaries

    def allocate(self, type_, name, node):
        width = self.width(type_, node)
        if width > self.config.max_evaluation_steps - self.scheduler.work:
            self.fail(node, "quantum allocation exceeds the construction budget", "Q4001")
        target = self.scheduler.allocate(width, name, node.span)
        self.scheduler.tick(target, width)
        self.frames[-1].add(target.id)
        return target

    def copy_value(self, source, type_, name, node):
        if isinstance(source, Collection):
            return Collection(tuple(self.copy_value(item, type_.element, f"{name}[{i}]", node)
                                    for i, item in enumerate(source.elements)))
        target = self.allocate(type_, name, node)
        self.scheduler.initialize(target, self.gated(self.copy_gates(target, source, node.span)))
        if type_.name == "qustring":
            self.lengths[target.id] = self.lengths[source.id]
        return target

    def create(self, expression, name):
        if expression.op == "search":
            return self.create_search(expression, name)
        if expression.type.array:
            if expression.op in {"load", "move"}:
                return self.copy_value(self.reference(expression), expression.type, name, expression)
            if expression.op == "array":
                elements = expression.arguments
            else:
                if expression.op == "lift":
                    values = expression.arguments[0].value
                elif expression.op == "new_array":
                    default = {"qubit": False, "quint": 0, "quchar": self.config.alphabet[0], "qustring": ""}[expression.type.name]
                    values = (default,) * expression.shape
                else:
                    self.fail(expression, f"unsupported quantum array construction {expression.op}")
                elements = tuple(ir.Expression(expression.span, expression.type.element, ir.Stage.QUANTUM, "lift",
                    (ir.Expression(expression.span, expression.type.element.classical, ir.Stage.STATIC, "literal", value=value),),
                    shape=len(value) if expression.type.name == "qustring" else None) for value in values)
            return Collection(tuple(self.create(item, f"{name}[{i}]") for i, item in enumerate(elements)))
        target = self.allocate(expression.type, name, expression)
        gates, temporaries = self.preparation(expression, target)
        self.scheduler.initialize(target, self.gated(gates))
        if expression.type.name == "qustring":
            self.lengths[target.id] = self.text_length(expression)
        self.release_temporaries(temporaries)
        return target

    def create_search(self, expression, name):
        if self.controls or self.conditions:
            self.fail(expression, "search cannot prepare state under dynamic control", "Q2004")
        collection = expression.arguments[0]
        count = collection.shape
        width = self.width(expression.type, expression)
        index_width = (count - 1).bit_length()
        try:
            phases = schedule(count, self.config.search_failure_probability, self.config.max_evaluation_steps)
        except ValueError as error:
            self.fail(expression, str(error), "Q4001")
        oracle = expression.value
        child = Lowerer(self.program)
        argument = child.allocate(expression.type, "$oracle_argument", expression)
        child.scheduler.initialize(argument, (), external=True)
        child.bindings[oracle.parameter.id] = argument
        if expression.type.name == "qustring":
            child.lengths[argument.id] = expression.shape
        child.block(oracle.body)
        result = child.reference(oracle.result)
        operations = tuple(child.scheduler.operations)
        if len(result.bits) != 1 or any(not isinstance(g, Gate) or g.kind in {"h", "ry", "phase"}
                                       or g.classical_controls or g.conditions for g in operations):
            self.fail(expression, "oracle must compute a reversible basis predicate", "Q2004")
        # Bound both retained workspace and repeated gate expansion before emitting.
        gate_bound = (len(operations) * 2 + count * width * 2 + count * 2 + 4) * max(1, len(phases)) + count * width
        if gate_bound + child.scheduler.qubit_count > self.config.max_evaluation_steps - self.scheduler.work:
            self.fail(expression, "search circuit expansion exceeds the construction budget", "Q4001")
        owner = self.scheduler.allocate(width + index_width + child.scheduler.qubit_count, name, expression.span)
        self.scheduler.tick(owner, len(owner.bits))
        self.frames[-1].add(owner.id)
        visible = View(owner, owner.bits[:width])
        indices = owner.bits[width:width + index_width]
        work = owner.bits[width + index_width:]
        self.search_layouts[owner.id] = (indices, work)
        mapping = dict(enumerate(work))
        body = tuple(replace(g, targets=tuple(mapping[b] for b in g.targets),
                             inputs=tuple(mapping[b] for b in g.inputs),
                             controls=tuple((mapping[b], expected) for b, expected in g.controls)) for g in operations)
        flag = mapping[result.bits[0]]
        element = View(owner, tuple(mapping[b] for b in argument.bits))
        if collection.stage == ir.Stage.STATIC:
            sources = []
            for value in collection.value:
                literal = ir.Expression(expression.span, expression.type.classical, ir.Stage.STATIC, "literal", value=value)
                lift = ir.Expression(expression.span, expression.type, ir.Stage.QUANTUM, "lift", (literal,))
                sources.append(self.encoded_constant(lift))
        else:
            data = self.reference(collection)
            if isinstance(data, Collection):
                sources = data.elements
            else:
                sources = [View(data.storage if isinstance(data, View) else data,
                                data.bits[i * width:(i + 1) * width]) for i in range(count)]

        def gather(target):
            gates = []
            for i, source in enumerate(sources):
                controls = tuple((bit, bool((i >> j) & 1)) for j, bit in enumerate(indices))
                gates.extend(controlled(g, controls) for g in self.copy_gates(target, source, expression.span))
            return tuple(gates)

        access = gather(element)
        compute = access + body
        preparation = uniform_index(indices, count, expression.span)
        gates = list(preparation)
        for alpha, beta in phases:
            gates.extend(compute)
            gates.append(Gate("phase", (flag,), angle=beta, span=expression.span))
            gates.extend(inverse(compute))
            gates.extend(inverse(preparation))
            gates.append(Gate("x", (indices[0],), span=expression.span))
            gates.append(Gate("phase", (indices[0],), controls=tuple((b, False) for b in indices[1:]),
                              angle=-alpha, span=expression.span))
            gates.append(Gate("x", (indices[0],), span=expression.span))
            gates.extend(preparation)
        gates.extend(gather(visible))
        self.scheduler.initialize_replayable(owner, tuple(gates))
        if expression.type.name == "qustring":
            self.lengths[owner.id] = expression.shape
        self.searches.append({"entries": count, "oracle_calls": 2 * len(phases),
                              "failure_probability": self.config.search_failure_probability,
                              "retained_index_qubits": index_width, "workspace_qubits": len(work),
                              "algorithm": "yoder-low-chuang", "access": "linear-controlled-copy"})
        return visible

    def release_temporaries(self, temporaries):
        self.scheduler.release_scope(set().union(*(storage_ids(value) for value in temporaries)))

    def contains(self, expression, target):
        if expression.op in {"load", "move", "index"} and expression.type.quantum:
            return self.reference(expression) is target
        return any(self.contains(argument, target) for argument in expression.arguments)

    def self_update(self, expression, target):
        op = expression.op
        if op in {"load", "move", "index"} and self.reference(expression) is target:
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

    def measure_value(self, source, type_, expression):
        if isinstance(source, Collection):
            return Result(type_.classical, "array", tuple(self.measure_value(item, type_.element, expression)
                                                         for item in source.elements))
        temporary = None
        if isinstance(source, View):
            temporary = self.copy_value(source, type_, "$observed_element", expression)
            source = temporary
        measurement = self.scheduler.measure(source)
        result = Result(type_.classical, "snapshot", bits=measurement.classical_bits,
                        alphabet=self.config.alphabet if type_.name in {"quchar", "qustring"} else None,
                        length=self.lengths.get(source.id), capacity=self.config.qustring_capacity)
        if temporary is not None:
            self.scheduler.release(temporary)
        return result

    def runtime(self, expression):
        if expression is None:
            return Result(ir.Type("void"), "literal")
        if expression.op == "load":
            value = self.bindings[expression.symbol.id]
            if not isinstance(value, Result):
                self.fail(expression, "a quantum value requires explicit measurement")
            return value
        arguments = tuple(self.runtime(argument) for argument in expression.arguments)
        if expression.op == "index":
            collection, index = arguments
            if collection.op == "array":
                return collection.arguments[index.value]
            if collection.op == "literal":
                return Result(expression.type, "literal", value=collection.value[index.value])
            if collection.op == "snapshot" and collection.type.name == "string":
                width = (len(collection.alphabet) - 1).bit_length()
                return Result(expression.type, "snapshot",
                              bits=collection.bits[index.value * width:(index.value + 1) * width],
                              alphabet=collection.alphabet, capacity=collection.capacity)
        return Result(expression.type, expression.op, arguments, expression.value)

    def block(self, block):
        for statement in block.statements:
            op = statement.op
            if op == "let":
                expression = statement.expressions[0]
                if expression.op == "measure":
                    source = self.reference(expression.arguments[0])
                    value = self.measure_value(source, expression.arguments[0].type, expression)
                elif expression.op == "move":
                    value = self.reference(expression)
                elif expression.type.quantum:
                    value = self.create(expression, statement.symbol.name)
                else:
                    value = self.runtime(expression)
                self.bindings[statement.symbol.id] = value
                if len(self.frames) == 1 and statement.symbol.type.quantum and not statement.symbol.name.startswith("$"):
                    self.script_values.update(storage_ids(value))
            elif op == "assign":
                target_expression, expression = statement.expressions
                target = self.reference(target_expression)
                if isinstance(target, Collection):
                    if expression.op in {"load", "move"} and self.reference(expression) is target:
                        continue
                    # An unconditional permutation can transfer the existing
                    # element storage. Other value copies own different storage;
                    # current index views resolve through this array binding.
                    if not self.controls and not self.conditions and expression.op == "array" and all(
                            item.op in {"load", "move", "index"} for item in expression.arguments):
                        reordered = tuple(self.reference(item) for item in expression.arguments)
                        if (len(reordered) == len(target.elements) and all(isinstance(item, Storage) for item in reordered)
                                and {item.id for item in reordered} == {item.id for item in target.elements}):
                            self.bindings[target_expression.symbol.id] = Collection(reordered)
                            continue
                    replacement = self.create(expression, "$array_value")
                    for old, new in zip(target.elements, replacement.elements, strict=True):
                        self.scheduler.overwrite(old, self.copy_gates(old, new, expression.span),
                                                 controls=self.controls, conditions=self.conditions)
                        if expression.type.name == "qustring":
                            self.lengths[old.id] = self.lengths[new.id]
                    self.release_temporaries((replacement,))
                    continue
                if self.contains(expression, target):
                    gates, temporaries = self.self_update(expression, target)
                    if gates:
                        self.scheduler.update(target.storage if isinstance(target, View) else target, self.gated(gates))
                else:
                    gates, temporaries = self.preparation(expression, target)
                    self.scheduler.overwrite(target.storage if isinstance(target, View) else target, gates, controls=self.controls, conditions=self.conditions)
                self.release_temporaries(temporaries)
                if target_expression.type.name == "qustring":
                    self.lengths[target.id] = self.text_length(expression)
            elif op == "scope":
                self.frames.append(set())
                self.block(statement.blocks[0])
                escapes = set()
                for expression in statement.expressions:
                    # Nested return expressions can refer to more than one local.
                    for identifier in expression.dependencies:
                        value = self.bindings.get(identifier)
                        escapes.update(storage_ids(value))
                owned = self.frames.pop()
                self.scheduler.release_scope(owned - escapes)
                self.frames[-1].update(owned & escapes)
            elif op == "if":
                condition = statement.expressions[0]
                if condition.stage == ir.Stage.QUANTUM:
                    predicate, temporaries = self.operand(condition)
                    if not isinstance(predicate, (Storage, View)) or len(predicate.bits) != 1:
                        self.fail(condition, "quantum condition must occupy one qubit")
                else:
                    predicate = runtime_predicate(self.runtime(condition))
                    self.scheduler.work += sum(1 for _ in predicate.nodes())
                    if self.scheduler.work > self.scheduler.max_steps:
                        self.fail(condition, "classical predicate construction budget exceeded", "Q4001")
                    temporaries = ()
                previous = self.controls
                previous_conditions = self.conditions
                before_lengths = self.lengths.copy()
                branch_lengths = []
                try:
                    for block, expected in zip(statement.blocks, (True, False), strict=True):
                        self.lengths = before_lengths.copy()
                        if condition.stage == ir.Stage.QUANTUM:
                            self.controls = (*previous, (predicate.bits[0], expected))
                        else:
                            self.conditions = (*previous_conditions, (predicate, expected))
                        self.frames.append(set())
                        self.block(block)
                        self.scheduler.release_scope(self.frames.pop())
                        branch_lengths.append(self.lengths.copy())
                finally:
                    self.controls = previous
                    self.conditions = previous_conditions
                for identifier in before_lengths:
                    a, b = (lengths[identifier] for lengths in branch_lengths)
                    if a != b:
                        self.fail(statement, "dynamic branches disagree on string length", "Q2004")
                    self.lengths[identifier] = a
                self.release_temporaries(temporaries)
            else:
                self.fail(statement, f"circuit lowering for {op} statements is not implemented yet")

    def run(self):
        self.block(self.program.body)
        result = self.runtime(self.program.result)
        scheduler = self.scheduler
        # Only explicitly named script values may survive until shot completion.
        # Escaping helper results and computed arguments used anonymously remain
        # compiler temporaries; they must not become silently retained garbage.
        scheduler.release_scope(self.frames[0] - self.script_values)
        allocations = tuple(Allocation(item.id, item.name, item.bits, item.released, item.span,
                                       *self.search_layouts.get(item.id, ((), ())))
                            for item in scheduler.storages)
        return Program(self.config, tuple(scheduler.operations), scheduler.qubit_count,
                       scheduler.classical_bit_count, allocations, tuple(scheduler.events), result,
                       searches=tuple(self.searches))


def lower(program: construction.Program) -> Program:
    return Lowerer(program).run()
