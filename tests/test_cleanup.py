"""Automatic schedules checked against independent complex-state expectations."""

import numpy as np
import pytest
from qiskit.quantum_info import Statevector

from qutes.cleanup import Scheduler
from qutes.diagnostics import DiagnosticError, Position, Span
from qutes.gates import Gate
from qutes.qiskit_backend import emit_gates
from tests.reference import field, random_state, replace_field

pytestmark = pytest.mark.backend
SPAN = Span("cleanup.qut", Position(0, 1, 1), Position(1, 1, 2))


def external(scheduler, name, width=2):
    storage = scheduler.allocate(width, name, SPAN)
    scheduler.initialize(storage, (), external=True)
    return storage


def derived(scheduler, source, name, amount=0):
    storage = scheduler.allocate(len(source.bits), name, SPAN)
    scheduler.initialize(storage, (Gate("copy", storage.bits, source.bits),
                                   Gate("add_constant", storage.bits, amount=amount)))
    return storage


def check_state(scheduler, input_qubits, transform, seed=71):
    source = random_state(input_qubits, seed)
    initial = np.zeros(2**scheduler.qubit_count, dtype=complex)
    initial[:len(source)] = source
    expected = np.zeros_like(initial)
    indices = [transform(index) for index in range(len(source))]
    assert len(set(indices)) == len(indices), "test expectation lost input information"
    expected[indices] = source
    actual = Statevector(initial).evolve(emit_gates(scheduler.qubit_count, scheduler.operations)).data
    np.testing.assert_allclose(actual, expected, atol=1e-10)


def test_clean_derived_value_after_source_changes_restores_current_source():
    scheduler = Scheduler()
    root = external(scheduler, "number")
    external(scheduler, "entangled reference", 1)
    temporary = derived(scheduler, root, "adjusted", 1)
    result = derived(scheduler, temporary, "result")
    scheduler.update(root, (Gate("add_constant", root.bits, amount=2),))
    scheduler.release(temporary)
    assert temporary.version == -1 and temporary.released
    assert root.version == 1 and result.version == 0

    def expected(index):
        value = field(index, 0, 2)
        return replace_field(replace_field(index, 0, 2, (value + 2) % 4), 5, 2, (value + 1) % 4)
    check_state(scheduler, 3, expected)
    assert scheduler.events[-1].restored_inputs[0].storage == root.id


def test_recompute_released_dependency_and_restore_it_to_zero():
    scheduler = Scheduler()
    root = external(scheduler, "number")
    external(scheduler, "reference", 1)
    temporary = derived(scheduler, root, "adjusted", 1)
    result = derived(scheduler, temporary, "result", 2)
    scheduler.update(root, (Gate("add_constant", root.bits, amount=3),))
    scheduler.release(temporary)
    scheduler.release(result)
    check_state(scheduler, 3, lambda index: replace_field(index, 0, 2, (field(index, 0, 2) + 3) % 4))
    assert temporary.released and temporary.version == -1


def test_two_mutated_dependencies_are_temporarily_restored_independently():
    scheduler = Scheduler()
    a = external(scheduler, "a")
    b = external(scheduler, "b")
    value = derived(scheduler, a, "value")
    scheduler.update(value, (Gate("add", value.bits, b.bits),))
    scheduler.update(a, (Gate("add_constant", a.bits, amount=1),))
    scheduler.update(b, (Gate("add", b.bits, a.bits),))
    scheduler.release(value)

    def expected(index):
        a_value, b_value = field(index, 0, 2), field(index, 2, 2)
        return replace_field(replace_field(index, 0, 2, (a_value + 1) % 4), 2, 2, (a_value + b_value + 1) % 4)
    check_state(scheduler, 4, expected)


def test_cyclic_cleanup_rejected_without_partially_emitted_schedule():
    scheduler = Scheduler()
    root = external(scheduler, "number")
    temporary = derived(scheduler, root, "temporary")
    scheduler.update(root, (Gate("add", root.bits, temporary.bits),))
    before = tuple(scheduler.operations)
    with pytest.raises(DiagnosticError, match="restoring number would read") as error:
        scheduler.release(temporary)
    assert error.value.code == "Q3001"
    assert tuple(scheduler.operations) == before
    assert (root.version, temporary.version, temporary.released) == (1, 0, False)


def test_root_cannot_be_unprepared_while_correlated_output_is_live():
    scheduler = Scheduler()
    root = scheduler.allocate(1, "choice", SPAN)
    scheduler.initialize(root, (Gate("h", root.bits),))
    result = derived(scheduler, root, "output")
    with pytest.raises(DiagnosticError, match="live value output"):
        scheduler.release(root)
    scheduler.release(result)
    scheduler.release(root)
    actual = Statevector.from_instruction(emit_gates(scheduler.qubit_count, scheduler.operations)).data
    np.testing.assert_allclose(actual, [1, 0, 0, 0], atol=1e-10)


