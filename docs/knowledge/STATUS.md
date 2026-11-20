# Current status

The public Git tag `2.0` identifies merge 6bc0ecf on `qutes2.0`. Its second parent e1c78a8 brings in all 30 original rewrite commits; its tree matches first parent d4410ae. The 2.0.0 release uses package version 2.0.0, language contract 0.4 and artifact schema 5. The original MIT license, citation and publication credits are retained.

- [Release and downloads](https://github.com/GabrieleMessina/qutes_lang/releases/tag/2.0.0)
- [Live playground](https://qutes-lang.web.app/play.html) with Teach, Build and Inspect routes.
- [Resources](../../resources/README.md) in the language repository root tree.
- [Language 0.4 specification](../spec/language-v0.4.md), [compiler audit](../v04-audit.md), and [release integration](../release-0.4.md).
- [Hosted compiler matrix](https://github.com/GabrieleMessina/qutes_lang/actions/runs/44785749075) passed 1,032 tests on each of Ubuntu and Windows with Python 3.12 and 3.13.
- [Hosted preview](https://github.com/GabrieleMessina/qutes_website/actions/runs/44791119262) and [production deployment](https://github.com/GabrieleMessina/qutes_website/actions/runs/44791968090) passed. Website tag qutes-site-2.0 resolves to 0af23e4eebf910fa613fac093a1ce9517d3235e7.

## Working defaults and limits

The 50-example tour runs locally. Four browser examples are verified. Edited sources execute on-device within the published limits of 10 physical qubits, 128 shots and a bounded work budget. Phase/correlation, cleanup, mid-circuit measurement, diagnostics, cancellation, project export and a clean Qiskit notebook are verified. Browser validation used Chromium, Firefox and Playwright WebKit. Native Safari was not exercised. Local execution uses the ideal Aer simulator.

The two repositories use separate release branches. Website builds verify the resource archive checksum and compiler commit. The standalone starter is a companion release asset. Use resources/starters/build_starter.py to reproduce it from the published bundle. The existing website main branch still has its previous Firebase workflow; coordinate future merges and deployments with the release branch.

## Resume

T034 is preparing versioned compiler and website downloads. Verify the wheel and the pinned resource bundle before dispatching the website deployment on qutes2.0.

From the language checkout, use Python 3.12 or 3.13 in a virtual environment. Install dependencies with `python -m pip install -r requirements-dev.lock`, run `python tools/check.py -q` and `python tools/verify_walkthrough.py`. From the website checkout use `npm ci`, `python scripts/build.py`, and the browser checks documented there. Exact verification runs and failed attempts are in VALIDATION and LEDGER.
