"""Source stops on the verified physical circuit, with one persistent simulated shot."""
from dataclasses import dataclass
import json
import random

from qutes import ir
from qutes.backend_ops import applications
from qutes.checker import analyze
from qutes.config import CompilerConfig
from qutes.construction import Constructor
from qutes.debug_state import step
from qutes.diagnostics import DiagnosticError, Span
from qutes.gates import Measurement
from qutes.lowering import Lowerer, Result
from qutes.parser import parse
from qutes.physical import physical_program
from qutes.serialization import json_text


@dataclass(frozen=True)
class QuantumArrayElements:
    type: ir.Type
    elements: tuple


class MarkedConstructor(Constructor):
    inside_search = False

    def __init__(self, program):
        super().__init__(program)
        self.names = {p.id: p.name for f in program.functions for p in f.parameters}
        self.caller_cells = []
        self.marker_bindings = {}

    def visible_cells(self):
        # Inner declarations and parameters shadow outer bindings with the same name.
        return {self.names[i]: cell for i, cell in self.environment.items() if i in self.names}

    def call(self, function, arguments, source, locations=()):
        self.caller_cells.append(self.visible_cells())
        try:
            return super().call(function, arguments, source, locations)
        finally:
            self.caller_cells.pop()

    @staticmethod
    def bindings(cells):
        rows = []
        for name, cell in cells.items():
            value = cell.value
            if value.op == "array_ref":
                view = value.value
                # Capture element expressions now: a mutable slice may be rebound later.
                elements = tuple(view.owner.elements[p] for p in view.positions[:16])
                if value.type.quantum and len(view.positions) <= 16:
                    rows.append((name, QuantumArrayElements(value.type, elements)))
                elif not view.positions or len(view.positions) > 16:
                    rows.append((name, f"{len(view.positions)} elements"))
                rows.extend((f"{name}[{index}]", element) for index, element in enumerate(elements))
            else:
                rows.append((name, value))
        return tuple(rows)

    def statement(self, statement):
        for symbol in (statement.symbol, statement.index_symbol):
            if symbol is not None:
                self.names[symbol.id] = symbol.name
        if statement.op != "block" and not self.inside_search:
            marker = ir.Statement(statement.span, "debug_point")
            self.output.append(marker)
            self.marker_bindings[id(marker)] = tuple(self.bindings(cells) for cells in
                (*self.caller_cells, self.visible_cells()))
        super().statement(statement)
        if statement.op == "for":
            for initializer in statement.blocks[0].statements:
                if initializer.op == "let":
                    self.names.pop(initializer.symbol.id, None)

    def expression(self, expression, **kwargs):
        if expression.op != "search":
            return super().expression(expression, **kwargs)
        # Synthesized oracle calls belong to the enclosing search expression.
        previous = self.inside_search
        self.inside_search = True
        try:
            return super().expression(expression, **kwargs)
        finally:
            self.inside_search = previous


@dataclass(frozen=True)
class QuantumBinding:
    bits: tuple[int, ...]
    layout: Result


@dataclass(frozen=True)
class Point:
    operation: int
    span: Span
    callers: tuple[tuple[str, Span], ...]
    conditions: tuple
    bindings: tuple


class MarkedLowerer(Lowerer):
    def __init__(self, program, marker_bindings):
        super().__init__(program)
        self.points = []
        self.callers = []
        self.marker_bindings = marker_bindings

    def binding_value(self, expression):
        if isinstance(expression, str):
            return expression
        if isinstance(expression, QuantumArrayElements):
            bits, elements = [], []
            for element in expression.elements:
                storage = self.reference(element)
                start = len(bits)
                bits.extend(storage.bits)
                elements.append(self.snapshot_layout(storage, element.type, tuple(range(start, len(bits)))))
            return QuantumBinding(tuple(bits), Result(expression.type.classical, "array", tuple(elements)))
        if expression.type.quantum:
            source = self.reference(expression)
            layout = self.snapshot_layout(source, expression.type, tuple(range(len(source.bits))))
            return QuantumBinding(source.bits, layout)
        return self.runtime(expression)

    def statement(self, statement):
        if statement.op == "debug_point":
            if len(self.points) >= 20000:
                raise DiagnosticError("QDBG", "Debug session exceeds 20,000 source stops.", statement.span)
            frames = self.marker_bindings.pop(id(statement))
            bindings = tuple(tuple((name, self.binding_value(expr)) for name, expr in frame) for frame in frames)
            self.points.append(Point(len(self.scheduler.operations), statement.span,
                                     tuple(self.callers), self.conditions, bindings))
        elif statement.op == "scope" and statement.source_name:
            self.callers.append((statement.source_name, statement.span))
            try:
                super().statement(statement)
            finally:
                self.callers.pop()
        else:
            super().statement(statement)


