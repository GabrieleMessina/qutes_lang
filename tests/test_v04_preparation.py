import numpy as np
import pytest
from qiskit.quantum_info import Operator, Statevector

from qutes.compiler import compile_source
from qutes.config import CompilerConfig
from qutes.diagnostics import DiagnosticError
from qutes.codegen import python_source
from tests.test_lowering import distribution


def compile(source, width=3, **settings):
    return compile_source(source, config=CompilerConfig(quint_bits=width, wire_reuse=False, **settings))


@pytest.mark.parametrize('initializer,expected', [
    ('superposition([-3,2])', {5:2**-.5,2:2**-.5}),
    ('superposition([-3,2], probabilities: [0.36,0.64])', {5:.6,2:.8}),
    ('superposition([-3,2], amplitudes: [complex(0.6,0),complex(0,0.8)])', {5:.6,2:.8j}),
    ('superposition([0], amplitudes: [-1])', {0:-1}),
    ('superposition([1,2], probabilities: [0.0,1.0])', {2:1}),
])
def test_sparse_preparation_full_amplitudes_and_inverse(initializer, expected):
    c=compile('quint n='+initializer+';')
    circuit=c.build()[0]
    state=np.zeros(8,dtype=complex)
    for i,a in expected.items():
        state[i]=a
    assert circuit.num_qubits == 3
    np.testing.assert_allclose(Statevector.from_instruction(circuit).data,state,atol=1e-12)
    np.testing.assert_allclose(Operator(circuit.compose(circuit.inverse())).data,np.eye(8),atol=1e-12)
    assert all(op.operation.name not in {'reset','initialize','measure'} for op in circuit.data)


def test_complex_input_preparation_and_generated_respecialization():
    c=compile_source('input complex[] a;qubit q=superposition([false,true],amplitudes:a);',inputs={'a':[.6,.8j]})
    namespace={'__name__':'generated_test'}
    exec(python_source(c),namespace)
    circuit,_=namespace['build']({'a':[1j,0]})
    np.testing.assert_allclose(Statevector.from_instruction(circuit).data,[1j,0],atol=1e-12)


def test_known_preparation_scope_is_fully_cleaned():
    c=compile('{quint q=superposition([0,2],amplitudes:[complex(0.6,0),complex(0,0.8)]);q-=1;}')
    np.testing.assert_allclose(Statevector.from_instruction(c.build()[0]).data,[1,0,0,0,0,0,0,0],atol=1e-12)
    assert all(a.released for a in c.program.allocations)


@pytest.mark.parametrize('initializer', [
    'superposition([])', 'superposition([1,1])', 'superposition([4])',
    'superposition([1,2],probabilities:[0.4,0.4])',
    'superposition([1,2],probabilities:[-0.1,1.1])',
    'superposition([1,2],amplitudes:[0.1,0.1])',
    'superposition([1,2],probabilities:[1.0])',
    'superposition([1],probabilities:[1.0],amplitudes:[1.0])',
    'superposition([1],unknown:[1.0])',
])
def test_invalid_preparation(initializer):
    with pytest.raises(DiagnosticError):
        compile('quint n='+initializer+';')


@pytest.mark.parametrize('width',[1,2,3])
def test_signed_subtraction_exhaustive_small_widths(width):
    bound=1<<(width-1)
    modulus=2*bound
    wrap=lambda v:(v+bound)%modulus-bound
    for a in range(-bound,bound):
        for b in range(-bound,bound):
            source=f'quint a={a};quint b={b};quint difference=a-b;quint negative=-a;a-=b;return [measure(difference),measure(negative),measure(a)];'
            expected=f'[{wrap(a-b)}, {wrap(-a)}, {wrap(a-b)}]'
            assert distribution(compile(source,width).program) == pytest.approx({expected:1})


def test_reversible_self_negation_reverse_subtraction_and_overlap():
    source='quint a=superposition([-3,1]);quint b=2;a=b-a;a=-a;return measure(a);'
    assert distribution(compile(source).program) == pytest.approx({'3':.5,'-1':.5})
    assert distribution(compile('quint a=superposition();quint b=a-a;return measure(b);').program) == pytest.approx({'0':1})
    with pytest.raises(DiagnosticError,match='Q3001'):
        compile('quint a=superposition();a-=a;')


def test_arithmetic_preserves_complex_reference_correlations():
    c=compile('qubit r=superposition();quint a=superposition([0,1],amplitudes:[complex(0.6,0),complex(0,0.8)]);if(r){a+=1;}quint b=-a;',2)
    expected=np.zeros(32,dtype=complex)
    for reference in (0,1):
        for before,amplitude in ((0,.6),(1,.8j)):
            value=(before+reference)%4
            expected[reference | value<<1 | ((-value)%4)<<3]=amplitude/np.sqrt(2)
    np.testing.assert_allclose(Statevector.from_instruction(c.build()[0]).data,expected,atol=1e-12)


def test_conditional_preparation_preserves_existing_restrictions():
    source='void f(){qubit q=superposition([false,true]);}qubit a=superposition();bool flag=measure(a);if(flag){f();}return flag;'
    assert distribution(compile(source).program) == pytest.approx({'false':.5,'true':.5})
    with pytest.raises(DiagnosticError,match='quantum control'):
        compile('void f(){qubit q=superposition([false,true]);}qubit a=superposition();if(a){f();}')
