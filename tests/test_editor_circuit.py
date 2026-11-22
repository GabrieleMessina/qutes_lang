import numpy as np
from qiskit.quantum_info import Statevector

from qutes.compiler import compile_source
from qutes.editor_circuit import circuit_report


def test_cancel_pair_preserves_an_entangled_relative_phase_and_all_other_gates():
    preparation = "qubit a=false; qubit b=false; hadamard(a); if(a){not(b);} phase(a,pi/3.0);"
    source = preparation + "hadamard(a); hadamard(a);"
    compiled = compile_source(source)
    report = circuit_report(compiled)
    [suggestion] = report["suggestions"]
    start, end = suggestion["range"]
    assert source[start:end] == "hadamard(a); hadamard(a);"
    reduced = compile_source(source[:start]+source[end:])
    assert compiled.metadata["resources"]["gate_applications"] - reduced.metadata["resources"]["gate_applications"] == 2
    np.testing.assert_allclose(Statevector.from_instruction(compiled.build()[0]).data,
                               Statevector.from_instruction(reduced.build()[0]).data, atol=1e-12)


def test_repeated_source_measurements_and_classical_controls_are_inspect_only():
    source = "// 🐈\nqubit q=false; for(int i=0;i<3;i++){hadamard(q);} bool b=measure(q); if(b){hadamard(q);}"
    report = circuit_report(compile_source(source))
    assert not report["suggestions"]
    assert all(g["edit"] is None for g in report["gates"])
    first = report["gates"][1]
    assert first["occurrences"] == 3
    start, end = first["range"]
    assert source.encode("utf-16-le")[2*start:2*end].decode("utf-16-le") == "hadamard(q)"


def test_measurement_boundary_and_shadowing():
    code = "qubit a=false; hadamard(a); bool m=measure(a); hadamard(a); return measure(a);"
    report = circuit_report(compile_source(code))
    assert not report["suggestions"]
    assert report["qubits"] == ["a"]
    assert code[report["insertAt"]:].startswith("return ")
    assert report["gates"][0]["edit"]["available"] == ["a"]


def test_controlled_not_edit_covers_the_guard_and_preserves_the_bell_program():
    source = "qubit a=false;qubit b=false;hadamard(a);if(a){not(b);}return [measure(a),measure(b)];"
    report = circuit_report(compile_source(source))
    edit = report["gates"][1]["edit"]
    assert (edit["gate"], edit["control"], edit["target"]) == ("controlled-not", "a", "b")
    left, right = edit["range"]
    assert source[left:right] == "if(a){not(b);}"
