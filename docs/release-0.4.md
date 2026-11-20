# Public release preparation

The compiler in this branch was imported from the validated rewrite at e1c78a8 (qutes_lang_chatgpt). Its parent branch is development of GabrieleMessina/qutes_lang. The existing MIT license, citation metadata and publication credits apply.

The previous playground/Home.ipynb uses the legacy compiler entry point. The VS Code grammar and wiki describe earlier syntax. The earlier requirements and Codespaces setup install that implementation. Use the 0.4 notebook, pyproject, CLI guide and active specification on this branch. Previous versions remain available on development.

Build from a clean release commit in an environment with the pinned build requirements and wheel installed:

```text
python tools/build_resource_bundle.py dist/qutes-resources-0.4.0.zip
```

The archive contains the compiler wheel, its parser runtime, the tour configuration, canonical examples, and resources. Publish these bytes once and pin the reported Git commit and archive SHA-256 in the website. Wheels can include build timestamps. Rebuilding the same source can produce a different archive hash.

Use the supplied wheel for local installation. The dependency pins and schema 5 contract are described in the guide. Report onboarding issues with the example name, package version, platform, and the edit that produced the problem.
