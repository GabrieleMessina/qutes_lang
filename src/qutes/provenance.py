"""Backend-independent presentation data; never an execution instruction."""
from dataclasses import dataclass
import re

from qutes.diagnostics import Span


@dataclass(frozen=True)
class Region:
    id: int
    parent: int | None
    kind: str
    label: str
    operation_start: int
    operation_end: int
    span: Span


@dataclass(frozen=True)
class SourceMapping:
    name: str
    bits: tuple[int, ...]
    classical: bool
    operation_start: int
    operation_end: int
    context: str
    span: Span


@dataclass(frozen=True)
class Register:
    name: str
    bits: tuple[int, ...]
    classical: bool = False


def expression_kind(expression):
    if expression.presentation:
        return expression.presentation
    op = expression.op
    if op in {"binary:==", "binary:!=", "binary:<", "binary:<=", "binary:>", "binary:>="}:
        return "compare"
    if op in {"binary:&&", "binary:||", "unary:!"}:
        return "boolean"
    return {"binary:+": "add", "rotateLeft": "rotate", "rotateRight": "rotate", "search": "search"}.get(op)


def registers(allocations, mappings, classical_count):
    """Partition existing wires without changing their order or adding aliases."""
    result, used = [], set()

    def add(name, bits, classical=False):
        if not bits:
            return
        name = name.replace("$comparison", "comparison_work").replace("$", "")
        base = re.sub(r"[^A-Za-z0-9_]", "_", name).strip("_") or "temporary"
        if not base[0].isalpha():
            base = "value_" + base
        candidate, suffix = base, 2
        while candidate in used:
            candidate = f"{base}_{suffix}"
            suffix += 1
        used.add(candidate)
        result.append(Register(candidate, tuple(bits), classical))

    for allocation in allocations:
        name = allocation.name
        if name.startswith("$"):
            candidates = [m for m in mappings if not m.classical and not m.name.startswith("$")
                          and m.bits and set(m.bits) <= set(allocation.bits)]
            if candidates:
                name = min(candidates, key=lambda m: (bool(m.context), m.operation_start)).name
        private = set(allocation.retained_index_bits + allocation.scratch_bits)
        add(name, [b for b in allocation.bits if b not in private])
        add(name + "_index", allocation.retained_index_bits)
        add(name + "_work", allocation.scratch_bits)
    # Name contiguous snapshot groups; aliases never duplicate physical bits.
    bit = 0
    while bit < classical_count:
        candidates = [m for m in mappings if m.classical and m.bits and m.bits[0] == bit
                      and m.bits == tuple(range(bit, bit + len(m.bits)))]
        chosen = min(candidates, key=lambda m: (m.name.startswith("$"), bool(m.context), m.operation_start)) if candidates else None
        bits = chosen.bits if chosen else (bit,)
        add(chosen.name if chosen else f"snapshot_{bit + 1}", bits, True)
        bit += len(bits)
    return tuple(result)


def cleanup_annotations(program):
    return tuple({"name": event.name, "operation_start": event.operation_start,
                  "operation_end": event.operation_end,
                  "zero_bits": program.allocations[event.storage].bits,
                  "restored_bits": tuple(sorted({bit for version in event.restored_inputs
                      for bit in program.allocations[version.storage].bits}))}
                 for event in program.cleanup_events)
