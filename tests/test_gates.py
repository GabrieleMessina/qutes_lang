import numpy as np
import pytest
from qiskit.quantum_info import Operator, Statevector

from qutes.gates import Gate, controlled, inverse
from qutes.qiskit_backend import emit_gates
from tests.reference import field, permutation, random_state, replace_field

pytestmark = pytest.mark.backend


@pytest.mark.parametrize("width", [1, 2, 3, 4])
@pytest.mark.parametrize("amount", [-3, -1, 0, 1, 5])
def test_constant_arithmetic_full_operator(width, amount):
    operation = Gate("add_constant", tuple(range(width)), amount=amount)
    matrix = Operator(emit_gates(width, (operation,))).data
    expected = np.zeros_like(matrix)
    for index in range(2**width):
        expected[(index + amount) % (2**width), index] = 1
    np.testing.assert_allclose(matrix, expected, atol=1e-10)
    identity = Operator(emit_gates(width, (operation, *inverse((operation,))))).data
    np.testing.assert_allclose(identity, np.eye(2**width), atol=1e-10)


@pytest.mark.parametrize("control_value", [False, True])
@pytest.mark.parametrize("inverse_operation", [False, True])
def test_controlled_addition_on_complex_entangled_state(control_value, inverse_operation):
    operation = Gate("add", (3, 4), (1, 2), controls=((0, control_value),), inverse=inverse_operation)
    source = random_state(6)

    def transform(index):
        if bool(index & 1) != control_value:
            return index
        amount = field(index, 1, 2) * (-1 if inverse_operation else 1)
        return replace_field(index, 3, 2, (field(index, 3, 2) + amount) % 4)
    actual = Statevector(source).evolve(emit_gates(6, (operation,))).data
    np.testing.assert_allclose(actual, permutation(source, transform), atol=1e-10)


@pytest.mark.parametrize("control_value", [False, True])
@pytest.mark.parametrize("inverse_operation", [False, True])
def test_addition_control_may_also_be_a_source_bit(control_value, inverse_operation):
    operation = Gate("add", (2, 3), (0, 1), controls=((1, control_value),), inverse=inverse_operation)
    source = random_state(5)

    def transform(index):
        if bool(index & 2) != control_value:
            return index
        amount = field(index, 0, 2) * (-1 if inverse_operation else 1)
        return replace_field(index, 2, 2, (field(index, 2, 2) + amount) % 4)
    actual = Statevector(source).evolve(emit_gates(5, (operation,))).data
    np.testing.assert_allclose(actual, permutation(source, transform), atol=1e-10)


@pytest.mark.parametrize("count", [0, 1, 2, 5])
def test_controlled_rotation_and_inverse(count):
    operation = Gate("rotate", (0, 1, 2), amount=count, controls=((3, False),))
    source = random_state(5)

    def transform(index):
        if index & 8:
            return index
        bits = [(index >> bit) & 1 for bit in range(3)]
        rotated = sum(value << ((position + count) % 3) for position, value in enumerate(bits))
        return replace_field(index, 0, 3, rotated)
    actual = Statevector(source).evolve(emit_gates(5, (operation,))).data
    np.testing.assert_allclose(actual, permutation(source, transform), atol=1e-10)
    restored = Statevector(actual).evolve(emit_gates(5, (operation.adjoint(),))).data
    np.testing.assert_allclose(restored, source, atol=1e-10)


def test_normalize_repeated_and_impossible_controls():
    gate = Gate("x", (2,), controls=((0, True),))
    assert controlled(gate, ((0, True), (1, False))).controls == ((0, True), (1, False))
    assert controlled(gate, ((0, False),)) is None


def test_copy_with_source_also_a_control_is_exact():
    gate = Gate("copy", (2, 3), (0, 1), controls=((0, False),))
    source = random_state(4)
    actual = Statevector(source).evolve(emit_gates(4, (gate,))).data
    np.testing.assert_allclose(actual, permutation(source, lambda i: i if i & 1 else i ^ ((i & 3) << 2)), atol=1e-10)
