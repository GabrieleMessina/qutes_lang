"""Small candidate circuit constructions for M1 feasibility verification.

Keep this separate from the compiler. Hand-constructed inverse cleanup here does
not constitute an automatic uncomputation synthesizer.
"""

from qiskit import QuantumCircuit
from qiskit.circuit.library import ModularAdderGate


def add_constant(width: int, amount: int) -> QuantumCircuit:
    """Add a fixed amount mod 2**width, using reversible controlled increments."""
    if type(width) is not int or width < 1 or type(amount) is not int:
        raise ValueError("expected positive integer width and integer amount")
    circuit = QuantumCircuit(width, name=f"add_{amount}")
    encoded = amount % (1 << width)
    for offset in range(width):
        if (encoded >> offset) & 1:
            for target in reversed(range(offset + 1, width)):
                circuit.mcx(list(range(offset, target)), target)
            circuit.x(offset)
    return circuit


def add_register(width: int) -> QuantumCircuit:
    """Source on low bits, distinct target on high bits; no overlapping operands."""
    circuit = QuantumCircuit(2 * width)
    circuit.append(ModularAdderGate(width), circuit.qubits)
    return circuit


def rotate_left(width: int, count: int) -> QuantumCircuit:
    if type(width) is not int or width < 1 or type(count) is not int or count < 0:
        raise ValueError("expected positive width and nonnegative rotation count")
    circuit = QuantumCircuit(width)
    for _ in range(count % width):
        for bit in range(1, width):
            circuit.swap(0, bit)
    return circuit
