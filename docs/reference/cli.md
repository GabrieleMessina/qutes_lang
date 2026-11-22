# Command-line reference

Run `qutes COMMAND FILE.qut`. If you extracted a portable folder, use `./qutes` or `.\qutes.exe` in place of `qutes`. Use `qutes --version` to identify your compiler and `qutes COMMAND --help` for the flags accepted by a particular command.

| Command | What it does |
| --- | --- |
| `parse` | Reads the grammar and reports the syntax tree. |
| `analyze` | Checks names, types, stages and effects without input bindings. |
| `construct` | Binds inputs, expands loops and specializes calls. |
| `check` | Compiles through cleanup and circuit lowering without running the circuit. |
| `explain` | Reports allocations, snapshots, cleanup and estimated resources. |
| `build` | Writes a Python module. Use `-o FILE.py` to choose its path. |
| `run` | Executes shots and reports decoded return values and their counts. |

## Check and run a file

Save the [first program](getting-started.md) as `bell.qut` in your working directory.

```sh
qutes check bell.qut
qutes explain bell.qut
qutes run bell.qut --shots 64 --seed 17
```

Use `--inputs FILE.json` for declared inputs and `--config FILE.toml` to select project settings. `--json` produces machine-readable results or diagnostics. The default CLI run requests 1024 shots. A fixed seed is useful for repeating a run in the same backend environment.

## Inspect a circuit

`check`, `explain`, `build` and `run` accept diagram flags. A drawing represents the circuit for the bound inputs.

```sh
qutes check bell.qut --print-circuit
qutes check bell.qut --save-circuit diagrams --circuit-format svg
```

`--save-circuit FOLDER` defaults to PNG. Output names include the source name, build hash and view hash. Use `--wire-view logical` or `physical` to select a wire view. `--unfold 1` opens one level of folded operations, and `--unfold all` opens every level. `--unfold-only NAME1,NAME2` selects the operations to expand. With `--json`, printed diagrams go to stderr.

## Export Python

```sh
qutes build bell.qut -o bell.py
python bell.py --shots 64 --seed 17
```

Use a Python environment with Qutes, Qiskit and Aer to run the CLI-generated file. Create the parent directory before choosing a nested output path. Rebuilding can replace an existing Qutes-generated file. `--force` explicitly permits replacement of another output file. See [Qiskit and Python](python.md) for the module interface and standalone playground export.
