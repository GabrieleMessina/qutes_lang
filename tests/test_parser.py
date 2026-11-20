import json
from pathlib import Path

import pytest

from qutes import syntax as ast
from qutes.diagnostics import DiagnosticError
from qutes.lexer import lex
from qutes.parser import parse


CORPUS = Path(__file__).parent / "acceptance"
CASES = json.loads((CORPUS / "cases.json").read_text(encoding="utf-8"))["cases"]


@pytest.mark.parametrize("case", CASES, ids=lambda case: case["id"])
def test_corpus_syntax_only(case):
    path = CORPUS / case["file"]
    source = path.read_text(encoding="utf-8")
    if case.get("stage") in {"lex", "parse"}:
        with pytest.raises(DiagnosticError) as failure:
            parse(source, str(path))
        assert failure.value.code == case["code"]
    else:
        # This intentionally includes semantic-negative cases: syntax is independent.
        assert isinstance(parse(source, str(path)), ast.Program)


def expression(source):
    return parse(f"int main() {{ return {source}; }}").functions[0].body.statements[0].value


def test_precedence_and_associativity():
    tree = expression("1 + 2 * 3 - 4")
    assert isinstance(tree, ast.Binary) and tree.operator == "-"
    assert tree.left.operator == "+" and tree.left.right.operator == "*"
    tree = expression("10 - 4 - 2")
    assert tree.operator == "-" and tree.left.operator == "-"
    tree = expression("a < b && c == d || !e")
    assert tree.operator == "||" and tree.left.operator == "&&"
    assert tree.left.left.operator == "<" and tree.left.right.operator == "=="
    assert isinstance(tree.right, ast.Unary) and tree.right.operator == "!"
    tree = expression("-(1 + 2) * 3")
    assert tree.operator == "*"
    assert isinstance(tree.left.operand, ast.Group)


def test_calls_indexing_length_and_array_shapes():
    tree = expression("calculate(values[1], values.Length)")
    assert tree.callee.identifier == "calculate"
    assert isinstance(tree.arguments[0], ast.Index)
    assert tree.arguments[1].name == "Length"
    assert expression("new quint[3]").element_type.name == "quint"
    assert expression("[]").elements == ()
    assert len(expression("[1, 2, 3]").elements) == 3


def test_loops_returns_and_else_if():
    tree = parse("""void main() {
        for (;;) { return; }
        if (true) { return; } else if (false) { return; } else { return; }
    }""")
    loop, conditional = tree.functions[0].body.statements
    assert isinstance(loop, ast.For)
    assert loop.initializer is loop.condition is loop.update is None
    assert isinstance(conditional.otherwise, ast.If)
    assert isinstance(conditional.otherwise.otherwise, ast.Block)


def test_assignment_is_separate_from_expression():
    statements = parse("int main() { quint n = 1; n = n + 2; n += 1; }").functions[0].body.statements
    assert isinstance(statements[1], ast.Assignment)
    assert statements[1].target.identifier == "n" and statements[1].value.operator == "+"
    assert statements[2].operator == "+="
    with pytest.raises(DiagnosticError):
        parse("int main() { return (n = 3); }")


def test_literals_comments_and_unicode():
    tokens = lex('''// heading\r\n/* detail */ "α\\n" '\\u0041' '😀' 123 true''')
    assert [token.value for token in tokens[:-1]] == ["α\n", "A", "😀", 123, "true"]
    assert tokens[0].span.start.line == 2
    assert expression("-128").operand.value == 128  # range checking follows unary minus
    assert expression("true").value is True


def test_locations_and_diagnostic_serialization():
    source = "int main() {\r\n    return 5\r\n}"
    with pytest.raises(DiagnosticError) as failure:
        parse(source, "example.qut")
    error = failure.value
    assert error.code == "Q1002"
    assert error.span.start.line == 3 and error.span.start.column == 1
    assert error.span.start.offset == source.index("}")
    assert "example.qut:3:1" in str(error)
    assert error.to_dict()["span"]["start"]["line"] == 3
    tree = parse("\ufeffint main() { return 1; }", "bom.qut")
    assert tree.functions[0].span.start.offset == 1
    assert tree.functions[0].span.start.column == 1
    assert ast.to_dict(tree)["node"] == "Program"


@pytest.mark.parametrize("source", [
    "int main() { quint x; }", "int main() { if (true) return 1; }",
    "int main() { return [1,]; }", "int main() { return f(1,); }",
    "int main() { return 1;", "int main() { for (int i = 0 i < 3; i++) {} }",
    "int main() { int[][] a = []; }", "namespace Example {}",
])
def test_malformed_syntax_is_diagnostic(source):
    with pytest.raises(DiagnosticError) as failure:
        parse(source)
    assert failure.value.code == "Q1002"


@pytest.mark.parametrize("source", [
    '"unfinished', "/* unfinished", r'"\q"', r'"\uD800"',
    "'ab'", "''", '"line\nbreak"', "@", "α", r'"\u12"',
])
def test_lexical_failures_are_diagnostics(source):
    with pytest.raises(DiagnosticError) as failure:
        lex(source)
    assert failure.value.code == "Q1001"


def test_deep_source_is_bounded():
    with pytest.raises(DiagnosticError, match="nesting"):
        expression("(" * 1000 + "1" + ")" * 1000)
    with pytest.raises(DiagnosticError, match="nesting"):
        expression("!" * 1000 + "true")
    with pytest.raises(DiagnosticError, match="nesting"):
        parse("void main() {" + "{" * 1000 + "}" * 1000 + "}")
    with pytest.raises(DiagnosticError, match="nesting"):
        expression(" + ".join(["1"] * 1000))
    with pytest.raises(DiagnosticError, match="nesting"):
        expression("value" + ".Length" * 1000)


def test_truncated_programs_never_crash():
    source = "int main() { quint[] a = [1, 2]; for (int i = 0; i < a.Length; i++) { a[i] += 1; } return measure(a[0]); }"
    for end in range(len(source)):
        try:
            parse(source[:end])
        except DiagnosticError as error:
            assert error.code in {"Q1001", "Q1002"}


def test_parse_does_not_typecheck():
    tree = parse("void[] strange(void argument) { return unknown.name(); }")
    assert tree.functions[0].return_type.array
    assert isinstance(tree.functions[0].body.statements[0].value, ast.Call)
