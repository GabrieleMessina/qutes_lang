# Editing and debugging

Use **Run** to see how often each returned value occurs. Use the debugger to follow one shot and inspect how a gate changes the state before measurement.

## Playground

Open [Bell pair](https://qutes-lang.web.app/play.html#bell). Edit `main.qut` and set **Shots**. For a program with inputs, enter a JSON object in `inputs.json`. Edits stay in memory until you reload or close the page. On narrow editors the three-dot button beside Run holds the additional controls.

- **Results** groups identical return values across shots.
- **Circuit** shows the compiled gates. Select a mapped gate to highlight its source.
- **Qiskit Python** exports the last successful run.
- **Debug** starts a single shot. Click beside a source line or press F9 to toggle a breakpoint. Continue to the breakpoint, step into a function, step over a statement or step out to its caller.

The arrow marks the statement about to execute. In **Variables**, each qubit shows its physical wire and its probabilities of 0 and 1. Expand an integer, text value or array to inspect its distribution. Array elements appear under the array. **Joint state** shows basis strings, probabilities and amplitudes in the displayed wire order. Two qubits can each have a 50% chance of 1 while only 00 and 11 occur together.

## VS Code

Install the extension from the [Marketplace](https://marketplace.visualstudio.com/items?itemName=GabrieleMessina.qutes). Open a `.qut` file for highlighting, completions, signature help and live diagnostics. The **Problems** panel includes compiler messages. The extension runs the current editor contents and looks for `qutes.toml` beside the file and up to the workspace folder.

| Action | Where to find it |
| --- | --- |
| Run the current file | Editor play button or **Qutes: Run Qutes File**. Results appear in the Qutes output channel. |
| Choose construction inputs | Command Palette → **Qutes: Choose Input JSON** |
| Set repetitions | Command Palette → **Qutes: Set Shot Count** |
| Debug one shot | Set a breakpoint and start **Run and Debug** (F5). Inspect the call stack and Variables. |
| Run through the debug console | F5 without a breakpoint or stop-on-entry runs the selected shots on Aer. |
| Cancel | **Qutes: Stop** for the run command, or the debug toolbar’s Stop for a debugging session. |

For a first debugging exercise, pause before a controlled flip in Bell. Step over it and compare the two single-qubit probabilities with the joint state.
