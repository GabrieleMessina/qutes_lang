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
| `float` | — | Finite construction-time binary64 number |
| `complex` | — | Finite binary64 real/imaginary components |

Declare and initialize together: `quint count = 3;`, `quchar letter = 'A';`,
`qustring word = "HI";`. Arrays have fixed lengths: `quint[] values = [1,2,3];`
or `quint[] values = new quint[3];`. Elements start at zero; text defaults use
the configured alphabet's first character or the empty string.

`number = number + 2` and `number += 2` are supported. At four bits, `7 + 1`
wraps to `-8`. Initialization outside `-8..7` is an error. `rotateLeft(number,1)`
and `rotateRight(number,1)` rotate bits; they do not discard shifted-out bits.
Quantum `a-b`, `-a`, and `a-=b` also wrap; negating the minimum integer returns
that integer. `a-=a` loses information and is rejected; `quint zero=a-a` creates a
separate result. Quantum multiplication/division remain deferred.

`float angle=pi/2.0;` and `complex value=complex(0.6,0.8);` are construction-time
values. Integers widen to floats, and both widen to complex values; narrowing and
float-to-quint conversion are rejected. JSON encodes complex values as
`{"real":0.6,"imag":0.8}`; the Python API also accepts native complex values.
Nonfinite components and division by zero are errors.

`quint number = superposition();` prepares all representable values with equal
amplitudes. Computation preserves the joint quantum state until observation.
`quint copy = number;` creates a correlated basis-value copy; it does not create
an independent arbitrary quantum state. Preparing superpositions is currently
available for qubit/quint initialization, not arbitrary text distributions.

```csharp
quint selected = superposition([1, 3]);
quint weighted = superposition([1, 3], probabilities: [0.25, 0.75]);
qubit phased = superposition([false, true], amplitudes: [complex(0.6, 0), complex(0, 0.8)]);
```

Lists must be nonempty, unique and representable. Use one weighting form with
matching lengths, nonnegative probabilities totaling one, or amplitudes with
squared magnitudes totaling one. Only rounding error up to `1e-12` is normalized.
Preparation initializes new state; it never resets an existing value.

## Arrays, slices and references

`T[]` assignment shares storage. `int[] b=a; b[0]=3;` also changes `a[0]`.
Use `copy(a)` for separate storage; quantum copies correlate basis values.
Array literals and `new T[length]` allocate. `a=[9];` changes that binding's
reference; existing aliases retain the original array. Allocations never resize.
Returning an array or slice shares its reference without an implicit copy.

`qubit[] part=bits[1..3];` is a mutable view of elements 1 and 2, emitting no
copy gates. The bounds must satisfy `0 <= start <= end <= Length`. A slice keeps
its whole backing allocation alive; `explain` reports retained backing qubits.
Dropping a view does not clear shared elements. `string`/`qustring` retain value
semantics; their slices are read-only character views.

`readonly qubit[] view=bits;` forbids rebinding and writes through `view`, including
gate calls or passing it to `mut` parameters. Other mutable aliases can still
change the elements. Explicit measurement remains allowed.

`quint value=values[index];` accepts a quantum integer index for Boolean, integer,
character and equal-length string collections. This is a correlated coherent read,
with no amplification or measurement, and cannot be assigned to. The compiler
must prove every possible signed index in range using finite supports/intervals.
For example, `superposition([0,2])` can index three entries; `superposition()`
usually cannot because it includes negative values. Conservative proofs can reject
safe programs; narrow the preparation/support or use a construction-time index.

## Functions, branches, and loops

Functions are top-level, with explicit parameter and return types:

```csharp
quint next(quint value) {
    return value + 1;
}
```

Parameters are read-only by default. `void advance(mut quint n){n+=1;}` updates
the caller's location. Mutable array parameters can update elements or replace
the caller's binding. A temporary slice can be passed only to a function that
does not rebind that parameter, including through nested helpers. Overlapping
mutable/readonly arguments and global aliases conflicting with active borrows are
rejected; disjoint regions are allowed. Quantum parameters borrow their input
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
Their conditions, array sizes, mutable element indices, and rotation counts must
be construction-time classical values. `foreach(qubit item,int i in bits)` exposes
read-only element and zero-based index bindings. Use `bits[i]` for intended writes,
subject to borrow/control protection. `foreach(int i in 0..bits.Length)` traverses
an ascending half-open static range. Equal endpoints are empty; descending ranges
are rejected. Measurement-driven or quantum-controlled loops are deferred.
General arithmetic on measured results and measurement inside branches are also
deferred. Observe first, then use snapshots in comparisons/Boolean conditions.

## Live operations

