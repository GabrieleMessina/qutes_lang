"""Source coordinates and structured diagnostics shared by compiler phases."""

from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class Position:
    offset: int
    line: int
    column: int


@dataclass(frozen=True)
class Span:
    path: str
    start: Position
    end: Position

    def through(self, other: "Span") -> "Span":
        if self.path != other.path:
            raise ValueError("cannot merge spans from different source files")
        return Span(self.path, self.start, other.end)


class DiagnosticError(Exception):
    def __init__(self, code: str, message: str, span: Span, *, help=None, related=(), source=None):
        self.code = code
        self.message = message
        self.span = span
        self.help = help
        self.related = tuple(related)
        self.source = source
        super().__init__(str(self))

    def __str__(self) -> str:
        start = self.span.start
        return f"{self.span.path}:{start.line}:{start.column}: {self.code}: {self.message}"

    def to_dict(self) -> dict:
        result = {"code": self.code, "message": self.message, "span": asdict(self.span)}
        if self.help:
            result["help"] = self.help
        if self.related:
            result["related"] = [{"message": message, "span": asdict(span)} for message, span in self.related]
        return result

    @property
    def diagnostics(self):
        return (self,)

    def render(self, source=None):
        source = self.source if source is None else source
        lines = [str(self)]
        if source is not None:
            source_lines = source.lstrip("\ufeff").splitlines()
            start = self.span.start
            if 0 < start.line <= len(source_lines):
                prefix = f"  {start.line} | "
                line = source_lines[start.line - 1]
                offset = len(line[:start.column - 1].expandtabs(4))
                width = max(1, self.span.end.column - start.column) if start.line == self.span.end.line else 1
                lines.extend([prefix + line.expandtabs(4), " " * (len(prefix) + offset) + "^" * min(width, 80)])
        if self.help:
            lines.append(f"Help: {self.help}")
        for message, span in self.related:
            lines.append(f"Related: {span.path}:{span.start.line}:{span.start.column}: {message}")
        return "\n".join(lines)


class DiagnosticErrors(DiagnosticError):
    """A bounded collection; first-error fields preserve the exception API."""
    def __init__(self, diagnostics):
        self.items = tuple(diagnostics)
        first = self.items[0]
        super().__init__(first.code, first.message, first.span, help=first.help,
                         related=first.related, source=first.source)

    @property
    def diagnostics(self):
        return self.items

    def render(self, source=None):
        return "\n\n".join(item.render(source) for item in self.items)
