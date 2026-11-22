# Work ledger

Append meaningful batches, failures, choices, checks, and handoff points. Use stable
entry IDs; do not rewrite history to hide failures.

## KB-001 — 2026-10-30 — Repository and continuity bootstrap

- User requested implementation, a knowledge-base workflow, and logical commits.
- Inspected workspace and ancestor instructions: only DEVELOPMENT_PLAN.md existed;
  no applicable ancestor AGENTS.md was found.
- PATH `python` and `py` failed as inaccessible Windows application aliases.
- Registry inspection found `C:\ProgramData\anaconda3\python.exe` (3.13.5).
  Confirmed installed Qiskit 2.3.0, Aer 0.17.2, NumPy 2.1.3, pytest 8.3.4.
- Initialized local Git on main; existing Git author identity is available. No
  remote created and no global settings/packages changed.
- Added contributor instructions, ignored generated artifacts, and this knowledge
  base with status, tasks, decisions, validation, and links to the roadmap.
- Initial Git staging failed because this environment protects `.git` writes.
  Retry uses the elevated Git operation authorized by the user's commit request;
  no file-permission changes or deletion of lock files are needed.
- Next: semantic contract, executable acceptance inventory, dependency pins, and
  independent backend feasibility checks. See T002-T004.

## KB-002 — 2026-10-30 — Specification and backend feasibility

- Committed KB-001 as `a29edbf`. Git's whitespace check caught extra blank EOF
  lines before that commit; normalized them and established LF attributes.
- Added a working EBNF grammar and language contract, diagnostic categories, and
  33 source examples (17 positive, 16 negative). Their semantic execution remains
  pending; the manifest records the intended first failure stage and outcomes.
- Added a Python package skeleton, central builtin vocabulary, validated config,
  signed arithmetic codecs, and configurable text encoding. Added exact installed
  dependency pins; no global packages were changed.
- Built an independent small-state oracle based on index permutations/projections,
  plus separately constructed Qiskit experiments. Checked coherent addition and
  rotation, correlated copy, compute/use/uncompute, and dynamic measurement with
  subsequent evolution and retained classical snapshots.
- First direct pytest attempt: 34 passed, 1 fixture setup error caused by the host
  temporary directory. No semantic test failed. Added tools/check.py to use fresh
  task-owned artifact directories and disable unrelated pytest plugin autoload.
- Second run passed all 35 then-existing tests. Installed IBM runtime contributes
  deprecation warnings through Qiskit plugin discovery; this is documented rather
  than hidden. Added corpus integrity and unchanged-repeat-measurement checks.
- Names remain documented working defaults; no independent human review is claimed.
- Next checkpoint: final M1 verification, then parser/source-location work T005.

## KB-003 — 2026-10-30 — Parser and syntax tooling

- M1 checkpoint committed as `4b8d3d8`; V002 recorded 37 passing tests.
- Implemented source coordinates/diagnostics, a UTF-8-aware lexer, immutable untyped
  AST, recursive-descent statements, and precedence-climbing expressions.
- All 33 corpus cases are checked at the syntax layer: 31 parse, and the two
  intentional lexical/syntax failures have the specified diagnostics. The 14
  semantic-negative cases remain deliberately unvalidated by the parser.
- Added `qutes parse FILE [--json]` and a checkout runner `tools/qutes.py`.
  Success explicitly says types and quantum safety have not been checked; file
  failures and malformed source return structured diagnostics and nonzero status.
- Added tests for precedence, grouping, calls, arrays, loops, literal escapes,
  Unicode scalar characters, CRLF/BOM positions, malformed and truncated input,
  CLI execution, and deep nesting. Inspection identified that flat operator
  chains could still produce deep serialized ASTs; added an iterative tree-depth
  check in addition to the parser recursion guard. Preserved CRLF offsets in CLI
  file reads rather than applying newline translation.
- Initial frontend subset: 82 passed, 18 backend tests deselected. Final full run:
  102 passed in 5.60 seconds; V003 contains the reproduction command and limits.
- No parser result is represented as semantic acceptance; no general uncomputation,
  source-to-circuit generation, or program execution has been implemented.
- Next: T006 name resolution/type/stage/effect analysis and structured typed IR.
  Begin with symbol tables, explicit classical/quantum/runtime categories, and the
  semantic-negative corpus. Keep cleanup failures (R004/R005) for the cleanup pass.

## KB-004 — 2026-10-30 — Typed frontend and staged helper analysis

- Revalidated the clean worktree at 18d3d56. The prior implementation checkpoint
  was concrete progress; the full goal remains active and incomplete.
- Implemented structured typed IR and name/type/stage/effect analysis, separate
  from parsing and cleanup. Symbols have stable IDs, values carry stages/shapes,
  and function helpers specialize for construction-time versus measured inputs.
- Added lexical scopes, readonly parameters/iteration views, return/entry-point
  checking, recursion rejection, operator/conversion checks, condition dependency
  protection, branch-state merging, loop-stage validation, and bounded analysis.
- Classical short-circuiting avoids eager constant faults in unused operands;
  type/name errors remain visible. Loop analysis discards stale constant values.
- Added developer `analyze` with typed JSON, config loading, and width overrides.
  It explicitly does not claim cleanup or full construction-time validation.
- All 17 positive corpus examples analyze. Twelve semantic-negative examples now
  produce their intended diagnostics; two cleanup-negative examples remain
  intentionally accepted at this layer. Lex/parse failures remain diagnosed too.
- Added 68 checker tests plus 3 CLI tests. Full suite: 173 passed (V004).
- Two batched documentation patches failed context verification and changed no
  files; reread the actual README and applied smaller verified edits.
- No design input is currently required. Next: bounded construction-time evaluator
  and user-function elaboration, then dependency/version-based cleanup synthesis.

## KB-005 — 2026-10-30 — Bounded construction and function inlining

- Committed KB-004 as e94314a. Continued the full active goal without a new design
  blocker; the next work is storage/version cleanup, not project completion.
- Added a bounded partial evaluator over typed IR. Classical operations execute;
  loops expand globally within budgets; helper calls inline with fresh local
  symbols. Quantum operations and runtime measurement snapshots remain symbolic.
- Added scope/ownership handoff annotations and explicit moves for owned helper
  results. These annotations are obligations for the cleanup pass, not proof that
  local quantum information can be discarded.
- All 17 positive source examples construct. Added input/range/bounds checks,
  dynamic shape validation, immutable classical array copies, early returns,
  distinct per-iteration storage, snapshot preservation, and deterministic IR.
- Review found compound indexed assignment could evaluate an index helper multiple
  times; fixed evaluation-once behavior and added a regression. Temporary quantum
  foreach arrays are now materialized once before borrowing elements.
- Review found quantum foreach aliases could bypass predicate-input protection.
  Propagated borrowed collection dependencies in the checker; added regression.
- Added configurable max_classical_bits (65536 default), which diagnoses resource
  excess without wrapping classical integers. Array allocation charges the step
  budget before allocating host memory.
- Added developer construct command with JSON inputs/IR, and construction IR docs.
  An initial documentation patch missed README context and made no changes; read
  the actual text and reapplied the patch successfully.
- Full suite: 216 passed (V005). Quantum cleanup synthesis, source-to-Qiskit output,
  runtime result decoding, and release verification remain outstanding.

## KB-006 — 2026-10-30 — Versioned cleanup scheduler and reversible adapter

- Continued from 5ad3bae with a clean tree; full goal remains active. No new user
  design decision is required. Inspected installed Qiskit APIs and primary Qiskit/
  Silq documentation before implementing the reversible layer.
- Added backend-independent operations and explicit positive/negative controls.
  Added a separately imported Qiskit adapter for copy, modular addition, constant
  addition, preparation, and rotation. Controls that overlap source bits are
  expanded without duplicating Qiskit operands; target overlap is rejected.
- Implemented automatic cleanup schedules with storage versions, captured input
  versions, temporary input restoration, released computation reconstruction,
  cyclic dependency rejection, root ownership, and bounded scope cleanup.
- Derived-value overwrite records a reversible composite step, preserving old
  versions for other consumers. Independent unknown roots cannot be overwritten.
  This does not restore the user's withdrawn function-only evolution restriction.
- Review found composite overwrite must allow a previously released dependency
  at version -1 (zero). Fixed dependency capture and added a complete-state test.
  Added bounded dependency nesting to avoid leaking host recursion failures.
- Added 51 checks for the scheduler and real emitted circuits: complex phases,
  entangled reference inputs, changed sources, recomputation, overwrite, roots,
  controlled arithmetic, rejection rollback, and resource diagnostics.
