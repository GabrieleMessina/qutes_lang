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


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    if git("status", "--porcelain", "--untracked-files=normal"):
        raise SystemExit("Commit the release before building its bundle.")
    commit = git("rev-parse", "HEAD")
    project = tomllib.loads((ROOT / "pyproject.toml").read_text())["project"]
    with tempfile.TemporaryDirectory() as temporary:
        folder = Path(temporary)
        subprocess.run([sys.executable, "-m", "pip", "wheel", "--no-build-isolation",
                        "--wheel-dir", str(folder), str(ROOT)], check=True)
        wheels = sorted(folder.glob("*.whl"))
        if len(wheels) != 2 or any(not p.name.endswith("-none-any.whl") for p in wheels):
            raise SystemExit("Expected the portable compiler and ANTLR wheels.")
        entries = {f"wheels/{p.name}": p.read_bytes() for p in wheels}
    paths = git("ls-files", "examples/language", "resources", "LICENSE", "CITATION.cff").splitlines()
    entries.update({p: (ROOT / p).read_bytes() for p in paths})
    entries["manifest.json"] = json.dumps({
        "version": project["version"], "commit": commit, "wheels": [p.name for p in wheels],
        "files": {p: hashlib.sha256(raw).hexdigest() for p, raw in entries.items()},
    }, indent=2).encode()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    pack(args.output, entries)
    print(commit, hashlib.sha256(args.output.read_bytes()).hexdigest(), args.output)


if __name__ == "__main__":
    main()
