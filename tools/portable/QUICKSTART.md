# Qutes 2.0.0 portable CLI

Extract the entire archive. Keep the executable and its `_internal` folder together.
Open a terminal in the extracted directory.

Windows PowerShell:

```powershell
.\qutes.exe --version
.\qutes.exe run examples\bell.qut --shots 64 --seed 17
```

macOS and Linux:

```sh
./qutes --version
./qutes run examples/bell.qut --shots 64 --seed 17
```

Both measurements agree in each shot. Expect rows for the two matching pairs.
The bundled compiler, local Aer simulator and circuit-image tools work offline.

From a separate project directory, supply the path to the portable command. For example,
use `& 'C:\Tools\Qutes\qutes.exe' run main.qut` in PowerShell or
`"$HOME/tools/qutes/qutes" run main.qut` on macOS or Linux. Adjust the path
to where you put the extracted folder. Qutes reads a source-adjacent `qutes.toml`.

Use `build main.qut -o main.qiskit.py` with the same executable to generate a Python
module, or `check main.qut --save-circuit images --circuit-format svg` to draw the circuit.
Running the exported module independently uses a Python environment with
`qutes-lang[backend]==2.0.0`. Use `--help` for more commands.

Compiler provenance and dependency versions are in `build-info.json`.
The Qutes license and citation are at the top level. Third-party notices are in `licenses/`.
