import pytest
from qutes.diagnostics import DiagnosticError
from qutes.parser import parse


def test_multiple_errors_have_actionable_hints_and_excerpts():
    source = 'void main() {\n int a = 1\n int b = 2\n return;\n}'
    with pytest.raises(DiagnosticError) as failure:
        parse(source, 'bad.qut')
    errors = failure.value.diagnostics
    assert len(errors) == 2
    assert all("';'" in error.message and error.help for error in errors)
    assert 'bad.qut:3:2' in failure.value.render()
    assert '^' in failure.value.render()
    assert errors[0].to_dict()['help']


def test_unclosed_delimiter_references_opening_location():
    with pytest.raises(DiagnosticError) as failure:
        parse('void main() { return;')
    assert failure.value.diagnostics[-1].related


def test_error_collection_is_bounded():
    with pytest.raises(DiagnosticError) as failure:
        parse('void main() {' + 'int a = 1\n' * 50 + '}')
    assert len(failure.value.diagnostics) == 10


def test_lexical_errors_are_collected_without_accepting_a_repaired_program():
    with pytest.raises(DiagnosticError) as failure:
        parse('void main() { @ # $ }')
    assert len(failure.value.diagnostics) == 3
    assert all(item.code == 'Q1001' for item in failure.value.diagnostics)