- Targeted runs: 49 then 51 passed. Full suite: 267 passed (V006). No source program
  is yet lowered through this scheduler; measurement boundaries, source branch
  integration, arrays/text, execution, and release work remain pending.
- Next: connect construction IR to the scheduler, starting with scalar arithmetic
  and scoped values, then add measurement checkpoints without consuming sources.

## KB-007 — 2026-10-30 — Scalar source circuits and measurement checkpoints

- Committed KB-006 as 0cdd467. Implemented explicit measurement operations, fresh
  snapshot bits, checkpoint-based cleanup/reconstruction, and dynamic Qiskit guards
  using recorded bits. Measurement leaves its source available for later updates.
- Kept pre-measurement version history instead of dropping older dependencies.
  Directly measured roots can be erased while their correlated outputs remain.
  Indirect measurement invalidates original preparations across the connected
  dependency graph; reject root cleanup without a direct checkpoint in that case.
- Connected source construction to storage and arithmetic lowering: scalar
  qubit/quint values, correlated copies, nested expressions, self-update chains,
  overwrite checks, scopes, helper moves, expanded loops, snapshots, result decoding.
  Main's remaining quantum values stay live until shot end; locals must be clean.
- Nine positive corpus cases now have exact output-distribution checks. All 16
  negative cases fail with the intended diagnostic, including R004/R005 at cleanup.
  Actual source-generated Qiskit executes the retained-snapshot program through Aer.
- Two targeted collection attempts failed with native Aer DLL initialization and
  Windows invalid-handle errors under pytest descriptor capture. Direct import and
  Python stream/no-capture runs succeeded. Updated the Windows runner to stream
  capture, preserving assertions and without changing global packages.
- First uncaptured source run: 42 passed, 3 test-fixture failures. Two constants 2
  were out of signed two-bit range; changed them to equivalent valid -2. One exact
  floating probability assertion was changed to the existing numerical tolerance.
  Targeted rerun: 45 passed. Full suite: 312 passed (V007).
- A documentation patch failed exact-context matching and made no changes; read
  the actual file and applied the corrected patch. No semantic rule was changed.
- T008 is complete for arithmetic/cleanup integration. T009 is active: coherent
  predicates/branches next, then quantum arrays/text, feedforward, and release tools.
  Full goal remains incomplete; no design decision is currently blocking progress.

## KB-008 — 2026-10-31 — Coherent predicates and branches

- Revalidated the prior worktree/test artifact and committed KB-007 as 0115815.
  The previous goal turn made concrete progress; no blocked/no-progress state.
- Added signed comparisons with reversible XOR-difference scratch and Boolean
  conjunction/disjunction. Literal operands and shared operands normalize without
  duplicated gate controls; the implementation does not enumerate truth tables.
- Added nested coherent if/else lowering and branch-local scope cleanup. Existing
  helper ownership and expanded loops compose with these controls.
- Extended overwrite scheduling to guard the entire erase/prepare sequence. A
  branch must preserve the old value when unselected; guarding only preparation
  would be incorrect. Reject cleanup that would modify the quantum condition.
- Added full complex-state tests with arbitrary inputs/reference entanglement,
  all six signed comparisons at widths 1-3, signed boundary constants, identical
  operands, Boolean combinations, nested branches, changed predicate inputs,
  conditional overwrite, helper/loop locals, and contradictory controls.
- A008/A009 now have exact source output-distribution checks. Targeted initial
  integration: 101 passed. Added one compound predicate regression and ran the
  full suite: 377 passed (V008). No new design input is required.
- T009 complete; T010 active for quantum arrays/text/layout/lifetime integration.
  Measured source feedforward and full CLI/release work still remain.

## KB-009 — 2026-10-31 — Quantum arrays and text

- Committed KB-008 as 6bde5d6. Added collection element storage and borrowed string
  bit views to lowering, including indexed updates, correlated value copies,
  whole-array replacement, foreach, empty arrays, and helper result ownership.
- Added configured character/string encoding and snapshot decoding, padded storage
  with separate logical lengths, length-aware equality, and retained text snapshots.
  Indexed string observation measures a copied view and cleans it using that
  explicit snapshot; it leaves the parent usable and adds no hidden measurement.
- Resolved the construction gap for string-array element lengths, propagating them
  through helpers, copies, updates, foreach views, branch joins, and measurements.
  Branches must agree per element; same array length alone is insufficient.
- Added unconditional array-permutation storage transfer without extra qubits.
  Conditional replacements still use guarded cleanup and may reject unsafe cycles.
- Added early type-width resource checks before huge integer encodings/padding and
  per-allocation budget checks. Tests use a huge configured width to establish an
  early diagnostic rather than actually allocating its physical bit tuple.
- Initial collection run: 61 passed, one invalid two-bit test constant. Corrected
  the test fixture. Full run then found a test assuming foreach over strings;
  kept the specified array-only contract and tested indexed text in a for loop.
  A failed documentation-context patch changed nothing and was reapplied correctly.
- Final full suite: 405 passed (V009). A013-A017 now execute with exact expected
  distributions; 16/17 positive examples have source circuit evidence.
- T010 complete. T011 active for source feedforward, followed by full CLI/build/run,
  serialization, resources, packaging, docs, CI, and release audit. Goal incomplete.

## KB-010 — 2026-10-31 — Runtime feedforward and ownership audit

- Continued from clean 0926943; the prior goal turn made committed progress.
  Checked primary Qiskit classical expression/control-flow documentation and
  validated emitted operations on the installed pinned backend versions.
- Added immutable classical predicate IR, balanced signed comparisons, Boolean
  combinations, text/length semantics, snapshot/index normalization, and Qiskit
  expression emission. Fresh backend expression nodes avoid mutable-node sharing.
- Runtime guards compose with coherent controls and cover complete overwrite
  transformations. Disabled unconditional array permutation rebinding under runtime
  guards. Snapshot IDs stay stable after later evolution or observations.
- Found direct RHS measurement in runtime &&/|| was being emitted eagerly by
  construction. Added Q2004 under the existing no-conditional-measurement rule;
  construction-time short-circuit and previously captured snapshot reads still work.
- Ownership audit found escaped helper results/computed arguments could remain as
  anonymous main values. Track explicitly named main quantum values; clean other
  temporaries at main end, rejecting stranded correlated roots instead of retaining
  hidden garbage. Added regressions for measured/unused roots and computed arguments.
- Added exhaustive classical signed predicates and real Aer execution for every
  positive corpus example, plus observed input-pair comparisons, mixed controls,
  stable snapshots, text/indexed predicates, branch overwrite, and cleanup tests.
- Targeted feedforward run: 118 passed. Full integration before ownership fix:
  526 passed. Final full suite: 529 passed (V010), 100 external warnings. No test
  failure or new user design blocker occurred in this batch.
- T011 complete, T012 active. Generated Python modules, public build/run/explain/check,
  resources, package validation, docs/CI, and release audit remain outstanding.
- The first Git staging attempt was not executed: automatic approval review hit
  a usage limit, explicitly not an unsafe-action determination. Worktree evidence
  remained intact. After the user resumed the goal and the indicated retry time
  passed, retry the ordinary approved Git path; do not bypass protected Git writes.
- The resumed normal approval review succeeded; Git staging is available again.

## KB-011 — 2026-10-31 — Delivery and installation

- Committed KB-010 as 6b92ec4. Added public compilation/runtime APIs, complete CLI
  check/build/run/explain, deterministic readable Python generation, embedded
  metadata/result layouts, and new-input respecialization. Factored reversible gate
  expansion so execution, generated Python, and cost reporting share one algorithm.
- Added pre-simulation limits, post-transpile limit checks, shot/seed validation,
  missing-backend/runtime diagnostics, safe atomic artifact writes, and source-file
  protection. Classical-only observable outputs explicitly report no simulator run.
- Added lossless large-integer JSON/source handling without changing Python's global
  digit limit. A new depth test exposed that installed packages can alter the host's
  recursion limit; JSON now has an explicit 512-level bound plus recursion handling.
- Existing CLI/feedforward checks: 132 passed. Initial delivery suite: 36 passed.
  Initial full run: 565 passed, 121 external warnings, run-4l_y7mpa. A later targeted
  run had one JSON-depth test failure (run-tg7h0zgo), now fixed; three targeted checks
  passed in run-g_dcctqy. Further example/runtime checks await the next full run.
- One combined delete/add patch was rejected atomically; reapplied the CLI rewrite
  as separate supported edits. No partial behavior was treated as validated.
- Added a user guide, runnable examples, installed-wheel smoke checker, and a
  Windows/Linux Python 3.12/3.13 CI matrix. No remote/push or hosted CI execution.
