import json
from pathlib import Path
import subprocess
import sys

from qutes.cli import main


def test_json_parse_is_explicitly_syntax_only(tmp_path, capsys):
    source = tmp_path / "example.qut"
    source.write_text("int main() { return unknown; }", encoding="utf-8")
    assert main(["parse", str(source), "--json"]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["stage"] == "syntax-only"
    assert payload["program"]["functions"][0]["name"] == "main"


def test_json_syntax_failure(tmp_path, capsys):
    source = tmp_path / "bad.qut"
    source.write_text("int main() { return;", encoding="utf-8")
    assert main(["parse", str(source), "--json"]) == 1
    payload = json.loads(capsys.readouterr().out)
    assert payload["diagnostics"][0]["code"] == "Q1002"


def test_missing_file_and_invalid_utf8(tmp_path, capsys):
    source = tmp_path / "missing.qut"
    assert main(["parse", str(source)]) == 1
    assert "Q0001" in capsys.readouterr().err
    source.write_bytes(b"\xff")
    assert main(["parse", str(source), "--json"]) == 1
    assert json.loads(capsys.readouterr().out)["diagnostics"][0]["code"] == "Q0001"


def test_cli_preserves_crlf_offsets(tmp_path, capsys):
    source = tmp_path / "crlf.qut"
    text = "int main() {\r\n    return 1;\r\n}"
    source.write_bytes(text.encode("utf-8"))
    assert main(["parse", str(source), "--json"]) == 0
    payload = json.loads(capsys.readouterr().out)
    statement = payload["program"]["functions"][0]["body"]["statements"][0]
    assert statement["span"]["start"]["offset"] == text.index("return")
    assert statement["span"]["start"]["line"] == 2


def test_developer_entrypoint_from_checkout():
    root = Path(__file__).resolve().parents[1]
    result = subprocess.run(
        [sys.executable, str(root / "tools/qutes.py"), "parse",
         str(root / "tests/acceptance/A004_snapshots.qut")],
        capture_output=True, text=True, check=False,
    )
    assert result.returncode == 0, result.stderr
    assert "Types and quantum safety have NOT been checked" in result.stdout
