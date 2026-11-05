# Current status

Updated: 2026-11-05, checkpoint KB-022. Circuit readability increment COMPLETE.
T021-T023 delivered; T024 physical wire reuse remains explicitly deferred.
Named registers, source/alias ranges, compact diagrams, selective unfolding,
cleanup annotations, resource units, wildcard warnings and CLI guidance are ready.
T020 delivers 38 independent examples, all executed within 24 qubits (maximum 21).
User-authorized config.py, .gitignore and snapshots.qut edits are included unchanged.
Current defaults: 4-bit quint and alphabet ABC. The tour explicitly uses 3-bit/AB?.
Package: 0.3.0.dev0. Language: 0.3. Generated artifact schema: 3.
Active contract: [language-v0.3](../spec/language-v0.3.md), extending 0.2.

## Delivered

- Coherent `in` for scalar membership and contiguous sequences, including strings,
  character arrays, whole text entries, left-side `?` wildcards and quantum patterns.
- Strings support character foreach. Membership evaluates operands once in order,
  respects logical lengths, protects predicate dependencies and cleans scratch.
- `search(collection, oracle)` accepts a named pure one-element qubit predicate,
  searches collection positions, and returns the selected quantum value. Matching
  probabilities are amplified automatically; measurement remains explicit.
- Yoder-Low-Chuang fixed-point schedule, configurable failure probability 0.01,
  exact non-power-of-two index preparation, honest linear-access resource reports.
- Owned retained indices and zeroed oracle workspace; replayable preparations with
  captured input versions; moves/returns, partial observation and guarded cleanup.
- RY/phase operations in backend-neutral gates, Qiskit execution and generated code.
- CLI/API, console diagrams, PNG/SVG export, generated build/run and changed-input
  specialization retained. Artifact v1/v2 imports fail with actionable rebuild errors.
- Existing ANTLR diagnostics, scripts, inputs/globals, ordinary main, readonly
  parameters, coherent control, classical loops and non-consuming measurement remain.

## Validation

- KB-022: full Windows **858 passed**, 58.95s (run-vojkmdco); Debian/WSL
  **858 passed**, 82.16s (run-3uds1wvr). Final wheel installed/smoke-tested on both;
  source/wheel contents verified. See V022 and ../readability-audit.md.
- Diagram full-operator/phase tests, quantum collection statevectors, scratch,
  dynamic measurement execution, image variants, budgets, aliases and legacy-v3
  modules pass. All 38 tour examples still execute within 24 qubits (maximum 21).

- KB-019: full Windows suite **814 passed**, 63.61s (run-dn9pqzbu); full Debian/WSL
  suite **814 passed**, 85.09s (run-372bgprl). Includes all 38 examples at 64 shots,
  seed 17. Tour guide links/counts and documented CLI inputs/config verified.
- V019 records current validation. The following packaging evidence is from KB-018;
  installed wheels were not rebuilt for the later user default changes.

- Full Windows Python 3.13.5 suite: **775 passed**, 52.95s;
  artifacts/checks/run-nou9xgzv.
- Full Debian/WSL Python 3.13.5 suite: **775 passed**, 71.23s;
  artifacts/checks/run-2nwmk3_m.
- Includes independent complex reference-entangled membership/search checks,
  Chebyshev success bounds, duplicate/no-match branches, zero scratch, input-version
  cleanup, effect/alias rejection, budgets, CLI diagrams and generated phase parity.
- Final installed Windows/Linux wheel smoke checks and dependency checks pass.
  Core-only install compiles with empty PATH and no Java/Qiskit; run reports Q5001.
- Pinned ANTLR regeneration check passes. Wheel matches all 33 compiler modules.
  Source distribution includes grammar, specs, examples, tests and regeneration tool.
- See V018 and release-audit.md for commands, intermediate failures and exact limits.

## Resume and demo commands

```powershell
& .\.venv\Scripts\python.exe tools/qutes.py run examples/language/33_search_strings.qut --shots 64 --seed 17
& .\.venv\Scripts\qutes.exe explain examples/search_numbers.qut
& .\.venv\Scripts\qutes.exe check examples/search.qut --alphabet AB --print-circuit
& .\.venv\Scripts\python.exe tools/check.py -q
& .\.venv\Scripts\python.exe -I tools/verify_install.py
$env:TEMP = Join-Path $PWD 'artifacts/install-temp'; $env:TMP = $env:TEMP
& .\.venv\Scripts\python.exe tools/generate_parser.py --jar artifacts/antlr/antlr-4.13.2-complete.jar --java "C:/Program Files/Android/openjdk/jdk-21.0.8/bin/java.exe" --check
```

Always set workspace-local TEMP/TMP for Windows pip/build/parser operations.
Linux environment: artifacts/linux-venv/bin/python under Debian WSL, workspace
/mnt/c/Users/gabry/Work/Quantum/qutes_lang_chatgpt. WSL/Git writes use normal approval
review. Backend pins remain Qiskit 2.3.0, Aer 0.17.2, NumPy 2.1.3, ANTLR 4.13.2.

## Handoff and limitations

T017-T023 are DONE. No required work remains for the approved readability plan.
For the next request, inspect git status/log and the active contract before editing.
Do not restore automatic main execution or consuming measurement.

The user-authorized snapshot experiment is included as supplied: it defines main
without calling it, so produces no output. grammar/.antlr is now ignored. No remote
was added and nothing was pushed. For examples start at examples/language/README.md.
Current wheel is installed in both project Windows and Debian environments.
Try `.venv/Scripts/qutes.exe check examples/language/12_quantum_ordering.qut
--print-circuit --unfold 1`; add `--unfold-only compare` to select comparisons.
See docs/cli-walkthrough.md for all modes and render APIs. No blockers. Next action:
take a new user request; do not begin deferred T024 without new authorization.

The 99% ideal success bound requires a match in the relevant data branch. No-match
branches can return nonmatching candidates. Quantum data can become entangled with
results. Search strings require equal entry lengths; no runtime indices, mixed
quantum lengths, custom domain preparation, hybrid retries or match enumeration.
Observed local selection state may be impossible to clean and fails explicitly.
Physical work wires remain reserved; large circuits may exceed simulation limits.
No hardware validation, human review, formal proof, or hosted CI run is claimed.
Python 3.12 is configured in CI but has not been locally tested.
