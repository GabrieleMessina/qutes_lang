import builtins
import io
from pathlib import Path
import xml.etree.ElementTree as ET

import pytest

from qutes.cli import main
from qutes.compiler import compile_source
from qutes.config import CompilerConfig
from qutes.diagnostics import DiagnosticError
from qutes.serialization import load_json
from qutes.visualization import render

pytestmark = pytest.mark.backend
SOURCE = """
    qubit q=superposition(); bool before=measure(q);
    if(before) { q=!q; }
    return [before,measure(q)];
"""


def compilation(source=SOURCE, **kwargs):
    return compile_source(source, path="sample.qut", config=CompilerConfig(quint_bits=3), **kwargs)


@pytest.mark.parametrize("command", ["check", "build", "run", "explain"])
def test_print_option_on_all_full_commands_preserves_json(command, tmp_path, capsys):
    source = tmp_path / "sample.qut"
    source.write_text(SOURCE)
    options = [command, str(source), "--print-circuit", "--json"]
    if command == "run":
        options.extend(["--shots", "16", "--seed", "1"])
    assert main(options) == 0
    output = capsys.readouterr()
    payload = load_json(output.out)
    assert payload["circuit_diagram"] == {"stage": "compiler-output", "printed": True, "image": None, "view": {"unfold": 0, "unfold_only": []}}
    assert "Final compiler circuit" in output.err and "If-0" in output.err
    assert "H" in output.err and "M" in output.err
    if command == "run":
        assert all(item["value"][1] is False for item in payload["outcomes"])


def test_human_output_prints_diagram_to_stdout(tmp_path, capsys):
    source = tmp_path / "sample.qut"
    source.write_text(SOURCE)
    assert main(["check", str(source), "--print-circuit"]) == 0
    output = capsys.readouterr()
    assert "Final compiler circuit" in output.out and "Check OK" in output.out
    assert not output.err


@pytest.mark.parametrize("image_format", ["png", "svg"])
def test_save_option_creates_nested_folder_and_valid_image(image_format, tmp_path, capsys):
    source, folder = tmp_path / "sample.qut", tmp_path / "nested" / "diagrams"
    source.write_text(SOURCE)
    assert main(["check", str(source), "--save-circuit", str(folder), "--circuit-format", image_format,
                 "--print-circuit", "--json"]) == 0
    output = capsys.readouterr()
    payload = load_json(output.out)
    path = Path(payload["circuit_diagram"]["image"])
    assert path.parent == folder.resolve() and path.suffix == "." + image_format
    assert path.name.startswith(f"sample-{payload['metadata']['build_sha256'][:12]}-")
    assert "If-0" in output.err
    if image_format == "png":
        from PIL import Image
        with Image.open(path) as image:
            assert image.format == "PNG"
            assert image.width > 100 and image.height > 50
            assert len(set(image.convert("RGB").getdata())) > 10
    else:
        assert ET.parse(path).getroot().tag == "{http://www.w3.org/2000/svg}svg"


def test_default_png_and_saved_image_message(tmp_path, capsys):
    source = tmp_path / "sample.qut"
    source.write_text(' quint n=1; return measure(n); ')
    assert main(["check", str(source), "--quint-bits", "2", "--save-circuit", str(tmp_path / "images")]) == 0
    assert "Saved circuit image:" in capsys.readouterr().out
    assert len(list((tmp_path / "images").glob("*.png"))) == 1


def test_input_bindings_get_distinct_images_and_repeated_build_reuses_filename(tmp_path):
    source = 'input int n;  quint q=n; return measure(q); '
    first = compilation(source, inputs={"n": 1})
    second = compilation(source, inputs={"n": 2})
    unrelated = tmp_path / "notes.txt"
    unrelated.write_text("keep")
    a = render(first, directory=tmp_path)
    b = render(second, directory=tmp_path)
    assert a["image"] != b["image"]
    assert render(first, directory=tmp_path)["image"] == a["image"]
    assert len(list(tmp_path.glob("*.png"))) == 2
    assert unrelated.read_text() == "keep"


def test_drawing_does_not_simulate_or_change_the_circuit(monkeypatch, tmp_path):
    import qiskit_aer
    def forbidden(*args, **kwargs):
        pytest.fail("drawing must not simulate")
    monkeypatch.setattr(qiskit_aer.AerSimulator, "run", forbidden)
    value = compilation(' quint n=superposition(); { quint temporary=n+1; } return measure(n); ')
    circuit, _ = value.build()
    expected = circuit.copy()
    monkeypatch.setattr(type(value), "build", lambda self: (circuit, None))
    render(value, print_circuit=True, directory=tmp_path, stream=io.StringIO())
    assert circuit == expected


