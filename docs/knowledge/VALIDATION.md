# Validation evidence

Record commands, results, environment, and what each check does NOT establish.

## V001 — 2026-10-30 — Environment and documentation bootstrap

- `git --version`: 2.50.1.windows.1.
- `& C:\ProgramData\anaconda3\python.exe --version`: Python 3.13.5.
- Import/version inspection succeeded for Qiskit 2.3.0, Aer 0.17.2, NumPy 2.1.3,
  and pytest 8.3.4. This establishes imports only, not circuit compatibility.
- PATH aliases `python`/`py` failed; use the explicit interpreter above.
- No implementation tests exist yet. Documentation bootstrap is not a compiler
  milestone or a quantum correctness result.

## V002 — 2026-10-30 — M1 executable foundation

Command: `& C:\ProgramData\anaconda3\python.exe tools/check.py -q`.
Result: **37 passed**, 63 external IBM-runtime deprecation warnings, 5.35 seconds.
Artifacts: `artifacts/checks/run-49cp5tqo/results.xml` and `environment.json` (ignored).

Coverage: exhaustive small-width signed addition/rotation codecs, text/alphabet
boundaries, configuration precedence, full operator comparison for constant
addition, random complex states entangled with reference qubits for register
addition/rotation, correlated copies, scratch cleanup including a deliberately
incorrect inverse omission, non-consuming repeated measurement, retained snapshots,
signed wraparound after measurement, and classical feedforward. State comparisons
use 1e-10 tolerances; supported sampling outcomes use fixed seeds. This is not a
statistical validation of all sampling probabilities.

The 33-case source manifest has structural/configuration checks, NOT compiler
semantic execution. Oracle/probe tests do not prove general cleanup synthesis.
Fresh dependency installation and Linux remain unverified. Initial raw pytest run
failed one temporary-directory fixture; the runner fixes that environment issue.

## V003 — 2026-10-30 — Parser and complete current suite

Command: `& C:\ProgramData\anaconda3\python.exe tools/check.py -q`.
Result: **102 passed**, 63 external IBM-runtime deprecation warnings, 5.60 seconds.
Artifacts: `artifacts/checks/run-kaa1s_hp/results.xml` and `environment.json` (ignored).

Includes all V002 checks plus all 33 corpus syntax cases, operator precedence and
associativity, function/array/control-flow shapes, Unicode escapes, comments,
invalid literals, source locations, EOF/truncated source, deep expressions/blocks,
flat deep ASTs, CLI JSON/text output, missing/invalid-UTF8 files, and the checkout
entrypoint. The frontend subset previously passed 82 tests with backend excluded.

Bounds: parser validation does not check names, types, return paths, staging,
effects, or cleanup. The acceptance manifest has 17 intended valid programs, 2
lex/parse failures, and 14 intended semantic failures. Those semantics have not
been executed. No hardware, clean-install, or cross-platform verification yet.

## V004 — 2026-10-30 — Typed frontend

Command: `& C:\ProgramData\anaconda3\python.exe tools/check.py -q`.
Result: **173 passed**, 63 external IBM-runtime deprecation warnings, 7.02 seconds.
Artifacts: `artifacts/checks/run-6fjunpjd/results.xml` and `environment.json`.

New evidence covers the 33-case corpus through the frontend (cleanup deliberately
excluded), lexical scope/readonly effects, invalid entry/returns, call recursion,
coherent predicate dependencies, stage changes inside loops, runtime helper
specialization, branch shape merges, integer conversions, short-circuiting,
classical division conventions, deterministic IR, and analysis CLI/config handling.
This does NOT establish source execution, circuit construction, or automatic cleanup.

## V005 — 2026-10-30 — Bounded symbolic construction

Command: `& C:\ProgramData\anaconda3\python.exe tools/check.py -q`.
Result: **216 passed**, 63 external IBM-runtime deprecation warnings, 6.39 seconds.
Artifacts: `artifacts/checks/run-ugle3txd/results.xml` and `environment.json`.

New coverage: all 17 positive examples construct, pure classical functions/loops
execute, calls/loops disappear from executable construction bodies, early returns,
readonly borrow aliases, fresh local identities, helper ownership moves, classical
array copying, retained measurement snapshots, input shape/range errors, global
loop/step/memory budgets, dynamic shape joins, indexed helper evaluation once,
quantum foreach materialization once, and construction CLI JSON inputs.

Limits: symbolic construction does not prove physical correctness of storage
reuse, automatic uncomputation, branch cleanup, or measurement boundaries. No
source-generated Qiskit circuit executes yet. Existing manually constructed
backend probes remain the only circuit-level evidence.

## V006 — 2026-10-30 — Cleanup schedules and reversible gate emission

Command: `& C:\ProgramData\anaconda3\python.exe tools/check.py -q`.
Result: **267 passed**, 63 existing external warnings, 7.23 seconds.
Artifacts: `artifacts/checks/run-6f8zch2u/results.xml` and `environment.json`.
Targeted command adding `tests/test_cleanup.py tests/test_gates.py`: 51 passed.

New evidence covers automatic cleanup schedules executed as Qiskit circuits,
checked against independent complete complex-state expectations. Includes changed
source versions, multiple inputs, released intermediate reconstruction, reversible
overwrite, preserved reference entanglement, zeroed scratch, forbidden cyclic
cleanup, root escape rejection, rollback, and budget/depth diagnostics. Arithmetic
has exhaustive small-width full operators and entangled controlled-operation tests.

This advances beyond manual probes, but does NOT establish source compilation,
measurement-safe cleanup, whole-program acceptance, hardware execution, clean
installation, or cross-platform compatibility. Those remain separate tasks.

## V007 — 2026-10-30 — Scalar source lowering and explicit measurement cleanup

Command: `& C:\ProgramData\anaconda3\python.exe tools/check.py -q`.
Result: **312 passed**, 65 external IBM runtime warnings, 7.63 seconds.
Artifacts: `artifacts/checks/run-ogcuhmp_/results.xml` and `environment.json`.
Targeted source/measurement run with `--capture=sys`: 45 passed in 4.97 seconds.

New evidence: source cases A001-A006/A010-A012 match exact ideal distributions;
all 16 negative examples produce the intended category. Compiler-generated
coherent circuits match full complex-state expectations for changed inputs,
nested arithmetic, and cleaned scratch. Helpers transfer owned results without
hidden root escapes. Expanded loops retain distinct snapshots and clean locals.

Measurement checks enumerate projected branches and compare full conditional
states/probabilities, including entangled references. They cover stable snapshots,
post-measurement updates, reconstruction of older dependencies, measured-root
overwrite/cleanup, indirect-observation rejection, and repeated observations.
Aer executes a source snapshot example and a dynamic checkpoint circuit; density
matrix output confirms the released measured register is zero.

Failed artifacts: run-oxwgjt3f and run-xz6bk5jo (Aer DLL collection failure under
Windows descriptor capture); run-e_oe6q1q (three corrected test-fixture issues).
The runner now uses Python stream capture on Windows. Clean installation and
Linux remain unverified. Dynamic source branches, quantum collections, and the
full CLI still await implementation; this is not full-language release evidence.

## V008 — 2026-10-31 — Coherent source control flow

Command: `& C:\ProgramData\anaconda3\python.exe tools/check.py -q`.
Result: **377 passed**, 65 external warnings, 9.16 seconds.
Artifacts: `artifacts/checks/run-j2oaqi3_/results.xml` and `environment.json`.
Targeted initial source/control integration: 101 passed in 6.63 seconds.

