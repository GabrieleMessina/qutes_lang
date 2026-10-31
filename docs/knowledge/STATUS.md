# Current status

Updated: 2026-10-31, checkpoint KB-008. Full implementation goal remains active.

## Completed capabilities

- Local Git main, no remote. Checkpoints: a29edbf knowledge base; 4b8d3d8 contract /
  probes; 18d3d56 parser; e94314a typed frontend; 5ad3bae construction; 0cdd467
  cleanup scheduler; 0115815 scalar lowering and measurement cuts. Current checkpoint
  adds signed predicates and coherent branches.
- Parser, source diagnostics, typed IR, name/type/stage/effect analysis.
- Bounded construction-time evaluator: classical inputs/functions/loops, inlining,
  fresh symbols, scopes, ownership moves, symbolic quantum operations and snapshots.
- Config/value codecs, independent small-state oracle, hand-built Qiskit probes.
- Backend-independent operations and version-aware cleanup scheduler; Qiskit
  reversible gate adapter, including controlled addition/rotation/copy.
- Scalar source-to-Qiskit lowering: qubit/quint arithmetic, self-updates, scopes,
  helper ownership, expanded loops, explicit measurement snapshots and cleanup.
- Signed comparisons, compound Boolean predicates, coherent if/else, conditional
  overwrite, nested controls, branch-local arithmetic and cleanup.
- Latest full run: 377 passed (V008). Eleven positive source cases have exact output
  distribution checks; all negative cases have their expected diagnostics.

## Commands / environment

```powershell
& C:\ProgramData\anaconda3\python.exe tools/check.py -q
& C:\ProgramData\anaconda3\python.exe tools/qutes.py construct tests/acceptance/A011_for.qut --quint-bits 4 --json
```

Commands: parse (syntax), analyze (typed IR), construct (expanded symbolic IR).
`--config FILE` and `--quint-bits N` apply to analysis/construction; construct also
accepts `--inputs FILE` for a JSON main-argument object. Construction output is still
explicitly unverified. Use lowering.lower(constructed).to_qiskit() for the scalar
subset; docs/spec/lowering.md describes the API and boundaries.

Python 3.13.5, Qiskit 2.3.0, Aer 0.17.2, NumPy 2.1.3, pytest 8.3.4 on Windows.
PATH Python aliases are unusable; explicit Anaconda interpreter works. No global
packages changed. Runner uses ignored workspace-local artifacts and Windows Python
stream capture to avoid Aer native DLL failures under descriptor capture. Git writes need
elevated Git calls; the user already authorized logical commits, not remote pushes.

## Exact next task: T010

Read docs/spec/lowering.md and cleanup-scheduling.md. Integrate quantum arrays,
quchar/qustring layout, indexing, foreach views, text length metadata, value copies,
and lifetime handling. Scalar predicates and coherent branches are now integrated.
Physical wires remain reserved after release; histories preserve source/control
versions. Keep string logical length distinct from padded physical capacity.

Start with A013-A017 and add quantum collection copy/alias/branch tests beyond those
examples. Resolve the pending string-array element length construction limitation.
Then finish feedforward/result integration (T011) and release tooling (T012).
R004 and R005 now fail correctly; never regress non-consuming measurement.

Inspect worktree changes before resuming; active work may postdate this checkpoint.
Keep ledger/status/evidence current and commit coherent verified units.

## Limits / completion audit

- Full check/build/run/explain are NOT implemented. Goal is NOT complete.
- Construction is an intermediate representation, not executable Qiskit output.
- Scalar coherent branches/predicates have source circuit evidence. Quantum
  arrays/text, general feedforward/results, and physical reuse remain pending.
- Positive corpus A001-A006/A008-A012 has exact distribution evidence; A007 and
  A013-A017 await source integration. All 16 negative examples are diagnosed.
- Indirect measurement conservatively invalidates connected roots' preparation;
  erasing such an unobserved root is rejected unless explicitly measured itself.
- Quantum string-array element lengths need complete layout/lifetime handling in
  T010; basic scalar text codecs and construction are not that full integration.
- Builtin spellings remain documented defaults, without a separate human review.
  Readonly parameter behavior remains the original V1 default.
- Never restore measurement consumption or function-only evolution restrictions.
- Clean installation/Linux remain unverified; external IBM runtime emits 65
  non-failing deprecation warnings in existing Qiskit tests.
