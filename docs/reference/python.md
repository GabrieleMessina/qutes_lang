# Qiskit and Python

Choose the export according to what should happen when you change an input.

| Export | What the file contains | Environment for running the file |
| --- | --- | --- |
| Playground **Qiskit Python** | Standalone circuit for the inputs used on the last run | Python with Qiskit and Qiskit Aer |
| CLI `qutes build` | Circuit, embedded Qutes source, bound inputs and configuration | Python with Qutes, Qiskit and Qiskit Aer |

## Run the playground export

Run the program, select **Qiskit Python**, and download the file. Run the following in the directory containing it. The exported file also lists its tested dependencies.

```sh
python -m pip install qiskit==2.3.0 qiskit-aer==0.17.2
python experiment.qiskit.py --shots 64 --seed 17
```

Use the decoded outcome values when comparing the export with the browser. The Qutes return expression determines their order. Raw Qiskit counts are bit strings ordered by classical memory. To inspect the underlying `QuantumCircuit`, call the exported `build_circuit()`. To change the Qutes inputs, edit them in the playground, run again and export again.

## Use a CLI-generated module

Build the [configuration example](configuration.md) with `qutes build count.qut --inputs inputs.json -o count_module.py`. Place your Python script beside that file.

```python
import count_module

circuit, layout = count_module.build(inputs={"steps": 2})
result = count_module.run(inputs={"steps": 2}, shots=32, seed=7)
print(result["outcomes"])
```

Omit `inputs` to use the build’s bound values. New input values can change the circuit and its result layout. `layout.decode(memory)` converts an integer containing the complete classical memory into the script result, with bit zero least significant. `run` combines counts with the same decoded value and includes build and execution metadata.

## Compile a string from Python

```python
from qutes.compiler import compile_source

program = compile_source("qubit q = false; return measure(q);")
print(program.run(shots=8, seed=7)["outcomes"])
```

Pass `inputs=` and `config=` explicitly to specialize a source program. The Python API uses defaults when configuration is omitted. A program with a known classical output can return its result without invoking the simulator.
