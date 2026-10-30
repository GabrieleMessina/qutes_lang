"""Run repository tests with isolated pytest plugins and workspace-local artifacts."""

import importlib.metadata
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
import tempfile


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    artifacts = root / "artifacts" / "checks"
    artifacts.mkdir(parents=True, exist_ok=True)
    run = Path(tempfile.mkdtemp(prefix="run-", dir=artifacts)).resolve()
    if not run.is_relative_to(artifacts.resolve()):
        raise RuntimeError("test output must stay inside the repository artifacts directory")
    # pytest may clear its basetemp: pass a fresh, task-owned subdirectory only.
    command = [sys.executable, "-m", "pytest", "--basetemp", str(run / "tmp"),
               "--junitxml", str(run / "results.xml"), *sys.argv[1:]]
    environment = dict(os.environ, PYTEST_DISABLE_PLUGIN_AUTOLOAD="1")
    result = subprocess.run(command, cwd=root, env=environment, check=False)
    versions = {}
    for name in ("qiskit", "qiskit-aer", "numpy", "pytest"):
        try:
            versions[name] = importlib.metadata.version(name)
        except importlib.metadata.PackageNotFoundError:
            versions[name] = None
    report = {
        "python": platform.python_version(), "platform": platform.platform(),
        "versions": versions, "command": command, "returncode": result.returncode,
        "junit": str(run / "results.xml"),
    }
    (run / "environment.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(f"Validation artifacts: {run}", flush=True)
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
