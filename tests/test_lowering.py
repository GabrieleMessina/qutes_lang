import json
from pathlib import Path

import numpy as np
import pytest
from qiskit import transpile
from qiskit.quantum_info import Statevector
from qiskit_aer import AerSimulator

from qutes.checker import analyze
from qutes.config import CompilerConfig
from qutes.construction import construct
from qutes.diagnostics import DiagnosticError
from qutes.lowering import lower
from qutes.parser import parse
from tests.test_measurement_cleanup import branches_for

pytestmark = pytest.mark.backend
ROOT = Path(__file__).parent / "acceptance"
CASES = json.loads((ROOT / "cases.json").read_text())["cases"]
SUPPORTED_CASES = {case["id"] for case in CASES if case["expect"] == "accept" and case["id"] != "A007"}


def compile_source(source, inputs=None, **settings):
    config = CompilerConfig.resolve({"quint_bits": 3}, settings)
    return lower(construct(analyze(parse(source, "program.qut"), config), inputs))


def distribution(program):
    probabilities = {}
    for branch in branches_for(program):
        memory = sum(value << index for index, value in enumerate(branch.snapshots))
        value = json.dumps(program.result.decode(memory))
        probabilities[value] = probabilities.get(value, 0) + branch.probability
    return probabilities


@pytest.mark.parametrize("case", [case for case in CASES if case["id"] in SUPPORTED_CASES], ids=lambda case: case["id"])
def test_supported_source_corpus_has_exact_output_distribution(case):
    program = compile_source((ROOT / case["file"]).read_text(), **case.get("config", {}))
    assert program.cleanup_verified
    expected = {json.dumps(item["value"]): item["probability"] for item in case["outputs"]}
    assert distribution(program) == pytest.approx(expected)
    assert all(allocation.bits for allocation in program.allocations)


@pytest.mark.parametrize("case", [case for case in CASES if case["expect"] == "reject"], ids=lambda case: case["id"])
def test_entire_negative_source_corpus_rejected_with_expected_diagnostic(case):
    with pytest.raises(DiagnosticError) as error:
        compile_source((ROOT / case["file"]).read_text(), **case.get("config", {}))
    assert error.value.code == case["code"]


def test_source_scope_cleanup_restores_changed_input_and_keeps_correlations():
    program = compile_source("""void main() {
        quint input = superposition();
        quint output = 0;
        { quint adjusted = input + 1; output += adjusted; input += -2; }
    }""", quint_bits=2)
    expected = np.zeros(2**program.qubit_count, dtype=complex)
    for value in range(4):
        expected[(value + 2) % 4 | (((value + 1) % 4) << 2)] = 0.5
    actual = Statevector.from_instruction(program.to_qiskit()).data
    np.testing.assert_allclose(actual, expected, atol=1e-10)
    assert len(program.cleanup_events) == 1
    assert program.allocations[-1].released


def test_nested_expressions_clean_their_computed_intermediates():
    program = compile_source("""void main() {
        quint input = superposition();
        quint output = rotateLeft(input + 1, 1) + (input + -2);
    }""", quint_bits=2)
    expected = np.zeros(2**program.qubit_count, dtype=complex)
    for value in range(4):
        a = (value + 1) % 4
        rotated = ((a & 1) << 1) | ((a >> 1) & 1)
        expected[value | (((rotated + value + 2) % 4) << 2)] = 0.5
    actual = Statevector.from_instruction(program.to_qiskit()).data
    np.testing.assert_allclose(actual, expected, atol=1e-10)
    assert all(item.released for item in program.allocations[2:])


def test_nested_reversible_assignment_uses_pre_assignment_operands():
    program = compile_source("""int main() {
        quint a=1; quint b=2;
        a = rotateLeft(a + b, 1) + (b + 1);
        return measure(a);
    }""", quint_bits=3)
    assert distribution(program) == {"1": 1}


def test_separate_result_doubling_is_allowed_but_aliased_doubling_is_not():
    program = compile_source("int main() { quint a=superposition(); quint b=a+a; return measure(b); }", quint_bits=2)
    assert distribution(program) == pytest.approx({"0": 0.5, "-2": 0.5})
    with pytest.raises(DiagnosticError) as error:
        compile_source("void main() { quint a=superposition(); a=a+a; }")
    assert error.value.code == "Q3001"


def test_helper_return_move_keeps_owned_result_and_cleans_local_work():
    program = compile_source("""quint compute(quint input) {
        quint local=input+1;
        return local+2;
    }
    int main() { quint input=1; quint result=compute(input); return measure(result); }""", quint_bits=4)
    assert distribution(program) == pytest.approx({"4": 1})
    assert len([item for item in program.allocations if not item.released]) == 2


def test_helper_cannot_hide_a_correlated_independent_root():
    with pytest.raises(DiagnosticError, match="still depends") as error:
        compile_source("""qubit invalid() { qubit local=superposition(); qubit result=local; return result; }
        bool main() { qubit output=invalid(); return measure(output); }""")
    assert error.value.code == "Q3001"


def test_measured_local_can_be_cleaned_and_result_snapshot_survives_scope():
    program = compile_source("""bool main() {
        bool result=false;
        { qubit local=superposition(); result=measure(local); local=!local; }
        return result;
    }""")
    assert distribution(program) == pytest.approx({"false": 0.5, "true": 0.5})
    for branch in branches_for(program):
        np.testing.assert_allclose(branch.state, [1, 0], atol=1e-10)


def test_indirect_observation_cannot_silently_use_original_preparation():
    with pytest.raises(DiagnosticError, match="related value was measured"):
        compile_source("""void main() {
            { qubit local=superposition(); qubit copy=local; bool value=measure(copy); }
        }""")


def test_expanded_loop_has_distinct_snapshots_and_clean_local_storage():
    program = compile_source("""int[] main() {
        int[] results=new int[3];
        for(int i=0;i<3;i++) { quint local=i; results[i]=measure(local); }
        return results;
    }""")
    assert distribution(program) == {"[0, 1, 2]": 1}
    assert len(program.cleanup_events) == 3
    assert program.classical_bit_count == 9
    for branch in branches_for(program):
        expected = np.zeros_like(branch.state)
        expected[0] = 1
        np.testing.assert_allclose(branch.state, expected, atol=1e-10)


def test_classical_only_program_needs_no_qubits():
    program = compile_source("int main(int n) { return n+2; }", {"n": 5})
    assert program.qubit_count == program.classical_bit_count == 0
    assert program.result.decode(0) == 7
    assert program.to_qiskit().num_qubits == 0


def test_source_generated_qiskit_executes_snapshots_and_evolution():
    program = compile_source((ROOT / "A004_snapshots.qut").read_text(), quint_bits=4)
    simulator = AerSimulator()
    compiled = transpile(program.to_qiskit(), simulator, optimization_level=0, seed_transpiler=13)
    results = simulator.run(compiled, shots=16, seed_simulator=17).result()
    counts = results.get_counts()
    assert len(counts) == 1
    assert program.result.decode(int(next(iter(counts)), 2)) == [5, 7]


def test_partial_lowerer_reports_unimplemented_feedforward_instead_of_ignoring_it():
    with pytest.raises(DiagnosticError, match="source feedforward lowering is not implemented"):
        compile_source((ROOT / "A007_feedforward.qut").read_text())
