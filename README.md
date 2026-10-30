# Qutes

A high-level, strongly typed quantum language with C#-inspired syntax and a
Qiskit backend. This repository has a parser, typed analysis, classical expansion,
and a separately tested cleanup scheduler. Source-to-Qiskit integration is pending.

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

## Try the syntax parser

```powershell
& C:\ProgramData\anaconda3\python.exe tools/qutes.py parse tests/acceptance/A004_snapshots.qut
& C:\ProgramData\anaconda3\python.exe tools/qutes.py parse tests/acceptance/A004_snapshots.qut --json
```

After installation the equivalent command is `qutes parse FILE [--json]`.
This checks **syntax only**. It intentionally accepts syntactically valid programs
whose types, staging, or quantum cleanup will later be rejected. The `check`,
`build`, `run`, and `explain` commands are not implemented yet.

- [Working language contract](docs/spec/language-v0.1.md)
- [Grammar](docs/spec/grammar.ebnf)
- [Source acceptance inventory](tests/acceptance/cases.json)

## Analyze types and execution stages

```powershell
& C:\ProgramData\anaconda3\python.exe tools/qutes.py analyze tests/acceptance/A004_snapshots.qut --quint-bits 4
```

`analyze` accepts `--json` for typed IR and `--config FILE` for a project settings
file. It validates names, types, execution stages, effects, and known shapes.
It deliberately does not claim quantum cleanup or complete construction-time
validation. Full `check`/`build`/`run` commands still await those passes.

## Inspect circuit construction

```powershell
& C:\ProgramData\anaconda3\python.exe tools/qutes.py construct tests/acceptance/A011_for.qut --quint-bits 4 --json
```

`construct` expands classical loops and inlines helpers, while preserving quantum
operations and measurement results symbolically. Use `--inputs FILE` for a JSON
object matching classical main parameters. This intermediate result is not yet
a verified circuit: integration with cleanup and Qiskit generation is still pending.

The [versioned cleanup scheduler](docs/spec/cleanup-scheduling.md) and reversible
gate adapter have full-state tests for arithmetic, changed inputs, dependency
recomputation, and rejected unsafe cleanup. Measurement-aware source lowering
and complete program execution remain to be implemented.
