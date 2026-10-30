"""Independent full-state and dynamic-execution checks, not compiler tests."""

import numpy as np
import pytest
from qiskit import QuantumCircuit, transpile
from qiskit.quantum_info import Operator, Statevector
from qiskit_aer import AerSimulator

from experiments.backend_probes import add_constant, add_register, rotate_left
from tests import reference as ref

pytestmark = pytest.mark.backend


def lowered(circuit):
    return transpile(circuit, basis_gates=["u", "cx"], optimization_level=0)


def equivalent(actual, expected):
    assert Statevector(actual).equiv(Statevector(expected), atol=1e-10, rtol=1e-10)


@pytest.mark.parametrize("width", range(1, 5))
def test_constant_addition_entire_operator(width):
    # Compare ALL basis columns with one global phase, not one phase per column.
    for amount in range(-(2 ** (width - 1)), 2 ** (width - 1)):
        actual = Operator(lowered(add_constant(width, amount))).data
        expected = np.zeros_like(actual)
        for value in range(2**width):
            expected[(value + amount) % (2**width), value] = 1
        np.testing.assert_allclose(actual, expected, atol=1e-10)


@pytest.mark.parametrize("width", range(1, 4))
def test_register_addition_entangled_reference(width):
    initial = ref.random_state(2 * width + 1)
    circuit = QuantumCircuit(2 * width + 1)
    circuit.compose(add_register(width), range(2 * width), inplace=True)
    actual = Statevector(initial).evolve(lowered(circuit)).data
    equivalent(actual, ref.register_sum(initial, 0, width, width))


@pytest.mark.parametrize("width", range(1, 5))
def test_rotation_with_entangled_reference(width):
    initial = ref.random_state(width + 1)
    for count in range(2 * width + 1):
        circuit = QuantumCircuit(width + 1)
        circuit.compose(rotate_left(width, count), range(width), inplace=True)
        actual = Statevector(initial).evolve(lowered(circuit)).data
        equivalent(actual, ref.rotation(initial, 0, width, count))


def test_correlated_copy_and_inverse_preserve_phase():
    width = 2
    source_with_reference = ref.random_state(width + 1)
    initial = np.zeros(2 ** (2 * width + 1), dtype=complex)
    for index, amplitude in enumerate(source_with_reference):
        initial[(index & 3) | ((index >> width) << (2 * width))] = amplitude
    circuit = QuantumCircuit(2 * width + 1)
    for bit in range(width):
        circuit.cx(bit, width + bit)
    copied = Statevector(initial).evolve(circuit).data
    expected = ref.permutation(initial, lambda index: ref.replace_field(
        index, width, width, ref.field(index, width, width) ^ ref.field(index, 0, width),
    ))
    equivalent(copied, expected)
    restored = Statevector(copied).evolve(circuit.inverse()).data
    equivalent(restored, initial)


def test_compute_use_uncompute_predicate_with_entanglement():
    # Source: bits 0-1 (signed); target: 2; scratch predicate: 3; reference: 4.
    arbitrary = ref.random_state(4)
    initial = np.zeros(32, dtype=complex)
    for index, amplitude in enumerate(arbitrary):
        initial[(index & 7) | ((index >> 3) << 4)] = amplitude
    circuit = QuantumCircuit(5)
    circuit.cx(1, 3)  # number < 0
    circuit.cx(3, 2)  # controlled update
    circuit.cx(1, 3)  # uncompute using unchanged source
    actual = Statevector(initial).evolve(circuit).data
    expected = ref.permutation(initial, lambda index: index ^ (4 if index & 2 else 0))
    equivalent(actual, expected)
    assert sum(abs(actual[index]) ** 2 for index in range(32) if index & 8) < 1e-20
    # Negative control: a missing inverse must be distinguishable from correct cleanup.
    incorrect = circuit.copy()
    incorrect.data.pop()
    assert not Statevector(initial).evolve(incorrect).equiv(Statevector(expected))


