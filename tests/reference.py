"""Small independent semantic oracle: integer permutations and projectors.

No Qiskit imports, compiler arithmetic, or backend gate helpers are permitted here.
This is a test oracle, not a source-language evaluator or production simulator.
"""

from dataclasses import dataclass
from typing import Callable

import numpy as np
from numpy.typing import NDArray

State = NDArray[np.complex128]


def field(index: int, start: int, width: int) -> int:
    return (index >> start) & ((1 << width) - 1)


def replace_field(index: int, start: int, width: int, value: int) -> int:
    mask = ((1 << width) - 1) << start
    return (index & ~mask) | (value << start)


def permutation(state: State, transform: Callable[[int], int]) -> State:
    destinations = [transform(index) for index in range(len(state))]
    if sorted(destinations) != list(range(len(state))):
        raise ValueError("reference transform is not a reversible permutation")
    result = np.empty_like(state)
    result[destinations] = state
    return result


def constant_sum(state: State, start: int, width: int, amount: int) -> State:
    modulus = 2**width
    return permutation(state, lambda index: replace_field(
        index, start, width, (field(index, start, width) + amount) % modulus,
    ))


def register_sum(state: State, source: int, target: int, width: int) -> State:
    return permutation(state, lambda index: replace_field(
        index, target, width,
        (field(index, source, width) + field(index, target, width)) % (2**width),
    ))


def rotation(state: State, start: int, width: int, count: int) -> State:
    # Deliberately use bit-list rearrangement, independently of integer codec logic.
    def transform(index: int) -> int:
        bits = [(index >> (start + bit)) & 1 for bit in range(width)]
        value = sum(bit << ((position + count) % width) for position, bit in enumerate(bits))
        return replace_field(index, start, width, value)
    return permutation(state, transform)


def random_state(qubits: int, seed: int = 41) -> State:
    generator = np.random.default_rng(seed)
    state = generator.normal(size=2**qubits) + 1j * generator.normal(size=2**qubits)
    return state / np.linalg.norm(state)


@dataclass(frozen=True)
class Branch:
    probability: float
    state: State
    snapshots: tuple[int, ...] = ()


def measure(branch: Branch, start: int, width: int) -> list[Branch]:
    results = []
    indices = np.arange(len(branch.state))
    for outcome in range(2**width):
        mask = ((indices >> start) & (2**width - 1)) == outcome
        projected = np.where(mask, branch.state, 0)
        probability = float(np.vdot(projected, projected).real)
        if probability > 1e-14:
            results.append(Branch(
                branch.probability * probability,
                projected / np.sqrt(probability),
                branch.snapshots + (outcome,),
            ))
    return results
