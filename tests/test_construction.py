import json
from pathlib import Path

import pytest

from qutes import ir
from qutes.checker import analyze
from qutes.config import CompilerConfig
from qutes.construction import construct
from qutes.diagnostics import DiagnosticError
from qutes.parser import parse


def build(source, inputs=None, **settings):
    return construct(analyze(parse(source, "build.qut"), CompilerConfig.resolve(settings)), inputs)


def statements(block):
    for statement in block.statements:
        yield statement
        for nested in statement.blocks:
            yield from statements(nested)


ROOT = Path(__file__).parent / "acceptance"
POSITIVE = [case for case in json.loads((ROOT / "cases.json").read_text())["cases"] if case["expect"] == "accept"]


@pytest.mark.parametrize("case", POSITIVE, ids=lambda case: case["id"])
def test_positive_corpus_constructs_symbolically(case):
    result = build((ROOT / case["file"]).read_text(), **case.get("config", {}))
    assert result.cleanup_verified is False
    assert result.result is not None
    assert result.result.stage in {ir.Stage.STATIC, ir.Stage.RUNTIME}
    assert not any(statement.op in {"while", "for", "foreach"} for statement in statements(result.body))


def test_classical_functions_loops_and_arrays_execute():
    source = """int sum(int[] values) {
        int total=0;
        foreach(int item in values) { total+=item; }
        return total;
    }
    input int count;
        int[] values = new int[count];
        for(int i=0; i<values.Length; i++) { values[i]=i+1; }
        return sum(values);
    """
    result = build(source, {"count": 4})
    assert result.result.value == 10
    assert result.loop_iterations == 8
    assert not any(statement.op in {"let", "assign", "if"} for statement in statements(result.body))


def test_classical_while_and_early_function_return():
    result = build("""int find(int n) {
        int i=0;
        while(i<n) { if(i==3) { return i; } i++; }
        return -1;
    }
     return find(10); """)
    assert result.result.value == 3
    assert result.loop_iterations == 4


def test_classical_copy_value_semantics():
    result = build(' int[] a=[1,2]; int[] b=copy(a); b[0]=3; return [a[0],b[0]]; ')
    assert result.result.value == (1, 3)


def test_snapshots_and_post_measurement_update_stay_symbolic():
    result = build(' quint q=5; int before=measure(q); q=q+2; int after=measure(q); return [before,after]; ')
    operations = list(statements(result.body))
    measurements = [s for s in operations if s.op == "let" and s.expressions[0].op == "measure"]
    assert len(measurements) == 2
    assert measurements[0].symbol.id != measurements[1].symbol.id
    assert measurements[0].expressions[0].arguments[0].symbol == measurements[1].expressions[0].arguments[0].symbol
    assert result.result.stage == ir.Stage.RUNTIME
    assert not result.result.known
    assert [s.op for s in operations if s.op not in {"bind", "roots"}] == ["let", "let", "assign", "let"]


def test_quantum_loop_body_references_fresh_local_storage_each_iteration():
    result = build(' for(int i=0; i<3; i++) { quint q=i; int sample=measure(q); } return 0; ')
    declarations = [s for s in statements(result.body) if s.op == "let"]
    assert len(declarations) == 6
    assert len({s.symbol.id for s in declarations}) == 6


def test_helper_calls_inline_and_move_owned_outputs():
    result = build('quint plus(quint q, int n) { return q+n; }  quint q=1; quint a=plus(q,1); quint b=plus(q,2); return measure(b); ')
    scopes = [s for s in statements(result.body) if s.op == "scope" and s.operator == "function"]
    assert len(scopes) == 2
    assert all(scope.expressions[0].op == "move" for scope in scopes)
    assert scopes[0].expressions[0].symbol.id != scopes[1].expressions[0].symbol.id


def test_static_branch_selects_one_body_dynamic_branch_is_preserved():
    result = build('input bool enabled;  quint q=1; if(enabled) { q+=2; } else { q+=3; } return measure(q); ', {"enabled": True})
    assert not any(s.op == "if" for s in statements(result.body))
    result = build(' qubit c=superposition(); quint q=1; bool selected=measure(c); if(selected) { q+=2; } return measure(q); ')
    branches = [s for s in statements(result.body) if s.op == "if"]
    assert len(branches) == 1 and branches[0].expressions[0].stage == ir.Stage.RUNTIME


