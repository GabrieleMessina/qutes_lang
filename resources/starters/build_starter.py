"""Create the offline Bell project from the canonical sources in a Qutes bundle."""
import argparse
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo


def build(bundle, destination):
    with ZipFile(bundle) as source:
        files = {"main.qut": source.read("examples/language/41_bell_gates.qut"),
                 "qutes.toml": source.read("examples/language/qutes.toml"),
                 "inputs.json": b"{}\n"}
        for name in source.namelist():
            if name.startswith("wheels/") or name in ("LICENSE", "CITATION.cff"):
                files[name] = source.read(name)
    files["README.md"] = b"""# Your first Qutes project

Open this folder in a terminal and activate a Python 3.12 or 3.13 virtual environment.

    python -m pip install --find-links wheels "qutes-lang[backend]==0.4.0"
    qutes run main.qut --config qutes.toml --inputs inputs.json --shots 64 --seed 17

Expect equal bits on every shot. Add not(bob); immediately before the return and
run again to see opposite bits. Inspect the circuit with qutes explain main.qut.
"""
    destination.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(destination, "w") as archive:
        for name, data in sorted(files.items()):
            archive.writestr(ZipInfo(name, (2026, 1, 1, 0, 0, 0)), data, compress_type=ZIP_DEFLATED)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("bundle", type=Path)
    parser.add_argument("destination", type=Path)
    args = parser.parse_args()
    build(args.bundle, args.destination)
