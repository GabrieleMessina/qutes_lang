import pytest

from qutes.compiler import compile_source
from qutes.config import CompilerConfig
from qutes.diagnostics import DiagnosticError
from tests.test_lowering import distribution


def classical(source):
    return compile_source(source).program.result.decode(0)


def quantum(source):
    return compile_source(source, config=CompilerConfig(quint_bits=3)).program


def test_classical_aliases_copy_rebind_and_returned_slice():
    assert classical('int[] a=[1,2]; int[] b=a; b[0]=3; return a;') == [3,2]
    assert classical('int[] a=[1,2]; int[] b=copy(a); b[0]=3; return a;') == [1,2]
    assert classical('int[] a=[1,2]; int[] b=a; a=[9]; return b;') == [1,2]
    assert classical('int[] f(){int[] a=[1,2,3]; return a[1..3];} int[] a=f(); a[0]=9; return a;') == [9,3]


def test_quantum_aliases_and_explicit_copy():
    source='quint[] a=[1,2]; quint[] b=a; b[0]+=1; return measure(a);'
    p=quantum(source)
    assert distribution(p) == pytest.approx({'[2, 2]':1})
    assert p.qubit_count == 6
    assert distribution(quantum(source.replace('b=a;', 'b=copy(a);'))) == pytest.approx({'[1, 2]':1})


def test_mutable_scalars_nested_calls_and_reference_rebinding():
    assert classical('void f(mut int x){x+=1;} void g(mut int x){f(x);} int n=1; g(n); return n;') == 2
    assert classical('void f(mut int[] a){a=[7,8];} int[] a=[1]; int[] b=a; f(a); return [a.Length,b[0]];') == [2,1]
    p=quantum('void f(mut quint q){q+=1;} quint q=1; f(q); return measure(q);')
    assert distribution(p) == pytest.approx({'2':1})


def test_mutable_slices_disjoint_arguments_and_backing_lifetime():
    assert classical('void f(mut int[] a){a[0]=9;} int[] a=[1,2,3]; f(a[1..3]); return a;') == [1,9,3]
    assert classical('void f(mut int a,mut int b){a+=1;b+=2;} int[] a=[0,0];f(a[0],a[1]);return a;') == [1,2]
    p=quantum('quint[] f(){quint[] a=[1,2];return a[1..2];} quint[] b=f();b[0]+=1;return measure(b);')
    assert distribution(p) == pytest.approx({'[3]':1})
    assert p.qubit_count == 6


@pytest.mark.parametrize('source', [
    'void f(mut int a,mut int b){} int n=1;f(n,n);',
    'void f(mut int[] a,int[] b){} int[] a=[1];f(a,a);',
    'void f(mut int[] a){a=[1];} int[] a=[2];f(a[0..1]);',
    'readonly int[] a=[1];int[] b=a;b[0]=2;',
    'readonly int n=1;void f(mut int n){}f(n);',
    'qubit[] a=[false,false];qubit[] b=a;if(a[0]){b[0]=!b[0];}',
    'quint[] a=[1,2];void f(quint p){a[1]+=1;}f(a[1]);',
    'int[] a=[1,2];int[] b=a[0..3];',
    'int[] a=3..1;',
])
def test_reference_safety(source):
    with pytest.raises(DiagnosticError):
        compile_source(source)


def test_ranges_and_readonly_text_slices():
    assert classical('int n=0;foreach(int i in 1..4){n+=i;}return n;') == 6
    assert classical('char[] text="ABC"[1..3];return text;') == ['B','C']
    with pytest.raises(DiagnosticError, match='readonly'):
        classical('char[] text="ABC"[1..3];text[0]=\'A\';')


def test_mutable_index_is_evaluated_once_and_nested_rebind_is_rejected():
    assert classical('int calls=0; int index(){calls+=1;return 0;} void set(mut int x){x=3;} int[] a=[0];set(a[index()]);return [calls,a[0]];') == [1,3]
    with pytest.raises(DiagnosticError, match='rebinds'):
        classical('void g(mut int[] a){a=[3];} void f(mut int[] a){g(a);} int[] a=[1,2];f(a[0..1]);')


def test_slice_retention_is_reported_and_readonly_return_cannot_escalate():
    c=compile_source('quint[] f(){quint[] a=[1,2];return a[1..2];} quint[] b=f();', config=CompilerConfig(quint_bits=3))
    assert c.metadata['resources']['retained_array_qubits'] == 3
    with pytest.raises(DiagnosticError, match='readonly'):
        classical('int[] f(int[] a){return a;}int[] a=[1];int[] b=f(a);b[0]=2;')
