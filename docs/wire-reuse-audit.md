# Wire reuse delivery audit

2026-11-06. Scope: [approved plan](wire-reuse-plan.md), T024. Language 0.3,
package 0.3.0.dev0, artifact 4; existing artifact 3 cached circuits remain executable.
This is implementation-agent verification, not independent human review or proof.

| Requirement | Implementation and direct evidence |
| --- | --- |
| Fixed schedule, zero proofs, no hidden measurement/reset | cleanup.py publishes transaction-end semantic certificates; wires.py changes quantum indices only. test_wire_execution checks complete operation equality modulo indices, including snapshots/conditions/angles. |
| Multiple lifetimes, reconstruction, deterministic allocation | wires.py derives per-bit epochs and checks coverage/collisions/handoffs. test_wires exercises arbitrary complex reference entanglement, reconstruction, stable lowest-free assignment, failed cleanup and overwrite. |
| Preserve final live values, zero-only locals and measured values | Terminal live-use intervals, omitted unused dead zeros, no release on measurement. test_wires and test_wire_views include 500 empty locals plus a live zero. |
| Search workspace versus retained selection state | Explicit zero workspace on preparation; owner/index stays live. test_search checks matching probabilities, valid index support and independent dense-reflection phases on physical wires. test_wire_execution compares mapped full states and each logical proof prefix, including repeated search and changed inputs. |
| Dynamic/coherent control and remaining quantum state | test_wire_execution compares joint classical snapshots, branch probabilities and remaining complex amplitudes before/after allocation. Existing feedforward/cleanup safety suite remains green. |
| Config and simulation limits | Strict Boolean wire_reuse, CLI enable/disable, build identity. Physical memory/width reports and existing pre/post-transpile guards. test_wire_execution and test_delivery cover config, limit rejection and generation; test_wires bounds wide no-op lifetime materialization before backend expansion. |
| Direct/generated compatibility | artifact_v4, retained v3 adapter; test_provenance exercises cached legacy code and changed inputs. test_delivery/search_delivery compare direct/generated circuits and outputs. Installed smoke runs respecialize inputs. |
| Names, aliases and source views | physical.py keeps stable exclusive/indexed names and shared work_N names; logical allocation/source mappings are explicitly identified. test_provenance covers alias/return/array/string and collision scenarios. |
| Physical/logical diagrams, folding and cleanup | test_wire_views verifies both widths, full complex operators, numeric/all/selective unfolding, empty cleanup, PNG/SVG and image identity. test_diagrams covers search and measurements. Image example12 inspected; labels/handoffs are legible. |
| Reports and examples | Example12: 19 logical, 10 physical, 29 unchanged operations, 16 logical cleaned, 7 physical free, 16 KiB instead of 8 MiB. Example39: 39 logical/6 physical, output -3. All 39 catalog examples run below 24, largest physical width 15. |
| Documentation and research | Active language/cleanup/lowering/value contracts plus wire-allocation.md; guide, roadmap, CLI walkthrough, tour and README updated. Literature and deferred scheduling work recorded in wire-reuse-plan.md. 17 walkthrough commands and local documentation links verified. |
| Distribution | 907 tests each on Windows and Debian/WSL. Parser regeneration check passes. Wheel installed/smoked on both; core-only compilation/codegen works with empty PATH/no Java/Qiskit. V025 records packaging commands and source archive checks. |
| Continuity and delivery | KB-023/024/025, decisions D079-D081, task/status/handoff; three logical local checkpoints. User snapshot and untracked root diagram preserved. No push. |

No hardware run, hosted CI run, Python 3.12 validation, formal proof, cleanup
rescheduling or dirty-ancilla borrowing is claimed. Physical reuse can constrain
parallelism; lower qubit width does not imply faster hardware execution.
