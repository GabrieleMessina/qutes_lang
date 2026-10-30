"""Developer-facing syntax command. Never misrepresent parsing as semantic checking."""

import argparse
import json
from pathlib import Path
import sys

from qutes import __version__
from qutes.diagnostics import DiagnosticError
from qutes.parser import parse
from qutes.syntax import to_dict


def main(arguments: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="qutes", description="Qutes compiler foundation (syntax only)")
    parser.add_argument("--version", action="version", version=__version__)
    commands = parser.add_subparsers(dest="command", required=True)
    syntax = commands.add_parser("parse", help="parse syntax; does not check types or quantum safety")
    syntax.add_argument("source", type=Path)
    syntax.add_argument("--json", action="store_true", help="emit a syntax tree or structured diagnostics")
    options = parser.parse_args(arguments)
    try:
        with options.source.open(encoding="utf-8", newline="") as stream:
            source = stream.read()
        program = parse(source, str(options.source))
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
    if options.json:
        print(json.dumps({"stage": "syntax-only", "program": to_dict(program)}, ensure_ascii=True))
    else:
        print(f"Syntax OK: {len(program.functions)} function(s). Types and quantum safety have NOT been checked.")
    return 0
