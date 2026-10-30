# Current status

Updated: 2026-10-30, checkpoint KB-002.

## State

- Local Git on main, no remote. Bootstrap commit: `a29edbf`.
- M1 initial specification and backend feasibility checks implemented and passing.
- Working language contract, EBNF, 33 acceptance examples, config and value codecs,
  independent small-state oracle, and Qiskit feasibility experiments exist.
- Latest full test run: 37 passed. See V002; semantic acceptance is not yet run.
- Active task: T005 parser/source locations. No compiler source execution yet.

## Environment and checks

- Windows PowerShell, workspace `C:\Users\gabry\Work\Quantum\qutes_lang_chatgpt`.
- Run: `& C:\ProgramData\anaconda3\python.exe tools/check.py -q`.
- Python 3.13.5; Qiskit 2.3.0; Aer 0.17.2; NumPy 2.1.3; pytest 8.3.4.
- PATH python/py aliases are inaccessible. Global packages were not changed.
- Runner uses workspace-local artifacts because the default pytest temp directory
  failed. No special permissions are needed for the tests.
- Git index/commits require an elevated Git tool call in this environment; user
  already authorized logical commits. No remote/push is authorized.

## Next action

Implement T005 from docs/spec/grammar.ebnf: source spans, lexer, recursive-descent
statements, precedence parser, AST. Parse all positive and semantic-negative corpus
cases, reject only lex/parse negatives at this layer, and test precedence/errors.
Do not lower circuits or silently implement type/staging rules inside the parser.

## Limits and pending decisions

- Builtin spellings are working defaults, not separately confirmed final branding.
- Parameters stay read-only; no mut/ref or function-only evolution proposal.
- Backend cleanup is hand-constructed in experiments, not automatically synthesized.
- No checker, IR, evaluator, source execution, or CLI yet.
- Clean-environment installation, Linux support, and a human specification review
  have not been performed. Pins describe the installed environment actually tested.
- IBM runtime installed on the host emits deprecation warnings during Qiskit
  plugin discovery. They do not fail the tests; do not suppress them without cause.
