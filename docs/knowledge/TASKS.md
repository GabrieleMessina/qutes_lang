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
| T007 | DONE | Bounded classical evaluator and user-function inlining with source mapping. | T006 |
| T008 | DONE | Dependency/version model, cleanup synthesizer, and arithmetic lowering with full-state verification. | T004, T006 |
| T009 | DONE | Integrate coherent branches, functions, and construction-time loops. | T007, T008 |
| T010 | DONE | Arrays/text/configuration integrated with lifetime analysis. | T009 |
| T011 | DONE | Non-consuming measurement, snapshots, feedforward, results decoding, Qiskit emitter. | T010 |
| T012 | DONE | CLI check/build/run/explain, generated modules, packaging, resource limits, documentation, CI/release evidence. | T011 |
| T013 | DONE | User-requested console circuit diagrams and PNG/SVG export to a folder; optional dependencies, CLI/API checks, documentation. | T012 |

M1 readiness requires T002-T004 plus a review of unresolved limitations. A passing
probe is evidence of backend feasibility, not proof of general automatic cleanup.
The scheduled milestones in the roadmap may overlap only when dependencies and
test evidence support doing so.

Evidence for T002-T004: KB-002 / V002, 37 passing tests. This is the initial automated specification/feasibility gate; final naming, human review, and a clean dependency installation are not implied.

Evidence for T005: KB-003 / V003, 102 passing tests total; all 33 corpus cases checked for syntax. T006 is the next unblocked task, not started. No semantic acceptance or source execution is claimed.

T006 evidence: KB-004 / V004, 173 passing tests. T007 is next; typed analysis deliberately leaves Q3001 cleanup obligations for the later pass.

T007 evidence: KB-005 / V005, 216 tests. T008 is next: scoped dependency/version cleanup and circuit lowering. T009-T012 remain pending integration/release; construction alone does not satisfy them.

T008 partial evidence: KB-006 / V006, 267 tests. Backend-neutral gates, standalone
versioned cleanup schedules, and the reversible Qiskit adapter are implemented.
Source integration, measurement checkpoints, and acceptance cleanup diagnostics
remain outstanding, so T008 stays ACTIVE.

T008 completed at KB-007 / V007: 312 tests. Scalar source arithmetic, assignment,
scope cleanup, measurement checkpoints, and both cleanup-negative examples are
integrated. T009 is ACTIVE: helpers and expanded loops work for scalars, while
quantum predicates/dynamic branches remain. T011 has partial measurement evidence,
but feedforward, text/array decoding, and full execution tooling are still pending.

T009 completed at KB-008 / V008: 377 tests. Signed/Boolean predicates, coherent
branches, conditional overwrite, branch cleanup, helpers/loops under controls,
and changed predicate-input history all have full-state evidence. T010 is ACTIVE.

T010 completed at KB-009 / V009: 405 tests. Arrays/text, indexing, foreach borrows,
value copy/ownership, lengths/padding, branch joins, snapshots, and type-width bounds
are integrated. T011 ACTIVE: only source feedforward remains from its core features;
release execution/serialization/CLI validation belongs to T012.

T011 completed at KB-010 / V010: 529 tests. All 17 positive examples execute on Aer;
signed/text/Boolean runtime predicates, immutable snapshots, mixed controls, guarded
overwrite, and anonymous temporary cleanup have independent semantic evidence.
T012 ACTIVE. Full goal remains incomplete until generated-module/API/CLI/release
requirements are implemented and audited, not merely the example corpus.

T012 completed at KB-011 / V011: 577 tests pass in each of clean Windows and Linux
Python 3.13.5 environments. Generated modules execute the complete corpus and
respecialize new inputs. Installed-wheel/entrypoint checks, core-only installation,
resource guards, documentation/examples, source package, and requirement audit are
complete. A Python 3.12/3.13 Windows/Linux CI matrix is included but has not run on
hosted infrastructure; no remote exists. See docs/release-audit.md for exact limits.

All V1 tasks are DONE. The hybrid/hardware/editor roadmap is future scope and
requires a new task; do not label it implicitly implemented by the current APIs.

T013 completed at KB-012 / V012: final compiler diagrams on check/build/run/explain,
PNG/SVG files, lazy optional dependencies, JSON-safe console output, atomic writes,
image-size guards, and documentation. Full Windows suite: 596 passed. Linux
rendering/CLI suite: 28 passed; installed flags verified on both platforms.

## Qutes 0.2 approved increment

- T014 DONE: ANTLR migration/diagnostics; KB-013 / V013.
- T015 DONE: scripts, globals, input declarations, inferred function effects.
- T016 DONE: migration, generated-artifact contract, Windows/Linux validation.

T015 evidence: KB-014 / V014; script/global/effect semantics and migrated semantic corpus.

T016 evidence: KB-015 / V015. Full Windows/Linux suites 666 each; installed wheels,
artifact migration guards, Java-free core installation, diagrams, regeneration,
source/wheel packaging and active 0.2 documentation verified. No hosted CI run.