- Windows venv ensurepip first failed because the host temp directory was not
  writable. Project-local TEMP/TMP fixed setup. Restricted network DNS then blocked
  dependency downloads; normal approval review permitted isolated installation.
- Clean install found psutil 5.9.0 lacks a Python 3.13 Windows wheel and requires
  unavailable C++ tools. Updated pin to 7.0.0 and retrying using wheels only. Existing
  Debian Python 3.13.5 is available; created artifacts/linux-venv and installing
  the same lock there. Docker daemon is unavailable; no service was started.
- Current work: finish isolated installs, wheel/entrypoint smoke checks, both full
  suites, coherent commit, and requirement audit. Goal remains active; no user
  language-design decision is needed.
- Completion of that work: clean Windows and Debian installs succeeded with the
  corrected wheel-backed pins. Initial isolated suites passed 575 Windows / 576
  Linux tests. Added deterministic guarded-artifact coverage and fixed embedded
  metadata decoding to honor explicitly raised classical integer memory limits;
  external JSON still has a bounded integer-token limit. Final suites: **577 passed
  on each platform**, no warnings. Exact commands/artifacts are in V011.
- Built/installed the wheel, checked isolated imports/entrypoints and generated
  respecialization, and verified dependency consistency. A separate environment
  with only pip and the core wheel checks/builds source; run reports Q5001 as intended.
- Added source distribution manifest, including examples, docs, tests, independent
  experiments, and CI. Package products/environments remain ignored. Reviewed the
  complete V1 requirement table in docs/release-audit.md; future hybrid/hardware
  scope is explicit. No public release, remote push, or human review is claimed.
- T012 and the V1 plan are complete. This batch is one coherent delivery commit;
  inspect Git log for its identifier. Keep named post-measurement values live and
  retain ordinary assignment in any future revisions.
- Built a wheel from the source distribution too; verified archive inventory and
  exact byte equality of all 24 compiler modules in both wheels and the checkout.
  Final documentation-only edits record this evidence and align the generated-module
  tutorial's parameter example with the actual loops program.

## KB-012 — 2026-11-01 — Circuit diagrams

- User requested a compiler option to print the final circuit and an option to
  save images in a folder. Read the knowledge base and inspected clean 906b88e.
- Plan: --print-circuit, --save-circuit FOLDER, --circuit-format png|svg on
  check/build/run/explain. Render the complete compiler-emitted Qiskit circuit
  before backend-specific decomposition, with all cleanup and measurements.
  JSON stdout stays parseable; text diagrams use stderr when --json is present.
- Verified Qiskit drawer documentation and installed 2.3.0 implementation.
  Use text and Matplotlib drawers, not LaTeX external processes. Image libraries
  will be optional and installed only into project-local environments.
- Implemented the planned flags with lazy rendering. Text remains legible on
  ASCII-only consoles. PNG/SVG files use source/build-hash names, atomic replacement,
  parent-folder creation, dimension bounds, and figure/temp-file cleanup. Empty
  classical programs have an explicit diagram. Added Q5003 rendering diagnostics.
- Added visualization extra and pinned Matplotlib 3.10.0/pylatexenc 2.10 plus
  transitive dependencies. Restricted package lookup failed; normal approved network
  access succeeded. pylatexenc builds a pure Python wheel; CI's binary-only install
  now has an explicit exception for that dependency. No global package changes.
- Initial targeted run: 26 passed, one ASCII-wire test failure. Added double-line
  wire mappings; rerun passed 27. Added a partial-figure failure regression, bringing
  rendering/CLI checks to 28, which pass on Linux. Generated PNGs for feedforward
  and coherent_if and visually verified labels, controls, measurement, and folds;
  SVG export also passed. Refreshed and exercised installed Windows/Linux commands.
- The first full suite had 595 passes and one failure because functions.qut changed
  during work to return [2,3] while its existing test expected 3. Preserved the edit
  and ran a temporary validation snapshot with only that fixture restored from HEAD:
  596 passed. The user then confirmed the edit was an experiment and reverted it.
  Verified the file has no diff and reran the normal workspace suite.
- Two status-document patches failed exact-context verification and made no changes;
  the corrected patch succeeded. T013 is complete; see V012 for final evidence.

## KB-013 — 2026-11-01 — ANTLR and diagnostics checkpoint

- Read continuity/specification and inspected 1826686; user snapshots.qut edit
  adds numberb and changes addition. Preserved byte-for-byte, excluded from commits.
- Implemented authoritative grammar, generated Python parser/lexer, independent
  AST adapter, scalar literal validation, bounded syntax/error collection, source
  excerpts and actionable hints. No backend semantics moved into grammar.
- Downloaded pinned generator and installed runtime only into project .venv.
  Initial restricted DNS failed; approved network retry succeeded. Existing Java:
  C:/Program Files/Android/openjdk/jdk-21.0.8/bin/java.exe. Jar under artifacts/antlr.
- Generator SHA256 is checked before regeneration; generated source is reproducible.
- Parser suite 60 passed; full suite 599 passed and one expected example mismatch:
  user's snapshots computes [5,-6] with configured four bits versus baseline [5,7].
  No compiler regression found; do not overwrite the experiment to make tests green.
- Next checkpoint: change entry semantics, globals/inputs, inferred call effects.

## KB-014 — 2026-11-01 — Scripts and inferred effects

- Implemented ordered script statements, inferred classical return type, root-only
  input declarations, filewide globals with initialization checks, ordinary main,
  global read/write effects, call-site borrow/predicate/dynamic-write protection,
  measurement in helpers, and shared global construction environments.
- Specialize each call against current global state; preserve function cleanup
  boundaries. All readonly parameter assignments still fail. No measurement/reset
  is introduced to repair invalid cleanup.
- Migrated embedded fixtures and acceptance programs to actual script source (no
  runtime adapter); retained function-syntax/parser location tests. R010 now tests
  forbidden conditional measurement through helpers; A018 tests allowed helpers.
- Mechanical migration initially exposed outdated main-required expectations,
  f-string fixtures, a Unicode source-offset edit issue, and input used as a former
  identifier. Corrected fixtures to test the new contract without dropping semantic
  coverage. New keyword is input; affected former variable names became operand.
- Existing full-state tests pass; added arbitrary complex reference-entangled state
  test for global updates and clean helper scratch, exact correlated measurement
  branches, nested readonly alias checks, and per-call stage/shape changes.
- Found/fixed skipped short-circuit RHS propagating global state in analysis; reject
  runtime conditional writes. Found/fixed unterminated-comment matcher swallowing
  closed comments with odd star runs. Added dedicated regressions for both.
- Full suite 653 passed; subsequent targeted frontend/script suite 117 passed.
- Still to deliver: versioned artifact compatibility, documentation, packaging and
  full Windows/Linux validation. Preserve user's snapshots file; canonical script
  now lives in measurement_snapshots.qut.

## KB-015 — 2026-11-01 — Versioned delivery and cross-platform completion

- Versioned package/language/artifacts to 0.2.0.dev0 / 0.2 / 2. Added artifact_v2
  adapter and import-time legacy error; tested cached and new-binding paths so
  old embedded main-only source can never silently execute with new semantics.
- Published active 0.2 contract; marked 0.1 historical. Updated grammar summary,
  guide, README, roadmap, IR/lowering notes, release audit, CLI help and CI. Added
  pinned-Java regeneration verification to CI; hosted workflow has not been run.
- Final semantic review distinguished owned computed arguments from direct readonly
  aliases and fixed global stage/shape joins across early return paths. Dedicated
  tests cover both; no broadening of runtime control/measurement scope.
- Added core dependency to metadata and adjusted its exact-key test. The first
  targeted delivery run had one stale metadata expectation; corrected and all
  subsequent suites pass. Diagnostics now describe active borrows as well as
  quantum-condition protection, with a targeted 50-test rerun after wording edit.
- Full Windows/Linux suites both passed 666 tests. Both installed package smoke
  checks execute CLI and respecialize generated modules; pip check passes.
- Pinned ANTLR runtime installed only in project Windows/Linux/core environments.
  Restricted DNS on wheel download failed; approved network retry succeeded.
  Existing Java 21 regenerated committed sources exactly; jar SHA256 checked.
- Core-only installed wheel compiled and generated source with PATH empty and no
  Qiskit; simulation produced Q5001. Installed console/SVG circuit export passed.
- Built final wheel/source distribution, verified every compiler .py byte in the
  wheel against checkout, and verified grammar/hash/generator/parser/spec in sdist.
  Reinstalled final wheel in Windows/Linux/core environments; no global packages.
- T016 and the approved increment are complete. Third coherent local checkpoint
  records code/tests/docs/knowledge. No remote/push, hardware or human-review claim.
