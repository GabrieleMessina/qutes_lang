# Qutes

A strongly typed quantum language with compact C#-inspired syntax, automatic
uncomputation, and a Qiskit backend. The first research implementation supports
quantum integers, bits, characters, strings, arrays, functions, ordinary assignment,
coherent branches, construction-time loops, and non-consuming measurement.

```csharp
int[] main() {
    quint number = 5;
    int before = measure(number);
    number = number + 2;
    return [before, measure(number)];
}
```

This returns `[5,7]`. Measurement leaves `number` available; `before` remains a
snapshot. `measure` and `superposition` are the current builtin spellings.

## Getting started

Use Python 3.12 or 3.13 and an isolated environment. Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install ".[backend]"
.\.venv\Scripts\qutes.exe check examples/snapshots.qut
.\.venv\Scripts\qutes.exe run examples/snapshots.qut --shots 32 --seed 7
.\.venv\Scripts\qutes.exe explain examples/snapshots.qut
.\.venv\Scripts\qutes.exe build examples/snapshots.qut -o snapshots.qiskit.py
```

On Linux use `.venv/bin/python` and `.venv/bin/qutes`. `python -m qutes` also works.
Core installation without `[backend]` supports checking and Python generation;
execution requires Qiskit/Aer. The tested backend pins are Qiskit 2.3.0, Aer 0.17.2,
and NumPy 2.1.3.

- [User guide and generated-module API](docs/guide.md)
- [Runnable examples](examples/)
- [Language contract](docs/spec/language-v0.1.md) and [grammar](docs/spec/grammar.ebnf)
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
python -m pip install --no-deps --force-reinstall dist/qutes_lang-0.1.0.dev0-py3-none-any.whl
python -I tools/verify_install.py
```

The knowledge base records exact environments, failed attempts, evidence, and
remaining work. Follow [AGENTS.md](AGENTS.md) before changing code. Local commits
capture coherent implementation checkpoints; no remote publication is implied.
