# Current status

## Active 0.4 implementation (2026-11-20)

T025-T028 checkpoints complete; T029 ACTIVE: version/artifact migration, examples,
documentation, safety audit and complete Windows/Linux/package validation.
Target contract docs/spec/language-v0.4.md. Current code adds float/complex,
readonly/mut, array references and copy, returned views/full backing retention,
indexed foreach, ranges and mutable/read-only slices. New source semantics are
in development; package/artifact labels remain0.3/4 until T029 version migration.
Do not distribute a release or claim the full0.4 plan is delivered yet.

Windows full932 passed (run-tdlfjb20); subsequent focused97 and126 passed after
nested-rebind/normalization/resource guards. Linux focused25 passed. Parser
reproduction passes. Live gates/atomic cleanup now pass177 focused tests (KB027/V027), including
Bell, QFT and teleportation with external entanglement. Next: sparse explicit
preparation and signed subtraction/negation are now complete (KB028/V028).
Bounded quantum indexing now complete (KB029/V029). Use tools/check.py/tools/qutes.py;
installed wheels remain0.3. Preserve both untracked root example12 PNGs and
snapshots.qut. See latest ledger/validation and git log for checkpoint commit.

## Previous completed release

Updated: 2026-11-06, checkpoint KB-025. T024 wire reuse COMPLETE.
Language 0.3; package 0.3.0.dev0; generated artifact schema 4 (v3 adapter retained).
Active contracts: [language](../spec/language-v0.3.md),
[wire allocation](../spec/wire-allocation.md), [audit](../wire-reuse-audit.md).

## Delivered

- Certified-zero wire reuse after complete cleanup scheduling, enabled by default.
  Per-bit lifetimes handle reconstruction; no new gates, reset or measurement.
- `--wire-reuse`/`--no-wire-reuse`, TOML and Python Boolean setting; physical-width
  resource/simulation guards, explicit logical/physical mapping and proof metadata.
- Default physical diagrams with stable work_N names and handoff annotations;
  `--wire-view logical` retains source storage. Folding/unfolding, cleanup and
  PNG/SVG continue in both views. View settings do not change build identity.
- Direct/generated execution, changed inputs, schema-3 cached artifacts supported.
  Rebuild old modules for reuse; old modules respecialize using current compiler.
- Previous scripts/ANTLR/globals, in/search, automatic cleanup, non-consuming
  measurement, circuit readability and wildcard guidance remain available.
- 39 runnable tour examples, largest physical width 15, all under 24. Example12:
  19->10 wires, unchanged 29 operations, 8MiB->16KiB. Example39: 39->6 wires.

## Evidence

Full Windows **907 passed**, 78.79s, run-917rvzk8; Debian/WSL **907 passed**,
96.02s, run-hh5g0qad. Installed wheel/CLI/generated modules/reuse/logical-view
smokes pass both. Core-only Java-free compile/codegen passes. Parser check and
all 17 CLI walkthrough commands pass. See V025 for exact commands and limitations.
Installed wheels are current in Windows .venv and artifacts/linux-venv.

## Resume commands

```powershell
.venv/Scripts/qutes.exe explain examples/language/12_quantum_ordering.qut
.venv/Scripts/qutes.exe check examples/language/12_quantum_ordering.qut --print-circuit --wire-view logical --unfold 1
.venv/Scripts/qutes.exe run examples/language/39_wire_reuse.qut --shots 64 --seed 17
.venv/Scripts/python.exe tools/check.py -q
.venv/Scripts/python.exe -I tools/verify_install.py
```

Use tools/qutes.py for checkout execution after future edits. Windows pip/build/
parser commands need TEMP/TMP set to workspace artifacts/install-temp. Linux uses
Debian WSL and artifacts/linux-venv/bin/python under the /mnt/c workspace path;
Git/WSL writes use normal approval review. Backend pins are unchanged: Qiskit 2.3.0,
Aer 0.17.2, NumPy 2.1.3, ANTLR 4.13.2, Python 3.13.5.

## Handoff and limits

No blockers or required work remains for T024. Next action: take a new user request,
inspect git/knowledge base and active contract. Do not start deferred scheduling,
dirty-ancilla, routing or hardware work without scope. Reduced width may constrain
parallelism and does not promise faster hardware execution. No hardware/hosted CI,
Python 3.12 or independent human review claimed. Search guarantees still require
matches per data branch; impossible cleanup remains Q3001.

Preserve user defaults (4-bit quint, alphabet ABC), snapshots.qut (ordinary main
function without automatic execution), .gitignore changes and the untracked root
12_quantum_ordering-1c59c0354694-64eeb63a.png. No remote/push was added. All changes
are local coherent checkpoints. Historical experiments/validation remain in LEDGER
and VALIDATION; they are not the current implementation status.
