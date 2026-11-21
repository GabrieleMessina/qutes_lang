# Current status

[Qutes 2.0.1](https://github.com/GabrieleMessina/qutes_lang/releases/tag/2.0.1) distributes the CLI for Windows x64, macOS ARM64 and x64, and Linux ARM64 and x64. All five archives use compiler commit `1c560fd`, Python 3.12.16, Pillow 13.0.0, fontTools 4.68.0, and the ABC example alphabet. The [2.0.0 release](https://github.com/GabrieleMessina/qutes_lang/releases/tag/2.0.0) retains its original six assets and points users to 2.0.1.

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

For the next patch, merge through the protected branches, verify the portable build from the final compiler revision, then pin the website to that revision. Only the website's `hosting.yml` workflow promotes a release to production. It uses separate Google identities and projects for preview and production, verifies the same site artifact on each and runs the public tutorial and download checks. Use an explicit live dispatch on `qutes2.0`.

## Local developer-tool candidate

The shared editor vocabulary, completion service, packaged desktop extension and circuit inspection are in local review. Native editor verification uses an installed VSIX and an isolated profile. Run the instructions in qutes-vscode/README.md and the manual editor-candidates workflow before Marketplace publication.

All five 2.0.1 extension packages passed on their native architectures in [the candidate workflow](https://github.com/GabrieleMessina/qutes_lang/actions/runs/44951396964). The local 2.0.4 debugger shows in-scope Qutes names and physical wire assignments beside the joint state while stepping. The Windows x64 package passed installed-extension checks and is installed in the owner's VS Code. The website preview uses website commit e148d06 and pins language efd784f, which contains the shared browser modules and circuit report. Local preview at http://127.0.0.1:4288/play.html. See the VS Code README to rebuild and retest the packages. Local review precedes website deployment and Marketplace publication.