New evidence includes all six signed comparisons at widths 1-3 on arbitrary
complex amplitudes entangled with a reference, preserving inputs and zeroing
comparison scratch. Signed constants, literal-left/identical operands, Boolean
operations, and compound predicates have independent expected semantics.

Full-state source tests cover nested branches, conditional overwrite of known and
derived values, branch-local cleanup after predicate inputs change, functions and
loops inside controls, contradictory controls, and rejected unknown-root overwrite.
A008/A009 now match the exact acceptance distributions. A007/A013-A017 remain
pending. No hardware, clean-install, cross-platform, or full release claim.

## V009 — 2026-10-31 — Quantum collections and text

Command: `& C:\ProgramData\anaconda3\python.exe tools/check.py -q`.
Result: **405 passed**, 65 external warnings, 9.83 seconds.
Artifacts: `artifacts/checks/run-191pxd3d/results.xml` and `environment.json`.

New evidence: A013-A017 exact source distributions; array copy/updates, correlated
storage, whole-array replacement, conditional assignment, helper ownership, empty
arrays, string-index observation, text snapshots, length-aware equality, coherent
text assignments, string-array element length propagation, per-element branch
joins, default empty strings, Unicode alphabets, self-permutation correlations,
character views, local text cleanup, and early quantum type-width resource errors.

Failed runs: run-ep9o5vq1 (invalid two-bit constant in a new fixture), run-p65z4ney
(new test incorrectly assumed string foreach support). Corrected the tests to the
existing contract; no acceptance requirement was removed. Physical-state tests
verify correlations and cleaned local storage. A007 measured feedforward, full
execution tooling, clean installation, Linux, and release audit remain pending.

## V010 — 2026-10-31 — Same-circuit feedforward and complete corpus execution

Command: `& C:\ProgramData\anaconda3\python.exe tools/check.py -q`.
Result: **529 passed**, 100 existing external-plugin warnings, 16.22 seconds.
Artifacts: `artifacts/checks/run-indfpw84/results.xml` and `environment.json`.
Earlier targeted feedforward run: 118 passed in 10.93 seconds.

All 17 positive source examples now execute through Qiskit transpilation and Aer
with fixed seeds and the expected output support; their ideal probabilities also
have exact projected-branch tests. All 16 negative examples retain their diagnostics.
Backend sampling checks output support/semantics, not a statistical confidence
claim about every probability. Exact comparator tests use independent Python
signed comparisons for widths 1-5 and constants beyond the measured range.

Additional evidence covers immutable snapshots, classical/quantum nesting with
preserved unmeasured coherence, branch-wide overwrite guards, helper predicates,
text length/alphabet/index behavior, conditional collections, short-circuit effect
diagnostics, anonymous measured/unobserved roots, and hidden-root escape rejection.

No CLI/build artifact, clean-install, Linux, hardware, or complete release evidence
is claimed yet. T012 must validate those delivery requirements separately.

## V011 — 2026-10-31 — Delivery, clean installation, and V1 audit

Final full suites:

- Windows: `& .\.venv\Scripts\python.exe tools/check.py -q` — **577 passed**,
  no warnings, 29.83 seconds. Artifacts: `artifacts/checks/run-o9kdw90c`.
- Debian/WSL: `artifacts/linux-venv/bin/python tools/check.py -q` from the mounted
  workspace — **577 passed**, no warnings, 36.90 seconds. Artifacts:
  `artifacts/checks/run-w6545yxc`.

Both use Python 3.13.5, Qiskit 2.3.0, Aer 0.17.2, NumPy 2.1.3, pytest 8.3.4,
and the corrected requirements-dev.lock, including psutil 7.0.0. The environments
were created inside the workspace without system/user-site packages. No global
package changes. Linux platform is Debian glibc 2.41 under WSL2 kernel 6.6.87.2.

Packaging and installed API checks (run with the corresponding environment Python):

```text
python -m pip install --only-binary=:all: -r requirements-dev.lock
python -m pip wheel --no-build-isolation --no-deps . -w dist
python -m pip install --no-index --no-deps --force-reinstall dist/qutes_lang-0.1.0.dev0-py3-none-any.whl
python -I tools/verify_install.py
python -m pip check
```

Windows and Linux installed-wheel smoke checks pass. The checker verifies the
imported module belongs to the isolated installation, invokes the public CLI with
isolated Python imports from a different working directory, and executes generated
Python with new inputs. Evidence: `artifacts/installation/windows.json` and
`linux.json`. Both dependency checks report no broken requirements. The wheel is
pure Python; final code wheel SHA256:
`5152f42594e06341878c2bd51ab93b40a91c10d94d2f961c5a22425d131a2246`.
Documentation-only source-package updates do not change the tested compiler code.
The source distribution also builds a wheel with `pip wheel --no-build-isolation
--no-deps dist/qutes_lang-0.1.0.dev0.tar.gz -w artifacts/sdist-wheel`. An archive
inventory check confirms the guide, examples, acceptance cases, independent backend
probes, smoke checker, and CI are included, with no environment/artifact/Git files.
Both wheels match all 24 current compiler Python source files byte for byte.

A separate Windows `artifacts/core-venv` contains only pip and qutes-lang. Its
isolated `python -m qutes check` and `build` commands succeed without the backend;
`run --json` returns Q5001 with installation guidance. Main parameter type checks
distinguish bool/float from int even when Python compares their values as equal.

New delivery coverage: all 17 accepted source cases execute from generated Python;
seven guide examples execute; mutable snapshots retain their old values; signed
arrays preserve ordering; generated input changes rebuild sizes/loops; deterministic
artifacts include guarded cleanup and embedded source; overwrite protection preserves
user files; missing backends and backend failures have diagnostics; preflight and
post-transpile guards prevent oversized simulation. Large classical integers round-
trip without global Python digit-limit changes, including explicitly raised memory
budgets. The test oracle remains independent of backend gate expansion.

Attempts and corrections:

- Initial integration: 565 passed on the original host (run-4l_y7mpa), with 121
  external plugin warnings. Clean environments eliminate those unrelated warnings.
- A JSON-depth regression initially expected the host recursion limit to reject
  2,000 nested arrays (run-tg7h0zgo). Added a deterministic 512-level input bound;
  targeted checks and final suites pass.
- venv ensurepip failed in the host's unwritable temp folder; task-local TEMP/TMP
  under artifacts/install-temp fixed it. Restricted DNS required normal approved
  network access for package downloads.
- The original psutil 5.9.0 pin required unavailable MSVC on Python 3.13. Changed
  to the wheel-backed 7.0.0 pin, then completed fresh Windows and Linux installs.
- Earlier clean suites (575 Windows / 576 Linux) preceded the final deterministic
  and raised-integer-budget regressions; the 577-test runs supersede them.

The complete requirement audit is docs/release-audit.md. Python 3.12 is configured
in the Windows/Linux CI matrix, but was not run locally. Hosted CI has not run;
there is no remote. No hardware, noisy simulation, public release, independent
human review, or formal proof of arbitrary programs is claimed.

## V012 — 2026-11-01 — Console and image circuit diagrams

- Final Windows workspace: `& .\.venv\Scripts\python.exe tools/check.py -q` with
  `MPLCONFIGDIR` pointing to `artifacts/matplotlib`: **596 passed**, no warnings,
  28.72 seconds. Artifacts: `artifacts/checks/run-7rwonw51`.
