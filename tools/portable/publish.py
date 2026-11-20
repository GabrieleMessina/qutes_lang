"""Attach the verified archives to the existing release and verify the public bytes."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile

REPO = "GabrieleMessina/qutes_lang"
TAG = "2.0.0"
TARGETS = [
    ("Windows x64", "windows-x64.zip", "Windows Server 2022 x64"),
    ("macOS Apple Silicon", "macos-arm64.zip", "macOS 15 ARM64"),
    ("macOS Intel", "macos-x64.zip", "macOS 15 Intel"),
    ("Linux x64", "linux-x64.tar.gz", "Ubuntu 22.04 x64"),
    ("Linux ARM64", "linux-arm64.tar.gz", "Ubuntu 22.04 ARM64"),
]
ORIGINAL = {
    "qutes_lang-2.0.0-py3-none-any.whl": (772899872, "289dfafbab44ccf25d685e4fd28384021947b97c87a4abe1a27821938d27f6d7"),
    "qutes-resources-2.0.0.zip": (772899877, "30819d5be08edd3357fa94cbc9c1af38876513c22854e5ccb7669a4f48a3cc1f"),
    "qutes-starter.zip": (772899871, "71a4b63a7ab0a2c96a9f1d9eace2355949f80ad188c964807b2f4cb59c40b7ed"),
}
NOTES = Path(__file__).with_name("release-notes.md")


def gh(*args):
    return subprocess.check_output(["gh", *args], text=True, encoding="utf-8").strip()


def release():
    result = json.loads(gh("api", f"repos/{REPO}/releases/tags/{TAG}"))
    assets = {a["name"]: a for a in result["assets"]}
    for name, (asset_id, digest) in ORIGINAL.items():
        if assets[name]["id"] != asset_id or assets[name]["digest"] != "sha256:" + digest:
            raise ValueError(f"Unexpected original release asset: {name}")
    return result, assets


def digest(path):
    with path.open("rb") as f:
        return hashlib.file_digest(f, "sha256").hexdigest()


def publish(folder):
    if gh("api", f"repos/{REPO}/commits/{TAG}", "--jq", ".sha") != "0367b5211448681485d5943586846997bcff2087":
        raise ValueError("The compiler tag no longer identifies the validated release")
    expected = [f"qutes-{TAG}-r2-{suffix}" for _, suffix, _ in TARGETS]
    expected += ["qutes-resources-2.0.0-r2.zip", "qutes-starter-2.0.0-r2.zip"]
    files = [folder / name for name in expected]
    hashes = {p.name: digest(p) for p in files}
    checksum = folder / "qutes-2.0.0-r2-SHA256SUMS.txt"
    checksum.write_bytes("".join(f"{sha}  {name}\n" for name, sha in hashes.items()).encode("ascii"))
    files.append(checksum)
    hashes[checksum.name] = digest(checksum)
    _, assets = release()
    previous = {name: (a["id"], a["digest"]) for name, a in assets.items() if name not in hashes}
    for path in files:
        if path.name in assets and assets[path.name]["digest"] != "sha256:" + hashes[path.name]:
            raise ValueError(f"Existing asset has different bytes: {path.name}")
    for path in files:
        if path.name not in assets:
            gh("release", "upload", TAG, str(path), "--repo", REPO)
    with tempfile.TemporaryDirectory() as temp:
        directory = Path(temp)
        for path in files:
            # Download each exact public asset, including the checksum file.
            gh("release", "download", TAG, "--repo", REPO, "--pattern", path.name, "--dir", temp)
            if digest(directory / path.name) != hashes[path.name]:
                raise ValueError(f"Public download verification failed: {path.name}")
        current, _ = release()
        notes = NOTES.read_text(encoding="utf-8").strip()
        if current["body"].strip() != notes:
            gh("release", "edit", TAG, "--repo", REPO, "--notes-file", str(NOTES))
        final, final_assets = release()
        if any((final_assets[n]["id"], final_assets[n]["digest"]) != value for n, value in previous.items()):
            raise ValueError("Pre-existing release assets changed")
        if final["body"].strip() != notes or any(final_assets[n]["digest"] != "sha256:" + h for n, h in hashes.items()):
            raise ValueError("Final release verification failed")
    print("Verified seven r2 archives, their checksums, the release notes and existing assets.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("folder", type=Path)
    publish(parser.parse_args().folder)