## Qutes 0.3 approved increment

- T017 DONE: coherent `in`, wildcard/sequence semantics, string foreach,
  independent reference behavior, tests and authoritative grammar regeneration.
- T018 DONE: `search(collection, oracle)`, fixed-point amplification at configurable
  99% success, returned selected value with retained selection index, phase gates,
  effect validation and ownership/cleanup. Depends on T017.
- T019 DONE: version 0.3/artifact 3, examples/specification, reports, generated code,
  full Windows/Linux validation and installed-package smoke tests. Depends on T018.

T017-T019 complete at KB-018 / V018: 775 tests on each platform, installed 0.3
wheel/CLI/search checks, artifact migration, core-only compile, parser reproduction,
source packaging and requirement audit. All commits local; user experiments preserved.

## Language operation examples

- T020 DONE (KB-019/V019): 38 independent operation examples, maximum 21 qubits,
  explicit config/input fixture, coverage/output catalog and linked guide. All run
  under the 24-qubit cap. Full Windows/Linux suites: 814 passed each. Includes the
  user's explicitly authorized config, ignore-file and snapshot edits.

## Circuit readability and CLI guidance

- T021 DONE (KB-020/V020): resource units, wildcard warnings, CLI walkthrough, roadmap consolidation.
- T022 DONE (KB-021/V021): source provenance, named registers, aliases, cleanup annotations.
- T023 DONE (KB-022/V022, 858 tests each platform): hierarchical diagrams, selective unfolding, integration and validation.
- T024 DONE (KB-025/V025): certified-zero reuse, multi-epoch reconstruction,
  physical execution/config/artifact4 with legacy3 support, physical/logical views,
  reports and 39-example tour. Full Windows/Linux 907 each; installed/core/parser
  checks pass. See docs/wire-reuse-audit.md. Scheduling/routing/dirty ancilla deferred.

## Approved 0.4 increment

- T025 DONE (KB026/V026): references/types, float/complex, readonly/mut, explicit copy, indexed foreach.
- T026 DONE (KB027/V027): live operations, atomic effects and cleanup safeguards.
- T027 DONE (KB028/V028): sparse explicit preparation and signed subtraction/negation.
- T028 DONE (KB029/V029): ranges/slices, conservative support and coherent quantum indexing.
- T029 DONE (KB030/V030): artifact5/legacy guard, migration, 50 examples, documentation,
  safety audit, full Windows/Linux 1032 each, parser, installed/core package and CLI validation.

Contract: docs/spec/language-v0.4.md. Parsing/probes do not constitute delivery.

T030 DONE: import, resources, release metadata and validated notebook. T031 DONE: pinned browser compiler and resource bundle, four verified starters, learning paths, standalone downloads, three browser engines, cross-backend checks, Firebase preview and live publication. See KB034/V033.

T032 DONE: publish qutes2.0 with both original histories, move the existing release to tag 2.0, verify assets and remove v0.4.0. See KB035 and V034.

T033 DONE: migrate both website release URLs, verify the pinned bytes, deploy to Firebase preview and production, and exercise the public download and playground.

T034 DONE: published compiler 2.0.0 and matching downloads, renamed website branch to qutes2.0, verified locally and dispatched website deployment without waiting for hosted completion.

T035 DONE through local delivery: interactive tutorial, three output tabs, updated navigation/footer and redirects. Publication awaits separate user approval.

T036 DONE locally: replaced the four-step tutorial with four modules and eight runnable labs, including a teleportation repair and receiver audit. Publication requires a new owner instruction. See KB039 and V038 for review and verification.

T037 DONE: five native portable archives, checksum manifest and platform chooser are public on the existing 2.0.0 release. See KB040 and V039.

T038 DONE locally: the Build page links five portable archives and guides readers through running and editing the bundled Bell program. Publication awaits owner review.

T039 DONE: published the five portable archives, starter, teaching bundle, checksum manifest and revised description on release 2.0.0. See KB042 and V041.

T040 DONE locally: simplify Tutorial and Build, and pin the preview to the r2 release. Publishing the website remains the owner's decision.

T041 DONE: release 2.0.0 has exactly the five r2 platform archives and their checksum file. Source instructions, native packaging, and the local website are updated. Next action is owner review before any website deployment. See KB044 and V043.

T042 DONE: production serves the reviewed website. All five platform links and checksums passed, the retired teaching ZIP returns 404, and merged Codex working branches were cleaned up in both repositories. See KB045 and V044.

T043 DONE locally: the standalone playground download passed the isolated Qiskit/Aer acceptance test. CLI exports match the previous generator. Review the local playground before authorizing publication.

T044 DONE: both qutes2.0 branches published in order, production promotion verified, and eight actual live browser exports executed in the isolated Qiskit/Aer environment. See KB047 and V046.

T045 DONE: verified the new cache policy on preview and production, reused the unchanged runtime, and downloaded the standalone Bell program in a returning browser. The hosting workflow now runs these HTTP checks on subsequent releases.
