# Current status

Updated: 2026-10-30, checkpoint KB-003. Read this before resuming work.

## State and completed capabilities

- Local Git on main, no remote. Logical checkpoints: `a29edbf` (knowledge base),
  `4b8d3d8` (M1 contract/feasibility), and the parser commit containing KB-003.
- M1 initial working specification and backend feasibility are implemented.
- T005 parser is complete: spans, lexical diagnostics, immutable AST, functions,
  expressions, arrays, all planned statement syntax, and bounded malformed-input
  handling. Developer command `parse` supports text/JSON output.
- Configuration validation, signed integer/text codecs, independent small-state
  oracle, and separate Qiskit experiments are implemented.
- Latest full run: **102 passed** (V003). Working tree should be clean after the
  checkpoint commit; inspect Git to confirm rather than assuming.

## Run and inspect

```powershell
& C:\ProgramData\anaconda3\python.exe tools/check.py -q
& C:\ProgramData\anaconda3\python.exe tools/qutes.py parse tests/acceptance/A004_snapshots.qut
& C:\ProgramData\anaconda3\python.exe tools/qutes.py parse tests/acceptance/A004_snapshots.qut --json
```

- Windows; Python 3.13.5; Qiskit 2.3.0; Aer 0.17.2; NumPy 2.1.3; pytest 8.3.4.
- PATH python/py aliases are inaccessible. Global packages were not changed.
- Runner uses fresh workspace-local artifacts; host pytest temp directories failed.
- Git index/commit writes need an elevated Git call in this environment. The user
  already authorized logical commits. No remote/push is authorized.

## Exact next work: T006

1. Read docs/spec/language-v0.1.md, grammar.ebnf, and tests/acceptance/cases.json.
2. Add symbol tables/name resolution and explicit classical/quantum/runtime-classical
   types/stages. Define a typed IR separately from the immutable syntax tree.
3. Typecheck operators, initialization, returns, readonly parameters, and builtin
   effects. Preserve source spans and stable diagnostic categories.
4. Activate the relevant semantic-negative corpus cases as checks are implemented.
   Do not claim all positives executable until lowering/execution exists. R004/R005
   require the later cleanup/overlap analysis, not ad hoc parser rejection.
5. Record evidence and update ledger/status/tasks; commit the next coherent unit.

## Boundaries and unresolved details

- `parse` is syntax-only. No `check`, `build`, `run`, or `explain` command yet.
- No typed IR, bounded classical evaluator, cleanup synthesizer, or source-to-Qiskit
  generation exists. Experiment circuits use hand-constructed cleanup.
- 17 positive / 16 negative examples specify the target. Only syntax and manifest
  integrity are executed: 14 semantic-negative cases intentionally still parse.
- Builtin names remain documented working defaults. No separate human specification
  review is claimed. Parameters retain the original read-only V1 default.
- Measurement is non-consuming; ordinary self-assignment remains supported by the
  contract. Do not restore withdrawn function-only evolution or consumption rules.
- Fresh dependency installation and Linux are unverified. The installed host IBM
  runtime emits 63 deprecation warnings during Qiskit plugin discovery; tests pass.
