"""Classical value encodings. These functions do not simulate quantum states."""

from dataclasses import dataclass

from qutes.config import validate_alphabet


def _integer(value: int, name: str) -> None:
    if type(value) is not int:
        raise ValueError(f"{name} must be an integer, not a Boolean or other value")


@dataclass(frozen=True)
class SignedInteger:
    width: int

    def __post_init__(self) -> None:
        _integer(self.width, "width")
        if self.width < 1:
            raise ValueError("width must be positive")

    @property
    def minimum(self) -> int:
        return -(1 << (self.width - 1))

    @property
    def maximum(self) -> int:
        return (1 << (self.width - 1)) - 1

    @property
    def modulus(self) -> int:
        return 1 << self.width

    def encode(self, value: int) -> int:
        _integer(value, "value")
        if not self.minimum <= value <= self.maximum:
            raise ValueError(f"{value} is outside {self.minimum}..{self.maximum}")
        return value % self.modulus

    def decode(self, bits: int) -> int:
        _integer(bits, "bits")
        if not 0 <= bits < self.modulus:
            raise ValueError("bit pattern does not fit the register")
        return bits if bits <= self.maximum else bits - self.modulus

    def add(self, left: int, right: int) -> int:
        return self.decode((self.encode(left) + self.encode(right)) % self.modulus)

    def rotate_left(self, value: int, count: int) -> int:
        _integer(count, "rotation count")
        if count < 0:
            raise ValueError("rotation count cannot be negative")
        bits = self.encode(value)
        count %= self.width
        rotated = ((bits << count) | (bits >> (self.width - count))) % self.modulus
        return self.decode(rotated)

    def rotate_right(self, value: int, count: int) -> int:
        _integer(count, "rotation count")
        if count < 0:
            raise ValueError("rotation count cannot be negative")
        return self.rotate_left(value, (-count) % self.width)


@dataclass(frozen=True)
class EncodedString:
    codes: tuple[int, ...]
    length: int


@dataclass(frozen=True)
class TextEncoding:
    alphabet: str
    capacity: int

    def __post_init__(self) -> None:
        validate_alphabet(self.alphabet)
        _integer(self.capacity, "capacity")
        if self.capacity < 1:
            raise ValueError("capacity must be positive")

    @property
    def bits_per_character(self) -> int:
        return (len(self.alphabet) - 1).bit_length()

    def encode_character(self, character: str) -> int:
        if not isinstance(character, str) or len(character) != 1:
            raise ValueError("expected one Unicode scalar character")
        try:
            return self.alphabet.index(character)
        except ValueError:
            raise ValueError(f"{character!r} is not in the configured alphabet") from None

    def decode_character(self, code: int) -> str:
        _integer(code, "character code")
        if not 0 <= code < len(self.alphabet):
            raise ValueError(f"unused or invalid character code: {code}")
        return self.alphabet[code]

    def encode_string(self, text: str) -> EncodedString:
        if not isinstance(text, str):
            raise ValueError("expected a string")
        if len(text) > self.capacity:
            raise ValueError("string exceeds configured capacity")
        codes = tuple(self.encode_character(character) for character in text)
        return EncodedString(codes + (0,) * (self.capacity - len(text)), len(text))

    def decode_string(self, value: EncodedString) -> str:
        _integer(value.length, "string length")
        if len(value.codes) != self.capacity or not 0 <= value.length <= self.capacity:
            raise ValueError("invalid encoded string shape")
        characters = [self.decode_character(code) for code in value.codes]
        if any(code != 0 for code in value.codes[value.length:]):
            raise ValueError("invalid nonzero string padding")
        return "".join(characters[:value.length])
