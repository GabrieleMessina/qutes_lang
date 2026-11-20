"""Sparse, reversible basis-state preparation with no reset or hidden index."""

from dataclasses import dataclass
import cmath
import math

from qutes.gates import Gate
from qutes.numeric import convert
from qutes.values import SignedInteger


@dataclass(frozen=True)
class PreparedState:
    values: tuple[int | bool, ...]
    amplitudes: tuple[complex, ...]


def validate(values, weights, kind, type_, width):
    values = tuple(values)
    if not values:
        raise ValueError("superposition requires a nonempty basis-value list")
    if len(set(values)) != len(values):
        raise ValueError("superposition basis values must be distinct")
    for value in values:
        if type_.name == "quint":
            SignedInteger(width).encode(value)
        elif type(value) is not bool:
            raise ValueError("qubit preparation requires Boolean basis values")
    if weights is None:
        amplitudes = (complex(1/math.sqrt(len(values))),) * len(values)
    else:
        if len(weights) != len(values):
            raise ValueError("preparation weights must match the basis-value list length")
        if kind == "probabilities":
            probabilities = tuple(convert(w, "float") for w in weights)
            if any(p < 0 for p in probabilities):
                raise ValueError("probabilities must be nonnegative")
            try:
                total = math.fsum(probabilities)
            except OverflowError:
                total = math.inf
            if not math.isfinite(total) or abs(total-1) > 1e-12:
                raise ValueError("probabilities must sum to one (tolerance 1e-12)")
            amplitudes = tuple(complex(math.sqrt(p/total)) for p in probabilities)
        else:
            amplitudes = tuple(convert(w, "complex") for w in weights)
            norm = math.hypot(*(part for a in amplitudes for part in (a.real, a.imag)))
            if not math.isfinite(norm) or abs(norm*norm-1) > 1e-12:
                raise ValueError("squared amplitude magnitudes must sum to one (tolerance 1e-12)")
            amplitudes = tuple(a/norm for a in amplitudes)
    return PreparedState(values, amplitudes)


def work_bound(state, width):
    # Prefix rotations and leaf phases carry up to width controls each.
    return max(1, len(state.values)) * (width*width + 5*width)


def gates(state, bits, span):
    width = len(bits)
    rows = tuple((int(v) % (1 << width), a) for v, a in zip(state.values, state.amplitudes, strict=True) if a != 0)
    pending, result = [(width-1, (), rows)], []
    while pending:
        bit, controls, entries = pending.pop()
        if bit < 0:
            continue
        zero = tuple(row for row in entries if not (row[0] >> bit) & 1)
        one = tuple(row for row in entries if (row[0] >> bit) & 1)
        n0 = math.hypot(*(abs(a) for _, a in zero))
        n1 = math.hypot(*(abs(a) for _, a in one))
        angle = 2*math.atan2(n1, n0)
        if angle:
            result.append(Gate("ry", (bits[bit],), controls=controls, angle=angle, span=span))
        if one:
            pending.append((bit-1, (*controls, (bits[bit], True)), one))
        if zero:
            pending.append((bit-1, (*controls, (bits[bit], False)), zero))
    for encoded, amplitude in rows:
        angle = cmath.phase(amplitude)
        if not angle:
            continue
        controls = tuple((bits[i], bool((encoded >> i) & 1)) for i in range(1, width))
        if not encoded & 1:
            result.append(Gate("x", (bits[0],), span=span))
        result.append(Gate("phase", (bits[0],), controls=controls, angle=angle, span=span))
        if not encoded & 1:
            result.append(Gate("x", (bits[0],), span=span))
    return tuple(result)
