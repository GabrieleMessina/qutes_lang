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

## V013 � 2026-11-01 � ANTLR frontend

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
