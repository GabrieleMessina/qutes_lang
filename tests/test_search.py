import math
import numpy as np
import pytest
from qiskit.quantum_info import Statevector
from qutes.compiler import compile_source
from qutes.config import CompilerConfig
from qutes.diagnostics import DiagnosticError
from qutes.search import schedule
from tests.test_lowering import compile_source as lower_source, distribution


def build(source, **settings):
    return compile_source(source, config=CompilerConfig(quint_bits=2, alphabet="AB", **settings))


def final_bits(program, bits):
    lookup = program.wire_allocation.lookup()
    return [lookup.at(bit, len(program.operations)) for bit in bits]


def assert_free_zero(program, state):
    live = {i.physical for i in program.wire_allocation.intervals if i.end > len(program.operations)}
    for bit in set(range(program.qubit_count)) - live:
        assert state.probabilities([bit])[1] < 1e-12


def probabilities(compilation, name="result"):
    program = compilation.program
    state = Statevector.from_instruction(program.to_qiskit())
    owner = next(a for a in program.allocations if a.name == name)
    width = len(owner.bits) - len(owner.retained_index_bits) - len(owner.scratch_bits)
    assert_free_zero(program, state)
    return state.probabilities(final_bits(program, owner.bits[:width]))


@pytest.mark.parametrize("n", [1,2,3,4,5])
@pytest.mark.parametrize("threshold", [-2,-1,0,1])
def test_all_match_counts_small_circuits(n, threshold):
    values = [i % 3 - 1 for i in range(n)]
    source = f'qubit good(quint x) {{ return x <= {threshold}; }} quint result=search({values},good);'
    compilation = build(source)
    p = probabilities(compilation)
    good = {v % 4 for v in values if v <= threshold}
    bad = {v % 4 for v in values if v > threshold}
    assert sum(p[i] for i in good | bad) == pytest.approx(1)
    if good:
        assert sum(p[i] for i in good) >= .99 - 1e-10
    else:
        assert sum(p[i] for i in bad) == pytest.approx(1)


def test_duplicate_positions_have_equal_weight():
    c = build('qubit good(quint x){return x>0;} quint result=search([1,1,-1],good);')
    owner = c.program.allocations[0]
    s = Statevector.from_instruction(c.program.to_qiskit())
    p = s.probabilities(final_bits(c.program, owner.retained_index_bits))
    assert p[0] == pytest.approx(p[1])
    assert p[0] + p[1] >= .99
    assert p[3] < 1e-12


@pytest.mark.parametrize("source", [
    'qubit good(quchar c){return c==\'B\';} quchar result=search("ABA",good);',
    'qubit good(qustring t){return "?B" in t;} qustring result=search(["AA","AB"],good);',
    'qubit good(qubit x){return x;} qubit result=search([false,true],good);',
])
def test_element_types(source):
    p = probabilities(build(source))
    assert p[-1 if len(p)==2 else 2] >= .99


def test_quantum_collection_keeps_branch_weights_and_entanglement():
    c = build('qubit seed=superposition(); qubit[] data=[seed,!seed]; qubit good(qubit x){return x;} qubit result=search(data,good);')
    s = Statevector.from_instruction(c.program.to_qiskit())
    result = next(a for a in c.program.allocations if a.name == 'result')
    assert s.probabilities([0]) == pytest.approx([.5,.5])
    assert s.probabilities(final_bits(c.program, [result.bits[0]]))[1] >= .99
    # Each collection branch has a different matching position.
    joint = s.probabilities(final_bits(c.program, [0, result.retained_index_bits[0]]))
    assert joint[1] + joint[2] >= .99


def test_no_match_data_branches_are_not_amplified_away():
    c = build('qubit seed=superposition(); qubit[] data=[seed,seed]; qubit good(qubit x){return x;} qubit result=search(data,good);')
    owner = next(a for a in c.program.allocations if a.name == 'result')
    s = Statevector.from_instruction(c.program.to_qiskit())
    assert s.probabilities([0]) == pytest.approx([.5,.5])
    assert s.probabilities(final_bits(c.program, [owner.bits[0]])) == pytest.approx([.5,.5])


