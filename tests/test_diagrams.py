from dataclasses import replace
import io
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


def compile(source):
    return compile_source(source, config=CompilerConfig(quint_bits=2, alphabet="AB"))


def labels(circuit):
    return [item.operation.label for item in circuit.data if item.operation.label]


def test_default_compact_comparisons_and_if():
    for name, expected in [("12_quantum_ordering", "number < 0"), ("15_coherent_if", "if (choice)")]:
        path = Path("examples/language") / (name + ".qut")
        c = compile_source(path.read_text(), config=CompilerConfig.load(path.parent / "qutes.toml"))
        executable, _ = c.build()
        saved = executable.copy()
        view = build_diagram(c)
        assert any(expected in label for label in labels(view))
        assert c.build()[0] == saved
        assert view.num_qubits == executable.num_qubits


def test_nested_depth_selectors_and_ancestor_paths():
    c = compile('''quint inner(quint n) { return n+1; }
quint outer(quint n) { return inner(n); }
quint n=0; quint a=outer(n); quint b=n+1;''')
    assert any("outer()" in s for s in labels(build_diagram(c)))
    assert any("inner()" in s for s in labels(build_diagram(c, unfold=1)))
    selected = labels(build_diagram(c, unfold=1, unfold_only="inner"))
    assert not any("outer()" in s or "inner()" in s for s in selected)
    assert any("n+1" in s for s in selected)  # unrelated addition stays folded


@pytest.mark.parametrize("depth", [0, 1, 2, "all"])
def test_full_operator_phase_and_cleanup_preserved(depth):
    c = compile('qubit q=superposition(); quint n=0; if(q) { n+=1; } { quint tmp=n+1; }')
    actual = build_diagram(c, unfold=depth)
    expected, _ = c.build()
    assert np.allclose(Operator(actual).data, Operator(expected).data, atol=1e-10)
    assert any("clean |0>" in s for s in labels(actual))
    assert not any(item.operation.name in {"reset", "measure"} for item in actual.data)


def test_search_oracle_selective_unfolding_and_complex_phase():
    c = compile('qubit accepts(qubit value) { return !value; } qubit q=search([false,true],accepts);')
    assert any(r.label == "accepts" for r in c.program.regions)
    expected = Operator(c.build()[0]).data
    for depth, selectors in [(0, None), (1, "accepts"), ("all", None)]:
        actual = build_diagram(c, unfold=depth, unfold_only=selectors)
        assert np.allclose(Operator(actual).data, expected, atol=1e-10)


def test_quantum_collection_non_power_of_two_phases_and_scratch():
    from qiskit.quantum_info import Statevector
    c = compile('qubit accepts(qubit v) { return !v; } qubit seed=superposition(); '
                'qubit[] values=[seed,!seed,true]; qubit result=search(values,accepts);')
    expected = Statevector.from_instruction(c.build()[0]).data
    for depth, selectors in [(0, None), (1, "accepts"), ("all", None)]:
        actual = Statevector.from_instruction(build_diagram(c, unfold=depth, unfold_only=selectors)).data
        assert np.allclose(actual, expected, atol=1e-10)
        live = {i.physical for i in c.program.wire_allocation.intervals if i.end > len(c.program.operations)}
        scratch = set(range(c.program.qubit_count)) - live
        assert sum(abs(actual[i]) ** 2 for i in range(len(actual)) if any(i >> b & 1 for b in scratch)) < 1e-12


def test_measurement_and_runtime_branch_never_hidden_in_gate():
    c = compile('''int helper(quint n) { int before=measure(n); return before; }
quint n=0; int result=helper(n); if(result==0) { n+=1; } return measure(n);''')
    view = build_diagram(c, unfold="all")
    assert any(item.operation.name == "measure" for item in view.data)
    assert any(item.operation.name == "if_else" for item in view.data)
    from qiskit import transpile
    from qiskit_aer import AerSimulator
    simulator = AerSimulator(max_parallel_threads=1)
    actual = simulator.run(transpile(view, simulator, optimization_level=0), shots=8, seed_simulator=3).result().get_counts()
    assert {int(bits.replace(" ", ""), 2) for bits in actual} == {4}


