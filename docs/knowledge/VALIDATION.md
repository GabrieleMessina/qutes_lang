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
