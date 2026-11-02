"""Verify the installed wheel, without checkout import paths or user-site packages."""

import importlib.util
import json
from pathlib import Path
import platform
import subprocess
import sys
import tempfile


def main():
    import qutes
    from qutes.codegen import write_python
    from qutes.compiler import compile_source, dependency_versions
    from qutes.config import CompilerConfig

    root = Path(__file__).resolve().parents[1]
    installed = Path(qutes.__file__).resolve()
    if installed.is_relative_to(root / "src") or not installed.is_relative_to(Path(sys.prefix).resolve()):
        raise RuntimeError(f"expected isolated installed package, got {installed}")
    output = root / "artifacts" / "installation"
    output.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="smoke-", dir=output) as temporary:
        folder = Path(temporary)
        source = folder / "smoke.qut"
        source.write_text('input int start;  quint n=start; int before=measure(n); n+=1; return [before,measure(n)]; ', encoding="utf-8")
        inputs = folder / "inputs.json"
        inputs.write_text('{"start":2}', encoding="utf-8")
        command = [sys.executable, "-I", "-m", "qutes", "run", str(source), "--inputs", str(inputs),
                   "--quint-bits", "3", "--shots", "8", "--seed", "17", "--json"]
        result = subprocess.run(command, cwd=folder, capture_output=True, text=True, check=True)
        cli = json.loads(result.stdout)
        assert cli["outcomes"] == [{"value": [2, 3], "count": 8, "probability": 1.0}]
        compilation = compile_source(source.read_text(), inputs={"start": 2}, config=CompilerConfig(quint_bits=3))
        artifact = folder / "generated.py"
        write_python(compilation, artifact)
        spec = importlib.util.spec_from_file_location("generated_smoke", artifact)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        outcomes = module.run({"start": 3}, shots=8, seed=17)["outcomes"]
        assert outcomes == [{"value": [3, -4], "count": 8, "probability": 1.0}]
    report = {"python": platform.python_version(), "platform": platform.platform(), "qutes": qutes.__version__,
              "installed_path": str(installed), "dependencies": dependency_versions(),
              "isolated_cli": "passed", "generated_module_respecialization": "passed"}
    target = output / ("windows.json" if sys.platform == "win32" else "linux.json")
    target.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
