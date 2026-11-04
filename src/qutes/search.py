"""Backend-independent fixed-point search schedules and index preparation.

Yoder, Low, Chuang, arXiv:1409.3305, equations (5), (6), (7), (10).
The mark phase is +beta and the preparation reflection phase is -alpha.
"""
import math
from qutes.gates import Gate


def schedule(count, failure, budget):
    if count == 1:
        return ()
    a = math.acosh(1 / math.sqrt(failure))
    denominator = math.atanh(1 / math.sqrt(count))
    estimate = a / denominator
    if not math.isfinite(estimate) or estimate > budget:
        raise ValueError("search amplification exceeds the construction budget")
    length = max(1, math.ceil(estimate))
    length += not (length % 2)
    while math.tanh(a / length)**2 > 1 / count:
        length += 2
    if length > budget:
        raise ValueError("search amplification exceeds the construction budget")
    alpha = [2 * math.atan2(1, math.tan(2 * math.pi * j / length) * math.tanh(a / length))
             for j in range(1, (length + 1) // 2)]
    return tuple(zip(alpha, (-x for x in reversed(alpha))))


def uniform_index(bits, count, span):
    """Prepare exactly the first count basis indices, without padded candidates."""
    gates = []

    def visit(level, start, size, controls):
        if level < 0:
            return
        half = 1 << level
        zeros, ones = min(size, half), max(0, size - half)
        angle = 2 * math.atan2(math.sqrt(ones), math.sqrt(zeros))
        if angle:
            gates.append(Gate("ry", (bits[level],), controls=controls, angle=angle, span=span))
        if zeros:
            visit(level - 1, start, zeros, (*controls, (bits[level], False)))
        if ones:
            visit(level - 1, start + half, ones, (*controls, (bits[level], True)))

    visit(len(bits) - 1, 0, count, ())
    return tuple(gates)
