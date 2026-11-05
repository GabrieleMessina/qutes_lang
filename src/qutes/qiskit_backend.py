"""Qiskit adapter for backend-neutral operations. Imported only on demand."""

from __future__ import annotations

from qutes.backend_ops import applications
from qutes.gates import Gate, Measurement


def classical_expression(predicate, circuit):
    from qiskit.circuit.classical import expr

    # Qiskit expression nodes may be mutable. Build fresh nodes for each tree
    # occurrence rather than sharing backend nodes from the immutable IR DAG.
    pending, values = [(predicate, False)], []
    while pending:
        node, ready = pending.pop()
        if not ready:
            pending.append((node, True))
            pending.extend((argument, False) for argument in reversed(node.arguments))
            continue
        count = len(node.arguments)
        arguments = values[-count:] if count else []
        if count:
            del values[-count:]
        if node.op == "literal": value = expr.lift(node.value)
        elif node.op == "bit": value = expr.lift(circuit.clbits[node.value])
        elif node.op == "not": value = expr.logic_not(arguments[0])
        elif node.op == "and": value = expr.logic_and(*arguments)
        elif node.op == "or": value = expr.logic_or(*arguments)
        else: value = expr.bit_xor(*arguments)
        values.append(value)
    return values[0]


def append_gate(circuit, operation: Gate):
    from qiskit.circuit.library import HGate, ModularAdderGate, SwapGate, XGate, RYGate, PhaseGate

    if operation.conditions or operation.classical_controls:
        from dataclasses import replace
        from qiskit.circuit.classical import expr
        tests = [(classical_expression(condition, circuit), expected) for condition, expected in operation.conditions]
        tests.extend((expr.lift(circuit.clbits[bit]), expected) for bit, expected in operation.classical_controls)
        tests = [test if expected else expr.logic_not(test) for test, expected in tests]
        while len(tests) > 1:
            tests = [expr.logic_and(tests[i], tests[i + 1]) if i + 1 < len(tests) else tests[i]
                     for i in range(0, len(tests), 2)]
        with circuit.if_test(tests[0]):
            append_gate(circuit, replace(operation, conditions=(), classical_controls=()))
        return

    for application in applications(operation):
        if application.kind == "add":
            gate = ModularAdderGate(len(application.targets))
            if application.inverse:
                gate = gate.inverse()
        elif application.kind in {"ry", "phase"}:
            gate = {"ry": RYGate, "phase": PhaseGate}[application.kind](application.angle)
        else:
            gate = {"x": XGate, "h": HGate, "swap": SwapGate}[application.kind]()
        if application.controls:
            gate = gate.control(len(application.controls), ctrl_state=application.control_state, annotated=False)
        circuit.append(gate, application.qubits)


def emit_gates(qubit_count: int, operations: tuple[Gate, ...] | list[Gate]):
    """Emit a measurement-free circuit; emit_operations handles full schedules."""
    from qiskit import QuantumCircuit

    circuit = QuantumCircuit(qubit_count)
    for operation in operations:
        append_gate(circuit, operation)
    return circuit


def named_circuit(qubit_count, classical_bit_count, registers=()):
    from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister

    if not registers:
        return QuantumCircuit(qubit_count, classical_bit_count)
    circuit = QuantumCircuit()
    for register in registers:
        cls = ClassicalRegister if register.classical else QuantumRegister
        circuit.add_register(cls(len(register.bits), register.name))
    assert circuit.num_qubits == qubit_count and circuit.num_clbits == classical_bit_count
    assert [b for r in registers if not r.classical for b in r.bits] == list(range(qubit_count))
    assert [b for r in registers if r.classical for b in r.bits] == list(range(classical_bit_count))
    return circuit


def emit_operations(qubit_count: int, classical_bit_count: int,
                    operations: tuple[Gate | Measurement, ...] | list[Gate | Measurement], *, registers=()):
    """Emit scheduled operations, including explicit measurements and snapshot use."""
    from qiskit import QuantumCircuit

    circuit = named_circuit(qubit_count, classical_bit_count, registers)
    for operation in operations:
        if isinstance(operation, Measurement):
            circuit.measure(operation.qubits, operation.classical_bits)
        else:
            append_gate(circuit, operation)
    return circuit
