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


def test_names_follow_the_selected_frame_and_measurement_boundary():
    source = """void pair(mut qubit target, mut qubit control) {
    hadamard(control);
    if(control){not(target);}
}
qubit alice=false;
qubit bob=false;
pair(bob,alice);
bool seen=measure(bob);
return [measure(alice),seen];"""
    shot = DebugShot(source, "pair.qut", seed=17)
    def scopes_at(line):
        return shot.advance("continue", {line}, 0)["sourceScopes"]

    assert scopes_at(5)[0]["variables"] == []
    assert scopes_at(6)[0]["variables"] == [{"name":"alice", "value":"q[0]"}]
    local, caller = scopes_at(2)
    script_vars = {"alice":"q[0]", "bob":"q[1]"}
    assert {v["name"]:v["value"] for v in caller["variables"]} == script_vars
    assert {v["name"]:v["value"] for v in local["variables"]} == {**script_vars, "control":"q[0]", "target":"q[1]"}
    assert caller["wireOrder"] == ["bob", "alice"]
    assert local["wireOrder"] == ["target", "control"]
    assert scopes_at(8)[0] == caller
    measured = scopes_at(9)[0]["variables"][-1]
    assert measured == {"name":"seen", "value":json_text(bool(shot.memory & 1))}
    assert finish(shot) == [json.loads(measured["value"])] * 2


def test_reused_wires_follow_each_live_source_binding():
    shot = DebugShot((TOUR / "39_wire_reuse.qut").read_text(), "reuse.qut", config=CompilerConfig.load(TOUR / "qutes.toml"))
    for iteration in range(12):
        before = shot.advance("continue", {6}, 0)["sourceScopes"][0]
        assert before["variables"][-1] == {"name":"i", "value":str(iteration)}
        after = shot.advance("continue", {7}, 0)["sourceScopes"][0]
        assert after["variables"][-1] == {"name":"temporary", "value":"q[3], q[4], q[5]"}
    final = shot.advance("continue", {9}, 0)["sourceScopes"][0]
    assert [v["name"] for v in final["variables"]] == ["number"]
