# Current status

GitHub release `2.0.0` publishes the wheel, teaching bundle and starter from 0367b52. The earlier Git tag `2.0` identifies merge 6bc0ecf on `qutes2.0`. Its second parent e1c78a8 brings in all 30 original rewrite commits; its tree matches first parent d4410ae. The 2.0.0 release uses package version 2.0.0, language contract 0.4 and artifact schema 5. The original MIT license, citation and publication credits are retained.

- [Release and downloads](https://github.com/GabrieleMessina/qutes_lang/releases/tag/2.0.0)
- [Live playground](https://qutes-lang.web.app/play.html) with Teach, Build and Inspect routes.
- [Resources](../../resources/README.md) in the language repository root tree.
- [Language 0.4 specification](../spec/language-v0.4.md), [compiler audit](../v04-audit.md), and [release integration](../release-0.4.md).
- [Hosted compiler matrix](https://github.com/GabrieleMessina/qutes_lang/actions/runs/44785749075) passed 1,032 tests on each of Ubuntu and Windows with Python 3.12 and 3.13.
- Previous deployment: [hosted preview](https://github.com/GabrieleMessina/qutes_website/actions/runs/44791119262) and [production deployment](https://github.com/GabrieleMessina/qutes_website/actions/runs/44791968090) passed. Website tag qutes-site-2.0 resolves to 0af23e4eebf910fa613fac093a1ce9517d3235e7.

## Working defaults and limits

The 50-example tour runs locally. Four browser examples are verified. Edited sources execute on-device within the published limits of 10 physical qubits, 128 shots and a bounded work budget. Phase/correlation, cleanup, mid-circuit measurement, diagnostics, cancellation, project export and a clean Qiskit notebook are verified. Browser validation used Chromium, Firefox and Playwright WebKit. Native Safari was not exercised. Local execution uses the ideal Aer simulator.

The two repositories use separate release branches. Website builds verify the resource archive checksum and compiler commit. The standalone starter is a companion release asset. Use resources/starters/build_starter.py to reproduce it from the published bundle. The existing website main branch still has its previous Firebase workflow; coordinate future merges and deployments with the release branch.

## Resume

T030–T034 are complete through the requested deployment dispatch. Both repositories use qutes2.0. Website tag qutes-site-2.0.0 targets b480812 and pins the 2.0.0 release bundle. Preview and production workflows were dispatched without waiting for their outcome at user request. For a subsequent deployment audit, check the tag workflow and live manifest.

From the language checkout, use Python 3.12 or 3.13 in a virtual environment. Install dependencies with `python -m pip install -r requirements-dev.lock`, run `python tools/check.py -q` and `python tools/verify_walkthrough.py`. From the website checkout use `npm ci`, `python scripts/build.py`, and the browser checks documented there. Exact verification runs and failed attempts are in VALIDATION and LEDGER.

Local website review checkpoint: website qutes2.0 at 8daa5d9 is four local commits ahead of origin. Review http://127.0.0.1:4197/tutorial.html and http://127.0.0.1:4197/build.html. Tutorial foundations are in the first two labs. Build contains platform downloads and first-run commands pinned to public r2 archives. Publication awaits owner review.

Portable release checkpoint: T037 completed. The 2.0.0 GitHub release now offers the full portable CLI for Windows x64, macOS Intel and Apple Silicon, and Ubuntu-baseline Linux x64 and ARM64. Packaging run 44809167547 passed all five clean extractions, published the archives and successfully downloaded and hashed each public asset. For a future version, update the wheel identity, dependency lock, version, tag and target matrix before building new versioned assets. Windows binaries are unsigned and macOS binaries have no Developer ID signature or notarization.

T039 release checkpoint: the GitHub release description points readers to the r2 downloads. Five native archives, the Python starter and the teaching bundle now default to ABC. Run 44813512817 verified every platform and the final public files. The published r2 resource SHA-256 is afc6dc2efcd9964dafbd03480679be6990856ffedabc9ef79703de47088dcf1b. Use this digest and the r2 resource URL when building a site preview.
