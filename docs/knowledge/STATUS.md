# Current status

Updated: 2026-11-02, checkpoint KB-015. The approved Qutes 0.2 increment is complete.
Package: 0.2.0.dev0. Language: 0.2. Generated artifact schema: 2.
Active contract: [language-v0.2](../spec/language-v0.2.md).

## Delivered

- ANTLR 4.13.2 lexer/parser with authoritative grammar/Qutes.g4, committed generated
  Python sources, matching runtime, pinned generator SHA256 and CI regeneration check.
- Source excerpts, carets, targeted hints, related opener locations, conservative
  name suggestions and up to ten syntax diagnostics. Recovered input never compiles.
- Ordered top-level statements; ordinary callable main; inferred explicit classical
  script return; empty/function-only files execute no statements and yield void.
- Root input declarations and shared readable/writable globals. Calls check global
  initialization order transitively and specialize against current stages/shapes.
- Measurement helpers and inferred read/write/quantum effects. Non-consuming
  measurement, readonly borrows, predicate protection, dynamic-write restrictions,
  function-local cleanup and script-global shot-end lifetimes are preserved.
- Global state joins across early function returns; skipped static short-circuit
  calls do not change analysis state. Runtime conditional writes/measurement fail.
- Existing arrays/text, addition/rotations, controlled branches, bounded classical
  loops, automatic uncomputation, Qiskit generation and execution remain supported.
- CLI/source/generated-module interfaces retained. Artifact-v2 guards reject old
  generated modules before execution/respecialization. Rebuild after source migration.
- Console circuit diagrams and PNG/SVG export remain supported and tested.

## Verification

- Full isolated Windows Python 3.13.5 suite: **666 passed**, 36.25s,
  artifacts/checks/run-0rphx8ss.
- Full isolated Debian/WSL Python 3.13.5 suite: **666 passed**, 43.38s,
  artifacts/checks/run-ggcdntc3.
- A final diagnostic wording improvement was followed by **50 script tests passed**,
  artifacts/checks/run-9cyfik1r. Behavior is unchanged from the full-suite runs.
- Installed Windows/Linux CLI and generated modules pass new-input respecialization;
  dependency checks pass. Final wheel source bytes match the checkout.
- Core-only install compiles/generates with PATH empty (no Java/Qiskit); execution
  reports Q5001 as intended. Source distribution includes grammar, generator and spec.
- Reproducible ANTLR generation and installed console/SVG output verified. See V015
  for exact commands, artifact paths, earlier failures and testing limits.

## Resume commands

```powershell
& .\.venv\Scripts\qutes.exe run examples/measurement_snapshots.qut --shots 32 --seed 7
& .\.venv\Scripts\qutes.exe check examples/measurement_snapshots.qut --print-circuit
& .\.venv\Scripts\python.exe tools/check.py -q
& .\.venv\Scripts\python.exe -I tools/verify_install.py
& .\.venv\Scripts\python.exe tools/generate_parser.py --jar artifacts/antlr/antlr-4.13.2-complete.jar --java "C:/Program Files/Android/openjdk/jdk-21.0.8/bin/java.exe" --check
```

For package/generator operations set TEMP/TMP to artifacts/install-temp on this host.
Linux environment: artifacts/linux-venv/bin/python under Debian WSL, workspace
/mnt/c/Users/gabry/Work/Quantum/qutes_lang_chatgpt. WSL/Git writes require normal tool
approval review. All commits are local; no remote/push or hosted CI run exists.
Backend pins: Qiskit 2.3.0, Aer 0.17.2, NumPy 2.1.3. Python 3.12 is configured in
CI but not locally tested. Generated files do not imply hardware validation or proof.

## User work and next action

User-modified examples/snapshots.qut is deliberately untouched and uncommitted.
It still defines main; add an explicit call to execute it under 0.2. The canonical
script tutorial/tests use examples/measurement_snapshots.qut. Do not overwrite or
stage the experiment during future work. Inspect git status/log before continuing.

T014-T016 are DONE. No implementation task remains from the approved increment.
Start future work from a new user request. Keep the knowledge base and coherent
commits current; never restore automatic main execution or consuming measurement.

Limits remain: conditional measurement, runtime arithmetic/indices/loops, recursion,
mutable parameters, hardware and multi-stage hybrid orchestration are deferred.
Quantum array-element borrows conservatively protect the whole backing array.
Cleanup can conservatively reject dependency cycles; released wires remain reserved
for historical recomputation. No hidden measurement/reset is used to accept them.
