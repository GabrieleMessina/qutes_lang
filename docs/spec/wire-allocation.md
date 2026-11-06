# Certified-zero physical wire allocation

Language 0.3, generated artifact schema 4. This pass follows complete versioned
cleanup scheduling and precedes circuit emission. It changes quantum wire indices,
never gates, measurement/snapshot IDs, order, conditions, angles or global phases.
It neither simulates nor introduces reset/measurement. See the
[research and delivery plan](../wire-reuse-plan.md) for sources and scope.

## Proofs and intervals

Logical storage IDs and bit tuples remain stable. The scheduler publishes semantic
`ZeroCertificate` records after successful transactions: cleanup to version -1,
restoration of already-zero dependencies, and zero search workspace. An overwrite
publishes only after its complete guarded schedule succeeds, not at the intermediate
zero target. Failed transactions leave no new certificates. Diagram annotations
are not proofs. A measurement, last use, or source scope exit alone is not proof.

Each certificate records logical bits, its operation boundary, transaction start
and reason. For each logical bit, first use begins an interval; the next certified
zero boundary ends it. Later reconstruction creates another epoch. An uncertified
state remains live through the schedule end. Final live script values, including
measured values and search indices, have a terminal use. Dead zero-only locals
without any operations need no physical wire. Unused live zeros still have a wire.

Intervals are half-open `[start,end)` in scheduled-operation indices. For M
operations, M denotes the final live-state use and M+1 its interval end. A zero
certificate at boundary K applies after operation K-1 and before operation K.
At a handoff, the outgoing interval must have a zero certificate. Source aliases,
views and returned ownership follow existing logical storage, never duplicate it.

A deterministic heap sweep assigns the lowest free physical wire or allocates a
new one. All simultaneous operands remain distinct. A verifier separately checks
the complete expected intervals, operation coverage, overlap and certified
handoffs. For these fixed intervals this uses their maximum overlap width; it
does not optimize the cleanup schedule or claim a globally minimal quantum circuit.
No dirty-ancilla borrowing, routing, or hardware parallelism optimization occurs.
Live-bit, operation-bit and certificate-bit references are preflighted against
max_evaluation_steps before lifetime materialization; excess is Q4001 even when
wide no-op gates would emit no elementary backend operations.

Search workspace has certified zero state after its reversible preparation and
after complete reconstruction/restoration transactions. Selected values and their
retained indices remain live together. Later cleanup can reacquire workspace in a
new epoch. A live captured input or measured selected value cannot be discarded to
save wires. Existing impossible-cleanup diagnostics remain in force.

## API, metadata and diagrams

`CompilerConfig(wire_reuse=True)` is the default. TOML `wire_reuse = false` or CLI
`--no-wire-reuse` disables remapping/elision; `--wire-reuse` enables it explicitly.
The Boolean setting participates in build identity. The low-level `lower()` API
returns logical operations. `compile_source(...).program` is physical and retains
`.logical_program` plus `.wire_allocation`. Do not index a physical statevector
using logical allocation bits; resolve the appropriate lifetime first.

Metadata distinguishes:

- `allocations`, `source_mappings`, `logical_registers`: logical storage/bindings;
- `registers`, executable operations and `cleanup_annotations`: physical wires;
- `wire_allocation`: logical/physical widths, per-bit intervals and zero proofs;
- `wire_handoffs`: physical wire, old/new logical epochs, operation and proof;
- classical snapshots and result layouts: unchanged classical bit indices.

Resource `allocated_qubits`/`physical_qubits`/`peak_allocated_qubits` are reserved
physical width. `logical_allocated_qubits` and `saved_qubits` explain reduction.
`cleaned_qubits_at_end` counts logical released storage; it is not a physical free
count. `physical_zero_qubits_at_end` counts unowned certified-zero physical wires,
excluding live zero-valued variables. Memory estimates and simulation caps use
physical width, with the existing additional check after backend decomposition.

Diagrams default to physical wires. `--wire-view logical` and Python
`render(..., wire_view="logical")` show original storage; folding/unfolding/filter
behavior works in either view. View options affect image identity only. Exclusive
wires retain source names where physical order permits, otherwise indexed names.
Shared wires use stable `work_N` names. Reuse markers show new owners, and folded
blocks count hidden handoffs. Cleanup marks the outgoing lifetime; omitted zero-only
locals get no physical marker. An empty marker must never become an all-wire barrier.
Markers do not enter executable circuits. `explain` lists logical binding ranges,
physical intervals and zero-certificate references.

New generated modules use `qutes.artifact_v4`. Existing schema-3 modules keep their
cached circuits through the independent v3 adapter. Changed inputs recompile with
the current compiler; absent legacy `wire_reuse` settings take the current default.
Schemas 1/2 remain rejected with a rebuild instruction. Rebuild v3 modules to apply
reuse to their cached circuits. Package/language versions remain 0.3.0.dev0/0.3.

Tests compare valid zero-initialized computations using mapped states, including
arbitrary reference entanglement, full complex phases, projected measurement
branches, and all certified free wires. Different-width whole operators are not
interchangeable. Fewer wires can constrain parallelism; no hardware speedup is
promised. Safe cleanup rescheduling is a separate future increment.
