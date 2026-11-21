"""Single-shot ideal-state operations for interactive circuit execution."""
import cmath
import math

from qutes.gates import Measurement


def bits(value, wires):
    return sum(((value >> wire) & 1) << index for index, wire in enumerate(wires))


def apply(state, gate):
    target = 1 << gate.targets[0]
    enabled = sum(1 << wire for wire, _ in gate.controls)
    required = sum(1 << wire for wire, value in gate.controls if value)
    kind = gate.kind
    if kind == 'add':
        result = state.copy()
        for i, amplitude in enumerate(state):
            if i & enabled != required:
                continue
            operand = bits(i, gate.inputs)
            before = bits(i, gate.targets)
            after = before + (-operand if gate.inverse else operand)
            changed = before ^ after
            destination = i
            for j, wire in enumerate(gate.targets):
                if changed & (1 << j):
                    destination ^= 1 << wire
            result[destination] = amplitude
        state[:] = result
        return
    for i in range(len(state)):
        if i & enabled != required or i & target:
            continue
        j = i | target
        a, b = state[i], state[j]
        if kind == 'x':
            state[i], state[j] = b, a
        elif kind == 'h':
            state[i], state[j] = (a + b) / math.sqrt(2), (a - b) / math.sqrt(2)
        elif kind == 'phase':
            state[j] = b * cmath.exp(1j * gate.angle)
        elif kind == 'ry':
            c, s = math.cos(gate.angle / 2), math.sin(gate.angle / 2)
            state[i], state[j] = c * a - s * b, s * a + c * b
        elif kind == 'swap':
            other = 1 << gate.targets[1]
            if i & other:
                j ^= other
                state[i], state[j] = state[j], a
        else:
            raise ValueError(f"Unsupported circuit operation {kind}.")


def step(state, operation, gates, memory, rng):
    if isinstance(operation, Measurement):
        for wire, dest in zip(operation.qubits, operation.classical_bits, strict=True):
            mask = 1 << wire
            weights = [0.0, 0.0]
            for i, amplitude in enumerate(state):
                weights[bool(i & mask)] += abs(amplitude) ** 2
            outcome = rng.random() * sum(weights) >= weights[0]
            scale = math.sqrt(weights[outcome])
            for i in range(len(state)):
                state[i] = state[i] / scale if bool(i & mask) == outcome else 0j
            memory = (memory & ~(1 << dest)) | (int(outcome) << dest)
    elif (all(bool(memory & (1 << bit)) == value for bit, value in operation.classical_controls)
          and all(test.evaluate(memory) == value for test, value in operation.conditions)):
        for gate in gates:
            apply(state, gate)
    return memory
