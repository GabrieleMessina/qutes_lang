# Qutes

[![Qiskit Ecosystem](https://img.shields.io/endpoint?style=flat&url=https%3A%2F%2Fqiskit.github.io%2Fecosystem%2Fb%2F79b52453)](https://qisk.it/e)
[![Qutes Build and Tests](https://github.com/GabrieleMessina/qutes_lang/actions/workflows/ci.yml/badge.svg?branch=qutes2.0)](https://github.com/GabrieleMessina/qutes_lang/actions/workflows/ci.yml?query=branch%3Aqutes2.0)

Qutes is a strongly typed quantum programming language that compiles to Qiskit circuits. You can write a conditional using a qubit, add two quantum integers, or search a collection. The compiler tracks temporary qubits, uncomputes them when it can prove cleanup is safe, and reuses the freed circuit wires.

[Open the playground](https://qutes-lang.web.app/play#bell) · [Follow the tutorial](https://qutes-lang.web.app/tutorial) · [Install Qutes for VS Code](https://marketplace.visualstudio.com/items?itemName=GabrieleMessina.qutes) · [Download the Qutes 2.0.1 CLI](https://qutes-lang.web.app/downloads)

## Try a Bell pair

Open the Bell example in the playground and click **Run**. Both qubits start at `false`. The Hadamard gate puts Alice's qubit into superposition, and the `if` uses it as a quantum control to flip Bob's qubit. The two qubits are measured only in the return statement.

```csharp
void entangle(mut qubit alice, mut qubit bob) {
    hadamard(alice);
    if (alice) { not(bob); }
}
qubit alice = false;
qubit bob = false;
entangle(alice, bob);
return [measure(alice), measure(bob)];
```

Every shot returns a matching pair, either `[false, false]` or `[true, true]`. Try inserting `not(bob);` immediately before `return` and run again. Now the two measurements disagree on every shot. Open **Circuit** to see the extra gate, or **Qiskit Python** to download your edited circuit as a Python program you can run with Qiskit and Aer. [Bell source](examples/language/41_bell_gates.qut)

## Run and debug in VS Code

Install **Qutes** by **Gabriele Messina** from the Extensions view in desktop VS Code. Version **2.0.6** includes the compiler and Qiskit Aer, so you can work offline after installation. VS Code selects the package for Windows x64, macOS Intel or Apple Silicon, or Linux x64 or ARM64. [Qutes on the VS Code Marketplace](https://marketplace.visualstudio.com/items?itemName=GabrieleMessina.qutes)

1. Save the Bell program above as `bell.qut` and open it in VS Code. As you type, the editor suggests names and gate parameters. Compiler errors appear under the source and in **Problems**.
2. Click **Run Qutes File** in the editor toolbar. The **Qutes** output channel shows the results of 64 shots by default. Both measurements in each pair should agree.
3. To follow one shot, set a breakpoint on `entangle(alice, bob);` and press **F5**. Choose **Step Into**, then **Step Over** to apply the Hadamard. In **Variables**, Alice now has a 50% chance of measuring 1 and Bob still has a 0% chance. Choose **Step Out** to finish entangling them, then expand **Quantum state** to see the two matching outcomes.

## Run the portable CLI

Choose the download for **Windows x64**, **macOS Apple Silicon or Intel**, or **Linux x64 or ARM64**. Extract the entire archive and open a terminal in the folder containing the executable. Python, Qiskit Aer, and circuit-image support are bundled, so you can run the example offline. [Downloads and first-run instructions](https://qutes-lang.web.app/downloads) · [Release files and checksums](https://github.com/GabrieleMessina/qutes_lang/releases/tag/2.0.1)

**Windows PowerShell**

```powershell
.\qutes.exe run examples\bell.qut --shots 64
```

**macOS and Linux**

```sh
./qutes run examples/bell.qut --shots 64
```

## See where the qubits go

A loop that creates a temporary quantum integer on every iteration does not necessarily need new hardware wires each time. In the wire-reuse example, Qutes maps **39 logical qubit allocations onto 6 physical wires**. To inspect it, run the following from a source checkout after installing the CLI, or open the experiment in the playground. [Wire-reuse experiment](https://qutes-lang.web.app/play#reuse) · [Example source](examples/language/39_wire_reuse.qut)

```sh
qutes explain examples/language/39_wire_reuse.qut
qutes run examples/language/39_wire_reuse.qut --shots 64
```

The program returns `-3`. Add `--no-wire-reuse` to the **explain** command to compare the circuit widths. Cleanup that the compiler cannot prove safe produces a source diagnostic. [Wire allocation rules](docs/spec/wire-allocation.md)

## Learn the language

| If you want to… | Start here |
| --- | --- |
| Study interference, teleportation, or Grover's algorithm | [Interactive tutorial with 17 chapters and three optional extensions](https://qutes-lang.web.app/tutorial) |
| Try quantum integers, shared arrays, mutable parameters, or coherent search | [Language tour with 50 runnable examples](examples/language/README.md) |
| Check a program, generate Python, or save a circuit as PNG or SVG | [CLI walkthrough](docs/cli-walkthrough.md) |
| Understand assignment, measurement, and the generated Python API | [User guide](docs/guide.md) · [Language specification](docs/spec/language-v0.4.md) |
| Teach a lab or run a notebook | [Teaching and study resources](resources/README.md) |

The playground runs bounded experiments in your browser. The portable CLI runs larger circuits locally with Aer, subject to available memory. Hardware execution is outside the current CLI.

## Install from source

From the repository root, create and activate a virtual environment with Python 3.12 or 3.13. Install the simulator and drawing dependencies, then check and run the same Bell source used above.

```sh
python -m pip install ".[backend,visualization]"
qutes check examples/language/41_bell_gates.qut
qutes run examples/language/41_bell_gates.qut --shots 64
```

A core install (`python -m pip install .`) supports checking and Python generation. The CLI's `qutes build` export uses the Qutes backend when run separately. The playground's Python download runs with just Qiskit and Aer. [Generated-module API](docs/guide.md)

## Contribute

In an activated development environment, install the pinned dependencies and run the compiler checks:

```sh
python -m pip install -r requirements-dev.lock
python -m pip install --no-build-isolation --no-deps -e .
python tools/check.py -q
```

The ANTLR grammar lives in `grammar/Qutes.g4`. Generated parser sources are included. Regeneration uses Java 21 and the ANTLR 4.13.2 complete jar. [Grammar](grammar/Qutes.g4) · [Parser generation tool](tools/generate_parser.py) · [Contributor instructions](AGENTS.md) · [Project status](docs/knowledge/STATUS.md)

## Research and license

Qutes was introduced by Simone Faro, Francesco Pio Marino, and Gabriele Messina. The project is distributed under the MIT License. [Original paper](https://doi.org/10.1145/3731545.3744153) · [Extending Qutes](https://doi.org/10.1093/comjnl/bxaf133) · [Citation metadata](CITATION.cff) · [License](LICENSE)
