"""Package the unchanged native releases with the same Marketplace identity on all targets."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
from zipfile import ZipFile
from xml.etree import ElementTree

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
TARGETS = {"windows-x64": "win32-x64", "macos-x64": "darwin-x64", "macos-arm64": "darwin-arm64",
           "linux-x64": "linux-x64", "linux-arm64": "linux-arm64"}


def package(archives, output, only=None):
    output.mkdir(parents=True, exist_ok=True)
    vsce = HERE / "node_modules/@vscode/vsce/vsce"
    manifest = json.loads((HERE / "package.json").read_text())
    for line in (HERE / "runtime-checksums.txt").read_text().splitlines():
        checksum, filename = line.split()
        folder = filename.removesuffix(".zip").removesuffix(".tar.gz")
        target = TARGETS[folder.removeprefix("qutes-2.0.1-")]
        if only and target != only:
            continue
        archive = archives / filename
        with archive.open("rb") as stream:
            if hashlib.file_digest(stream, "sha256").hexdigest() != checksum:
                raise ValueError(f"Incorrect released runtime: {filename}")
        with tempfile.TemporaryDirectory(dir=output, prefix="stage-") as temp:
            stage = Path(temp)
            for name in ["extension.cjs", "runtime.cjs", "README.md", "language-configuration.json"]:
                shutil.copyfile(HERE / name, stage / name)
            shipped = {key: value for key, value in manifest.items() if key not in {"devDependencies", "overrides"}}
            (stage / "package.json").write_text(json.dumps(shipped, indent=2), encoding="utf-8")
            shutil.copytree(HERE / "syntaxes", stage / "syntaxes")
            shutil.copyfile(ROOT / "LICENSE", stage / "LICENSE")
            (stage / "runtime").mkdir()
            shutil.copyfile(archive, stage / "runtime" / filename)
            (stage / "language").mkdir()
            for name in ["language.mjs", "vocabulary.mjs"]:
                shutil.copyfile(ROOT / "editors" / name, stage / "language" / name)
            receipt = dict(target=target, root=folder, archive=filename, sha256=checksum)
            (stage / "runtime.json").write_text(json.dumps(receipt))
            result = output / f"qutes-{manifest['version']}-{target}.vsix"
            subprocess.run(["node", str(vsce), "package", "--no-dependencies", "--skip-license",
                            "--target", target, "--out", str(result)], cwd=stage, check=True)
            with ZipFile(result) as zipped:
                identity = ElementTree.fromstring(zipped.read("extension.vsixmanifest")).find(".//{*}Identity")
                if (identity.get("TargetPlatform"), identity.get("Publisher"), identity.get("Id")) != (
                    target, manifest["publisher"], manifest["name"]
                ):
                    raise ValueError("Unexpected Marketplace package identity")
                with zipped.open("extension/runtime/" + filename) as stream:
                    if hashlib.file_digest(stream, "sha256").hexdigest() != checksum:
                        raise ValueError("Packaged runtime differs from the verified archive")
            print(f"{result.name}: {result.stat().st_size:,} bytes", flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archives", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--target", choices=TARGETS.values())
    args = parser.parse_args()
    package(args.archives.resolve(), args.output.resolve(), args.target)
