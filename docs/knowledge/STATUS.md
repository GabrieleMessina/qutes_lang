# Current status

Qutes 0.4.0 is public. The release compiler is language 0.4, artifact schema 5, from the validated rewrite e1c78a8. The published language tag v0.4.0 resolves to a78cc16ec2192aa19f3147aa5e154a68db4f78c4 on the release branch. The original MIT license, citation and publication credits are retained.

- [Release and downloads](https://github.com/GabrieleMessina/qutes_lang/releases/tag/v0.4.0)
- [Live playground](https://qutes-lang.web.app/play.html) with Teach, Build and Inspect routes.
- [Resources](../../resources/README.md) in the language repository root tree.
- [Language 0.4 specification](../spec/language-v0.4.md), [compiler audit](../v04-audit.md), and [release integration](../release-0.4.md).
- [Hosted compiler matrix](https://github.com/GabrieleMessina/qutes_lang/actions/runs/44785749075) passed 1,032 tests on each of Ubuntu and Windows with Python 3.12 and 3.13.
- [Hosted preview](https://github.com/GabrieleMessina/qutes_website/actions/runs/44786813596) and [production deployment](https://github.com/GabrieleMessina/qutes_website/actions/runs/44787628431) passed. Website tag qutes-site-0.4.0 resolves to 466bfe430e358dab5483c4fa88712544a3fb7e1d.

## Working defaults and limits

The 50-example tour runs locally. Four browser examples are verified. Edited sources execute on-device within the published limits of 10 physical qubits, 128 shots and a bounded work budget. Phase/correlation, cleanup, mid-circuit measurement, diagnostics, cancellation, project export and a clean Qiskit notebook are verified. Browser validation used Chromium, Firefox and Playwright WebKit. Native Safari was not exercised. Local execution uses the ideal Aer simulator.

The two repositories use separate release branches. Website builds verify the resource archive checksum and compiler commit. The standalone starter is a companion release asset. Use resources/starters/build_starter.py to reproduce it from the published bundle. The existing website main branch still has its previous Firebase workflow; coordinate future merges and deployments with the release branch.

## Resume

T030 and T031 are complete. Next action is to triage onboarding feedback via the issue link on the site. No implementation or deployment blockers remain for this release.

From the language checkout, use Python 3.12 or 3.13 in a virtual environment. Install dependencies with `python -m pip install -r requirements-dev.lock`, run `python tools/check.py -q` and `python tools/verify_walkthrough.py`. From the website checkout use `npm ci`, `python scripts/build.py`, and the browser checks documented there. Exact verification runs and failed attempts are in VALIDATION and LEDGER.
