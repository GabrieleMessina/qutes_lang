# Qutes command walkthrough

For a command lookup, see the [command-line reference](reference/cli.md). This walkthrough uses the examples in a source checkout.

Run these commands from the repository root with the project environment installed.
On Windows, use `.\.venv\Scripts\qutes.exe` in place of `qutes`. On Linux, use
`.venv/bin/qutes`. To use the current checkout before reinstalling it, replace
`qutes` with `.\.venv\Scripts\python.exe tools/qutes.py`.

The examples discover their adjacent configuration automatically and stay below
24 qubits. The default tour alphabet is `ABC`. Examples 22 and 30 store a quantum
wildcard and use the explicit option `--alphabet "AB?"`, which produces QW0001.
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
names. With reuse, exclusive wires keep source names where possible and shared
wires use `work_N`. `reuse` labels identify handoffs; folded blocks show hidden
reuse counts. `explain` lists logical-to-physical intervals and their zero proofs.

Image names include both build and view hashes, so compact and expanded views
coexist. Drawing options do not change build identity or the execution circuit.
Use `qutes.visualization.render(compilation, print_circuit=True, unfold=1,
unfold_only="compare,next", wire_view="physical")` from Python for the same view controls.

Example 12 uses **10 physical qubits** for 19 logical qubits, including 16 cleaned
logical qubits and 7 physical wires free at the end. Statevector storage is **16 KiB**
(8 MiB with reuse disabled). Backend overhead is additional. Cleanup scheduling
and operation order are unchanged; later reconstruction receives a new lifetime.
Reduced width does not guarantee better hardware depth or execution time.

```text
qutes check examples/language/12_quantum_ordering.qut --print-circuit --wire-view logical --unfold 1
qutes explain examples/language/12_quantum_ordering.qut --no-wire-reuse
qutes run examples/language/39_wire_reuse.qut --shots 64 --seed 17
```

The last example returns `-3`, using 6 physical qubits for 39 logical qubits.
`--no-wire-reuse` retains all 39 and cannot run under the default 24-qubit cap.
`--wire-reuse` enables reuse explicitly. These flags override `wire_reuse` in
TOML; Python uses `CompilerConfig(wire_reuse=False)`. Unlike allocation settings,
`--wire-view physical|logical` changes only diagrams/image names, requires diagram
output, and does not change build identity. Empty zero-only locals may disappear
from physical views; logical views retain their cleanup annotations.

Compile success does not imply a large circuit fits the simulator; `run` checks
physical width before and after backend decomposition.

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

## Qutes 2.0.0 walkthrough

These commands also work with `qutes.exe` on Windows. Preparation weights use
explicit JSON real/imaginary components; the Python API additionally accepts
native complex numbers. The inputs remain construction-time values.

```text
qutes parse examples/language/48_numeric_inputs.qut --json
qutes analyze examples/language/43_qft_inverse.qut --json
qutes construct examples/language/40_array_references.qut --json
qutes check examples/language/41_bell_gates.qut --print-circuit --unfold 1
qutes explain examples/language/49_returned_slice.qut --json
qutes build examples/language/48_numeric_inputs.qut --inputs examples/language/48_numeric_inputs.json -o artifacts/weighted.qiskit.py
qutes run examples/language/48_numeric_inputs.qut --inputs examples/language/48_numeric_inputs.json --shots 64 --seed 17 --json
python artifacts/weighted.qiskit.py --shots 64 --seed 17
qutes check examples/language/43_qft_inverse.qut --save-circuit artifacts/tour-circuits --circuit-format png
```

`analyze` cannot prove quantum index bounds without construction inputs; `check`
does. `construct` includes the conservative support information used for those
proofs. `explain` identifies retained backing qubits for slices. The QFT image
folds functions; use `--unfold 1 --unfold-only qft` to expose that function.
Schema-5 modules can respecialize inputs. Schema-3/4 modules execute cached inputs
only: review array copies and rebuild before changing those inputs under 0.4.