class ValueDistributions:
    """Compute each visible register's marginal once for the paused shot."""

    def __init__(self, state):
        self.weights = [(basis, abs(a) ** 2) for basis, a in enumerate(state) if a]
        self.total = sum(weight for _, weight in self.weights)
        self.cache = {}
        self.children = []

    def percent(self, weight):
        percent = 100 * weight / self.total
        if 0 < percent < 0.00005:
            return "<0.0001%"
        return f"{percent:.4f}".rstrip("0").rstrip(".") + "%"

    def describe(self, layout, wires):
        key = (layout, wires)
        if key in self.cache:
            return self.cache[key]
        # A logical bit awaiting its first gate is zero even if its future
        # physical wire still belongs to another register.
        positions = [(index, wire) for index, wire in enumerate(wires) if wire is not None]
        weights = {}
        for basis, weight in self.weights:
            encoded = sum(((basis >> wire) & 1) << index for index, wire in positions)
            weights[encoded] = weights.get(encoded, 0.0) + weight
        if layout.type == ir.Type("bool"):
            summary = "  ".join(f"P({bit})={self.percent(weights.get(bit, 0))}" for bit in (0, 1))
            result = summary, None
        else:
            rows = []
            for encoded in sorted(weights, key=lambda n: (-weights[n], n)):
                try:
                    value = layout.decode(encoded)
                    label = json.dumps(value, ensure_ascii=False, separators=(",", ":"))
                except ValueError:
                    label = f"<invalid encoding {encoded:#b}>"
                rows.append({"name": label, "value": self.percent(weights[encoded])})
            summary = "  ".join(f"P({r['name']})={r['value']}" for r in rows[:2])
            if len(rows) > 2:
                summary += f"  (+{len(rows) - 2} more)"
            result = summary, len(self.children)
            self.children.append(rows)
        self.cache[key] = result
        return result


