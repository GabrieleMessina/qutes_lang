# Qutes for VS Code

Open a `.qut` file and click **Run and Debug** in the sidebar (F5). With a line breakpoint or the launch option `stopOnEntry`, you can follow one simulated shot. With no breakpoint, F5 runs the selected number of shots on Aer. **Run Without Debugging** (Ctrl+F5 on Windows and Linux) always runs on Aer. Both show measurements in the Debug Console. The toolbar's **Run Qutes File** shows results in the Qutes output channel.

The first run or analysis unpacks the bundled Qutes simulator into VS Code's extension storage. It works offline on Windows x64, macOS Intel and Apple Silicon, and Linux x64 and ARM64.

The editor highlights Qutes, suggests names in scope, shows call signatures, and reports compiler errors in Problems. Run uses your current edits. The closest `qutes.toml` beside your file or up to the workspace folder supplies project settings. Choose **Qutes: Choose Input JSON** for programs with inputs and **Qutes: Set Shot Count** to change the default of 64. **Qutes: Stop** cancels a run. Measurements appear in the Qutes output channel.

Install **Qutes** by **Gabriele Messina** in the Extensions view. VS Code selects the package for your extension host. For a local build, use **Extensions: Install from VSIX**. [Marketplace listing](https://marketplace.visualstudio.com/items?itemName=GabrieleMessina.qutes)

For a first program, try:

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

1. Choose **Step Into** (**F11**) to enter `entangle`. Expand **Variables** and **Qutes variables**. Alice and Bob each show a 100% probability of measuring 0.
2. Choose **Step Over** (**F10**) to apply the Hadamard. Alice now shows `q[0]  P(0)=50%  P(1)=50%`, and Bob still has a 100% probability of measuring 0. Expand **Quantum state · |bob alice⟩** to see the two equally likely outcomes, `00` and `01`. The rightmost digit is Alice's.
3. Choose **Step Out** (**Shift+F11**) to run the controlled flip and return to the caller. Both qubits now show 50% for each outcome. The joint state shows their correlation: only `00` and `11` can occur.
4. Press **F5** to continue through measurement. The Debug Console shows this shot's returned pair.

**Step Over** runs a function call at the current depth. **Step Out** returns to its caller. Both honor breakpoints encountered on the way. Ordinary line breakpoints work on statements reached for the current inputs. Synthesized search oracles step as part of the search expression. Editing the source ends the session so the next run uses your changes.

While paused, use the three arrow icons after **Continue** on the debug toolbar, or open the **Run** menu to see the actions by name. The editor's **Run Qutes File** play button starts an ordinary run.

The offline step simulator shows amplitudes and probabilities for up to 16 basis states and any measured classical bits. It supports up to 12 physical qubits, the project's simulation limit, and a bounded amount of work per shot. Use **Run Without Debugging** for larger circuits and multi-shot results.

Select a call stack frame to see its in-scope Qutes names. Each quantum variable shows its wires and the probabilities of its measurement outcomes in the current shot. Qubits show 0 and 1. A `quint` shows signed integers, and a `quchar` or `qustring` shows text decoded with the project's alphabet and the string's current length. For example, pause before `return measure(number);` in `examples/language/44_weighted_preparation.qut` to see `P(2)=75%` and `P(-1)=25%`.

Expand a typed value to see every outcome with nonzero probability, highest probability first. Its row previews the two most likely values. Arrays of up to 16 elements also show the probabilities of whole-array outcomes, including correlations between elements. Larger arrays show their first 16 elements individually. Inspection preserves the state. Classical variables show their current values, including measurements the program has already made.

## Build and verify a local package

From the language repository root, install the packaging tools with `npm ci --prefix qutes-vscode` and the compiler's parser with `python -m pip install antlr4-python3-runtime==4.13.2`. Download the five native archives from the [2.0.1 release](https://github.com/GabrieleMessina/qutes_lang/releases/tag/2.0.1) into `artifacts/editor-runtimes`. Run `python qutes-vscode/package.py artifacts/editor-runtimes artifacts/editor-packages` with Python 3.12 or 3.13. The builder verifies the release hashes before bundling and reads each completed VSIX back to check its target, identity and runtime.

Run `node qutes-vscode/tests/run-installed.cjs PATH_TO_VSIX` on the matching operating system and architecture. Set `QUTES_VSCODE` to an installed VS Code executable to reuse it. Otherwise the test runner first downloads VS Code. The test uses its own profile and workspace. The manual **Verify offline VS Code candidates** workflow runs these checks on five native hosts and attaches the candidates as workflow artifacts.

## Release a new extension version

Update the extension version and lockfile together with `npm version patch --no-git-tag-version` in `qutes-vscode/` (use `minor` or `major` when appropriate). Merge the change into `qutes2.0`. The **Compiler and package checks** workflow tests the compiler and installs each of the five desktop packages on its native platform. When every check passes, the publish job reads the VSIX files from that run, verifies their identities and SHA-256 checksums, and uploads them to the existing listing. Publication starts automatically. Microsoft then validates each platform.

If an upload stops partway through, select **Re-run failed jobs** on the original run to reuse its tested files. The job compares previously submitted packages by SHA-256 and uploads the missing targets. A checksum conflict stops the release for investigation.

An unchanged version on the release branch skips the release jobs. Manually running **Compiler and package checks** on `qutes2.0` exercises the tests and publisher connection without uploading. GitHub authenticates through the `vscode-marketplace` environment, restricted to `qutes2.0`. Its one-time Marketplace Trusted Publishing policy names `GabrieleMessina/qutes_lang`, workflow `ci.yml`, and that environment.
