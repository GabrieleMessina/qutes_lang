import pytest
import numpy as np
from qiskit.quantum_info import Statevector
from qutes.diagnostics import DiagnosticError
from tests.test_lowering import compile_source, distribution


@pytest.mark.parametrize("expression,expected", [
    ("3 in [1,3,5]", True), ("[1,3] in [1,2,3]", False),
    ("[2,3] in [1,2,3,4]", True), ('\'B\' in "ABC"', True),
    ('"BC" in "ABCD"', True), ('[\'B\',\'C\'] in "ABCD"', True),
    ('"BC" in [\'A\',\'B\',\'C\']', True), ('"B" in ["AB","BC"]', False),
    ('["AB","CD"] in ["XY","AB","CD"]', True),
    ('"A?C" in "XABCY"', True), ('"AA" in "AAA"', True),
    ('"" in ""', True), ("[] in []", True), ("1 in []", False),
    ('"ABC" in "AB"', False), ('"ABC" in "A?C"', False),
])
def test_classical_membership(expression, expected):
    assert compile_source(f"return {expression};").result.decode(0) is expected


@pytest.mark.parametrize("source", [
    'quint[] a=[1,2]; return measure(2 in a);',
    'quint p=2; return measure(p in [1,2]);',
    'qustring t="AB"; return measure("A?" in t);',
    'qustring p="A?"; return measure(p in "AB");',
    'qustring t="AAA"; return measure("AA" in t);',
    'qustring t="AB"; return measure(t in t);',
])
def test_quantum_membership(source):
    program = compile_source(source, alphabet="AB?", qustring_capacity=3, quint_bits=3)
    assert distribution(program) == pytest.approx({"true": 1})


def test_classical_wildcard_does_not_need_encoding():
    program = compile_source('qustring t="AB"; return measure("A?" in t);', alphabet="AB")
    assert distribution(program) == pytest.approx({"true": 1})


def test_membership_preserves_joint_amplitudes_and_cleans_scratch():
    program = compile_source('qubit a=superposition(); qubit b=superposition(); qubit[] xs=[a,b]; qubit found=true in xs;')
    state = Statevector.from_instruction(program.to_qiskit()).data
    live = {item.name: item.bits for item in program.allocations if not item.released}
    expected = np.zeros_like(state)
    for a in range(2):
        for b in range(2):
            value = sum(bit_value << live[name][0] for name, bit_value in [("a", a), ("b", b), ("xs[0]", a), ("xs[1]", b), ("found", a | b)])
            expected[value] = .5
    np.testing.assert_allclose(state, expected, atol=1e-10)


def test_foreach_strings():
    assert compile_source('int n=0; foreach(char c in "ABC") { n+=1; } return n;').result.decode(0) == 3
    program = compile_source('qustring t="AB"; qubit found=false; foreach(quchar c in t) { if(c==\'B\') { found=!found; } } return measure(found);', alphabet="AB")
    assert distribution(program) == pytest.approx({"true": 1})


@pytest.mark.parametrize("source", ['return 1 in 2;', 'return true in [1,2];', 'quint x=1; int y=measure(x); return y in [1,2];'])
def test_invalid_membership(source):
    with pytest.raises(DiagnosticError):
        compile_source(source)


def test_left_operand_is_captured_before_right_operand_updates_it():
    p = compile_source('quint p=1; quint[] items(){p+=1; return [1];} qubit found=p in items(); return measure(found);')
    assert distribution(p) == pytest.approx({'true':1})


def test_quantum_wildcard_value_preserves_correlation():
    p = compile_source('qubit seed=superposition(); quchar pattern=\'A\'; if(seed){pattern=\'?\';} qubit found=pattern in "B"; return [measure(seed),measure(found)];', alphabet='AB?')
    assert distribution(p) == pytest.approx({'[false, false]':.5,'[true, true]':.5})


def test_overlapping_membership_with_complex_reference_entanglement():
    from qiskit import QuantumCircuit
    from qutes.qiskit_backend import emit_gates
    from tests.reference import random_state
    p = compile_source('qubit a=superposition(); qubit b=superposition(); qubit[] arr=[a,b,a]; qubit found=[true,true] in arr;')
    live = {item.name:item.bits for item in p.allocations if not item.released}
    initial = random_state(3)
    reference = p.qubit_count
    qc = QuantumCircuit(reference+1)
    qc.initialize(initial,[0,1,reference])
    qc.compose(emit_gates(p.qubit_count,p.operations[2:]),list(range(p.qubit_count)),inplace=True)
    state = Statevector.from_instruction(qc).data
    expected = np.zeros_like(state)
    for a in (0,1):
        for b in (0,1):
            for r in (0,1):
                bits = [('a',a),('b',b),('arr[0]',a),('arr[1]',b),('arr[2]',a),('found',a & b)]
                position = sum(value<<live[name][0] for name,value in bits) | r<<reference
                expected[position] = initial[a+2*b+4*r]
    np.testing.assert_allclose(state,expected,atol=1e-10)


def test_membership_protects_all_quantum_dependencies():
    with pytest.raises(DiagnosticError,match='protected'):
        compile_source('quint p=1; quint[] a=[1,2]; if(p in a){a[0]+=1;}')


def test_classical_membership_preflights_comparison_work():
    with pytest.raises(DiagnosticError, match='budget') as error:
        compile_source('input int[] p; input int[] a; return p in a;',
                       inputs={'p':[1]*15,'a':[1]*30},max_evaluation_steps=100)
    assert error.value.code == 'Q4001'
