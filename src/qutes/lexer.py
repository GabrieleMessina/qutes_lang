"""UTF-8 source tokens, literal decoding, and exact source spans."""

from dataclasses import dataclass

from qutes.diagnostics import DiagnosticError, Position, Span
from bisect import bisect_right
import re
import math
from antlr4 import InputStream, CommonTokenStream
from qutes.generated.QutesLexer import QutesLexer
from qutes.generated.QutesParser import QutesParser
from qutes.serialization import parse_integer
from qutes.diagnostics import DiagnosticErrors


@dataclass(frozen=True)
class Token:
    kind: str
    text: str
    value: str | int | None
    span: Span


class LiteralDecoder:
    ESCAPES = {"n": "\n", "r": "\r", "t": "\t", "0": "\0", "\\": "\\", '"': '"', "'": "'"}

    def __init__(self, source: str, path: str = "<source>"):
        self.source = source
        self.path = path
        self.index = 1 if source.startswith("\ufeff") else 0
        self.line = 1
        self.column = 1

    def position(self) -> Position:
        return Position(self.index, self.line, self.column)

    def advance(self) -> str:
        character = self.source[self.index]
        self.index += 1
        if character == "\r":
            if self.source[self.index:self.index + 1] == "\n":
                self.index += 1
            self.line += 1
            self.column = 1
        elif character == "\n":
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        return character

    def error(self, message: str, start: Position) -> DiagnosticError:
        return DiagnosticError("Q1001", message, Span(self.path, start, self.position()))

    def literal(self, quote: str, start: Position) -> str:
        self.advance()
        characters = []
        while self.index < len(self.source):
            character = self.source[self.index]
            if character == quote:
                self.advance()
                value = "".join(characters)
                if quote == "'" and len(value) != 1:
                    raise self.error("character literal must contain exactly one character", start)
                return value
            if ord(character) < 32:
                raise self.error("control characters in literals must be escaped", start)
            self.advance()
            if character == "\\":
                if self.index == len(self.source):
                    raise self.error("unterminated escape sequence", start)
                escape = self.advance()
                if escape == "u":
                    digits = self.source[self.index:self.index + 4]
                    if len(digits) != 4 or any(digit not in "0123456789abcdefABCDEF" for digit in digits):
                        raise self.error("Unicode escape requires four hexadecimal digits", start)
                    for _ in range(4):
                        self.advance()
                    character = chr(int(digits, 16))
                elif escape in self.ESCAPES:
                    character = self.ESCAPES[escape]
                else:
                    raise self.error(f"unsupported escape: \\{escape}", start)
            if 0xD800 <= ord(character) <= 0xDFFF:
                raise self.error("literal contains a surrogate, not a Unicode scalar", start)
            characters.append(character)
        raise self.error("unterminated literal", start)


class SourceMap:
    def __init__(self, source, path):
        self.source, self.path = source, path
        self.bom = int(source.startswith("\ufeff"))
        self.starts = [self.bom] + [m.end() for m in re.finditer(r"\r\n|\r|\n", source)]

    def position(self, offset):
        offset = min(len(self.source), max(self.bom, offset))
        line = bisect_right(self.starts, offset) - 1
        return Position(offset, line + 1, offset - self.starts[line] + 1)

    def span(self, start, end):
        return Span(self.path, self.position(start), self.position(end))

    def token_span(self, token):
        start = token.start + self.bom
        return self.span(start, start if token.type == -1 else token.stop + 1 + self.bom)


def token_value(token, locations):
    kind = QutesParser.symbolicNames[token.type] if token.type > 0 else "EOF"
    text = token.text
    span = locations.token_span(token)
    if kind in {"STRING", "CHAR"}:
        decoder = LiteralDecoder(locations.source, locations.path)
        decoder.index, decoder.line, decoder.column = span.start.offset, span.start.line, span.start.column
        return decoder.literal(text[0], span.start)
    if kind == "INT":
        try:
            return parse_integer(text)
        except ValueError:
            raise DiagnosticError("Q1001", "integer literal exceeds parser limits", span) from None
    if kind == "FLOAT":
        value = float(text)
        if not math.isfinite(value):
            raise DiagnosticError("Q1001", "floating-point literal must be finite", span)
        return value
    return text


def token_stream(source, path):
    locations = SourceMap(source, path)
    lexer = QutesLexer(InputStream(source[locations.bom:]))
    lexer.removeErrorListeners()
    stream = CommonTokenStream(lexer)
    stream.fill()
    errors = []
    bad = {QutesLexer.UNTERMINATED_COMMENT: "unterminated block comment",
           QutesLexer.UNTERMINATED_STRING: "unterminated literal",
           QutesLexer.UNTERMINATED_CHAR: "unterminated literal"}
    for token in stream.tokens:
        try:
            if token.type in bad:
                raise DiagnosticError("Q1001", bad[token.type], locations.token_span(token),
                                      help="Close the comment or quoted literal before continuing.")
            if token.type == QutesLexer.INVALID:
                raise DiagnosticError("Q1001", f"unexpected character {token.text!r}", locations.token_span(token))
            if token.type in {QutesLexer.STRING, QutesLexer.CHAR, QutesLexer.INT, QutesLexer.FLOAT}:
                token_value(token, locations)
        except DiagnosticError as error:
            error.source = source
            if not error.help:
                error.help = "Use a valid literal; supported escapes include \\n, \\t and \\uXXXX." if token.type in {QutesLexer.STRING, QutesLexer.CHAR} else "Remove or replace the invalid token."
            errors.append(error)
            if len(errors) == 10:
                break
    if errors:
        raise DiagnosticErrors(errors)
    return stream, locations


def lex(source: str, path: str = "<source>") -> tuple[Token, ...]:
    stream, locations = token_stream(source, path)
    result = []
    for token in stream.tokens:
        if token.type == -1:
            result.append(Token("EOF", "", None, locations.token_span(token)))
            continue
        kind = QutesParser.symbolicNames[token.type]
        if kind not in {"IDENT", "INT", "FLOAT", "STRING", "CHAR"}:
            kind = token.text
        value = token_value(token, locations) if kind in {"IDENT", "INT", "FLOAT", "STRING", "CHAR"} or token.text[0].isalpha() else None
        result.append(Token(kind, token.text, value, locations.token_span(token)))
    return tuple(result)
