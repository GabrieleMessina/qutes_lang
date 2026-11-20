"""Build an archive on its target platform in a clean Python 3.12 environment."""
import argparse
import hashlib
from importlib import metadata
import json
import os
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import tarfile
import tempfile

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
VERSION = "2.0.0"
COMMIT = "0367b5211448681485d5943586846997bcff2087"
WHEEL = "qutes_lang-2.0.0-py3-none-any.whl"
DIGEST = "289dfafbab44ccf25d685e4fd28384021947b97c87a4abe1a27821938d27f6d7"


def sha256(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def install(wheel):
    if wheel.name != WHEEL or sha256(wheel) != DIGEST:
        raise ValueError("Expected the published Qutes 2.0.0 wheel and SHA-256")
    if sys.prefix == sys.base_prefix or sys.version_info[:2] != (3, 12):
        raise ValueError("Build in an isolated Python 3.12 virtual environment")
    subprocess.run([sys.executable, "-m", "pip", "install", "--only-binary=:all:", "--no-binary=pylatexenc",
                    "-c", str(ROOT / "requirements-dev.lock"), "setuptools==72.1.0",
                    "pyinstaller==6.16.0", "pyinstaller-hooks-contrib==2025.9",
                    f"qutes-lang[backend,visualization] @ {wheel.resolve().as_uri()}"], check=True)
    subprocess.run([sys.executable, "-m", "pip", "check"], check=True)


def copy_notices(folder):
    licenses = folder / "licenses"
    licenses.mkdir()
    for dist in metadata.distributions():
        for item in dist.files or ():
            name = item.name.lower()
            if not any(word in name for word in ("license", "licence", "copying", "notice")):
                continue
            if item.is_absolute() or ".." in item.parts or name.endswith((".py", ".pyc")):
                continue
            original = Path(dist.locate_file(item))
            if original.is_file():
                target = licenses / dist.metadata["Name"] / item
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(original, target)
    base = Path(sys.base_prefix)
    for license_file in (base / "LICENSE.txt", base / "LICENSE", Path(os.__file__).parent / "LICENSE.txt"):
        if license_file.is_file():
            shutil.copyfile(license_file, licenses / "Python-LICENSE.txt")
            break
    else:
        raise FileNotFoundError("CPython distribution license")


def build(wheel, output):
    install(wheel)
    operating_system = {"Windows": "windows", "Darwin": "macos", "Linux": "linux"}[platform.system()]
    arch = {"amd64": "x64", "x86_64": "x64", "arm64": "arm64", "aarch64": "arm64"}[platform.machine().lower()]
    name = f"qutes-{VERSION}-r2-{operating_system}-{arch}"
    output.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="qutes-build-") as temp:
        work = Path(temp)
        subprocess.run([sys.executable, "-m", "PyInstaller", "--noconfirm", "--distpath", str(work / "dist"),
                        "--workpath", str(work / "intermediate"), str(HERE / "qutes.spec")], cwd=work, check=True)
        folder = work / name
        (work / "dist" / "qutes").rename(folder)
        examples = folder / "examples"
        examples.mkdir()
        # Keep the compiler-era program and credits, and use this packaging revision’s defaults.
        shutil.copyfile(ROOT / "examples/language/qutes.toml", examples / "qutes.toml")
        for dest, source in ((examples / "bell.qut", "examples/language/41_bell_gates.qut"),
                             (folder / "LICENSE", "LICENSE"), (folder / "CITATION.cff", "CITATION.cff")):
            dest.write_bytes(subprocess.check_output(["git", "show", f"{COMMIT}:{source}"], cwd=ROOT))
        copy_notices(folder)
        shutil.copyfile(HERE / "QUICKSTART.md", folder / "README.md")
        receipt = {"version": VERSION, "compiler_commit": COMMIT, "wheel_sha256": DIGEST,
                   "packaging_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
                   "system": platform.platform(), "architecture": arch, "python": platform.python_version(),
                   "dependencies": {d.metadata["Name"]: d.version for d in metadata.distributions()}}
        (folder / "build-info.json").write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
        if operating_system == "linux":
            archive = output / (name + ".tar.gz")
            with tarfile.open(archive, "w:gz", compresslevel=6) as stream:
                stream.add(folder, arcname=name)
        elif operating_system == "macos":
            archive = output / (name + ".zip")
            subprocess.run(["ditto", "-c", "-k", "--keepParent", str(folder), str(archive)], check=True)
        else:
            archive = Path(shutil.make_archive(str(output / name), "zip", work, name))
        print(sha256(archive), archive.name)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("wheel", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    build(args.wheel.resolve(), args.output.resolve())
