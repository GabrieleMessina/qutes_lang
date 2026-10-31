# Current status

Updated: 2026-10-31, checkpoint KB-009. Full implementation goal remains active.

## Completed capabilities

- Local Git main, no remote. Checkpoints: a29edbf knowledge base; 4b8d3d8 contract /
  probes; 18d3d56 parser; e94314a typed frontend; 5ad3bae construction; 0cdd467
  cleanup scheduler; 0115815 scalar lowering/measurement cuts; 6bde5d6 coherent
  branches. Current checkpoint adds quantum arrays/text and their lifetimes.
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
- Quantum arrays, indexing, foreach views, value copies, helper ownership, text
  encoding/decoding, padded strings, element length tracking, collection snapshots.
- Latest full run: 405 passed (V009). Sixteen positive source cases have exact output
  distribution checks; all negative cases have their expected diagnostics.

## Commands / environment

```powershell
& C:\ProgramData\anaconda3\python.exe tools/check.py -q
& C:\ProgramData\anaconda3\python.exe tools/qutes.py construct tests/acceptance/A011_for.qut --quint-bits 4 --json
```

Commands: parse (syntax), analyze (typed IR), construct (expanded symbolic IR).
`--config FILE` and `--quint-bits N` apply to analysis/construction; construct also
accepts `--inputs FILE` for a JSON main-argument object. Construction output is still
explicitly unverified. Use lowering.lower(constructed).to_qiskit() for the supported
subset; docs/spec/lowering.md describes the API and boundaries.

Python 3.13.5, Qiskit 2.3.0, Aer 0.17.2, NumPy 2.1.3, pytest 8.3.4 on Windows.
PATH Python aliases are unusable; explicit Anaconda interpreter works. No global
packages changed. Runner uses ignored workspace-local artifacts and Windows Python
stream capture to avoid Aer native DLL failures under descriptor capture. Git writes need
elevated Git calls; the user already authorized logical commits, not remote pushes.

## Exact next task: T011

Read docs/spec/lowering.md and cleanup-scheduling.md. Add same-circuit feedforward
for runtime comparisons/Boolean expressions. Gate guards need immutable snapshot
expressions in addition to existing single-bit classical controls. Apply the guard
to complete overwrite transformations and disable unconditional array-permutation
rebinding inside classical conditional branches too. Preserve signed comparisons,
out-of-range classical constants, text encoding/length semantics, and nested controls.

Start with A007, then combined runtime predicates, mixed quantum/runtime nesting,
snapshot updates, text/array branches, and generated-circuit execution. Existing
measurement checkpoints and result codecs are integrated. Then add T012 CLI,
serialization, resources, packaging, docs, CI, and complete release audit.
R004 and R005 now fail correctly; never regress non-consuming measurement.

Inspect worktree changes before resuming; active work may postdate this checkpoint.
Keep ledger/status/evidence current and commit coherent verified units.

## Limits / completion audit

- Full check/build/run/explain are NOT implemented. Goal is NOT complete.
- Construction is an intermediate representation, not executable Qiskit output.
- Source coherent branches/predicates and quantum arrays/text have circuit evidence.
  General measured feedforward, execution tooling, and physical reuse remain pending.
- Positive corpus A001-A006/A008-A017 has exact distribution evidence; A007 awaits
  feedforward. All 16 negative examples are diagnosed.
- Indirect measurement conservatively invalidates connected roots' preparation;
  erasing such an unobserved root is rejected unless explicitly measured itself.
- String-array element lengths now propagate through construction and lowering,
  including helper borrows, indexed writes, foreach views, branches, and snapshots.
- Some dependency cycles still receive conservative Q3001 diagnostics; conditional
  permutations cannot use unconditional storage-rebinding optimization.
- Builtin spellings remain documented defaults, without a separate human review.
  Readonly parameter behavior remains the original V1 default.
- Never restore measurement consumption or function-only evolution restrictions.
- Clean installation/Linux remain unverified; external IBM runtime emits 65
  non-failing deprecation warnings in existing Qiskit tests.
