# Write and run Qutes

Qutes lets you express quantum computations using typed values, functions,
assignments, and familiar control flow. Its compiler builds Qiskit circuits and
cleans temporary quantum storage automatically when it can establish a safe
schedule. V1 is a local simulator research implementation. It does not provide
a search/optimization algorithm library or promise a speedup for ordinary code.

## Install and run

Use Python 3.12 or 3.13 in a virtual environment. From the repository:

```text
python -m venv .venv
# Windows: .venv\Scripts\python.exe
# Linux:   .venv/bin/python
python -m pip install ".[backend]"
qutes run examples/snapshots.qut --shots 32 --seed 7
```

Run the install command using the virtual environment's Python, or activate the
environment first. Nothing needs to be installed globally. `qutes` is installed
in that environment's Scripts/bin directory; `python -m qutes` is equivalent.
For the exactly pinned development environment, follow README.md.

The snapshots example always returns `[5,7]`:

```csharp
int[] main() {
    quint number = 5;
    int before = measure(number);
    number = number + 2;
    return [before, measure(number)];
}
```

`measure` returns an ordinary classical value. `number` remains available, and
later operations evolve its post-measurement state. `before` stays 5.
Each simulator shot begins a fresh execution of the whole circuit.

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
without an implicit copy. Helpers cannot measure in V1; main can.

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

Main's explicitly named quantum values remain live until the shot ends. Cleaned
wires are still reserved in V1 to allow historical recomputation, so a temporary
can increase the reported qubit count even after it is cleaned.

Use `qutes check FILE` for complete compilation checks and `qutes explain FILE`
to inspect storage, snapshots, cleanup counts, and estimated circuit size.
Diagnostics include a stable category and source location. `--json` provides
structured results. See [all categories](spec/language-v0.1.md).

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

Defaults are eight-bit quint, ASCII alphabet, text capacity two, 24 simulator
qubits, and at most one million shots per call. Construction limits are 10,000
loop iterations, 100,000 evaluation/expansion work units, and 65,536 classical
integer bits. Each limit is configurable. Resource diagnostics do not wrap values
or silently truncate work. Statevector memory alone grows as `16 * 2^qubits`
bytes; backend overhead is additional. Reports count reserved wires and gate
applications before device decomposition, not physical hardware costs.

Main accepts classical arguments from a JSON object:

```text
qutes run examples/loops.qut --inputs examples/inputs.json --shots 16 --seed 7
qutes explain examples/loops.qut --inputs examples/inputs.json --json
```

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

Use the parameter names declared by that module's main. `None` uses the bound
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
