import pytest
from qutes.codegen import python_source
from qutes.compiler import compile_source
from qutes.serialization import json_text, load_json


def test_legacy_import_contract_fails_before_recompilation(monkeypatch):
    import qutes.compiler
    def forbidden(*args, **kwargs):
        pytest.fail('legacy source must never be recompiled under new entry semantics')
    monkeypatch.setattr(qutes.compiler, 'compile_source', forbidden)
    legacy = '''
from qutes.compiler import compile_source
from qutes.runtime import checked_build, execute, layout_from_metadata
SOURCE = "int main(int n) { return n; }"
def run(inputs):
    return compile_source(SOURCE, inputs=inputs).run()
run({"n": 2})
'''
    with pytest.raises(ImportError, match='Migrate.*rebuild'):
        exec(legacy, {})


@pytest.mark.parametrize('inputs', [None, {'count':2}])
@pytest.mark.parametrize('field,bad', [('artifact_schema',1), ('language_version','0.1')])
def test_artifact_guard_precedes_both_cached_and_new_binding_paths(inputs, field, bad):
    namespace = {'__name__':'generated_test'}
    compilation = compile_source('input int count; return count;', inputs={'count':1})
    exec(python_source(compilation), namespace)
    metadata = load_json(namespace['_METADATA_JSON'])
    metadata[field] = bad
    namespace['_METADATA_JSON'] = json_text(metadata)
    for command in ('build','run'):
        with pytest.raises(ValueError, match='rebuild'):
            namespace[command](inputs)


def test_generated_script_inputs_and_version_metadata():
    namespace = {'__name__':'generated_test'}
    compilation = compile_source('input int count; int n=0; void add(){n+=count;} add(); return n;', inputs={'count':1})
    exec(python_source(compilation), namespace)
    result = namespace['run']({'count':3}, shots=2)
    assert result['outcomes'][0]['value'] == 3
    assert result['build']['artifact_schema'] == 4
    assert result['build']['language_version'] == '0.3'
    assert result['build']['compiler_version'] == '0.3.0.dev0'


def test_v02_generated_import_is_rejected_before_compilation(monkeypatch):
    import qutes.compiler
    monkeypatch.setattr(qutes.compiler, 'compile_source', lambda *args, **kwargs: pytest.fail('must not recompile'))
    with pytest.raises(ImportError, match='rebuild'):
        exec('from qutes.artifact_v2 import checked_build, execute, layout_from_metadata, validate_metadata', {})
