"""Create an executable physical view without mutating logical construction."""
from collections import defaultdict
from dataclasses import replace
from itertools import chain

from qutes.provenance import Register
from qutes.wires import allocate, remap, quantum_bits
from qutes.diagnostics import DiagnosticError


def physical_registers(registers, allocation):
    if not allocation.enabled:
        return registers
    owners = defaultdict(set)
    for interval in allocation.intervals:
        owners[interval.physical].add(interval.logical)
    names = {bit: (register, index) for register in registers if not register.classical
             for index, bit in enumerate(register.bits)}
    classical = tuple(register for register in registers if register.classical)
    used = {register.name for register in classical}
    result = []
    bit = 0
    while bit < allocation.physical_count:
        bits = [bit]
        if len(owners[bit]) != 1:
            base = f"work_{bit + 1}"
        else:
            logical = next(iter(owners[bit]))
            register, index = names[logical]
            # Retain whole exclusive source registers where physical order allows.
            end = bit + 1
            while (end < allocation.physical_count and len(owners[end]) == 1
                   and names[next(iter(owners[end]))] == (register, index + end - bit)):
                bits.append(end)
                end += 1
            base = register.name if index == 0 and len(bits) == len(register.bits) else f"{register.name}_{index}"
        name, suffix = base, 2
        while name in used:
            name = f"{base}_{suffix}"
            suffix += 1
        used.add(name)
        result.append(Register(name, tuple(bits)))
        bit += len(bits)
    return tuple(result) + classical


def physical_program(logical):
    workspace = {bit for storage in logical.allocations for bit in storage.scratch_bits}
    live = tuple(bit for storage in logical.allocations if not storage.released
                 for bit in storage.bits if bit not in workspace)
    # A scheduled no-op can still reference a wide value. Bound lifetime/proof
    # materialization independently of the later elementary backend expansion.
    work = 0
    sizes = chain((len(live),), (len(quantum_bits(op)) for op in logical.operations),
                  (len(proof.bits) for proof in logical.zero_certificates))
    for size in sizes:
        work += size
        if work > logical.config.max_evaluation_steps:
            raise DiagnosticError("Q4001", "wire allocation references exceed the construction budget",
                                  logical.allocations[0].span)
    allocation = allocate(logical.operations, logical.qubit_count, logical.zero_certificates,
                          live, enabled=logical.config.wire_reuse)
    return replace(logical, operations=remap(logical.operations, allocation),
                   qubit_count=allocation.physical_count,
                   registers=physical_registers(logical.registers, allocation),
                   logical_program=logical, wire_allocation=allocation)


def handoffs(program):
    allocation = program.wire_allocation
    if allocation is None or not allocation.enabled:
        return ()
    names = {bit: f"{register.name}[{index}]" for register in program.logical_program.registers
             if not register.classical for index, bit in enumerate(register.bits)}
    previous, result = {}, []
    for interval in allocation.intervals:
        old = previous.get(interval.physical)
        if old is not None:
            result.append({"physical": interval.physical, "operation": interval.start,
                           "from_logical": old.logical, "to_logical": interval.logical,
                           "from_epoch": old.epoch, "to_epoch": interval.epoch,
                           "certificate": old.certificate, "name": names[interval.logical]})
        previous[interval.physical] = interval
    return tuple(result)