- Linux: `artifacts/linux-venv/bin/python tools/check.py -q tests/test_visualization.py
  tests/test_cli.py`, with project-local MPLCONFIGDIR: **28 passed**, no warnings,
  14.28 seconds. Artifacts: `artifacts/checks/run-m6j_f4sr`. This was targeted Linux
  validation; the preceding full Linux suite remains V011.
- Built/reinstalled the wheel in both existing isolated environments. Exercised the
  installed Windows `qutes.exe run ... --print-circuit --save-circuit ...` and SVG
  check command; Linux `python -I -m qutes check ... --print-circuit --save-circuit
  ... --circuit-format svg` passed too. Windows pip check reports no broken requirements.

Coverage includes all four full commands, normal/JSON console streams, ASCII
fallback, measured conditions and cleanup, PNG/SVG validity, empty classical
programs, binding-specific names, repeated writes, unrelated-file preservation,
missing dependencies, output errors, size guards, partial figure cleanup, and
verification that rendering neither simulates nor changes the circuit.

Manually inspected generated feedforward and coherent_if PNGs in
`artifacts/circuit-preview/`; labels, control lines, measurements, and folded rows
are legible. The snapshots SVG was parsed/produced successfully. Qiskit's text/mpl
drawers display the complete compiler circuit before backend-specific decomposition;
no claim of hardware-transpiled gate display is made.

