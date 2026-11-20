import json
from pathlib import Path

import pytest

from qutes import ir
from qutes.checker import analyze
from qutes.config import CompilerConfig
from qutes.diagnostics import DiagnosticError
from qutes.parser import parse


ROOT = Path(__file__).parent / "acceptance"
CASES = json.loads((ROOT / "cases.json").read_text(encoding="utf-8"))["cases"]


def check(source, **settings):
    return analyze(parse(source, "test.qut"), CompilerConfig.resolve(settings))


def rejects(source, code, **settings):
    with pytest.raises(DiagnosticError) as error:
        check(source, **settings)
    assert error.value.code == code, str(error.value)
    assert error.value.span.path == "test.qut"
    return error.value


@pytest.mark.parametrize("case", CASES, ids=lambda case: case["id"])
def test_acceptance_frontend_semantics(case):
    source = (ROOT / case["file"]).read_text(encoding="utf-8")
    if case["expect"] == "reject" and case["stage"] != "cleanup":
        rejects(source, case["code"], **case.get("config", {}))
    else:
        result = check(source, **case.get("config", {}))
        assert result.cleanup_verified is False
        assert result.validated == ("names", "types", "stages", "effects")


@pytest.mark.parametrize("source", [
    'quint q=1; return q;', 'int f() {}',
    'void f() { return 1; }', 'int f() { return; }',
    'return 1; return true;', 'return 1; return;',
    'input bool b;  if (b) { return 1; } ',
    ' qubit q=superposition(); if(q) { return 1; } return 0; ',
])
def test_entry_and_return_contract(source):
    rejects(source, "Q2005")


@pytest.mark.parametrize("source", [
    ' return missing; ', ' return missing(); ',
    "int main() { return 0; } int main() { return 1; }",
    'int measure() { return 0; }  return 0; ',
    ' int measure = 1; return measure; ',
    ' int a=1; int a=2; return a; ',
    'int f(int x, int x) { return x; }  return 0; ',
    'int f() { return g(); } int g() { return f(); }  return 0; ',
    'int main() { return main(); }',
])
def test_names_and_recursion(source):
    rejects(source, "Q2002")


@pytest.mark.parametrize("source", [
    ' void x=0; ', 'void[] f() {}',
    ' bool flag = 1; return 0; ',
    ' if (1) {} return 0; ',
    ' quint q=1; q *= 2; return 0; ',  # grammar does not include *=
])
def test_invalid_types_and_numeric_truthiness(source):
    rejects(source, "Q1002" if "*=" in source else "Q2001")


def test_quantum_operator_restrictions_and_range():
    for expression in ["q * 2", "q / 2", "!q", "q < 128"]:
        rejects(f" quint q=1; quint other={expression}; return 0; ", "Q2001")
    rejects(' quint q=1; q++; return 0; ', "Q2001")
    check(' quint q=-128; q=q+(-1); return measure(q); ', quint_bits=8)


def test_readonly_and_lexical_scopes():
    rejects('int f(int[] a) { a[0]=2; return 0; }  return 0; ', "Q2004")
    rejects(' int[] a=[1]; foreach(int x in a) { x++; } return 0; ', "Q2004")
    check(' int a=1; { int a=2; } return a; ')
    rejects(' { int a=2; } return a; ', "Q2002")
    # Concrete element overlap is checked while expanding the loop.
    from qutes.construction import construct
    with pytest.raises(DiagnosticError, match='Q2004'):
        construct(check('qubit[] bits=[true,false]; foreach(qubit bit in bits) { if(bit) { bits[0]=false; } } return 0;'))


def test_measurement_does_not_consume_and_preserves_stages():
    result = check(' quint q=1; int before=measure(q); q+=1; int after=measure(q); return [before,after]; ')
    main = next(function for function in result.functions if function.key == result.entry)
    statements = main.body.statements
    assert statements[0].expressions[0].stage == ir.Stage.QUANTUM
    assert statements[1].expressions[0].stage == ir.Stage.RUNTIME
    assert statements[2].expressions[1].stage == ir.Stage.QUANTUM
    assert main.return_stage == ir.Stage.RUNTIME
    assert statements[1].symbol.id != statements[3].symbol.id
    assert "measure" in main.effects


