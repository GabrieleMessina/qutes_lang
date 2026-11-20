# Current status

GitHub release `2.0.0` distributes the full CLI for Windows x64, macOS ARM64 and x64, and Linux ARM64 and x64. The five r2 archives use compiler commit 0367b52 and ship ABC as the default example alphabet. The earlier Git tag `2.0` identifies merge 6bc0ecf on `qutes2.0`. Its second parent e1c78a8 brings in all 30 original rewrite commits; its tree matches first parent d4410ae. The 2.0.0 release uses package version 2.0.0, language contract 0.4 and artifact schema 5. The original MIT license, citation and publication credits are retained.

- [Release and downloads](https://github.com/GabrieleMessina/qutes_lang/releases/tag/2.0.0)
- [Live playground](https://qutes-lang.web.app/play.html) with Teach, Build and Inspect routes.
- [Resources](../../resources/README.md) in the language repository root tree.
- [Language 0.4 specification](../spec/language-v0.4.md), [compiler audit](../v04-audit.md), and [release integration](../release-0.4.md).
- [Hosted compiler matrix](https://github.com/GabrieleMessina/qutes_lang/actions/runs/44785749075) passed 1,032 tests on each of Ubuntu and Windows with Python 3.12 and 3.13.
- Previous deployment: [hosted preview](https://github.com/GabrieleMessina/qutes_website/actions/runs/44791119262) and [production deployment](https://github.com/GabrieleMessina/qutes_website/actions/runs/44791968090) passed. Website tag qutes-site-2.0 resolves to 0af23e4eebf910fa613fac093a1ce9517d3235e7.

## Working defaults and limits

The 50-example tour runs locally. Four browser examples are verified. Edited sources execute on-device within the published limits of 10 physical qubits, 128 shots and a bounded work budget. Phase/correlation, cleanup, mid-circuit measurement, diagnostics, cancellation, Qiskit Python export and a clean Qiskit notebook are verified. Browser validation used Chromium, Firefox and Playwright WebKit. Native Safari was not exercised. Local execution uses the ideal Aer simulator.

Both repositories use their own `qutes2.0` branch. Native packaging installs the compiler from its exact Git release commit. The local website builds its browser compiler from checksum-pinned language source and parser code.

## Resume

For the CLI, start at the release page linked above. The repository keeps the example tour, notebook, presentations and lessons as editable sources. Windows binaries are unsigned. macOS binaries have no Developer ID signature or notarization.

The owner asked to keep all website changes local. The deployed site's direct GitHub download links can be stale until the owner approves deployment. The updated local Build page offers the five platform downloads and their checksums.

For language development, use Python 3.12 or 3.13 in a virtual environment and run `python tools/check.py -q`. For a website preview, use `npm ci` and `python scripts/build.py` in the website checkout. Verification history is in VALIDATION and LEDGER.
