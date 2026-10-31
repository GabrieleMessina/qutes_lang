"""Exact projected-branch checks plus emitted dynamic-circuit smoke tests."""

from dataclasses import replace

import numpy as np
import pytest
from qiskit import transpile
from qiskit.quantum_info import Statevector
from qiskit_aer import AerSimulator

from qutes.cleanup import Scheduler
from qutes.diagnostics import DiagnosticError
from qutes.gates import Gate, Measurement
from qutes.qiskit_backend import emit_gates, emit_operations
from tests.reference import Branch, field, measure, random_state, replace_field
from tests.test_cleanup import SPAN, derived, external

pytestmark = pytest.mark.backend


def branches_for(scheduler, initial=None):
    state = np.zeros(2**scheduler.qubit_count, dtype=complex)
    if initial is None:
        state[0] = 1
    else:
        state[:len(initial)] = initial
    branches = [Branch(1, state)]
    for operation in scheduler.operations:
        if isinstance(operation, Measurement):
            for bit, classical_bit in zip(operation.qubits, operation.classical_bits):
                assert all(len(branch.snapshots) == classical_bit for branch in branches)
                branches = [result for branch in branches for result in measure(branch, bit, 1)]
        else:
            circuit = emit_gates(scheduler.qubit_count, (replace(operation, classical_controls=()),))
            branches = [replace(branch, state=Statevector(branch.state).evolve(circuit).data)
                        if all(bool(branch.snapshots[bit]) == value for bit, value in operation.classical_controls)
                        else branch for branch in branches]
    return branches


def assert_basis_branch(branch, expected_index):
    expected = np.zeros_like(branch.state)
    expected[expected_index] = 1
    np.testing.assert_allclose(branch.state, expected, atol=1e-10)


def test_measurement_keeps_source_available_and_snapshot_stable():
    scheduler = Scheduler()
    value = scheduler.allocate(3, "number", SPAN)
    scheduler.initialize(value, (Gate("x", (value.bits[0], value.bits[2])),))
    before = scheduler.measure(value)
    scheduler.update(value, (Gate("add_constant", value.bits, amount=2),))
    after = scheduler.measure(value)
    assert before.classical_bits != after.classical_bits
    assert not value.released and value.version == 1
    branches = branches_for(scheduler)
    assert len(branches) == 1
    assert branches[0].snapshots == (1, 0, 1, 1, 1, 1)
    assert_basis_branch(branches[0], 7)


def test_measured_root_can_be_cleaned_while_correlated_copy_remains_live():
    scheduler = Scheduler()
    root = scheduler.allocate(1, "choice", SPAN)
    scheduler.initialize(root, (Gate("h", root.bits),))
    result = derived(scheduler, root, "output")
    scheduler.measure(root)
    scheduler.release(root)
    branches = branches_for(scheduler)
    assert len(branches) == 2
    for branch in branches:
        assert branch.probability == pytest.approx(0.5)
        assert_basis_branch(branch, branch.snapshots[0] << result.bits[0])


def test_snapshot_at_new_version_can_reconstruct_old_dependency():
    scheduler = Scheduler()
    root = scheduler.allocate(2, "number", SPAN)
    scheduler.initialize(root, (Gate("h", root.bits),))
    result = derived(scheduler, root, "old_value", 1)
    scheduler.update(root, (Gate("add_constant", root.bits, amount=2),))
    scheduler.measure(root)
    scheduler.release(root)
    scheduler.release(result)
    branches = branches_for(scheduler)
    assert len(branches) == 4
    for branch in branches:
        assert branch.probability == pytest.approx(0.25)
        assert_basis_branch(branch, 0)


def test_measurement_then_update_cleanup_retains_entangled_reference_branch():
    scheduler = Scheduler()
    root = external(scheduler, "input")
    external(scheduler, "reference", 1)
    initial = random_state(3)
    scheduler.measure(root)
    scheduler.update(root, (Gate("rotate", root.bits, amount=1),))
    scheduler.update(root, (Gate("add_constant", root.bits, amount=1),))
    scheduler.release(root)
    actual = branches_for(scheduler, initial)
    expected = measure(Branch(1, initial), 0, 2)
    for branch in actual:
        outcome = branch.snapshots[0] + 2 * branch.snapshots[1]
        reference = next(item for item in expected if item.snapshots == (outcome,))
        state = np.zeros(8, dtype=complex)
        for index, amplitude in enumerate(reference.state):
            if field(index, 0, 2) == outcome:
                state[replace_field(index, 0, 2, 0)] = amplitude
        assert branch.probability == pytest.approx(reference.probability)
        np.testing.assert_allclose(branch.state, state, atol=1e-10)


def test_indirect_measurement_invalidates_original_root_preparation():
    scheduler = Scheduler()
    root = scheduler.allocate(1, "choice", SPAN)
    scheduler.initialize(root, (Gate("h", root.bits),))
    copy = derived(scheduler, root, "copy")
    scheduler.measure(copy)
    scheduler.release(copy)
    with pytest.raises(DiagnosticError, match="related value was measured"):
        scheduler.release(root)
    # An explicit direct measurement provides the missing valid checkpoint.
    scheduler.measure(root)
    scheduler.release(root)
    for branch in branches_for(scheduler):
        assert branch.snapshots[0] == branch.snapshots[1]
        assert_basis_branch(branch, 0)


def test_measurement_invalidates_connected_roots_in_both_directions():
    scheduler = Scheduler()
    a = scheduler.allocate(1, "a", SPAN)
    scheduler.initialize(a, (Gate("h", a.bits),))
    b = scheduler.allocate(1, "b", SPAN)
    scheduler.initialize(b, (Gate("h", b.bits),))
    scheduler.update(a, (Gate("copy", a.bits, b.bits),))
    scheduler.measure(b)
    scheduler.release(b)
    with pytest.raises(DiagnosticError, match="related value was measured"):
        scheduler.release(a)


def test_overwrite_after_explicit_measurement_preserves_old_consumers():
    scheduler = Scheduler()
    root = scheduler.allocate(2, "number", SPAN)
    scheduler.initialize(root, (Gate("h", root.bits),))
    result = derived(scheduler, root, "old_value", 1)
    scheduler.measure(root)
    scheduler.overwrite(root, (Gate("x", (root.bits[1],)),))
    scheduler.release(result)
    for branch in branches_for(scheduler):
        assert_basis_branch(branch, 2)


def test_repeated_measurements_and_evolution_execute_as_a_dynamic_circuit():
    scheduler = Scheduler()
    root = scheduler.allocate(1, "choice", SPAN)
    scheduler.initialize(root, (Gate("h", root.bits),))
    scheduler.measure(root)
    scheduler.measure(root)
    scheduler.update(root, (Gate("x", root.bits),))
    scheduler.measure(root)
    scheduler.release(root)
    circuit = emit_operations(scheduler.qubit_count, scheduler.classical_bit_count, scheduler.operations)
    circuit.save_density_matrix()
    simulator = AerSimulator(method="density_matrix")
    compiled = transpile(circuit, simulator, optimization_level=0, seed_transpiler=13)
    result = simulator.run(compiled, shots=256, seed_simulator=17).result()
    assert set(result.get_counts()) == {"100", "011"}
    np.testing.assert_allclose(result.data()["density_matrix"].data, [[1, 0], [0, 0]], atol=1e-10)
