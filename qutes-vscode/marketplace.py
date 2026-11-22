"""Promote the five VSIX files that passed the native tests in this workflow run."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
from urllib.request import Request, urlopen
from xml.etree import ElementTree
from zipfile import ZipFile

from package import TARGETS

HERE = Path(__file__).resolve().parent
PUBLISHER = "GabrieleMessina"
NAME = "qutes"
GALLERY = "https://marketplace.visualstudio.com/_apis/public/gallery"


def version_parts(version):
    if not re.fullmatch(r"(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)", version):
        raise ValueError(f"Expected a stable extension version, got {version!r}")
    return tuple(map(int, version.split(".")))


def release_mode(previous, current):
    current_parts = version_parts(current)
    if previous is None:
        return "check"
    if current_parts < version_parts(previous):
        raise ValueError(f"Extension version decreased from {previous} to {current}")
    return "unchanged" if current == previous else "publish"


def previous_version(before):
    # Manual dispatch and the first import of the extension exercise the connection only.
    if not before or before == "0" * 40:
        return None
    path = "qutes-vscode/package.json"
    if not subprocess.check_output(["git", "ls-tree", before, "--", path]):
        return None
    return json.loads(subprocess.check_output(["git", "show", f"{before}:{path}"]))["version"]


def file_hash(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def package_path(directory, version, target):
    return directory / f"qutes-{version}-{target}.vsix"


def verify(directory, version):
    packages = {}
    for target in TARGETS.values():
        path = package_path(directory / f"qutes-{target}", version, target)
        digest = file_hash(path)
        if digest != path.with_suffix(".vsix.sha256").read_text().strip():
            raise ValueError(f"Tested VSIX checksum mismatch for {target}")
        with ZipFile(path) as archive:
            manifest = json.loads(archive.read("extension/package.json"))
            identity = ElementTree.fromstring(archive.read("extension.vsixmanifest")).find(".//{*}Identity")
        if (manifest["publisher"], manifest["name"], manifest["version"]) != (PUBLISHER, NAME, version):
            raise ValueError(f"Unexpected extension in {path}")
        if identity is None or tuple(identity.get(key) for key in ("Publisher", "Id", "Version", "TargetPlatform")) != (
            PUBLISHER, NAME, version, target
        ):
            raise ValueError(f"Unexpected Marketplace identity in {path}")
        packages[target] = (path.resolve(), digest)
        print(f"Verified {path.name}  {digest}")
    if {path.resolve() for path in directory.rglob("*.vsix")} != {path for path, _ in packages.values()}:
        raise ValueError("Unexpected VSIX in the workflow artifacts")
    return packages


def published_targets(version):
    # Include submitted versions still under Microsoft review when resuming a partial upload.
    query = {"criteria": [{"filterType": 7, "value": f"{PUBLISHER}.{NAME}"}], "pageNumber": 1, "pageSize": 1}
    body = {"filters": [query], "flags": 1}
    request = Request(f"{GALLERY}/extensionquery", data=json.dumps(body).encode(),
                      headers={"Accept": "application/json;api-version=7.2-preview.1", "Content-Type": "application/json"})
    with urlopen(request, timeout=45) as response:
        extension, = json.load(response)["results"][0]["extensions"]
    if (extension["publisher"]["publisherName"], extension["extensionName"]) != (PUBLISHER, NAME):
        raise ValueError("The public gallery returned a different listing")
    return {entry.get("targetPlatform") for entry in extension["versions"] if entry["version"] == version}


def gallery_hash(version, target):
    url = f"{GALLERY}/publishers/{PUBLISHER}/vsextensions/{NAME}/{version}/vspackage?targetPlatform={target}"
    with urlopen(url, timeout=120) as response:
        return hashlib.file_digest(response, "sha256").hexdigest()


def publish(packages, version):
    existing = published_targets(version)
    if existing - packages.keys():
        raise ValueError(f"Unexpected Marketplace targets for {version}: {existing}")
    # Check all collisions before making the first write. Retrying failed jobs reuses the original artifacts.
    for target in sorted(existing):
        if gallery_hash(version, target) != packages[target][1]:
            raise ValueError(f"Marketplace {version} for {target} differs from this run's tested package")
    missing = [str(path) for target, (path, _) in packages.items() if target not in existing]
    if missing:
        subprocess.run(["node", "node_modules/@vscode/vsce/vsce", "publish", "--oidc", "--packagePath", *missing],
                       cwd=HERE, check=True)
    else:
        print("The Marketplace already has the five exact packages.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("plan").add_argument("before")
    receipt = commands.add_parser("receipt")
    receipt.add_argument("directory", type=Path)
    receipt.add_argument("target", choices=TARGETS.values())
    for command in ("verify", "publish"):
        commands.add_parser(command).add_argument("directory", type=Path)
    args = parser.parse_args()
    version = json.loads((HERE / "package.json").read_text())["version"]
    if args.command == "plan":
        print(f"mode={release_mode(previous_version(args.before), version)}")
        print(f"version={version}")
    elif args.command == "receipt":
        path = package_path(args.directory, version, args.target)
        path.with_suffix(".vsix.sha256").write_text(file_hash(path) + "\n", encoding="ascii")
    else:
        packages = verify(args.directory, version)
        if args.command == "publish":
            publish(packages, version)


if __name__ == "__main__":
    main()