def test_units_and_restored_wires_marked_separately():
    c = compile('quint n=0; quint output=0; { quint t=n+1; output+=t; n+=1; }')
    text = labels(build_diagram(c, unfold="all"))
    assert any("clean |0>" in s for s in text)
    assert "inputs restored" in text
    assert c.metadata["resources"]["wire_reuse"] is True


def test_zero_operation_cleanup_has_marker():
    c = compile_source('{ quint empty=0; }', config=CompilerConfig(quint_bits=2, wire_reuse=False))
    view = build_diagram(c)
    assert any("clean |0>: empty" == s for s in labels(view))


def test_same_named_zero_length_cleanup_events_are_distinct():
    c = compile_source('for(int i=0;i<3;i++) { quint empty=0; }', config=CompilerConfig(quint_bits=2, wire_reuse=False))
    view = build_diagram(c)
    markers = [item for item in view.data if item.operation.name == "barrier"]
    assert len(markers) == 3
    assert len({tuple(view.find_bit(bit).index for bit in item.qubits) for item in markers}) == 3


def test_invalid_selectors_and_budget_fail_deliberately():
    c = compile('quint n=1; quint m=n+1;')
    with pytest.raises(DiagnosticError, match="did you mean 'add'"):
        build_diagram(c, unfold=1, unfold_only="adds")
    limited = replace(c, program=replace(c.program, config=replace(c.program.config, max_evaluation_steps=2)))
    with pytest.raises(DiagnosticError) as error:
        build_diagram(limited, unfold="all")
    assert error.value.code == "Q4001"


@pytest.mark.parametrize("args", [["--unfold", "1"], ["--print-circuit", "--unfold", "-1"],
    ["--print-circuit", "--unfold-only", "add"], ["--print-circuit", "--unfold", "2", "--unfold-only", "add,"]])
def test_invalid_cli_view_options(args, tmp_path):
    p = tmp_path / "test.qut"
    p.write_text("return 1;")
    with pytest.raises(SystemExit) as e:
        main(["check", str(p), *args])
    assert e.value.code == 2


def test_image_variants_have_independent_names_and_same_build(tmp_path):
    c = compile('quint n=1; quint m=n+1;')
    identity = c.metadata["build_sha256"]
    a = render(c, directory=tmp_path, image_format="svg")
    b = render(c, directory=tmp_path, image_format="svg", unfold=1)
    assert a["image"] != b["image"]
    assert c.metadata["build_sha256"] == identity
    assert render(c, directory=tmp_path, image_format="svg")["image"] == a["image"]


def test_expanded_text_output_has_cleanup_annotations():
    c = compile('{ quint n=0; n+=1; }')
    stream = io.StringIO()
    result = render(c, print_circuit=True, stream=stream, unfold="all")
    assert result["view"]["unfold"] == "all"
    assert "clean |0>" in stream.getvalue()


def test_api_rejects_view_options_without_output():
    with pytest.raises(DiagnosticError, match="require printed or saved"):
        render(compile("return 1;"), unfold=1)


def test_all_reaches_elementary_adder_and_phase_gates():
    c = compile('quint a=1; quint b=0; a+=b;')
    assert set(build_diagram(c, unfold="all").count_ops()) <= {"u", "cx", "barrier"}


def test_wide_lazy_gate_expansion_is_rejected_before_definition():
    c = compile_source('quint n=superposition(); return measure(n==0);', config=CompilerConfig(quint_bits=20))
    with pytest.raises(DiagnosticError, match="preflight budget") as e:
        build_diagram(c, unfold="all")
    assert e.value.code == "Q4001"
