"""Physical/logical diagrams and their public CLI/report interfaces."""
import io
import json
from pathlib import Path

import numpy as np
import pytest
from qiskit.quantum_info import Operator

from qutes.cli import main
from qutes.compiler import compile_source
from qutes.config import CompilerConfig
from qutes.diagrams import build_diagram
from qutes.diagnostics import DiagnosticError
from qutes.visualization import render

pytestmark = pytest.mark.backend
SOURCE = 'qubit q=superposition(); void helper(){ qubit local=!q; } helper(); helper();'


@pytest.mark.parametrize("view", ["physical", "logical"])
@pytest.mark.parametrize("depth,selector", [(0,None),(1,None),(2,None),(1,"helper"),("all",None)])
def test_wire_views_preserve_operators_and_cleanup(view, depth, selector):
    c = compile_source(SOURCE)
    circuit = c.build()[0]
    saved = circuit.copy()
    result = build_diagram(c, wire_view=view, unfold=depth, unfold_only=selector)
    expected = circuit if view == "physical" else c.program.logical_program.to_qiskit()
    np.testing.assert_allclose(Operator(result).data, Operator(expected).data, atol=1e-10)
    assert c.build()[0] == saved
    assert result.num_qubits == (2 if view == "physical" else 3)
    labels = [item.operation.label or "" for item in result.data]
    if view == "physical":
        assert any("reuse" in label for label in labels)
        assert any(register.name.startswith("work_") for register in result.qregs)
    else:
        assert not any("reuse" in label for label in labels)


def test_empty_cleanup_never_becomes_all_wire_barrier():
    c = compile_source('qubit q=true; {qubit empty=false;} {qubit local=!q;}')
    physical = build_diagram(c, unfold="all")
    assert not any("empty" in (item.operation.label or "") for item in physical.data)
    logical = build_diagram(c, wire_view="logical", unfold="all")
    markers = [item for item in logical.data if "empty" in (item.operation.label or "")]
    assert len(markers) == 1 and len(markers[0].qubits) == 1


@pytest.mark.parametrize("image_format", ["png", "svg"])
def test_image_views_coexist_and_do_not_change_identity(tmp_path, image_format):
    c = compile_source(SOURCE)
    identity = c.metadata["build_sha256"]
    physical = render(c, directory=tmp_path, image_format=image_format)
    logical = render(c, directory=tmp_path, image_format=image_format, wire_view="logical", unfold=1)
    assert physical["image"] != logical["image"]
    assert Path(physical["image"]).stat().st_size > 100
    assert Path(logical["image"]).stat().st_size > 100
    assert c.metadata["build_sha256"] == identity


@pytest.mark.parametrize("command", ["check", "build", "run", "explain"])
def test_cli_wire_view_in_json_and_report(command, tmp_path, capsys):
    source = tmp_path / "example.qut"
    source.write_text(SOURCE)
    assert main([command, str(source), "--json", "--print-circuit", "--wire-view", "logical"]) == 0
    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert payload["circuit_diagram"]["view"]["wire_view"] == "logical"
    assert "Final compiler circuit" in captured.err


def test_invalid_and_budgeted_views():
    from dataclasses import replace
    c = compile_source(SOURCE)
    with pytest.raises(DiagnosticError, match="wire-view"):
        render(c, wire_view="logical")
    with pytest.raises(DiagnosticError, match="wire-view"):
        render(c, print_circuit=True, wire_view="bad", stream=io.StringIO())
    tiny = replace(c.program.logical_program, config=replace(c.program.config, max_evaluation_steps=1))
    limited = replace(c, program=replace(c.program, logical_program=tiny))
    with pytest.raises(DiagnosticError) as error:
        build_diagram(limited, wire_view="logical", unfold="all")
    assert error.value.code == "Q4001"


def test_example12_reports_physical_memory_and_logical_cleanup(capsys):
    path = "examples/language/12_quantum_ordering.qut"
    assert main(["explain", path]) == 0
    output = capsys.readouterr().out
    assert "physical qubits: 10; logical qubits: 19; saved: 9" in output
    assert "Logical qubits cleaned: 16; physical wires free at end: 7" in output
    assert "16 KiB" in output and "epoch" in output
    assert main(["explain", path, "--no-wire-reuse"]) == 0
    assert "8 MiB" in capsys.readouterr().out
    with pytest.raises(SystemExit):
        main(["check", path, "--wire-view", "logical"])


def test_many_unused_locals_and_final_live_zero_have_bounded_physical_width(capsys, tmp_path):
    source = tmp_path / "empty.qut"
    source.write_text('for(int i=0;i<500;i++){qubit empty=false;} qubit live=false;')
    c = compile_source(source.read_text())
    assert c.program.qubit_count == 1
    assert c.program.logical_program.qubit_count == 501
    assert not any(item.operation.name == "barrier" for item in build_diagram(c).data)
    assert main(["explain", str(source)]) == 0
    assert "Unused zero-only logical wires omitted" in capsys.readouterr().out