- User snapshots.qut experiment remains byte-for-byte untouched and uncommitted.
  Its ordinary main now requires an explicit call; tutorial replacement is
  measurement_snapshots.qut. Future agents must preserve this distinction.

### 2026-11-02 — Resume the final Git checkpoint

The first staging attempt did not execute: automatic approval review had reached
its usage limit. On resume, the index was empty and both earlier checkpoint
commits were present. Verified all 30 compiler modules against the tested 0.2
wheel and confirmed the recorded Windows/Linux JUnit reports (666 each, zero
failures, errors or skips) and final diagnostic regression run (50 passed).
Only the delivery changes belong in this commit; the snapshots experiment is
excluded. No compiler changes or additional packaging were needed on resume.
The staged diff exposed an encoding change to punctuation in historical records;
restored it and verified both documents retain the complete original 0.1 records.

### 2026-11-04 — KB-016 membership implementation underway

Resumed KB-015 baseline and approved 0.3 plan. Preserved snapshots.qut and newly
observed untracked grammar/.antlr directory. Implemented independent membership
semantics, asymmetric typing, bounded window expansion through reversible Boolean
comparisons, wildcard handling, and string foreach. Regenerated ANTLR from the
pinned jar. Initial 28 focused tests pass (run-hkmyce4j, 15.40s). A combined test/
ledger patch failed its ledger context check; reapplied test file separately.
Search and release integration remain unimplemented.

Membership checkpoint: 694 full Windows tests pass (V016). T017 DONE; T018
ACTIVE. Reviewed implementation and grammar diff; no changes to user snapshots
or untracked grammar/.antlr. Search and release are still outstanding.

### 2026-11-04 — KB-017 automatic collection search

Implemented named oracle validation and transitive purity checks; construction
specializes classical captures and compiles one reusable quantum-element oracle.
Added backend-neutral RY/phase gates, exact non-power-of-two index preparation,
and Yoder-Low-Chuang amplification with failure default 0.01. Selection index and
zero workspace belong to the result allocation; a visible view exposes only its
value. Replayable preparations record input versions and retain measurement/live
dependency guards. Added resource/algorithm reports and emitted phase operations.

Initial tests had six fixture failures (out-of-range 2-bit threshold and reserved
input identifier), fixed without changing language behavior. A direct probe first
loaded the installed 0.2 wheel; corrected to explicitly import checkout src.
The first Git staging attempt was denied by filesystem permissions; approved
local Git retry committed membership as 5197bf5. No remote operation.

Full suite: 744 passed, then added independent complex reference-entangled search
check: 51 search tests passed. Search state phases, duplicates, branch-conditioned
success, zero scratch, changed-input cleanup and impossible measured cleanup are
covered. Release/artifact migration and Linux distribution checks remain T019.

### 2026-11-04 — KB-018 release integration and audit underway

Updated package/language to 0.3 and artifact contract to 3. Old generated 0.2
imports now fail with a rebuild instruction. Added CLI floating-point failure
configuration, search reports, examples, acceptance cases and documentation.
Added phase-bearing generated-module comparisons/respecialization, CLI SVG and
console checks, and backend-free compilation. A release patch initially failed
because it deleted/recreated one file in one patch; reapplied as an update.

Audit fixes: snapshot a quantum left membership operand before RHS global updates;
fold Boolean constants in expanded predicates; measure the visible part of a
search owner directly without allocating a correlated observation copy. Partial
measurement never creates a full-owner cleanup checkpoint. Configuration rejects
very large invalid integer failure bounds with ValueError instead of OverflowError.
Added complex reference-entangled membership, quantum wildcard, predicate-protection,
no-match quantum branch, budget, helper-control and oracle local arithmetic tests.

Windows/Linux initial release suites: 770 passed each (run-pwmfr49e and
run-ale006ao). Both installed wheels passed isolated CLI and generated search
respecialization. Core-only compilation succeeded with PATH empty, no Java/Qiskit,
and execution correctly gave Q5001. Pinned parser regeneration --check passed.
Final suites are rerunning after the configuration validation edge-case fix.

Environment failures and recovery: WSL required normal approval review; retry
succeeded. Windows pip uninstall failed when default temporary directories were
used, temporarily leaving qutes absent and two ~utes backup directories. Reinstalled
using workspace-local TEMP/TMP, verified isolated imports/smokes, then removed only
the two resolved project-environment backup directories. pip check passes.
No source data or user experiment was deleted or altered. Test-session handles
expired across a continuation; completion was recovered from final environment
and JUnit artifacts rather than restarting completed jobs.

Final audit added classical membership comparison preflight and per-character
quantum expansion charging, covering input-bound patterns that could otherwise
bypass the work limit. Focused membership/search suite: 89 passed, run-g84xvyk4.
The preceding final suites passed 774 each (Windows run-afj8jxfs, Linux
run-n9y5rkto); final suites rerun for the budget guard. Example runs produced only
matching outputs at seed 17: strings AB/BB, numbers 1/3 (64 shots each). Another
parser check accidentally used default temporary storage and failed to write;
workspace TEMP/TMP retry passed reproducible generation without source changes.

KB-018 final validation: 775 tests passed on each platform (V018). Final wheel
installed and verified on Windows/Linux; core-only install verified again with
empty PATH. All 33 compiler modules match the wheel. Requirements audited in
docs/release-audit.md. T017-T019 DONE; preparing third coherent local checkpoint.
User snapshots.qut and untracked grammar/.antlr remain excluded.

Source archive rebuilt and inspected successfully. Third checkpoint contains
release integration, compatibility, audit fixes, examples and full validation
evidence. No required work remains; future work starts from a new user request.

### 2026-11-04/05 - KB-019 language operation tour


Resumed KB-018 and inspected grammar, vocabulary, active specs and acceptance
cases. User requested examples for every supported operation within 24 qubits,
then explicitly authorized committing their config.py (4-bit/ABC defaults),
.gitignore and snapshots.qut edits. Preserved these three edited files as supplied.

Added 38 independent examples in examples/language, explicit adjacent config,
all-classical input JSON, coverage/output catalog, and README with per-example
qubit counts and expected outputs. Coverage includes scalar types, arithmetic,
logic/comparisons, arrays/text, scripts/globals/functions, all control-flow forms,
superposition, measurement/feedforward, rotations, cleanup, generic membership,
quantum wildcard patterns and search over scalar/text/quantum collections.
Examples compile to 0-21 qubits; all 38 executed successfully at 64 shots, seed 17
(39 tests including catalog completeness, run-iwrb6snr). Guide links were checked;
corrected an initial relative-link depth error before publication.

Full regression run-pr215uh3: 812 passed, 2 failed. Both tests implicitly assumed
old defaults (-128 requires 8 bits; CD requires D in the alphabet). Made those two
semantic tests request their intended width/alphabet explicitly, preserving the
new user defaults. No compiler behavior was changed by the example work. Updated
current default descriptions in the guide/roadmap. Final regressions pending.

Follow-up run-01c8sgfw: 813 passed, 1 failed. Example 22 had changed on disk to
assign "A?" while its catalog still expected "AB". Preserved the source edit and
updated the catalog/guide; direct execution confirmed ["A?", "B"]. The stricter
JSON comparison also distinguishes bool from int outputs. An initial ad hoc probe
used a nonexistent top-level import; reran with qutes.compiler/qutes.config.
Final Windows run-dn9pqzbu: 814 passed (63.61s). Verified all 38 documented qubit
counts against compilation (maximum 21), all tour guide links, and documented CLI
input execution/search explanation with automatic adjacent-config discovery.

Final Linux run-372bgprl: 814 passed (85.09s). Completed T020 and current handoff;
all example docs/tests plus the three authorized user files form one local commit.
A Windows-default-encoding documentation update failed; recovered the untouched
ledger history from HEAD, retained the new entry, and used explicit UTF-8 thereafter.
No push, compiler feature change, package rebuild, hardware run or human review.

## KB-020 - 2026-11-05 reporting and CLI guidance

Resumed clean d9fdd05, read active contracts/knowledge base, and implemented the
first approved readability checkpoint. Added exact-integer binary storage units,
nonfatal QW0001 in CLI/API metadata, and a targeted quantum-wildcard diagnostic.
No alphabet mutation or state preparation. Added seven-mode command walkthrough;
archived the full old roadmap, extracted core value contracts, and updated active
references. No grammar or execution changes. Initial exploration PowerShell brace
expansion and cp1252 Qiskit drawing probes failed; retried with explicit paths and
UTF-8. Focused suite: 92 passed. Next T022 retains source provenance through inlining
and lowering, then T023 will consume that information for diagram-only folding.

## KB-021 - 2026-11-05 source provenance and register names

