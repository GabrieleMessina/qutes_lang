"""Bounded partial evaluation and inlining; quantum/runtime values stay symbolic.

The result is a loop-free, call-free structured program. It has not yet passed
storage/version cleanup analysis and must not be submitted directly to a backend.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Any

from qutes import ir
from qutes.diagnostics import DiagnosticError
from qutes.values import SignedInteger, TextEncoding
from qutes.membership import matches, pattern_is_element, work_bound
from qutes.numeric import RANK, convert, divide, finite
from qutes.references import Cell, ElementCell, ArrayObject, ArrayView
from qutes.preparation import validate as validate_preparation, work_bound as preparation_work


@dataclass(frozen=True)
class Program:
    typed: ir.Program
    body: ir.Block
    result: ir.Expression | None
    inputs: dict[str, Any]
    evaluation_steps: int
    loop_iterations: int
    cleanup_verified: bool = False


class Returned(Exception):
    def __init__(self, value):
        self.value = value


@dataclass(frozen=True)
class SearchOracle:
    parameter: ir.Symbol
    body: ir.Block
    result: ir.Expression


class Constructor:
    def __init__(self, program: ir.Program):
        self.program = program
        self.config = program.config
        self.functions = {function.key: function for function in program.functions}
        self.environment: dict[int, Cell | ElementCell] = {}
        self.arrays: list[ArrayObject] = []
        self.protected_regions = []
        self.read_borrows = []
        self.output: list[ir.Statement] = []
        self.owned: set[int] = set()
        self.symbol_sequence = 0
        self.steps = 0
        self.iterations = 0
        self.call_depth = 0
        self.expression_overrides: dict[int, ir.Expression] = {}
        self.array_shapes: dict[int, tuple[int | None, ...]] = {}
        self.global_ids = {symbol.id for symbol in program.globals}
        self.input_values = {}

    def fail(self, code, message, node):
        raise DiagnosticError(code, message, node.span)

    def bind(self, identifier, value):
        self.environment[identifier] = Cell(value)

    def freeze(self, value):
        """Capture an array's current contents for an operation, not its identity."""
        if value.op != "array_ref":
            return value
        self.step(value, len(value.value.positions))
        view = value.value
        if value.type.quantum:
            return replace(value, op="array_view", arguments=(view.owner.backing,), value=view.positions,
                           dependencies=view.owner.backing.dependencies, readonly=view.readonly)
        elements = view.elements
        if all(item.stage == ir.Stage.STATIC for item in elements):
            return self.literal(value, tuple(item.value for item in elements))
        return replace(value, op="array", arguments=elements, value=None, stage=ir.Stage.RUNTIME,
                       dependencies=frozenset().union(*(e.dependencies for e in elements)))

    def array_value(self, value, name="$array", *, copy=False):
        if value.op == "array_ref" and not copy:
            return value
        value = self.freeze(value)
        if value.type.quantum:
            backing = self.materialize(value, name)
            elements = [self.index_value(backing, i, value) for i in range(value.shape)]
        else:
            backing = None
            elements = [self.index_value(value, i, value) for i in range(value.shape)]
        owner = ArrayObject(elements, backing)
        self.arrays.append(owner)
        return ir.Expression(value.span, value.type, value.stage, "array_ref",
                             value=ArrayView(owner, tuple(range(len(elements)))), shape=len(elements),
                             dependencies=backing.dependencies if backing else value.dependencies)

    def readonly_value(self, value):
        if value.op == "array_ref":
            return replace(value, value=replace(value.value, readonly=True), readonly=True)
        return value

    def location(self, expression):
        if expression.op == "slice":
            return Cell(self.expression(expression))
        if expression.op == "load":
            cell = self.environment[expression.symbol.id]
            if expression.symbol.readonly:
                self.fail("Q2004", "cannot write through a readonly binding", expression)
            return cell
        if expression.op == "index":
            base = self.expression(expression.arguments[0])
            index = self.static_integer(self.expression(expression.arguments[1]), expression, "index")
            if base.op != "array_ref":
                self.fail("Q2001", "mutable indexed arguments require an array location", expression)
            self.index_value(base, index, expression)
            if base.value.readonly:
                self.fail("Q2004", "cannot write through a readonly array reference", expression)
            return ElementCell(base.value.owner, base.value.positions[index])
        self.fail("Q2001", "mutable argument requires a variable or array element", expression)

    def regions(self, value, cell=None):
        if isinstance(cell, ElementCell):
            return {(id(cell.owner), cell.index)}
        if value.op == "array_ref":
            self.step(value, len(value.value.positions))
            return {(id(value.value.owner), i) for i in value.value.positions}
        if value.op == "index" and value.arguments[0].type.array:
            base = value.arguments[0]
            owner = next((a for a in self.arrays if a.backing and a.backing.symbol.id == base.symbol.id), None)
            return {(id(owner) if owner else ('q', base.symbol.id), value.arguments[1].value)}
        if value.type.quantum and value.op in {"load", "move"}:
            return {(('q', value.symbol.id), 0)}
        return {(id(cell), 0)} if cell else set()

    def check_write(self, cell, expression):
        value = cell.value
        if value.op == "array_ref" and value.value.readonly:
            self.fail("Q2004", "cannot mutate a readonly array reference", expression)
        regions = self.regions(value, cell)
        if any(regions & forbidden for forbidden in (*self.protected_regions, *self.read_borrows)):
            self.fail("Q2004", "write is protected by an active quantum condition or readonly borrow", expression)

    def live_values(self):
        return tuple(self.freeze(cell.value) for cell in self.environment.values() if cell.value.type.quantum)

    def condition_regions(self, value):
        if value.type.quantum and value.op in {"load", "move", "index"}:
            return self.regions(value)
        return set().union(*(self.condition_regions(a) for a in value.arguments))

    def step(self, node, amount=1):
        self.steps += amount
        if self.steps > self.config.max_evaluation_steps:
            self.fail("Q4001", "construction evaluation step budget exceeded", node)

    def iteration(self, node):
        self.iterations += 1
        if self.iterations > self.config.max_loop_iterations:
            self.fail("Q4001", "loop expansion limit exceeded", node)
        self.step(node)

    def literal(self, source, value, type_=None):
        type_ = type_ or source.type
        try:
            finite(value)
        except ValueError as error:
            self.fail("Q2001", str(error), source)
        shape = len(value) if type_.array or type_.name == "string" else None
        if type(value) is int and value.bit_length() > self.config.max_classical_bits:
            self.fail("Q4001", f"classical integer exceeds construction memory limit ({self.config.max_classical_bits} bits)", source)
        return ir.Expression(source.span, type_, ir.Stage.STATIC, "literal", value=value,
                             known=True, shape=shape)

    def symbol(self, name, type_, span):
        symbol = ir.Symbol(self.symbol_sequence, name, type_, False, span)
        self.symbol_sequence += 1
        return symbol

    def load(self, symbol, stage, shape=None):
        return ir.Expression(symbol.span, symbol.type, stage, "load", symbol=symbol,
                             shape=shape, dependencies=frozenset({symbol.id}))

    def materialize(self, expression, name="$temporary", op="let"):
        symbol = self.symbol(name, expression.type, expression.span)
        self.output.append(ir.Statement(expression.span, op, (expression,), symbol=symbol))
        if expression.type.quantum:
            self.owned.add(symbol.id)
        shapes = self.element_shapes(expression)
        if shapes is not None:
            self.array_shapes[symbol.id] = shapes
        return self.load(symbol, expression.stage, expression.shape)

    def element_shapes(self, expression):
        if not expression.type.array or expression.type.name not in {"string", "qustring"}:
            return None
        if expression.op in {"load", "move"}:
            return self.array_shapes.get(expression.symbol.id)
        if expression.op == "array_ref":
            return tuple(item.shape for item in expression.value.elements)
        if expression.op == "array_view":
            shapes = self.element_shapes(expression.arguments[0])
            return tuple(shapes[i] for i in expression.value) if shapes is not None else None
        if expression.op == "array":
            return tuple(self.value_shape(item) for item in expression.arguments)
        if expression.op == "new_array":
            return (0,) * expression.shape
        if expression.op == "lift":
            return tuple(len(value) for value in expression.arguments[0].value)
        if expression.op == "literal":
            return tuple(len(value) for value in expression.value)
        if expression.op == "measure":
            return self.element_shapes(expression.arguments[0])
        return None

    def value_shape(self, expression):
        if expression.op == "index":
            collection, index = expression.arguments
            shapes = self.element_shapes(collection)
            if shapes is not None:
                return shapes[index.value]
        return expression.shape

    def validate_input(self, value, type_, node):
        if type_.array:
            if not isinstance(value, (list, tuple)):
                self.fail("Q2001", f"input requires {type_}", node)
            self.step(node, len(value))
            return tuple(self.validate_input(item, type_.element, node) for item in value)
        if type_.name in {"float", "complex"}:
            try:
                return convert(value, type_.name)
            except ValueError as error:
                self.fail("Q2001", str(error), node)
        expected = {"int": int, "bool": bool, "char": str, "string": str}.get(type_.name)
        if expected is None or type(value) is not expected:
            self.fail("Q2001", f"input requires {type_}", node)
        if type_.name in {"char", "string"}:
            if type_.name == "char" and len(value) != 1:
                self.fail("Q2001", "char input requires one Unicode scalar", node)
            if any(0xD800 <= ord(character) <= 0xDFFF for character in value):
                self.fail("Q2001", "text input contains an invalid Unicode scalar", node)
        self.literal(ir.Expression(node.span, type_, ir.Stage.STATIC, "literal"), value)
        return value

    def run(self, inputs):
        entry = self.functions[self.program.entry]
        expected = {parameter.name for parameter in self.program.inputs}
        if set(inputs) != expected:
            self.fail("Q2001", f"script inputs must be exactly {sorted(expected)}", entry)
        resolved = {}
        for parameter in self.program.inputs:
            value = self.validate_input(inputs[parameter.name], parameter.type, parameter)
            resolved[parameter.name] = value
            self.input_values[parameter.id] = self.literal(
                ir.Expression(parameter.span, parameter.type, ir.Stage.STATIC, "literal"), value)
        result = None
        try:
            self.statements(entry.body)
        except Returned as returned:
            result = returned.value
        if result is not None:
            result = self.freeze(result)
        self.output.append(ir.Statement(entry.span, "roots", tuple(self.freeze(cell.value)
            for identifier, cell in self.environment.items() if identifier in self.global_ids and cell.value.type.quantum)))
        if entry.return_type != ir.Type("void") and result is None:
            self.fail("Q2005", "script ended without a value", entry)
        return Program(self.program, ir.Block(entry.body.span, tuple(self.output)), result,
                       resolved, self.steps, self.iterations)

    def rebuild(self, source, arguments, *, shape=None):
        dependencies = frozenset().union(*(argument.dependencies for argument in arguments))
        effects = frozenset().union(*(argument.effects for argument in arguments))
        return replace(source, arguments=tuple(arguments), known=False, value=None,
                       shape=shape, dependencies=dependencies, effects=effects)

    def expression(self, expression):
        self.step(expression)
        if id(expression) in self.expression_overrides:
            return self.expression_overrides[id(expression)]
        op = expression.op
        if op == "load":
            value = self.environment[expression.symbol.id].value
            if value.op == "array_ref":
                stage = ir.Stage.QUANTUM if value.type.quantum else ir.Stage.RUNTIME if any(e.stage == ir.Stage.RUNTIME for e in value.value.elements) else ir.Stage.STATIC
                value = replace(value, stage=stage)
            return replace(value, span=expression.span, shape=self.value_shape(value))
        if op == "literal":
            return self.literal(expression, expression.value)
        if op == "superposition":
            return replace(expression, known=False)
        if op == "prepare":
            arguments = tuple(self.freeze(self.expression(a)) for a in expression.arguments)
            if any(a.stage != ir.Stage.STATIC for a in arguments):
                self.fail("Q2003", "preparation values and weights must be construction-time data", expression)
            try:
                state = validate_preparation(arguments[0].value, arguments[1].value if len(arguments) > 1 else None,
                                             expression.value, expression.type, self.config.quint_bits)
            except (ValueError, OverflowError) as error:
                self.fail("Q2001", str(error), expression)
            self.step(expression, preparation_work(state, self.config.quint_bits if expression.type.name == "quint" else 1))
            return replace(expression, arguments=(), value=state)
        if op.startswith("gate:"):
            name = op.split(":", 1)[1]
            values, occupied = [], set()
            for i, argument in enumerate(expression.arguments):
                if name == "phase" and i == 1:
                    value = self.expression(argument)
                    if value.stage != ir.Stage.STATIC:
                        self.fail("Q2003", "phase angle must be known during construction", argument)
                else:
                    cell = self.location(argument)
                    self.check_write(cell, argument)
                    regions = self.regions(cell.value, cell)
                    if occupied & regions:
                        self.fail("Q2004", "swap operands must be distinct qubits", expression)
                    occupied.update(regions)
                    value = cell.value
                values.append(value)
            self.output.append(ir.Statement(expression.span, "gate", tuple(values), operator=name))
            return self.literal(expression, None)
        if op == "call":
            function = self.functions[expression.value]
            arguments, locations = [], []
            for parameter, argument in zip(function.parameters, expression.arguments, strict=True):
                if not parameter.readonly and argument.op == "slice" and f"rebind:{parameter.id}" in function.effects:
                    self.fail("Q2004", "cannot pass a temporary slice to a function that rebinds its parameter", argument)
                cell = self.location(argument) if not parameter.readonly else None
                arguments.append(cell.value if cell else self.expression(argument))
                locations.append(cell)
            return self.call(function, tuple(arguments), expression, tuple(locations))
        if op == "copy":
            return self.array_value(self.expression(expression.arguments[0]), "$copy", copy=True)
        if op == "slice":
            base = self.expression(expression.arguments[0])
            start, end = (self.static_integer(self.expression(a), expression, "slice bound") for a in expression.arguments[1:])
            if base.shape is None or not 0 <= start <= end <= base.shape:
                self.fail("Q4001", "slice bounds must satisfy 0 <= start <= end <= Length", expression)
            if base.type.array:
                base = self.array_value(base)
                view = replace(base.value, positions=base.value.positions[start:end])
            else:
                if base.type.quantum and base.op not in {"load", "index"}:
                    base = self.materialize(base, "$text_view")
                owner = ArrayObject([self.index_value(base, i, expression) for i in range(base.shape)], base if base.type.quantum else None)
                self.arrays.append(owner)
                view = ArrayView(owner, tuple(range(start, end)), True)
            return replace(expression, op="array_ref", arguments=(), value=view, shape=end-start,
                           dependencies=base.dependencies, readonly=view.readonly)
        if op == "range":
            start, end = (self.static_integer(self.expression(a), expression, "range bound") for a in expression.arguments)
            if start > end:
                self.fail("Q2001", "range start cannot exceed its end", expression)
            self.step(expression, end-start)
            return self.array_value(self.literal(expression, tuple(range(start, end))))
        if op == "membership":
            left = self.freeze(self.expression(expression.arguments[0]))
            if left.type.quantum and any(effect == "measure" or effect.startswith("write:")
                                         for effect in expression.arguments[1].effects):
                left = self.materialize(left, "$membership_snapshot")
            right = self.freeze(self.expression(expression.arguments[1]))
            if left.stage == right.stage == ir.Stage.STATIC:
                self.step(expression, work_bound(left.value, right.value, left.type, right.type))
                return self.literal(expression, matches(left.value, right.value, left.type, right.type))
            return replace(self.membership(expression, left, right), presentation="membership")
        if op == "search":
            collection = self.freeze(self.expression(expression.arguments[0]))
            if collection.type.quantum and collection.op not in {"load", "index", "array_view"}:
                collection = self.materialize(collection, "$search_collection")
            if collection.shape is None or collection.shape == 0:
                self.fail("Q2001", "search requires a nonempty collection of known length", expression)
            shape = None
            if expression.type.name == "qustring":
                shapes = self.element_shapes(collection)
                if shapes is None or None in shapes or len(set(shapes)) != 1:
                    self.fail("Q2001", "search requires string entries with the same known length", expression)
                shape = shapes[0]
            if collection.stage == ir.Stage.STATIC:
                for value in collection.value:
                    self.validate_quantum_constant(value, expression.type, expression)
            parameter = self.symbol("$search_element", expression.type, expression.span)
            parent_output, parent_owned = self.output, self.owned
            self.output, self.owned = [], set()
            try:
                result = self.call(self.functions[expression.value],
                                   (self.load(parameter, ir.Stage.QUANTUM, shape),), expression)
                oracle = SearchOracle(parameter, ir.Block(expression.span, tuple(self.output)), result)
            finally:
                self.output, self.owned = parent_output, parent_owned
            return replace(expression, arguments=(collection,), value=oracle, shape=shape,
                           dependencies=collection.dependencies)
        if op.startswith("binary:"):
            operator = op.split(":", 1)[1]
            left = self.expression(expression.arguments[0])
            if left.stage == ir.Stage.STATIC and left.type == ir.Type("bool"):
                if (operator == "&&" and not left.value) or (operator == "||" and left.value):
                    return self.literal(expression, left.value)
            right = self.expression(expression.arguments[1])
            if left.stage == right.stage == ir.Stage.STATIC:
                return self.classical_binary(expression, operator, left.value, right.value)
            if ir.Stage.RUNTIME in {left.stage, right.stage} and operator in {"+", "-", "*", "/", "%"}:
                self.fail("Q2003", "arithmetic on measurement results is deferred", expression)
            return self.rebuild(expression, (left, right))
        if op.startswith("unary:"):
            operand = self.expression(expression.arguments[0])
            if operand.stage != ir.Stage.STATIC:
                return self.rebuild(expression, (operand,))
            operator = op.split(":", 1)[1]
            value = not operand.value if operator == "!" else (-operand.value if operator == "-" else operand.value)
            return self.literal(expression, value)
        arguments = tuple(self.expression(argument) for argument in expression.arguments)
        if op in {"numeric_convert", "complex"}:
            if any(a.stage != ir.Stage.STATIC for a in arguments):
                self.fail("Q2003", "numeric values must be known during construction", expression)
            try:
                value = convert(arguments[0].value, expression.type.name) if op == "numeric_convert" else complex(*(a.value for a in arguments))
                return self.literal(expression, finite(value))
            except ValueError as error:
                self.fail("Q2001", str(error), expression)
        if op == "lift":
            value = self.freeze(arguments[0])
            if value.stage != ir.Stage.STATIC:
                self.fail("Q2003", "quantum initialization requires construction-time data", expression)
            self.validate_quantum_constant(value.value, expression.type, expression)
            return self.rebuild(expression, (value,), shape=value.shape)
        if op == "array":
            if all(argument.stage == ir.Stage.STATIC for argument in arguments) and not expression.type.quantum:
                return self.literal(expression, tuple(argument.value for argument in arguments))
            return self.rebuild(expression, arguments, shape=len(arguments))
        if op == "new_array":
            length = self.static_integer(arguments[0], expression, "array length")
            if length < 0:
                self.fail("Q4001", "array length cannot be negative", expression)
            self.step(expression, length)
            if expression.type.quantum:
                return self.rebuild(expression, arguments, shape=length)
            default = {"int": 0, "float": 0.0, "complex": 0j, "bool": False, "char": self.config.alphabet[0], "string": ""}[expression.type.name]
            return self.literal(expression, (default,) * length)
        if op == "length":
            collection = arguments[0]
            if collection.shape is None:
                self.fail("Q2003", "collection length is not known during construction", expression)
            return self.literal(expression, collection.shape)
        if op == "index":
            collection, index = arguments
            position = self.static_integer(index, expression, "index")
            return self.index_value(collection, position, expression)
        if op in {"rotateLeft", "rotateRight"}:
            count = self.static_integer(arguments[1], expression, "rotation count")
            if count < 0:
                self.fail("Q2001", "rotation count cannot be negative", expression)
            return self.rebuild(expression, arguments)
        if op == "measure":
            argument = self.freeze(arguments[0])
            if argument.op not in {"load", "index", "array_view"}:
                argument = self.materialize(argument)
            measured = self.rebuild(expression, (argument,), shape=argument.shape)
            return self.materialize(measured, "$measurement")
        raise AssertionError(f"unsupported typed expression {op}")

    def validate_quantum_constant(self, value, type_, node):
        if type_.array:
            self.step(node, len(value))
            for item in value:
                self.validate_quantum_constant(item, type_.element, node)
            return
        try:
            if type_.name == "quint":
                SignedInteger(self.config.quint_bits).encode(value)
            elif type_.name == "quchar":
                TextEncoding(self.config.alphabet, self.config.qustring_capacity).encode_character(value)
            elif type_.name == "qustring":
                TextEncoding(self.config.alphabet, self.config.qustring_capacity).encode_string(value)
        except ValueError as error:
            self.fail("Q2001", str(error), node)

    def membership(self, source, left, right):
        # Operands are evaluated once before expanding the position comparisons.
        def stable(value):
            if value.type.quantum and value.op not in {"load", "index", "array_view"}:
                return self.materialize(value, "$membership_input")
            return value
        left, right = stable(left), stable(right)
        scalar = pattern_is_element(left.type, right.type)
        count = 1 if scalar else left.shape
        if count is None or right.shape is None:
            self.fail("Q2003", "membership requires known sequence lengths", source)
        self.step(source, max(1, right.shape - count + 1) * max(1, count))

        def constant(value):
            return self.literal(source, value, ir.Type("bool"))

        def combine(op, items):
            if not items:
                return constant(op == "&&")
            while len(items) > 1:
                merged = []
                for i in range(0, len(items), 2):
                    if i + 1 == len(items):
                        merged.append(items[i])
                        continue
                    a, b = items[i:i + 2]
                    if a.stage == b.stage == ir.Stage.STATIC:
                        merged.append(constant((a.value and b.value) if op == "&&" else (a.value or b.value)))
                    elif a.stage == ir.Stage.STATIC:
                        merged.append(b if bool(a.value) == (op == "&&") else a)
                    elif b.stage == ir.Stage.STATIC:
                        merged.append(a if bool(b.value) == (op == "&&") else b)
                    else:
                        merged.append(binary(op, a, b))
                items = merged
            return items[0]

        def lift(value, type_):
            if value.type == type_:
                return value
            self.validate_quantum_constant(value.value, type_, source)
            return ir.Expression(source.span, type_, ir.Stage.QUANTUM, "lift", (value,), shape=value.shape)

        def binary(op, a, b):
            target = a.type if a.type.quantum else b.type
            a, b = lift(a, target), lift(b, target)
            return ir.Expression(source.span, ir.Type("qubit"), ir.Stage.QUANTUM, "binary:" + op,
                                 (a, b), dependencies=a.dependencies | b.dependencies)

        def equal(a, b):
            self.step(source)
            if a.type.classical.name == "string":
                if a.shape != b.shape:
                    return constant(False)
                return combine("&&", [equal(self.index_value(a, j, source), self.index_value(b, j, source))
                                       for j in range(a.shape)])
            character = a.type.classical.name == "char"
            if character and a.stage == ir.Stage.STATIC and a.value == "?":
                return constant(True)
            if a.stage == b.stage == ir.Stage.STATIC:
                return constant(a.value == b.value)
            result = binary("==", a, b)
            if character and a.type.quantum and "?" in self.config.alphabet:
                wildcard = self.literal(source, "?", ir.Type("char"))
                result = combine("||", [binary("==", a, wildcard), result])
            return result

        windows = []
        for i in range(right.shape - count + 1):
            windows.append(combine("&&", [equal(left if scalar else self.index_value(left, j, source),
                                                self.index_value(right, i + j, source)) for j in range(count)]))
        result = combine("||", windows)
        return lift(result, ir.Type("qubit"))

    def classical_binary(self, expression, operator, a, b):
        if operator in {"/", "%"} and b == 0:
            self.fail("Q4001", "division by zero", expression)
        if operator == "+": value = a + b
        elif operator == "-": value = a - b
        elif operator == "*": value = a * b
        elif operator in {"/", "%"}:
            value = divide(a, b, operator == "%")
        elif operator == "&&": value = a and b
        elif operator == "||": value = a or b
        elif operator == "==": value = a == b
        elif operator == "!=": value = a != b
        elif operator == "<": value = a < b
        elif operator == "<=": value = a <= b
        elif operator == ">": value = a > b
        elif operator == ">=": value = a >= b
        else: raise AssertionError(operator)
        return self.literal(expression, value)

    def static_integer(self, value, node, purpose):
        if value.stage != ir.Stage.STATIC or value.type != ir.Type("int"):
            self.fail("Q2003", f"{purpose} must be a construction-time integer", node)
        return value.value

    def index_value(self, collection, position, source):
        if collection.shape is None or not 0 <= position < collection.shape:
            self.fail("Q4001", "index is outside the collection", source)
        if collection.op == "array_ref":
            return collection.value.elements[position]
        if collection.op == "array_view":
            return self.index_value(collection.arguments[0], collection.value[position], source)
        if collection.stage == ir.Stage.STATIC:
            return self.literal(source, collection.value[position], collection.type.element)
        if collection.op == "array":
            return collection.arguments[position]
        offset = ir.Expression(source.span, ir.Type("int"), ir.Stage.STATIC, "literal", value=position, known=True)
        shapes = self.element_shapes(collection)
        return ir.Expression(source.span, collection.type.element, collection.stage, "index", (collection, offset),
                             shape=shapes[position] if shapes is not None else None, dependencies=collection.dependencies)

    def condition(self, expression):
        value = self.expression(expression)
        if value.stage != ir.Stage.STATIC or value.type != ir.Type("bool"):
            self.fail("Q2003", "loop condition is not a construction-time Boolean", expression)
        return value.value

    def statements(self, block):
        for statement in block.statements:
            self.statement(statement)

    def region(self, block, kind="block", aliases=()):
        outer_ids = set(self.environment)
        previous_output, previous_owned = self.output, self.owned
        self.output, self.owned = [], set()
        returned = None
        try:
            self.statements(block)
        except Returned as result:
            returned = result
        finally:
            child, owned = tuple(self.output), self.owned
            self.output, self.owned = previous_output, previous_owned
        self.environment = {identifier: cell for identifier, cell in self.environment.items() if identifier in outer_ids}
        escapes = self.live_values()
        if returned and returned.value is not None and returned.value.type.quantum:
            escapes = (*escapes, self.freeze(returned.value))
            self.owned.update(owned & set(returned.value.dependencies))
        self.output.append(ir.Statement(block.span, "scope", escapes,
                                        (ir.Block(block.span, child),), operator=kind, aliases=aliases))
        if returned:
            raise returned

    def statement(self, statement):
        self.step(statement)
        op = statement.op
        if op == "input":
            value = self.input_values[statement.symbol.id]
            self.bind(statement.symbol.id, self.array_value(value, statement.symbol.name) if value.type.array else value)
        elif op == "let":
            value = self.expression(statement.expressions[0])
            if value.type.array:
                value = self.array_value(value, statement.symbol.name)
                if statement.symbol.readonly:
                    value = self.readonly_value(value)
            elif value.type.quantum:
                value = self.materialize(value, statement.symbol.name)
            if not value.type.quantum:
                self.output.append(ir.Statement(statement.span, "bind", (self.freeze(value),), symbol=statement.symbol,
                    operator="global" if statement.symbol.id in self.global_ids else None))
            elif value.type.array:
                if value.value.owner.backing.symbol.name != statement.symbol.name:
                    self.output.append(ir.Statement(statement.span, "alias", (self.freeze(value),), symbol=statement.symbol))
            self.bind(statement.symbol.id, value)
        elif op == "assign":
            target_source, value_source = statement.expressions
            cell = self.location(target_source)
            self.check_write(cell, statement)
            target = cell.value
            # Compound assignments share their target expression with the RHS IR.
            # Evaluate it once, including any helper used to compute an index.
            self.expression_overrides[id(target_source)] = target
            try:
                value = self.expression(value_source)
            finally:
                del self.expression_overrides[id(target_source)]
            if target.type.array:
                updated = self.array_value(value, "$rebound_array")
            elif target.type.quantum:
                self.output.append(ir.Statement(statement.span, "assign", (target, value), operator="="))
                updated = replace(target, shape=value.shape)
                if isinstance(cell, ElementCell) and target.type.name == "qustring":
                    backing = cell.owner.backing
                    shapes = list(self.array_shapes[backing.symbol.id])
                    shapes[cell.index] = value.shape
                    self.array_shapes[backing.symbol.id] = tuple(shapes)
            else:
                updated = value
            cell.value = updated
            if target_source.op == "load":
                if target.type.quantum and target.type.array:
                    self.output.append(ir.Statement(statement.span, "alias", (self.freeze(updated),), symbol=target_source.symbol))
                if not target.type.quantum:
                    self.output.append(ir.Statement(statement.span, "bind", (self.freeze(updated),), symbol=target_source.symbol,
                        operator="global" if target_source.symbol.id in self.global_ids else None))
        elif op == "return":
            raise Returned(self.expression(statement.expressions[0]) if statement.expressions else None)
        elif op == "expr":
            self.expression(statement.expressions[0])
        elif op == "block":
            self.region(statement.blocks[0])
        elif op == "if":
            self.if_statement(statement)
        elif op in {"while", "for"}:
            if op == "for":
                self.statements(statement.blocks[0])
                body, update = statement.blocks[1:]
            else:
                body, update = statement.blocks[0], None
            while self.condition(statement.expressions[0]):
                self.iteration(statement)
                self.region(body, "iteration")
                if update:
                    self.statements(update)
        elif op == "foreach":
            collection = self.expression(statement.expressions[0])
            if collection.type.array:
                collection = self.array_value(collection, "$iteration_source")
            elif collection.type.quantum and collection.op not in {"load", "index"}:
                collection = self.materialize(collection, "$iteration_source")
            if collection.shape is None:
                self.fail("Q2003", "foreach length must be known during construction", statement)
            for index in range(collection.shape):
                self.iteration(statement)
                item = self.index_value(collection, index, statement)
                self.bind(statement.symbol.id, item)
                if statement.index_symbol:
                    self.bind(statement.index_symbol.id, self.literal(collection, index, ir.Type("int")))
                self.region(statement.blocks[0], "iteration", aliases=((statement.symbol.name, item),))
            self.environment.pop(statement.symbol.id, None)
            if statement.index_symbol:
                self.environment.pop(statement.index_symbol.id, None)
        else:
            raise AssertionError(op)

    def if_statement(self, statement):
        condition = self.expression(statement.expressions[0])
        if condition.stage == ir.Stage.STATIC:
            self.region(statement.blocks[0 if condition.value else 1])
            return
        before = self.environment.copy()
        before_values = {identifier: cell.value for identifier, cell in before.items()}
        before_arrays = [(owner, list(owner.elements)) for owner in self.arrays]
        before_shapes = self.array_shapes.copy()
        parent_output, parent_owned = self.output, self.owned
        branches, states, shape_states, array_states = [], [], [], []
        prior_protected = self.protected_regions
        if condition.stage == ir.Stage.QUANTUM:
            self.protected_regions = prior_protected + [self.condition_regions(condition)]
        try:
            for block in statement.blocks:
                self.output, self.owned = [], set()
                self.environment = before.copy()
                for identifier, cell in before.items():
                    cell.value = before_values[identifier]
                for owner, elements in before_arrays:
                    owner.elements[:] = elements
                self.array_shapes = before_shapes.copy()
                self.statements(block)
                branches.append(ir.Block(block.span, tuple(self.output)))
                states.append({identifier: cell.value for identifier, cell in self.environment.items()})
                array_states.append([list(owner.elements) for owner, _ in before_arrays])
                shape_states.append(self.array_shapes.copy())
        finally:
            self.output, self.owned = parent_output, parent_owned
            self.environment = before.copy()
            for identifier, cell in before.items():
                cell.value = before_values[identifier]
            for owner, elements in before_arrays:
                owner.elements[:] = elements
            self.array_shapes = before_shapes.copy()
            self.protected_regions = prior_protected
        for identifier in before_shapes:
            a, b = (state[identifier] for state in shape_states)
            if a != b:
                self.fail("Q2004", "dynamic branches disagree on string-array element lengths", statement)
            self.array_shapes[identifier] = a
        for identifier, cell in before.items():
            value = before_values[identifier]
            a, b = (state[identifier] for state in states)
            if a.shape != b.shape:
                self.fail("Q2004", "dynamic branches disagree on collection/string length", statement)
            if value.type.quantum:
                cell.value = replace(value, shape=a.shape)
            elif a != value or b != value:
                self.fail("Q2004", "dynamic branches cannot change classical state", statement)
        for i, (owner, _) in enumerate(before_arrays):
            a, b = array_states[0][i], array_states[1][i]
            if any(x.shape != y.shape for x, y in zip(a, b, strict=True)):
                self.fail("Q2004", "dynamic branches disagree on array element lengths", statement)
            owner.elements[:] = a
        self.output.append(ir.Statement(statement.span, "if", (condition,), tuple(branches)))

    def call(self, function, arguments, source, locations=()):
        self.step(source)
        if self.call_depth >= 64:
            self.fail("Q4001", "function inlining depth exceeded", source)
        self.call_depth += 1
        normalized = []
        for argument in arguments:
            if argument.type.array:
                argument = self.array_value(argument, "$argument")
            elif argument.type.quantum and argument.op not in {"load", "index"}:
                argument = self.materialize(argument, "$argument")
            normalized.append(argument)
        parent_environment, parent_output, parent_owned = self.environment, self.output, self.owned
        if not locations:
            locations = (None,) * len(arguments)
        borrowed = [(self.regions(a, c), not p.readonly) for p, a, c in zip(function.parameters, normalized, locations, strict=True)]
        for i, (region, mutable) in enumerate(borrowed):
            for other, other_mutable in borrowed[:i]:
                if (mutable or other_mutable) and region & other:
                    self.fail("Q2004", "function arguments have overlapping mutable/readonly borrows", source)
        for cell in locations:
            if cell is not None:
                self.check_write(cell, source)
        self.environment = {identifier: value for identifier, value in parent_environment.items() if identifier in self.global_ids}
        for parameter, argument, cell in zip(function.parameters, normalized, locations, strict=True):
            self.environment[parameter.id] = cell if cell is not None else Cell(self.readonly_value(argument))
        previous_borrows = self.read_borrows
        self.read_borrows = previous_borrows + [region for (region, mutable), argument in zip(borrowed, normalized, strict=True) if not mutable and (argument.type.quantum or argument.type.array)]
        self.output, self.owned = [], set()
        result = None
        try:
            try:
                self.statements(function.body)
            except Returned as returned:
                result = returned.value
            if result is not None and result.type.array:
                result = self.array_value(result, "$return")
            elif result is not None and result.type.quantum:
                if result.op != "load" or result.symbol.id not in self.owned:
                    result = self.materialize(result, "$return")
                result = replace(result, op="move")
            body = ir.Block(function.body.span, tuple(self.output))
        finally:
            parent_environment.update({identifier: value for identifier, value in self.environment.items() if identifier in self.global_ids})
            self.environment, self.output, self.owned = parent_environment, parent_output, parent_owned
            self.call_depth -= 1
            self.read_borrows = previous_borrows
        escapes = self.live_values()
        if result is not None and result.type.quantum:
            escapes = (self.freeze(result), *escapes)
        self.output.append(ir.Statement(source.span, "scope", escapes, (body,), operator="function",
            source_name=function.name, aliases=tuple((p.name, self.freeze(a)) for p, a in zip(function.parameters, normalized, strict=True))))
        if result is None:
            return ir.Expression(source.span, ir.Type("void"), ir.Stage.STATIC, "literal", known=True)
        return replace(result, span=source.span)


def construct(program: ir.Program, inputs: dict[str, Any] | None = None) -> Program:
    if inputs is not None and not isinstance(inputs, dict):
        raise DiagnosticError("Q2001", "script inputs must be a name-to-value mapping", program.span)
    return Constructor(program).run({} if inputs is None else inputs)
