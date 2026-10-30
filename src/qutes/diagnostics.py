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
    def __init__(self, code: str, message: str, span: Span):
        self.code = code
        self.message = message
        self.span = span
        super().__init__(str(self))

    def __str__(self) -> str:
        start = self.span.start
        return f"{self.span.path}:{start.line}:{start.column}: {self.code}: {self.message}"

    def to_dict(self) -> dict:
        return {"code": self.code, "message": self.message, "span": asdict(self.span)}
