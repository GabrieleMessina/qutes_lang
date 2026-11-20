"""Execute each published CLI walkthrough command against the current checkout."""
import json
import os
from pathlib import Path
import shlex
import subprocess
import sys


def main():
    root = Path(__file__).resolve().parents[1]
    environment = dict(os.environ, PYTHONPATH=str(root / "src"))
    (root / "artifacts").mkdir(exist_ok=True)
    report = []
    fenced = False
    for line in (root / "docs/cli-walkthrough.md").read_text(encoding="utf-8").splitlines():
        if line.startswith("```"):
            fenced = not fenced
            continue
        if not fenced or not line.startswith(("qutes ", "python artifacts/")):
            continue
        arguments = shlex.split(line)
        command = [sys.executable, str(root / "tools/qutes.py"), *arguments[1:]] if arguments[0] == "qutes" else [sys.executable, *arguments[1:]]
        result = subprocess.run(command, cwd=root, env=environment, capture_output=True, text=True, encoding="utf-8")
        report.append({"command": line, "exit_code": result.returncode})
        if result.returncode:
            print(result.stdout + result.stderr)
            raise SystemExit(f"Walkthrough failed: {line}")
    output = root / "artifacts" / "walkthrough-v04.json"
    output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(f"{len(report)} documented commands passed; evidence: {output}")


if __name__ == "__main__":
    main()
