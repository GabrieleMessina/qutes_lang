"""Conservative signed basis support, independent of circuits and simulation.

Finite sets are capped at 256 entries; larger results become enclosing intervals.
No probability threshold or sampling participates in a bounds proof.
"""

from dataclasses import dataclass

LIMIT = 256


def work(*supports):
    cost = 1
    for item in supports:
        cost *= len(item.values) if item.values is not None else 1
    return min(LIMIT, cost)


@dataclass(frozen=True)
class Support:
    lower: int
    upper: int
    values: tuple[int, ...] | None = None


def full(width):
    bound = 1 << (width - 1)
    return Support(-bound, bound - 1)


def finite(values):
    values = tuple(sorted(set(values)))
    if not values:
        raise ValueError("basis support cannot be empty")
    return Support(values[0], values[-1], values if len(values) <= LIMIT else None)


def join(a, b):
    if a.values is not None and b.values is not None:
        return finite((*a.values, *b.values))
    return Support(min(a.lower, b.lower), max(a.upper, b.upper))


def wrap(value, width):
    bound = 1 << (width - 1)
    return (value + bound) % (2 * bound) - bound


def interval(lower, upper, width):
    bound = 1 << (width - 1)
    if (lower + bound) // (2 * bound) != (upper + bound) // (2 * bound):
        return full(width)
    return Support(wrap(lower, width), wrap(upper, width))


def arithmetic(a, b, operator, width):
    if a.values is not None and b.values is not None and len(a.values) * len(b.values) <= LIMIT:
        return finite(wrap(x+y if operator == "+" else x-y, width) for x in a.values for y in b.values)
    return interval(a.lower+b.lower, a.upper+b.upper, width) if operator == "+" else interval(a.lower-b.upper, a.upper-b.lower, width)


def negate(a, width):
    return finite(wrap(-x, width) for x in a.values) if a.values is not None else interval(-a.upper, -a.lower, width)


def rotate(a, count, width):
    if a.values is None:
        return full(width)
    count %= width
    mask = (1 << width) - 1
    return finite(wrap(((x & mask) << count | (x & mask) >> (width-count)) & mask, width) for x in a.values)