`hadamard(q)`, `not(q)`, `phaseFlip(q)`, `phase(q,angle)` and `swap(a,b)` are
statement-only operations on mutable individual qubits. Array elements require
construction-time indices. `not` flips the basis bit in place; `phaseFlip` negates
the true component's amplitude. `phase` multiplies it by `exp(i*angle)` using finite
static radians, including negative inverse angles. `swap` needs distinct qubits.
Use loops for arrays; there is no implicit broadcasting.

`if(alice){not(bob);}` is coherent controlled NOT; `if(alice){phase(bob,pi/2.0);}`
is controlled phase. No measurement occurs. The condition's wires stay protected
through aliases. A measured Boolean condition provides classical feedforward.
See examples 41–43 for Bell preparation, teleportation and QFT plus its inverse.

## Automatic cleanup and diagnostics

Local temporaries are cleaned at scope exit; callers receive owned function
results. You do not write inverse operations or manual cleanup calls. The compiler
tracks which version of each value produced a temporary and may temporarily
reconstruct an older input to clean it.

Basis changes, phases and joint operations can invalidate such reconstruction.
Qutes records these effects atomically and can reverse completely private groups
together. It conservatively rejects independent cleanup through incompatible
effects, external quantum dependencies or destroyed coherence. Some mathematically
valid ancilla schemes therefore remain unsupported; no phase effects are silently
erased. Keep affected values live or restructure the computation when Q3001 occurs.

Some familiar assignments cannot be supported safely. For example, replacing an
unknown superposition with `number = 0` would erase information, and `number +=
number` is not an ordinary reversible in-place addition. These receive `Q3001`.
The compiler never inserts hidden measurement or reset to make them work.

The script's explicitly named quantum values remain live until the shot ends. Certified-zero
work wires are reused by later computations. Historical recomputation starts a new
lifetime and reacquires zeroed wires. Measurement alone never permits reuse.

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
wire_reuse = true
```

Defaults are four-bit quint, alphabet `ABC`, text capacity two, 24 simulator
qubits, and at most one million shots per call. Construction limits are 10,000
loop iterations, 100,000 evaluation/expansion work units, and 65,536 classical
integer bits. Each limit is configurable. Resource diagnostics do not wrap values
or silently truncate work. Statevector memory alone grows as `16 * 2^qubits`
bytes; backend overhead is additional. Reports distinguish logical allocations
from physical wire width and count gates before device decomposition. Set
`wire_reuse = false`, pass `--no-wire-reuse`, or use `CompilerConfig(wire_reuse=False)`
for baseline allocation. Reuse affects build identity; it never changes the
scheduled operation order or inserts measurement/reset.

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

The physical view is the default; `--wire-view logical` shows original source
storage instead of shared wires. Both views use source-level operation/function boxes. Use `--unfold 1`
(or another depth), `--unfold all`, and optionally `--unfold-only compare,myFunction`
to reveal detail. `explain` lists selectors. Measurement/runtime branches remain
visible, and cleanup markers identify zeroed wires separately from restored inputs.
Shared wires have stable `work_N` names and `reuse` handoff labels.
Markers exist only in diagrams. Direct/generated executable circuits keep their
operation structure and receive named registers. The [CLI walkthrough](cli-walkthrough.md)
shows every command and view option. Drawing does not run extra simulations. `run` renders after a successful execution; `check`
lets you inspect a circuit without executing it. Idle/reserved wires remain visible.
Images fold long circuits into rows; excessive image dimensions receive Q4001
(40 million estimated pixels or 32,000 pixels on either side at 120 dpi).
Use console output to inspect a circuit that exceeds this image-size bound.

## Generated Python and future pipelines

The playground's **Download Qiskit Python** exports the circuit for the inputs in the last run.
Install `qiskit==2.3.0` and `qiskit-aer==0.17.2`, then run `python experiment.qiskit.py`.
The file exposes `build_circuit()` for notebooks and accepts `--shots` and `--seed` for local simulation.
To change a construction-time input, run the playground again and download the new circuit.

The CLI export can recompile the embedded source with new input values.

```text
qutes build examples/loops.qut --inputs examples/inputs.json -o artifacts/loops.py
python artifacts/loops.py --shots 32 --seed 7
```

Create the output directory first. Generation does not need Qiskit installed.
Generated Python contains readable circuit construction, embedded source, settings,
bound inputs, result layout, source/build hashes, versions, and resource metadata.
New modules use schema 5. Schema-3/4 modules remain executable with their cached
inputs and circuits. They reject changed inputs with a rebuild instruction before
recompilation. Review old array assignments: replace intended copies with
`copy(array)`, then rebuild under 0.4. Schemas 1/2 remain unsupported.
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
