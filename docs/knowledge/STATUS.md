# Current status

Updated: 2026-10-30, checkpoint KB-004. Full implementation goal remains active.

## Completed capabilities

- Local Git main; no remote. Previous commits: a29edbf (knowledge base), 4b8d3d8
  (contract/feasibility), 18d3d56 (parser). Current checkpoint adds typed analysis.
- Parser with source spans/diagnostics, immutable syntax tree, and JSON/text output.
- Structured typed IR; name resolution, types, construction/quantum/runtime stages,
  readonly effects, helper specialization, return checks, branch/loop flow checks.
- Config validation, signed integer/text encodings, independent small-state oracle,
  and separate hand-constructed Qiskit feasibility probes.
- Latest full run: 173 passed (V004). No source-to-circuit execution yet.

## Commands / environment

```powershell
& C:\ProgramData\anaconda3\python.exe tools/check.py -q
& C:\ProgramData\anaconda3\python.exe tools/qutes.py analyze tests/acceptance/A004_snapshots.qut --quint-bits 4
```

Use `parse` for syntax only; `analyze --json` for typed IR. `--config FILE` loads
explicit project settings. Neither command proves automatic-cleanup safety.
Python 3.13.5 / Qiskit 2.3.0 / Aer 0.17.2 / NumPy 2.1.3 / pytest 8.3.4 on Windows.
PATH Python aliases are unusable; the explicit interpreter works. No global
packages/settings changed. Runner writes fresh workspace-local artifacts.
Git staging/commits require elevated Git calls in this environment; the user has
already authorized logical commits. No remote or push is authorized.

## Exact next task: T007

Implement bounded construction-time evaluation and function elaboration over the
new typed IR. Preserve parameter scopes, source spans, signed integer conventions,
short-circuit evaluation, fixed array shapes, loop budgets, and readonly borrows.
Quantum and runtime values must remain symbolic; do not simulate them as classical
values. Keep the resulting representation independent of Qiskit and suitable for
version/dependency cleanup analysis (T008). Follow docs/spec and the corpus.

Inspect the current worktree before resuming: the active work batch may be newer
than this checkpoint. Update ledger, evidence, and tasks at each logical boundary.

## Limitations / decisions

- Full `check`, `build`, `run`, and `explain` commands remain unimplemented.
- General cleanup synthesis, construction-time execution, circuit lowering, and
  decoded source results remain pending. Backend probes are not the compiler.
- 17 positive examples pass frontend analysis; 12 semantic negatives produce
  expected diagnostics; 2 cleanup negatives deliberately pass this layer. The 2
  lexical/syntactic failures are diagnosed by the parser/lexer.
- Working builtin names remain defaults. No separate human spec review is claimed.
- Measurement is non-consuming and ordinary self-assignment remains accepted;
  never restore the withdrawn function-only evolution restriction.
- Clean-install/Linux verification is pending. Installed IBM runtime produces
  non-failing deprecation warnings during Qiskit plugin discovery.