def test_scope_cleanup_and_returned_ownership():
    c = build('qubit good(quint x){return x==1;} {quint local=search([0,1],good);}')
    s = Statevector.from_instruction(c.program.to_qiskit()).data
    assert abs(s[0]) == pytest.approx(1)
    assert all(a.released for a in c.program.allocations)
    returned = build('qubit good(quint x){return x==1;} quint pick(){return search([0,1],good);} quint result=pick();')
    assert probabilities(returned, '$return')[1] >= .99


def test_explicit_measurement_and_post_measurement_evolution():
    p = lower_source('qubit good(qubit x){return x;} qubit result=search([false,true],good); bool before=measure(result); result=!result; return [before,measure(result)];')
    d = distribution(p)
    assert d['[true, false]'] >= .99
    assert sum(d.values()) == pytest.approx(1)


@pytest.mark.parametrize("source", [
    'qubit good(quint x){return x==0;} int[] a=[]; quint x=search(a,good);',
    'qubit good(qustring x){return true;} qustring x=search(["A","AB"],good);',
    'bool good(quint x){return true;} quint x=search([0,1],good);',
    'qubit good(quint x){int a=measure(x); return true;} quint x=search([0,1],good);',
    'qubit good(quint x){qubit a=superposition(); return a;} quint x=search([0,1],good);',
    'int g=0; qubit good(quint x){g=1; return true;} quint x=search([0,1],good);',
    'quint g=0; qubit good(quint x){return x==g;} quint x=search([0,1],good);',
    'qubit good(quint x){return x==1;} qubit flag=superposition(); if(flag){quint x=search([0,1],good);}',
    'qubit good(quint x){return good(x);} quint x=search([0,1],good);',
])
def test_rejected_search(source):
    with pytest.raises(DiagnosticError):
        build(source)


@pytest.mark.parametrize("value", [0,1,-.1,True,float('nan'),float('inf'),10**1000])
def test_invalid_failure_probability(value):
    with pytest.raises(ValueError, match='search_failure_probability'):
        CompilerConfig(search_failure_probability=value)


def test_schedule_matches_independent_chebyshev_bound():
    for n in (2,3,4,5,16,32):
        for failure in (.01,.05,.001):
            length = 2 * len(schedule(n,failure,10000)) + 1
            gamma_inverse = math.cosh(math.acosh(1/math.sqrt(failure))/length)
            for m in range(1,n+1):
                x = gamma_inverse * math.sqrt(1-m/n)
                assert abs(x) <= 1 + 1e-12
                success = 1 - failure * math.cos(length*math.acos(min(1,x)))**2
                assert success >= 1-failure-1e-12


def test_oracle_on_selected_string_and_source_inputs():
    source = 'input string[] texts; qubit good(qustring t){return "?B" in t;} qustring result=search(texts,good); return [measure(good(result)),measure(result[1])==\'B\'];'
    c = compile_source(source, inputs={'texts':['AA','AB']}, config=CompilerConfig(alphabet='AB'))
    d = distribution(c.program)
    assert d['[true, true]'] >= .99
    assert sum(d.values()) == pytest.approx(1)


def test_search_cleanup_restores_changed_input_versions():
    c = build('qubit seed=superposition(); qubit[] data=[seed,!seed]; qubit good(qubit x){return x;} {qubit local=search(data,good); data[0]=!data[0];}')
    s = Statevector.from_instruction(c.program.to_qiskit())
    owner = next(a for a in c.program.allocations if a.name == 'local')
    assert_free_zero(c.program, s)
    assert s.probabilities([0]) == pytest.approx([.5,.5])


def test_measured_hidden_selection_cannot_be_erased():
    with pytest.raises(DiagnosticError, match='measured'):
        build('qubit good(qubit x){return x;} {qubit local=search([false,true],good); bool b=measure(local);}')


