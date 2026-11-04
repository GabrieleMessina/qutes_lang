"""Public delivery commands and explicit intermediate compiler views."""

import argparse
from pathlib import Path
import sys

from qutes import __version__, ir
from qutes.checker import analyze
from qutes.codegen import write_python
from qutes.compiler import compile_source
from qutes.config import CompilerConfig
from qutes.construction import construct
from qutes.diagnostics import DiagnosticError, Position, Span
from qutes.parser import parse
from qutes.serialization import json_text, load_json
from qutes.syntax import to_dict


def diagnostic(code, message, path):
    point = Position(0, 1, 1)
    return DiagnosticError(code, message, Span(str(path), point, point))


def configuration(options):
    path = options.config
    if path is None:
        adjacent = options.source.parent / "qutes.toml"
        if adjacent.is_file():
            path = adjacent
    overrides = {key: getattr(options, key) for key in CompilerConfig.__dataclass_fields__
                 if getattr(options, key, None) is not None}
    try:
        return CompilerConfig.load(path, overrides) if path else CompilerConfig.resolve(overrides=overrides)
    except (OSError, ValueError) as error:
        raise diagnostic("Q0002", f"invalid configuration: {error}", path or "<options>") from None


def input_values(options):
    path = getattr(options, "inputs", None)
    if path is None:
        return {}
    try:
        return load_json(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, ValueError) as error:
        raise diagnostic("Q0003", f"invalid input file: {error}", path) from None


def argument_parser():
    parser = argparse.ArgumentParser(prog="qutes", description="Compile and run high-level quantum programs")
    parser.add_argument("--version", action="version", version=__version__)
    commands = parser.add_subparsers(dest="command", required=True)
    descriptions = {
        "check": "validate types, staging, resource bounds, and automatic cleanup",
        "build": "write a readable Qiskit Python module",
        "run": "execute on the local simulator and decode results",
        "explain": "show allocations, cleanup, snapshots, and resource estimates",
        "parse": "parse syntax only; does not check types or quantum safety",
        "analyze": "check names/types/stages/effects; does not verify cleanup",
        "construct": "expand classical work and inline calls; does not verify cleanup",
    }
    for command, description in descriptions.items():
        sub = commands.add_parser(command, help=description)
        sub.add_argument("source", type=Path)
        sub.add_argument("--json", action="store_true", help="emit structured results or diagnostics")
        if command != "parse":
            sub.add_argument("--config", type=Path, help="explicit config; otherwise read source-adjacent qutes.toml")
            for key in CompilerConfig.__dataclass_fields__:
                flag = "--max-qubits" if key == "max_simulation_qubits" else "--" + key.replace("_", "-")
                argument_type = str if key == "alphabet" else float if key == "search_failure_probability" else int
                sub.add_argument(flag, dest=key, type=argument_type, help=f"override {key}")
        if command not in {"parse", "analyze"}:
            sub.add_argument("--inputs", type=Path, help="JSON object binding script input declarations")
        if command in {"check", "build", "run", "explain"}:
            sub.add_argument("--print-circuit", action="store_true", help="print the final compiler circuit (stderr with --json)")
            sub.add_argument("--save-circuit", type=Path, metavar="FOLDER", help="save a circuit image in this folder (created if needed)")
            sub.add_argument("--circuit-format", choices=("png", "svg"), help="image format for --save-circuit; default: png")
        if command == "build":
            sub.add_argument("-o", "--output", type=Path, help="output module; default: SOURCE.qiskit.py")
            sub.add_argument("--force", action="store_true", help="replace an existing non-generated output file")
        if command == "run":
            sub.add_argument("--shots", type=int, default=1024)
            sub.add_argument("--seed", type=int)
    return parser


