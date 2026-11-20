import json
import numpy as np
import pytest
from qiskit.quantum_info import Statevector
from qutes.cli import main
from qutes.codegen import python_source
from qutes.compiler import compile_source
from qutes.config import CompilerConfig


SOURCE = 'input bool[] values; qubit good(qubit value){return value;} qubit result=search(values,good); return measure(result);'


def test_generated_search_respecializes_and_emits_identical_phases():
    c = compile_source(SOURCE, inputs={'values':[False,True]})
    namespace = {'__name__':'generated_search'}
    exec(python_source(c), namespace)
    qc, layout = namespace['build']()
    original = c.program.to_qiskit().remove_final_measurements(inplace=False)
    emitted = qc.remove_final_measurements(inplace=False)
    np.testing.assert_allclose(Statevector.from_instruction(original).data,
                               Statevector.from_instruction(emitted).data, atol=1e-10)
    result = namespace['run']({'values':[True,False,True]}, shots=64, seed=17)
    assert result['build']['searches'][0]['entries'] == 3
    assert sum(item['count'] for item in result['outcomes'] if item['value']) >= 59
    assert layout.metadata['artifact_schema'] == 5


def test_cli_configuration_reports_and_circuit_images(tmp_path, capsys):
    source = tmp_path/'search.qut'
    source.write_text('qubit good(qubit x){return x;} qubit result=search([false,true],good); return measure(result);')
    assert main(['check',str(source),'--search-failure-probability','.05','--json','--print-circuit',
                 '--save-circuit',str(tmp_path/'images'),'--circuit-format','svg']) == 0
    captured = capsys.readouterr()
    result = json.loads(captured.out)
    assert result['metadata']['config']['search_failure_probability'] == .05
    assert result['metadata']['searches'][0]['failure_probability'] == .05
    assert captured.err
    assert list((tmp_path/'images').glob('*.svg'))
    assert main(['explain',str(source)]) == 0
    assert 'oracle calls' in capsys.readouterr().out
    assert main(['check',str(source),'--search-failure-probability','0','--json']) == 1
    assert 'search_failure_probability' in capsys.readouterr().out


def test_search_compilation_is_backend_independent(monkeypatch):
    import builtins
    original = builtins.__import__
    def guarded(name,*args,**kwargs):
        if name.startswith(('qiskit','numpy')):
            raise AssertionError('backend import during compilation')
        return original(name,*args,**kwargs)
    monkeypatch.setattr(builtins,'__import__',guarded)
    c = compile_source(SOURCE, inputs={'values':[True,False]})
    assert 'PhaseGate' in python_source(c)


def test_failure_target_changes_build_identity_and_resources():
    a = compile_source(SOURCE, inputs={'values':[True,False,False]})
    b = compile_source(SOURCE, inputs={'values':[True,False,False]}, config=CompilerConfig(search_failure_probability=.001))
    assert a.metadata['build_sha256'] != b.metadata['build_sha256']
    assert a.metadata['searches'][0]['oracle_calls'] < b.metadata['searches'][0]['oracle_calls']
