import json

import pytest

from qutes.cli import main
from qutes.compiler import compile_source
from qutes.config import CompilerConfig
from qutes.diagnostics import DiagnosticError
from qutes.reporting import storage_size


@pytest.mark.parametrize("amount,expected", [(0, "0 B"), (1023, "1023 B"),
    (1024, "1 KiB"), (1536, "1.5 KiB"), (8388608, "8 MiB"),
    (1 << 30, "1 GiB"), (1 << 60, "1 EiB")])
def test_storage_units(amount, expected):
    assert storage_size(amount, 0) == expected


def test_huge_storage_is_symbolic():
    assert storage_size(None, 1000004) == "2^999944 EiB"


@pytest.mark.parametrize("command", ["analyze", "construct", "check", "explain", "build"])
def test_warning_once_and_json_clean(command, tmp_path, capsys):
    source = tmp_path / "wildcard.qut"
    source.write_text('qustring text="A?"; return measure(text);')
    args = [command, str(source), "--alphabet", "AB?"]
    assert main(args) == 0
    output = capsys.readouterr()
    assert output.err.count("QW0001") == 1
    assert main(args + ["--json"]) == 0
    output = capsys.readouterr()
    assert not output.err
    assert json.loads(output.out)["warnings"][0]["code"] == "QW0001"


def test_wildcards_remain_patterns_and_api_is_silent(capsys):
    c = compile_source('qustring s="AB"; return measure("A?" in s);', config=CompilerConfig(alphabet="AB"))
    assert c.metadata["warnings"] == []
    with pytest.raises(DiagnosticError, match="does not prepare a superposition"):
        compile_source('qustring s="A?";', config=CompilerConfig(alphabet="AB"))
    c = compile_source('qustring s="A?";', config=CompilerConfig(alphabet="AB?"))
    assert c.metadata["warnings"][0]["severity"] == "warning"
    assert not capsys.readouterr().out
    assert not capsys.readouterr().err
