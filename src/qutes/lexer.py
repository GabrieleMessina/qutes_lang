"""UTF-8 source tokens, literal decoding, and exact source spans."""

from dataclasses import dataclass

from qutes.diagnostics import DiagnosticError, Position, Span
from qutes.vocabulary import KEYWORDS


@dataclass(frozen=True)
class Token:
    kind: str
    text: str
    value: str | int | None
    span: Span


def _identifier_start(character: str) -> bool:
    return character.isascii() and (character.isalpha() or character == "_")


class Lexer:
    DOUBLE = frozenset({"==", "!=", "<=", ">=", "+=", "-=", "++", "--", "&&", "||"})
    SINGLE = frozenset("(){}[],;.+-*/%!<>=")
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

    def tokens(self) -> tuple[Token, ...]:
        result = []
        while self.index < len(self.source):
            character = self.source[self.index]
            if character in " \t\r\n":
                self.advance()
                continue
            start = self.position()
            pair = self.source[self.index:self.index + 2]
            if pair == "//":
                while self.index < len(self.source) and self.source[self.index] not in "\r\n":
                    self.advance()
                continue
            if pair == "/*":
                self.advance()
                self.advance()
                while self.index < len(self.source) and self.source[self.index:self.index + 2] != "*/":
                    self.advance()
                if self.index == len(self.source):
                    raise self.error("unterminated block comment", start)
                self.advance()
                self.advance()
                continue
            value: str | int | None = None
            if _identifier_start(character):
                self.advance()
                while self.index < len(self.source):
                    current = self.source[self.index]
                    if not (_identifier_start(current) or current in "0123456789"):
                        break
                    self.advance()
                value = self.source[start.offset:self.index]
                kind = value if value in KEYWORDS else "IDENT"
            elif character in "0123456789":
                self.advance()
                while self.index < len(self.source) and self.source[self.index] in "0123456789":
                    self.advance()
                try:
                    value = int(self.source[start.offset:self.index])
                except ValueError:
                    raise self.error("integer literal exceeds parser limits", start) from None
                kind = "INT"
            elif character in "\"'":
                value = self.literal(character, start)
                kind = "STRING" if character == '"' else "CHAR"
            elif pair in self.DOUBLE:
                self.advance()
                self.advance()
                kind = pair
            elif character in self.SINGLE:
                self.advance()
                kind = character
            else:
                self.advance()
                raise self.error(f"unexpected character {character!r}", start)
            result.append(Token(kind, self.source[start.offset:self.index], value,
                                Span(self.path, start, self.position())))
        end = self.position()
        result.append(Token("EOF", "", None, Span(self.path, end, end)))
        return tuple(result)


def lex(source: str, path: str = "<source>") -> tuple[Token, ...]:
    return Lexer(source, path).tokens()