def test_empty_classical_program_has_explicit_text_and_image(tmp_path):
    output = io.StringIO()
    result = render(compilation(' return 42; '), print_circuit=True, directory=tmp_path, stream=output)
    assert "No quantum operations or measurements" in output.getvalue()
    assert Path(result["image"]).is_file()


def test_ascii_console_falls_back_to_legible_wires():
    buffer = io.BytesIO()
    output = io.TextIOWrapper(buffer, encoding="ascii")
    render(compilation(), print_circuit=True, stream=output)
    output.flush()
    text = buffer.getvalue().decode("ascii")
    assert "--" in text and "|" in text and "H" in text and "M" in text


def test_missing_image_dependency_reports_how_to_install(monkeypatch, tmp_path):
    original = builtins.__import__
    def unavailable(name, *args, **kwargs):
        if name == "matplotlib":
            raise ImportError("test missing plotting library")
        return original(name, *args, **kwargs)
    monkeypatch.setattr(builtins, "__import__", unavailable)
    with pytest.raises(DiagnosticError, match=r"qutes-lang\[visualization\]") as error:
        render(compilation(), directory=tmp_path)
    assert error.value.code == "Q5001"
    # Console drawing still works without image libraries.
    render(compilation(), print_circuit=True, stream=io.StringIO())


def test_output_error_is_deliberate_and_closes_figure(tmp_path):
    from matplotlib import pyplot as plt
    blocked = tmp_path / "not-a-folder"
    blocked.write_text("keep")
    before = plt.get_fignums()
    with pytest.raises(DiagnosticError) as error:
        render(compilation(), directory=blocked)
    assert error.value.code == "Q0004"
    assert blocked.read_text() == "keep" and plt.get_fignums() == before


def test_failed_write_preserves_previous_image_and_cleans_temporary_file(monkeypatch, tmp_path):
    from matplotlib.figure import Figure
    from matplotlib import pyplot as plt
    value = compilation()
    path = Path(render(value, directory=tmp_path)["image"])
    previous = path.read_bytes()
    def broken(*args, **kwargs):
        raise OSError("test disk failure")
    monkeypatch.setattr(Figure, "savefig", broken)
    with pytest.raises(DiagnosticError, match="test disk failure"):
        render(value, directory=tmp_path)
    assert path.read_bytes() == previous
    assert not list(tmp_path.glob(".qutes-circuit-*.tmp"))
    assert not plt.get_fignums()


def test_huge_image_is_rejected_before_creating_output(monkeypatch, tmp_path):
    import qutes.visualization as visualization
    from matplotlib import pyplot as plt
    monkeypatch.setattr(visualization, "MAX_IMAGE_PIXELS", 1)
    with pytest.raises(DiagnosticError) as error:
        render(compilation(), directory=tmp_path / "images")
    assert error.value.code == "Q4001"
    assert not (tmp_path / "images").exists() and not plt.get_fignums()


def test_format_requires_output_folder(tmp_path):
    with pytest.raises(SystemExit) as error:
        main(["check", str(tmp_path / "unused.qut"), "--circuit-format", "svg"])
    assert error.value.code == 2


def test_drawer_failure_becomes_a_source_diagnostic(monkeypatch):
    from qiskit import QuantumCircuit
    def broken(*args, **kwargs):
        raise RuntimeError("test drawer failure")
    monkeypatch.setattr(QuantumCircuit, "draw", broken)
    with pytest.raises(DiagnosticError, match="test drawer failure") as error:
        render(compilation(), print_circuit=True)
    assert error.value.code == "Q5003" and error.value.span.path == "sample.qut"


def test_image_drawer_failure_cleans_partial_figure(monkeypatch, tmp_path):
    from qiskit import QuantumCircuit
    from matplotlib import pyplot as plt
    def broken(*args, **kwargs):
        plt.figure()
        raise RuntimeError("partial image")
    monkeypatch.setattr(QuantumCircuit, "draw", broken)
    with pytest.raises(DiagnosticError, match="partial image") as error:
        render(compilation(), directory=tmp_path)
    assert error.value.code == "Q5003" and not plt.get_fignums()