T022 implemented: backend-neutral operation regions, source binding ranges,
function/foreach aliases and return moves, deterministic named registers including
search value/index/work partitions and measurement snapshots. Direct/generated
circuits preserve flattened wire order. Existing runtime already strips Qiskit's
inter-register count spaces. Added cleanup annotation data identifying zeroed and
restored wires. Explain lists selectors, bindings and cleanup ranges.

First focused run: 109 passed/2 failed (run-dk8f5iof): a test decoded raw multi-register
counts without removing spaces, and a construction test counted presentation-only
bind annotations as computation. Updated those assertions without changing results.
Next run: 257 passed (run-k_x9s2k9); final provenance/construction/search delivery/
visualization run: 75 passed (run-k5klc840). Classical binding updates and array
permutation ranges are recorded, not simulated. Example 12 retains 19 wires and
51 gate applications. Next T023: consume regions in a separate drawing circuit;
fold only reversible segments and leave measurement/runtime conditions visible.

## KB-022 - 2026-11-05 hierarchical diagrams and final validation

Completed T023: separate drawing circuits with compact source blocks, numeric/all
unfolding and optional function/kind filters. Ancestor paths reveal selected blocks
while unrelated siblings stay folded. Measurement/runtime conditions remain visible.
Oracle source regions and bindings are imported for each forward/inverse search
invocation; inverse cleanup is recomputation. Cleanup markers distinguish zeroed
wires from touched/restored inputs. Exact event IDs fix coincident zero-length
cleanup ranges. Rendering options participate only in view/image identity.

Added incremental and conservative preflight limits for lazy backend decomposition;
no silently weakened views. Indexed name lookup and monotone suffix counters avoid
quadratic register-name scans for repeated locals. A 500-local compile probe passed.
New operator tests compare full phases (not equivalence up to global phase), selected
search views, quantum-collection correlations and zero scratch; dynamic view execution
preserves decoded results. Legacy artifact-v3 modules without new fields still run.

Intermediate attempts: a new diagram test had an extra closing parenthesis and
failed collection (run-47d1kmne); corrected, then 43 passed (run-y6oqm3yl). An ad hoc
adder-definition printing probe hit the Windows cp1252 console; later probes only
printed operation counts. Expanded adder/search views reach U/CX. Successive focused
runs: 40 passed (run-9e_6i0w5), 28 passed (run-w93xzb_w), 46 passed (run-1ib411za).
Full intermediate runs passed 852 and then 856 each platform; final audit added
zero-cost-event identity and wide-definition preflight tests: 858 each platform.

All 13 documented Qutes walkthrough commands and generated module execution pass.
Named compact example 15 and expanded example 24 images inspected and legible;
PNG/SVG, image variants and bounded exports tested. Docs links checked. Historical
roadmap links corrected after relocation; MANIFEST now includes example READMEs.
Audit: docs/readability-audit.md. Final wheel rebuilt/installed in project Windows
and Linux environments, smoke checks pass; dependencies unchanged. Knowledge base
and handoff updated. Third local checkpoint completes the plan; no push or hardware
run, no claim of independent human review. Physical reuse and text preparation
remain deferred by user choice. Next action: wait for a new user request.

## KB-023 - 2026-11-05 certified-zero lifetime foundation

Resumed 3063a7f and inspected KB/contracts/scheduler. Preserved untracked user image
12_quantum_ordering-1c59c0354694-64eeb63a.png. Prior planning literature and approved
choices consolidated in docs/wire-reuse-plan.md. Implemented transaction-end zero
certificates for cleanup, restored zero dependencies, overwrite and search workspace.
Added fixed-schedule lifetime epochs, deterministic lowest-free-wire allocation,
coverage/collision/handoff verifier, and quantum-only operation remapping. Logical
program/execution remains unchanged in this checkpoint; integration is next.

Initial run-pwtqj7sa: 131 passed/2 failed, because Measurement exposes qubits rather
than Gate.bits. Added explicit operation-kind dispatch; run-s58tv4om 133 passed.
Tests demonstrate example12 19->10 with 29 operations unchanged, zero-only dead
storage elision, live-zero retention, measured state retention, atomic certificates,
reconstruction and arbitrary complex amplitudes with an external reference.
No simulator, reset or measurement is introduced by the allocation pass.

## KB-024 - 2026-11-06 physical execution and artifact compatibility

Connected the allocator after complete lowering; retain Program.logical_program
for source identities and use remapped operations/registers for direct/generated
execution. Added strict Boolean wire_reuse configuration (default true), CLI
positive/negative flags, physical memory/limit accounting, interval/proof metadata
and artifact_v4. artifact_v3 remains supported without silently reinterpreting
cached circuits; changed inputs respecialize through the current compiler.
Basic physical/logical view selection and diagram handoff annotations were wired
during integration; final targeted view coverage/documentation remains checkpoint 3.

Focused run-8b_kgp7n: 108 passed. Initial run-_xut9u6p had 107/1 failure: a new
2-bit test used out-of-range literal +2; changed to -2. Full run-v9brsams had
850/31 failures: stale schema assertions and tests reading logical indices directly
from physical statevectors. Updated assertions to explicit mapping, preserving
independent expected amplitudes/search reflections; no execution algorithm changed.
run-w4b095x4: 147 passed. Full run-lnrddums: 880/1, old explain wording assertion;
updated for enabled reuse. No full cross-platform/package completion claim yet.

Next: exhaustive view/report checks, joint measured/unmeasured state checks, 24-qubit
reuse example, active specs/docs/counts, Windows/Linux/parser/installed validation.
Preserve the untracked root PNG and snapshots.qut. Current installed wheels still
precede wire reuse; use tools/qutes.py against checkout until rebuilding packages.

## KB-025 - 2026-11-06 wire reuse delivery validation

Completed physical/logical diagram/report guidance, exact logical/physical resource
distinctions, stable handoff labels and empty-marker protection. Added joint
classical/remaining-quantum branch checks and both-view operator/image/CLI tests.
New tour39 uses 6 physical wires for 39 logical and returns -3; all 39 examples
execute under 24 (largest physical width15). Updated active docs/spec/roadmap and
added wire-allocation contract and wire-reuse-audit requirement evidence.

Focused run-_b8350rt: 34 passed/1 invalid fixture (n=t created a forbidden cleanup
cycle). Kept Q3001 semantics and changed fixture to reversible n+=1; run-uf2n0x1_
87 passed. An ad hoc tour-count documentation script used Windows default decoding
and rejected a Unicode char fixture; no docs were written before failure. Retried
with explicit UTF-8, checked all table counts and local links successfully.

Full Windows run-zg8e_zot: 906 passed, 81.98s. Debian run-9oamdb49: 906 passed,
96.61s. Parser reproduction passed. All 17 walkthrough commands passed. Inspected
artifacts/wire-preview/12_quantum_ordering-6bc8b9eac72f-5b224130.png: physical
work wires, cleanup and reuse handoffs legible. Rendering adds no executable gates.

Built/installed final source wheel in project Windows/Linux environments. Initial
installed verifier assumed one contiguous n register for input2; first-use physical
allocation legitimately yields indexed n registers. Corrected verifier to accept
source-indexed names under the approved naming contract; both installed smoke runs
then passed, including reused execution and logical views. Core-only installation
compiles with empty PATH and no Qiskit, emits artifact4 and reports Q5001 for build.
Dependencies consistent on both platforms. The final audit follow-up below
supersedes these initial full-test/package results.

Final delivery audit is docs/wire-reuse-audit.md. Preserve snapshots.qut and root
untracked PNG. No remote/push or user-file deletion. Remaining future choices are
cleanup rescheduling, dirty ancilla and hardware-aware placement, outside this
increment. Next request can start from KB-025; no required wire-reuse task remains.

Final audit follow-up: allocation materialization needed its own early reference
bound because repeated wide no-op gates may emit no backend operations. Added
Q4001 preflight over live/operation/proof references and a regression. Converted
private workspace membership to a set to avoid quadratic wide-storage scans.
Focused run-clza2c6j:47 passed; final focused run-qv2or_fx:103 passed. A compile-only
20,000-bit single-entry search probe returned 40,001 logical/20,000 physical in
0.83s without simulation (initial ad hoc expectation incorrectly included an index
bit for N=1; corrected observation, no compiler change).

Final complete source: Windows run-917rvzk8 **907 passed**,78.79s; Debian
run-hh5g0qad **907 passed**,96.02s. Supersedes successful intermediate907 runs
4zwbd261/gt05by5g before the workspace lookup refactor. Final wheel SHA256
dea2099d260ae46c3a23cf5526d459cf4de9c0c960c75a5c46ac53bf39844af4 installed and
smoked in Windows/Linux/core environments; both installed verifiers pass. Source
archive and wheel bytes checked again after final documentation. All required
work complete; the third coherent local commit closes T024, with no push.

