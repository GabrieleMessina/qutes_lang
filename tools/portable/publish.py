"""Attach the verified archives to the existing release and verify the public bytes."""
import argparse
import os
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile

REPO = "GabrieleMessina/qutes_lang"
TAG = "2.0.1"
TARGETS = [
    ("Windows x64", "windows-x64.zip", "Windows Server 2022 x64"),
    ("macOS Apple Silicon", "macos-arm64.zip", "macOS 15 ARM64"),
    ("macOS Intel", "macos-x64.zip", "macOS 15 Intel"),
    ("Linux x64", "linux-x64.tar.gz", "Ubuntu 22.04 x64"),
    ("Linux ARM64", "linux-arm64.tar.gz", "Ubuntu 22.04 ARM64"),
]
NOTES = Path(__file__).with_name("release-notes.md")


def gh(*args):
    return subprocess.check_output(["gh", *args], text=True, encoding="utf-8").strip()


def release():
    result = json.loads(gh("release", "view", TAG, "--repo", REPO, "--json", "assets,body,isDraft"))
    assets = {a["name"]: a for a in result["assets"]}
    return result, assets


def digest(path):
    with path.open("rb") as f:
        return hashlib.file_digest(f, "sha256").hexdigest()


def publish(folder):
    revision = os.environ["GITHUB_SHA"]
    expected = [f"qutes-{TAG}-{suffix}" for _, suffix, _ in TARGETS]
    files = [folder / name for name in expected]
    hashes = {p.name: digest(p) for p in files}
    checksum = folder / f"qutes-{TAG}-SHA256SUMS.txt"
    checksum.write_bytes("".join(f"{sha}  {name}\n" for name, sha in hashes.items()).encode("ascii"))
    files.append(checksum)
    hashes[checksum.name] = digest(checksum)
    # Create the tag only after all five native build and verification jobs passed.
    ref = f"refs/tags/{TAG}"
    matches = json.loads(gh("api", f"repos/{REPO}/git/matching-refs/tags/{TAG}"))
    if not any(item["ref"] == ref for item in matches):
        gh("api", "-X", "POST", f"repos/{REPO}/git/refs", "-f", f"ref={ref}", "-f", f"sha={revision}")
    if gh("api", f"repos/{REPO}/commits/{TAG}", "--jq", ".sha") != revision:
        raise ValueError("Existing release tag differs from the verified build")
    releases = gh("api", "--paginate", f"repos/{REPO}/releases", "--jq", ".[].tag_name").splitlines()
    if TAG not in releases:
        gh("release", "create", TAG, "--repo", REPO, "--verify-tag", "--draft",
           "--title", f"Qutes {TAG}", "--notes-file", str(NOTES))
    _, assets = release()
    if assets.keys() - hashes.keys():
        raise ValueError("Unexpected assets on the release; review the inventory before publishing")
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
        current, uploaded = release()
        if set(uploaded) != set(hashes) or any(uploaded[n]["digest"] != "sha256:" + h for n, h in hashes.items()):
            raise ValueError("Uploaded asset inventory differs from the tested archives")
        notes = NOTES.read_text(encoding="utf-8").strip()
        if current["isDraft"] or current["body"].strip() != notes:
            gh("release", "edit", TAG, "--repo", REPO, "--notes-file", str(NOTES), "--draft=false", "--latest")
        final, final_assets = release()
        if (final["isDraft"] or final["body"].strip() != notes or final_assets.keys() != hashes.keys()
                or any(final_assets[n]["digest"] != "sha256:" + h for n, h in hashes.items())):
            raise ValueError("Final release verification failed")
    print("Verified five portable archives, their checksum file and the release notes.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("folder", type=Path)
    publish(parser.parse_args().folder)