class DebugShot:
    def __init__(self, source, filename, inputs=None, config=None, seed=None):
        config = config or CompilerConfig()
        typed = analyze(parse(source, filename), config)
        if inputs is not None and not isinstance(inputs, dict):
            raise DiagnosticError("Q2001", "script inputs must be a name-to-value mapping", typed.span)
        constructor = MarkedConstructor(typed)
        constructed = constructor.run({} if inputs is None else inputs)
        lowerer = MarkedLowerer(constructed, constructor.marker_bindings)
        self.program = physical_program(lowerer.run())
        self.points = lowerer.points
        self.wires = self.program.wire_allocation.lookup()
        self.first_owner = {}
        for interval in self.program.wire_allocation.intervals:
            self.first_owner.setdefault(interval.physical, interval)
        self.lines = source.split("\n")
        self.cursor = -1
        self.previous = None
        self.operation = self.memory = 0
        self.rng = random.Random(seed)
        width = self.program.qubit_count
        if width > min(12, config.max_simulation_qubits):
            raise DiagnosticError("QDBG", "Circuit exceeds the stepping limit of 12 physical qubits or the project's simulation limit. Use Run Without Debugging.", typed.span)
        self.gates = []
        work = 0
        for operation in self.program.operations:
            gates = () if isinstance(operation, Measurement) else tuple(applications(operation))
            work += len(operation.qubits) if isinstance(operation, Measurement) else sum(len(g.qubits) for g in gates)
            if work * (1 << width) > 20_000_000:
                raise DiagnosticError("QDBG", "Circuit exceeds the interactive simulation budget. Use Run Without Debugging.", typed.span)
            self.gates.append(gates)
        self.state = [0j] * (1 << width)
        self.state[0] = 1
        self.measured = set()

    def execute_to(self, end):
        if not self.operation <= end <= len(self.gates):
            raise ValueError("This circuit has no stable source-step mapping. Use Run Without Debugging.")
        while self.operation < end:
            op = self.program.operations[self.operation]
            self.memory = step(self.state, op, self.gates[self.operation], self.memory, self.rng)
            if isinstance(op, Measurement):
                self.measured.update(op.classical_bits)
            self.operation += 1

    def advance(self, mode, breakpoints, depth, limit=256):
        for _ in range(limit):
            self.cursor += 1
            if self.cursor == len(self.points):
                self.execute_to(len(self.gates))
                return {"done": True, "result": self.program.result.decode(self.memory)}
            point = self.points[self.cursor]
            self.execute_to(point.operation)
            if not all(test.evaluate(self.memory) == expected for test, expected in point.conditions):
                continue
            previous = self.previous
            same_line = (previous and point.callers == previous.callers and
                         point.span.start.line == previous.span.start.line and point.span != previous.span)
            self.previous = point
            if same_line:
                continue
            hit = point.span.start.line in breakpoints
            level = len(point.callers)
            if hit or mode in {"entry", "stepIn", "pause"} or (mode == "next" and level <= depth) or (mode == "stepOut" and level < depth):
                frames = []
                span = point.span
                for name, caller_span in reversed(point.callers):
                    frames.append(self.frame(name, span))
                    span = caller_span
                frames.append(self.frame("Script", span))
                distributions = ValueDistributions(self.state)
                scopes = [self.source_scope(frame, distributions) for frame in reversed(point.bindings)]
                return {"reason": "breakpoint" if hit else mode if mode in {"entry", "pause"} else "step",
                        "frames": frames, "variables": self.variables(),
                        "sourceScopes": scopes, "distributions": distributions.children}
        return {}

    def frame(self, name, span):
        line, column = span.start.line, span.start.column
        prefix = self.lines[line - 1][:column - 1]
        return {"name": name, "line": line, "column": len(prefix.encode("utf-16-le")) // 2 + 1}

    def physical_wire(self, logical):
        intervals = self.wires.by_bit.get(logical)
        if not intervals:
            return None
        # A zero-initialized variable can be declared before its first gate.
        # Label its future wire early only when it is the wire's first owner.
        first = intervals[0]
        if self.operation < first.start and first == self.first_owner[first.physical]:
            return first.physical
        try:
            return self.wires.at(logical, self.operation)
        except ValueError:
            return None

    def before_first_use(self, logical):
        intervals = self.wires.by_bit.get(logical)
        return not intervals or self.operation < intervals[0].start

    def source_scope(self, bindings, distributions):
        rows = []
        order = [f"q[{i}]" for i in range(self.program.qubit_count)]
        for name, binding in bindings:
            row = {"name": name}
            if isinstance(binding, QuantumBinding):
                wires = tuple(self.physical_wire(bit) for bit in binding.bits)
                value = ", ".join(f"q[{wire}]" if wire is not None else "unallocated" for wire in wires)
                if all(wire is not None or self.before_first_use(bit) for bit, wire in zip(binding.bits, wires)):
                    odds, index = distributions.describe(binding.layout, wires)
                    if index is None:
                        value += "  " + odds
                    else:
                        value = odds + ("  ·  " + value if value else "")
                        row["distribution"] = index
                else:
                    value += "  ·  probabilities unavailable"
                for i, wire in enumerate(wires):
                    # More local names (including function parameters) come last.
                    if wire is not None:
                        order[wire] = name if len(wires) == 1 else f"{name}[{i}]"
            elif isinstance(binding, Result):
                value = json_text(binding.decode(self.memory))
                if len(value) > 150:
                    value = value[:149] + "…"
            else:
                value = binding
            row["value"] = value
            rows.append(row)
        return {"variables": rows, "wireOrder": list(reversed(order))}

    def variables(self):
        width = self.program.qubit_count
        active = sorted(((abs(a)**2, i, a) for i, a in enumerate(self.state) if abs(a) > 1e-12), reverse=True)
        result = []
        for probability, basis, amplitude in active[:16]:
            result.append({"name": f"|{basis:0{width}b}⟩", "value": f"{probability:.4%}   amplitude {amplitude:.5g}"})
        if len(active) > 16:
            result.append({"name": "Other basis states", "value": str(len(active) - 16)})
        for bit in sorted(self.measured):
            result.append({"name": f"c[{bit}]", "value": str(bool(self.memory & (1 << bit))).lower()})
        return result
