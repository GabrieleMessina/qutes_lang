"""Integrity of the target corpus; this is NOT semantic acceptance execution."""

import json
from pathlib import Path

from qutes.config import CompilerConfig


def test_acceptance_inventory_is_consistent():
    root = Path(__file__).parent / "acceptance"
    document = json.loads((root / "cases.json").read_text(encoding="utf-8"))
    assert document["schema_version"] == 1
    cases = document["cases"]
    assert len({case["id"] for case in cases}) == len(cases)
    assert {case["file"] for case in cases} == {path.name for path in root.glob("*.qut")}
    for case in cases:
        assert (root / case["file"]).is_file()
        CompilerConfig.resolve(case.get("config"))
        if case["expect"] == "accept":
            assert sum(output["probability"] for output in case["outputs"]) == 1
        else:
            assert case["expect"] == "reject"
            assert case["stage"] in {"lex", "parse", "type", "stage", "effect", "cleanup"}
            assert case["code"].startswith("Q")
