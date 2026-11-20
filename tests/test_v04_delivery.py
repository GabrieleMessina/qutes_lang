from dataclasses import replace
import io

import numpy as np
import pytest
from qiskit.quantum_info import Statevector

from qutes.compiler import compile_source
from qutes.config import CompilerConfig
from qutes.codegen import python_source
from qutes.visualization import render


@pytest.mark.parametrize('schema', [3,4])
def test_old_artifact_cached_array_copies_execute_but_changed_inputs_require_rebuild(schema, monkeypatch):
    original='input int start;quint[] a=[start];quint[] b=a;b[0]+=1;return measure(a);'
    equivalent=original.replace('b=a;', 'b=copy(a);')
    c=compile_source(equivalent,inputs={'start':1},config=CompilerConfig(quint_bits=3))
    metadata={**c.metadata,'artifact_schema':schema,'language_version':'0.3','compiler_version':'0.3.0.dev0'}
    source=python_source(replace(c,source=original,metadata=metadata)).replace('qutes.artifact_v5',f'qutes.artifact_v{schema}')
    import qutes.compiler
    monkeypatch.setattr(qutes.compiler,'compile_source',lambda *a,**k:pytest.fail('must not reinterpret old array semantics'))
    namespace={'__name__':'legacy_generated'}
    exec(source,namespace)
    assert namespace['run'](shots=2)['outcomes'][0]['value'] == [1]
    assert namespace['run']({'start':1},shots=2)['outcomes'][0]['value'] == [1]
    for name in ('build','run'):
        with pytest.raises(ValueError,match='Review array copies and rebuild'):
            namespace[name]({'start':2})


@pytest.mark.parametrize('unfold', [0,1,'all'])
def test_phase_preparation_and_index_diagrams_do_not_change_execution(tmp_path,unfold):
    c=compile_source('quint i=superposition([0,1],amplitudes:[complex(0.6,0),complex(0,0.8)]);bool[] values=[false,true];qubit q=values[i];phase(q,pi/3.0);',config=CompilerConfig(quint_bits=2))
    before=Statevector.from_instruction(c.build()[0]).data
    operations=c.program.operations
    render(c,print_circuit=True,stream=io.StringIO(),directory=tmp_path,image_format='svg',unfold=unfold)
    assert list(tmp_path.glob('*.svg'))
    assert c.program.operations == operations
    np.testing.assert_allclose(Statevector.from_instruction(c.build()[0]).data,before,atol=1e-12)


def test_schema5_numeric_inputs_generated_alias_semantics():
    c=compile_source('input float angle;input complex[] weights;qubit q=superposition([false,true],amplitudes:weights);phase(q,angle);',inputs={'angle':0,'weights':[1,0]})
    namespace={'__name__':'generated_test'}
    exec(python_source(c),namespace)
    circuit,layout=namespace['build']({'angle':np.pi/2,'weights':[.6,.8j]})
    np.testing.assert_allclose(Statevector.from_instruction(circuit).data,[.6,-.8],atol=1e-12)
    assert layout.metadata['artifact_schema'] == 5
    assert layout.metadata['language_version'] == '0.4'
