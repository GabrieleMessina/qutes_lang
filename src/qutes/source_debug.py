"""Source stops on the verified physical circuit, with one persistent simulated shot."""
from dataclasses import dataclass
import random

from qutes import ir
from qutes.backend_ops import applications
from qutes.checker import analyze
from qutes.config import CompilerConfig
from qutes.construction import Constructor
from qutes.debug_state import step
from qutes.diagnostics import DiagnosticError, Span
from qutes.gates import Measurement
from qutes.lowering import Lowerer
from qutes.parser import parse
from qutes.physical import physical_program


class MarkedConstructor(Constructor):
    inside_search = False

    def statement(self, statement):
        if statement.op != "block" and not self.inside_search:
            self.output.append(ir.Statement(statement.span, "debug_point"))
        super().statement(statement)

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
class Point:
    operation: int
    span: Span
    callers: tuple[tuple[str, Span], ...]
    conditions: tuple


class MarkedLowerer(Lowerer):
    def __init__(self, program):
        super().__init__(program)
        self.points = []
        self.callers = []

    def statement(self, statement):
        if statement.op == "debug_point":
            if len(self.points) >= 20000:
                raise DiagnosticError("QDBG", "Debug session exceeds 20,000 source stops.", statement.span)
            self.points.append(Point(len(self.scheduler.operations), statement.span,
                                     tuple(self.callers), self.conditions))
        elif statement.op == "scope" and statement.source_name:
            self.callers.append((statement.source_name, statement.span))
            try:
                super().statement(statement)
            finally:
                self.callers.pop()
        else:
            super().statement(statement)


class DebugShot:
    def __init__(self, source, filename, inputs=None, config=None, seed=None):
        config = config or CompilerConfig()
        typed = analyze(parse(source, filename), config)
        if inputs is not None and not isinstance(inputs, dict):
            raise DiagnosticError("Q2001", "script inputs must be a name-to-value mapping", typed.span)
        constructed = MarkedConstructor(typed).run({} if inputs is None else inputs)
        lowerer = MarkedLowerer(constructed)
        self.program = physical_program(lowerer.run())
        self.points = lowerer.points
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
                return {"reason": "breakpoint" if hit else mode if mode in {"entry", "pause"} else "step",
                        "frames": frames, "variables": self.variables()}
        return {}

    def frame(self, name, span):
        line, column = span.start.line, span.start.column
        prefix = self.lines[line - 1][:column - 1]
        return {"name": name, "line": line, "column": len(prefix.encode("utf-16-le")) // 2 + 1}

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
