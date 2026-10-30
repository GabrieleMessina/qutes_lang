# Current status

Updated: 2026-10-30, checkpoint KB-006. Full implementation goal remains active.

## Completed capabilities

- Local Git main, no remote. Checkpoints: a29edbf knowledge base; 4b8d3d8 contract /
  probes; 18d3d56 parser; e94314a typed frontend; 5ad3bae construction. Current
  checkpoint adds the independently tested cleanup scheduler and gate adapter.
- Parser, source diagnostics, typed IR, name/type/stage/effect analysis.
- Bounded construction-time evaluator: classical inputs/functions/loops, inlining,
  fresh symbols, scopes, ownership moves, symbolic quantum operations and snapshots.
- Config/value codecs, independent small-state oracle, hand-built Qiskit probes.
- Backend-independent operations and version-aware cleanup scheduler; Qiskit
  reversible gate adapter, including controlled addition/rotation/copy.
- Latest full run: 267 passed (V006). No source-generated circuit execution yet.

## Commands / environment

```powershell
& C:\ProgramData\anaconda3\python.exe tools/check.py -q
& C:\ProgramData\anaconda3\python.exe tools/qutes.py construct tests/acceptance/A011_for.qut --quint-bits 4 --json
```

Commands: parse (syntax), analyze (typed IR), construct (expanded symbolic IR).
`--config FILE` and `--quint-bits N` apply to analysis/construction; construct also
accepts `--inputs FILE` for a JSON main-argument object. Cleanup is explicitly
unverified. Use API modules for detailed inspection.

Python 3.13.5, Qiskit 2.3.0, Aer 0.17.2, NumPy 2.1.3, pytest 8.3.4 on Windows.
PATH Python aliases are unusable; explicit Anaconda interpreter works. No global
packages changed. Runner uses ignored workspace-local artifacts. Git writes need
elevated Git calls; the user already authorized logical commits, not remote pushes.

## Exact next task: T008

Read docs/spec/construction-ir.md and docs/spec/cleanup-scheduling.md. Integrate
construction.py output with cleanup.Scheduler and gates.Gate. The scheduler already
handles input-version restoration, released basis-value recomputation, cyclic
rejection, and basis-value overwrite. Physical wires remain reserved after release.
It does NOT yet understand measurement checkpoints or whole source programs.

Start source integration with scalar arithmetic and the two pending cleanup-negative corpus cases
(R004 unknown overwrite, R005 overlapping doubling). Verify scoped computed
scratch cleanup and full complex states independently, including entangled inputs.
Then integrate coherent branches/loops/functions (T009), array/text layouts
(T010), and measurement/feedforward/results (T011). Do not substitute hand-written
inverse experiment circuits for an automatic compiler cleanup schedule.

Inspect worktree changes before resuming; active work may postdate this checkpoint.
Keep ledger/status/evidence current and commit coherent verified units.

## Limits / completion audit

- Full check/build/run/explain are NOT implemented. Goal is NOT complete.
- Construction is an intermediate representation, not executable Qiskit output.
- Cleanup scheduling and reversible arithmetic have independent circuit evidence;
  source integration, lifetime-aware physical reuse, branch cleanup, measurement
  boundaries, and result decoding still need implementation.
- Positive corpus has frontend/construction coverage, not full execution. Cleanup
  negative cases intentionally pass until the cleanup phase.
- Quantum string-array element lengths need complete layout/lifetime handling in
  T010; basic scalar text codecs and construction are not that full integration.
- Builtin spellings remain documented defaults, without a separate human review.
  Readonly parameter behavior remains the original V1 default.
- Never restore measurement consumption or function-only evolution restrictions.
- Clean installation/Linux remain unverified; external IBM runtime emits 63
  non-failing deprecation warnings in existing Qiskit tests.
