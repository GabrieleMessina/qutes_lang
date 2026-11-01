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
