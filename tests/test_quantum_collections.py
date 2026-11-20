import json

import numpy as np
import pytest
from qiskit.quantum_info import Statevector

from qutes.diagnostics import DiagnosticError
from tests.test_lowering import compile_source, distribution

pytestmark = pytest.mark.backend


def build(source, **settings):
    return compile_source(source, alphabet="AB", qustring_capacity=2, **settings)


def test_array_value_copy_preserves_old_values_after_indexed_updates():
    program = build("""
        quint[] a=[1,2]; quint[] b=copy(a); a[0]+=1; a[1]=1;
        return [measure(a[0]),measure(a[1]),measure(b[0]),measure(b[1])];
    """)
    assert distribution(program) == pytest.approx({"[2, 1, 1, 2]": 1})


def test_quantum_array_copies_keep_correlations_and_distinct_storage():
    program = build("""
        qubit flag=superposition(); qubit[] values=[flag,flag]; qubit[] copy=copy(values);
        values[0]=!values[0];
    """)
    expected = np.zeros(32, dtype=complex)
    expected[2] = expected[29] = 1 / np.sqrt(2)
    np.testing.assert_allclose(Statevector.from_instruction(program.to_qiskit()).data, expected, atol=1e-10)


def test_whole_array_assignment_uses_value_copy():
    program = build("""
        quint[] a=[1,-2]; quint[] b=[-1,0]; a=copy(b); b[0]+=1;
        return [measure(a[0]),measure(a[1]),measure(b[0])];
    """, quint_bits=2)
    assert distribution(program) == pytest.approx({"[-1, 0, 0]": 1})


def test_conditional_array_assignment_preserves_unselected_array():
    program = build("""
        qubit flag=superposition(); quint[] values=[0,1];
        if(flag) { values[0]=1; values[1]=0; }
        return measure(values);
    """, quint_bits=2)
    assert distribution(program) == pytest.approx({"[0, 1]": 0.5, "[1, 0]": 0.5})


def test_array_helper_return_moves_owned_elements_and_cleans_temporaries():
    program = build("""qubit[] pair(qubit flag) { qubit[] values=[flag,!flag]; return values; }
     qubit flag=superposition(); qubit[] result=pair(flag); return measure(result); """)
    assert distribution(program) == pytest.approx({"[false, true]": 0.5, "[true, false]": 0.5})
    assert len([allocation for allocation in program.allocations if not allocation.released]) == 3


def test_empty_quantum_array_has_no_storage_and_measures_empty_result():
    program = build(' qubit[] values=[]; return measure(values); ')
    assert program.qubit_count == program.classical_bit_count == 0
    assert program.result.decode(0) == []


def test_qustring_index_observation_keeps_parent_available():
    program = build("""
        qustring text="AB"; char initial=measure(text[1]); string before=measure(text);
        text="B"; string after=measure(text); return [before,after];
    """)
    assert distribution(program) == pytest.approx({'["AB", "B"]': 1})
    assert any(item.name == "$observed_element" and item.released for item in program.allocations)


def test_string_snapshot_retains_its_logical_length_after_overwrite():
    program = build(' qustring text=""; string a=measure(text); text="A"; return [a,measure(text)]; ')
    assert distribution(program) == pytest.approx({'["", "A"]': 1})


def test_string_equality_includes_length_and_padding():
    program = build(' qustring a=""; qustring b="A"; qustring c="B"; return [measure(a==b),measure(b!=c),measure(b=="A")]; ')
    assert distribution(program) == pytest.approx({"[false, true, true]": 1})


def test_coherent_character_and_string_assignment():
    program = build("""
        qubit flag=superposition(); qustring text="";
        if(flag) { text="A"; } else { text="B"; }
        return measure(text);
    """)
    assert distribution(program) == pytest.approx({'"A"': 0.5, '"B"': 0.5})


def test_text_array_lengths_are_known_through_helpers_and_foreach():
    program = build("""int size(qustring[] words) {
        int count=0; foreach(qustring word in words) { count+=word.Length; } return count;
    }
     qustring[] words=["A","BB",""]; words[0]="AB"; return size(words); """)
    assert program.result.decode(0) == 4


