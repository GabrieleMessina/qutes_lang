"""Check version triggers and retries without contacting the Marketplace."""
from pathlib import Path
from unittest.mock import Mock

import pytest


@pytest.fixture
def release(monkeypatch):
    monkeypatch.syspath_prepend(str(Path(__file__).resolve().parents[1] / "qutes-vscode"))
    import marketplace
    return marketplace


def test_version_trigger(release):
    assert release.release_mode(None, "2.0.6") == "check"
    assert release.release_mode("2.0.6", "2.0.6") == "unchanged"
    assert release.release_mode("2.0.9", "2.0.10") == "publish"
    with pytest.raises(ValueError, match="decreased"):
        release.release_mode("2.1.0", "2.0.10")


def test_partial_upload_resumes_with_exact_packages(release, monkeypatch, tmp_path):
    packages = {t: (tmp_path / (t + ".vsix"), t) for t in release.TARGETS.values()}
    existing = {"linux-arm64"}
    monkeypatch.setattr(release, "published_targets", lambda version: existing)
    monkeypatch.setattr(release, "gallery_hash", lambda version, target: target)
    upload = Mock()
    monkeypatch.setattr(release.subprocess, "run", upload)
    release.publish(packages, "2.0.7")
    paths = [str(p) for t, (p, _) in packages.items() if t not in existing]
    upload.assert_called_once_with(["node", "node_modules/@vscode/vsce/vsce", "publish",
                                    "--oidc", "--packagePath", *paths], cwd=release.HERE, check=True)

    upload.reset_mock()
    existing.update(packages)
    release.publish(packages, "2.0.7")
    upload.assert_not_called()

    existing.remove("linux-x64")
    monkeypatch.setattr(release, "gallery_hash", lambda version, target: "different")
    with pytest.raises(ValueError, match="differs"):
        release.publish(packages, "2.0.7")
    upload.assert_not_called()
