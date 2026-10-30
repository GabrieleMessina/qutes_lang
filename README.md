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

Implementation and validation commands will be added as the first executable
milestone is completed. Do not infer feature support from the roadmap alone.
