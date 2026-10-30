# Task queue

Status vocabulary: TODO, ACTIVE, DONE, BLOCKED. A task is DONE only with evidence.

| ID | Status | Work / completion gate | Dependencies |
| --- | --- | --- | --- |
| T001 | DONE | Initialize Git and knowledge-base continuity; inspected environment recorded in KB-001. | None |
| T002 | ACTIVE | Specify the initial grammar, types/staging, effects, diagnostics, and acceptance cases, separating planned from implemented behavior. | T001 |
| T003 | TODO | Package bootstrap, validated dependency pins, reproducible test commands. | T001 |
| T004 | TODO | Independent small-state reference semantics and Qiskit probes: addition, rotation, correlation, predicate cleanup, repeated measurement, classical feedforward, signed/text decoding. | T002, T003 |
| T005 | TODO | Parser and source spans; parse positive/semantic-negative corpus, reject lexical/syntactic errors; no backend work in parser. | T002, T004 |
| T006 | TODO | Name resolution, type/stage checking, structured typed IR, readonly parameters, coherent-condition restrictions, explicit unsupported diagnostics. | T005 |
| T007 | TODO | Bounded classical evaluator and user-function inlining with source mapping. | T006 |
| T008 | TODO | Dependency/version model, cleanup synthesizer, and arithmetic lowering with full-state verification. | T004, T006 |
| T009 | TODO | Integrate coherent branches, functions, and construction-time loops. | T007, T008 |
| T010 | TODO | Arrays/text/configuration integrated with lifetime analysis. | T009 |
| T011 | TODO | Non-consuming measurement, snapshots, feedforward, results decoding, Qiskit emitter. | T010 |
| T012 | TODO | CLI build/run/explain, packaging, resource limits, documentation, CI/release evidence. | T011 |

M1 readiness requires T002-T004 plus a review of unresolved limitations. A passing
probe is evidence of backend feasibility, not proof of general automatic cleanup.
The scheduled milestones in the roadmap may overlap only when dependencies and
test evidence support doing so.
