# Current status

Public release checkout on codex/qutes-0.4-release. Package 0.4.0, language 0.4, schema 5. T030 integrates the validated rewrite from e1c78a8; T031 is browser proof, preview and publication. The following 0.4 compiler handoff is historical.


Updated 2026-11-20, KB030/V030. **Qutes 0.4 complete**, T025-T029 DONE.
Language 0.4; package 0.4.0.dev0; generated artifact schema 5. Active contract:
[language 0.4](../spec/language-v0.4.md), [delivery audit](../v04-audit.md).

## Delivered

- Mutable reference arrays and slices, explicit copy, readonly capabilities,
  mut scalar/array parameters, caller-visible rebinding and concrete borrow checks.
- Float/complex arithmetic, inputs/arrays/outputs and JSON/Python complex codec.
- hadamard/not/phaseFlip/phase/swap; coherent if and measured feedforward controls.
- Sparse reversible qubit/quint preparation with probabilities/complex amplitudes;
  signed subtraction/negation, indexed foreach, ranges and proven-bounds coherent reads.
- Phase-aware atomic cleanup safeguards, private-component inverse cleanup,
  retained slice backing and certified-zero wire reuse. No hidden reset/measurement.
- Schema 5 generation; cached 3/4 modules execute original inputs but require source
  review/rebuild before changed inputs. Array assignment now shares storage.
- 50 runnable tour examples, maximum 15 physical qubits; new examples 40-50 use 0-12.
  Guide, specification, grammar summary, CLI walkthrough and roadmap updated.

## Final evidence

- Windows full **1032 passed**, 83.44s, run-f40mx194.
- Debian/WSL full **1032 passed**, 123.51s, run-s0dkm8xk.
- 26 documented CLI commands, parser reproduction, PNG/SVG/console diagrams,
  generated/direct execution, changed inputs, reuse and independent phase/correlation
  tests pass. QFT PNG visually inspected.
- Installed 0.4 wheels verified independently of checkout imports on Windows/Linux;
  pip check passes. Core-only compilation/codegen passes with empty PATH and no Qiskit.
- Wheel matches all 45 Python source files; source-distribution coverage checked.
  Exact commands, hashes, failed attempts and limitations are in V030/LEDGER.

## Resume and handoff

No required work or blockers remain for this increment. Next action: read this KB,
inspect git status/log, then take a new user request. Do not start deferred hybrid,
hardware or cleanup-rescheduling work without scope. Commits are local; no push.
Use the checkout runner after editing; installed wheels currently match 0.4 source.

```powershell
.venv/Scripts/python.exe tools/qutes.py run examples/language/41_bell_gates.qut --shots 64 --seed 17
.venv/Scripts/python.exe tools/qutes.py run examples/language/48_numeric_inputs.qut --inputs examples/language/48_numeric_inputs.json --shots 64 --seed 17
.venv/Scripts/python.exe tools/check.py -q
.venv/Scripts/python.exe -I tools/verify_install.py
.venv/Scripts/python.exe tools/verify_walkthrough.py
```

Windows build/install/parser commands need TEMP/TMP set to workspace
artifacts/install-temp. Linux uses Debian WSL and artifacts/linux-venv/bin/python
under /mnt/c/Users/gabry/Work/Quantum/qutes_lang_chatgpt. Git/WSL commands use normal
approval review. Python 3.13.5; ANTLR 4.13.2, Qiskit 2.3.0, Aer 0.17.2, NumPy 2.1.3.

Bounds and cleanup proofs are intentionally conservative. Unknown index bounds
or incompatible unitary cleanup fail deliberately. No hardware/hosted CI run,
Python 3.12 execution or independent human review claimed. Whole-array gate
broadcasting, quantum writes, runtime loops and text-state preparation remain deferred.

Preserve examples/snapshots.qut, user config/.gitignore and both untracked root
12_quantum_ordering PNGs. They were not modified in 0.4. Build products/environments
stay ignored. Historical 0.3 status and evidence remain in the ledger/validation.
