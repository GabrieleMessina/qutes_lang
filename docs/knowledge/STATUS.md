# Current status

Updated: 2026-11-01, checkpoint KB-013. Qutes 0.2 implementation is ACTIVE.
User approved scripts-only execution, ANTLR, globals, input declarations, inferred
measurement effects, and improved diagnostics. No additional design approval needed.

Checkpoint 1 implemented: generated ANTLR 4.13.2 lexer/parser, AST adapter,
structured diagnostic collections, excerpts/hints, reproducible generation.
Validation: 60 parser tests pass; full Windows suite 599 passed, one pre-existing
user-example expectation mismatch (snapshots.qut deliberately changed). See V013.

Next action: implement script/global/input semantics and transitive effects, then
migrate examples/tests/docs and version generated artifacts. Preserve the user's
snapshots.qut edit (numberb and number + numberb); do not stage this file.

## Previous delivery baseline

Updated: 2026-11-01, checkpoint KB-012. V1 implementation and delivery are complete
within the research-tool boundary of DEVELOPMENT_PLAN.md. No user design decision
is currently blocking the implementation. See [release audit](../release-audit.md)
for requirement coverage and the distinction between automated evidence and review.

## Delivered

- Compact C#-inspired syntax, strong typing, source locations, stable diagnostics.
- qubit, signed fixed-width quint, configured quchar/qustring, one-dimensional
  arrays, user functions, readonly borrows, owned return values, ordinary assignment.
- Addition, wraparound, rotations, signed/Boolean comparisons, coherent if/else,
  construction-time for/while/foreach, bounded construction and function inlining.
- Version-aware automatic uncomputation with full-state tests, dependency
  restoration, safe overwrite, scoped/anonymous cleanup, deliberate cycle errors.
- Non-consuming measurement, immutable snapshots, post-measurement updates,
  measurement checkpoints, mixed coherent/classical conditions, same-circuit feedforward.
- Public check/build/run/explain commands and JSON output. Intermediate parse,
  analyze, and construct commands remain explicitly partial views.
- Circuit diagrams on full commands: --print-circuit, --save-circuit FOLDER,
  --circuit-format png|svg. Includes cleanup/measurement before backend-specific
  decomposition; preserves JSON stdout. Optional image dependencies are pinned
  and installed in the project-local environments. See the guide.
- Source API, deterministic readable Qiskit Python artifacts, build(inputs) and
  run(inputs,shots,seed), actual respecialization for new inputs, ordered decoding,
  source/build identity, config/version metadata, resource/cleanup reports.
- Bounded local Aer execution, optional backend dependency, atomic output files,
  large-integer serialization, runnable examples, user guide, source/wheel packaging.
- Windows/Linux Python 3.12/3.13 CI matrix checked in; no hosted run or remote push.

## Verified evidence

- KB-012: **596 passed** on Windows; **28 rendering/CLI tests passed** on Linux.
  PNG/SVG export and installed entrypoints were verified on both platforms.
  Measured/coherent PNG diagrams were visually checked. See V012 for exact
  commands and the resolved temporary example edit during validation.

- **577 passed on isolated Windows Python 3.13.5**, no warnings, 29.83 seconds:
  `artifacts/checks/run-o9kdw90c`.
- **577 passed on isolated Debian/WSL Python 3.13.5**, no warnings, 36.90 seconds:
  `artifacts/checks/run-w6545yxc`.
- All 17 positive acceptance examples execute from generated Python and have
  exact projected-branch distributions. All 16 negative cases keep their expected
  diagnostic. Seven tutorial examples execute with expected output support.
- Installed-wheel checks use isolated Python imports, verify package paths outside
  checkout sources, CLI execution, and new-input generated-module behavior.
  Evidence: `artifacts/installation/{windows,linux}.json`; dependency checks pass.
- A separate core-only environment checks/generates without Qiskit/Aer and reports
  Q5001 for requested simulation. Wheel/source artifacts are ignored under `dist/`.

Pinned backend: Qiskit 2.3.0, Aer 0.17.2, NumPy 2.1.3. `requirements-dev.lock`
adds reproducibility pins; psutil 7.0.0 replaces the host's non-installable 5.9.0
pin. No global package was modified. Python 3.12 is configured in CI, not locally
tested. Hosted CI requires a future user-authorized remote/publication step.

## Commands in this workspace

```powershell
& .\.venv\Scripts\qutes.exe run examples/snapshots.qut --shots 32 --seed 7
& .\.venv\Scripts\qutes.exe explain examples/coherent_if.qut
& .\.venv\Scripts\python.exe tools/check.py -q
& .\.venv\Scripts\python.exe -I tools/verify_install.py
```

The fallback existing interpreter is `C:\ProgramData\anaconda3\python.exe`;
PATH python/py aliases were unusable. Its external IBM-runtime plugin adds
deprecation warnings, absent in the clean environment. The Windows runner uses
Python stream capture to avoid native Aer handle failures under descriptor capture.

Linux environment: `artifacts/linux-venv/bin/python` under Debian WSL, with the
workspace at `/mnt/c/Users/gabry/Work/Quantum/qutes_lang_chatgpt`. WSL execution and
Git writes need normal elevated tool review in this host. Git commits are already
user-authorized; no remote exists and no push was requested. Package installs used
project-local TEMP/TMP because the host's default temporary directory was unwritable.

## Limits and next work

No V1 implementation task remains. Start future work from a new concrete user
request, not by silently expanding the approved language boundary. The later
roadmap includes hybrid multi-stage orchestration, measured loops, higher-level
algorithms, hardware backends, and editor support.

- Released wires remain reserved for historical recomputation. Resource reports
  include them; a safe last-use allocator is a future optimization.
- Some valid dependency cycles receive conservative Q3001. Indirect measurement
  does not prove a root erasable without a direct checkpoint. No hidden reset or
  observation is permitted as a workaround.
- Conditional measurement, runtime arithmetic/indices/loops, dynamic quantum
  sizes/text lengths, general state preparation and mutation parameters are deferred.
- Named main quantum outputs may remain live until shot end; scoped/anonymous
  temporaries must clean or fail. Measurement never consumes a named value.
- Builtin names remain the documented defaults; no separate human naming or
  correctness review has been claimed. This is a local research implementation,
  not a published package, hardware validation, or formal proof of all programs.

Before resuming, read AGENTS.md and the knowledge base, inspect Git status/log,
and check whether any uncommitted work postdates this checkpoint. Maintain the
ledger and commit coherent tested units; never reintroduce the withdrawn
function-only evolution rule or use-after-measurement errors.
