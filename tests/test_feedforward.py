import json
import operator

import numpy as np
import pytest
from qiskit import transpile
from qiskit_aer import AerSimulator

from qutes import classical as c, ir
from qutes.diagnostics import DiagnosticError
from qutes.feedforward import predicate
from qutes.gates import Measurement
from qutes.lowering import Result
from tests.test_lowering import CASES, ROOT, compile_source, distribution
from tests.test_measurement_cleanup import branches_for

pytestmark = pytest.mark.backend
OPERATORS = {"==": operator.eq, "!=": operator.ne, "<": operator.lt,
             "<=": operator.le, ">": operator.gt, ">=": operator.ge}


def executed_values(program, shots=256):
    simulator = AerSimulator()
    circuit = transpile(program.to_qiskit(), simulator, optimization_level=0, seed_transpiler=31)
    counts = simulator.run(circuit, shots=shots, seed_simulator=71).result().get_counts()
    return [(program.result.decode(int(memory.replace(" ", ""), 2)), count) for memory, count in counts.items()]


@pytest.mark.parametrize("width", [1, 2, 3, 4, 5])
@pytest.mark.parametrize("op", OPERATORS)
def test_classical_signed_comparison_exhaustive(width, op):
    a = tuple(c.Predicate("bit", value=i) for i in range(width))
    b = tuple(c.Predicate("bit", value=i + width) for i in range(width))
    condition = c.compare(a, b, op, signed=True)
    for x in range(2**width):
        for y in range(2**width):
            sx = x - 2**width if x & (1 << (width - 1)) else x
            sy = y - 2**width if y & (1 << (width - 1)) else y
            assert condition.evaluate(x | (y << width)) == OPERATORS[op](sx, sy)


@pytest.mark.parametrize("op", OPERATORS)
@pytest.mark.parametrize("constant", [-1000, -5, -4, -1, 0, 3, 4, 1000])
def test_classical_constants_are_sign_extended_never_truncated(op, constant):
    snapshot = Result(ir.Type("int"), "snapshot", bits=(0, 1, 2))
    value = Result(ir.Type("bool"), f"binary:{op}", (snapshot, Result(ir.Type("int"), "literal", value=constant)))
    condition = predicate(value)
    for bits in range(8):
        number = bits - 8 if bits >= 4 else bits
        assert condition.evaluate(bits) == OPERATORS[op](number, constant)


@pytest.mark.parametrize("case", [item for item in CASES if item["expect"] == "accept"], ids=lambda item: item["id"])
def test_all_positive_source_examples_execute_on_aer(case):
    program = compile_source((ROOT / case["file"]).read_text(), **case.get("config", {}))
    actual = {json.dumps(value) for value, _ in executed_values(program)}
    expected = {json.dumps(outcome["value"]) for outcome in case["outputs"]}
    assert actual == expected


@pytest.mark.parametrize("op", OPERATORS)
def test_generated_qiskit_signed_comparison_matches_every_observed_input_pair(op):
    program = compile_source(f"""
        quint a=superposition(); quint b=superposition();
        int x=measure(a); int y=measure(b); quint result=0;
        if(x {op} y) {{ result=1; }}
        return [x,y,measure(result)];
    """, quint_bits=2)
    values = executed_values(program, shots=512)
    assert len(values) == 16
    for (a, b, actual), _ in values:
        assert actual == int(OPERATORS[op](a, b))


def test_runtime_predicate_helpers_and_nested_boolean_expressions():
    program = compile_source("""bool selected(int value) { return value<0 || value==1; }
     quint q=superposition(); int n=measure(q); quint result=0;
        if(selected(n) && !(n == -1)) { result=1; }
        return [n,measure(result)];
    """, quint_bits=2)
    for (n, result), _ in executed_values(program):
        assert result == int((n < 0 or n == 1) and n != -1)


def test_earlier_snapshot_controls_after_source_changes_and_is_measured_again():
    program = compile_source("""
        qubit q=superposition(); bool before=measure(q); q=!q; bool after=measure(q);
        qubit output=false; if(before) { output=true; }
        return [before,after,measure(output)];
    """)
    assert distribution(program) == pytest.approx({"[false, true, false]": 0.5, "[true, false, true]": 0.5})
    assert {tuple(value) for value, _ in executed_values(program)} == {(False, True, False), (True, False, True)}


def test_conditional_overwrite_preserves_old_value_in_unselected_runtime_branch():
    program = compile_source("""
        qubit q=superposition(); bool selected=measure(q); quint result=1;
        if(selected) { result=2; } return measure(result);
    """)
    assert distribution(program) == pytest.approx({"1": 0.5, "2": 0.5})
    assert {value for value, _ in executed_values(program)} == {1, 2}


def test_runtime_and_quantum_controls_preserve_unmeasured_coherence():
    program = compile_source("""
        qubit choice=superposition(); qubit coherent=superposition();
        bool selected=measure(choice); quint result=0;
        if(selected) { if(coherent) { result+=2; } }
        else { if(coherent) { result+=1; } }
    """)
    assert sum(isinstance(op, Measurement) for op in program.operations) == 1
    for branch in branches_for(program):
        selected = branch.snapshots[0]
        expected = np.zeros_like(branch.state)
        expected[selected] = 1 / np.sqrt(2)
        expected[selected | 2 | ((2 if selected else 1) << 2)] = 1 / np.sqrt(2)
        np.testing.assert_allclose(branch.state, expected, atol=1e-10)
        assert branch.probability == pytest.approx(0.5)


