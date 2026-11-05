"""Source-level circuit views. Nothing in this module changes executable schedules."""
from dataclasses import replace
import difflib

from qutes.diagnostics import DiagnosticError
from qutes.gates import Measurement
from qutes.provenance import cleanup_annotations
from qutes.qiskit_backend import append_gate, named_circuit


def unfold_depth(value):
    if value == "all":
        return value
    if isinstance(value, str) and value.isdecimal():
        value = int(value)
    if type(value) is not int or value < 0:
        raise ValueError("unfold must be a nonnegative integer or 'all'")
    return value


def view_options(unfold=0, unfold_only=None):
    unfold = unfold_depth(unfold)
    if isinstance(unfold_only, str):
        unfold_only = unfold_only.split(",")
    selectors = tuple(sorted(set(item.strip() for item in (unfold_only or ()))))
    if selectors and (not all(selectors) or unfold == 0):
        raise ValueError("unfold-only requires nonempty selector names and positive/all unfolding")
    return {"unfold": unfold, "unfold_only": list(selectors)}


class DiagramBuilder:
    def __init__(self, compilation, options):
        self.compilation = compilation
        self.program = compilation.program
        self.options = options
        self.regions = self.program.regions
        self.children = {}
        for region in self.regions:
            self.children.setdefault(region.parent, []).append(region)
        for children in self.children.values():
            children.sort(key=lambda r: (r.operation_start, r.operation_end, r.id))
        self.cleanup_counts = [int(r.kind == "cleanup") for r in self.regions]
        for region in reversed(self.regions):
            if region.parent is not None:
                self.cleanup_counts[region.parent] += self.cleanup_counts[region.id]
        self.impure_prefix = [0]
        for op in self.program.operations:
            self.impure_prefix.append(self.impure_prefix[-1] + int(isinstance(op, Measurement) or bool(op.classical_controls or op.conditions)))
        self.annotations = cleanup_annotations(self.program)
        self.annotation_by_region = {annotation["region"]: annotation for annotation in self.annotations}
        self.available = {r.kind for r in self.regions} | {r.label for r in self.regions if r.kind == "function"}
        requested = set(options["unfold_only"])
        unknown = requested - self.available
        if unknown:
            name = sorted(unknown)[0]
            suggestion = difflib.get_close_matches(name, sorted(self.available), n=1, cutoff=0.7)
            self.fail("unknown diagram selector " + repr(name) + ("; did you mean " + repr(suggestion[0]) + "?" if suggestion else "; available: " + ", ".join(sorted(self.available))))
        self.selected = {r.id for r in self.regions if r.kind in requested or (r.kind == "function" and r.label in requested)}
        self.paths = set(self.selected)
        for region in reversed(self.regions):
            if region.id in self.paths and region.parent is not None:
                self.paths.add(region.parent)
        self.work = 0
        self.limit = self.program.config.max_evaluation_steps
        self.circuit = named_circuit(self.program.qubit_count, self.program.classical_bit_count, self.program.registers)

    def fail(self, message, code="Q5003"):
        raise DiagnosticError(code, message, self.program.allocations[0].span if self.program.allocations else self._empty_span())

    def _empty_span(self):
        from qutes.diagnostics import Position, Span
        p = Position(0, 1, 1)
        return Span(self.compilation.source_path, p, p)

    def tick(self, amount=1):
        self.work += amount
        if self.work > self.limit:
            self.fail("circuit diagram expansion exceeds the construction budget; reduce --unfold or use --unfold-only", "Q4001")

    @staticmethod
    def lower_depth(depth):
        return "all" if depth == "all" else max(0, depth - 1)

    def label(self, region):
        if region.kind == "function":
            label = region.label + "()"
        elif region.kind == "cleanup":
            label = "cleanup " + region.label.lstrip("$")
        else:
            span = region.span
            source = self.compilation.source.lstrip("\ufeff")[span.start.offset:span.end.offset]
            label = " ".join(source.split()).rstrip(";")
            if region.kind == "if":
                label = label.split("{")[0].strip()
            label = label[:65] if label else region.kind
        if region.inverse:
            label += " [inverse]"
        count = self.cleanup_counts[region.id]
        if count and region.kind != "cleanup":
            label += f" (+{count} cleanup)"
        return label

    def elementary(self, circuit, operation, qargs, cargs, depth, nesting=0):
        """Expand definitions directly, budgeting before each appended instruction."""
        self.tick(1 + len(qargs) + len(cargs))
        if nesting > 128:
            self.fail("circuit decomposition nesting exceeds the diagram budget", "Q4001")
        # Control-flow remains explicit; source schedules emit its bodies separately.
        if depth == 0 or operation.name in {"measure", "barrier"}:
            circuit.append(operation, qargs, cargs)
            return
        # Some backend definitions are generated lazily and can themselves be
        # enormous. Reject a conservative expansion bound before requesting one.
        remaining = self.limit - self.work
        controls = getattr(operation, "num_ctrl_qubits", 0)
        if operation.num_qubits ** 2 > remaining or (controls and controls >= max(0, remaining).bit_length()):
            self.fail("wide gate decomposition exceeds the diagram preflight budget; reduce --unfold or increase max_evaluation_steps", "Q4001")
        definition = operation.definition
        if definition is None:
            circuit.append(operation, qargs, cargs)
            return
        if len(definition.data) > self.limit - self.work:
            self.fail("circuit diagram expansion exceeds the construction budget", "Q4001")
        circuit.global_phase += definition.global_phase
        for item in definition.data:
            qs = [qargs[definition.find_bit(bit).index] for bit in item.qubits]
            cs = [cargs[definition.find_bit(bit).index] for bit in item.clbits]
            self.elementary(circuit, item.operation, qs, cs, self.lower_depth(depth), nesting + 1)

    def operation(self, index, depth):
        operation = self.program.operations[index]
        if isinstance(operation, Measurement):
            self.tick(len(operation.qubits))
            self.circuit.measure(operation.qubits, operation.classical_bits)
            return
        # Let the existing backend construct the exact classical condition, then
        # decompose its body in-place on this fresh, presentation-only circuit.
        before = len(self.circuit.data)
        append_gate(self.circuit, operation)
        added = list(self.circuit.data[before:])
        del self.circuit.data[before:]
        for item in added:
            self.append_instruction(item.operation, item.qubits, item.clbits, depth)

    def append_instruction(self, operation, qubits, clbits, depth):
        if hasattr(operation, "blocks"):
            blocks = []
            for block in operation.blocks:
                expanded = block.copy_empty_like()
                for item in block.data:
                    self.elementary(expanded, item.operation, item.qubits, item.clbits, depth)
                blocks.append(expanded)
            self.tick()
            self.circuit.append(operation.replace_blocks(blocks), qubits, clbits)
        else:
            self.elementary(self.circuit, operation, qubits, clbits, depth)

    def pure(self, start, end):
        return self.impure_prefix[start] == self.impure_prefix[end]

    def folded(self, start, end, label):
        from qiskit import QuantumCircuit
        operations = self.program.operations[start:end]
        bits = sorted({bit for op in operations for bit in op.bits})
        if not bits:
            return
        mapping = {bit: i for i, bit in enumerate(bits)}
        local = QuantumCircuit(len(bits))
        for op in operations:
            self.tick(1 + len(op.bits))
            append_gate(local, replace(op, targets=tuple(mapping[b] for b in op.targets),
                inputs=tuple(mapping[b] for b in op.inputs),
                controls=tuple((mapping[b], value) for b, value in op.controls)))
        self.circuit.append(local.to_gate(label=label), bits)

    def raw(self, start, end, depth, label=None):
        index = start
        while index < end:
            if label and depth == 0 and self.pure(index, index + 1):
                stop = index + 1
                while stop < end and self.pure(stop, stop + 1):
                    stop += 1
                self.folded(index, stop, label + " (part)")
                index = stop
            else:
                self.operation(index, depth)
                index += 1

    def contents(self, parent, start, end, depth, label=None):
        cursor = start
        for child in self.children.get(parent, ()):
            self.raw(cursor, child.operation_start, depth, label)
            self.region(child, depth)
            cursor = child.operation_end
        self.raw(cursor, end, depth, label)

    def region(self, region, depth):
        if region.id in self.selected:
            requested = self.options["unfold"]
            depth = "all" if "all" in (depth, requested) else max(depth, requested)
        expanded = depth != 0 or region.id in self.paths
        label = self.label(region)
        if not expanded and self.pure(region.operation_start, region.operation_end):
            self.folded(region.operation_start, region.operation_end, label)
        else:
            child_depth = self.lower_depth(depth) if expanded else depth
            # Mixed regions cannot become gates; their reversible segments can.
            self.contents(region.id, region.operation_start, region.operation_end, child_depth,
                          label if not expanded else None)
        if region.kind == "cleanup":
            event = self.annotation_by_region.get(region.id)
            if event is not None:
                self.tick(len(event["zero_bits"]) + len(event["restored_bits"]))
                self.circuit.barrier(*event["zero_bits"], label="clean |0>: " + event["name"].lstrip("$"))
                if event["restored_bits"]:
                    self.circuit.barrier(*event["restored_bits"], label="inputs restored")

    def build(self):
        depth = 0 if self.options["unfold_only"] else self.options["unfold"]
        self.contents(None, 0, len(self.program.operations), depth)
        return self.circuit


def build_diagram(compilation, *, unfold=0, unfold_only=None):
    return DiagramBuilder(compilation, view_options(unfold, unfold_only)).build()
