"""Exercise only the previously built archive on a separate clean runner."""
import argparse
import ast
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tarfile
import tempfile
import xml.etree.ElementTree as ET
import zipfile


def verify(archive, work):
    if archive.name.endswith(".tar.gz"):
        with tarfile.open(archive) as reader:
            reader.extractall(work, filter="data")
    elif sys.platform == "darwin":
        subprocess.run(["ditto", "-x", "-k", str(archive), str(work)], check=True)
    else:
        with zipfile.ZipFile(archive) as reader:
            reader.extractall(work)
    folder, = work.glob("qutes-2.0.0-*")
    installed = work / "Relocated Qutes CLI"
    folder.rename(installed)
    exe = installed / ("qutes.exe" if os.name == "nt" else "qutes")
    project = work / "Learner project"
    project.mkdir()
    empty = work / "empty path"
    empty.mkdir()
    # No checkout, virtualenv, host Python, graphical session or cached user packages for the CLI.
    env = {k: os.environ[k] for k in ("SYSTEMROOT", "WINDIR", "COMSPEC", "TEMP", "TMP", "TMPDIR")
           if k in os.environ}
    env.update(PATH=str(empty), HOME=str(project), USERPROFILE=str(project), PYTHONNOUSERSITE="1",
               MPLCONFIGDIR=str(project / "mpl"), OPENBLAS_NUM_THREADS="1", OMP_NUM_THREADS="1")
    assert not shutil.which("python", path=env["PATH"])

    def cli(*args, success=True):
        result = subprocess.run([exe, *args], cwd=project, env=env, capture_output=True,
                                encoding="utf-8", errors="replace", timeout=120, stdin=subprocess.DEVNULL)
        if (result.returncode == 0) != success:
            raise RuntimeError(f"{args} returned {result.returncode}\n{result.stdout}\n{result.stderr}")
        if "QW0001" in result.stderr:
            raise AssertionError(f"Unexpected wildcard warning from {args}: {result.stderr}")
        return result.stdout

    assert cli("--version").strip() == "2.0.0"
    assert (installed / "licenses/Python-LICENSE.txt").stat().st_size > 100
    receipt = json.loads((installed / "build-info.json").read_text(encoding="utf-8"))
    assert receipt["wheel_sha256"] == "289dfafbab44ccf25d685e4fd28384021947b97c87a4abe1a27821938d27f6d7"
    bell = installed / "examples/bell.qut"
    assert "QW0001" not in cli("check", bell, "--json")
    assert "QW0001" in cli("check", bell, "--alphabet", "AB?", "--json")

    def run(source):
        return json.loads(cli("run", source, "--shots", "64", "--seed", "17", "--json"))["outcomes"]

    counts = run(bell)
    assert {tuple(row["value"]) for row in counts} == {(False, False), (True, True)}, counts
    assert sum(row["count"] for row in counts) == 64
    for stage in ("parse", "analyze", "construct"):
        assert json.loads(cli(stage, bell, "--json"))["stage"]
    source = project / "phase.qut"
    source.write_text("qubit q=false; hadamard(q); phaseFlip(q); hadamard(q); return measure(q);")
    assert run(source) == [{"value": True, "count": 64, "probability": 1.0}]
    shutil.copyfile(installed / "examples/qutes.toml", project / "qutes.toml")
    source.write_text("quint n=1; for(int i=0;i<12;i++){quint t=n+1; n+=1;} return measure(n);")
    resources = json.loads(cli("explain", source, "--json"))["resources"]
    assert (resources["logical_allocated_qubits"], resources["allocated_qubits"]) == (39, 6)
    assert run(source)[0]["value"] == -3
    cli("build", bell, "-o", "bell_export.py")
    generated = (project / "bell_export.py").read_text(encoding="utf-8")
    assert {"build", "run"} <= {node.name for node in ast.parse(generated).body if isinstance(node, ast.FunctionDef)}
    for fmt in ("png", "svg"):
        result = json.loads(cli("check", bell, "--save-circuit", "images", "--circuit-format", fmt, "--json"))
        image = Path(result["circuit_diagram"]["image"])
        # Windows runner TEMP can use a short (8.3) alias for the same directory.
        assert image.parent.samefile(project / "images"), (image, project)
        assert image.stat().st_size > 1000, (image, image.stat().st_size)
        if fmt == "png":
            assert image.read_bytes()[:8] == b"\x89PNG\r\n\x1a\n"
        else:
            assert ET.parse(image).getroot().tag.endswith("}svg")
    source.write_text("qubit q = ;")
    diagnostic = json.loads(cli("check", source, "--json", success=False))["diagnostics"][0]
    assert diagnostic["code"].startswith("Q") and diagnostic["message"]
    print(f"{archive.name}: archived CLI passed all seven commands, Bell, phase, reuse, PNG/SVG and diagnostics")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive", type=Path)
    args = parser.parse_args()
    with tempfile.TemporaryDirectory(prefix="Qutes clean machine ") as temp:
        verify(args.archive.resolve(), Path(temp))
