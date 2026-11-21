# Public release preparation

The compiler in this branch was imported from the validated rewrite at e1c78a8 (qutes_lang_chatgpt). Its parent branch is development of GabrieleMessina/qutes_lang. The existing MIT license, citation metadata and publication credits apply.

The previous playground/Home.ipynb uses the legacy compiler entry point. The VS Code grammar and wiki describe earlier syntax. The earlier requirements and Codespaces setup install that implementation. Use the 0.4 notebook, pyproject, CLI guide and active specification on this branch. Previous versions remain available on development.

The [Qutes 2.0.1 release](https://github.com/GabrieleMessina/qutes_lang/releases/tag/2.0.1) supplies five portable archives and their SHA-256 checksums. Each build used the tagged source at `1c560fd02b2bd1c7a43f92042e85ca882169e01b`. The build receipt inside each archive records its exact compiler, Python and dependencies.

To reproduce a native build, check out the release tag, activate an isolated Python 3.12.16 environment on the target architecture, and run these commands. Replace ARCHIVE with the built archive path.

```text
python tools/portable/build.py dist
python -I tools/portable/verify.py ARCHIVE --commit 1c560fd02b2bd1c7a43f92042e85ca882169e01b
```

The release workflow verifies the five built archives on separate clean runners before tagging and publishing their exact bytes. Subsequent security updates use a new version. The [2.0.0 release](https://github.com/GabrieleMessina/qutes_lang/releases/tag/2.0.0) retains the original r2 files.

The dependency pins and schema 5 contract are described in the guide. Report onboarding issues with the example name, package version, platform, and the edit that produced the problem.
