# Qutes 2.0.0

A strongly typed quantum language with compact C#-inspired syntax, automatic
uncomputation, and a Qiskit backend. The first research implementation supports
quantum integers, bits, characters, strings, arrays, functions, ordinary assignment,
coherent branches, construction-time loops, and non-consuming measurement.

```csharp
quint number = 5;
int before = measure(number);
number = number + 2;
return [before, measure(number)];
```

This returns `[5,7]`. Measurement leaves `number` available; `before` remains a
snapshot. Qutes 2.0.0 also supports readable live gates, mutable parameters, array
references and slices, weighted preparation, subtraction and coherent indexing.

## Getting started

### Portable CLI

Download the archive for your operating system and processor from the
[Qutes 2.0.0 release](https://github.com/GabrieleMessina/qutes_lang/releases/tag/2.0.0).
Extract the whole folder and open a terminal there. On Windows run
`.\qutes.exe run examples\bell.qut`. On macOS and Linux run
`./qutes run examples/bell.qut`. The portable CLI includes Python, the Aer
simulator and circuit-image export. The included README explains how to use it
from your own project directory.

### Python environment

For a source installation, use Python 3.12 or 3.13 and an isolated environment. Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install ".[backend]"
.\.venv\Scripts\qutes.exe check examples/measurement_snapshots.qut
.\.venv\Scripts\qutes.exe run examples/measurement_snapshots.qut --shots 32 --seed 7
.\.venv\Scripts\qutes.exe explain examples/measurement_snapshots.qut
.\.venv\Scripts\qutes.exe build examples/measurement_snapshots.qut -o snapshots.qiskit.py
```

Add `--print-circuit` to print the final compiler circuit, or
`--save-circuit artifacts/circuits` to save its image. PNG is the default;
`--circuit-format svg` selects SVG. Both options work on check/build/run/explain.
For images, install `".[backend,visualization]"` in the virtual environment.

On Linux use `.venv/bin/python` and `.venv/bin/qutes`. `python -m qutes` also works.
Core installation without `[backend]` supports checking and Python generation;
execution requires Qiskit/Aer. The tested backend pins are Qiskit 2.3.0, Aer 0.17.2,
and NumPy 2.1.3.

- [User guide and generated-module API](docs/guide.md)
- [All seven CLI modes](docs/cli-walkthrough.md)
- [Runnable examples](examples/)
- [Complete language tour: 50 runnable examples, all within 24 qubits](examples/language/README.md)
- [Language contract](docs/spec/language-v0.4.md) and [grammar](docs/spec/grammar.ebnf)
- [Knowledge base and handoff](docs/knowledge/README.md)
- [Current status and validation limits](docs/knowledge/STATUS.md)
- [V1 release audit](docs/release-audit.md)
- [Development plan](DEVELOPMENT_PLAN.md)

## Boundaries

V1 runs on a local ideal simulator. Hybrid multi-job pipelines, measurement-driven
loops, general runtime arithmetic, hardware jobs, and a large algorithm library
belong to later milestones. Some cleanup dependency patterns are conservatively
rejected with a source diagnostic. No hidden measurement/reset substitutes for
uncomputation. Certified-zero wires are reused after cleanup; reports distinguish logical storage
from physical circuit width. Use `--no-wire-reuse` for the original allocation.

Quantum values are not unrestricted classical mutable values: copying correlates
basis values, quantum branches preserve coherence, and unsafe erasure is rejected.
See the guide for the rules and examples. These primitives alone do not imply a
quantum speedup.

## Membership and automatic search

`in` checks scalar membership or contiguous sequences. Strings act as character
sequences, with `?` matching one character on the pattern side. Quantum operands
produce a coherent qubit predicate without measurement or amplification.

```csharp
qubit accepts(qustring text) { return "?B" in text; }
string[] texts = ["AA", "AB", "BB"];
qustring candidate = search(texts, accepts);
return measure(candidate);
```

`search` amplifies matching entries automatically and returns a quantum value.
Its named oracle receives one element and returns qubit. Measurement is explicit.
The default ideal success bound is 99% when a match exists; with no matches the
result is a nonmatching candidate. Set `search_failure_probability` in qutes.toml
or pass `--search-failure-probability 0.01`. `explain` reports oracle calls and the
retained selection/workspace qubits. Controlled collection access has linear cost.

```text
python tools/qutes.py run examples/search.qut --alphabet AB --shots 128 --seed 17
python tools/qutes.py explain examples/search_numbers.qut
python tools/qutes.py check examples/search.qut --alphabet AB --print-circuit
```

The alphabet override keeps the string example small enough to simulate. Search
requires equal-length string entries. A search result retains an internal index;
measurement can make local cleanup impossible, which is reported explicitly.
See the [0.3 contract](docs/spec/language-v0.3.md) for oracle effects and ownership.
New generated modules use artifact schema 5. Schema-3/4 modules still execute their
cached circuits with the original inputs. Review array assignments and rebuild
with `qutes build` before changing their inputs: arrays now share storage by default.

## Live gates and shared arrays

```csharp
void entangle(mut qubit alice, mut qubit bob) {
    hadamard(alice);
    if (alice) { not(bob); }
}
qubit[] bits = [false, false];
qubit[] alias = bits;
entangle(alias[0], alias[1]);
return measure(bits);
```

This returns `[false,false]` or `[true,true]`. `phaseFlip`, `phase` (radians), and
`swap` complete the live operations. Coherent `if` supplies quantum controls.
Arrays/slices share backing storage; use `copy(bits)` for a correlated basis-value
copy. Parameters default to read-only; `mut` grants caller-visible updates.
`readonly` prevents writes through a binding and allows explicit measurement.
See tour examples 40–50 for preparation, QFT, teleportation, slices and indexing.

## Development and verification

Inside an activated virtual environment:

```text
python -m pip install -r requirements-dev.lock
python -m pip install --no-build-isolation --no-deps -e .
python tools/check.py -q
```

`tools/qutes.py` runs the checkout CLI without installation. `parse`, `analyze`,
and `construct` expose intermediate representations and explicitly do not claim
complete validation. Use `check` for the full compilation path.

The test runner disables unrelated pytest plugins and stores JUnit/environment
evidence in ignored `artifacts/checks/`. Tests include an independent small-state
oracle, full complex-state comparisons, measurement branches, signed arithmetic,
cleanup histories, generated Python execution, and every acceptance example.

To verify an installed wheel independently of checkout import paths:

```text
python -m pip wheel --no-build-isolation --no-deps . -w dist
python -m pip install --no-deps --force-reinstall dist/qutes_lang-2.0.0-py3-none-any.whl
python -I tools/verify_install.py
```

The knowledge base records exact environments, failed attempts, evidence, and
remaining work. Follow [AGENTS.md](AGENTS.md) before changing code. Local commits
capture coherent implementation checkpoints; no remote publication is implied.

## Parser development

The authoritative grammar is [Qutes.g4](grammar/Qutes.g4). Generated Python sources
are committed, so installations do not require Java. To regenerate, use Java 21
and the official ANTLR 4.13.2 complete jar (the script verifies its SHA256):

```text
python tools/generate_parser.py --jar artifacts/antlr/antlr-4.13.2-complete.jar
python tools/generate_parser.py --jar artifacts/antlr/antlr-4.13.2-complete.jar --check
```

Use `--java PATH` if Java is not on PATH. The runtime is pinned to the same version.
The [0.4 language contract](docs/spec/language-v0.4.md) documents the current
reference, preparation and gate rules and links the unchanged script/search rules.

## Teaching and research

[Teach, build locally, or inspect a Qiskit circuit](resources/README.md). Qutes was introduced by Simone Faro, Francesco Pio Marino, and Gabriele Messina. See [citation metadata](CITATION.cff), [the original paper](https://doi.org/10.1145/3731545.3744153), and [Extending Qutes](https://doi.org/10.1093/comjnl/bxaf133).
