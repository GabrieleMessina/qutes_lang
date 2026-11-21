# Qutes for VS Code

Open a `.qut` file and choose **Run Qutes File** in the editor toolbar. The first run or analysis unpacks the bundled Qutes simulator into VS Code's extension storage. It works offline on Windows x64, macOS Intel and Apple Silicon, and Linux x64 and ARM64.

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

## Build and verify a local package

From the language repository root, install the packaging tools with `npm ci --prefix qutes-vscode`. Download the five native archives from the [2.0.1 release](https://github.com/GabrieleMessina/qutes_lang/releases/tag/2.0.1) into `artifacts/editor-runtimes`. Run `python qutes-vscode/package.py artifacts/editor-runtimes artifacts/editor-packages` with Python 3.12 or 3.13. The builder verifies the release hashes before bundling and reads each completed VSIX back to check its target, identity and runtime.

Run `node qutes-vscode/tests/run-installed.cjs PATH_TO_VSIX` on the matching operating system and architecture. Set `QUTES_VSCODE` to an installed VS Code executable to reuse it. Otherwise the test runner first downloads VS Code. The test uses its own profile and workspace. The manual **Verify offline VS Code candidates** workflow runs these checks on five native hosts and attaches the candidates as workflow artifacts.