def test_quantum_outer_runtime_inner_controls_execute_correctly():
    program = compile_source("""
        qubit a=superposition(); qubit b=superposition(); bool selected=measure(a); quint output=0;
        if(b) { if(selected) { output+=1; } else { output+=2; } }
        return measure(output);
    """)
    assert distribution(program) == pytest.approx({"0": 0.5, "1": 0.25, "2": 0.25})
    assert {value for value, _ in executed_values(program)} == {0, 1, 2}


def test_runtime_branch_locals_clean_after_input_version_changes():
    program = compile_source("""
        qubit q=superposition(); bool selected=measure(q); quint n=1; quint result=0;
        if(selected) { quint local=n+1; result+=local; n+=1; }
        return measure(result);
    """)
    assert distribution(program) == pytest.approx({"0": 0.5, "2": 0.5})
    assert all(item.released for item in program.allocations if item.name == "local")


@pytest.mark.parametrize("literal, expected", [('"AB"', 1), ('"BA"', 0), ('"A"', 0), ('"ZZ"', 0)])
def test_runtime_text_equality_includes_encoding_and_length(literal, expected):
    program = compile_source(f"""
        qustring text="AB"; string observed=measure(text); quint result=0;
        if(observed == {literal}) {{ result=1; }} return measure(result);
    """, alphabet="AB", qustring_capacity=2)
    assert executed_values(program, shots=8) == [(expected, 8)]


def test_runtime_text_index_and_array_snapshots_can_control_circuit():
    program = compile_source("""
        qustring[] words=["AB","BA"]; string[] samples=measure(words); quint result=0;
        if(samples[0][1]=='B' && samples[1]=="BA") { result=1; }
        return measure(result);
    """, alphabet="AB", qustring_capacity=2)
    assert executed_values(program, shots=8) == [(1, 8)]


def test_runtime_array_replacement_is_guarded():
    program = compile_source("""
        qubit q=superposition(); bool selected=measure(q); quint[] values=[0,1];
        if(selected) { values=[1,0]; } return measure(values);
    """, quint_bits=2)
    assert distribution(program) == pytest.approx({"[0, 1]": 0.5, "[1, 0]": 0.5})
    assert {tuple(value) for value, _ in executed_values(program)} == {(0, 1), (1, 0)}


def test_runtime_self_permutation_never_uses_unconditional_rebinding():
    source = """
        qubit q=superposition(); bool selected=measure(q); quint[] values=[0,1];
        if(selected) { values=[values[1],values[0]]; } return measure(values);
    """
    try:
        program = compile_source(source, quint_bits=2)
    except DiagnosticError as error:
        # The conservative scheduler may reject the temporary dependency cycle.
        assert error.code == "Q3001"
    else:
        assert distribution(program) == pytest.approx({"[0, 1]": 0.5, "[1, 0]": 0.5})


@pytest.mark.parametrize("expression", ["selected || measure(other)", "selected && measure(other)"])
def test_short_circuit_never_silently_emits_conditional_measurement_eagerly(expression):
    with pytest.raises(DiagnosticError, match="short-circuited") as error:
        compile_source(f" qubit a=false; qubit other=false; bool selected=measure(a); return {expression}; ")
    assert error.value.code == "Q2004"


def test_construction_time_short_circuit_can_skip_measurement():
    program = compile_source(' qubit q=superposition(); return false && measure(q); ')
    assert not any(isinstance(op, Measurement) for op in program.operations)
    assert program.result.decode(0) is False


def test_constant_folded_runtime_condition_and_repeated_conditions():
    program = compile_source("""
        qubit q=superposition(); bool selected=measure(q); quint value=0;
        if(selected || true) { value+=1; }
        if(selected) { if(selected) { value+=1; } else { value=3; } }
        return measure(value);
    """)
    assert {value for value, _ in executed_values(program)} == {1, 2}


def test_runtime_branch_can_prepare_and_clean_an_independent_local():
    program = compile_source("""
        qubit choice=superposition(); bool selected=measure(choice);
        if(selected) { qubit unused=superposition(); }
        return selected;
    """)
    for branch in branches_for(program):
        expected = np.zeros_like(branch.state)
        expected[branch.snapshots[0]] = 1
        np.testing.assert_allclose(branch.state, expected, atol=1e-10)


def test_out_of_range_constant_feedforward_executes_without_unsigned_wrapping():
    program = compile_source("""
        quint q=superposition(); int observed=measure(q); quint result=0;
        if(observed < 1000 && -1000 < observed && observed != 1000) { result=1; }
        return measure(result);
    """, quint_bits=2)
    assert {value for value, _ in executed_values(program)} == {1}


def test_anonymous_measured_helper_result_is_cleaned_without_consuming_named_values():
    program = compile_source('qubit choice() { qubit q=superposition(); return q; }  return measure(choice()); ')
    assert all(item.released for item in program.allocations)
    for branch in branches_for(program):
        np.testing.assert_allclose(branch.state, [1, 0], atol=1e-10)
    assert distribution(program) == pytest.approx({"false": 0.5, "true": 0.5})


def test_unused_helper_root_and_anonymous_computed_argument_do_not_leak():
    program = compile_source("""qubit prepare() { qubit q=superposition(); return q; }
    quint add(quint q) { return q+1; }
     prepare(); quint operand=0; quint output=add(operand+1); return measure(output); """, quint_bits=3)
    assert distribution(program) == pytest.approx({"2": 1})
    assert len([item for item in program.allocations if not item.released]) == 2


def test_anonymous_root_correlated_with_named_result_cannot_be_hidden_at_shot_end():
    with pytest.raises(DiagnosticError, match="still depends") as error:
        compile_source("""qubit prepare() { qubit q=superposition(); return q; }
         qubit flag=superposition(); qubit result=prepare() && flag; """)
    assert error.value.code == "Q3001"
