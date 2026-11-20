# Qutes 0.3 completion audit

Date: 2026-11-04. Package 0.3.0.dev0; language 0.3; artifact schema 3.
Validation evidence and exact environments are in knowledge/VALIDATION.md (V018).

| Requirement | Implementation and evidence |
| --- | --- |
| Generic membership and contiguous patterns | membership.py independent semantics; asymmetric checker; construction expansion; test_membership.py and A019 |
| Strings as sequences and wildcard patterns | string/char-array combinations, whole string entries, foreach, quantum wildcard correlation and padding-aware character access |
| Coherent comparison and cleanup | existing reversible comparisons/Boolean networks; complex reference-entangled overlap test and zero-workspace checks |
| Named one-element oracle and selected value | checker purity/signature/call graph checks; SearchOracle construction; visible view over owned result/index/workspace |
| Automatic conditional 99% success | Yoder-Low-Chuang schedule; independent Chebyshev checks and emitted small-state circuits across match counts |
| Quantum collections, duplicates, no matches | branch/reference-entanglement tests, duplicate index weighting, invalid-index suppression and no-match branch tests |
| Ownership, alias protection and measurement | replayable preparation with captured versions; moves/returns, changed-input cleanup, readonly guards, partial measurement and explicit impossible cleanup |
| Bounded construction | membership comparison preflight, search expansion checks, backend operand limits; configuration and budget rejection tests |
| Public integration | CLI float setting/reports, artifact-v3 generation and legacy import rejection, generated phase comparison/respecialization, SVG/console tests and existing PNG tests |
| Distribution | full Windows/Linux suites, installed isolated CLI/search smoke tests, pinned parser regeneration, no-Java/no-Qiskit core compilation, wheel source inventory and source package checks |
| Continuity and Git | KB-016 through KB-018, V016 through V018, three coherent local checkpoints; user snapshots and grammar/.antlr excluded |

Known limits match the approved scope: same-length searched strings, one-dimensional
representable collections, pure basis oracles, explicit measurement, no hybrid
retry/enumeration, no general quantum indexing, no custom state-domain preparation.
Selected-value measurement may prevent local hidden-index cleanup. Linear indexed
access is reported honestly; no end-to-end speedup or hardware validation is claimed.
Python 3.12 and hosted CI are configured but not run locally. No human review claimed.

## Historical 0.2 audit

# Qutes 0.2 increment audit

Date: 2026-11-01. Package 0.2.0.dev0; language 0.2; artifact schema 2.

- ANTLR 4.13.2 authoritative grammar, committed generated Python, matching runtime,
  pinned generator hash, reproducible regeneration check in CI. No Java for users.
- Top-level execution, ordinary callable main, inferred explicit classical returns,
  root input declarations, shared globals with transitive initialization checks.
- Inferred function effects, measurement helpers, readonly alias/predicate protection,
  current-global specialization and joins across early returns. Existing staging,
  loop, cleanup and no-hidden-measurement requirements remain enforced.
- Syntax errors include excerpts/hints/related locations and bounded collections.
  No recovered program executes. Unknown-name suggestions are conservative.
- Versioned generated-module API rejects old modules before cached execution or
  embedded-source respecialization. Public source compilation API remains stable.
- Semantic fixtures migrated directly to scripts; exact quantum-state/correlation
  and cleanup tests retained. New coverage includes global effects, arbitrary complex
  states entangled with references, snapshots, input schemas and artifact guards.
- User-edited snapshots.qut is untouched. The canonical script example is now
  measurement_snapshots.qut; the preserved legacy main requires an explicit call.

Final cross-platform/package evidence is recorded in knowledge/VALIDATION.md (V015).
No hosted CI, remote push, hardware validation, formal proof or human review is claimed.

## Historical V1 delivery audit

### Original V1 audit

Date: 2026-10-31. Package: 0.1.0.dev0; language contract: 0.1.
The evidence below concerns the V1 boundary in [the archived plan](history/development-plan-v0.3.md), not the later
hybrid/hardware roadmap. This is an automated implementation and verification
audit, not a claim of independent human review or formal proof of the compiler.

## Requirement coverage