@pytest.mark.parametrize("source,inputs,code", [
    ('input int n;  return n; ', {}, "Q2001"),
    ('input int n;  return n; ', {"n": True}, "Q2001"),
    ('input char c;  return c; ', {"c": "ab"}, "Q2001"),
    ('input int n;  quint q=n; return measure(q); ', {"n": 128}, "Q2001"),
    ('input int n;  int[] a=new int[n]; return 0; ', {"n": -1}, "Q4001"),
    ('input int i;  int[] a=[1]; return a[i]; ', {"i": 1}, "Q4001"),
    ('input int n;  return 10/n; ', {"n": 0}, "Q4001"),
    ('input string s;  qustring q=s; return measure(q); ', {"s": "long"}, "Q2001"),
])
def test_deferred_input_range_and_bound_checks(source, inputs, code):
    with pytest.raises(DiagnosticError) as error:
        build(source, inputs)
    assert error.value.code == code


def test_global_loop_and_evaluation_budgets():
    with pytest.raises(DiagnosticError, match="loop expansion"):
        build(' while(true) {} ', max_loop_iterations=5)
    with pytest.raises(DiagnosticError, match="loop expansion"):
        build(' for(int i=0;i<3;i++) { for(int j=0;j<3;j++) {} } ', max_loop_iterations=7)
    with pytest.raises(DiagnosticError, match="step budget"):
        build('input int n;  int[] a=new int[n]; ', {"n": 1000}, max_evaluation_steps=100)


def test_short_circuit_with_runtime_inputs_to_classical_helper():
    result = build('input int denominator;  return false && (1/denominator==0); ', {"denominator": 0})
    assert result.result.value is False


def test_dynamic_shape_validation_after_argument_resolution():
    source = 'input string a; input string b;  qubit c=superposition(); qustring result=a; if(c) { result=b; } return measure(result); '
    with pytest.raises(DiagnosticError) as error:
        build(source, {"a": "A", "b": "AB"})
    assert error.value.code == "Q2004"


def test_construction_serializes_deterministically():
    source = ' quint q=1; return measure(q); '
    assert ir.to_dict(build(source)) == ir.to_dict(build(source))


def test_index_helper_is_evaluated_once_for_compound_assignment():
    result = build('int index() { qubit scratch=superposition(); return 0; }  int[] values=[1]; values[index()]+=2; return values[0]; ')
    functions = [s for s in statements(result.body) if s.op == "scope" and s.operator == "function"]
    assert len(functions) == 1
    assert result.result.value == 3


def test_runtime_array_element_replacement_preserves_other_snapshots():
    result = build(' quint a=1; quint b=2; int[] samples=[measure(a),measure(b)]; samples[0]=3; return samples; ')
    assert result.result.op == "array"
    assert result.result.arguments[0].value == 3
    assert result.result.arguments[1].stage == ir.Stage.RUNTIME


def test_returned_quantum_local_escapes_nested_scope():
    result = build('quint prepare() { { quint q=superposition(); return q; } }  quint q=prepare(); return measure(q); ')
    function = next(s for s in statements(result.body) if s.op == "scope" and s.operator == "function")
    assert function.expressions[0].op == "move"
    assert function.blocks[0].statements[0].expressions[0].type == ir.Type("quint")


def test_integer_memory_limit_is_configurable_and_not_wrapping():
    with pytest.raises(DiagnosticError, match="memory limit"):
        build('input int n;  return n*n; ', {"n": 200}, max_classical_bits=8)
    result = build('input int n;  return n*n; ', {"n": 200}, max_classical_bits=16)
    assert result.result.value == 40_000


def test_input_mapping_required():
    with pytest.raises(DiagnosticError, match="mapping"):
        build(' return 0; ', [])


def test_quantum_foreach_temporary_is_materialized_once():
    result = build(' quint total=0; foreach(quint item in [total,total]) { total+=1; } return measure(total); ')
    temporary = [s for s in statements(result.body) if s.op == "let" and s.symbol.name == "$iteration_source"]
    assert len(temporary) == 1
