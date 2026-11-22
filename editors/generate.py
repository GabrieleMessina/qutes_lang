"""Refresh editor vocabulary and TextMate grammar from the compiler's declarations."""
import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from qutes.vocabulary import Builtin, KEYWORDS, TYPES

PARAMETERS = {
    Builtin.SUPERPOSITION: [[], ["values"], ["values", "probabilities: weights"], ["values", "amplitudes: weights"]],
    Builtin.MEASURE: [["value"]], Builtin.ROTATE_LEFT: [["value", "amount"]],
    Builtin.ROTATE_RIGHT: [["value", "amount"]], Builtin.SEARCH: [["collection", "oracle"]],
    Builtin.COPY: [["arrayOrSlice"]], Builtin.COMPLEX: [["real", "imag"]],
    Builtin.HADAMARD: [["mut qubit q"]], Builtin.NOT: [["mut qubit q"]],
    Builtin.PHASE_FLIP: [["mut qubit q"]], Builtin.PHASE: [["mut qubit q", "float angle"]],
    Builtin.SWAP: [["mut qubit a", "mut qubit b"]],
}


def outputs():
    assert set(PARAMETERS) == set(Builtin)
    data = dict(types=sorted(TYPES), keywords=sorted(KEYWORDS - TYPES - {"true", "false"}),
                constants=["true", "false", "pi"], builtins=PARAMETERS)
    def words(items):
        return r"\b(?:" + "|".join(sorted(items)) + r")\b"
    variable = r"[A-Za-z_]\w*"
    patterns = [
        {"name": "comment.line.double-slash.qutes", "match": "//.*$"},
        {"name": "comment.block.qutes", "begin": r"/\*", "end": r"\*/"},
    ]
    for quote, kind in [('"', "double"), ("'", "single")]:
        patterns.append(dict(name=f"string.quoted.{kind}.qutes", begin=quote,
                             end=quote + "|$", patterns=[{"match": r"\\.", "name": "constant.character.escape.qutes"}]))
    declaration = "(" + words(TYPES) + r")(\s*(?:\[\s*\])?\s+)(" + variable + ")"
    for lookahead, scope in [(r"(?=\s*\()", "entity.name.function"), ("", "variable.other.definition")]:
        patterns.append({"match": declaration + lookahead, "captures": {
            "1": {"name": "storage.type.qutes"}, "3": {"name": scope + ".qutes"}}})
    for name, match in [
        ("support.function", words(PARAMETERS) + r"(?=\s*\()"), ("storage.type", words(TYPES)),
        ("keyword.control", words(data["keywords"])), ("constant.language", words(data["constants"])),
        ("constant.numeric", r"\b\d+(?:\.\d+)?(?:[eE][+-]?\d+)?\b"),
        ("entity.name.function", variable + r"(?=\s*\()"), ("keyword.operator", r"[+*/%!=&|<>.:-]+")]:
        patterns.append({"name": name + ".qutes", "match": match})
    return {"vocabulary.mjs": "export default " + json.dumps(data, indent=2) + ";\n",
            "../qutes-vscode/syntaxes/qutes.tmLanguage.json": json.dumps(
                dict(name="Qutes", scopeName="source.qutes", patterns=patterns), indent=2) + "\n"}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    for_check = parser.parse_args().check
    for name, value in outputs().items():
        path = Path(__file__).parent / name
        if for_check:
            if path.read_text(encoding="utf-8") != value:
                raise SystemExit(f"Regenerate {path.name} with python editors/generate.py")
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(value, encoding="utf-8", newline="\n")
