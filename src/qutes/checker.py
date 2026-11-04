"""Name/type/stage/effect analysis. This pass does not prove quantum cleanup."""

from __future__ import annotations

from contextlib import contextmanager
from dataclasses import dataclass, fields, replace
from typing import Any
from difflib import get_close_matches

from qutes import ir, syntax as ast
from qutes.config import CompilerConfig
from qutes.diagnostics import DiagnosticError, Span
from qutes.values import SignedInteger, TextEncoding
from qutes.vocabulary import Builtin
from qutes.membership import is_sequence, pattern_is_element, matches


@dataclass
class Binding:
    symbol: ir.Symbol
    stage: ir.Stage
    known: bool = False
    value: Any = None
    shape: int | None = None
    alias_dependencies: frozenset[int] = frozenset()
    initialized: bool = True


def _walk(node):
    pending = [node]
    while pending:
        current = pending.pop()
        yield current
        for field in fields(current):
            value = getattr(current, field.name)
            if isinstance(value, ast.Node):
                pending.append(value)
            elif isinstance(value, tuple):
                pending.extend(item for item in value if isinstance(item, ast.Node))


def _merge_stage(expressions) -> ir.Stage:
    stages = {expression.stage for expression in expressions}
    if ir.Stage.QUANTUM in stages:
        return ir.Stage.QUANTUM
    return ir.Stage.RUNTIME if ir.Stage.RUNTIME in stages else ir.Stage.STATIC


