"""Developer commands expose each implemented analysis stage honestly."""

import argparse
import json
from pathlib import Path
import sys

from qutes import __version__
from qutes import ir
from qutes.checker import analyze
from qutes.config import CompilerConfig
from qutes.diagnostics import DiagnosticError, Position, Span
from qutes.parser import parse
from qutes.syntax import to_dict


def main(arguments: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="qutes", description="Qutes compiler foundation")
    parser.add_argument("--version", action="version", version=__version__)
    commands = parser.add_subparsers(dest="command", required=True)
    syntax = commands.add_parser("parse", help="parse syntax; does not check types or quantum safety")
    syntax.add_argument("source", type=Path)
    syntax.add_argument("--json", action="store_true", help="emit a syntax tree or structured diagnostics")
    analysis = commands.add_parser("analyze", help="check names/types/stages/effects; cleanup is not yet checked")
    analysis.add_argument("source", type=Path)
    analysis.add_argument("--json", action="store_true", help="emit typed IR or structured diagnostics")
    analysis.add_argument("--config", type=Path, help="explicit qutes.toml project configuration")
    analysis.add_argument("--quint-bits", type=int, help="override the configured quantum integer width")
    options = parser.parse_args(arguments)
    try:
        with options.source.open(encoding="utf-8", newline="") as stream:
            source = stream.read()
        program = parse(source, str(options.source))
        typed = None
        if options.command == "analyze":
            overrides = {} if options.quint_bits is None else {"quint_bits": options.quint_bits}
            try:
                config = CompilerConfig.load(options.config, overrides) if options.config else CompilerConfig.resolve(overrides=overrides)
            except (OSError, ValueError) as error:
                point = Position(0, 1, 1)
                raise DiagnosticError("Q0002", f"invalid configuration: {error}",
                                      Span(str(options.config or "<options>"), point, point)) from None
            typed = analyze(program, config)
    except DiagnosticError as error:
        if options.json:
            print(json.dumps({"diagnostics": [error.to_dict()]}, ensure_ascii=True))
        else:
            print(error, file=sys.stderr)
        return 1
    except (OSError, UnicodeError) as error:
        message = f"cannot read UTF-8 source: {error}"
        if options.json:
            print(json.dumps({"diagnostics": [{"code": "Q0001", "message": message,
                                               "path": str(options.source)}]}))
        else:
            print(f"{options.source}: Q0001: {message}", file=sys.stderr)
        return 1
    if typed is not None:
        if options.json:
            print(json.dumps({"stage": "types-stages-effects", "program": ir.to_dict(typed)}, ensure_ascii=True))
        else:
            print("Analysis OK: names, types, stages, and effects. Quantum cleanup and build-time bounds have NOT been verified.")
    elif options.json:
        print(json.dumps({"stage": "syntax-only", "program": to_dict(program)}, ensure_ascii=True))
    else:
        print(f"Syntax OK: {len(program.functions)} function(s). Types and quantum safety have NOT been checked.")
    return 0
