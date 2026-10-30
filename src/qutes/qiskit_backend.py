"""Qiskit adapter for backend-neutral operations. Imported only on demand."""

from __future__ import annotations

from qutes.gates import Gate


def append_gate(circuit, operation: Gate):
    from qiskit.circuit.library import HGate, ModularAdderGate, SwapGate, XGate

    controls = tuple(bit for bit, _ in operation.controls)
    state = sum(int(value) << index for index, (_, value) in enumerate(operation.controls))

    def append(gate, bits, *, extra_controls=()):
        # Input bits may also be global controls. Elementary copy gates can merge
        # those controls; whole-register addition uses a decomposed constant sum
        # when that overlap occurs, avoiding duplicate Qiskit operands.
        merged = dict(operation.controls)
        for bit in extra_controls:
            if bit in merged and not merged[bit]:
                return
            merged[bit] = True
        pairs = tuple(merged.items())
        if pairs:
            encoded = sum(int(value) << index for index, (_, value) in enumerate(pairs))
            gate = gate.control(len(pairs), ctrl_state=encoded, annotated=False)
        circuit.append(gate, [*(bit for bit, _ in pairs), *bits])

    def constant(amount, extra_controls=()):
        amount %= 1 << len(operation.targets)
        for offset in range(len(operation.targets)):
            if (amount >> offset) & 1:
                for index in reversed(range(offset + 1, len(operation.targets))):
                    append(XGate(), (operation.targets[index],),
                           extra_controls=(*extra_controls, *operation.targets[offset:index]))
                append(XGate(), (operation.targets[offset],), extra_controls=extra_controls)

    kind = operation.kind
    if kind in {"x", "h"}:
        for target in operation.targets:
            append(XGate() if kind == "x" else HGate(), (target,))
    elif kind == "copy":
        for source, target in zip(operation.inputs, operation.targets):
            append(XGate(), (target,), extra_controls=(source,))
    elif kind == "add_constant":
        constant(-operation.amount if operation.inverse else operation.amount)
    elif kind == "add":
        if set(controls) & set(operation.inputs):
            for index, source in enumerate(operation.inputs):
                constant(-(1 << index) if operation.inverse else 1 << index, (source,))
        else:
            gate = ModularAdderGate(len(operation.targets))
            if operation.inverse:
                gate = gate.inverse()
            if controls:
                gate = gate.control(len(controls), ctrl_state=state, annotated=False)
            circuit.append(gate, [*controls, *operation.inputs, *operation.targets])
    elif kind == "rotate":
        count = (-operation.amount if operation.inverse else operation.amount) % len(operation.targets)
        for _ in range(count):
            for index in range(1, len(operation.targets)):
                append(SwapGate(), (operation.targets[0], operation.targets[index]))
    else:
        raise ValueError(f"unsupported operation {kind}")


def emit_gates(qubit_count: int, operations: tuple[Gate, ...] | list[Gate]):
    """Emit a coherent circuit; this is not yet the full source-program emitter."""
    from qiskit import QuantumCircuit

    circuit = QuantumCircuit(qubit_count)
    for operation in operations:
        append_gate(circuit, operation)
    return circuit
