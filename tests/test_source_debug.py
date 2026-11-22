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
    zero = "  P(0)=100%  P(1)=0%"
    even = "  P(0)=50%  P(1)=50%"
    assert scopes_at(6)[0]["variables"] == [{"name":"alice", "value":"q[0]" + zero}]
    local, caller = scopes_at(2)
    script_vars = {"alice":"q[0]" + zero, "bob":"q[1]" + zero}
    assert {v["name"]:v["value"] for v in caller["variables"]} == script_vars
    assert {v["name"]:v["value"] for v in local["variables"]} == {
        **script_vars, "control":script_vars["alice"], "target":script_vars["bob"]}
    assert caller["wireOrder"] == ["bob", "alice"]
    assert local["wireOrder"] == ["target", "control"]
    assert [row["value"] for row in scopes_at(8)[0]["variables"]] == ["q[0]" + even, "q[1]" + even]
    alice, bob, measured = scopes_at(9)[0]["variables"]
    collapsed = "  P(0)=0%  P(1)=100%" if shot.memory & 1 else zero
    assert (alice["value"], bob["value"]) == ("q[0]" + collapsed, "q[1]" + collapsed)
    assert measured == {"name":"seen", "value":json_text(bool(shot.memory & 1))}
    assert finish(shot) == [json.loads(measured["value"])] * 2


def test_marginals_include_basis_states_outside_the_joint_preview():
    source = """qubit coin=superposition([false,true], probabilities:[0.25,0.75]);
qubit a=superposition();
qubit b=superposition();
qubit c=superposition();
qubit d=superposition();
return [measure(coin),measure(a),measure(b),measure(c),measure(d)];"""
    shot = DebugShot(source, "five.qut", seed=17)
    stop = shot.advance("continue", {6}, 0)
    assert stop["variables"][-1] == {"name":"Other basis states", "value":"16"}
    coin, *others = stop["sourceScopes"][0]["variables"]
    assert coin["value"].endswith("P(0)=25%  P(1)=75%")
    assert all(row["value"].endswith("P(0)=50%  P(1)=50%") for row in others)
    assert finish(shot) == finish(DebugShot(source, "five.qut", seed=17))


def test_reused_wires_follow_each_live_source_binding():
    shot = DebugShot((TOUR / "39_wire_reuse.qut").read_text(), "reuse.qut", config=CompilerConfig.load(TOUR / "qutes.toml"))
    for iteration in range(12):
        before = shot.advance("continue", {6}, 0)["sourceScopes"][0]
        assert before["variables"][-1] == {"name":"i", "value":str(iteration)}
        after = shot.advance("continue", {7}, 0)["sourceScopes"][0]
        temporary = after["variables"][-1]
        assert temporary["name"] == "temporary"
        assert temporary["value"].startswith(f"P({(iteration + 6) % 8 - 4})=100%")
        assert temporary["value"].endswith("q[3], q[4], q[5]")
    final = shot.advance("continue", {9}, 0)["sourceScopes"][0]
    assert [v["name"] for v in final["variables"]] == ["number"]


def outcomes(stop, name):
    row = next(v for v in stop["sourceScopes"][0]["variables"] if v["name"] == name)
    return {v["name"]: v["value"] for v in stop["distributions"][row["distribution"]]}


def test_typed_distributions_use_signed_values_and_full_support():
    src = """quint number=superposition([-1,2], probabilities:[0.25,0.75]);
quint all=superposition();
return measure(number);"""
    shot = DebugShot(src, "weighted.qut", config=CompilerConfig(quint_bits=5), seed=17)
    stop = shot.advance("continue", {3}, 0)
    assert outcomes(stop, "number") == {"-1":"25%", "2":"75%"}
    assert outcomes(stop, "all") == {str(i):"3.125%" for i in range(-16, 16)}
    assert finish(shot) == finish(DebugShot(src, "weighted.qut", config=shot.program.config, seed=17))


def test_text_views_follow_alphabet_length_and_program_measurement():
    src = """qubit flag=superposition();
qustring word="YX";
if(flag){word="XY";}
quchar first=word[0];
string seen=measure(word);
return seen;"""
    shot = DebugShot(src, "words.qut", config=CompilerConfig(alphabet="XYZ", qustring_capacity=3), seed=7)
    stop = shot.advance("continue", {5}, 0)
    assert outcomes(stop, "word") == {'"YX"':"50%", '"XY"':"50%"}
    assert outcomes(stop, "first") == {'"Y"':"50%", '"X"':"50%"}
    after = shot.advance("continue", {6}, 0)
    value = finish(shot)
    assert outcomes(after, "word") == {json_text(value):"100%"}
    assert outcomes(after, "first") == {json_text(value[0]):"100%"}


def test_array_marginal_preserves_correlations_and_slice_order():
    src = """qubit[] pair=[false,false];
hadamard(pair[0]);
if(pair[0]){not(pair[1]);}
qubit[] view=pair[1..2];
return measure(pair);"""
    shot = DebugShot(src, "pair.qut")
    stop = shot.advance("continue", {5}, 0)
    assert outcomes(stop, "pair") == {"[false,false]":"50%", "[true,true]":"50%"}
    assert outcomes(stop, "view") == {"[false]":"50%", "[true]":"50%"}


def test_one_bit_registers_use_their_declared_type():
    src = """quint number=-1;
quchar letter='Y';
qustring word="X";
qustring empty="";
return measure(word);"""
    shot = DebugShot(src, "narrow.qut", config=CompilerConfig(quint_bits=1, alphabet="XY", qustring_capacity=1))
    stop = shot.advance("continue", {5}, 0)
    assert outcomes(stop, "number") == {"-1":"100%"}
    assert outcomes(stop, "letter") == {'"Y"':"100%"}
    assert outcomes(stop, "word") == {'"X"':"100%"}
    assert outcomes(stop, "empty") == {'""':"100%"}
