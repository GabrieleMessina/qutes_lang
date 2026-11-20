# Circuit readability delivery audit

The approved increment changes presentation and additive metadata; language 0.3,
artifact 3, value semantics, cleanup scheduling and physical allocation remain.
Validation commands and run identifiers are recorded in V020-V022.

| Requirement | Implementation and evidence |
| --- | --- |
| Source names in circuits | Named quantum/classical registers in direct and generated builds; deterministic collision handling; search value/index/work partitions. `test_provenance` checks generated equality, snapshots, returns, readonly aliases, permutations and repeated calls. |
| Alias and source ranges | Construction preserves function names, parameter/foreach bindings and source expressions. Lowering records half-open operation ranges; explain lists mappings. Aliases allocate no extra wires. An additional compile probe checks 500 repeated locals with unique names and zero execution gates. |
| Compact source-level operations | Backend-independent regions cover comparisons, arithmetic, rotations, Boolean expressions, membership, search, function calls and branches. `test_diagrams` checks examples 12/15, nested functions, named oracle calls and inverse labels. |
| Selective unfolding | CLI and Python render APIs support depth/all and optional comma-separated selectors. Ancestors open, unrelated siblings stay folded, unknown selectors provide hints. Tests cover every mode, invalid options and image variants. |
| Cleanup visibility | Distinct event IDs connect annotations to exact zeroed and touched/restored wires. Same-name zero-cost events remain distinct. Folded parents count hidden cleanup; inverse oracle cleanup is recomputation, never labeled as zeroing. Tests cover zero-length events, restored dependencies and retained search scratch. |
| Execution unchanged | Drawing builds a separate circuit. Full-operator phase checks, quantum-collection statevectors, scratch checks and dynamic execution comparisons exercise compact/expanded/selected views. Generated/direct execution and input respecialization remain covered by the existing suite. |
| Resource reporting | Integer-based B/KiB/MiB/GiB/TiB/PiB/EiB formatting, symbolic huge estimates, unchanged exact JSON bytes. Example 12 remains 19 reserved qubits/51 gate applications and prints 8 MiB. Wide lazy backend definitions receive conservative preflight checks before generation, plus incremental expansion bounds. |
| Wildcards | QW0001 warns without changing the alphabet. Classical matching needs no ? encoding; storing a quantum marker does. CLI warnings are nonfatal, JSON remains parseable and the Python API is silent. Reporting tests cover these cases. |
| CLI and roadmap | Walkthrough covers all seven modes, inputs, JSON, diagrams, selective unfolding and generated execution. Historical roadmap is archived; active value contracts live in the specification. Documentation links and walkthrough commands were executed/checked. |
| Distribution | Wheel smoke verifier checks named registers, selective rendering, CLI execution and generated respecialization. Legacy artifact-3 modules without presentation metadata still build/run; source distributions include the new guides, archived roadmap and tour README. |

Text and PNG/SVG image tests exercise diagrams. Compact example 15 and expanded
example 24 were also visually inspected: source names, folded operations, cleanup
and restored-input labels are legible. Image dimension limits remain enforced.

## Intentional boundaries

- Physical wires are not reused: a released value may still be reconstructed for
  cleanup. T024 records this separate future allocation task.
- Measurement and runtime branches stay visible. Mixed functions show reversible
  segments rather than a fictitious unitary gate for the entire function.
- Diagram markers are not instructions in executable/generated circuits. Changing
  view options changes the image identity, not the build identity or simulation.
- Backend decomposition preflight is conservative; an oversized view fails Q4001
  with advice to reduce unfolding or raise the configured construction budget.
- Explicit quantum text distribution preparation remains deferred. Wildcards do
  not create superpositions and literal wildcard escaping is still unsupported.
- No hardware validation, hosted CI execution or independent human review is claimed.
