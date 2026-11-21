import json
from pathlib import Path

import pytest

from qutes.compiler import compile_source
from qutes.config import CompilerConfig
from qutes.diagnostics import DiagnosticError
from qutes.serialization import json_text
from qutes.source_debug import DebugShot


TOUR = Path(__file__).resolve().parents[1] / "examples/language"


def finish(shot):
    while True:
        result = shot.advance("continue", set(), 0)
        if result.get("done"):
            return result["result"]


def test_debug_markers_preserve_the_compiled_tour_circuits_and_results():
    catalog = json.loads((TOUR / "catalog.json").read_text(encoding="utf-8"))
    for case in catalog["examples"]:
        filename = case["file"]
        source = (TOUR / filename).read_text(encoding="utf-8")
        inputs = json.loads((TOUR / case["inputs"]).read_text(encoding="utf-8")) if case.get("inputs") else {}
        config = CompilerConfig.load(TOUR / "qutes.toml", case.get("overrides"))
        reference = compile_source(source, path=filename, inputs=inputs, config=config).program
        if reference.qubit_count > 12:
            with pytest.raises(DiagnosticError, match="12 physical qubits"):
                DebugShot(source, filename, inputs, config)
            continue
        shot = DebugShot(source, filename, inputs, config, seed=17)
        assert shot.program.operations == reference.operations, filename
        assert shot.program.result == reference.result, filename
        assert json.loads(json_text(finish(shot))) in case["outputs"], filename


def test_runtime_branch_and_loop_breakpoints():
    source = """qubit q=false;
bool choice=measure(q);
if (choice) {
    not(q);
}
for(int i=0;i<3;i++){
    hadamard(q);
}
return measure(q);"""
    shot = DebugShot(source, "loop.qut", seed=17)
    for _ in range(3):
        stop = shot.advance("continue", {4, 7}, 0)
        assert stop["frames"][0]["line"] == 7
    assert shot.advance("continue", {4, 7}, 0)["done"]


def test_state_inspection_preserves_phase_and_bell_correlations():
    for seed in range(8):
        shot = DebugShot((TOUR / "42_teleportation.qut").read_text(encoding="utf-8"), "teleport.qut", seed=seed)
        while True:
            result = shot.advance("stepIn", set(), 0)
            if result.get("done"):
                assert result["result"] is False
                break
    bell = (TOUR / "41_bell_gates.qut").read_text(encoding="utf-8")
    assert {tuple(finish(DebugShot(bell, "bell.qut", seed=i))) for i in range(12)} == {(True, True), (False, False)}
