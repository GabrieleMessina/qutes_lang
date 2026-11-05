# Write and run Qutes

Qutes lets you express quantum computations using typed values, functions,
assignments, and familiar control flow. Its compiler builds Qiskit circuits and
cleans temporary quantum storage automatically when it can establish a safe
schedule. V1 is a local simulator research implementation. It does not provide
a broad optimization algorithm library or promise a speedup for ordinary code.

## Install and run

Use Python 3.12 or 3.13 in a virtual environment. From the repository:

```text
python -m venv .venv
# Windows: .venv\Scripts\python.exe
# Linux:   .venv/bin/python
python -m pip install ".[backend]"
qutes run examples/measurement_snapshots.qut --shots 32 --seed 7
```

Run the install command using the virtual environment's Python, or activate the
environment first. Nothing needs to be installed globally. `qutes` is installed
in that environment's Scripts/bin directory; `python -m qutes` is equivalent.
For the exactly pinned development environment, follow README.md.

The snapshots example always returns `[5,7]`:

```csharp
quint number = 5;
int before = measure(number);
number = number + 2;
return [before, measure(number)];
```

`measure` returns an ordinary classical value. `number` remains available, and
later operations evolve its post-measurement state. `before` stays 5.
Each simulator shot begins a fresh execution of the whole circuit.

## Scripts, inputs, and shared values

Write executable statements directly in the file. A `main` function is optional
and ordinary: defining it does nothing until you call it. A script returns a
classical result with an explicit `return`; otherwise it has no output value.

```csharp
input int increment;
quint number = 1;

void advance() {
    number += increment;
}

int sample() {
    return measure(number);
}

advance();
return sample();
```

Run with `--inputs FILE.json`, where the file contains, for example,
`{"increment": 2}`. Functions can read and update root variables. Initialize a
variable before calling any function that accesses it. Function definitions can
appear before or after their calls; variables inside blocks remain local.

To migrate a 0.1 program, move main's body to the top level and turn each parameter
into an `input` declaration. Rebuild generated Python with `qutes build`: older
artifacts deliberately report an incompatibility error. The preserved legacy
`examples/snapshots.qut` uses an ordinary main declaration; the script tutorial is
`examples/measurement_snapshots.qut`.

## Types and ordinary expressions

| Classical type | Quantum type | Meaning |
| --- | --- | --- |
| `bool` | `qubit` | False/true basis values |
| `int` | `quint` | Signed fixed-width quantum integer; classical integers have a configurable resource bound |
| `char` | `quchar` | One character in the configured quantum alphabet |
| `string` | `qustring` | Quantum text with fixed capacity and a separate known logical length |

Declare and initialize together: `quint count = 3;`, `quchar letter = 'A';`,
`qustring word = "HI";`. Arrays have fixed lengths: `quint[] values = [1,2,3];`
or `quint[] values = new quint[3];`. Elements start at zero; text defaults use
the configured alphabet's first character or the empty string.

`number = number + 2` and `number += 2` are supported. At four bits, `7 + 1`
wraps to `-8`. Initialization outside `-8..7` is an error. `rotateLeft(number,1)`
and `rotateRight(number,1)` rotate bits; they do not discard shifted-out bits.
Quantum multiplication, division, general subtraction, and resizing are deferred.
Adding a negative classical constant is supported.

`quint number = superposition();` prepares all representable values with equal
amplitudes. Computation preserves the joint quantum state until observation.
`quint copy = number;` creates a correlated basis-value copy; it does not create
an independent arbitrary quantum state. Preparing superpositions is currently
available for qubit/quint initialization, not arbitrary text distributions.

## Functions, branches, and loops

Functions are top-level, with explicit parameter and return types:

```csharp
quint next(quint value) {
    return value + 1;
}
```

Parameters are read-only: return a result and assign it at the call site.
The compiler diagnoses parameter writes. Quantum parameters borrow their input
without an implicit copy. Functions may measure; the compiler infers this effect
through calls and rejects it in conditional bodies. Measurement changes the
post-measurement state even though the parameter binding is read-only.

An `if` over quantum values preserves coherence and applies controlled
operations behind the scenes. It must not change the values used by its condition.
An `if` over a measured snapshot controls subsequent operations using that
recorded classical result. Both forms use ordinary braces and `else`.

```csharp
qubit choice = superposition();
bool selected = measure(choice);
qubit result = false;
if (selected) {
    result = true;
}
```

`for` and `while` run during circuit construction and have bounded expansion.
Their conditions, array indices, array sizes, and rotation counts must be
construction-time classical values. `foreach` reads array elements; its iteration
variable is read-only. Measurement-driven or quantum-controlled loops are deferred.
General arithmetic on measured results and measurement inside branches are also
deferred. Observe first, then use snapshots in comparisons/Boolean conditions.

## Automatic cleanup and diagnostics

Local temporaries are cleaned at scope exit; callers receive owned function
results. You do not write inverse operations or manual cleanup calls. The compiler
tracks which version of each value produced a temporary and may temporarily
reconstruct an older input to clean it.

Some familiar assignments cannot be supported safely. For example, replacing an
unknown superposition with `number = 0` would erase information, and `number +=
number` is not an ordinary reversible in-place addition. These receive `Q3001`.
The compiler never inserts hidden measurement or reset to make them work.

The script's explicitly named quantum values remain live until the shot ends. Cleaned
wires are still reserved in V1 to allow historical recomputation, so a temporary
can increase the reported qubit count even after it is cleaned.

