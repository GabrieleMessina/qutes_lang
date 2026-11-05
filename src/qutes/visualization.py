"""Optional drawings of the complete compiler-emitted circuit; never simulate."""

import os
from pathlib import Path
import re
import sys
import tempfile
import hashlib
from qutes.serialization import json_text

from qutes.diagnostics import DiagnosticError, Position, Span

IMAGE_DPI = 120
MAX_IMAGE_PIXELS = 40_000_000
MAX_IMAGE_SIDE = 32_000


def failure(compilation, code, message, path=None):
    point = Position(0, 1, 1)
    return DiagnosticError(code, message, Span(str(path or compilation.source_path), point, point))


def write_text(text, stream):
    encoding = getattr(stream, "encoding", None) or "utf-8"
    try:
        text.encode(encoding)
    except UnicodeEncodeError:
        # Keep wires legible on terminals that cannot display Unicode box drawing.
        boxes = {code: "+" for code in range(0x2500, 0x2580)}
        boxes.update({ord(char): "-" for char in "─━"})
        boxes.update({ord("═"): "="})
        boxes.update({ord(char): "|" for char in "│┃║"})
        boxes.update({ord("■"): "o", ord("«"): "<", ord("»"): ">"})
        boxes[ord("░")] = ":"
        text = text.translate(boxes).encode(encoding, errors="replace").decode(encoding)
    print(text, file=stream)


def save_image(circuit, compilation, directory, image_format, options):
    try:
        import matplotlib
        # This compiler feature writes files only; it must not open GUI windows.
        matplotlib.use("Agg")
        from matplotlib import pyplot as plt
        import pylatexenc  # Required by Qiskit's Matplotlib drawer, not a LaTeX process.
    except ImportError as error:
        raise failure(compilation, "Q5001", f"circuit images require qutes-lang[visualization]: {error}") from None

    directory = Path(directory)
    stem = re.sub(r"[^A-Za-z0-9._-]", "_", Path(compilation.source_path).stem).strip("._") or "circuit"
    view_hash = hashlib.sha256(json_text(options).encode("utf-8")).hexdigest()[:8]
    filename = f"{stem}-{compilation.metadata['build_sha256'][:12]}-{view_hash}.{image_format}"
    target = directory / filename
    figure = None
    temporary = None
    existing_figures = set(plt.get_fignums())
    try:
        # Empty classical programs still get an explicit, useful image.
        if not circuit.num_qubits and not circuit.num_clbits:
            figure = plt.figure(figsize=(6, 1.5))
            figure.text(0.5, 0.5, "No quantum operations or measurements", ha="center", va="center")
        else:
            figure = circuit.draw(output="mpl", fold=25, idle_wires=True, cregbundle=False,
                                  reverse_bits=False, style="iqp", interactive=False, expr_len=80)
        width, height = (float(side) * IMAGE_DPI for side in figure.get_size_inches())
        if max(width, height) > MAX_IMAGE_SIDE or width * height > MAX_IMAGE_PIXELS:
            raise failure(compilation, "Q4001", "circuit image is too large; use --print-circuit or a smaller program")
        directory.mkdir(parents=True, exist_ok=True)
        with tempfile.NamedTemporaryFile(dir=directory, prefix=".qutes-circuit-", suffix=".tmp", delete=False) as output:
            temporary = Path(output.name)
        figure.savefig(temporary, format=image_format, dpi=IMAGE_DPI, bbox_inches="tight", facecolor="white")
        os.replace(temporary, target)
        return target.resolve()
    except OSError as error:
        raise failure(compilation, "Q0004", f"cannot save circuit image: {error}", target) from None
    finally:
        if figure is not None:
            plt.close(figure)
        # The drawer can create a figure and fail before returning it.
        for number in set(plt.get_fignums()) - existing_figures:
            plt.close(number)
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def render(compilation, *, print_circuit=False, directory=None, image_format="png", stream=None,
           unfold=0, unfold_only=None):
    """Render final compiler output, before backend-specific transpilation.

    One circuit exists per compilation/input binding. File names include the build
    identity so different bindings can share a folder. Repeating a build replaces
    only that build's image. Image export uses Matplotlib's headless Agg backend.
    """
    if image_format not in {"png", "svg"}:
        raise failure(compilation, "Q5003", "circuit image format must be png or svg")
    if not print_circuit and directory is None:
        if unfold != 0 or unfold_only is not None:
            raise failure(compilation, "Q5003", "unfold options require printed or saved diagram output")
        return None
    stream = sys.stdout if stream is None else stream
    try:
        from qutes.diagrams import build_diagram, view_options
        try:
            options = view_options(unfold, unfold_only)
        except (ValueError, TypeError, AttributeError) as error:
            raise failure(compilation, "Q5003", str(error)) from None
        circuit = build_diagram(compilation, **options)
        image = save_image(circuit, compilation, directory, image_format, options) if directory is not None else None
        if print_circuit:
            if not circuit.num_qubits and not circuit.num_clbits:
                drawing = "(No quantum operations or measurements.)"
            else:
                text = circuit.draw(output="text", fold=100, idle_wires=True, cregbundle=False, reverse_bits=False, expr_len=80)
                text.encoding = "utf-8"
                drawing = str(text)
            write_text("Final compiler circuit (presentation view; cleanup markers are annotations):\n" + drawing, stream)
        return {"stage": "compiler-output", "printed": print_circuit, "image": str(image) if image else None,
                "view": options}
    except DiagnosticError:
        raise
    except ImportError as error:
        raise failure(compilation, "Q5001", f"circuit drawing dependencies are unavailable: {error}") from None
    except Exception as error:
        raise failure(compilation, "Q5003", f"cannot draw circuit: {error}") from None
