# Qutes

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
snapshot. `measure` and `superposition` are the current builtin spellings.

## Getting started

Use Python 3.12 or 3.13 and an isolated environment. Windows PowerShell:

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
- [Runnable examples](examples/)
- [Language contract](docs/spec/language-v0.3.md) and [grammar](docs/spec/grammar.ebnf)
- [Knowledge base and handoff](docs/knowledge/README.md)
- [Current status and validation limits](docs/knowledge/STATUS.md)
- [V1 release audit](docs/release-audit.md)
- [Development plan](DEVELOPMENT_PLAN.md)

## Boundaries

V1 runs on a local ideal simulator. Hybrid multi-job pipelines, measurement-driven
loops, general runtime arithmetic, hardware jobs, and a large algorithm library
belong to later milestones. Some cleanup dependency patterns are conservatively
rejected with a source diagnostic. No hidden measurement/reset substitutes for
uncomputation. Cleaned wires remain reserved and are included in resource reports.

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
Rebuild older generated Python modules with `qutes build` for artifact schema 3.

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
python -m pip install --no-deps --force-reinstall dist/qutes_lang-0.3.0.dev0-py3-none-any.whl
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
The [0.3 language contract](docs/spec/language-v0.3.md) documents scripts, globals,
input declarations, diagnostics, inferred effects, and migration from 0.1.