def test_root_dependency_survives_releasing_intermediate_value():
    scheduler = Scheduler()
    root = scheduler.allocate(1, "choice", SPAN)
    scheduler.initialize(root, (Gate("h", root.bits),))
    temporary = derived(scheduler, root, "temporary")
    result = derived(scheduler, temporary, "result")
    scheduler.release(temporary)
    with pytest.raises(DiagnosticError, match="live value result"):
        scheduler.release(root)
    scheduler.release_scope({root.id, result.id})
    actual = Statevector.from_instruction(emit_gates(scheduler.qubit_count, scheduler.operations)).data
    np.testing.assert_allclose(actual, [1, 0, 0, 0, 0, 0, 0, 0], atol=1e-10)


def test_overwrite_derived_value_retains_old_version_for_other_dependents():
    scheduler = Scheduler()
    root = external(scheduler, "number")
    temporary = derived(scheduler, root, "temporary", 1)
    result = derived(scheduler, temporary, "result")
    scheduler.update(root, (Gate("add_constant", root.bits, amount=2),))
    scheduler.overwrite(temporary, (Gate("x", (temporary.bits[1],)),))
    scheduler.release(result)

    def expected(index):
        return replace_field(replace_field(index, 0, 2, (index + 2) % 4), 2, 2, 2)
    check_state(scheduler, 2, expected)
    assert temporary.version == 1


def test_overwrite_unknown_root_is_diagnostic():
    scheduler = Scheduler()
    root = scheduler.allocate(2, "number", SPAN)
    scheduler.initialize(root, (Gate("h", root.bits),))
    with pytest.raises(DiagnosticError, match="reversible update"):
        scheduler.overwrite(root, ())


def test_overwrite_can_recompute_a_previously_released_input():
    scheduler = Scheduler()
    root = external(scheduler, "number")
    intermediate = derived(scheduler, root, "intermediate", 1)
    target = derived(scheduler, intermediate, "target", 2)
    dependent = derived(scheduler, target, "dependent")
    scheduler.release(intermediate)
    scheduler.overwrite(target, (Gate("x", (target.bits[1],)),))
    scheduler.release(dependent)
    check_state(scheduler, 2, lambda index: replace_field(index, 4, 2, 2))
    assert intermediate.version == -1


def test_deep_cleanup_returns_resource_diagnostic_instead_of_recursion_error():
    scheduler = Scheduler(max_steps=100_000)
    root = external(scheduler, "input", 1)
    chain = [root]
    for index in range(135):
        chain.append(derived(scheduler, chain[-1], f"local{index}"))
    # Every predecessor is now released, requiring nested recomputation.
    # Construct this invariant with accepted individual releases first.
    for storage in chain[1:-1]:
        try:
            scheduler.release(storage)
        except DiagnosticError as error:
            assert error.code == "Q4001"
            return
    with pytest.raises(DiagnosticError) as error:
        scheduler.release(chain[-1])
    assert error.value.code == "Q4001"


def test_external_state_cannot_be_erased():
    scheduler = Scheduler()
    root = external(scheduler, "input")
    with pytest.raises(DiagnosticError, match="unknown input state"):
        scheduler.release(root)


def test_cleanup_budget_returns_diagnostic_and_no_partial_cleanup():
    scheduler = Scheduler()
    root = external(scheduler, "number")
    temporary = derived(scheduler, root, "temporary")
    before = tuple(scheduler.operations)
    scheduler.max_steps = scheduler.work + 1
    with pytest.raises(DiagnosticError) as error:
        scheduler.release(temporary)
    assert error.value.code == "Q4001"
    assert tuple(scheduler.operations) == before
    assert temporary.version == 0


def test_low_level_overlap_is_never_silently_treated_as_addition():
    with pytest.raises(ValueError, match="overlap"):
        Gate("add", (0, 1), (0, 1))


@pytest.mark.parametrize("seed", [11, 34, 93, 105])
def test_long_chain_recomputation_preserves_phases_and_reference(seed):
    scheduler = Scheduler()
    root = external(scheduler, "input", 1)
    external(scheduler, "reference", 1)
    chain = [root]
    for index in range(4):
        chain.append(derived(scheduler, chain[-1], f"local{index}", index % 2))
    scheduler.update(root, (Gate("x", root.bits),))
    for storage in chain[1:]:
        scheduler.release(storage)
    check_state(scheduler, 2, lambda index: index ^ 1, seed)
