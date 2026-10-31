# Current status

Updated: 2026-10-31, checkpoint KB-010. Full implementation goal remains active.

## Completed capabilities

- Local Git main, no remote. Checkpoints: a29edbf knowledge base; 4b8d3d8 contract /
  probes; 18d3d56 parser; e94314a typed frontend; 5ad3bae construction; 0cdd467
  cleanup scheduler; 0115815 scalar lowering/measurement cuts; 6bde5d6 coherent
  branches; 0926943 arrays/text. Current checkpoint adds measured feedforward and
  anonymous main-temporary cleanup.
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
- Runtime snapshot predicates, signed/text/Boolean conditions, mixed quantum and
  classical nesting, guarded overwrite, anonymous helper/argument cleanup.
- Latest full run: 529 passed (V010). All 17 positive examples have exact output
  distributions AND execute on Aer; all 16 negative examples have expected diagnostics.

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

## Exact next task: T012

Read DEVELOPMENT_PLAN.md section 4 and the current lowering/feedforward specs.
Implement check/build/run/explain, readable generated Qiskit Python, resource
reports, deterministic artifacts, and Aer execution with pre-simulation limits.
Generated modules must expose build(inputs) -> (circuit, result layout) and
run(inputs, shots, seed) -> decoded results plus metadata; do not silently freeze
new input bindings to the specialization used when generating the artifact.

Then finish packaging/isolated installation, user docs/examples, Linux CI coverage,
and a requirement-by-requirement release audit. Keep codegen and execution separate
for later hybrid pipelines. Report compiler/language/dependency versions, effective
config, source identity, result layout, and resource estimates. Reserve actual
reuse optimization for a safe last-use allocator or clearly report reserved cost.
R004 and R005 now fail correctly; never regress non-consuming measurement.

Inspect worktree changes before resuming; active work may postdate this checkpoint.
Keep ledger/status/evidence current and commit coherent verified units.

## Limits / completion audit

- Full check/build/run/explain are NOT implemented. Goal is NOT complete.
- Construction is an intermediate representation, not executable Qiskit output.
- Core source features, including measured feedforward, have circuit evidence.
  Generated modules, execution tooling, packaging/release checks remain pending.
- Every positive corpus example executes; this is necessary but not sufficient
  evidence for the release requirements. Allocation still reserves released wires.
- Indirect measurement conservatively invalidates connected roots' preparation;
  erasing such an unobserved root is rejected unless explicitly measured itself.
- String-array element lengths now propagate through construction and lowering,
  including helper borrows, indexed writes, foreach views, branches, and snapshots.
- Some dependency cycles still receive conservative Q3001 diagnostics; conditional
  permutations cannot use unconditional storage-rebinding optimization.
- Builtin spellings remain documented defaults, without a separate human review.
  Readonly parameter behavior remains the original V1 default.
- Never restore measurement consumption or function-only evolution restrictions.
- Short-circuited runtime measurement is deliberately rejected under the existing
  conditional-measurement restriction. Reading snapshots remains supported.
- Clean installation/Linux remain unverified; external IBM runtime emits 100
  non-failing deprecation warnings in existing Qiskit tests.
