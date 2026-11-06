"""Fixed-schedule reuse, including reconstructed and reference-entangled state."""
from dataclasses import replace
from pathlib import Path

import numpy as np
import pytest
from qiskit.quantum_info import Statevector

from qutes.cleanup import Scheduler
from qutes.compiler import compile_source
from qutes.config import CompilerConfig
from qutes.diagnostics import DiagnosticError
from qutes.gates import Gate, Measurement
from qutes.qiskit_backend import emit_operations
from qutes.wires import allocate, remap, verify, ZeroCertificate
from tests.test_cleanup import SPAN, derived, external
from tests.reference import random_state

pytestmark = pytest.mark.backend


def allocation_for(scheduler):
    live = tuple(b for s in scheduler.storages if not s.released for b in s.bits
                 if b not in s.zero_workspace)
    initial = tuple(b for s in scheduler.storages if s.external for b in s.bits)
    return allocate(scheduler.operations, scheduler.qubit_count, scheduler.zero_certificates,
                    live, initial_bits=initial), live, initial


def test_example_12_fixed_schedule_reuses_comparison_work():
    path = Path("examples/language/12_quantum_ordering.qut")
    program = compile_source(path.read_text(), config=CompilerConfig.load(path.parent / "qutes.toml")).program.logical_program
    live = tuple(b for a in program.allocations if not a.released for b in a.bits)
    allocation = allocate(program.operations, program.qubit_count, program.zero_certificates, live)
    assert allocation.logical_count == 19
    assert allocation.physical_count == 10
    assert len(remap(program.operations, allocation)) == len(program.operations) == 29


@pytest.mark.parametrize("seed", [11, 34, 93, 105])
def test_reconstruction_has_new_epoch_and_preserves_complex_reference(seed):
    scheduler = Scheduler()
    root = external(scheduler, "input", 1)
    external(scheduler, "reference", 1)
    intermediate = derived(scheduler, root, "intermediate", 1)
    result = derived(scheduler, intermediate, "result")
    scheduler.release(intermediate)
    spare = derived(scheduler, root, "spare")
    scheduler.release(spare)
    scheduler.update(root, (Gate("x", root.bits),))
    scheduler.release(result)
    allocation, live, initial_bits = allocation_for(scheduler)
    assert len([i for i in allocation.intervals if i.logical == intermediate.bits[0]]) >= 2
    assert allocation.physical_count < allocation.logical_count
    initial = random_state(2, seed)
    def state(width, mapping):
        vector = np.zeros(2 ** width, complex)
        for index, amplitude in enumerate(initial):
            destination = sum(((index >> i) & 1) << mapping[b] for i, b in enumerate(initial_bits))
            vector[destination] = amplitude
        return vector
    logical = Statevector(state(scheduler.qubit_count, dict(zip(initial_bits, initial_bits)))).evolve(
        emit_operations(scheduler.qubit_count, 0, scheduler.operations)).data
    lookup = allocation.lookup()
    physical = Statevector(state(allocation.physical_count, {b: lookup.at(b, 0) for b in initial_bits})).evolve(
        emit_operations(allocation.physical_count, 0, remap(scheduler.operations, allocation))).data
    expected = np.zeros_like(physical)
    for index, amplitude in enumerate(logical):
        if any((index >> b) & 1 for b in range(scheduler.qubit_count) if b not in live):
            assert abs(amplitude) < 1e-10
        else:
            destination = sum(((index >> b) & 1) << lookup.at(b, len(scheduler.operations)) for b in live)
            expected[destination] = amplitude
    np.testing.assert_allclose(physical, expected, atol=1e-10)


def test_measurement_is_not_a_zero_certificate_and_keeps_snapshots():
    ops = (Gate("h", (0,)), Measurement((0,), (0,), SPAN), Gate("x", (1,)),
           Gate("x", (0,), classical_controls=((0, True),)))
    allocation = allocate(ops, 2, (), (0, 1))
    assert allocation.physical_count == 2
    assert remap(ops, allocation) == ops


def test_zero_only_dead_storage_elided_but_live_zero_retained():
    scheduler = Scheduler()
    dead = scheduler.allocate(1, "dead", SPAN)
    scheduler.initialize(dead, ())
    scheduler.release(dead)
    live = scheduler.allocate(1, "live", SPAN)
    scheduler.initialize(live, ())
    allocation, _, _ = allocation_for(scheduler)
    assert allocation.physical_count == 1
    assert len(allocation.intervals) == 1
    assert allocation.intervals[0].logical == live.bits[0]
    assert allocation.lookup().ending(dead.bits[0], 0) is None


def test_failed_cleanup_does_not_publish_zero_proofs():
    scheduler = Scheduler()
    root = external(scheduler, "number")
    temporary = derived(scheduler, root, "temporary")
    scheduler.update(root, (Gate("add", root.bits, temporary.bits),))
    before = tuple(scheduler.zero_certificates)
    with pytest.raises(DiagnosticError):
        scheduler.release(temporary)
    assert tuple(scheduler.zero_certificates) == before


def test_overwrite_certifies_reconstructed_dependency_only_after_transaction():
    scheduler = Scheduler()
    root = external(scheduler, "root", 1)
    temporary = derived(scheduler, root, "temporary")
    result = derived(scheduler, temporary, "result")
    scheduler.release(temporary)
    start = len(scheduler.operations)
    scheduler.overwrite(result, (Gate("x", result.bits),))
    proofs = [p for p in scheduler.zero_certificates if p.operation_start == start]
    assert proofs and all(p.boundary == len(scheduler.operations) for p in proofs)
    assert all(result.bits[0] not in p.bits for p in proofs)
    allocation_for(scheduler)


def test_independent_verifier_rejects_collisions_and_missing_lifetimes():
    ops = (Gate("x", (0,)), Gate("copy", (1,), (0,)))
    allocation = allocate(ops, 2, (), (0, 1))
    with pytest.raises(ValueError, match="overlapping"):
        verify(replace(allocation, intervals=tuple(replace(i, physical=0) for i in allocation.intervals)), ops, (0, 1))
    with pytest.raises(ValueError, match="cover"):
        verify(replace(allocation, intervals=allocation.intervals[:1]), ops, (0, 1))
    with pytest.raises(ValueError, match="boundary"):
        allocate(ops, 2, (ZeroCertificate((0,), 3, 0, "invalid"),), (0, 1))


def test_disabled_allocator_preserves_identity_and_is_deterministic():
    ops = (Gate("x", (0,)), Gate("x", (0,)), Gate("h", (1,)))
    proofs = (ZeroCertificate((0,), 2, 0, "cleanup"),)
    reused = allocate(ops, 2, proofs, (1,))
    assert reused == allocate(ops, 2, proofs, (1,))
    assert reused.physical_count == 1
    baseline = allocate(ops, 2, proofs, (1,), enabled=False)
    assert baseline.physical_count == 2
    assert remap(ops, baseline) == ops
