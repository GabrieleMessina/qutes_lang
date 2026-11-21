# Qutes for VS Code

Open a `.qut` file and click **Run and Debug** in the sidebar (F5). With a line breakpoint or the launch option `stopOnEntry`, you can follow one simulated shot. With no breakpoint, F5 runs the selected number of shots on Aer. **Run Without Debugging** (Ctrl+F5 on Windows and Linux) always runs on Aer. Both show measurements in the Debug Console. The toolbar's **Run Qutes File** shows results in the Qutes output channel.

The first run or analysis unpacks the bundled Qutes simulator into VS Code's extension storage. It works offline on Windows x64, macOS Intel and Apple Silicon, and Linux x64 and ARM64.

The editor highlights Qutes, suggests names in scope, shows call signatures, and reports compiler errors in Problems. Run uses your current edits. The closest `qutes.toml` beside your file or up to the workspace folder supplies project settings. Choose **Qutes: Choose Input JSON** for programs with inputs and **Qutes: Set Shot Count** to change the default of 64. **Qutes: Stop** cancels a run. Measurements appear in the Qutes output channel.

For local review, use **Extensions: Install from VSIX** and choose the package matching your desktop or remote extension host. For a first program, try:

```qutes
qubit alice = false;
qubit bob = false;
hadamard(alice);
if (alice) { not(bob); }
return [measure(alice), measure(bob)];
```

Only matching pairs should appear. [Learn Qutes](https://qutes-lang.web.app/tutorial)

## Step through the Bell example

Open `examples/language/41_bell_gates.qut`. Click the gutter on line 7, next to `entangle(alice, bob);`, then press **F5**. The highlight marks the statement about to execute.

1. Press **F11** to enter `entangle`. The call stack shows the function and its caller.
2. Press **F10** to execute the Hadamard. Under **Variables**, expand **Quantum state**. The two basis states each have probability 50%. For Bell the digits are ordered Bob, Alice.
3. Press **Shift+F11** to finish the function. At the return line, the joint state has equal probabilities for `00` and `11`. Inspecting it preserves the state.
4. Press **F5** to continue through measurement. The Debug Console shows this shot's returned pair.

**Step Over** runs a function call at the current depth. **Step Out** returns to its caller. Both honor breakpoints encountered on the way. Ordinary line breakpoints work on statements reached for the current inputs. Synthesized search oracles step as part of the search expression. Editing the source ends the session so the next run uses your changes.

The offline step simulator shows amplitudes and probabilities for up to 16 basis states and any measured classical bits. It supports up to 12 physical qubits, the project's simulation limit, and a bounded amount of work per shot. Use **Run Without Debugging** for larger circuits and multi-shot results.

## Build and verify a local package

From the language repository root, install the packaging tools with `npm ci --prefix qutes-vscode` and the compiler's parser with `python -m pip install antlr4-python3-runtime==4.13.2`. Download the five native archives from the [2.0.1 release](https://github.com/GabrieleMessina/qutes_lang/releases/tag/2.0.1) into `artifacts/editor-runtimes`. Run `python qutes-vscode/package.py artifacts/editor-runtimes artifacts/editor-packages` with Python 3.12 or 3.13. The builder verifies the release hashes before bundling and reads each completed VSIX back to check its target, identity and runtime.

Run `node qutes-vscode/tests/run-installed.cjs PATH_TO_VSIX` on the matching operating system and architecture. Set `QUTES_VSCODE` to an installed VS Code executable to reuse it. Otherwise the test runner first downloads VS Code. The test uses its own profile and workspace. The manual **Verify offline VS Code candidates** workflow runs these checks on five native hosts and attaches the candidates as workflow artifacts.
