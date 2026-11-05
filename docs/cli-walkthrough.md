# Qutes command walkthrough

Run these commands from the repository root with the project environment installed.
On Windows, use `.\.venv\Scripts\qutes.exe` in place of `qutes`. On Linux, use
`.venv/bin/qutes`. To use the current checkout before reinstalling it, replace
`qutes` with `.\.venv\Scripts\python.exe tools/qutes.py`.

The examples discover their adjacent configuration automatically and stay below
24 qubits. Their intentional `?` alphabet entry produces a nonfatal QW0001 warning.
Warnings go to stderr; `--json` includes structured warnings in its JSON output.

| Command | When to use it | What success establishes |
| --- | --- | --- |
| `parse` | Inspect syntax and AST | Syntax only; no type or quantum safety checks |
| `analyze` | Inspect names, types, stages and effects | No construction bounds or cleanup verification |
| `construct` | Inspect expanded loops and inlined calls with inputs | No cleanup verification |
| `check` | Validate a complete program without simulation | Types, construction bounds and cleanup |
| `explain` | Understand storage, cleanup and resource costs | Complete compilation, with resource estimates |
| `build` | Generate a reusable Qiskit Python module | Complete compilation; no simulation |
| `run` | Sample decoded classical outputs | Compilation and bounded local simulation |

```text
qutes parse examples/language/06_functions_globals.qut --json
qutes analyze examples/language/07_inputs.qut --json
qutes construct examples/language/07_inputs.qut --inputs examples/language/07_inputs.json --json
qutes check examples/language/12_quantum_ordering.qut
qutes explain examples/language/12_quantum_ordering.qut
qutes build examples/language/10_quantum_addition.qut -o artifacts/tour.qiskit.py
qutes run examples/language/10_quantum_addition.qut --shots 64 --seed 17
qutes run examples/language/07_inputs.qut --inputs examples/language/07_inputs.json --shots 64 --seed 17
```

The addition example returns `[3,1,3]`. The input example returns six true values.
`analyze` needs no input bindings; `construct` and the full compiler commands do.
Use `--config FILE` or individual overrides when exploring different encodings.

## Circuit diagrams

The full compiler commands accept `--print-circuit` and `--save-circuit FOLDER`.
Images require the visualization extra; no simulator is run to draw a circuit.

```text
qutes check examples/language/12_quantum_ordering.qut --print-circuit
qutes check examples/language/15_coherent_if.qut --save-circuit artifacts/tour-circuits --circuit-format svg
qutes check examples/language/12_quantum_ordering.qut --print-circuit --unfold 1
qutes check examples/language/15_coherent_if.qut --print-circuit --unfold all
qutes check examples/language/24_quantum_functions.qut --print-circuit --unfold 1 --unfold-only next
```

The default view folds source operations/functions into boxes. `--unfold N`
opens N levels, first source blocks and then Qiskit definitions. `all` opens all
definitions to elementary gates (typically U and CX). Measurements and runtime
branches remain visible, even in functions. `--unfold-only compare,next` selects
operation kinds or named functions; enclosing paths open while unrelated siblings
stay folded. `explain` lists selectors. Every matching occurrence is selected,
including named oracle calls inside search and their labeled inverse operations.

`clean |0>` marks wires restored to zero; `inputs restored` marks touched dependency
wires returned to their earlier state. These markers are diagram annotations,
not executable resets or barriers. A folded parent reports its internal cleanup
count; unfold it to see the timing and wires. Inverse oracle cleanup is shown as
recomputation and is never incorrectly labeled as zeroing.

Register names identify physical storage. `explain` shows other source names and
their operation ranges: aliases, readonly parameters and returned values do not
necessarily get independent wires. Array entries and repeated locals use unique
names; search keeps separate value, index and workspace register names.

Image names include both build and view hashes, so compact and expanded views
coexist. Drawing options do not change build identity or the execution circuit.
Use `qutes.visualization.render(compilation, print_circuit=True, unfold=1,
unfold_only="compare,next")` from Python for the same view controls.

Example 12 reserves 19 qubits, 16 eventually cleaned, and needs **8 MiB** for the
statevector alone. Cleanup restores temporary storage to zero, but the current
allocator does not reuse those wires: later cleanup may reconstruct an older value.
Backend overhead is additional. Compile success does not imply a large circuit
fits the simulator; `run` checks the limit before and after backend decomposition.

## Generated modules

After the `build` command above, run the generated module with the environment's
Python executable:

```text
python artifacts/tour.qiskit.py --shots 64 --seed 17
```

For Python integration, load that module with `importlib.util.spec_from_file_location`
and call `build()` for `(circuit, result_layout)` or `run(shots=64, seed=17)` for
decoded outcomes. Both accept `inputs={...}` to specialize an input-using program.
Generated artifacts keep their bound inputs, compiler settings and result layout.
See [the guide](guide.md#generated-python-and-future-pipelines) for API examples.