@pytest.mark.parametrize('body', [
    'qubit f(quint x){return measure(x)==0;} qubit good(quint x){return f(x);}',
    'qubit f(quint x){qubit y=superposition(); return y;} qubit good(quint x){return f(x);}',
    'qubit f(quint x){return x==0;} qubit good(quint x){quint y=search([0,1],f); return y==0;}',
])
def test_transitive_oracle_effects_rejected(body):
    with pytest.raises(DiagnosticError):
        build(body + ' quint result=search([0,1],good);')


def test_classical_capture_changes_across_calls():
    c = build('int wanted=0; qubit good(quint x){return x==wanted;} quint first=search([0,1],good); wanted=1; quint second=search([0,1],good);')
    s = Statevector.from_instruction(c.program.to_qiskit())
    for name, expected in [('first',0),('second',1)]:
        owner = next(a for a in c.program.allocations if a.name == name)
        assert s.probabilities(final_bits(c.program, owner.bits[:2]))[expected] >= .99


def test_full_complex_state_with_external_reference_and_clean_workspace():
    from qiskit import QuantumCircuit
    from qutes.qiskit_backend import emit_gates
    from tests.reference import random_state
    c = build('qubit seed=superposition(); qubit[] data=[seed,!seed]; qubit good(qubit x){return x;} qubit result=search(data,good);')
    p = c.program
    owner = next(a for a in p.allocations if a.name == 'result')
    data = final_bits(p, [next(a for a in p.allocations if a.name == f'data[{i}]').bits[0] for i in range(2)])
    index_bit, value_bit = final_bits(p, [owner.retained_index_bits[0], owner.bits[0]])
    reference = p.qubit_count
    initial = random_state(2)
    qc = QuantumCircuit(reference + 1)
    qc.initialize(initial, [0, reference])
    # Replace the source's H preparation by an arbitrary reference-entangled state.
    qc.compose(emit_gates(p.qubit_count, p.operations[1:]), qubits=list(range(p.qubit_count)), inplace=True)
    actual = Statevector.from_instruction(qc).data
    expected = np.zeros_like(actual)
    # Independent dense reflections, with phases derived directly from the paper.
    L = 5
    scale = math.tanh(math.acosh(10)/L)
    alpha = [2*math.atan2(1,math.tan(2*math.pi*j/L)*scale) for j in (1,2)]
    for seed in (0,1):
        s = np.array([1,1], dtype=complex)/math.sqrt(2)
        selected = s.copy()
        for a,b in zip(alpha, [-v for v in reversed(alpha)]):
            marked = np.diag([np.exp(1j*b) if seed else 1, 1 if seed else np.exp(1j*b)])
            reflection = np.eye(2)-(1-np.exp(-1j*a))*np.outer(s,s.conj())
            selected = reflection @ marked @ selected
        for ref in (0,1):
            for index in (0,1):
                value = seed if index == 0 else 1-seed
                position = seed | (ref<<reference) | (seed<<data[0]) | ((1-seed)<<data[1])
                position |= index<<index_bit | value<<value_bit
                expected[position] = initial[seed+2*ref]*selected[index]
    np.testing.assert_allclose(actual, expected, atol=1e-10)


def test_search_budget_rejects_without_weakening_success_target():
    with pytest.raises(DiagnosticError, match='search.*budget') as error:
        build('qubit good(quint x){return x==1;} quint result=search([0,1,-1],good);',
              max_evaluation_steps=100, search_failure_probability=.000001)
    assert error.value.code == 'Q4001'


def test_search_through_helper_cannot_bypass_dynamic_control():
    with pytest.raises(DiagnosticError, match='dynamic control'):
        build('qubit good(qubit x){return x;} qubit pick(){return search([false,true],good);} qubit seed=superposition(); bool flag=measure(seed); if(flag){qubit result=pick();}')


def test_oracle_local_arithmetic_and_control():
    c = build('qubit good(quint x){quint shifted=x+1; qubit yes=false; if(shifted==0){yes=!yes;} return yes;} quint result=search([-1,0],good);')
    assert probabilities(c)[3] >= .99
