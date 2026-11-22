# Inputs and configuration

Declare a construction-time input at the top level and bind it by name. Each input can change the circuit that Qutes builds, including loop lengths and initial preparations.

```qutes
input int steps;
quint value = 0;
for (int i = 0; i < steps; i++) { value += 1; }
return measure(value);
```

Save this as `count.qut`. In the playground’s `inputs.json` tab, or in a local file named `inputs.json`, enter:

```json
{"steps": 3}
```

Run `qutes run count.qut --inputs inputs.json`. With defaults, every shot returns 3. A complex JSON value uses fields `real` and `imag`. Arrays use ordinary JSON arrays.

## Project settings

The CLI reads `qutes.toml` beside the source file. Select a different file with `--config FILE`. Individual command-line flags override file settings. The Python API takes its configuration explicitly.

```toml
[qutes]
quint_bits = 4
alphabet = "ABC"
qustring_capacity = 2
wire_reuse = true
```

| Key | Default | Controls |
| --- | --- | --- |
| `quint_bits` | 4 | Signed quantum integer width |
| `alphabet` | `"ABC"` | Distinct characters available to quantum text; at least two are required |
| `qustring_capacity` | 2 | Storage capacity of a quantum string |
| `wire_reuse` | `true` | Reuse of work wires certified to be zero |
| `search_failure_probability` | 0.01 | Failure bound between zero and one, exclusive |
| `max_loop_iterations` | 10000 | Limit on construction-time iteration |
| `max_evaluation_steps` | 100000 | Construction and expansion work budget |
| `max_classical_bits` | 65536 | Bit-length bound on classical integers |
| `max_simulation_qubits` | 24 | Local simulator width limit |
| `max_simulation_shots` | 1000000 | Maximum shots per local run |

Use `qutes run --help` to find the matching overrides, including `--max-qubits` and `--no-wire-reuse`. A program that compiles can still exceed a simulator limit. The browser uses its own smaller limits, shown under the editor.
