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