def explain(metadata):
    cost = metadata["resources"]
    print(f"Qutes {metadata['compiler_version']}; language {metadata['language_version']}")
    for search in metadata.get("searches", ()):
        print(f"Search: {search['entries']} entries, {search['oracle_calls']} oracle calls, "
              f"failure bound {search['failure_probability']:g} when a match exists; "
              f"{search['retained_index_qubits']} retained index qubits, "
              f"{search['workspace_qubits']} workspace qubits; linear controlled access")
    print(f"Build: {metadata['build_sha256']}")
    print(f"Reserved qubits: {cost['allocated_qubits']} (including {cost['cleaned_qubits_at_end']} cleaned; wires are not reused)")
    print(f"Snapshot bits: {cost['classical_bits']}; cleanup events: {cost['cleanup_events']}")
    print(f"Gate applications: {cost['gate_applications']}; library adders: {cost['library_adders']} (before backend decomposition)")
    estimate = cost["statevector_bytes"]
    print(f"Statevector storage alone: {estimate if estimate is not None else '2^' + str(cost['statevector_bytes_power_of_two'])} bytes; backend overhead is additional")
    print(f"Simulation limit: {cost['simulation_limit_qubits']} qubits; within limit: {cost['simulation_within_limit']}")
    print("Inputs are construction-time values; quantum conditions stay coherent; measured conditions use snapshots.")
    for allocation in metadata["allocations"]:
        status = "cleaned" if allocation["released"] else "live at shot end"
        print(f"  {allocation['name']}: wires {allocation['bits']}, {status}")
    print(f"Result layout: {json_text(metadata['result_layout'])}")


def main(arguments: list[str] | None = None) -> int:
    parser = argument_parser()
    options = parser.parse_args(arguments)
    if getattr(options, "circuit_format", None) and options.save_circuit is None:
        parser.error("--circuit-format requires --save-circuit FOLDER")
    try:
        try:
            with options.source.open(encoding="utf-8", newline="") as stream:
                source = stream.read()
        except (OSError, UnicodeError) as error:
            raise diagnostic("Q0001", f"cannot read UTF-8 source: {error}", options.source) from None
        if options.command in {"parse", "analyze", "construct"}:
            syntax = parse(source, str(options.source))
            if options.command == "parse":
                payload = {"stage": "syntax-only", "program": to_dict(syntax)}
                message = f"Syntax OK: {len(syntax.functions)} function(s). Types and quantum safety have NOT been checked."
            else:
                typed = analyze(syntax, configuration(options))
                if options.command == "analyze":
                    payload = {"stage": "types-stages-effects", "program": ir.to_dict(typed)}
                    message = "Analysis OK: names, types, stages, and effects. Quantum cleanup and build-time bounds have NOT been verified."
                else:
                    constructed = construct(typed, input_values(options))
                    payload = {"stage": "construction", "program": ir.to_dict(constructed)}
                    message = f"Construction OK: {constructed.loop_iterations} expanded iterations; quantum cleanup has NOT been verified."
            print(json_text(payload) if options.json else message)
            return 0

        compilation = compile_source(source, path=str(options.source), inputs=input_values(options), config=configuration(options))
        metadata = compilation.metadata
        if options.command == "run":
            payload = compilation.run(shots=options.shots, seed=options.seed)
        elif options.command == "build":
            output = options.output or options.source.with_suffix(".qiskit.py")
            write_python(compilation, output, force=options.force)
            payload = {"stage": "build", "output": str(output), "metadata": metadata}
        elif options.command == "explain":
            payload = dict(metadata)
        else:
            payload = {"stage": "checked", "cleanup_verified": True, "metadata": metadata}
        if options.print_circuit or options.save_circuit is not None:
            from qutes.visualization import render
            payload["circuit_diagram"] = render(compilation, print_circuit=options.print_circuit,
                directory=options.save_circuit, image_format=options.circuit_format or "png",
                stream=sys.stderr if options.json else sys.stdout)
        if options.json:
            print(json_text(payload))
        else:
            if options.command == "run":
                print(f"{payload['execution']['shots']} shots; {payload['execution']['backend']}")
                for outcome in payload["outcomes"]:
                    print(f"{json_text(outcome['value'])}: {outcome['count']} ({outcome['probability']:.1%})")
            elif options.command == "build":
                print(f"Built {output}; {metadata['resources']['allocated_qubits']} reserved qubits.")
            elif options.command == "explain":
                explain(metadata)
            else:
                print("Check OK: types, staging, construction bounds, and automatic cleanup verified.")
            image = payload.get("circuit_diagram", {}).get("image")
            if image:
                print(f"Saved circuit image: {image}")
        return 0
    except DiagnosticError as error:
        if options.json:
            print(json_text({"diagnostics": [item.to_dict() for item in error.diagnostics]}))
        else:
            print(error.render(locals().get("source")), file=sys.stderr)
        return 1
