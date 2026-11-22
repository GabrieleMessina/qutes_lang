# Current status

[Qutes 2.0.1](https://github.com/GabrieleMessina/qutes_lang/releases/tag/2.0.1) distributes the CLI for Windows x64, macOS ARM64 and x64, and Linux ARM64 and x64. All five archives use compiler commit `1c560fd`, Python 3.12.16, Pillow 13.0.0, fontTools 4.68.0, and the ABC example alphabet. The [2.0.0 release](https://github.com/GabrieleMessina/qutes_lang/releases/tag/2.0.0) retains its release notes and points users to 2.0.1. Its superseded assets and the six binaries attached to the historical Latest Build prerelease were removed.

- [Tutorial](https://qutes-lang.web.app/tutorial), [playground](https://qutes-lang.web.app/play) and [platform downloads](https://qutes-lang.web.app/downloads).
- [Editable resources](../../resources/README.md), [language specification](../spec/language-v0.4.md) and [native release instructions](../release-0.4.md).
- [Compiler matrix](https://github.com/GabrieleMessina/qutes_lang/actions/runs/44896494115) on Ubuntu and Windows with Python 3.12 and 3.13.
- [Clean-runner verification and publication of all five archives](https://github.com/GabrieleMessina/qutes_lang/actions/runs/44896877774).
- [Website verification and production deployment](https://github.com/GabrieleMessina/qutes_website/actions/runs/44898076520).

## Release and language contracts

Both repositories require pull requests and successful GitHub Actions checks on `qutes2.0`, including for administrators. Only one maintainer was available when protection was configured. The new release uses language contract 0.4 and artifact schema 5. The original MIT license, citation and publication credits apply. The earlier tag `2.0` identifies merge `6bc0ecf`. Its second parent `e1c78a8` preserves the rewrite history.

The live workbook uses 17 chapters and three optional extensions. It runs bounded experiments in the browser and exports standalone Qiskit programs. CLI-generated Python uses the Qutes backend. Native Safari was outside browser validation. Windows binaries are unsigned, and macOS binaries have no Developer ID signature or notarization.

## Resume

For compiler development, use Python 3.12 or 3.13 in a virtual environment and run `python tools/check.py -q`. For website development, run `npm ci`, build with `python scripts/build.py`, serve `dist/` and run `npm test`. The 50-example tour and editable study experiments live in this repository.

For a portable compiler update, verify the build from the final compiler revision before updating its website links. The website's `hosting.yml` workflow builds and tests every push to `qutes2.0`, deploys that artifact to production, then checks the hosted compiler, tutorial and downloads. A push to `qutes2.0-dev` follows the same process for the separate preview project.

## Website and desktop developer tools

The public website uses the shared language service in the playground, workbook and practice labs. All five 2.0.6 VSIX downloads from the [existing Marketplace listing](https://marketplace.visualstudio.com/items?itemName=GabrieleMessina.qutes) matched the tested files in V066. Microsoft marked both macOS and Linux architectures validated. Windows x64 was still in review at the last check, and a clean Windows install selected 1.2.1. Live polling stopped at the owner's request. The [language README](../../README.md#run-and-debug-in-vs-code) covers installation and debugging Bell.

All five 2.0.6 RC1 extension packages from `ea40fdf` passed native installation and debugging in workspace and single-file sessions on Windows x64, macOS Intel and Apple Silicon, and Linux x64 and ARM64. The debugger shows qubit probabilities and expandable distributions for signed integers, characters, strings and small quantum arrays. [Native package verification](https://github.com/GabrieleMessina/qutes_lang/actions/runs/45009272870).

Website merge `8b2f29d` deployed the reviewed files from `8265174` with the compiler pinned to `ea40fdf`. The [Bell playground](https://qutes-lang.web.app/play#bell) and [circuit builder](https://qutes-lang.web.app/play#sketch) passed live browser checks. See V067 for local candidate verification and V068 for the [production release](https://github.com/GabrieleMessina/qutes_website/actions/runs/45012044702).

Automatic extension publishing is live on `qutes2.0`. The [first protected-branch run](https://github.com/GabrieleMessina/qutes_lang/actions/runs/45022170891) passed four compiler checks and five native installation tests, verified the five packages, and authenticated with the Marketplace. This setup run skipped upload. A future stable extension version bump triggers submission of the tested files without a separate approval. See the [release instructions](../../qutes-vscode/README.md#release-a-new-extension-version).

The five-platform extension workflow has two entry points: the release workflow and a manual candidate check. Ordinary pushes to verification branches run the normal compiler CI.

The publisher uses the historical `vscode-extension` environment. Its branch rule now names `qutes2.0`; the 15 original deployment records are retained. Run a check-only dispatch to validate Marketplace trust following an environment change.

Local public documentation preview starts with docs/README.md and docs/reference/measurement.md. Website publication awaits review.

The local public manual now includes 14 reference topics. Source lives under docs/reference with docs/README.md as the navigation index. It is ready for website review.

The GitHub Wiki home and all 14 public reference topics now mirror the Markdown manual. Edit docs/README.md and docs/reference/ on qutes2.0 for ongoing publication.