## KB-026 - 2026-11-20, 0.4 implementation in progress

Resumed KB025, inspected specs/source/git. Two untracked root example12 PNGs are
user files and untouched. Added approved0.4 contract. Initial multi-file doc
patches failed on invalid context and made no changes; retried individual files.
Regenerated ANTLR4.13.2 after grammar/AST additions. Implemented finite float and
complex values/conversion/input/JSON layout decoding, readonly bindings, indexed
foreach. Initial focused run-cdm52k2i:228 passed/3 failed because builtin copy
reserved an existing variable name. D085 permits that value-position name. Added
independent numeric/reference tests; run-x5g90cwn:242 passed. No array-reference,
mut, gate, preparation or quantum-index completion claim. Next: locations and
array identities; keep semantics in checker/construction, not grammar actions.

KB026 checkpoint completion: implemented Cell/ArrayObject/ArrayView constructor
locations, mut caller-visible updates, readonly capabilities, explicit copy,
reference rebinding/returns, ranges/slices and concrete borrow/predicate checks.
Lowering receives immutable operation snapshots, root reachability and backing
retention; dropped views do not clean shared storage. Added retained_array_qubits
and explain text. Search rejects mutable oracles and float/complex elements.

Focused25 new tests pass (run-o06wkjmm). First broad run-ljprnuy5:915 passed/17
failed, chiefly old copy/conditional-rebind expectations plus provenance and
predicate-reference handling. Migrated intent-preserving tests/examples03/17 to
copy and element writes; views no longer materialize incidental membership copies.
Fixed string-array snapshot shapes and source alias intervals. Focused412 pass
(run-ttr0vcz5), full932 pass (run-tdlfjb20). New nested-rebind/retention tests and
numeric overflow/resource guards then pass97 (run-6bpoiomx),126(run-bbmsj_9g).
Linux initial restricted WSL launch denied; authorized elevated WSL retry passes
25 (run-wuz3y0nx). Parser check passes. No full Linux/release claim yet.

Next: T026 live operations. Existing scheduler.update rejects H/RY; do not simply
remove that guard: dependency replay through basis changes can falsely certify
zero. Add explicit unitary effect barriers/atomic multi-owner records and tests.
Remaining: sparse prep/subtraction, quantum support/access, artifact5 and migration,
release docs/examples/package/full Windows+Linux. No user images/snapshot edited.

## KB-027 - 2026-11-20 live operations checkpoint

T025 committed locally as8e0a71f. Added statement-only hadamard/not/phaseFlip/phase/
swap, finite static angles, mutable locations, if-based coherent/feedforward
control and transitive search-oracle rejection of basis/phase effects. Native
swap expands through the existing backend/codegen SwapGate path. Source regions
carry readable operation labels. No public cx/cphase aliases.

Scheduler records multi-owner mutations atomically. Old version replay cannot
cross explicit unitary effects; closed private components can be reversed jointly
and receive zero certificates only after the full inverse. External dependencies
and measurements reject that fallback. Controlled NOT on a quantum root carries
the same barrier as its equivalent assignment to protect observable phase effects.

Independent full-state/operator tests cover Bell, signed phase inverses, QFT versus
DFT, teleportation for four phases and preservation of external entanglement in
Z/X bases, returned Bell arrays/slices, snapshot evolution, closed joint cleanup
and unsafe replay/phase kickback rejection. run-d6d7hq_6:16 pass; final focused
run-y3w8_ajz:177 pass including18 new operation tests plus cleanup/control/search/
wire execution. No reset/implicit measurement inserted. No full release claim.
Next T027: sparse preparation/normalization and signed subtraction; then bounded
quantum indexing, artifact migration, docs/examples and final distribution checks.

## KB-028 - 2026-11-20 explicit preparation and signed arithmetic

T026 committed82a6d50. Added sparse qubit/quint preparation with uniform, probability
and complex-amplitude forms, finite strict normalization and reversible prefix
rotations/leaf phases. Signed subtraction and negation use inverse modular adders
and two's complement; self-overlap rejects information loss. Full-state tests cover
complex/global phases, external correlations, inverse preparation, local cleanup,
generated changed inputs and exhaustive small signed widths.

Initial focused20 passed run-76wcfsmn. Full run-4jqgbudz:974 passed/2 failed: old
subtraction-rejection expectation and an overbroad new restriction on preparation
under measured control. Removed obsolete rejection, restored existing legal private
runtime-branch preparation, and tested helper/coherent restrictions. Final focused
220 passed run-7pkw7b34. No full Linux/release claim yet. Next T028: conservative
support analysis and coherent indexed copies, followed by T029 artifact migration,
examples/docs and full distribution validation. User PNGs/snapshots untouched.

## KB-029 - 2026-11-20 coherent collection access

T027 committedbfec197. Added independent finite/interval signed-support analysis,
propagated through sparse preparation, copies, arithmetic, rotations, aliases,
mutable calls, returned values and branch joins. Every possible index must fit;
nonzero tiny amplitudes remain included. Reads evaluate operands once left-to-right,
copy the selected basis value with controlled access and preserve source/index.
Text lengths/encodings and non-assignable result rules checked explicitly. Existing
array lifetimes/cleanup and wire reuse apply; no Grover or extra selection storage.

Focused run-9up2pjqz:138 passed/1 failed from an overly conservative support-work
charge. Charge actual bounded set work instead. New31 index tests: first run
86 passed/1 diagnostic expectation mismatch, corrected with an explicit lvalue
diagnostic. Full run-57jpnj3y:1006 passed/1 old R011 type-pass expectation; the
unsafe index still rejects in construction. Acceptance now records that pass.
Final focused220 pass run-kea5b2gr. Tests include full complex correlations, shared
storage, zero scratch/reuse, all supported collections, tiny weights, joins/calls,
generated parity and independent interval-overflow containment. Next T029 only:
artifact5/legacy guard, migration/examples, safety audit and final validation.

## KB-030 - 2026-11-20 integration in progress

T028 committedf29be9e. Added package/language0.4 and artifact5, preserved cached
schema3/4 execution with pre-recompilation changed-input rejection. Updated guide,
grammar summary, roadmap and contracts, added examples40-50 and a runnable26-command
walkthrough verifier. Installed-wheel verifier now checks new references/gates,
coherent reads and complex codec. Source snapshots/two user PNGs remain untouched.

Safety audit fixed transitive scalar-element updates falsely labeled array rebind,
global alias access during mutable borrows, and safe replacement of a readonly view
by a mutable binding. Forced preparation bits use exact X, avoiding unnecessary
pi rotations. Regressions cover each. One documentation patch had invalid context
and failed atomically; corrected without partial edits. Initial rendering tests
used wrong keyword names:69 passed/3 failed run-2fp3zkk2; corrected to existing API.
Tour/delivery focused58 passed run-zlikcp4t. Broad Windows1030 passed run-fg7587z9;
26 CLI commands passed and QFT PNG visually checked. Final readonly-view fix focused
100 passed run-rwggcob1. Linux full suite and final installation/package checks are
still pending at this entry. Next: collect results, finish packaging evidence,
update status/tasks and commit the coherent integration checkpoint; do not push.

KB030 completion: Windows final1031 passed run-j6foy26j; Debian final1031 passed
run-zjpl31z4 (supersedes1030 before final readonly-view regression, run-70bx56ej).
Installed wheel/CLI/generated/reuse/numeric checks pass both platforms. Initial
Windows pip reinstall used sandbox-default TEMP and partially removed the old
package; its verifier failed import. Retried with workspace TEMP/TMP, restored0.4,
verified installation, and removed only verified in-workspace stale ~utes backup
directories. pip check now clean. No external temp directories were deleted.

Final wheel SHA25652781a627f655ad6094f668bd102dee4c3a97d01ff55b203fe01cdeff4297d1c
matches all45 source Python files. Installed in Windows/Linux/core environments.
Core-only empty-PATH compile/codegen passes without Java/Qiskit. A tour-count probe
initially used platform-default decoding and failed on Unicode; rerun with explicit
UTF-8 succeeds:50 programs, max15 physical qubits; new examples0-12. The actual tour
tests always used UTF-8. Fixed the CI wheel filename, which still named0.2; hosted
CI was not run. Parser --check and all26 walkthrough commands pass. Source archive
and final documentation included in packaging audit. Git diff check passes.
A combined delete/add STATUS patch was rejected atomically as a duplicate target;
replaced it with one update. No source edits resulted from that failed attempt.