def test_foreach_text_view_sees_current_element_length():
    program = build("""
        qustring[] words=["A"]; int size=0;
        foreach(qustring word in words) { words[0]="AB"; size=word.Length; }
        return size;
    """)
    assert program.result.decode(0) == 2


def test_measured_text_array_has_known_element_lengths_and_preserved_snapshots():
    program = build(' qustring[] a=["A","BB"]; string[] before=measure(a); a[0]="B"; return before; ')
    assert distribution(program) == pytest.approx({'["A", "BB"]': 1})
    lengths = build(' qustring[] a=["A","BB"]; string[] measured=measure(a); return measured[1].Length; ')
    assert lengths.result.decode(0) == 2


def test_text_array_branch_lengths_must_agree_per_element():
    with pytest.raises(DiagnosticError, match="element lengths") as error:
        build(' qubit f=superposition(); qustring[] a=["A"]; if(f) { a[0]="BB"; } ')
    assert error.value.code == "Q2004"


def test_text_array_equal_branch_lengths_allow_different_text():
    program = build(' qubit f=superposition(); qustring[] a=[""]; if(f) { a[0]="AA"; } else { a[0]="BB"; } return measure(a); ')
    assert distribution(program) == pytest.approx({'["AA"]': 0.5, '["BB"]': 0.5})


def test_new_text_arrays_are_empty_strings_with_zero_padding():
    program = build(' qustring[] words=new qustring[2]; return measure(words); ')
    assert distribution(program) == pytest.approx({'["", ""]': 1})


def test_unicode_alphabet_measurement_and_copy():
    program = compile_source("quchar c='猫'; quchar d=c; return measure(d);", alphabet="λ猫", qustring_capacity=1)
    assert distribution(program) == pytest.approx({json.dumps("猫"): 1})


def test_huge_quantum_allocation_fails_before_building_bit_tuple():
    with pytest.raises(DiagnosticError) as error:
        build(' quint value=0; ', quint_bits=10**9)
    assert error.value.code == "Q4001"


def test_array_literal_rebinding_preserves_correlations():
    program = build("""
        qubit a=superposition(); qubit b=superposition(); qubit[] values=[a,b];
        values=[values[1],values[0]];
        return [measure(a),measure(b),measure(values[0]),measure(values[1])];
    """)
    assert program.qubit_count == 6
    expected = {json.dumps([a,b,b,a]): 0.25 for a in (False,True) for b in (False,True)}
    assert distribution(program) == pytest.approx(expected)


def test_string_permutation_preserves_each_elements_length():
    program = build(' qustring[] a=["A","BB"]; a=[a[1],a[0]]; return measure(a); ')
    assert distribution(program) == pytest.approx({'["BB", "A"]': 1})


def test_indexed_character_views_support_quantum_conditions():
    program = build("""
        qustring text="AB"; quint count=0;
        for(int i=0;i<text.Length;i++) { if(text[i]=='A') { count+=1; } }
        return measure(count);
    """, quint_bits=2)
    assert distribution(program) == pytest.approx({"1": 1})


def test_local_text_cleanup_preserves_coherent_result():
    program = build("""
        qubit flag=superposition(); qustring output="A";
        { qustring local="A"; if(flag) { local="B"; } output=local; }
    """)
    expected = np.zeros(2**program.qubit_count, dtype=complex)
    expected[0] = expected[3] = 1 / np.sqrt(2)
    np.testing.assert_allclose(Statevector.from_instruction(program.to_qiskit()).data, expected, atol=1e-10)
    assert program.allocations[-1].released


def test_classical_text_array_input_lifts_and_keeps_element_shapes():
    program = compile_source('input string[] words;  qustring[] qwords=words; return qwords[1].Length; ',
                             {"words": ["A", "BB"]}, alphabet="AB", qustring_capacity=2)
    assert program.result.decode(0) == 2
