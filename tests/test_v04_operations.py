import math

import numpy as np
import pytest
from qiskit.quantum_info import Operator, Statevector

from qutes.compiler import compile_source
from qutes.config import CompilerConfig
from qutes.diagnostics import DiagnosticError
from tests.test_lowering import distribution


def compile(source, **settings):
    return compile_source(source, config=CompilerConfig(wire_reuse=False, **settings))


def test_bell_helper_has_two_wires_and_preserves_phase():
    source='void entangle(mut qubit a,mut qubit b){hadamard(a);if(a){not(b);}} qubit a=false;qubit b=false;entangle(a,b);'
    c=compile(source)
    assert c.program.qubit_count == 2
    np.testing.assert_allclose(Statevector.from_instruction(c.build()[0]).data, [2**-.5,0,0,2**-.5], atol=1e-12)
    phased=compile(source+'phaseFlip(b);')
    np.testing.assert_allclose(Statevector.from_instruction(phased.build()[0]).data, [2**-.5,0,0,-2**-.5], atol=1e-12)


def test_inverse_phase_and_swap_full_operators():
    c=compile('qubit a=false;qubit b=false;hadamard(a);if(a){phase(b,pi/3.0);}swap(a,b);swap(a,b);if(a){phase(b,-pi/3.0);}hadamard(a);')
    np.testing.assert_allclose(Operator(c.build()[0]).data, np.eye(4), atol=1e-12)


@pytest.mark.parametrize('angle', [0.0, math.pi/2, -.713, math.pi])
def test_teleportation_with_explicit_measurement_and_corrections(angle):
    source=f'''
        qubit message=false;hadamard(message);phase(message,{angle});
        qubit alice=false;qubit bob=false;
        hadamard(alice);if(alice){{not(bob);}}
        if(message){{not(alice);}}hadamard(message);
        bool first=measure(message);bool second=measure(alice);
        if(second){{not(bob);}}if(first){{phaseFlip(bob);}}
        phase(bob,{-angle});hadamard(bob);
        return measure(bob);
    '''
    assert distribution(compile(source).program) == pytest.approx({'false':1.0})


@pytest.mark.parametrize('x_basis', [False, True])
def test_teleportation_preserves_external_entanglement(x_basis):
    source='''
        qubit reference=false;qubit message=false;
        hadamard(reference);if(reference){not(message);}
        qubit alice=false;qubit bob=false;
        hadamard(alice);if(alice){not(bob);}
        if(message){not(alice);}hadamard(message);
        bool first=measure(message);bool second=measure(alice);
        if(second){not(bob);}if(first){phaseFlip(bob);}
    '''
    if x_basis:
        source+='hadamard(reference);hadamard(bob);'
    source+='return [measure(reference),measure(bob)];'
    assert distribution(compile(source).program) == pytest.approx({'[false, false]':.5,'[true, true]':.5})


def test_qft_against_independent_fourier_matrix():
    source='''
        void qft(mut qubit[] bits){
            for(int k=bits.Length-1;k>=0;k--){
                hadamard(bits[k]);float angle=pi/2.0;
                for(int j=k-1;j>=0;j--){
                    if(bits[j]){phase(bits[k],angle);}
                    angle=angle/2.0;
                }
            }
            for(int i=0;i<bits.Length/2;i++){swap(bits[i],bits[bits.Length-1-i]);}
        }
        qubit[] bits=new qubit[3];qft(bits);
    '''
    actual=Operator(compile(source).build()[0]).data
    indices=np.arange(8)
    expected=np.exp(2j*np.pi*np.outer(indices,indices)/8)/np.sqrt(8)
    np.testing.assert_allclose(actual,expected,atol=1e-12)


def test_closed_joint_state_cleanup_and_certificates():
    c=compile('{qubit a=false;qubit b=false;hadamard(a);if(a){not(b);}hadamard(a);swap(a,b);}')
    np.testing.assert_allclose(Statevector.from_instruction(c.build()[0]).data, [1,0,0,0], atol=1e-12)
    assert all(a.released for a in c.program.allocations)
    assert any(p.reason == 'joint-unitary-cleanup' for p in c.program.zero_certificates)


def test_returned_bell_array_transfers_joint_ownership_and_slice_updates():
    source='qubit[] bell(){qubit[] b=new qubit[2];hadamard(b[0]);if(b[0]){not(b[1]);}return b;} qubit[] bits=bell();qubit[] part=bits[1..2];phaseFlip(part[0]);'
    c=compile(source)
    np.testing.assert_allclose(Statevector.from_instruction(c.build()[0]).data,[2**-.5,0,0,-2**-.5],atol=1e-12)


def test_partial_measurement_and_post_measurement_basis_evolution():
    c=compile('qubit[] b=new qubit[2];hadamard(b[0]);if(b[0]){not(b[1]);}bool before=measure(b[0]);not(b[0]);return [before,measure(b[0]),measure(b[1])];')
    assert distribution(c.program) == pytest.approx({'[false, true, false]':.5,'[true, false, true]':.5})


@pytest.mark.parametrize('source', [
    'qubit q=false;qubit r=hadamard(q);',
    'qubit q=false;swap(q,q);',
    'readonly qubit q=false;not(q);',
    'qubit q=false;qubit[] a=[q];if(a[0]){hadamard(a[0]);}',
    # Copying, changing basis, then copying again defeats independent replay.
    'qubit a=superposition();qubit result=false;{qubit b=a;hadamard(a);result=a;}',
    # Silently reversing this local phase would erase observable kickback.
    'qubit a=superposition();{qubit b=a;phaseFlip(b);}',
])
def test_live_operation_safety(source):
    with pytest.raises(DiagnosticError):
        compile(source)
