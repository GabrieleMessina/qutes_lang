# Certified-zero wire reuse: approved implementation plan

Authorized 2026-11-05. Language remains 0.3. Preserve assignment, non-consuming
measurement, full phases/correlations and existing scheduled operation order.
Never introduce reset/measurement. No subagents; local coherent commits, no push.

## Research and scope

- [Unqomp, section 5.4](https://files.sri.inf.ethz.ch/website/papers/pldi21-unqomp.pdf)
  motivates lifetime intervals and greedy allocation for a fixed linearization.
  Use a deterministic lowest-free-wire sweep after Qutes cleanup scheduling.
- [Reqomp](https://arxiv.org/abs/2212.10395) explores recomputation/space tradeoffs.
  Defer cleanup rescheduling and memory-budget-driven recomputation.
- [SQUARE](https://arxiv.org/abs/2004.08539) motivates future locality-aware choices:
  reduced width can constrain parallelism and is not a hardware speed guarantee.
- [Modular uncomputation](https://arxiv.org/abs/2406.14227) supports retaining
  structured ownership information; do not try to recover proof from gate names.
- [Qiskit reuse plugin](https://github.com/qiskit-community/qiskit-qubit-reuse)
  relies on measurement/reset; it does not fit this coherent temporary contract.

These sources were consulted during planning. The linear-scan optimality claim
applies only to the chosen fixed certified intervals, never globally to circuits.

## Required implementation

1. Scheduler emits semantic zero certificates at successful cleanup, restored-zero
   dependency, overwrite and search-workspace boundaries. Rollbacks publish none.
   Split a logical wire into lifetime epochs when later cleanup reconstructs it.
   Keep unknown state live, even after last use; keep final live values and search
   selection indices. Elide unused zero-only temporaries. Verify coverage, distinct
   simultaneous operands, nonoverlap and certified-zero handoffs independently.
2. Preserve a logical program; execute a remapped physical schedule with identical
   gate order/angles/conditions/classical snapshots. Default `wire_reuse=true`;
   `--wire-reuse`/`--no-wire-reuse`, TOML and Python configuration. Include setting
   in build identity. Artifact 4 distinguishes logical IDs/physical wires. Existing
   artifact 3 cached builds still execute; respecialization may produce artifact 4.
3. Default physical diagrams, `--wire-view physical|logical` and Python equivalent.
   Stable exclusive source register names; shared wires `work_N`, handoff markers
   and interval maps in explain. Retain source folding/selectors/cleanup in both
   views. Skip empty annotations (an empty Qiskit barrier would affect all wires).
   Wire view affects image hash, not build identity. Preserve image/expansion caps.
4. Report logical count, physical width/peak, saved wires, reuse setting, exact
   mapping and certificate references. Simulation/memory limits use physical width.
   Separate logical cleaned totals from physical final-free state. Update docs/tour.

## Delivery checkpoints and acceptance

1. Certificates, epochs, allocator and verifier, focused tests and knowledge base.
2. Physical execution, configuration, generated artifacts and compatibility tests.
3. Diagrams/reports/docs/examples and full Windows/Linux/installed validation.

Example12: 19 logical -> 10 physical, unchanged 29 scheduled operations (19 with
reuse disabled). Validate sequential/overlapping/reconstructed lifetimes, alias
views and returns, non-consuming measurement/feedforward, zero-only locals and live
zeros, search scratch/index lifetimes, repeated calls and cleanup failure paths.
Compare enabled/disabled using mapped statevectors, arbitrary complex amplitudes,
reference entanglement, correlations and zero scratch. Do not compare unequal-width
full operators as if they had identical input spaces. Test no operation insertion,
deletion/reordering, direct/generated parity and input specialization, legacy v3,
both wire views/depth/filter/PNG/SVG, simulator caps and budgets. Include a tour
example that fits 24 only with reuse. Run full Windows/Linux suites, parser check,
package installation/smokes. Keep exact evidence and handoff in knowledge base.

Deferred: dirty ancilla borrowing, cleanup scheduling, routing, hardware performance
guarantees and memory-budget-driven recomputation. Preserve user snapshot changes
and unrelated untracked diagram images.
