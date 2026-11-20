"""Finite construction-time numeric values and their external representation."""

import math

RANK = {"int": 0, "float": 1, "complex": 2}


def finite(value):
    parts = (value.real, value.imag) if type(value) is complex else (value,)
    if any(type(part) is float and not math.isfinite(part) for part in parts):
        raise ValueError("numeric values must be finite")
    return value


def convert(value, kind):
    if kind == "complex" and isinstance(value, dict):
        if set(value) != {"real", "imag"} or any(type(v) not in (int, float) for v in value.values()):
            raise ValueError("complex input requires numeric real and imag components")
        try:
            return finite(complex(value["real"], value["imag"]))
        except OverflowError:
            raise ValueError("numeric conversion exceeds finite floating-point range") from None
    allowed = {"int": (int,), "float": (int, float), "complex": (int, float, complex)}[kind]
    if type(value) not in allowed:
        raise ValueError(f"input requires {kind}")
    try:
        return finite({"int": int, "float": float, "complex": complex}[kind](value))
    except OverflowError:
        raise ValueError("numeric conversion exceeds finite floating-point range") from None


def divide(a, b, remainder=False):
    if b == 0:
        raise ValueError("division by zero")
    if type(a) is int and type(b) is int:
        quotient = (abs(a) // abs(b)) * (-1 if (a < 0) != (b < 0) else 1)
        return a - quotient * b if remainder else quotient
    return a % b if remainder else a / b


def from_data(value, type_):
    if type_.array:
        return tuple(from_data(item, type_.element) for item in value)
    return convert(value, "complex") if type_.name == "complex" else value
