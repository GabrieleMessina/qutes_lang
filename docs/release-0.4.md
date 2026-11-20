# Public release preparation

The compiler in this branch was imported from the validated rewrite at e1c78a8 (qutes_lang_chatgpt). Its parent branch is development of GabrieleMessina/qutes_lang. The existing MIT license, citation metadata and publication credits apply.

The previous playground/Home.ipynb uses the legacy compiler entry point. The VS Code grammar and wiki describe earlier syntax. The earlier requirements and Codespaces setup install that implementation. Use the 0.4 notebook, pyproject, CLI guide and active specification on this branch. Previous versions remain available on development.

The [Qutes 2.0.0 release](https://github.com/GabrieleMessina/qutes_lang/releases/tag/2.0.0) offers five portable CLI archives and their SHA-256 checksums. Each platform build installs the compiler from Git commit `0367b5211448681485d5943586846997bcff2087` and uses the example configuration from the packaging branch.

To build on a native target, activate a clean Python 3.12 virtual environment in a full checkout and run:

```text
python tools/portable/build.py dist
```

The portable workflow runs `python -I tools/portable/verify.py PATH_TO_ARCHIVE` on a fresh runner for each target. The publisher accepts verified archives and refuses to replace a file with different bytes. Use a new revision name when changing a distributed build.

The dependency pins and schema 5 contract are described in the guide. Report onboarding issues with the example name, package version, platform, and the edit that produced the problem.