All requested0.4 checkpoints complete. Remaining proof conservatism/deferred features
are documented limits, not pending0.4 tasks. Final coherent integration commit includes
source/tests/examples/docs and this handoff. No push, no user PNG/snapshot changes.

Final diff audit found one unsupported form accepted silently: whole temporary-slice
assignment rebound a temporary Cell and discarded it. Added an explicit type-pass
rejection and regression; element writes and named-view rebinding remain valid.
Repeating full platform checks and refreshing wheels after this final guard. The
1031-test results above precede this additional test; final results follow below.

Final guard validated: Windows1032 passed83.44s run-f40mx194; Debian1032 passed
123.51s run-s0dkm8xk. Refreshed final wheel SHA256
39317efad83e27d30387e6ea8b1423dfef7225054bcaf92352823b78f9e64168;
all45 Python source bytes match. Reinstalled/reverified Windows/Linux/core packages;
core empty-PATH smoke passes. This supersedes the earlier wheel hash and1031 counts.
Source archive refreshed after final handoff edits. No implementation work remains.

KB031: imported e1c78a8 from qutes_lang_chatgpt over origin/development; retained LICENSE and CITATION.cff. Audited legacy notebook, extension, wiki and setup in docs/release-0.4.md. Ran 1032 tests and 26 walkthrough commands. Notebook execution initially hit Windows console encoding on circuit printing; UTF-8 rerun passed.

KB032: hosted build 44785282615 passed three matrix jobs. Windows 3.12 installed into runner Python and pip check detected an unrelated preinstalled pipx/packaging conflict. Run the unchanged pins in a fresh venv on each runner. Browser Chromium proved Bell edit, exported project and wire reuse; installed Aer reproduces the browser export (30 false/true, 34 true/false).

KB033: 0.4.0 assets staged as a GitHub prerelease. Companion starter uses the published canonical Bell source/config and wheels. Website candidate 466bfe4 pins a78cc16. Hosted website run 44786317981 failed because Playwright 1.56 cannot install on Ubuntu 26.04; pinned Ubuntu 24.04. Hosting preview uses the existing website GitHub Actions credential; local Firebase account lookup failed.

KB034: published the GitHub v0.4.0 release before promoting the website. Preview 44786813596 served the pinned compiler and reproduced the Bell edit. Verified public starter checksum, then deployed tag qutes-site-0.4.0 (466bfe4) in run 44787628431 and repeated the experiment on https://qutes-lang.web.app. No default-branch merge. Existing main hosting workflow still applies to future pushes there.

KB035: fetched e1c78a8 from the local rewrite checkout by object ID, joined histories using the ours merge strategy, and pushed qutes2.0. Moved release ID 453003397 and its three assets to tag 2.0 before deleting the old tag with an expected-object lease. The live website used hard-coded old URLs; site migration was raised separately.

KB036: user approved migrating the website release links and redeploying. Website commit 0af23e4 uses release tag 2.0 for the starter and build-time resource download. Added the new promotion tag qutes-site-2.0 in place of the previous deployment trigger. Verified both archives and an edited Bell experiment on preview and production. This resolves the stale-link finding in KB035.

KB037: renamed the website branch on GitHub using the branch rename API; verified local tracking and the original tip 0af23e4. Prepared new package metadata and public labels. Starter instructions now read the exact version from the input archive manifest.

KB037 completion: immutable release 2.0.0 created from 0367b52 with three validated downloads. The website build pins the archive and all its public package labels and install instructions use 2.0.0. GitHub accepted the atomic push of website branch qutes2.0 and tag qutes-site-2.0.0 at b480812. Hosted website outcome unverified by request.

KB038: implemented and locally committed the redesign in the website checkout. GPT-6.2 Sol at medium effort reviewed desktop/mobile and keyboard flows. Fixed misleading Hadamard feedback, duplicate counts, step focus and small-screen spacing. Browser tests initially raced hash navigation and tried editing collapsed inputs; synchronized transitions and opened the inputs panel. Review is by an agent. No push or deployment.

KB039: local website commit 81bd84c adds a primer, worked derivations and traces, eight editable labs, and a teleportation repair and audit. The learner’s observations, drafts, progress and written report persist in the browser. During the requested Sol review, a faulty protocol could earn completion after a successful compile and a quiz answer. Replaced that gate with observed outcomes, compiler diagnostics, resource counts and angle-specific runs, including the injected fault and restored pass. The agent reproduced the repaired gates on desktop and phone and flagged the primer layout. Corrected that layout and replaced the obsolete four-step walkthrough test. The owner has reserved publication for a later instruction.

KB040: added a checksum-pinned wheel build, native archive packaging, separate clean-runner acceptance and release backfill workflow on a dedicated branch. Existing remote release assets and tag were verified. Hosted acceptance and distribution pending.

KB040 Windows candidate: the fresh runner reached image export after Bell, phase, wire reuse and code generation passed. Its pathname comparison used textual equality across Windows TEMP aliases. Check directory identity and image bytes separately.

KB040 completion: release workflow 44809167547 completed successfully from d314f6e. Windows x64 passed first, then the two macOS 15 and two Ubuntu 22.04 targets built and passed fresh-runner checks. The publisher verified all assets after download and added release instructions. Anonymous HTTPS requests confirmed working links. No website operation was performed.

KB041: website commit 4dcc8c1 replaces the Python-first Build page with five platform downloads, extraction steps, shell commands, observed Bell output and a one-line edit. Optional Python, teaching and playground handoff paths remain accessible. Running the CLI exposed its example configuration warning, now explained below the commands. Local preview only.

KB042: the compiler already defaults to ABC; the example settings overrode it with AB?. Corrected the shared configuration, scoped the opt-in to two tour entries, and prepared revisioned archives built from the original published compiler wheel.

KB042 completion: GitHub run 44813512817 attached seven r2 archives and their checksum file under new names, verified their public bytes and updated the release description. All pre-existing asset IDs and hashes were preserved.

KB043: the local website commit 8daa5d9 moves the primer into measurement and phase labs, removes output and edit sections from Build, updates the links and pins the published r2 teaching bundle. The local compilation of that ZIP had different archive bytes than the hosted version; all extracted files were identical. The preview uses the published checksum.

KB044: migrated native packaging to the exact compiler Git commit. Removed the obsolete distribution builders and updated the notebook and source documentation. The separately maintained local website now builds a browser runtime directly from checksum-pinned language source and parser code. The live site still links to retired files. The owner chose to keep it local.

KB044 publication: replaced the r2 checksum manifest at its original URL and edited the GitHub release notes. Removed eleven explicitly identified obsolete assets. Rechecked the final six-asset inventory, public checksum bytes and the GitHub IDs and digests of the five retained archives. Website remained local.

KB044 completion: compiler and portable checks passed on the language branch, including all five fresh archive verifications. Production still uses the earlier site, pending the owner's review.

KB045: pushed website qutes2.0 from b480812 to 0d0d46d. Dispatched hosting workflow 44818550125 on that exact revision using the live channel. Verified branch ancestry, open pull requests and active checkouts, then removed the merged portable-cli-2.0 and portable-cli-2.0-r2 Codex branches on GitHub. Removed the four merged local language working branches and both repositories’ stale Codex remote-tracking refs. The website’s working branch was already absent from GitHub.

KB045 completion: GitHub verified the reviewed site and deployed the same artifact through Firebase preview to live. Compared the production Build HTML with the website checkout. All five public r2 archive URLs returned 200 and the five checksum entries matched the release API. The old teaching ZIP and former compiler wheel path on the website both returned 404.

KB046: extracted the existing circuit emitter for reuse and added a separate generator for a standalone circuit, specialized return decoder and Aer runner. CLI output retains its original format and behavior. Set up an isolated Python environment by installing only qiskit==2.3.0 and qiskit-aer==0.17.2 as direct dependencies.

KB046 regression: a valid return expression unrolled over 205 or more negations exceeded Python’s parsing limit when emitted as nested parentheses. Emit intermediate values in evaluation order for compound return expressions.

KB046 local delivery: the website pins compiler 5ee169d and displays and downloads the identical standalone script. Verified the source pin against the complete Git archive contents, independent of ZIP compression. The published and local Git archives of previously public commit 7070205 matched under that digest. An initial tamper-test fixture reused mutable ZipInfo entries; copying those entries verified a one-file change changes the digest. Website c55aa4c and compiler changes are local. No push, release or hosting action.

KB047: published the standalone generator and guide to the compiler branch at 62371da. Fetched the public GitHub archive for compiler revision 5ee169d and matched its commit and content checksum to the website lock. Then pushed website commit c55aa4c to qutes2.0 and dispatched production hosting run 44824624905.