New pins: Matplotlib 3.10.0, pylatexenc 2.10, Pillow 11.1.0, contourpy 1.3.1,
cycler 0.11.0, fonttools 4.55.3, kiwisolver 1.4.8, pyparsing 3.2.0. Installed only
in the project-local Windows/Linux environments. pylatexenc is built as a pure
Python wheel; all other new packages were installed as wheels. See the
[Qiskit circuit drawer reference](https://quantum.cloud.ibm.com/docs/en/api/qiskit/qiskit.visualization.circuit_drawer).

Earlier failures: run-ds5npi83 had one ASCII-wire mapping failure (fixed);
run-s_60ux17 had 595 passes and one expected-output mismatch from the user's
temporary functions.qut experiment. A separate snapshot with the committed fixture
passed 596 tests at artifacts/circuit-validation-3zmfr3d8/artifacts/checks/run-m02hz69v.
The user subsequently reverted the experiment; the final normal workspace run
above passes without altering tests or excluding that example.

## V013 — 2026-11-01 — ANTLR frontend

- `.venv/Scripts/python.exe tools/check.py -q tests/test_parser.py`: 60 passed,
  artifacts/checks/run-t3qszxdr.
- Full Windows `tools/check.py -q`: 599 passed, 1 failed, 30.08s,
  artifacts/checks/run-as9eqx7n. Failure is test_documented_examples_execute for
  user's modified snapshots.qut, expected [5,7], actual correct [5,-6].
- `tools/generate_parser.py --jar artifacts/antlr/antlr-4.13.2-complete.jar
  --java "C:/Program Files/Android/openjdk/jdk-21.0.8/bin/java.exe" --check`: passed.
- Four new diagnostic tests cover independent errors, error count bound, lexer
  collection, source excerpts and related opener locations. Existing parser corpus,
  truncation, Unicode/BOM/CRLF and nesting tests pass unchanged.

## V014 — 2026-11-01 — Script/global/effect semantics

- `tools/check.py -q`: 653 passed, 26.90s, Windows isolated Python 3.13.5,
  artifacts/checks/run-zl5icgqo.
- Earlier targeted semantic/backend/delivery suite: 324 passed, 20.53s,
  artifacts/checks/run-kuk3mdsg.
- Final targeted after short-circuit/comment corrections:
  `tools/check.py -q tests/test_scripts.py tests/test_parser.py tests/test_diagnostics.py`:
  117 passed, artifacts/checks/run-ftrkcdgl. Includes 48 script behavior/safety tests
  and independent full-state/reference-branch evidence.
- Intermediate migration runs exposed stale test expectations/fixtures; these were
  updated to the approved script contract, not bypassed by legacy compiler modes.
  Canonical snapshots test now uses new measurement_snapshots.qut, leaving user's
  edited source intact. Both source and tests explicitly express top-level execution.

## V015 — 2026-11-01 — Qutes 0.2 delivery

Full suites (Python 3.13.5, isolated dependencies, no warnings):

- Windows: `$env:MPLCONFIGDIR = Join-Path $PWD 'artifacts/matplotlib';
  & .\.venv\Scripts\python.exe tools/check.py -q`: **666 passed**, 36.25s,
  artifacts/checks/run-0rphx8ss.
- Debian/WSL, from /mnt/c/Users/gabry/Work/Quantum/qutes_lang_chatgpt:
  `MPLCONFIGDIR="$PWD/artifacts/matplotlib-linux" artifacts/linux-venv/bin/python
  tools/check.py -q`: **666 passed**, 43.38s, artifacts/checks/run-ggcdntc3.
- After final diagnostic wording only: Windows `tools/check.py -q
  tests/test_scripts.py`: **50 passed**, artifacts/checks/run-9cyfik1r.
- Early-return/alias regressions: checker/construction/scripts **162 passed**,
  artifacts/checks/run-6_vvz2k9 (superseded by full runs).

Distribution and entrypoints:

- Built dist/qutes_lang-0.2.0.dev0-py3-none-any.whl with
  `python -m pip wheel --no-build-isolation --no-deps . -w dist` and installed into
  existing project Windows/Linux/core environments using --force-reinstall.
- `.venv/Scripts/python.exe -I tools/verify_install.py` and
  `artifacts/linux-venv/bin/python -I tools/verify_install.py`: passed. Reports:
  artifacts/installation/windows.json and linux.json. Paths prove isolated imports;
  CLI and generated new-input execution passed. Both pip check commands passed.
- Final wheel source inventory matches every src/qutes/**/*.py byte in checkout.
  `setuptools.build_meta.build_sdist('dist')` produced 0.2 source archive; verified
  grammar/Qutes.g4, grammar/antlr.sha256, tools/generate_parser.py, generated parser,
  and docs/spec/language-v0.2.md. Build log: artifacts/sdist-v02.log.
- Core-only `artifacts/core-venv/Scripts/python.exe -I` with empty PATH:
  no Java/Qiskit discoverable, script compilation/Python generation passed,
  requested simulation returned Q5001. Runtime dependency 4.13.2 installed offline
  from downloaded pinned wheel; no generator/JRE bundled or invoked.
- ANTLR regeneration `tools/generate_parser.py --jar
  artifacts/antlr/antlr-4.13.2-complete.jar --java
  "C:/Program Files/Android/openjdk/jdk-21.0.8/bin/java.exe" --check`: passed.
- Installed Windows `qutes.exe check examples/measurement_snapshots.qut
  --print-circuit --save-circuit artifacts/circuit-v02 --circuit-format svg`:
  passed. Both full suites also cover PNG/SVG exports and JSON stream separation.

Coverage includes 18 positive and 16 negative acceptance programs, script globals,
input schemas, helper measurement, repeated snapshots, transitive restrictions,
full complex reference-entangled states and clean scratch, early exits, mutable
stages/shapes, ordinary main/no-op scripts, error recovery and artifact guards.
Initial delivery run-gpbbv0xa had 63 passes/one stale dependency-metadata key
expectation; corrected for the new ANTLR runtime and superseded by the full runs.

Python 3.12 is configured in CI but not run locally. Hosted CI has not run; no remote
or push exists. No hardware validation, formal proof or independent human review.
User experiment snapshots.qut is preserved; canonical tutorial tests run the new
measurement_snapshots.qut. No semantic tests use a legacy main-execution adapter.

## V016 — 2026-11-04 membership checkpoint

Windows project Python 3.13.5. Commands:
- `.venv/Scripts/python.exe tools/check.py -q tests/test_membership.py`: 28 passed,
  15.40s; artifacts/checks/run-hkmyce4j.
- `.venv/Scripts/python.exe tools/check.py -q`: 694 passed, 40.50s;
  artifacts/checks/run-0ezaqi_y.
- `tools/generate_parser.py --jar artifacts/antlr/antlr-4.13.2-complete.jar --java
  "C:/Program Files/Android/openjdk/jdk-21.0.8/bin/java.exe"` regenerated sources.
- `git diff --check`: passed. Linux and 0.3 distribution validation pending.

## V017 — 2026-11-04 search checkpoint

Windows project Python 3.13.5, Qiskit 2.3.0.
- `tools/check.py -q tests/test_search.py`: initial 37 passed/6 failed due to
  test fixtures; corrected signed range and reserved identifier. run-8kfd6k_t.
- `tools/check.py -q tests/test_search.py tests/test_cleanup.py tests/test_gates.py`:
  94 passed, 4.64s; run-gfw3934c.
- `tools/check.py -q`: 744 passed, 41.91s; run-rzmb69nz.
- After adding a full complex-state reference-entanglement check,
  `tools/check.py -q tests/test_search.py`: 51 passed, 4.22s; run-op7p_yb5.
Commands used `.venv/Scripts/python.exe`; reports under artifacts/checks.
No hardware, Linux release, installed 0.3 package or human review claimed yet.

## V018 — 2026-11-04 release validation

Final source package/language 0.3, artifact schema 3. Python 3.13.5 on Windows 11
and Debian/WSL; Qiskit 2.3.0, Aer 0.17.2, NumPy 2.1.3, ANTLR runtime 4.13.2.

- `.venv/Scripts/python.exe tools/check.py -q`: **775 passed**, 52.95s;
  artifacts/checks/run-nou9xgzv (zero errors/failures/skips).
- `wsl.exe -d Debian -- /mnt/c/Users/gabry/Work/Quantum/qutes_lang_chatgpt/artifacts/linux-venv/bin/python /mnt/c/Users/gabry/Work/Quantum/qutes_lang_chatgpt/tools/check.py -q`:
  **775 passed**, 71.23s; artifacts/checks/run-2nwmk3_m.
- Earlier release runs passed 770 each, then 774 each after added oracle/resource
  cases. Final budget-guard source supersedes them; 89 focused membership/search
  tests also passed (run-g84xvyk4).
- `.venv/Scripts/python.exe -m pip wheel --no-build-isolation --no-deps . -w dist`:
  built qutes_lang-0.3.0.dev0-py3-none-any.whl, SHA256
  d88eb6bca6960a4dff8c1cf2d4485cb226c9664dbb54df6603a04c721e2f908a.
  All 33 src/qutes/**/*.py files match archived wheel bytes exactly.
- Installed final wheel using `python -m pip install --no-deps --force-reinstall
  dist/qutes_lang-0.3.0.dev0-py3-none-any.whl` in project Windows, Linux, and
  core-only environments. No global packages changed. `python -I
  tools/verify_install.py` passes Windows/Linux CLI, generated module and generated
  search changed-input specialization. Reports: artifacts/installation/windows.json
  and linux.json. `python -m pip check` passes both environments.
- Core-only `artifacts/core-venv/Scripts/python.exe -I -` with PATH empty:
  membership/search source compiles, artifact-v3 Python generates, Qiskit is absent,
  execution deliberately reports Q5001. Java is not needed to install/use compiler.
- With workspace TEMP/TMP, `.venv/Scripts/python.exe tools/generate_parser.py --jar
  artifacts/antlr/antlr-4.13.2-complete.jar --java
  "C:/Program Files/Android/openjdk/jdk-21.0.8/bin/java.exe" --check`: passed.
- Installed `qutes run examples/search.qut --alphabet AB --shots 64 --seed 17`:
  AB 34, BB 30, 8 qubits. Numeric example: 1 34, 3 30, 21 qubits. These are
  deterministic-seed smoke samples, not statistical proof of the success bound.
- test_search_delivery covers generated/direct phase parity, changed input lengths,
  CLI floating-point config and JSON diagnostics, console diagrams and saved SVG.
  Existing visualization suites cover PNG and resource guards on both platforms.
- test_search and test_membership cover independent full complex/reference-entangled
  states, scratch zero, duplicate indices, no-match branch weights, conditional
  success bounds, literal/quantum wildcards, operand order, alias protection,
  ownership moves, input-version cleanup, non-consuming measurement, impossible
  cleanup, transitive effects, non-power-of-two sizes and work-budget rejection.
- `git diff --check`: passed. Expanded acceptance corpus: 20 positive and 17
  negative programs; frontend, construction, execution and generated-module suites.

Environment failures are recorded in KB-018: default Windows temporary directories
caused pip/parser failures; workspace TEMP/TMP retries succeeded. Failed pip backup
folders were removed only after installed-package verification. WSL needs normal
approval review. No test failures are being suppressed. No hardware, formal proof,
independent human review, Python 3.12 execution, hosted CI or remote publication.

Source distribution: `setuptools.build_meta.build_sdist("dist")` passed;
artifacts/sdist-v03.log. Verified dist/qutes_lang-0.3.0.dev0.tar.gz includes the
authoritative grammar/hash, regeneration tool, active spec, compiler modules,
search tests and examples.


## V019 - 2026-11-05 language operation tour and user defaults

Environment: Windows 11 and Debian/WSL, Python 3.13.5; backend pins unchanged from
V018. Tests import the current checkout. No installed-wheel rebuild in this batch.

- `.venv/Scripts/python.exe tools/check.py -q tests/test_language_examples.py`:
  initial 39 passed, 6.67s (run-iwrb6snr).
- `.venv/Scripts/python.exe tools/check.py -q`: final **814 passed**, 63.61s;
  artifacts/checks/run-dn9pqzbu.
- `wsl.exe -d Debian -- /mnt/c/Users/gabry/Work/Quantum/qutes_lang_chatgpt/artifacts/linux-venv/bin/python /mnt/c/Users/gabry/Work/Quantum/qutes_lang_chatgpt/tools/check.py -q`:
  **814 passed**, 85.09s; artifacts/checks/run-372bgprl.
- The 38 tour examples run at 64 shots/seed 17 with explicit adjacent qutes.toml.
  Each stays under 24 qubits including backend decomposition; maximum allocated 21.
  JSON output comparisons preserve type distinctions. Search sampling threshold is
  a smoke check only; mathematical/statevector checks remain in the existing suite.
- `.venv/Scripts/python.exe tools/qutes.py run examples/language/07_inputs.qut --inputs examples/language/07_inputs.json --shots 64 --seed 17`:
  [true,true,true,true,true,true] in all 64 shots.
- `.venv/Scripts/python.exe tools/qutes.py explain examples/language/33_search_strings.qut`:
  13 qubits, 4 oracle calls, 2 retained index qubits, 7 workspace qubits, limit 24.
  Confirms automatic discovery of the adjacent tour config.
- Ad hoc compile audit compared all 38 guide qubit counts to compiler reports and
  resolved every Markdown link in the tour guide: passed. `git diff --check` passed.

Earlier full runs: run-pr215uh3 had 812 passed/2 failed because two tests depended
on former 8-bit/ASCII defaults; those tests now explicitly request their intended
width/alphabet. run-01c8sgfw had 813 passed/1 failed because example 22 was edited
on disk to assign A? but its catalog still expected AB. Preserved the source and
corrected expected outputs/docs. Final runs supersede these failures. KB-019 records
an initial incorrect ad hoc import, corrected before the direct execution check.
No hardware, hosted CI, independent human review or new package-install validation.

## V020 - 2026-11-05 reporting and documentation

Windows Python 3.13.5; unchanged pinned dependencies.
`.venv/Scripts/python.exe tools/check.py -q tests/test_readability_reporting.py tests/test_values.py tests/test_delivery.py tests/test_cli.py`:
92 passed, 17.93s; artifacts/checks/run-7xdbn37f. Covers units, huge symbolic
estimates, CLI warning deduplication/JSON, silent Python API, existing encoding,
delivery and command behavior. `git diff --check` passed. Walkthrough commands
executed through tools/qutes.py against the checkout, plus generated module.
Final complete cross-platform/package checks are reserved for checkpoint T023.

## V021 - 2026-11-05 provenance and named circuits

Windows Python 3.13.5, pinned Qiskit 2.3.0/Aer 0.17.2.
- `.venv/Scripts/python.exe tools/check.py -q tests/test_lowering.py tests/test_construction.py tests/test_cleanup.py tests/test_language_examples.py tests/test_search.py tests/test_delivery.py`:
  257 passed, 19.87s; run-k_x9s2k9.
- `.venv/Scripts/python.exe tools/check.py -q tests/test_provenance.py tests/test_construction.py tests/test_search_delivery.py tests/test_visualization.py`:
  75 passed, 5.80s; run-k5klc840 after final binding-range changes.
- Covers direct/generated circuit equality, decoded snapshots, collisions, aliases,
  returned storage, permutations/foreach views, search partitions, region nesting,
  membership provenance, zero/restored wires and unchanged example-12 resources.
- Earlier 109/2 failed representation assertions and fixes recorded in KB-021.
  Full cross-platform validation is still pending T023; no wire reuse introduced.

## V022 - 2026-11-05 final readability validation

Python 3.13.5 on Windows 11 and Debian/WSL, Qiskit 2.3.0, Aer 0.17.2, NumPy 2.1.3,
ANTLR runtime 4.13.2; language 0.3, artifact 3, package 0.3.0.dev0 unchanged.

- `.venv/Scripts/python.exe tools/check.py -q`: **858 passed**, 58.95s;
  artifacts/checks/run-vojkmdco.
- `wsl.exe -d Debian -- /mnt/c/Users/gabry/Work/Quantum/qutes_lang_chatgpt/artifacts/linux-venv/bin/python /mnt/c/Users/gabry/Work/Quantum/qutes_lang_chatgpt/tools/check.py -q`:
  **858 passed**, 82.16s; artifacts/checks/run-3uds1wvr.
- Focused source tests and superseded intermediate runs recorded in KB-022.
  test_diagrams verifies exact complex operators, selected oracle phases, quantum
  collection statevectors/correlations, zero scratch, dynamic execution, depth,
  selector errors, image identity, zero-cost cleanup and lazy-decomposition budgets.
- All 13 `qutes ...` lines in docs/cli-walkthrough.md executed via tools/qutes.py;
  generated `python artifacts/tour.qiskit.py --shots 64 --seed 17` also passed.
  Markdown file targets in changed guides/spec references/archive resolve.
- `.venv/Scripts/qutes.exe check examples/language/15_coherent_if.qut --unfold 1
  --print-circuit --json` passed against installed wheel; JSON stdout stored at
  artifacts/installed-diagram.json. Diagram remains on stderr.
- Ad hoc compile of `for(int i=0;i<500;i++) { qubit temporary=false; }`:
  500 unique register names and exact cleanup annotations, zero execution gates.
- Visual inspection: artifacts/readability-preview/15_coherent_if-74c0905e31a4-64eeb63a.png
  and 24_quantum_functions-b10fd174aae1-125722a6.png; names, source blocks and separate
  cleanup/restored-input labels legible. Existing image tests cover PNG and SVG.
- With workspace TEMP/TMP, `python -m pip wheel --no-build-isolation --no-deps . -w dist`
  built final qutes_lang-0.3.0.dev0-py3-none-any.whl, SHA256
  80d322734ea83532cc1a4c5953830c718a9762a70376c84ef67e45edd5d2bc36.
  Installed via `python -m pip install --no-deps --force-reinstall WHEEL` in each
  project environment. `python -I tools/verify_install.py` passes Windows/Linux
  CLI, named registers, selective diagrams and generated input respecialization.
  Reports: artifacts/installation/windows.json and linux.json. `python -m pip check`
  passes both environments; no dependency changes. No global installation.
- Source distribution rebuilt using setuptools.build_meta.build_sdist, inspected
  for new guides/contracts/archive/tour README/diagram module. Wheel module bytes
  compared with src/qutes/**/*.py. `git diff --check` passes.

No hosted CI, hardware execution, Python 3.12 run, or independent human review.
Wire reuse remains deferred; rendered annotations never enter executable circuits.

## V023 - 2026-11-05 allocation foundation

Windows Python 3.13.5, existing pinned dependencies.
`.venv/Scripts/python.exe tools/check.py -q tests/test_wires.py tests/test_cleanup.py tests/test_search.py tests/test_lowering.py`:
**133 passed**, 5.58s; artifacts/checks/run-s58tv4om. Earlier two Measurement
field-access failures corrected (KB-023). Independent complex state comparison
checks final live logical-to-physical mapping and zero released state, including
reference entanglement and later reconstruction. This is checkpoint-1 evidence,
not full execution/CLI/diagram/distribution validation. Those remain required.

## V024 - 2026-11-06 physical execution checkpoint

Windows Python 3.13.5, unchanged backend pins.
`.venv/Scripts/python.exe tools/check.py -q tests/test_wire_execution.py tests/test_wires.py tests/test_delivery.py tests/test_diagrams.py tests/test_search.py tests/test_scripts.py tests/test_provenance.py tests/test_visualization.py tests/test_artifact_v2.py tests/test_search_delivery.py`:
**240 passed**, 20.59s, artifacts/checks/run-ow5c4uz6. Covers mapped full complex
search/reference states, free scratch, cleanup proof prefixes, input specialization,
generated/direct equality, legacy schema 3, config switches, physical simulation
limits, measured snapshots/feedforward and existing view/image tests. Earlier
failed/intermediate runs recorded in KB-024. `git diff --check` passes.
Full Windows/Linux/release acceptance remains checkpoint 3.

## V025 - 2026-11-06 final wire reuse validation

Windows11 and Debian/WSL, Python3.13.5; Qiskit2.3.0, Aer0.17.2, NumPy2.1.3,
ANTLR4.13.2 unchanged. Language0.3/package0.3.0.dev0/artifact4 with v3 compatibility.

- `.venv/Scripts/python.exe tools/check.py -q`: **907 passed**, 78.79s;
  artifacts/checks/run-917rvzk8.
- `wsl.exe -d Debian -- /mnt/c/Users/gabry/Work/Quantum/qutes_lang_chatgpt/artifacts/linux-venv/bin/python /mnt/c/Users/gabry/Work/Quantum/qutes_lang_chatgpt/tools/check.py -q`:
  **907 passed**, 96.02s; artifacts/checks/run-hh5g0qad.
- `.venv/Scripts/python.exe tools/check.py -q tests/test_wire_execution.py tests/test_wire_views.py tests/test_language_examples.py tests/test_wires.py`:
  87 passed, 10.46s; run-uf2n0x1_. Earlier fixture correction in KB-025.
- With workspace-local TEMP/TMP, `.venv/Scripts/python.exe tools/generate_parser.py --jar artifacts/antlr/antlr-4.13.2-complete.jar --java "C:/Program Files/Android/openjdk/jdk-21.0.8/bin/java.exe" --check`: pass.
- All 17 commands in docs/cli-walkthrough.md executed with tools/qutes.py (generated
  module with source PYTHONPATH); artifacts/wire-walkthrough.json records each exit0.
  Tour resource-count and active-document link audits pass. PNG inspected as KB-025.
- `.venv/Scripts/python.exe -m pip wheel --no-build-isolation --no-deps . -w dist`
  with workspace TEMP/TMP: qutes_lang-0.3.0.dev0-py3-none-any.whl, SHA256
  dea2099d260ae46c3a23cf5526d459cf4de9c0c960c75a5c46ac53bf39844af4.
  Installed via `python -m pip install --no-deps --force-reinstall WHEEL` in project
  Windows, Debian and Windows core-only environments. No global install.
- `.venv/Scripts/python.exe -I tools/verify_install.py` and Linux equivalent pass;
  artifacts/installation/windows.json and linux.json. Includes CLI, generated input
  changes, named/indexed registers, selective diagrams, 39->6 reuse and logical view.
  Initial verifier naming assumption fixed as KB-025; no compiler change required.
- `python -m pip check` passes Windows/Linux. Core-only Python with PATH empty
  compiles 39->6 and generates artifact4 without Java/Qiskit; build reports Q5001.
- Source archive built with setuptools.build_meta.build_sdist('dist'); wheel source
  bytes and source archive coverage checked at final commit. `git diff --check` passes.

No hosted CI, hardware, Python3.12 execution or independent human review.
All simulation limits remain enforced; reduced physical width is not a promise
of hardware speedup. Logical allocated IDs cannot directly index physical states.

Final source includes the independent allocation reference preflight and linear
workspace membership lookup. Focused command
`.venv/Scripts/python.exe tools/check.py -q tests/test_wire_execution.py tests/test_wires.py tests/test_search.py tests/test_wire_views.py`:
103 passed,7.25s,run-qv2or_fx. KB-025 records superseded907 runs and the wide
compile-only probe. No simulation was attempted for that oversized probe.

## V026 - 2026-11-20, partial 0.4 foundation

Windows/Python3.13.5, existing pinned backend. Parser regenerated with
.venv/Scripts/python.exe tools/generate_parser.py --jar artifacts/antlr/antlr-4.13.2-complete.jar --java "C:/Program Files/Android/openjdk/jdk-21.0.8/bin/java.exe"
(TEMP/TMP workspace artifacts/install-temp).
.venv/Scripts/python.exe tools/check.py -q tests/test_v04_types.py tests/test_parser.py tests/test_checker.py tests/test_construction.py tests/test_scripts.py
242 passed,4.64s,run-x5g90cwn. Earlier failed228/3 run-cdm52k2i described KB026.
No full suite/Linux/package claim yet; installed wheel remains0.3.

V026 checkpoint evidence (supersedes foundation-only status):
- .venv/Scripts/python.exe tools/check.py -q:932 passed,54.18s,run-tdlfjb20.
- Focused checker/construction/membership/provenance/collections/feedforward/
  scripts/tour/references suite:412 passed,31.28s,run-ttr0vcz5.
- After transitive-rebind/retention assertions: tests/test_v04_references.py
  tests/test_v04_types.py tests/test_search.py tests/test_readability_reporting.py:
  97 passed,3.96s,run-6bpoiomx.
- After final overflow and reference-budget guards: .venv/Scripts/python.exe
  tools/check.py -q tests/test_v04_types.py tests/test_v04_references.py
  tests/test_language_examples.py tests/test_search.py:126 passed,8.15s,run-bbmsj_9g.
- wsl.exe -d Debian -- /mnt/c/Users/gabry/Work/Quantum/qutes_lang_chatgpt/artifacts/linux-venv/bin/python /mnt/c/Users/gabry/Work/Quantum/qutes_lang_chatgpt/tools/check.py -q tests/test_v04_references.py tests/test_v04_types.py:
  25 passed,15.75s,run-wuz3y0nx (before final additional regressions). Initial
  restricted launch Wsl/E_ACCESSDENIED; elevated retry succeeded.
- Pinned parser --check passes with V026 command/environment. git diff --check
  passes (Git warns about CRLF normalization only). Initial failures recorded KB026.
No installation or complete0.4 validation yet. Package/artifact version migration
and old artifact respecialization guard remain T029 before any release.

## V027 - 2026-11-20 live operations

.venv/Scripts/python.exe tools/check.py -q tests/test_gates.py tests/test_cleanup.py tests/test_coherent_control.py tests/test_measurement_cleanup.py tests/test_v04_references.py
138 passed,5.42s,run-7r8jaife.
.venv/Scripts/python.exe tools/check.py -q tests/test_v04_operations.py
16 passed,1.80s,run-d6d7hq_6 (initial cases).
.venv/Scripts/python.exe tools/check.py -q tests/test_v04_operations.py tests/test_coherent_control.py tests/test_measurement_cleanup.py tests/test_cleanup.py tests/test_wire_execution.py tests/test_search.py
177 passed,8.72s,run-y3w8_ajz (18 final operation cases). QFT compares the full8x8
operator to an independent Fourier matrix; inverse compares full operators;
teleportation checks external correlations in complementary bases. Joint cleanup
checks the complete final state and zero certificates. Final Windows/Linux/package
validation remains T029. No independent human review claimed.

## V028 - 2026-11-20 preparation and subtraction

Windows Python3.13.5, existing pinned dependencies.
- .venv/Scripts/python.exe tools/check.py -q tests/test_v04_preparation.py:
  20 passed,4.58s,run-76wcfsmn (before two further correlation/control tests).
- .venv/Scripts/python.exe tools/check.py -q:
  974 passed/2 failed,57.48s,run-4jqgbudz; both corrected as KB028.
- .venv/Scripts/python.exe tools/check.py -q tests/test_v04_preparation.py tests/test_checker.py tests/test_feedforward.py:
  220 passed,12.43s,run-7pkw7b34. Includes22 new preparation/arithmetic cases.
- git diff --check passes; only line-ending normalization warnings.
Full final Windows/Linux/package checks remain T029. No release claim yet.

## V029 - 2026-11-20 coherent indexing

Windows Python3.13.5, pinned backend. Commands:
- .venv/Scripts/python.exe tools/check.py -q:
  1006 passed/1 failed,61.12s,run-57jpnj3y. R011 now explicitly validates its
  construction-time bounds rejection; type analysis alone cannot prove bounds.
- .venv/Scripts/python.exe tools/check.py -q tests/test_v04_indexing.py tests/test_checker.py tests/test_construction.py tests/test_search.py tests/test_v04_references.py:
  220 passed,5.36s,run-kea5b2gr. Includes31 indexing/support cases.
Earlier focused failures and fixes are recorded KB029. Full final platform and
distribution validation remains T029. No simulator or samples used for proof.

## V030 - 2026-11-20 Qutes0.4 integration and delivery

Final source: package0.4.0.dev0/language0.4/artifact5. Windows11 and Debian/WSL2,
Python3.13.5; ANTLR4.13.2/Qiskit2.3.0/Aer0.17.2/NumPy2.1.3. No independent review,
hardware/hosted CI or Python3.12 execution. Exact evidence stays in ignored artifacts.

- `.venv/Scripts/python.exe tools/check.py -q`: **1032 passed**,83.44s,
  artifacts/checks/run-f40mx194. Prior1031 passed85.98s run-j6foy26j precedes the
  final unsupported whole-slice assignment guard. Earlier1030 passed90.86s run-fg7587z9 precedes the
  final mutable-binding/readonly-view regression. Focused final100 passed17.75s,
  run-rwggcob1. Initial rendering keyword failures are recorded KB030.
- `wsl.exe -d Debian -- /mnt/c/Users/gabry/Work/Quantum/qutes_lang_chatgpt/artifacts/linux-venv/bin/python /mnt/c/Users/gabry/Work/Quantum/qutes_lang_chatgpt/tools/check.py -q`:
  **1032 passed**,123.51s,run-s0dkm8xk. Prior1031 passed109.30s run-zjpl31z4;
  earlier1030 passed119.04s run-70bx56ej. Both superseded by the final run.
- `.venv/Scripts/python.exe tools/generate_parser.py --jar artifacts/antlr/antlr-4.13.2-complete.jar --java "C:/Program Files/Android/openjdk/jdk-21.0.8/bin/java.exe" --check`:
  pass, byte-reproducible generated parser. TEMP/TMP=workspace artifacts/install-temp.
- `.venv/Scripts/python.exe tools/verify_walkthrough.py`:26 commands pass;
  artifacts/walkthrough-v04.json. Covers all seven modes, JSON/inputs/generated
  execution, console, PNG/SVG and unfolded views. QFT PNG inspected visually.
- All50 tour files execute at64 shots/seed17 within24 wires (full-suite test).
  Installed compiler resource audit: max15; examples40-50 respectively
  0,2,3,3,4,12,6,3,1,3,0. artifacts/tour-v04-resources.json. Unicode probe retry KB030.
- `.venv/Scripts/python.exe -m pip wheel --no-build-isolation --no-deps . -w dist`
  with workspace TEMP/TMP: qutes_lang-0.4.0.dev0-py3-none-any.whl, SHA256
  39317efad83e27d30387e6ea8b1423dfef7225054bcaf92352823b78f9e64168.
  Zip entries match all45 src/qutes Python files byte-for-byte, including parser
  sources, numeric/reference/support/preparation and artifact adapters.
- `python -m pip install --no-deps --force-reinstall WHEEL` in project .venv,
  artifacts/linux-venv and artifacts/core-venv. Windows TEMP retry detailed KB030.
  `.venv/Scripts/python.exe -I tools/verify_install.py` and Linux equivalent pass:
  artifacts/installation/windows.json and linux.json. Both `python -m pip check`
  pass with no broken requirements. Installed wheel retains all CLI modes.
- Core-only `artifacts/core-venv/Scripts/python.exe -I` with PATH empty and no
  Qiskit: compile sparse preparation/coherent read/phase and generate schema5
  successfully. Installation/compilation requires no Java.
- Source archive: `setuptools.build_meta.build_sdist('dist')`; checked inclusion
  of grammar, active docs, new source/tests, all50 tour files and walkthrough tool.
  `git diff --check` passes; normalization warnings only. Snapshots/config/ignore
  file diff is empty; both untracked user images preserved. No remote/push.

Full phase/correlation/operator checks include Bell, teleportation with reference
entanglement, QFT versus DFT, inverse preparation/gates, index/data correlations,
zero scratch and deliberately impossible cleanup. Schemas3/4 cached array-copy
semantics and changed-input rejection are tested before compiler invocation.

V031 (Windows, Python 3.13.5): python tools/check.py -q passed 1032 in 97.93s (run-f1eopz74), including all 50 tour programs. python tools/verify_walkthrough.py passed 26. Executed the notebook code cells in order with PYTHONIOENCODING=utf-8 and release src on PYTHONPATH; both matching and opposite correlations passed on Aer.
Import diff flags three inherited blank lines at EOF, two in byte-reproducible ANTLR output. Retained source bytes.

Clean 0.4.0 wheel installation: artifacts/rc-env/Scripts/python.exe -I tools/verify_install.py passed; pip check clean. First hosted run 44784591985 rejected workflow YAML before jobs; block-quoted the pip filter containing a colon.

V032: corrected run 44785749075 passed Windows and Ubuntu on Python 3.12 and 3.13. Release a78cc16, bundle SHA-256 3764ecf7e8ea7767b929660ec87643b7a81d3314f19019c07fbadf41db218a88. Fresh wheel verifier and pip check passed. Executed extracted notebook in the clean wheel environment with -I -X utf8 (Windows -I ignores PYTHONIOENCODING); both correlations passed. Standalone starter SHA-256 3a96943d51a5ea0ad7d97a444906f4d504d6437d797c3171406a21b416c6c552: extracted and ran main.qut with bundled inputs/config in clean Aer, 34/30 equal outcomes. Browser export gave 30/34 opposite outcomes. Chromium/Firefox/WebKit passed four curated cases, diagnostics, cancellation/restart, limits and exports on Windows. Website tests/test_engine.py passed full-state comparisons and feedforward. Native Safari untested.

V033: gh run view 44785749075 reported 1032 successes in each matrix job (Linux 3.12/3.13 29.24s/38.78s; Windows 3.12/3.13 31.55s/47.49s). Website npm test passed with published ZIP in hosted runs 44786813596 and 44787628431; the Firebase preview and live site returned only opposite bits for the edited Bell source, and manifest.commit matched a78cc16. Live Build route linked the verified starter. gh release view v0.4.0 confirmed a public non-prerelease with three assets. A clean build from 9d49e5e produced the matching canonical standalone source and config; release assets remain the pinned published bytes. Hosted actions reported Node 20 action-runtime deprecation warnings; deployments succeeded.

V034 (Windows, Git/GitHub CLI): git show -s --format="%H %P %T" 2.0 identified merge 6bc0ecf, parents d4410ae and e1c78a8, tree 8fc8e21. git diff --exit-code d4410ae 2.0 passed. git rev-list --count e1c78a8 returned 30. git merge-base --is-ancestor e1c78a8 2.0 passed. GitHub commit API confirmed both parents. git ls-remote origin refs/tags/2.0 refs/tags/v0.4.0 returned only 2.0. GitHub releases API before/after matched the same release ID, asset IDs, names, sizes and digests. curl -L on the new starter URL returned 200; the old returned 404. Compiler tests were not rerun locally for this history-only merge.

V035: Windows: python scripts/build.py downloaded the 2.0 release archive and verified the pinned SHA-256 and build revision a78cc16. Hosted npm test and python tests/test_engine.py passed in preview run 44791119262 and production run 44791968090. Playwright Chromium followed the link on /build, verified HTTP 200 and SHA-256 3a96943d51a5ea0ad7d97a444906f4d504d6437d797c3171406a21b416c6c552 for the starter and 3764ecf7e8ea7767b929660ec87643b7a81d3314f19019c07fbadf41db218a88 for /qutes-resources.zip, then ran the Bell example with not(bob) before return. Both Firebase endpoints produced only opposite pairs. Downloadable compiler version is 0.4.0.
V036: Windows Python 3.13.5, python tools/check.py -q: 1032 passed in 69.01s (run-1j6wq1qi) with package version 2.0.0 and unchanged schema 5. Release asset validation follows after the build from this commit.

V036 release: python tools/build_resource_bundle.py dist/qutes-resources-2.0.0.zip from clean commit 0367b52; manifest file digests and starter wheel equality verified. Bundle SHA-256 30819d5be08edd3357fa94cbc9c1af38876513c22854e5ccb7669a4f48a3cc1f, starter 71a4b63a7ab0a2c96a9f1d9eace2355949f80ad188c964807b2f4cb59c40b7ed, wheel 289dfafbab44ccf25d685e4fd28384021947b97c87a4abe1a27821938d27f6d7. Installed wheel in artifacts/rc-env; python -I tools/verify_install.py, python -m pip check and qutes --version passed. Starter run: 64 shots, 34/30 equal pairs. Website python scripts/build.py fetched the published package; python tests/test_engine.py passed both cases. A local Chromium check followed the new download URL, verified starter bytes, and ran the 2.0.0 browser compiler on the Bell program. Tag pushed to dispatch hosting; no website pipeline wait.

V039 initial: Python py_compile checked the portable launcher, packager and smoke harness. git diff --exit-code 0367b52 -- requirements-dev.lock passed. GitHub release metadata matched the original tag and the three existing asset digests.

V039 Windows attempt 44808550082: native archive built. Clean verification stopped on the combined parent-path/size assertion for the exported circuit. Publication stayed gated.

V039 final: workflow 44809167547 ran Python 3.12 tools/portable/build.py on five native runners with the pinned release wheel. Separate jobs ran python -I tools/portable/verify.py on the exact uploaded archives; all seven CLI commands, Bell pairs, phase, 39 logical / 6 physical qubits, generated Python, PNG, SVG and compiler diagnostics passed. A local Windows run of the corrected verifier also passed on the first candidate. The publisher re-downloaded and SHA-256-verified all five delivered archives and their manifest, confirmed original asset IDs and hashes and the release tag. Anonymous HTTPS HEAD returned 200 for every platform asset after fetching the public checksum file. The baseline suite at the packaging commit is tracked separately by CI run 44809167569.

V041 initial: compiled all 50 tour sources with the installed 2.0.0 wheel and UTF-8 decoding. Only examples 22 and 30 report QW0001. Bell passed at 64 shots (34/30 matching pairs). An initial ad hoc Windows check using the system text encoding misread a Unicode literal; explicit UTF-8 fixed the check.

V041 final release: compiler CI 44813512750 passed all four Windows/Ubuntu Python 3.12/3.13 jobs; portable workflow 44813512817 passed five build/clean-verification pairs, including the default and explicit wildcard checks. The publisher downloaded and re-hashed all r2 assets before changing the release description. The local starter emitted no warning, and both bundled wheels matched the original release exactly.

V043 local: in the website checkout, python scripts/build.py fetched and checked both pinned inputs. With QUTES_PREVIEW_URL=http://127.0.0.1:4197, npm.cmd test passed 5/5 (Chromium, Firefox, WebKit, static download page and eight labs). python tests/test_engine.py passed both comparisons with Qiskit. The local website change starts at 191c5f7. At 0d0d46d verified both python scripts/build.py --source PATH and python scripts/build.py produce an identical browser compiler ZIP with SHA-256 07e43644affb2e1a98c10f0362e8a9ab56a8d6cf5b1a7022ebf00502bab3cc00 and unchanged browser-tested contents. Language packaging scripts passed python -m compileall -q tools/portable. No browser or compiler semantics changed.

V043 packaging: git archive of 0367b52 followed by python -m pip wheel --no-deps built Qutes 2.0.0. Compared all compiler modules with the original SHA-256-verified release wheel. Only the line endings of qutes/__init__.py differed. An initial comparison used a cached 0.4.0 artifact, which was discarded before this check.

V043 release: gh release download 2.0.0 --repo GabrieleMessina/qutes_lang --pattern 'qutes-2.0.0-r2-*' --dir artifacts/portable-only fetched the five archives and original manifest. Each file matched its previous manifest row and the GitHub API SHA-256. After cleanup, gh api repos/GabrieleMessina/qutes_lang/releases/tags/2.0.0 showed six uploaded assets, the same five archive IDs and the updated notes. An anonymous GET of the canonical checksum URL returned five rows, file SHA-256 8627f863eba00bc2c3cf7e1dfcd11356fbf0dbfcabd852ae5d4120ced49cad2a. python -I tools/portable/verify.py on the public Windows archive passed Bell, phase, reuse, diagnostics, export and all seven CLI commands. Compiler CI 44817037480 passed all four jobs. Anonymous HEAD confirmed the live starter link returns 404 and the old site-hosted ZIP returns 200.

V043 publisher: tested the matching release and unexpected-asset refusal using a temporary offline fixture and disabled external subprocess calls. Live release verification used the read-only release API and public downloads.

V043 hosted: run 44817037408 built the compiler from the Git source pin and passed all five clean archive verifications. The publisher was skipped. At website commit 0d0d46d, node --test tests/build.test.cjs tests/tutorial.test.cjs passed 2/2 again against the final local preview.

V044: git ls-remote --heads origin, git branch --merged origin/qutes2.0, git worktree list and gh pr list established the scope of branch cleanup. No local or remote Codex working refs remained in either repository. Website commit 0d0d46d058294f64f37aeaec9869040328ef1e46 was pushed to qutes2.0. gh workflow run 425273117 --ref qutes2.0 -f channel=live --repo GabrieleMessina/qutes_website started run 44818550125. Hosted tests, preview manifest verification and production promotion all passed. Anonymous HTTPS verified the production Build HTML, five archive HEAD responses (200), the five-row checksum file against GitHub asset digests, and the 2.0.0 manifest at source revision 7070205. HEAD /qutes-resources.zip and /release/wheels/qutes_lang-2.0.0-py3-none-any.whl each returned 404.

V044 live browser: with QUTES_PREVIEW_URL=https://qutes-lang.web.app, node --test --test-name-pattern 'Build offers|chromium runs' tests/build.test.cjs tests/playground.test.cjs passed 2/2. This exercised the five visible downloads without JavaScript, first-run commands, responsive layouts, and playground execution and generated Qiskit export in Chromium.

V045 compiler: python -m pytest -q tests/test_standalone.py tests/test_delivery.py passed 102 tests. The new exporter produced matching circuits and decoded sampled classical bit patterns for all 50 tour examples. Compared the original Git revision of python_source with the refactored CLI generator on all 50 examples and got byte-identical modules. The isolated Windows Python 3.13.5 environment passed pip check and has neither the qutes nor antlr4 module.

V045 decoder: reproduced Python SyntaxError on an unrolled 225-iteration return expression. After emitting intermediate assignments, python -m pytest -q tests/test_standalone.py passed all 52 cases including this regression.

V045 final: on Windows/Python 3.13.5, python -m pytest -q passed 1,084 compiler tests on 5ee169d. Website python scripts/build.py used the local Git archive; tests/test_engine.py passed both native Qiskit comparisons. QUTES_PREVIEW_URL=http://127.0.0.1:4197 and QUTES_EXPORT_PYTHON pointing to artifacts/standalone-aer-env/Scripts/python.exe: npm.cmd test passed 6/6 across Chromium, Firefox and WebKit. The expanded node --test tests/standalone.test.cjs passed again, including text and complex results. It saved actual browser downloads to an external temp directory, verified the qutes module was absent, ran each file under python -I, and checked the public circuit API, selected shots, overrides, Bell edits, signed wire reuse, two construction-time bindings, phase and feedforward. Only qiskit==2.3.0 and qiskit-aer==0.17.2 were directly installed in the fresh venv. The saved review file in website artifacts/standalone-review/experiment.qiskit.py, run with --seed 17, returned 34 false/false and 30 true/true in 64 shots. Local HTTP verified the final source revision and export panel.