def test_helper_specializes_for_runtime_predicates_but_not_arithmetic():
    source = 'bool negative(int n) { return n<0; }  quint q=1; int n=measure(q); if(negative(n)) { q+=1; } return measure(q); '
    result = check(source)
    predicates = [f for f in result.functions if f.name == "negative"]
    assert {f.return_stage for f in predicates} == {ir.Stage.RUNTIME}
    rejects('int plus(int n) { return n+1; }  quint q=1; int n=measure(q); return plus(n); ', "Q2003")


def test_prepare_effect_propagates_through_helpers():
    rejects('qubit prepare() { qubit q=superposition(); return q; }  qubit c=superposition(); if(c) { qubit x=prepare(); } return 0; ', "Q2004")
    rejects(' quint q=1; q=superposition(); return 0; ', "Q2001")


def test_dynamic_branch_effects_and_shape_joins():
    rejects(' qubit q=superposition(); int i=0; if(q) { i=1; } return i; ', "Q2004")
    rejects(' qubit q=superposition(); qustring s="A"; if(q) { s="AB"; } return measure(s); ', "Q2004")
    check(' qubit q=superposition(); qustring s="A"; if(q) { s="AB"; } else { s="CD"; } return measure(s); ', alphabet="ABCD")
    check(' qubit q=superposition(); quint total=0; if(q) { for(int i=0; i<3; i++) { total+=i; } } return measure(total); ')


def test_predicate_dependencies_and_loop_stage_changes():
    rejects(' quint a=1; quint b=2; if(a<b) { b+=1; } return 0; ', "Q2004")
    rejects(' quint q=1; int i=0; while(i<3) { i=measure(q); } return i; ', "Q2003")
    rejects(' quint q=1; int n=measure(q); quint[] a=new quint[n]; return 0; ', "Q2003")
    rejects(' quint q=1; int n=measure(q); q=rotateLeft(q,n); return 0; ', "Q2003")


def test_arrays_strings_and_empty_context():
    check(' int[] a=[]; return a; ')
    rejects(' int[] a=[1,true]; return 0; ', "Q2001")
    check(' int[] a=[1]; a=[1,2]; return 0; ')
    rejects(' int[] a=[1]; return a[1]; ', "Q4001")
    rejects(' int[] a=new int[-1]; return 0; ', "Q4001")
    rejects(' int x=1; return x.Length; ', "Q2001")
    rejects(' int[] a=[1]; a.Length=3; return 0; ', "Q2001")


def test_classical_short_circuit_is_not_eager_constant_evaluation():
    result = check(' return false && (1/0 == 0); ')
    assert result.functions[0].body.statements[0].expressions[0].value is False
    check(' return true || (1/0 == 0); ')
    rejects(' return 1/0; ', "Q4001")
    rejects(' return false && 1; ', "Q2001")


def test_classical_signed_division_and_remainder():
    result = check(' return [-7/3, -7%3, 7/-3, 7%-3]; ')
    values = result.functions[0].body.statements[0].expressions[0]
    assert values.value == (-2, -1, -2, 1)


def test_loop_constants_do_not_escape_as_first_iteration_values():
    result = check(' int i=0; while(i<3) { i++; } return i; ')
    value = result.functions[0].body.statements[-1].expressions[0]
    assert value.stage == ir.Stage.STATIC
    assert not value.known


def test_step_budget_is_diagnostic():
    rejects(' int x=1; return x; ', "Q4001", max_evaluation_steps=1)


def test_ir_serialization_is_deterministic_and_explicit():
    source = ' quint q=1; return measure(q); '
    first, second = ir.to_dict(check(source)), ir.to_dict(check(source))
    assert first == second
    assert json.loads(json.dumps(first))["cleanup_verified"] is False
