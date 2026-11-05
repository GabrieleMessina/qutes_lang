"""Certified-zero lifetime analysis and fixed-order physical wire allocation.

This pass never infers zero from last use, measurement, or source scope. Proofs
come from successful cleanup/preparation transactions. Reconstructed values get
new intervals; their logical identity is unchanged. No backend is imported.
"""
from dataclasses import dataclass, replace
from collections import defaultdict
from bisect import bisect_right
import heapq

from qutes.gates import Measurement


def quantum_bits(operation):
    return operation.qubits if isinstance(operation, Measurement) else operation.bits


@dataclass(frozen=True)
class ZeroCertificate:
    bits: tuple[int, ...]
    boundary: int
    operation_start: int
    reason: str


@dataclass(frozen=True)
class Lifetime:
    logical: int
    epoch: int
    start: int
    end: int
    certificate: int | None
    physical: int = -1


@dataclass(frozen=True)
class WireAllocation:
    logical_count: int
    physical_count: int
    operation_count: int
    intervals: tuple[Lifetime, ...]
    certificates: tuple[ZeroCertificate, ...]
    enabled: bool

    def lookup(self):
        return WireLookup(self)


class WireLookup:
    def __init__(self, allocation):
        self.by_bit = defaultdict(list)
        for interval in allocation.intervals:
            self.by_bit[interval.logical].append(interval)
        self.starts = {bit: [item.start for item in items] for bit, items in self.by_bit.items()}

    def at(self, bit, operation):
        items = self.by_bit.get(bit, ())
        index = bisect_right(self.starts.get(bit, ()), operation) - 1
        if index >= 0 and operation < items[index].end:
            return items[index].physical
        raise ValueError(f"logical wire {bit} has no lifetime at operation {operation}")

    def ending(self, bit, boundary):
        """An annotation belongs to the outgoing owner, never its successor."""
        items = self.by_bit.get(bit, ())
        index = bisect_right(self.starts.get(bit, ()), boundary - 1) - 1
        if index >= 0 and boundary <= items[index].end:
            return items[index].physical
        return None


def lifetimes(operations, logical_count, certificates, live_bits, *, initial_bits=()):
    """Half-open gate-index intervals; operation_count denotes final live state."""
    stop = len(operations)
    uses = defaultdict(list)
    for index, operation in enumerate(operations):
        for bit in quantum_bits(operation):
            uses[bit].append(index)
    for bit in initial_bits:
        uses[bit].insert(0, 0)
    for bit in live_bits:
        uses[bit].append(stop)
    boundaries = defaultdict(dict)
    for index, proof in enumerate(certificates):
        if not 0 <= proof.operation_start <= proof.boundary <= stop:
            raise ValueError("invalid zero certificate boundary")
        for bit in proof.bits:
            if not 0 <= bit < logical_count:
                raise ValueError("zero certificate refers to unknown logical wire")
            boundaries[bit].setdefault(proof.boundary, index)
    result = []
    for bit, positions in sorted(uses.items()):
        if not 0 <= bit < logical_count:
            raise ValueError("operation refers to unknown logical wire")
        ends = sorted(boundaries[bit])
        epoch = 0
        current = None
        for position in positions:
            if current is not None and position < current.end:
                continue
            successor = bisect_right(ends, position)
            end = ends[successor] if successor < len(ends) else stop + 1
            current = Lifetime(bit, epoch, position, end, boundaries[bit].get(end))
            result.append(current)
            epoch += 1
    return tuple(sorted(result, key=lambda item: (item.start, item.logical, item.epoch)))


def allocate(operations, logical_count, certificates, live_bits, *, enabled=True, initial_bits=()):
    intervals = lifetimes(operations, logical_count, certificates, live_bits, initial_bits=initial_bits)
    active, free, assigned = [], [], []
    width = 0
    for interval in intervals:
        while active and active[0][0] <= interval.start:
            _, physical = heapq.heappop(active)
            heapq.heappush(free, physical)
        if not enabled:
            physical = interval.logical
        elif free:
            physical = heapq.heappop(free)
        else:
            physical = width
            width += 1
        assigned.append(replace(interval, physical=physical))
        if enabled:
            heapq.heappush(active, (interval.end, physical))
    allocation = WireAllocation(logical_count, width if enabled else logical_count,
                                len(operations), tuple(assigned), tuple(certificates), enabled)
    verify(allocation, operations, live_bits, initial_bits=initial_bits)
    return allocation


def verify(allocation, operations, live_bits, *, initial_bits=()):
    """Check coverage, certified handoffs and collisions independently of the heap."""
    expected = lifetimes(operations, allocation.logical_count, allocation.certificates,
                         live_bits, initial_bits=initial_bits)
    if tuple(replace(item, physical=-1) for item in allocation.intervals) != expected:
        raise ValueError("allocation does not cover the certified logical lifetimes")
    physical = defaultdict(list)
    for interval in allocation.intervals:
        if not 0 <= interval.physical < allocation.physical_count:
            raise ValueError("allocation refers to unknown physical wire")
        physical[interval.physical].append(interval)
    for intervals in physical.values():
        previous = None
        for interval in sorted(intervals, key=lambda item: item.start):
            if previous is not None:
                if previous.end > interval.start:
                    raise ValueError("overlapping lifetimes share a physical wire")
                if previous.certificate is None:
                    raise ValueError("wire handoff has no zero certificate")
            previous = interval
    lookup = allocation.lookup()
    for index, operation in enumerate(operations):
        mapped = [lookup.at(bit, index) for bit in quantum_bits(operation)]
        if len(set(mapped)) != len(mapped):
            raise ValueError("distinct operation operands share a physical wire")


def remap(operations, allocation):
    lookup = allocation.lookup()
    result = []
    for index, operation in enumerate(operations):
        def bits(values):
            return tuple(lookup.at(bit, index) for bit in values)
        if isinstance(operation, Measurement):
            result.append(replace(operation, qubits=bits(operation.qubits)))
        else:
            result.append(replace(operation, targets=bits(operation.targets), inputs=bits(operation.inputs),
                                  controls=tuple((lookup.at(bit, index), value) for bit, value in operation.controls)))
    return tuple(result)