Use `qutes check FILE` for complete compilation checks and `qutes explain FILE`
to inspect storage, snapshots, cleanup counts, and estimated circuit size.
Diagnostics include a stable category, source excerpt, caret, and relevant hints.
Parsing can report up to ten errors together; invalid programs never run. `--json` provides
structured results. See [all categories](spec/language-v0.2.md).

## Configuration and inputs

The CLI reads `qutes.toml` beside the source file only. `--config FILE` selects
another file; command-line overrides win. The Python API uses explicit config
or defaults and does not discover files.

```toml
[qutes]
quint_bits = 4
alphabet = " ABCDEFGHIJKLMNOPQRSTUVWXYZ"
qustring_capacity = 2
max_simulation_qubits = 24
max_simulation_shots = 1000000
```

Defaults are four-bit quint, alphabet `ABC`, text capacity two, 24 simulator
qubits, and at most one million shots per call. Construction limits are 10,000
loop iterations, 100,000 evaluation/expansion work units, and 65,536 classical
integer bits. Each limit is configurable. Resource diagnostics do not wrap values
or silently truncate work. Statevector memory alone grows as `16 * 2^qubits`
bytes; backend overhead is additional. Reports count reserved wires and gate
applications before device decomposition, not physical hardware costs.

Declare external values at the top level, for example `input int count;`.
Supply them through a JSON object:

```text
qutes run examples/loops.qut --inputs examples/inputs.json --shots 16 --seed 7
qutes explain examples/loops.qut --inputs examples/inputs.json --json
```

## Print or save the circuit

The full compiler commands (`check`, `build`, `run`, and `explain`) accept these
options, individually or together:

```text
qutes check examples/measurement_snapshots.qut --print-circuit
qutes build examples/measurement_snapshots.qut --save-circuit artifacts/circuits
qutes run examples/feedforward.qut --print-circuit --save-circuit artifacts/circuits --circuit-format svg
```

`--print-circuit` prints a text diagram. `--save-circuit FOLDER` creates the folder
if needed and saves a PNG; use `--circuit-format svg` for a scalable image. Image
export requires the optional visualization libraries:

```text
python -m pip install ".[backend,visualization]"
```

Use your virtual environment's Python. Console diagrams only require Qiskit;
normal checking/Python generation still do not require a backend installation.
Image export is headless and does not open windows or require a LaTeX installation.

Each compilation has one circuit for its bound script inputs. Files are named
`SOURCE-BUILDHASH-VIEWHASH.png` (or `.svg`), so different inputs/settings can share a folder.
Repeating the same build and view replaces that image atomically. Other files remain intact.
With `--json`, text diagrams go to stderr, and stdout includes the image path in
`circuit_diagram.image` alongside the normal JSON result.

Both views default to named source-level operation/function boxes. Use `--unfold 1`
(or another depth), `--unfold all`, and optionally `--unfold-only compare,myFunction`
to reveal detail. `explain` lists selectors. Measurement/runtime branches remain
visible, and cleanup markers identify zeroed wires separately from restored inputs.
Markers exist only in diagrams. Direct/generated executable circuits keep their
operation structure and receive named registers. The [CLI walkthrough](cli-walkthrough.md)
shows every command and view option. Drawing does not run extra simulations. `run` renders after a successful execution; `check`
lets you inspect a circuit without executing it. Idle/reserved wires remain visible.
Images fold long circuits into rows; excessive image dimensions receive Q4001
(40 million estimated pixels or 32,000 pixels on either side at 120 dpi).
Use console output to inspect a circuit that exceeds this image-size bound.

## Generated Python and future pipelines

```text
qutes build examples/loops.qut --inputs examples/inputs.json -o artifacts/loops.py
python artifacts/loops.py --shots 32 --seed 7
```

Create the output directory first. Generation does not need Qiskit installed.
Generated Python contains readable circuit construction, embedded source, settings,
bound inputs, result layout, source/build hashes, versions, and resource metadata.
Existing Qutes-generated outputs are replaced atomically; unrelated files require
an explicit `--force`. The source file is never overwritten.

The module requires the Qutes runtime and Qiskit/Aer to execute. Import it normally
(or with `importlib` for an arbitrary filename) and use:

```python
circuit, layout = module.build(inputs={"count": 3})
results = module.run(inputs={"count": 4}, shots=128, seed=7)
```

Use the names declared by that module's `input` declarations. `None` uses the bound
inputs recorded at build time. New inputs recompile the embedded source, including
loops and array sizes, instead of silently running the old circuit. Each build
returns its own layout; `layout.decode(memory)` decodes an integer representing
the complete classical memory, with bit zero least significant.

`run` returns `outcomes` (value/count/empirical probability), `execution` (shots,
seed, backend, actual dependency versions), and `build` metadata. Counts with the
same decoded return value are combined. Programs with no measurements return
their known classical output with backend `classical-output`; no simulator is
executed. A supplied seed supports reproducibility in a fixed tested environment,
not identical samples across all dependency versions.

The source API is `qutes.compiler.compile_source(source, inputs=..., config=...)`;
the returned compilation exposes `.build()` and `.run()`. These interfaces keep
construction, execution, and decoding separate for later hybrid orchestration.
V1 does not preserve live quantum state across jobs or implement multi-stage
hybrid pipelines, hardware submission, editor tooling, or a large standard library.
