import builtins
import importlib.util
import json
from pathlib import Path
import sys

import pytest

from qutes.cli import main
from qutes.codegen import python_source, write_python
from qutes.compiler import compile_source
from qutes.config import CompilerConfig
from qutes.diagnostics import DiagnosticError
from qutes.runtime import ResultLayout, execute
from qutes.artifact_v2 import layout_from_metadata
from qutes.serialization import integer_text, json_text, load_json, parse_integer

ROOT = Path(__file__).parent / "acceptance"
CASES = json.loads((ROOT / "cases.json").read_text())["cases"]


def compiled(source, inputs=None, **settings):
    return compile_source(source, inputs=inputs, config=CompilerConfig.resolve({"quint_bits": 3}, settings))


def generated(compilation, tmp_path):
    path = tmp_path / "program.py"
    write_python(compilation, path)
    spec = importlib.util.spec_from_file_location("generated_program", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.mark.backend
@pytest.mark.parametrize("case", [case for case in CASES if case["expect"] == "accept"], ids=lambda case: case["id"])
def test_all_positive_cases_execute_from_generated_python(case, tmp_path):
    compilation = compiled((ROOT / case["file"]).read_text(), **case.get("config", {}))
    module = generated(compilation, tmp_path)
    circuit, layout = module.build()
    assert circuit == compilation.build()[0]
    assert layout.to_dict() == compilation.metadata["result_layout"]
    outcome = module.run(shots=256, seed=73)
    assert {json_text(item["value"]) for item in outcome["outcomes"]} == {json_text(item["value"]) for item in case["outputs"]}
    assert sum(item["count"] for item in outcome["outcomes"]) == 256
    assert sum(item["probability"] for item in outcome["outcomes"]) == pytest.approx(1)
    assert outcome["build"]["build_sha256"] == compilation.metadata["build_sha256"]


@pytest.mark.backend
def test_generated_build_respecializes_inputs_and_preserves_old_binding(tmp_path):
    compilation = compiled('input int count;  quint[] values=new quint[count]; return measure(values); ', {"count": 1})
    module = generated(compilation, tmp_path)
    circuit, layout = module.build({"count": 2})
    assert circuit.num_qubits == 6
    assert layout.decode(0) == [0, 0]
    assert module.run({"count": 2}, shots=4, seed=19)["outcomes"] == [{"value": [0, 0], "count": 4, "probability": 1.0}]
    assert module.build()[0].num_qubits == 3
    assert module.run(shots=4)["outcomes"][0]["value"] == [0]
    assert layout.metadata["build_sha256"] != compilation.metadata["build_sha256"]
    for invalid in ({"count": True}, {"count": 1.0}, {"count": 1, "extra": 0}, []):
        with pytest.raises(DiagnosticError) as error:
            module.build(invalid)
        assert error.value.code == "Q2001"


@pytest.mark.backend
def test_generated_runtime_conditions_snapshots_and_cleanup(tmp_path):
    module = generated(compiled("""
        quint n=superposition(); int before=measure(n); n+=1; int after=measure(n);
        quint value=0;
        if(before<0 && after>=0 || before==after) { value=1; } else { value=2; }
        { quint local=n+1; }
        return [before,after,measure(value)];
    """, quint_bits=3), tmp_path)
    outcomes = module.run(shots=256, seed=17)["outcomes"]
    assert len(outcomes) == 8
    for item in outcomes:
        before, after, value = item["value"]
        assert after == (before + 1 + 4) % 8 - 4
        assert value == (1 if before < 0 <= after or before == after else 2)


def test_deterministic_artifacts_identity_and_safe_source_embedding(tmp_path):
    source = """ return "\\"; __import__(\\"sys\\")";  // λ
"""
    compilation = compiled(source)
    assert python_source(compilation) == python_source(compiled(source))
    module = generated(compilation, tmp_path)
    assert module.SOURCE == source
    assert module.run(shots=2)["outcomes"][0]["value"] == '"; __import__("sys")'
    identity = compilation.metadata["build_sha256"]
    assert compiled(source + " ").metadata["build_sha256"] != identity
    assert compiled(source, quint_bits=4).metadata["build_sha256"] != identity
    assert set(compilation.metadata["dependency_versions"]) == {"antlr4-python3-runtime", "numpy", "qiskit", "qiskit-aer"}


def test_artifacts_with_quantum_cleanup_and_runtime_guards_are_deterministic():
    source = """
        quint n=superposition(); int sample=measure(n); quint result=0;
        if(sample<0 || sample==2) { result+=1; }
        { quint temporary=n+1; if(temporary==2) { result+=1; } }
        return measure(result);
    """
    a, b = compiled(source), compiled(source)
    assert a.metadata == b.metadata
    assert python_source(a) == python_source(b)


def test_compilation_and_python_generation_do_not_import_backend(monkeypatch, tmp_path):
    original = builtins.__import__
    def no_backend(name, *args, **kwargs):
        if name.startswith(("qiskit", "numpy")):
            raise AssertionError(f"unexpected backend import {name}")
        return original(name, *args, **kwargs)
    monkeypatch.setattr(builtins, "__import__", no_backend)
    compilation = compiled(' quint q=1; return measure(q); ')
    generated(compilation, tmp_path)
    path = tmp_path / "main.qut"
    path.write_text(compilation.source)
    assert main(["check", str(path)]) == 0


def test_resource_report_counts_reserved_storage_and_preflights_before_builder():
    compilation = compiled(' quint q=1; { quint temporary=q+1; } return measure(q); ', max_simulation_qubits=3)
    cost = compilation.metadata["resources"]
    assert cost["allocated_qubits"] > cost["cleaned_qubits_at_end"] > 0
    assert not cost["wire_reuse"] and not cost["simulation_within_limit"]
    assert cost["statevector_bytes"] == 16 * 2**cost["allocated_qubits"]
    def forbidden():
        pytest.fail("builder must not run before preflight")
    with pytest.raises(DiagnosticError, match="simulation limit") as error:
        execute(forbidden, ResultLayout(compilation.program.result, compilation.metadata))
    assert error.value.code == "Q4001"


@pytest.mark.parametrize("options", [{"shots": 0}, {"shots": True}, {"shots": 1_000_001}, {"seed": -1}, {"seed": 2**32}, {"seed": False}])
def test_execution_options_checked_before_classical_or_quantum_execution(options):
    with pytest.raises(DiagnosticError) as error:
        compiled(' return 9; ').run(**options)
    assert error.value.code == "Q4001"


def test_classical_output_explicitly_reports_no_simulator_execution(tmp_path):
    compilation = compiled('input int n;  int total=0; for(int i=0;i<n;i++){ total+=i; } return total; ', {"n": 4})
    module = generated(compilation, tmp_path)
    result = module.run({"n": 5}, shots=3)
    assert result["outcomes"] == [{"value": 10, "count": 3, "probability": 1.0}]
    assert result["execution"]["backend"] == "classical-output"
    assert result["build"]["inputs"] == {"n": 5}


def test_lossless_large_integers_without_global_python_changes(tmp_path):
    limit = sys.get_int_max_str_digits()
    value = 10**5000 + 3
    source = 'input int n;  return n+1; '
    compilation = compiled(source, {"n": value})
    module = generated(compilation, tmp_path)
    payload = module.run(shots=1)
    assert load_json(json_text(payload))["outcomes"][0]["value"] == value + 1
    assert parse_integer(integer_text(-value)) == -value
    assert compiled("return " + integer_text(value) + ";").run(shots=1)["outcomes"][0]["value"] == value
    assert sys.get_int_max_str_digits() == limit
    with pytest.raises(ValueError, match="limit"):
        load_json("1" * 100_001)
    with pytest.raises(DiagnosticError):
        compiled("return " + "1" * 100_001 + ";")


def test_generated_metadata_honors_explicitly_larger_classical_memory_budget(tmp_path):
    value = 1 << 335_000
    compilation = compiled('input int n;  return n; ', {"n": value}, max_classical_bits=400_000)
    module = generated(compilation, tmp_path)
    assert module.run(shots=1)["outcomes"][0]["value"] == value


def test_artifact_write_is_deterministic_and_preserves_unrelated_files(tmp_path):
    compilation = compiled(' return 1; ')
    target = tmp_path / "output.py"
    target.write_text("user data", encoding="utf-8")
    with pytest.raises(DiagnosticError) as error:
        write_python(compilation, target)
    assert error.value.code == "Q0004" and target.read_text() == "user data"
    write_python(compilation, target, force=True)
    previous = target.read_bytes()
    write_python(compilation, target)
    assert target.read_bytes() == previous
    source = tmp_path / "source.qut"
    source.write_text(compilation.source)
    with pytest.raises(DiagnosticError, match="source file"):
        write_python(compile_source(compilation.source, path=str(source)), source, force=True)
    assert source.read_text() == compilation.source
    with pytest.raises(DiagnosticError):
        write_python(compilation, tmp_path / "absent" / "output.py")
    assert not list(tmp_path.glob(".qutes-*.tmp"))


def test_layout_roundtrip_and_unknown_schema():
    compilation = compiled(' qustring[] words=["A","AB"]; return measure(words); ', alphabet="AB")
    layout = layout_from_metadata(load_json(json_text(compilation.metadata)))
    assert layout.to_dict() == compilation.metadata["result_layout"]
    with pytest.raises(ValueError, match="schema"):
        layout_from_metadata({"artifact_schema": 10})


def test_missing_backend_is_a_deliberate_diagnostic(monkeypatch):
    compilation = compiled(' quint q=1; return measure(q); ')
    original = builtins.__import__
    def unavailable(name, *args, **kwargs):
        if name.startswith("qiskit"):
            raise ImportError("unavailable")
        return original(name, *args, **kwargs)
    monkeypatch.setattr(builtins, "__import__", unavailable)
    with pytest.raises(DiagnosticError) as error:
        compilation.run(shots=1)
    assert error.value.code == "Q5001"
    with pytest.raises(DiagnosticError) as error:
        compilation.build()
    assert error.value.code == "Q5001"


def test_deep_json_and_large_invalid_quantum_value_have_deliberate_diagnostics():
    with pytest.raises(ValueError, match="nesting"):
        load_json("[" * 2000 + "0" + "]" * 2000)
    with pytest.raises(DiagnosticError) as error:
        compiled('input int n;  quint q=n; return measure(q); ', {"n": 10**5000})
    assert error.value.code == "Q2001"
    assert "outside" in error.value.message


def test_cli_check_build_explain_and_config_precedence(tmp_path, capsys):
    source, config = tmp_path / "main.qut", tmp_path / "qutes.toml"
    source.write_text(' quint n=3; return measure(n); ')
    config.write_text("[qutes]\nquint_bits=3\nmax_simulation_qubits=2\n")
    assert main(["check", str(source), "--json"]) == 0
    checked = load_json(capsys.readouterr().out)
    assert checked["cleanup_verified"] is True
    assert checked["metadata"]["config"]["quint_bits"] == 3
    assert checked["metadata"]["resources"]["simulation_within_limit"] is False
    assert main(["build", str(source), "--json"]) == 0
    artifact = load_json(capsys.readouterr().out)
    assert Path(artifact["output"]).is_file()
    assert main(["explain", str(source), "--quint-bits", "4", "--json"]) == 0
    assert load_json(capsys.readouterr().out)["resources"]["allocated_qubits"] == 4
    assert main(["explain", str(source)]) == 0
    assert "wires are not reused" in capsys.readouterr().out
    assert main(["run", str(source), "--json"]) == 1
    assert load_json(capsys.readouterr().out)["diagnostics"][0]["code"] == "Q4001"


@pytest.mark.backend
def test_cli_seeded_run_decodes_signed_array_order(tmp_path, capsys):
    source = tmp_path / "main.qut"
    source.write_text(' quint[] values=[-1,2,0]; return measure(values); ')
    assert main(["run", str(source), "--quint-bits", "3", "--shots", "8", "--seed", "5", "--json"]) == 0
    assert load_json(capsys.readouterr().out)["outcomes"] == [{"value": [-1, 2, 0], "count": 8, "probability": 1.0}]


def test_cli_checks_unsafe_cleanup_and_non_object_inputs(tmp_path, capsys):
    source, inputs = tmp_path / "main.qut", tmp_path / "inputs.json"
    source.write_text(' quint n=superposition(); n=1; return measure(n); ')
    assert main(["check", str(source), "--json"]) == 1
    assert load_json(capsys.readouterr().out)["diagnostics"][0]["code"] == "Q3001"
    source.write_text(' return 1; ')
    inputs.write_text("[]")
    assert main(["check", str(source), "--inputs", str(inputs), "--json"]) == 1
    assert load_json(capsys.readouterr().out)["diagnostics"][0]["code"] == "Q2001"


@pytest.mark.backend
@pytest.mark.parametrize("filename,inputs,expected", [
    ("measurement_snapshots.qut", {}, [[5, 7]]), ("feedforward.qut", {}, [[False, False], [True, True]]),
    ("arrays.qut", {}, [6]), ("functions.qut", {}, [3]), ("coherent_if.qut", {}, [0, 1]),
    ("text.qut", {}, ["HI"]), ("loops.qut", {"count": 3}, [-4]),
])
def test_documented_examples_execute(filename, inputs, expected):
    folder = Path(__file__).resolve().parents[1] / "examples"
    compilation = compile_source((folder / filename).read_text(), inputs=inputs, config=CompilerConfig.load(folder / "qutes.toml"))
    result = compilation.run(shots=256, seed=73)
    assert {json_text(item["value"]) for item in result["outcomes"]} == {json_text(value) for value in expected}


@pytest.mark.backend
def test_limit_rechecked_after_backend_transpilation(monkeypatch):
    from qiskit import QuantumCircuit
    import qiskit
    import qiskit_aer
    compilation = compiled(' qubit q=false; return measure(q); ', max_simulation_qubits=2)
    monkeypatch.setattr(qiskit, "transpile", lambda *args, **kwargs: QuantumCircuit(3, 1))
    def forbidden(*args, **kwargs):
        pytest.fail("simulation must not start above the post-transpile limit")
    monkeypatch.setattr(qiskit_aer.AerSimulator, "run", forbidden)
    with pytest.raises(DiagnosticError, match="transpiled circuit") as error:
        compilation.run(shots=1)
    assert error.value.code == "Q4001"


@pytest.mark.backend
def test_backend_failure_is_diagnostic_and_seeded_runs_are_repeatable(monkeypatch):
    import qiskit
    compilation = compiled(' qubit q=superposition(); return measure(q); ')
    assert compilation.run(shots=32, seed=10) == compilation.run(shots=32, seed=10)
    def broken(*args, **kwargs):
        raise RuntimeError("test backend failure")
    monkeypatch.setattr(qiskit, "transpile", broken)
    with pytest.raises(DiagnosticError, match="test backend failure") as error:
        compilation.run(shots=1)
    assert error.value.code == "Q5002"
