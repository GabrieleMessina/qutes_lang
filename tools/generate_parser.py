"""Reproducibly regenerate/check the committed ANTLR Python frontend."""
import argparse
import hashlib
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
VERSION = "4.13.2"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--jar", type=Path, required=True)
    parser.add_argument("--java", default="java")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    jar = args.jar.resolve()
    expected = (ROOT / "grammar/antlr.sha256").read_text().split()[0]
    if hashlib.sha256(jar.read_bytes()).hexdigest() != expected:
        parser.error(f"generator must be the pinned ANTLR {VERSION} jar")
    with tempfile.TemporaryDirectory() as directory:
        subprocess.run([args.java, "-jar", str(jar), "-Dlanguage=Python3", "-visitor",
                        "-no-listener", "-o", directory, "Qutes.g4"],
                       cwd=ROOT / "grammar", check=True)
        destination = ROOT / "src/qutes/generated"
        for path in sorted(Path(directory).glob("*.py")):
            target = destination / path.name
            # ANTLR emits trailing spaces; normalize deterministically across OSes.
            data = ("\n".join(line.rstrip() for line in path.read_text(encoding="utf-8").splitlines()) + "\n").encode("utf-8")
            if args.check:
                if not target.exists() or data != target.read_bytes():
                    parser.error(f"generated source differs: {target.name}")
            else:
                target.write_bytes(data)


if __name__ == "__main__":
    main()
