Qutes 2.0.1 compiles Qutes programs to Qiskit circuits. The portable CLI includes Python, the Qiskit Aer simulator and circuit-image export.

This security patch updates the bundled interpreter to Python 3.12.16 on all five platforms, Pillow to 13.0.0 and fontTools to 4.68.0.

## Download the portable CLI

| Platform | Download | Tested on |
|---|---|---|
| Windows | [x64 ZIP](https://github.com/GabrieleMessina/qutes_lang/releases/download/2.0.1/qutes-2.0.1-windows-x64.zip) | Windows Server 2022 |
| macOS | [Apple Silicon ZIP](https://github.com/GabrieleMessina/qutes_lang/releases/download/2.0.1/qutes-2.0.1-macos-arm64.zip) · [Intel ZIP](https://github.com/GabrieleMessina/qutes_lang/releases/download/2.0.1/qutes-2.0.1-macos-x64.zip) | macOS 15 |
| Linux | [x64 tar.gz](https://github.com/GabrieleMessina/qutes_lang/releases/download/2.0.1/qutes-2.0.1-linux-x64.tar.gz) · [ARM64 tar.gz](https://github.com/GabrieleMessina/qutes_lang/releases/download/2.0.1/qutes-2.0.1-linux-arm64.tar.gz) | Ubuntu 22.04 |

Extract the whole archive and open a terminal in the folder containing the executable. Keep the `_internal` folder beside it.

**Windows PowerShell**

```powershell
.\qutes.exe run examples\bell.qut --shots 64
```

**macOS and Linux**

```sh
./qutes run examples/bell.qut --shots 64
```

The Windows executable is unsigned. The macOS builds have no Developer ID signature or Apple notarization. [SHA-256 checksums for 2.0.1](https://github.com/GabrieleMessina/qutes_lang/releases/download/2.0.1/qutes-2.0.1-SHA256SUMS.txt)