def test_computed_temporary_cleanup_before_measurement():
    # Copy x, compute temporary x+1, use its sign, undo it, then undo the copy.
    circuit = QuantumCircuit(5)
    circuit.h([0, 1])
    circuit.cx(0, 2)
    circuit.cx(1, 3)
    circuit.compose(add_constant(2, 1), [2, 3], inplace=True)
    circuit.cx(3, 4)
    circuit.compose(add_constant(2, 1).inverse(), [2, 3], inplace=True)
    circuit.cx(1, 3)
    circuit.cx(0, 2)
    actual = Statevector.from_instruction(lowered(circuit)).data
    expected = np.zeros(32, dtype=complex)
    for source in range(4):
        is_negative = ((source + 1) % 4) >= 2
        expected[source | (int(is_negative) << 4)] = 0.5
    equivalent(actual, expected)
    assert sum(abs(actual[index]) ** 2 for index in range(32) if index & 12) < 1e-20


def test_reference_rejects_information_losing_self_update():
    with pytest.raises(ValueError, match="not a reversible permutation"):
        ref.permutation(ref.random_state(3), lambda value: (2 * value) % 8)


def test_repeated_measurement_and_classical_feedforward():
    # q0 and q1 start correlated. Observe q0, then evolve it; retain both snapshots.
    circuit = QuantumCircuit(3, 4)
    circuit.h(0)
    circuit.cx(0, 1)
    circuit.measure(0, 0)
    with circuit.if_test((circuit.clbits[0], True)):
        circuit.x(2)
    circuit.x(0)
    circuit.measure(0, 1)
    circuit.measure(1, 2)
    circuit.measure(2, 3)
    # Save each post-measurement trajectory to check more than classical counts.
    circuit.save_statevector(pershot=True)
    simulator = AerSimulator(method="statevector", max_parallel_threads=1)
    result = simulator.run(
        transpile(circuit, simulator, optimization_level=0, seed_transpiler=41),
        shots=128, seed_simulator=41, memory=True,
    ).result()
    assert result.success

    initial = np.zeros(8, dtype=complex)
    initial[0] = initial[3] = 1 / np.sqrt(2)
    expected = {}
    for branch in ref.measure(ref.Branch(1.0, initial), 0, 1):
        state = ref.permutation(branch.state, lambda value: value ^ (4 if branch.snapshots[0] else 0))
        state = ref.permutation(state, lambda value: value ^ 1)
        branches = [ref.Branch(branch.probability, state, branch.snapshots)]
        for bit in (0, 1, 2):
            branches = [child for current in branches for child in ref.measure(current, bit, 1)]
        for outcome in branches:
            key = "".join(str(bit) for bit in reversed(outcome.snapshots))
            expected[key] = outcome
    assert set(expected) == {"0010", "1101"}
    assert all(np.isclose(branch.probability, 0.5) for branch in expected.values())
    assert set(result.get_counts()) == set(expected)
    for memory, state in zip(result.get_memory(), result.data()["statevector"], strict=True):
        equivalent(state, expected[memory].state)


def test_measurement_then_signed_addition_preserves_snapshot():
    width = 3
    circuit = QuantumCircuit(width, 2 * width)
    # Signed +3 wraps to -3 after +2; first snapshot must stay +3.
    circuit.x([0, 1])
    circuit.measure(range(width), range(width))
    circuit.compose(add_constant(width, 2), inplace=True)
    circuit.measure(range(width), range(width, 2 * width))
    simulator = AerSimulator(method="statevector", max_parallel_threads=1)
    result = simulator.run(transpile(circuit, simulator), shots=8, seed_simulator=41).result()
    assert result.get_counts() == {"101011": 8}


def test_repeated_unchanged_measurement_agrees():
    circuit = QuantumCircuit(1, 2)
    circuit.h(0)
    circuit.measure(0, 0)
    circuit.measure(0, 1)
    simulator = AerSimulator(method="statevector", max_parallel_threads=1)
    result = simulator.run(transpile(circuit, simulator), shots=64, seed_simulator=41).result()
    assert set(result.get_counts()) == {"00", "11"}
