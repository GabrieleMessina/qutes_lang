"""Deterministic JSON with bounded, lossless large classical integers.

Avoid changing Python's process-wide decimal conversion limit. Chunk conversion
also works for valid classical values larger than that limit.
"""

import json


def integer_text(value: int) -> str:
    negative = value < 0
    value = abs(value)
    pieces = []
    while value >= 1_000_000_000:
        value, remainder = divmod(value, 1_000_000_000)
        pieces.append(f"{remainder:09d}")
    return ("-" if negative else "") + str(value) + "".join(reversed(pieces))


def parse_integer(text: str, max_digits=100_000) -> int:
    negative = text.startswith("-")
    digits = text[1:] if negative else text
    if max_digits is not None and len(digits) > max_digits:
        raise ValueError("integer text exceeds the serialization limit")
    value = 0
    for index in range(0, len(digits), 9):
        chunk = digits[index:index + 9]
        value = value * 10**len(chunk) + int(chunk)
    return -value if negative else value


def json_text(value) -> str:
    if value is None: return "null"
    if value is True: return "true"
    if value is False: return "false"
    if isinstance(value, int): return integer_text(value)
    if isinstance(value, str): return json.dumps(value, ensure_ascii=True)
    if isinstance(value, float): return json.dumps(value, allow_nan=False)
    if isinstance(value, complex): return json_text({"real": value.real, "imag": value.imag})
    if isinstance(value, (tuple, list)):
        return "[" + ",".join(json_text(item) for item in value) + "]"
    if isinstance(value, dict):
        if not all(isinstance(key, str) for key in value):
            raise TypeError("JSON object keys must be strings")
        return "{" + ",".join(json_text(key) + ":" + json_text(value[key]) for key in sorted(value)) + "}"
    raise TypeError(f"cannot serialize {type(value).__name__}")


def load_json(text: str, *, max_integer_digits=100_000):
    def invalid_constant(value):
        raise ValueError(f"non-finite JSON value {value} is not supported")
    try:
        value = json.loads(text, parse_int=lambda token: parse_integer(token, max_integer_digits),
                           parse_constant=invalid_constant)
    except RecursionError:
        raise ValueError("JSON nesting exceeds the input limit") from None
    pending = [(value, 0)]
    while pending:
        current, depth = pending.pop()
        if depth > 512:
            raise ValueError("JSON nesting exceeds the input limit")
        if isinstance(current, dict):
            pending.extend((child, depth + 1) for child in current.values())
        elif isinstance(current, list):
            pending.extend((child, depth + 1) for child in current)
    return value
