# Qutes

A high-level, strongly typed quantum language with C#-inspired syntax and a
Qiskit backend. This repository is at the specification and feasibility stage;
it is not yet a working source-to-Qiskit compiler.

```csharp
int main() {
    quint number = 5;
    int before = measure(number);
    number = number + 2;
    return measure(number);
}
```

This planned program returns 7. Measurement leaves `number` usable; `before`
remains a snapshot of 5. `measure` and `superposition` are working builtin names.

## Start here

- [Knowledge base / handoff](docs/knowledge/README.md)
- [Current status](docs/knowledge/STATUS.md)
- [Task queue](docs/knowledge/TASKS.md)
- [Development plan](DEVELOPMENT_PLAN.md)
- [Contributor instructions](AGENTS.md)

## Development and validation

Python 3.12+ is the target; Python 3.13.5 on Windows is the currently exercised
environment. To prepare a fresh isolated environment:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.lock
.\.venv\Scripts\python.exe -m pip install --no-build-isolation --no-deps -e .
.\.venv\Scripts\python.exe tools/check.py -q
```

The pins describe the tested installed packages. A clean install and Linux support
still need verification. No global package installation is required.

In the current workspace, a working existing interpreter is available:

```powershell
& C:\ProgramData\anaconda3\python.exe tools/check.py -q
```

The runner disables unrelated pytest plugins, puts temporary files inside ignored
`artifacts/checks/`, and records a JUnit report and environment metadata for each
run. Backend probes compare full states with an independent small-state model.
They do not prove that automatic cleanup or source compilation is implemented.

- [Working language contract](docs/spec/language-v0.1.md)
- [Grammar](docs/spec/grammar.ebnf)
- [Source acceptance inventory](tests/acceptance/cases.json)
