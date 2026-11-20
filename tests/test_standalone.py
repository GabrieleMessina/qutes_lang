import ast
import json
from pathlib import Path
import tomllib

import pytest

from qutes.compiler import compile_source
from qutes.config import CompilerConfig
from qutes.serialization import json_text
from qutes.standalone import standalone_source


TOUR = Path(__file__).resolve().parents[1] / "examples/language"
CASES = json.loads((TOUR / "catalog.json").read_text(encoding="utf-8"))["examples"]


@pytest.mark.backend
@pytest.mark.parametrize("case", CASES, ids=[case["file"] for case in CASES])
def test_standalone_circuit_and_decoding_match_compiler(case):
    config = tomllib.loads((TOUR / "qutes.toml").read_text())["qutes"]
    inputs = json.loads((TOUR / case["inputs"]).read_text()) if "inputs" in case else {}
    compilation = compile_source((TOUR / case["file"]).read_text(encoding="utf-8"), inputs=inputs,
                                 config=CompilerConfig.resolve(config, case.get("overrides", {})))
    source = standalone_source(compilation, default_shots=17)
    for node in ast.walk(ast.parse(source)):
        if isinstance(node, ast.ImportFrom):
            assert node.module.split(".")[0] in {"qiskit", "qiskit_aer"}
        if isinstance(node, ast.Import):
            assert all(item.name in {"argparse", "json"} for item in node.names)
    module = {"__name__": "standalone"}
    exec(source, module)
    reference, layout = compilation.build()
    assert module["build_circuit"]() == reference
    # Include non-palindromic patterns to exercise register and bit order.
    for memory in range(min(1 << reference.num_clbits, 128)):
        try:
            expected = layout.decode(memory)
        except ValueError:  # Padding or unused character codes outside valid circuit outputs.
            with pytest.raises((IndexError, ValueError)):
                module["decode_result"](memory)
        else:
            assert json_text(module["decode_result"](memory)) == json_text(expected)


def test_standalone_unrolled_snapshot_expression():
    compilation = compile_source("qubit q=false; bool b=measure(q);"
                                 "for(int i=0;i<225;i++){b=!b;} return b;")
    module = {"__name__": "standalone"}
    exec(standalone_source(compilation), module)
    assert [module["decode_result"](memory) for memory in (0, 1)] == [True, False]


def test_standalone_large_literal_and_runtime_arguments():
    result = 10**5000
    compilation = compile_source("input int n; return n;", inputs={"n": result})
    source = standalone_source(compilation, default_shots=3)
    module = {"__name__": "standalone"}
    exec(source, module)
    data = module["run"]()["outcomes"]
    assert data == [{"value": result, "count": 3, "probability": 1.0}]
    assert module["json_text"](data) == json_text(data)
    with pytest.raises(ValueError, match="shots"):
        module["run"](shots=0)
    with pytest.raises(ValueError, match="seed"):
        module["run"](seed=-1)
