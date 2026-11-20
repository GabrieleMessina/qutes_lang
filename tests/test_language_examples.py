"""The published language tour must execute within its advertised 24-qubit cap."""
import json
from dataclasses import replace
from pathlib import Path

import pytest

from qutes.compiler import compile_source
from qutes.config import CompilerConfig
from qutes.serialization import json_text


ROOT = Path(__file__).resolve().parents[1] / "examples" / "language"
CATALOG = json.loads((ROOT / "catalog.json").read_text(encoding="utf-8"))


def test_catalog_lists_every_runnable_tour_file():
    assert {case["file"] for case in CATALOG["examples"]} == {p.name for p in ROOT.glob("*.qut")}
    assert len(CATALOG["examples"]) == len({case["file"] for case in CATALOG["examples"]})
    assert CompilerConfig.load(ROOT / "qutes.toml").max_simulation_qubits == 24


def test_reuse_example_only_fits_limit_with_reuse():
    config = CompilerConfig.load(ROOT / "qutes.toml")
    source = (ROOT / "39_wire_reuse.qut").read_text()
    enabled = compile_source(source, config=config)
    disabled = compile_source(source, config=replace(config, wire_reuse=False))
    assert enabled.program.qubit_count == 6
    assert disabled.program.qubit_count == 39
    assert enabled.metadata["resources"]["simulation_within_limit"]
    assert not disabled.metadata["resources"]["simulation_within_limit"]


@pytest.mark.backend
@pytest.mark.parametrize("case", CATALOG["examples"], ids=lambda case: case["file"])
def test_published_example_runs_with_expected_results_under_24_qubits(case):
    inputs = json.loads((ROOT / case["inputs"]).read_text(encoding="utf-8")) if "inputs" in case else {}
    compilation = compile_source((ROOT / case["file"]).read_text(encoding="utf-8"),
                                 path=str(ROOT / case["file"]), inputs=inputs,
                                 config=CompilerConfig.load(ROOT / "qutes.toml"))
    assert compilation.program.qubit_count <= 24
    # run also enforces the limit after backend decomposition.
    result = compilation.run(shots=CATALOG["shots"], seed=CATALOG["seed"])
    assert sum(item["count"] for item in result["outcomes"]) == CATALOG["shots"]
    allowed = {json_text(value) for value in case["outputs"]}
    assert all(json_text(item["value"]) in allowed for item in result["outcomes"])
    if "preferred" in case:
        preferred = {json.dumps(value) for value in case["preferred"]}
        successes = sum(item["count"] for item in result["outcomes"] if json.dumps(item["value"]) in preferred)
        # A bounded seeded execution smoke check, not a proof of the 99% bound.
        assert successes >= 0.9 * CATALOG["shots"]
