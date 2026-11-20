Qutes 2.0.0 compiles Qutes programs to Qiskit circuits. The portable CLI includes Python, the Qiskit Aer simulator and circuit-image export.

**Download revision r2** uses `ABC` as the example alphabet. The bundled Bell program runs with the default settings. Tour examples 22 and 30 opt in to `--alphabet "AB?"` to demonstrate storing a wildcard in quantum data. The compiler wheel, language contract (0.4) and artifact schema (5) are the same as in the original 2.0.0 release.

## Download the portable CLI

| Platform | Download | Tested on |
|---|---|---|
| Windows | [x64 ZIP](https://github.com/GabrieleMessina/qutes_lang/releases/download/2.0.0/qutes-2.0.0-r2-windows-x64.zip) | Windows Server 2022 |
| macOS | [Apple Silicon ZIP](https://github.com/GabrieleMessina/qutes_lang/releases/download/2.0.0/qutes-2.0.0-r2-macos-arm64.zip) · [Intel ZIP](https://github.com/GabrieleMessina/qutes_lang/releases/download/2.0.0/qutes-2.0.0-r2-macos-x64.zip) | macOS 15 |
| Linux | [x64 tar.gz](https://github.com/GabrieleMessina/qutes_lang/releases/download/2.0.0/qutes-2.0.0-r2-linux-x64.tar.gz) · [ARM64 tar.gz](https://github.com/GabrieleMessina/qutes_lang/releases/download/2.0.0/qutes-2.0.0-r2-linux-arm64.tar.gz) | Ubuntu 22.04 |

Extract the whole archive and open a terminal in the folder containing the executable. Keep the `_internal` folder beside it.

**Windows PowerShell**

```powershell
.\qutes.exe run examples\bell.qut --shots 64
```

**macOS and Linux**

```sh
./qutes run examples/bell.qut --shots 64
```

The Windows executable is unsigned. The macOS builds have no Developer ID signature or Apple notarization. [SHA-256 checksums for r2](https://github.com/GabrieleMessina/qutes_lang/releases/download/2.0.0/qutes-2.0.0-r2-SHA256SUMS.txt)

## Python and teaching downloads

- [Bell starter project](https://github.com/GabrieleMessina/qutes_lang/releases/download/2.0.0/qutes-starter-2.0.0-r2.zip) — extract it, activate a Python 3.12 or 3.13 virtual environment, and run `python -m pip install --find-links wheels "qutes-lang[backend]==2.0.0"` from the project folder. Run `qutes run main.qut --shots 64`.
- [Teaching bundle](https://github.com/GabrieleMessina/qutes_lang/releases/download/2.0.0/qutes-resources-2.0.0-r2.zip) — includes the 50-program tour, lesson, notebook, presentation and wheels.
- [Compiler wheel](https://github.com/GabrieleMessina/qutes_lang/releases/download/2.0.0/qutes_lang-2.0.0-py3-none-any.whl) — for integrating Qutes into an existing Python environment.
