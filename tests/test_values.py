import pytest

from qutes.config import CompilerConfig
from qutes.values import EncodedString, SignedInteger, TextEncoding


@pytest.mark.parametrize("width", range(1, 6))
def test_signed_arithmetic_exhaustive(width):
    integer = SignedInteger(width)
    lower, upper = -(2 ** (width - 1)), 2 ** (width - 1) - 1
    for a in range(lower, upper + 1):
        assert integer.decode(integer.encode(a)) == a
        for b in range(lower, upper + 1):
            expected = ((a + b - lower) % (2**width)) + lower
            assert integer.add(a, b) == expected


@pytest.mark.parametrize("width", range(1, 6))
def test_rotation_exhaustive(width):
    integer = SignedInteger(width)
    for value in range(integer.minimum, integer.maximum + 1):
        for count in range(2 * width + 1):
            bits = format(value % (2**width), f"0{width}b")
            step = count % width
            rotated = bits[step:] + bits[:step]
            expected = int(rotated, 2)
            if rotated[0] == "1":
                expected -= 2**width
            assert integer.rotate_left(value, count) == expected
            assert integer.rotate_right(expected, count) == value


@pytest.mark.parametrize("value", [-129, 128, True, 1.5])
def test_invalid_integer_initializers(value):
    with pytest.raises(ValueError):
        SignedInteger(8).encode(value)


def test_invalid_width_bits_and_rotation():
    for width in [0, -1, True]:
        with pytest.raises(ValueError):
            SignedInteger(width)
    for bits in [-1, 256, False]:
        with pytest.raises(ValueError):
            SignedInteger(8).decode(bits)
    for count in [-1, True, 1.5]:
        with pytest.raises(ValueError):
            SignedInteger(8).rotate_left(1, count)
        with pytest.raises(ValueError):
            SignedInteger(8).rotate_right(1, count)


def test_non_power_of_two_text_alphabet_and_padding():
    encoding = TextEncoding("ACG", 4)
    assert encoding.bits_per_character == 2
    for value in ["", "A", "AC", "GCAA"]:
        assert encoding.decode_string(encoding.encode_string(value)) == value
    for code in [-1, 3, True]:
        with pytest.raises(ValueError):
            encoding.decode_character(code)
    for value in ["Z", "ACGAC"]:
        with pytest.raises(ValueError):
            encoding.encode_string(value)
    for value in [EncodedString((0, 0), 2), EncodedString((0, 0, 0, 0), 5),
                  EncodedString((0, 1, 0, 0), 1)]:
        with pytest.raises(ValueError):
            encoding.decode_string(value)


def test_unicode_scalar_custom_alphabet():
    encoding = TextEncoding("αβ😀", 2)
    assert encoding.decode_string(encoding.encode_string("😀α")) == "😀α"
    for alphabet in ["", "A", "AA", "A\ud800"]:
        with pytest.raises(ValueError):
            TextEncoding(alphabet, 2)


def test_config_precedence_validation_and_toml(tmp_path):
    config = CompilerConfig.resolve({"quint_bits": 4}, {"quint_bits": 3, "alphabet": "ACG"})
    assert config.quint_bits == 3
    assert config.quchar_bits == 2
    assert config.qustring_capacity == 2
    project = tmp_path / "qutes.toml"
    project.write_text('[qutes]\nquint_bits = 4\nalphabet = "ACGT"\n', encoding="utf-8")
    assert CompilerConfig.load(project, {"quint_bits": 2}).quint_bits == 2
    for settings in [{"quint_bits": 0}, {"quint_bits": True}, {"unknown": 1}, {"alphabet": "AA"}]:
        with pytest.raises(ValueError):
            CompilerConfig.resolve(settings)
    project.write_text('[other]\nquint_bits = 4\n', encoding="utf-8")
    with pytest.raises(ValueError):
        CompilerConfig.load(project)
