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