class Checker:
    def __init__(self, program: ast.Program, config: CompilerConfig):
        self.source = program
        self.config = config
        self.functions: dict[str, ast.Function] = {}
        self.instances: dict[tuple, ir.Function] = {}
        self.sequence = 0
        self.function_sequence = 0
        self.scopes: list[dict[str, Binding]] = []
        self.function: ast.Function | None = None
        self.return_type = ir.Type("void")
        self.return_values: list[ir.Expression] = []
        self.effects: set[str] = set()
        self.if_depth = 0
        self.coherent_depth = 0
        self.dynamic_outers: set[int] = set()
        self.protected: set[int] = set()
        self.dynamic_depth = 0
        self.deferred_faults = 0
        self.steps = 0
        self.call_depth = 0
        self.global_symbols = {}
        self.global_ids = set()
        self.script_return_seen = False
        self.exit_globals = []

    def fail(self, code: str, message: str, node, *, help=None) -> None:
        raise DiagnosticError(code, message, node if isinstance(node, Span) else node.span, help=help)

    def suggestion(self, name, candidates):
        matches = get_close_matches(name, sorted(set(candidates)), n=2, cutoff=0.75)
        return f"Did you mean {matches[0]!r}?" if len(matches) == 1 else None

    def step(self, node):
        self.steps += 1
        if self.steps > self.config.max_evaluation_steps:
            self.fail("Q4001", "semantic analysis step budget exceeded", node)

    def type(self, node: ast.TypeRef, allow_void=False) -> ir.Type:
        if node.name == "void" and (not allow_void or node.array):
            self.fail("Q2001", "void is only allowed as a scalar function return type", node)
        quantum_width = {"qubit": 1, "quint": self.config.quint_bits,
                         "quchar": self.config.quchar_bits,
                         "qustring": self.config.quchar_bits * self.config.qustring_capacity}.get(node.name, 0)
        if quantum_width > self.config.max_evaluation_steps:
            self.fail("Q4001", "quantum type width exceeds the construction budget", node)
        return ir.Type(node.name, node.array)

    def run(self) -> ir.Program:
        for function in self.source.functions:
            if function.name in self.functions or function.name in set(Builtin):
                self.fail("Q2002", f"duplicate or reserved function name {function.name!r}", function)
            self.functions[function.name] = function
            self.type(function.return_type, allow_void=True)
            for parameter in function.parameters:
                self.type(parameter.type)
        self.scopes = [{}]
        inputs = []
        for statement in self.source.statements:
            if isinstance(statement, (ast.Declaration, ast.Input)):
                type_ = self.type(statement.type)
                if isinstance(statement, ast.Input) and type_.quantum:
                    self.fail("Q2001", "inputs must be classical data", statement)
                value = ir.Expression(statement.span, type_, ir.Stage.QUANTUM if type_.quantum else ir.Stage.STATIC, "global")
                symbol = self.declare(statement.name, type_, value, statement)
                self.global_symbols[statement.name] = symbol
                self.global_ids.add(symbol.id)
                self.scopes[0][statement.name].initialized = False
                if isinstance(statement, ast.Input):
                    inputs.append(symbol)
        script = ast.Function(self.source.span, ast.TypeRef(self.source.span, "void"), "$script", (),
                              ast.Block(self.source.span, self.source.statements))
        self.functions["$script"] = script
        self.check_calls()
        self.function = script
        body = self.block(script.body, new_scope=False)
        if self.return_type != ir.Type("void") and not body.returns:
            self.fail("Q2005", "script must return a value on every path", self.source)
        entry = ir.Function(script.span, "$script", "$script", (), self.return_type,
                            _merge_stage(self.return_values), None, body, frozenset(self.effects))
        # Validate uncalled definitions too, with symbolic globals. Calls from the
        # script were already checked using their actual initialization/staging state.
        final_globals = self.snapshot()[0]
        for function in self.source.functions:
            if any(instance.name == function.name for instance in self.instances.values()):
                continue
            self.scopes = [{name: replace(binding, initialized=True, known=False, value=None)
                            for name, binding in final_globals.items()}]
            parameters = tuple((ir.Stage.QUANTUM if self.type(p.type).quantum else ir.Stage.STATIC, None)
                               for p in function.parameters)
            self.function_instance(function.name, parameters)
        return ir.Program(self.source.span, self.config, (*self.instances.values(), entry), entry.key,
                          globals=tuple(self.global_symbols.values()), inputs=tuple(inputs))

    def check_calls(self):
        graph = {name: [] for name in self.functions}
        for name, function in self.functions.items():
            for node in _walk(function.body):
                if isinstance(node, ast.Call) and isinstance(node.callee, ast.Name):
                    target = node.callee.identifier
                    if target in self.functions:
                        graph[name].append((target, node))
                    if target == Builtin.SEARCH and len(node.arguments) == 2 and isinstance(node.arguments[1], ast.Name):
                        oracle = node.arguments[1].identifier
                        if oracle in self.functions:
                            graph[name].append((oracle, node))
        visiting, finished = set(), set()

        def visit(name, depth=0):
            if depth > 64:
                self.fail("Q4001", "function call nesting limit exceeded", self.functions[name])
            visiting.add(name)
            for target, node in graph[name]:
                if target in visiting:
                    self.fail("Q2002", "recursive calls are not supported in V1", node)
                if target not in finished:
                    visit(target, depth + 1)
            visiting.remove(name)
            finished.add(name)

        for name in graph:
            if name not in finished:
                visit(name)

    def function_instance(self, name, parameter_info, arguments=()):
        # Globals are mutable and their stages/shapes vary by call site. Each
        # specialization is analyzed against its current environment, never cached.
        cache_key = (name, self.function_sequence)
        function = self.functions[name]
        if self.call_depth >= 64:
            self.fail("Q4001", "function specialization nesting limit exceeded", function)
        self.call_depth += 1
        state = (self.scopes, self.function, self.return_type, self.return_values, self.effects,
                 self.if_depth, self.coherent_depth, self.dynamic_outers, self.protected,
                 self.dynamic_depth, self.deferred_faults, self.exit_globals)
        global_scope = {name: replace(binding, known=False, value=None) for name, binding in self.scopes[0].items()}
        self.scopes, self.function = [global_scope, {}], function
        self.return_type = self.type(function.return_type, allow_void=True)
        self.return_values, self.effects = [], set()
        self.exit_globals = []
        # Inherit call-site restrictions, but returns belong to this function.
        self.dynamic_outers = set(self.dynamic_outers)
        self.protected = set(self.protected)
        aliases = tuple(argument.dependencies if argument.type.quantum and argument.op in {"load", "index"}
                        else frozenset() for argument in arguments)
        for dependencies in aliases:
            self.protected.update(identifier for identifier in dependencies if identifier in self.global_ids
                                  and any(symbol.id == identifier and symbol.type.quantum for symbol in self.global_symbols.values()))
        self.dynamic_depth = self.deferred_faults = 0
        key = f"{name}${self.function_sequence}"
        self.function_sequence += 1
        try:
            parameters = []
            for index, (parameter, (stage, shape)) in enumerate(zip(function.parameters, parameter_info, strict=True)):
                type_ = self.type(parameter.type)
                expression = ir.Expression(parameter.span, type_, stage, "parameter", shape=shape)
                dependencies = aliases[index] if arguments else frozenset()
                parameters.append(self.declare(parameter.name, type_, expression, parameter, readonly=True, alias_dependencies=dependencies))
            body = self.block(function.body, new_scope=False)
            if self.return_type.name != "void" and not body.returns:
                self.fail("Q2005", f"function {name!r} must return a value on every path", function)
            if not body.returns:
                self.exit_globals.append(self.snapshot()[0])
            # Early returns are separate outgoing states. A later assignment on
            # another path must not hide a measurement/stage change on an exit.
            if self.exit_globals:
                for global_name, binding in self.scopes[0].items():
                    exits = [scope[global_name] for scope in self.exit_globals]
                    binding.stage = _merge_stage(exits)
                    binding.shape = exits[0].shape if all(item.shape == exits[0].shape for item in exits) else None
                    binding.known = all(item.known and item.value == exits[0].value for item in exits)
                    binding.value = exits[0].value if binding.known else None
            stage = _merge_stage(self.return_values)
            shapes = {value.shape for value in self.return_values}
            result = ir.Function(function.span, key, name, tuple(parameters), self.return_type,
                                 stage, next(iter(shapes)) if len(shapes) == 1 else None,
                                 body, frozenset(self.effects))
            self.instances[cache_key] = result
            return result
        finally:
            updated_globals = self.scopes[0]
            (self.scopes, self.function, self.return_type, self.return_values, self.effects,
             self.if_depth, self.coherent_depth, self.dynamic_outers, self.protected,
             self.dynamic_depth, self.deferred_faults, self.exit_globals) = state
            self.scopes[0] = updated_globals
            self.call_depth -= 1

    def binding(self, name, node):
        for scope in reversed(self.scopes):
            if name in scope:
                binding = scope[name]
                if not binding.initialized:
                    self.fail("Q2002", f"global {name!r} is accessed before its declaration executes", node,
                              help="Move the declaration before this statement or the call that accesses it.")
                if binding.symbol.id in self.global_ids:
                    self.effects.add(f"read:{binding.symbol.id}")
                return binding
        self.fail("Q2002", f"unknown variable {name!r}", node,
                  help=self.suggestion(name, (key for scope in self.scopes for key in scope)))

    def declare(self, name, type_, expression, node, readonly=False, alias_dependencies=frozenset()):
        if name in self.scopes[-1] or name in self.functions or name in set(Builtin):
            self.fail("Q2002", f"duplicate or reserved variable name {name!r}", node)
        symbol = ir.Symbol(self.sequence, name, type_, readonly, node.span)
        self.sequence += 1
        self.scopes[-1][name] = Binding(symbol, expression.stage, expression.known,
                                      expression.value, expression.shape, alias_dependencies)
        return symbol

    def snapshot(self):
        return [{name: replace(binding) for name, binding in scope.items()} for scope in self.scopes]

    def restore(self, snapshot):
        self.scopes = [{name: replace(binding) for name, binding in scope.items()} for scope in snapshot]

    @contextmanager
    def scope(self):
        self.scopes.append({})
        try:
            yield
        finally:
            self.scopes.pop()

    def expression(self, node: ast.Expr, expected: ir.Type | None = None, allow_prepare=False) -> ir.Expression:
        self.step(node)
        if isinstance(node, ast.Group):
            return replace(self.expression(node.expression, expected, allow_prepare), span=node.span)
        if isinstance(node, ast.Literal):
            shape = len(node.value) if node.kind == "string" else None
            result = ir.Expression(node.span, ir.Type(node.kind), ir.Stage.STATIC, "literal",
                                   value=node.value, known=True, shape=shape)
        elif isinstance(node, ast.Name):
            binding = self.binding(node.identifier, node)
            result = ir.Expression(node.span, binding.symbol.type, binding.stage, "load",
                                   value=binding.value, symbol=binding.symbol, known=binding.known,
                                   shape=binding.shape, dependencies=frozenset({binding.symbol.id}) | binding.alias_dependencies)
        elif isinstance(node, ast.Unary):
            operand = self.expression(node.operand)
            operator = node.operator
            if operator == "!":
                if operand.type not in (ir.Type("bool"), ir.Type("qubit")):
                    self.fail("Q2001", "! requires a Boolean or qubit predicate", node)
            elif operand.type != ir.Type("int"):
                self.fail("Q2001", "unary numeric operators require classical integers", node)
            if operand.stage == ir.Stage.RUNTIME and operator != "!":
                self.fail("Q2003", "arithmetic on measurement results is deferred", node)
            value = None
            if operand.known:
                value = not operand.value if operator == "!" else (-operand.value if operator == "-" else operand.value)
            result = self.make(node, operand.type, operand.stage, "unary", (operand,),
                               value=value, known=operand.known, operator=operator)
        elif isinstance(node, ast.Binary):
            if node.operator == "in" and isinstance(node.left, ast.ArrayLiteral) and not node.left.elements:
                right = self.expression(node.right, ir.Type("int", True) if isinstance(node.right, ast.ArrayLiteral) and not node.right.elements else None)
                if not is_sequence(right.type):
                    self.fail("Q2001", "the right operand of in must be an array or string", node.right)
                left = self.expression(node.left, ir.Type(right.type.element.classical.name, True))
                result = self.binary(node, left, right)
                return self.coerce(result, expected, node) if expected else result
            left = self.expression(node.left)
            shorted = left.type == ir.Type("bool") and left.known and (
                (node.operator == "&&" and not left.value) or (node.operator == "||" and left.value))
            before_right, before_effects = self.snapshot(), set(self.effects)
            self.deferred_faults += int(shorted)
            try:
                empty_type = None
                if node.operator == "in" and isinstance(node.right, ast.ArrayLiteral) and not node.right.elements:
                    empty_type = ir.Type((left.type.element if is_sequence(left.type) else left.type).classical.name, True)
                right = self.expression(node.right, empty_type)
            finally:
                self.deferred_faults -= int(shorted)
                if shorted:
                    self.restore(before_right)
                    self.effects = before_effects
            result = self.binary(node, left, right)
            if shorted and right.type == ir.Type("bool"):
                result = replace(result, stage=ir.Stage.STATIC, known=True, value=left.value,
                                 dependencies=left.dependencies, effects=left.effects)
        elif isinstance(node, ast.Call):
            result = self.call(node, expected, allow_prepare)
        elif isinstance(node, ast.ArrayLiteral):
            if expected is not None and not expected.array:
                self.fail("Q2001", "array literal requires an array type", node)
            if not node.elements and expected is None:
                self.fail("Q2001", "empty array literal needs a declared array type", node)
            element_type = expected.element if expected else None
            elements = []
            for child in node.elements:
                item = self.expression(child, element_type)
                if element_type is None:
                    element_type = item.type
                if item.type.array or item.type.name == "void":
                    self.fail("Q2001", "nested and void arrays are not supported", child)
                elements.append(item)
            type_ = ir.Type(element_type.name, True)
            stage = ir.Stage.QUANTUM if type_.quantum else _merge_stage(elements)
            result = self.make(node, type_, stage, "array", tuple(elements), shape=len(elements),
                               known=all(item.known for item in elements),
                               value=tuple(item.value for item in elements))
        elif isinstance(node, ast.NewArray):
            element_type = self.type(node.element_type)
            length = self.expression(node.length)
            self.require_static_integer(length, node.length, "array length")
            if length.known and length.value < 0:
                self.fail("Q4001", "array length cannot be negative", node.length)
            result = self.make(node, ir.Type(element_type.name, True),
                               ir.Stage.QUANTUM if element_type.quantum else ir.Stage.STATIC,
                               "new_array", (length,), shape=length.value if length.known else None)
        elif isinstance(node, ast.Index):
            collection, index = self.expression(node.collection), self.expression(node.index)
            if not collection.type.array and collection.type.name not in {"string", "qustring"}:
                self.fail("Q2001", "indexing requires an array or string", node.collection)
            self.require_static_integer(index, node.index, "index")
            if index.known and (index.value < 0 or (collection.shape is not None and index.value >= collection.shape)):
                self.fail("Q4001", "index is outside the collection", node.index)
            known = collection.known and index.known
            result = self.make(node, collection.type.element, collection.stage, "index", (collection, index),
                               known=known, value=collection.value[index.value] if known else None)
            if result.type.name in {"string", "qustring"} and result.known:
                result = replace(result, shape=len(result.value))
        elif isinstance(node, ast.Member):
            receiver = self.expression(node.receiver)
            if node.name != "Length" or (not receiver.type.array and receiver.type.name not in {"string", "qustring"}):
                self.fail("Q2001", "only arrays and strings have a .Length property", node)
            result = self.make(node, ir.Type("int"), ir.Stage.STATIC, "length", (receiver,),
                               known=receiver.shape is not None, value=receiver.shape)
        else:
            raise AssertionError(f"unhandled expression: {type(node).__name__}")
        return self.coerce(result, expected, node) if expected is not None else result

    def make(self, node, type_, stage, op, arguments=(), *, value=None, known=False, shape=None, operator=None):
        dependencies = frozenset().union(*(arg.dependencies for arg in arguments))
        effects = frozenset().union(*(arg.effects for arg in arguments))
        # Operators have a dedicated op suffix; value remains available for constants.
        return ir.Expression(node.span, type_, stage, f"{op}:{operator}" if operator else op,
                             arguments, value, known=known, shape=shape,
                             dependencies=dependencies, effects=effects)

    def coerce(self, value, target, node):
        if value.type == target:
            return value
        if not target.quantum or value.type != target.classical:
            self.fail("Q2001", f"cannot use {value.type} where {target} is required", node)
        if value.stage != ir.Stage.STATIC:
            self.fail("Q2003", "only construction-time classical values can initialize quantum data", node)
        if value.known:
            values = value.value if target.array else (value.value,)
            try:
                for item in values:
                    if target.name == "quint":
                        SignedInteger(self.config.quint_bits).encode(item)
                    elif target.name == "quchar":
                        TextEncoding(self.config.alphabet, self.config.qustring_capacity).encode_character(item)
                    elif target.name == "qustring":
                        TextEncoding(self.config.alphabet, self.config.qustring_capacity).encode_string(item)
            except ValueError as error:
                self.fail("Q2001", str(error), node)
        return self.make(node, target, ir.Stage.QUANTUM, "lift", (value,), shape=value.shape)

    def require_static_integer(self, value, node, purpose):
        if value.stage != ir.Stage.STATIC:
            self.fail("Q2003", f"{purpose} must be known during circuit construction", node)
        if value.type != ir.Type("int"):
            self.fail("Q2001", f"{purpose} must be a classical integer", node)

    def binary(self, node, left, right):
        operator = node.operator
        if operator == "in":
            try:
                pattern_is_element(left.type, right.type)
            except ValueError as error:
                self.fail("Q2001", str(error), node)
            if ir.Stage.RUNTIME in {left.stage, right.stage}:
                self.fail("Q2003", "membership on runtime-classical data is deferred", node)
            stage = _merge_stage((left, right))
            known = stage == ir.Stage.STATIC and left.known and right.known
            return self.make(node, ir.Type("qubit" if stage == ir.Stage.QUANTUM else "bool"), stage,
                             "membership", (left, right), known=known,
                             value=matches(left.value, right.value, left.type, right.type) if known else None)
        if left.type.quantum or right.type.quantum:
            target = left.type if left.type.quantum else right.type
            left, right = self.coerce(left, target, node.left), self.coerce(right, target, node.right)
        if left.type != right.type or left.type.array:
            self.fail("Q2001", "operator requires matching scalar operand types", node)
        base = left.type.classical.name
        stage = _merge_stage((left, right))
        if operator in {"&&", "||"} and left.stage == ir.Stage.RUNTIME and any(
                effect == "measure" or effect.startswith("write:") for effect in right.effects):
            self.fail("Q2004", "measurement or global writes in a short-circuited runtime operand are not supported; perform them separately", node.right)
        if operator in {"&&", "||"}:
            if base != "bool":
                self.fail("Q2001", "Boolean operators require Boolean operands", node)
            type_ = left.type
        elif operator in {"==", "!=", "<", "<=", ">", ">="}:
            if base == "void" or (operator not in {"==", "!="} and base != "int"):
                self.fail("Q2001", "this comparison is not supported for these operands", node)
            type_ = ir.Type("qubit" if stage == ir.Stage.QUANTUM else "bool")
        else:
            if base != "int" or (stage == ir.Stage.QUANTUM and operator != "+"):
                self.fail("Q2001", "unsupported arithmetic operator for these operands", node)
            if stage == ir.Stage.RUNTIME:
                self.fail("Q2003", "arithmetic on measurement results is deferred", node)
            type_ = left.type
        known = left.known and right.known
        value = None
        if known:
            a, b = left.value, right.value
            if operator in {"/", "%"} and b == 0:
                if not self.deferred_faults:
                    self.fail("Q4001", "division by zero", node)
                return self.make(node, type_, stage, "binary", (left, right), operator=operator)
            if operator == "+": value = a + b
            elif operator == "-": value = a - b
            elif operator == "*": value = a * b
            elif operator in {"/", "%"}:
                quotient = (abs(a) // abs(b)) * (-1 if (a < 0) != (b < 0) else 1)
                value = quotient if operator == "/" else a - quotient * b
            elif operator == "&&": value = a and b
            elif operator == "||": value = a or b
            elif operator == "==": value = a == b
            elif operator == "!=": value = a != b
            elif operator == "<": value = a < b
            elif operator == "<=": value = a <= b
            elif operator == ">": value = a > b
            elif operator == ">=": value = a >= b
            if type(value) is int and value.bit_length() > 4096:
                # Avoid unbounded constant folding here; elaboration owns evaluation.
                known, value = False, None
        return self.make(node, type_, stage, "binary", (left, right), value=value, known=known, operator=operator)

    def call(self, node, expected, allow_prepare):
        if not isinstance(node.callee, ast.Name):
            self.fail("Q2002", "only named functions and builtins can be called", node.callee)
        name = node.callee.identifier
        if name == Builtin.SEARCH:
            if len(node.arguments) != 2 or not isinstance(node.arguments[1], ast.Name):
                self.fail("Q2001", "search requires a collection and a named oracle function", node)
            if self.dynamic_depth or self.coherent_depth or self.dynamic_outers:
                self.fail("Q2004", "search cannot prepare state under dynamic control", node)
            collection = self.expression(node.arguments[0])
            if not is_sequence(collection.type):
                self.fail("Q2001", "search requires an array or string", node)
            if collection.stage == ir.Stage.RUNTIME:
                self.fail("Q2003", "search cannot use runtime-classical collections", node)
            quantum_name = {v: k for k, v in ir.QUANTUM_TO_CLASSICAL.items()}[collection.type.element.classical.name]
            element_type = ir.Type(quantum_name)
            oracle_name = node.arguments[1].identifier
            oracle = self.functions.get(oracle_name)
            if oracle is None:
                self.fail("Q2002", f"unknown search oracle {oracle_name!r}", node.arguments[1])
            if (len(oracle.parameters) != 1 or self.type(oracle.parameters[0].type) != element_type
                    or self.type(oracle.return_type, allow_void=True) != ir.Type("qubit")):
                self.fail("Q2001", f"search oracle must take one {element_type} parameter and return qubit", node)
            instance = self.function_instance(oracle_name, ((ir.Stage.QUANTUM, None),))
            for effect in instance.effects:
                if effect in {"measure", "prepare", "search"} or effect.startswith("write:"):
                    self.fail("Q2004", "search oracle must be a pure basis predicate without measurement, preparation, search, or global writes", node)
                if effect.startswith("read:"):
                    identifier = int(effect.split(":")[1])
                    binding = next(b for b in self.scopes[0].values() if b.symbol.id == identifier)
                    if binding.stage != ir.Stage.STATIC:
                        self.fail("Q2004", "search oracle captures must be construction-time classical values", node)
            self.effects.update(instance.effects | {"prepare", "search"})
            value = self.make(node, element_type, ir.Stage.QUANTUM, "search", (collection,), value=instance.key)
            return replace(value, effects=value.effects | instance.effects | {"prepare", "search"})
        if name == Builtin.SUPERPOSITION:
            if node.arguments or not allow_prepare or expected not in (ir.Type("qubit"), ir.Type("quint")):
                self.fail("Q2001", "superposition() requires an initializing qubit or quint declaration", node)
            if self.coherent_depth:
                self.fail("Q2004", "cannot prepare a superposition inside a quantum condition", node)
            self.effects.add("prepare")
            return ir.Expression(node.span, expected, ir.Stage.QUANTUM, "superposition",
                                 effects=frozenset({"prepare"}))
        if name == Builtin.MEASURE:
            if len(node.arguments) != 1:
                self.fail("Q2001", "measure requires one quantum argument", node)
            if self.if_depth:
                self.fail("Q2004", "measurement is not allowed in conditional bodies, including through function calls", node)
            argument = self.expression(node.arguments[0])
            if not argument.type.quantum:
                self.fail("Q2001", "measure requires quantum data", node.arguments[0])
            self.effects.add("measure")
            value = self.make(node, argument.type.classical, ir.Stage.RUNTIME, "measure", (argument,), shape=argument.shape)
            return replace(value, effects=value.effects | {"measure"})
        if name in (Builtin.ROTATE_LEFT, Builtin.ROTATE_RIGHT):
            if len(node.arguments) != 2:
                self.fail("Q2001", f"{name} requires a quint and a rotation count", node)
            value = self.expression(node.arguments[0], ir.Type("quint"))
            count = self.expression(node.arguments[1])
            self.require_static_integer(count, node.arguments[1], "rotation count")
            if count.known and count.value < 0:
                self.fail("Q2001", "rotation count cannot be negative", node.arguments[1])
            return self.make(node, ir.Type("quint"), ir.Stage.QUANTUM, str(name), (value, count))
        if name not in self.functions:
            self.fail("Q2002", f"unknown function {name!r}", node.callee,
                      help=self.suggestion(name, set(self.functions) | set(Builtin)))
        function = self.functions[name]
        if len(node.arguments) != len(function.parameters):
            self.fail("Q2001", f"{name} expects {len(function.parameters)} arguments", node)
        arguments = tuple(self.expression(argument, self.type(parameter.type))
                          for argument, parameter in zip(node.arguments, function.parameters, strict=True))
        instance = self.function_instance(name, tuple((argument.stage, argument.shape) for argument in arguments), arguments)
        if self.coherent_depth and "prepare" in instance.effects:
            self.fail("Q2004", "this helper prepares quantum state inside a quantum condition", node)
        self.effects.update(instance.effects)
        value = self.make(node, instance.return_type, instance.return_stage, "call", arguments,
                          shape=instance.return_shape, value=instance.key)
        reads = frozenset(int(effect.split(':')[1]) for effect in instance.effects if effect.startswith('read:'))
        return replace(value, effects=value.effects | instance.effects, dependencies=value.dependencies | reads)

    def block(self, node, new_scope=True):
        if new_scope:
            with self.scope():
                return self.block(node, new_scope=False)
        statements = []
        returns = False
        for source in node.statements:
            statement, completed = self.statement(source)
            statements.append(statement)
            returns = returns or completed
        return ir.Block(node.span, tuple(statements), returns)

    def statement(self, node):
        self.step(node)
        if isinstance(node, ast.Block):
            block = self.block(node)
            return ir.Statement(node.span, "block", blocks=(block,)), block.returns
        if isinstance(node, ast.Input):
            binding = self.scopes[0][node.name]
            binding.initialized = True
            return ir.Statement(node.span, "input", symbol=binding.symbol), False
        if isinstance(node, ast.Declaration):
            type_ = self.type(node.type)
            value = self.expression(node.initializer, type_, allow_prepare=True)
            if self.function.name == "$script" and len(self.scopes) == 1:
                binding = self.scopes[0][node.name]
                symbol = binding.symbol
                binding.initialized = True
                binding.stage, binding.known, binding.value, binding.shape = value.stage, value.known, value.value, value.shape
            else:
                symbol = self.declare(node.name, type_, value, node)
            return ir.Statement(node.span, "let", (value,), symbol=symbol), False
        if isinstance(node, (ast.Assignment, ast.Update)):
            target = self.expression(node.target)
            binding = self.mutable_target(node.target)
            if isinstance(node, ast.Update):
                if target.type != ir.Type("int") or target.stage != ir.Stage.STATIC:
                    self.fail("Q2001", "++ and -- require construction-time classical integers", node)
                operand = ir.Expression(node.span, ir.Type("int"), ir.Stage.STATIC, "literal", value=1, known=True)
                proxy = ast.Binary(node.span, "+" if node.operator == "++" else "-", node.target, ast.Literal(node.span, "int", 1))
                value = self.binary(proxy, target, operand)
            elif node.operator == "=":
                value = self.expression(node.value, target.type)
            else:
                right = self.expression(node.value)
                proxy = ast.Binary(node.span, node.operator[0], node.target, node.value)
                value = self.binary(proxy, target, right)
            # RHS calls can replace the shared global analysis environment.
            binding = self.mutable_target(node.target)
            if target.type.array and target.shape is not None and value.shape is not None and target.shape != value.shape:
                self.fail("Q2001", "array assignment cannot change its fixed length", node)
            if isinstance(node.target, ast.Name):
                binding.stage, binding.known = value.stage, value.known
                binding.value, binding.shape = value.value, value.shape
            else:
                # An indexed write changes the aggregate stage; keep its fixed shape.
                binding.stage = _merge_stage((target, value))
                binding.known, binding.value = False, None
            return ir.Statement(node.span, "assign", (target, value), operator=node.operator), False
        if isinstance(node, ast.ExpressionStatement):
            value = self.expression(node.expression)
            if not isinstance(node.expression, ast.Call):
                self.fail("Q2001", "standalone expressions must be function calls", node)
            return ir.Statement(node.span, "expr", (value,)), False
        if isinstance(node, ast.Return):
            if self.dynamic_depth:
                self.fail("Q2005", "return inside a quantum or runtime branch is deferred", node)
            if self.function.name == "$script":
                value = self.expression(node.value) if node.value is not None else None
                type_ = value.type if value else ir.Type("void")
                if type_.quantum:
                    self.fail("Q2005", "script output must be classical data; use measure() explicitly", node)
                if self.script_return_seen and self.return_type != type_:
                    self.fail("Q2005", "script returns must have one consistent type; cannot mix values and void", node)
                self.script_return_seen, self.return_type = True, type_
                if value:
                    self.return_values.append(value)
                return ir.Statement(node.span, "return", (value,) if value else ()), True
            if node.value is None:
                if self.return_type != ir.Type("void"):
                    self.fail("Q2005", "this function must return a value", node)
                self.exit_globals.append(self.snapshot()[0])
                return ir.Statement(node.span, "return"), True
            if self.return_type == ir.Type("void"):
                self.fail("Q2005", "void functions cannot return a value", node)
            value = self.expression(node.value, self.return_type)
            self.exit_globals.append(self.snapshot()[0])
            self.return_values.append(value)
            return ir.Statement(node.span, "return", (value,)), True
        if isinstance(node, ast.If):
            return self.if_statement(node)
        if isinstance(node, ast.While):
            self.invalidate_loop_constants()
            condition = self.loop_condition(node.condition)
            body = self.block(node.body)
            self.loop_condition(node.condition)  # body cannot change the control stage
            self.invalidate_loop_constants()
            return ir.Statement(node.span, "while", (condition,), (body,)), False
        if isinstance(node, ast.For):
            with self.scope():
                initialization = () if node.initializer is None else (self.statement(node.initializer)[0],)
                self.invalidate_loop_constants()
                condition = self.loop_condition(node.condition) if node.condition else ir.Expression(
                    node.span, ir.Type("bool"), ir.Stage.STATIC, "literal", value=True, known=True)
                body = self.block(node.body)
                update = () if node.update is None else (self.statement(node.update)[0],)
                if node.condition:
                    self.loop_condition(node.condition)
                self.invalidate_loop_constants()
                blocks = (ir.Block(node.span, initialization), body, ir.Block(node.span, update))
                return ir.Statement(node.span, "for", (condition,), blocks), False
        if isinstance(node, ast.Foreach):
            collection = self.expression(node.collection)
            if not is_sequence(collection.type):
                self.fail("Q2001", "foreach requires an array or string", node.collection)
            type_ = self.type(node.type)
            if type_ != collection.type.element:
                self.fail("Q2001", "foreach binding must match the element type", node.type)
            self.invalidate_loop_constants()
            with self.scope():
                element = ir.Expression(node.span, type_, collection.stage, "element")
                symbol = self.declare(node.name, type_, element, node, readonly=True,
                                      alias_dependencies=collection.dependencies)
                body = self.block(node.body)
            self.invalidate_loop_constants()
            return ir.Statement(node.span, "foreach", (collection,), (body,), symbol=symbol), False
        raise AssertionError(f"unhandled statement: {type(node).__name__}")

    def mutable_target(self, node):
        if isinstance(node, ast.Name):
            binding = self.binding(node.identifier, node)
        elif isinstance(node, ast.Index) and isinstance(node.collection, ast.Name):
            binding = self.binding(node.collection.identifier, node.collection)
            if not binding.symbol.type.array:
                self.fail("Q2001", "only array elements support indexed assignment in V1", node)
        else:
            self.fail("Q2001", "assignment requires a variable or an array element", node)
        if binding.symbol.readonly:
            self.fail("Q2004", f"{binding.symbol.name!r} is a read-only parameter or iteration binding", node)
        if binding.symbol.id in self.protected:
            self.fail("Q2004", f"{binding.symbol.name!r} is protected by an active quantum condition or read-only borrow", node)
        if binding.symbol.id in self.dynamic_outers and not binding.symbol.type.quantum:
            self.fail("Q2004", "dynamic branches cannot change outer classical state in V1", node)
        if binding.symbol.id in self.global_ids:
            self.effects.add(f"write:{binding.symbol.id}")
        return binding

    def condition(self, node):
        value = self.expression(node)
        if value.type not in (ir.Type("bool"), ir.Type("qubit")):
            self.fail("Q2001", "conditions require bool or qubit, not numeric truthiness", node)
        return value

    def loop_condition(self, node):
        value = self.condition(node)
        if value.stage != ir.Stage.STATIC:
            self.fail("Q2003", "loop condition must be known during circuit construction", node)
        return value

    def invalidate_loop_constants(self):
        for scope in self.scopes:
            for binding in scope.values():
                if not binding.symbol.readonly and not binding.symbol.type.quantum:
                    binding.known, binding.value = False, None

    def if_statement(self, node):
        condition = self.condition(node.condition)
        if condition.stage == ir.Stage.QUANTUM and any(effect in {"prepare", "measure"} or effect.startswith("write:") for effect in condition.effects):
            self.fail("Q2004", "quantum predicates must be free of preparation and measurement", node.condition)
        before = self.snapshot()
        old_if, old_coherent = self.if_depth, self.coherent_depth
        old_dynamic = self.dynamic_depth
        old_outers, old_protected = self.dynamic_outers, self.protected
        self.if_depth += 1
        if condition.stage != ir.Stage.STATIC:
            self.dynamic_depth += 1
            self.dynamic_outers = old_outers | {binding.symbol.id for scope in self.scopes for binding in scope.values()}
        if condition.stage == ir.Stage.QUANTUM:
            self.coherent_depth += 1
            self.protected = old_protected | condition.dependencies
        try:
            then = self.block(node.then_block)
            then_state = self.snapshot()
            self.restore(before)
            if isinstance(node.otherwise, ast.If):
                otherwise, returns = self.if_statement(node.otherwise)
                other = ir.Block(node.otherwise.span, (otherwise,), returns)
            elif node.otherwise:
                other = self.block(node.otherwise)
            else:
                other = ir.Block(node.span, ())
            other_state = self.snapshot()
        finally:
            self.if_depth, self.coherent_depth = old_if, old_coherent
            self.dynamic_depth = old_dynamic
            self.dynamic_outers, self.protected = old_outers, old_protected
        self.restore(before)
        for level, scope in enumerate(self.scopes):
            for name, binding in scope.items():
                a, b = then_state[level][name], other_state[level][name]
                if condition.stage == ir.Stage.STATIC and condition.known:
                    chosen = a if condition.value else b
                    binding.stage, binding.known = chosen.stage, chosen.known
                    binding.value, binding.shape = chosen.value, chosen.shape
                    continue
                if a.stage != b.stage:
                    binding.stage = ir.Stage.RUNTIME if ir.Stage.RUNTIME in {a.stage, b.stage} else a.stage
                else:
                    binding.stage = a.stage
                binding.known = a.known and b.known and a.value == b.value
                binding.value = a.value if binding.known else None
                if condition.stage != ir.Stage.STATIC and a.shape != b.shape:
                    self.fail("Q2004", "dynamic branches must agree on collection/string shape", node)
                binding.shape = a.shape if a.shape == b.shape else None
        returns = then.returns and other.returns
        if condition.stage == ir.Stage.STATIC and condition.known:
            returns = then.returns if condition.value else other.returns
        return ir.Statement(node.span, "if", (condition,), (then, other)), returns


def analyze(program: ast.Program, config: CompilerConfig | None = None) -> ir.Program:
    """Validate names/types/stages/effects and produce IR; cleanup remains unchecked."""
    return Checker(program, config or CompilerConfig()).run()
