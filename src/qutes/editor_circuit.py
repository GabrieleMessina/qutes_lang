"""Read-only circuit inspection for source editors, in UTF-16 document offsets."""
from collections import Counter

from qutes import syntax as ast
from qutes.gates import Measurement
from qutes.parser import parse

EDITABLE_GATES = {"hadamard", "not", "phaseFlip"}


def circuit_report(compilation, limit=24):
    source, program = compilation.source, compilation.program
    offsets = [0]
    for character in source:
        offsets.append(offsets[-1] + (2 if ord(character) > 0xffff else 1))

    def bounds(span):
        return [offsets[span.start.offset], offsets[span.end.offset]] if span else None

    statements = parse(source).statements
    qubits, direct = [], {}
    insert_at = len(source)
    for statement in statements:
        if isinstance(statement, ast.Return):
            insert_at = statement.span.start.offset
            break
        if isinstance(statement, ast.Declaration) and statement.type.name == "qubit" and not (
            statement.type.array or statement.readonly
        ):
            qubits.append(statement.name)
        if not isinstance(statement, ast.ExpressionStatement):
            continue
        call = statement.expression
        if (isinstance(call, ast.Call) and isinstance(call.callee, ast.Name)
                and call.callee.identifier in EDITABLE_GATES and len(call.arguments) == 1
                and isinstance(call.arguments[0], ast.Name) and call.arguments[0].identifier in qubits):
            direct[(call.span.start.offset, call.span.end.offset)] = {
                "range": bounds(statement.span), "gate": call.callee.identifier,
                "target": call.arguments[0].identifier, "available": list(qubits)}

    def key(span):
        return (span.start.offset, span.end.offset) if span else None

    occurrences = Counter(key(op.span) for op in program.operations)
    cleanups = compilation.metadata["cleanup_annotations"]
    handoffs = compilation.metadata["wire_handoffs"]
    snapshots = {(m.operation_end, m.bits): m.span for m in program.source_mappings
                 if m.classical and m.name == "$measurement"}
    gates, suggestions = [], []
    for index, op in enumerate(program.operations[:limit]):
        measured = isinstance(op, Measurement)
        span = snapshots.get((index + 1, op.classical_bits), op.span) if measured else op.span
        cleanup = next((c["name"] for c in cleanups if c["operation_start"] <= index < c["operation_end"]), None)
        bits = set(op.qubits if measured else op.bits)
        reuse = sorted({h["physical"] for h in handoffs if h["physical"] in bits and h["operation"] <= index})
        repeated = occurrences[key(span)]
        edit = direct.get(key(span)) if not (cleanup or measured or repeated != 1 or op.controls
                                               or op.conditions or op.classical_controls) else None
        gates.append(dict(range=bounds(span), edit=edit, occurrences=repeated, cleanup=cleanup, reused= reuse))
        if index and edit and edit["gate"] == "hadamard":
            previous = gates[index - 1]["edit"]
            if (previous and previous["gate"] == "hadamard" and previous["target"] == edit["target"]
                    and program.operations[index - 1].targets == op.targets
                    and not any(h["operation"] == index for h in handoffs)
                    and not source[program.operations[index - 1].span.end.offset:span.start.offset].strip().strip(";").strip()
                    and (not suggestions or suggestions[-1]["gates"][-1] < index - 1)):
                suggestions.append(dict(gates=[index - 1, index], target=edit["target"],
                                        range=[previous["range"][0], edit["range"][1]]))
    return dict(gates=gates, suggestions=suggestions, qubits=qubits, insertAt=offsets[insert_at],
                operations=len(program.operations))
