import operator

import numpy as np
import pytest
from qiskit.quantum_info import Statevector

from qutes.diagnostics import DiagnosticError
from qutes.qiskit_backend import emit_gates
from tests.reference import random_state
from tests.test_lowering import compile_source, distribution

pytestmark = pytest.mark.backend
COMPARISONS = {"==": operator.eq, "!=": operator.ne, "<": operator.lt,
               "<=": operator.le, ">": operator.gt, ">=": operator.ge}


def signed(value, width):
    return value - 2**width if value >= 2**(width - 1) else value


@pytest.mark.parametrize("width", [1, 2, 3])
@pytest.mark.parametrize("comparison", COMPARISONS)
def test_signed_comparator_full_complex_state_and_clean_scratch(width, comparison):
    program = compile_source(f"void main() {{ quint a=0; quint b=0; qubit p=a {comparison} b; }}", quint_bits=width)
    # Use arbitrary inputs entangled with an extra reference, while computed
    # output and scratch begin at zero. No backend comparator is used by the oracle.
    source = random_state(2 * width + 1, seed=47)
    initial = np.zeros(2**(program.qubit_count + 1), dtype=complex)
    expected = np.zeros_like(initial)
    for index, amplitude in enumerate(source):
        a, b = index % 2**width, (index >> width) % 2**width
        base = (index % 2**(2 * width)) | ((index >> (2 * width)) << program.qubit_count)
        truth = COMPARISONS[comparison](signed(a, width), signed(b, width))
        initial[base] = amplitude
        expected[base | (int(truth) << (2 * width))] = amplitude
    actual = Statevector(initial).evolve(emit_gates(program.qubit_count + 1, program.operations)).data
    np.testing.assert_allclose(actual, expected, atol=1e-10)
    assert all(item.released for item in program.allocations[3:])


@pytest.mark.parametrize("comparison", COMPARISONS)
@pytest.mark.parametrize("constant", [-4, -1, 0, 3])
def test_signed_comparison_against_classical_constant(comparison, constant):
    program = compile_source(f"bool main() {{ quint a=superposition(); qubit p=a {comparison} {constant}; return measure(p); }}")
    truth_count = sum(COMPARISONS[comparison](value, constant) for value in range(-4, 4))
    expected = {}
    if truth_count:
        expected["true"] = truth_count / 8
    if truth_count < 8:
        expected["false"] = 1 - truth_count / 8
    assert distribution(program) == pytest.approx(expected)


@pytest.mark.parametrize("comparison", COMPARISONS)
def test_comparison_with_identical_operands(comparison):
    program = compile_source(f"bool main() {{ quint a=superposition(); qubit p=a {comparison} a; return measure(p); }}")
    expected = COMPARISONS[comparison](0, 0)
    assert distribution(program) == pytest.approx({str(expected).lower(): 1})


@pytest.mark.parametrize("expression", ["a && b", "a || b", "a && a", "a || a", "a == b", "a != b", "!a"])
def test_boolean_predicates_preserve_coherence(expression):
    program = compile_source(f"void main() {{ qubit a=superposition(); qubit b=superposition(); qubit result={expression}; }}")
    expected = np.zeros(2**program.qubit_count, dtype=complex)
    for a in (False, True):
        for b in (False, True):
            truth = {"a && b": a and b, "a || b": a or b, "a && a": a,
                     "a || a": a, "a == b": a == b, "a != b": a != b, "!a": not a}[expression]
            expected[int(a) | (int(b) << 1) | (int(truth) << 2)] = 0.5
    np.testing.assert_allclose(Statevector.from_instruction(program.to_qiskit()).data, expected, atol=1e-10)


def test_conditional_overwrite_preserves_unselected_old_value():
    program = compile_source("void main() { qubit flag=superposition(); quint value=1; if(flag) { value=2; } }")
    expected = np.zeros(2**program.qubit_count, dtype=complex)
    expected[1 << 1] = expected[1 | (2 << 1)] = 1 / np.sqrt(2)
    np.testing.assert_allclose(Statevector.from_instruction(program.to_qiskit()).data, expected, atol=1e-10)


def test_conditional_overwrite_of_derived_value_controls_its_cleanup():
    program = compile_source("""void main() {
        qubit flag=superposition(); quint source=superposition(); quint value=source+1;
        if(flag) { value=source + -1; }
    }""", quint_bits=2)
    expected = np.zeros(2**program.qubit_count, dtype=complex)
    for flag in range(2):
        for source in range(4):
            value = (source + (-1 if flag else 1)) % 4
            expected[flag | (source << 1) | (value << 3)] = 1 / np.sqrt(8)
    np.testing.assert_allclose(Statevector.from_instruction(program.to_qiskit()).data, expected, atol=1e-10)


def test_nested_branches_and_local_arithmetic_leave_zero_scratch():
    program = compile_source("""void main() {
        quint input=superposition(); quint result=0;
        if(input<0) {
            quint local=input+1;
            if(local == 0) { result=1; } else { result=2; }
        } else { result=3; }
    }""")
    expected = np.zeros(2**program.qubit_count, dtype=complex)
    for value in range(8):
        logical = signed(value, 3)
        result = (1 if logical == -1 else 2) if logical < 0 else 3
        expected[value | (result << 3)] = 1 / np.sqrt(8)
    np.testing.assert_allclose(Statevector.from_instruction(program.to_qiskit()).data, expected, atol=1e-10)
    assert all(item.released for item in program.allocations[2:])


def test_branch_dependent_local_cleans_after_predicate_input_changes():
    program = compile_source("""void main() {
        quint input=superposition(); quint output=0;
        { quint local=0; if(input<0) { local+=1; } output+=local; input+=1; }
    }""", quint_bits=2)
    expected = np.zeros(2**program.qubit_count, dtype=complex)
    for value in range(4):
        expected[((value + 1) % 4) | (int(value >= 2) << 2)] = 0.5
    np.testing.assert_allclose(Statevector.from_instruction(program.to_qiskit()).data, expected, atol=1e-10)


def test_functions_and_loops_inside_coherent_branch():
    program = compile_source("""quint next(quint n) { return n+1; }
    int main() {
        qubit flag=superposition(); quint output=0;
        if(flag) { for(int i=0;i<2;i++) { quint value=next(output); output+=1; } }
        return measure(output);
    }""")
    assert distribution(program) == pytest.approx({"0": 0.5, "2": 0.5})


def test_contradictory_nested_controls_do_nothing():
    program = compile_source("""int main() {
        qubit flag=superposition(); quint output=1;
        if(flag) { if(flag) { output+=1; } else { output=3; } }
        return measure(output);
    }""")
    assert distribution(program) == pytest.approx({"1": 0.5, "2": 0.5})


def test_unknown_root_overwrite_stays_rejected_inside_branch():
    with pytest.raises(DiagnosticError) as error:
        compile_source("void main() { qubit flag=superposition(); quint n=superposition(); if(flag) { n=0; } }")
    assert error.value.code == "Q3001"


def test_compound_predicate_and_literal_left_comparison():
    program = compile_source("""int main() {
        quint n=superposition(); quint result=0;
        if ((0 > n && n >= -1) || n == 1) { result=1; }
        return measure(result);
    }""", quint_bits=2)
    assert distribution(program) == pytest.approx({"0": 0.5, "1": 0.5})