| Requirement | Implementation and evidence |
| --- | --- |
| Compact C#-inspired syntax, strong types | Lexer/parser, grammar, checker, source spans; parser/checker tests and all 33 acceptance cases |
| qubit, signed quint, quchar, qustring | Configured codecs, typed IR, lowering; exhaustive small signed widths and custom/unused alphabet-code tests |
| Familiar assignment and value copies | Reversible self-update, versioned overwrite, separate correlated storage; full-state/correlation tests and unsafe-overwrite negatives |
| Addition and rotations | Shared gate expansion and Qiskit ModularAdderGate; independent permutations on basis and complex entangled inputs |
| Functions | Read-only borrows, inlining, owned return transfer, recursion rejection, anonymous result cleanup; construction/lowering ownership tests |
| if/else | Signed/Boolean coherent predicates, controlled branches, cleaned scratch; full-state comparator/control tests |
| for/while/foreach | Bounded construction-time expansion, array views, shape/index checks; accepted loops and measured/quantum-loop negatives |
| Arrays and text | Fixed lengths/capacity, configured alphabet, separate string length, indexing, updates, copies, equality, snapshots; collection tests |
| Automatic uncomputation | Version-aware dependencies, temporary input restoration, cycle rejection, no hidden observation/reset; cleanup tests with reference entanglement |
| Non-consuming measurement | Explicit distinct snapshot bits, continued evolution, measurement checkpoints, conservative indirect-measurement rejection; exact projected-branch and Aer tests |
| Measured if | Immutable snapshot predicates, sign extension, compound guards, mixed controls; exhaustive classical comparator and source feedforward tests |
| Qiskit transpilation | Backend-neutral scheduled gates, readable generated Qiskit Python; all 17 positive corpus cases execute from generated modules |
| Public interfaces | check/build/run/explain, JSON diagnostics, compile_source, generated build(inputs)/run(inputs,shots,seed); delivery tests |
| Fresh classical inputs | Generated modules actually recompile with new bindings/array sizes; invalid Boolean-vs-integer inputs cannot use specialization cache |
| Metadata and decoding | Source/build hashes, versions, resolved settings, ordered result layout, allocations/cleanup, estimates; deterministic artifacts and signed/text/array decoding tests |
| Resource bounds | Parser/evaluator/loop/width/JSON/expansion/shot bounds; reserved-qubit preflight and post-transpile check; guard tests before simulator execution |
| Future hybrid integration | Source compilation, circuit building, execution, decoding separated; no claim that live state survives separate jobs |
| Durable AI handoff and Git | AGENTS.md, knowledge status/tasks/decisions/ledger/validation; coherent local checkpoints, no remote publication |

## Delivery evidence

- Full isolated Windows Python 3.13.5 suite: **577 passed**, no warnings,
  `artifacts/checks/run-o9kdw90c`.
- Wheel built and installed in the clean environment. `pip check` reports no
  broken requirements. `python -I tools/verify_install.py` verifies installed
  imports, CLI entry point, execution, and new-input generated-module behavior.
  Evidence: `artifacts/installation/windows.json`.
- A second environment containing only the core wheel successfully checks source
  and generates Python without Qiskit/Aer installed.
- Full isolated Debian/WSL Python 3.13.5 suite: **577 passed**, no warnings,
  `artifacts/checks/run-w6545yxc`. The installed wheel passes the same isolated
  CLI/respecialization checks; dependency consistency passes. Evidence:
  `artifacts/installation/linux.json`.
- A Windows/Linux Python 3.12/3.13 GitHub Actions matrix is included. It has not run
  on hosted CI: this repository has no remote. Python 3.12 is a CI target, not a
  locally exercised environment in this audit.

## Intentional limits

- Conservative cleanup can reject legal quantum computations that need stronger
  dependency analysis. Released physical wires remain reserved for reconstruction;
  reports include their cost. Physical reuse is optional under the V1 contract.
- Main's named quantum outputs may remain live until shot completion. Anonymous
  helper results and scoped temporaries must clean or fail; there is no silent
  garbage retention as a substitute for uncomputation.
- Conditional measurement, measurement-driven/quantum loops, measured arithmetic,
  quantum indexing, dynamic sizes/lengths, mutation parameters, recursion, general
  state preparation, and broader quantum arithmetic remain outside V1.
- No backend/hardware/noise claim beyond the pinned ideal Aer environment. Estimated
  gate counts are before backend decomposition; statevector memory excludes overhead.
- Builtin spellings are the documented working defaults. No separate naming review,
  independent human correctness review, public package publication, or remote push
  is implied by this implementation.

## Primary backend and packaging references

- [Qiskit classical expressions](https://quantum.cloud.ibm.com/docs/en/api/qiskit/circuit_classical)
- [ModularAdderGate](https://quantum.cloud.ibm.com/docs/en/api/qiskit/qiskit.circuit.library.ModularAdderGate)
- [AerSimulator](https://qiskit.github.io/qiskit-aer/stubs/qiskit_aer.AerSimulator.html)
- [psutil 7.0.0 release files](https://pypi.org/project/psutil/7.0.0/#files)
- [GitHub checkout](https://github.com/actions/checkout), [setup-python](https://github.com/actions/setup-python), [upload-artifact](https://github.com/actions/upload-artifact)

Online references were checked during delivery work. Runtime compatibility claims
come from the pinned local tests, since current online API docs can describe newer
versions than those installed.
