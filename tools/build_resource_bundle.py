"""Bundle a clean, committed release and its pure Python wheels for static hosting."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import tomllib
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

ROOT = Path(__file__).resolve().parents[1]


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT).decode().strip()


def pack(destination, entries):
    with ZipFile(destination, "w") as archive:
        for name, data in sorted(entries.items()):
            info = ZipInfo(name, (2026, 1, 1, 0, 0, 0))
            info.compress_type = ZIP_DEFLATED
            archive.writestr(info, data)


def released_wheels(bundle):
    with bundle.open("rb") as stream:
        if hashlib.file_digest(stream, "sha256").hexdigest() != "30819d5be08edd3357fa94cbc9c1af38876513c22854e5ccb7669a4f48a3cc1f":
            raise ValueError("Expected the original published Qutes 2.0.0 resource bundle")
        with ZipFile(stream) as archive:
            manifest = json.loads(archive.read("manifest.json"))
            return manifest["commit"], {f"wheels/{w}": archive.read(f"wheels/{w}") for w in manifest["wheels"]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    parser.add_argument("--reuse-2-0-0-wheels", type=Path, help="original release ZIP for a resources-only revision")
    parser.add_argument("--starter-output", type=Path)
    args = parser.parse_args()
    if git("status", "--porcelain", "--untracked-files=normal"):
        raise SystemExit("Commit the release before building its bundle.")
    commit = git("rev-parse", "HEAD")
    project = tomllib.loads((ROOT / "pyproject.toml").read_text())["project"]
    compiler_commit = commit
    if args.reuse_2_0_0_wheels:
        if project["version"] != "2.0.0":
            raise ValueError("The pinned wheels are for compiler 2.0.0")
        compiler_commit, entries = released_wheels(args.reuse_2_0_0_wheels)
    else:
        with tempfile.TemporaryDirectory() as temporary:
            folder = Path(temporary)
            subprocess.run([sys.executable, "-m", "pip", "wheel", "--no-build-isolation",
                            "--wheel-dir", str(folder), str(ROOT)], check=True)
            wheels = sorted(folder.glob("*.whl"))
            if len(wheels) != 2 or any(not p.name.endswith("-none-any.whl") for p in wheels):
                raise SystemExit("Expected the portable compiler and ANTLR wheels.")
            entries = {f"wheels/{p.name}": p.read_bytes() for p in wheels}
    wheel_names = sorted(Path(name).name for name in entries)
    paths = git("ls-files", "examples/language", "resources", "LICENSE", "CITATION.cff").splitlines()
    # Package the committed bytes on both Windows and Linux, independent of checkout line endings.
    entries.update({p: subprocess.check_output(["git", "show", f"{commit}:{p}"], cwd=ROOT) for p in paths})
    entries["manifest.json"] = json.dumps({
        "version": project["version"], "commit": compiler_commit, "resources_commit": commit, "wheels": wheel_names,
        "files": {p: hashlib.sha256(raw).hexdigest() for p, raw in entries.items()},
    }, indent=2).encode()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    pack(args.output, entries)
    subprocess.run([sys.executable, str(ROOT / "resources/starters/build_starter.py"),
                    str(args.output), str(args.starter_output or args.output.with_name("qutes-starter.zip"))], check=True)
    print(commit, hashlib.sha256(args.output.read_bytes()).hexdigest(), args.output)


if __name__ == "__main__":
    main()
