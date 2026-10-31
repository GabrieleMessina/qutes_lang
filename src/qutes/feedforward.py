"""Convert typed snapshot values to backend-independent classical predicates."""

from __future__ import annotations

from qutes import classical as c
from qutes.values import TextEncoding


def integer_bits(value, width):
    if value.op == "literal":
        return tuple(c.literal(bool((value.value >> i) & 1)) for i in range(width))
    bits = tuple(c.Predicate("bit", value=bit) for bit in value.bits)
    return bits + (bits[-1],) * (width - len(bits))


def text_bits(value, alphabet, capacity):
    if value.op == "snapshot":
        return tuple(c.Predicate("bit", value=bit) for bit in value.bits)
    codec = TextEncoding(alphabet, capacity)
    if value.type.name == "char":
        codes = (codec.encode_character(value.value),)
    else:
        codes = codec.encode_string(value.value).codes
    return tuple(c.literal(bool((code >> i) & 1)) for code in codes for i in range(codec.bits_per_character))


def predicate(value) -> c.Predicate:
    if value.op == "literal":
        return c.literal(value.value)
    if value.op == "snapshot":
        if value.type.name != "bool" or len(value.bits) != 1:
            raise ValueError("a scalar measurement predicate must be Boolean")
        return c.Predicate("bit", value=value.bits[0])
    if value.op == "unary:!":
        return c.invert(predicate(value.arguments[0]))
    if not value.op.startswith("binary:"):
        raise ValueError(f"unsupported feedforward predicate {value.op}")
    op = value.op[7:]
    a, b = value.arguments
    if op in {"&&", "||"}:
        return c.combine("and" if op == "&&" else "or", predicate(a), predicate(b))
    if a.type.name == "bool":
        result = c.invert(c.combine("xor", predicate(a), predicate(b)))
        return c.invert(result) if op == "!=" else result
    if a.type.name == "int":
        widths = [len(item.bits) if item.op == "snapshot" else max(1, (item.value if item.value >= 0 else ~item.value).bit_length() + 1)
                  for item in (a, b)]
        width = max(widths)
        return c.compare(integer_bits(a, width), integer_bits(b, width), op, signed=True)
    if a.type.name in {"char", "string"}:
        if a.op == b.op == "literal":
            return c.literal((a.value == b.value) if op == "==" else (a.value != b.value))
        snapshot = a if a.op == "snapshot" else b
        if a.type.name == "string":
            lengths = [item.length if item.op == "snapshot" else len(item.value) for item in (a, b)]
            if lengths[0] != lengths[1]:
                return c.literal(op == "!=")
        try:
            a_bits = text_bits(a, snapshot.alphabet, snapshot.capacity)
            b_bits = text_bits(b, snapshot.alphabet, snapshot.capacity)
        except ValueError:
            # An arbitrary classical literal may be outside the quantum alphabet.
            # It cannot equal a valid measured value; it is not a quantum cast.
            return c.literal(op == "!=")
        return c.compare(a_bits, b_bits, op)
    raise ValueError(f"unsupported feedforward comparison for {a.type}")
