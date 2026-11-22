# Diagnostics

A diagnostic identifies the source location, a code and a message. Start with the first marked expression. Check that its type, execution stage and permitted effects match the operation around it. Use `qutes check FILE` for complete compiler checks and add `--json` for structured output.

| Code | What to inspect |
| --- | --- |
| `Q0001` | Source path, permissions or UTF-8 encoding |
| `Q0002` | Project configuration or command-line overrides |
| `Q0003` | Input file path and JSON syntax |
| `Q0004` | Output path or artifact write failure |
| `Q1001`, `Q1002` | Invalid literal, escape or token; missing delimiter or statement terminator |
| `Q2001` | Type, conversion, argument count or unsupported operation |
| `Q2002` | Unknown or duplicate name, reserved built-in name or recursive call |
| `Q2003` | Value needed during construction but available only during execution |
| `Q2004` | Mutation through a read-only binding, protected control, or forbidden conditional effect |
| `Q2005` | Function or script return contract |
| `Q3001` | An overwrite, overlap or cleanup step the compiler cannot implement reversibly |
| `Q4001` | Bounds or resource budget, including expansion, simulation or diagram size |
| `Q5001`, `Q5002`, `Q5003` | Missing backend dependency, backend execution or diagram rendering respectively |
| `QW0001` | The configured quantum alphabet includes the pattern wildcard `?` |

## A stage error

If a loop bound comes from `measure(q)`, the compiler cannot know how many copies of the loop body to build. Supply a classical `input int` for a construction-time bound. If you want one gate to follow a measurement outcome, measure first and use the recorded Boolean in an `if`.

## A cleanup error

Overwriting an unknown qubit with a constant can discard quantum information. If you intend a reversible flip, use `not(q)`. If you need both the old and derived value, keep separate bindings and check their lifetimes. See [Assignment, cleanup and wire reuse](cleanup.md).

## A resource error

Run `qutes explain FILE` with the same inputs and configuration. Compare physical qubits with the simulator limit. Reducing an integer width or text capacity can help when your values fit the smaller encoding. Statevector storage alone grows as 16 × 2ⁿ bytes for n qubits. Browser and local simulator budgets differ.
