# Task queue

Status vocabulary: TODO, ACTIVE, DONE, BLOCKED. A task is DONE only with evidence.

| ID | Status | Work / completion gate | Dependencies |
| --- | --- | --- | --- |
| T001 | DONE | Initialize Git and knowledge-base continuity; inspected environment recorded in KB-001. | None |
| T002 | DONE | Specify the initial grammar, types/staging, effects, diagnostics, and acceptance cases, separating planned from implemented behavior. | T001 |
| T003 | DONE | Package bootstrap, validated dependency pins, reproducible test commands. | T001 |
| T004 | DONE | Independent small-state reference semantics and Qiskit probes: addition, rotation, correlation, predicate cleanup, repeated measurement, classical feedforward, signed/text decoding. | T002, T003 |
| T005 | DONE | Parser and source spans; parse positive/semantic-negative corpus, reject lexical/syntactic errors; no backend work in parser. | T002, T004 |
| T006 | DONE | Name resolution, type/stage checking, structured typed IR, readonly parameters, coherent-condition restrictions, explicit unsupported diagnostics. | T005 |
| T007 | ACTIVE | Bounded classical evaluator and user-function inlining with source mapping. | T006 |
| T008 | TODO | Dependency/version model, cleanup synthesizer, and arithmetic lowering with full-state verification. | T004, T006 |
| T009 | TODO | Integrate coherent branches, functions, and construction-time loops. | T007, T008 |
| T010 | TODO | Arrays/text/configuration integrated with lifetime analysis. | T009 |
| T011 | TODO | Non-consuming measurement, snapshots, feedforward, results decoding, Qiskit emitter. | T010 |
| T012 | TODO | CLI build/run/explain, packaging, resource limits, documentation, CI/release evidence. | T011 |

M1 readiness requires T002-T004 plus a review of unresolved limitations. A passing
probe is evidence of backend feasibility, not proof of general automatic cleanup.
The scheduled milestones in the roadmap may overlap only when dependencies and
test evidence support doing so.

Evidence for T002-T004: KB-002 / V002, 37 passing tests. This is the initial automated specification/feasibility gate; final naming, human review, and a clean dependency installation are not implied.

Evidence for T005: KB-003 / V003, 102 passing tests total; all 33 corpus cases checked for syntax. T006 is the next unblocked task, not started. No semantic acceptance or source execution is claimed.

T006 evidence: KB-004 / V004, 173 passing tests. T007 is next; typed analysis deliberately leaves Q3001 cleanup obligations for the later pass.