KB047 deployment: production run 44824624905 passed its browser checks, preview manifest check and Firebase production promotion. The parallel branch preview run 44824605772 initially saw an unexpected manifest immediately after deployment. Once the preview and production returned the pinned compiler revision, the failed preview job passed on its second attempt. Downloads from the production UI passed the clean-interpreter test.

KB048: live HTML, worker, engine, compiler ZIP and WebAssembly all returned max-age=3600. Warmed persistent Chromium profiles on production and preview before deployment. In the Windows Firebase emulator, the initial catch-all glob did not match clean URLs. A catch-all regex passed the real two-revision navigation test. Published website d69bb7f and dispatched workflow 44827178923.

KB048 correction: on the first Firebase preview, public, no-cache returned HTTP 200 for repeated conditional GETs with an unchanged ETag, including the large WebAssembly file. The preview guard caught this before production. Cancelled the superseded live run. The local Firebase CLI could run its emulator, but its remote credentials returned 401, so all preview and live publication uses the repository’s existing hosting workflow. Switched to max-age=0, must-revalidate for browsers and s-maxage=60 for shared caches. The two-revision browser test passed again at f027525.

KB048 production: website qutes2.0 at f027525 passed preview run 44828151606 and live run 44828171128. Both public hosts returned the new browser policy and a bodyless 304 for unchanged WebAssembly. Both returning profiles ran Bell and downloaded its standalone export. A normal first visit still used previously fresh content. A hard refresh updated the page and editor, but old worker-loaded files remained fresh under the previous one-hour rule. Clearing only the disposable profile's HTTP cache immediately updated all four assets and preserved its saved storage marker.

KB049: inspected the 2026–27 UniCT syllabus and last year’s archive. Authored 17 chapters, six guided paths and three optional extensions around 16 original programs. The first BB84 draft attempted conditional measurement (Q2004); the tested version conditionally couples a Z probe and measures it unconditionally. Local browser-engine acceptance passed all 72 teaching variants.

KB049 local delivery: both study formats render from the verified language archive. Walked all 20 topic routes, checked all disclosures, returned from course experiments, restored drafts and progress, and inspected desktop and phone layouts. The full playground now preserves workbook edits in both directions. Chromium exercised 72 variants, and the isolated Aer interpreter ran actual downloads for all 16 experiments including an edited Grover program. Firefox and WebKit each verified both Grover routes. Clarified readout and Fourier notation after proofing. Local previews only.

KB050: removed the companion from the local build, updated Tutorial navigation and verified the workbook at website c98452f.

KB051: renamed the local workbook to tutorial.html, removed university attribution, syllabus links and topic picker, and preserved the earlier exercises at practice-labs.html.

Renamed the shared teaching directory and updated the resource index and CLI example.

KB054. Protected both qutes2.0 branches with required checks and administrator enforcement. Prepared component pins and a release verification gate bound to the compiler revision and all five build inventories.

KB055 (2026-11-21). Released compiler 1c560fd as 2.0.1 after language PR 100 and the native verification matrix. Website PR 4 retired the default-branch publisher. Website PR 5 fixed both stale navigation expectations, pinned the exact compiler and asset names, and promoted the same tested artifact through an isolated preview project and production. Google required a fresh Firebase sign-in. The initial IAM write encountered account propagation and succeeded on retry. Disabled the old Google key and removed its repository secret after independent production verification. Re-read IAM to confirm the disable had propagated. All user-facing release steps completed.

KB056. Reused the released CLI semantic analysis and browser compiler. Generated syntax vocabularies, built the five target-specific candidates, and added phase-sensitive circuit report and scope tests. Clean VS Code installation exposed a Windows native import failure at a deeply nested runtime path. Shortened the extraction path and retained verification of the full SHA-256. The packaging-tool minimatch advisory was resolved using the patched development dependency.

KB057. Clean-profile Windows VS Code now runs Bell offline after shortening the installation path. Fixed the missing playground circuit-starter link, immediate Enter acceptance of a visible completion, and selection of repeated loop gates. Added direct controlled-NOT construction using ordinary Qutes if syntax, and named the limitations of the first optimization report.

KB058. Exercised both desktop editors using the actual installed extension and a clean profile. On Linux with an intentionally empty editor PATH, GNU tar needs its system gzip for bootstrap. Scoped the system search path to extraction. The Debian desktop test passed after the correction. Verified the two actual tokenizers against all 50 tour examples. Website f9bd96c preserves public browser paths and adds the circuit builder and report. The full browser suite passed after fixing the missing sketch link, point-style JSON diagnostics and the loop selection event. Local branches and artifacts only.

KB059. Website 2569cad adds an explicit source mark while keyboard focus stays on a circuit gate. The browser assertion checks the visible marked text as well as the document selection. Fast-forwarded the local review branch in the regular website repository to the tested preview checkout.

KB060. The owner authorized native GitHub verification on a temporary language-only branch. Pushed a2af516 to codex/verify-editor-native. All five desktop extension installations passed run 44951396964 and the parallel compiler matrix passed run 44951396920. Website branch 2569cad and Marketplace publication remain for local review.

KB061. Installed the verified Windows x64 VSIX in the owner's regular VS Code and opened the canonical Bell example. Reproduced the browser's pale diagnostic on a pale background in dark mode. Website review commit e148d06 gives popups the active theme's text and surface colors and makes the diagnostic code easier to read. Both local website review branches include the fix.

KB062. The editor toolbar ran Qutes, but the Run and Debug sidebar offered to search the Marketplace. Registered a Qutes run session that calls the same simulator and supports Stop. The Windows extension update needed a window reload before the existing Bell window picked it up. After reloading, clicking the sidebar button produced both matching Bell outcomes in the Debug Console.

KB063. Added line breakpoints, Step In/Over/Out, Continue, call frames and joint-state inspection. The worker bundles the compiler, parser and the same pinned Pyodide version used by the browser editor. Initial offline npm installation missed its local cache; installed the pinned dependency normally. Corrected the first tour probe to read UTF-8 and use each example's inputs and configuration. Synthesized search internals step with their enclosing expression. Installed the Windows package and left the regular VS Code window paused at Bell line 7 with the initial state visible.

KB064. Captured source bindings at debugger stops and mapped them to physical wires and already available classical values. Bell now labels the rightmost digit Alice and the leftmost digit Bob. Verified a helper with renamed parameters, reused wires, and scope exit. Installed 2.0.4 in the regular Windows VS Code profile and paused at line 3 with both variable groups expanded. The local editor shows two equally likely states after the Hadamard.

KB065. Reused the simulator's computational-basis measurement weights to show P(0) and P(1) beside each allocated single qubit. Calculation uses the full joint state, shares results across aliases and leaves the shot untouched. In the regular VS Code window the step icons were on the floating toolbar, with Step Out dimmed at script level. Clicked Step Into and Step Over in the updated session and left both probability views expanded at Bell line 3.

KB066. Shared the compiler's typed snapshot layout with the debugger to decode measurement probabilities at source stops. Added expandable, paged outcomes for numeric and text registers and arrays, retaining source-frame aliases and physical wire order. The owner's Bell experiment now observes the integer increment and array in the current working copy. For installed tests, staged the committed Bell fixture separately to preserve the owner's ongoing edits. A separate review window for the weighted preparation example opened in Restricted Mode. Trusted isolated VS Code hosts exercised the debugger.

KB067. Froze language commit ea40fdfeceb1d039eaca886eac05324a7dbfb0a8 for extension 2.0.6 RC1 on codex/verify-editor-2.0.6-rc1. Run 45009272870 installed the correct VSIX on all five native targets and each log recorded two successful VS Code test hosts. Compiler run 45009272871 also passed on the same commit. The verification branch was the only remote update made for this batch. Website work and public distribution await the owner.

KB068. Updated the local website source pin from efd784f to the frozen ea40fdf and saved the tested build configuration as website commit 8265174. Compared the GitHub source archive with a local Git archive and checked all 49 Python compiler modules in the served bundle. Verified the Bell diagnostic and recovery, constructing Bell with the graphical editor, and previewing the cancellation of adjacent Hadamards. The full local suite and independent Qiskit exports passed (V067). The regular website checkout now has the same local review branch revision and remains on dev. The local preview is available for owner review.

KB069. Published the reviewed website after the owner authorized production. PR #14 passed the required full suite and merged as 8b2f29d. GitHub auto-merge was disabled, so the normal protected merge ran after verification. The merged file tree matched the reviewed 8265174 exactly. The production workflow deployed to qutes-lang.web.app and verified the changed compiler, cache behavior, Grover tutorial and download links. A separate Chromium session against the live site checked editor feedback, constructing Bell, previewing a cancelling pair of Hadamards, and running exported Python independently. Marketplace publication stays pending.
