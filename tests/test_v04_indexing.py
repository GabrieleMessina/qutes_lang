import numpy as np
import pytest
from qiskit.quantum_info import Statevector

from qutes.compiler import compile_source
from qutes.config import CompilerConfig
from qutes.diagnostics import DiagnosticError
from qutes.codegen import python_source
from qutes import support
from tests.test_lowering import distribution


def compile(source, **settings):
    return compile_source(source, config=CompilerConfig(quint_bits=3, alphabet='AB', **settings))


@pytest.mark.parametrize('declaration,result,expected', [
    ('int[] values=[1,2,3];', 'quint', {'1':.5,'3':.5}),
    ('quint[] values=[1,2,3];', 'quint', {'1':.5,'3':.5}),
    ('bool[] values=[false,true,true];', 'qubit', {'false':.5,'true':.5}),
    ('qubit[] values=[false,true,true];', 'qubit', {'false':.5,'true':.5}),
    ('string values="ABA";', 'quchar', {'"A"':1}),
    ('qustring values="ABA";', 'quchar', {'"A"':1}),
    ("char[] values=['A','A','B'];", 'quchar', {'"A"':.5,'"B"':.5}),
    ('string[] values=["AA","AA","BB"];', 'qustring', {'"AA"':.5,'"BB"':.5}),
    ('qustring[] values=["AA","AA","BB"];', 'qustring', {'"AA"':.5,'"BB"':.5}),
    ('string[] values=["","",""];', 'qustring', {'""':1}),
])
def test_quantum_reads_across_collection_types(declaration, result, expected):
    c=compile(declaration+'quint i=superposition([0,2]);'+result+' selected=values[i];return measure(selected);',qustring_capacity=3)
    assert distribution(c.program) == pytest.approx(expected)
    assert not c.program.searches


def test_quantum_read_full_complex_correlations_and_zero_workspace():
    c=compile('''
        qubit reference=false;hadamard(reference);phase(reference,pi/3.0);
        quint i=superposition([0,1],amplitudes:[complex(0.6,0),complex(0,0.8)]);
        quint[] values=[0,1];if(reference){values[0]+=1;values[1]+=1;}
        quint chosen=values[i];
    ''',wire_reuse=False)
    expected=np.zeros(1<<13,dtype=complex)
    for r in (0,1):
        for i, amplitude in ((0,.6),(1,.8j)):
            basis=r | i<<1 | r<<4 | (1+r)<<7 | (i+r)<<10
            expected[basis]=amplitude*np.exp(1j*r*np.pi/3)/np.sqrt(2)
    assert c.program.qubit_count == 13
    np.testing.assert_allclose(Statevector.from_instruction(c.build()[0]).data,expected,atol=1e-12)


def test_index_and_collection_can_share_storage():
    c=compile('quint i=superposition([0,1]);quint[] values=[i,0];quint selected=values[values[0]];return measure(selected);')
    assert distribution(c.program) == pytest.approx({'0':1})


def test_bounds_follow_mutable_calls_copies_and_dynamic_joins():
    c=compile('''
        void next(mut quint i){i+=1;}
        quint previous(quint i){return i-1;}
        quint[] a=[0];quint[] alias=a;next(alias[0]);
        quint[] b=copy(a);qubit flag=superposition();if(flag){b[0]+=1;}
        quint i=previous(b[0]);int[] values=[2,3];quint selected=values[i];
        return measure(selected);
    ''')
    assert distribution(c.program) == pytest.approx({'2':.5,'3':.5})


@pytest.mark.parametrize('body', [
    'quint i=superposition();quint x=values[i];',
    'quint i=superposition([-1,0]);quint x=values[i];',
    'quint i=superposition([0,2]);quint x=values[i];',
    'quint i=superposition([0,2],amplitudes:[1.0,complex(1e-200,0)]);quint x=values[i];',
    'quint i=1;i+=3;quint x=values[i];',
    'quint i=0;qubit b=superposition();if(b){i+=2;}quint x=values[i];',
    'quint[] a=[0];quint[] b=a;b[0]+=2;quint x=values[a[0]];',
    'quint[] a=[0];qubit b=superposition();if(b){a[0]+=2;}quint x=values[a[0]];',
])
def test_unsafe_or_unproved_bounds_reject(body):
    with pytest.raises(DiagnosticError,match='cannot prove quantum index bounds'):
        compile('int[] values=[1,2];'+body)


@pytest.mark.parametrize('source,message', [
    ('float[] a=[1.0];quint i=0;quint b=a[i];','quantum indexing supports'),
    ('string[] a=["A","BB"];quint i=0;qustring b=a[i];','same known length'),
    ('qubit q=false;bool[] a=[measure(q)];quint i=0;qubit b=a[i];','runtime-classical'),
    ('qubit[] a=[false];quint i=0;not(a[i]);','mutable'),
    ('quint[] a=[0];quint i=0;a[i]=1;','quantum-indexed'),
])
def test_invalid_quantum_read_forms(source,message):
    with pytest.raises(DiagnosticError,match=message):
        compile(source)


def test_zero_weight_outside_bounds_is_ignored_but_not_tiny_weights():
    c=compile('int[] a=[2];quint i=superposition([0,-1],probabilities:[1.0,0.0]);quint b=a[i];return measure(b);')
    assert distribution(c.program) == pytest.approx({'2':1})


def test_quantum_read_cleanup_and_reuse_generated_parity():
    source='quint i=superposition([0,1]);int[] values=[2,3];{quint temp=values[i];}quint selected=values[i];'
    c=compile(source)
    assert c.program.qubit_count == 6
    namespace={'__name__':'generated_test'}
    exec(python_source(c),namespace)
    np.testing.assert_allclose(Statevector.from_instruction(namespace['build']()[0]).data,Statevector.from_instruction(c.build()[0]).data,atol=1e-12)
    logical=compile(source,wire_reuse=False)
    state=Statevector.from_instruction(logical.build()[0]).data
    assert all(abs(a)<1e-12 for n,a in enumerate(state) if n>>3 & 7)


def test_operand_evaluation_is_left_to_right_and_once():
    c=compile('int[] values=[1,2];int count=0;quint index(){count+=1;values[0]=3;quint i=0;return i;}quint selected=values[index()];return [measure(selected),count,values[0]];')
    assert distribution(c.program) == pytest.approx({'[1, 1, 3]':1})


def test_support_intervals_never_exclude_possible_wrapped_values():
    width=10
    a=support.finite(range(-300,301))
    assert a.values is None
    for lo,hi in ((-20,30),(400,500),(-510,-490)):
        b=support.Support(lo,hi)
        for op in ('+','-'):
            result=support.arithmetic(a,b,op,width)
            for x in range(a.lower,a.upper+1):
                for y in range(lo,hi+1):
                    value=support.wrap(x+y if op=='+' else x-y,width)
                    assert result.lower <= value <= result.upper
    assert support.negate(support.finite((-512,)),width).values == (-512,)


def test_singleton_intervals_and_rotations_prove_valid_reads():
    c=compile('quint i=1;i=rotateLeft(i,1);i-=1;quint j=-(-i);int[] a=[2,3];quint x=a[j];return measure(x);')
    assert distribution(c.program) == pytest.approx({'3':1})
