import math

import pytest

from qutes.compiler import compile_source
from qutes.diagnostics import DiagnosticError
from qutes.parser import parse
from qutes.serialization import json_text, load_json
from qutes.runtime import result_from_data
from qutes.ir import to_dict


def result(source, inputs=None):
    return compile_source(source, inputs=inputs).program.result.decode(0)


def test_float_complex_arithmetic_and_generated_layout():
    c = compile_source('complex a=complex(0.6,0.8); float n=2; return a*a/n;')
    assert c.program.result.decode(0) == pytest.approx(complex(-0.14, 0.48))
    layout = result_from_data(load_json(json_text(to_dict(c.program.result))))
    assert layout.decode(0) == c.program.result.decode(0)
    assert result('return pi / 2.0;') == math.pi / 2
    assert result('return -7 / 3;') == -2
    assert result('return -7.0 / 2;') == -3.5


def test_numeric_inputs_arrays_and_functions():
    source = 'input complex z; complex scale(complex a, float x){return a*x;} return scale(z,2);'
    assert result(source, {'z': {'real': 1, 'imag': 2}}) == 2+4j
    assert result(source, {'z': 1+2j}) == 2+4j
    assert result('float[] a=[1,2.5]; return a;') == [1.0,2.5]
    assert result('complex[] a=new complex[2]; return a;') == [0j,0j]


@pytest.mark.parametrize('source', [
    'return 1e309;', 'return 1e308*1e308;', 'return 1.0/1e-320;', 'return complex(1,2)/complex(0,0);',
    'int n=1.5;', 'quint q=1.0;', 'return complex(1,2)<complex(2,3);',
    'readonly int n=1; n=2;', 'void f(){readonly int n=1;n++;} f();',
    'qubit accepts(quint n){return n==1;} float[] a=[1.0];quint n=search(a,accepts);',
])
def test_invalid_numeric_and_readonly_programs(source):
    with pytest.raises(DiagnosticError):
        compile_source(source)


def test_indexed_foreach_and_range_lexing():
    assert result('int sum=0; foreach(int n,int i in [4,5,6]){sum+=n*i;} return sum;') == 17
    tree = parse('foreach(int i in 1..3){} float n=1.2e-3;')
    assert tree.statements[0].collection.operator == '..'
    assert tree.statements[1].initializer.value == .0012
    with pytest.raises(DiagnosticError, match='index binding'):
        parse('foreach(int n, float i in [1]){}')
