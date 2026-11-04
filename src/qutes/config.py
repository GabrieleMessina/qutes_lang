"""Validated build settings, independent of Qiskit and source parsing."""

from dataclasses import asdict, dataclass, fields
from pathlib import Path
from typing import Any, Mapping
import math
import tomllib


def validate_alphabet(alphabet: str) -> None:
    if not isinstance(alphabet, str) or len(alphabet) < 2:
        raise ValueError("alphabet must contain at least two characters")
    if len(set(alphabet)) != len(alphabet):
        raise ValueError("alphabet characters must be distinct")
    if any(0xD800 <= ord(character) <= 0xDFFF for character in alphabet):
        raise ValueError("alphabet entries must be Unicode scalar values")


@dataclass(frozen=True)
class CompilerConfig:
    quint_bits: int = 8
    alphabet: str = "".join(chr(code) for code in range(128))
    qustring_capacity: int = 2
    max_simulation_qubits: int = 24
    max_simulation_shots: int = 1_000_000
    max_loop_iterations: int = 10_000
    max_evaluation_steps: int = 100_000
    max_classical_bits: int = 65_536
    search_failure_probability: float = 0.01

    def __post_init__(self) -> None:
        for name in (
            "quint_bits", "qustring_capacity", "max_simulation_qubits", "max_simulation_shots",
            "max_loop_iterations", "max_evaluation_steps", "max_classical_bits",
        ):
            value = getattr(self, name)
            if type(value) is not int or value < 1:
                raise ValueError(f"{name} must be a positive integer")
        validate_alphabet(self.alphabet)
        failure = self.search_failure_probability
        if type(failure) not in (int, float) or not math.isfinite(failure) or not 0 < failure < 1:
            raise ValueError("search_failure_probability must be finite and strictly between zero and one")

    @property
    def quchar_bits(self) -> int:
        return (len(self.alphabet) - 1).bit_length()

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def resolve(
        cls,
        project: Mapping[str, Any] | None = None,
        overrides: Mapping[str, Any] | None = None,
    ) -> "CompilerConfig":
        values: dict[str, Any] = {}
        valid = {field.name for field in fields(cls)}
        for layer in (project, overrides):
            if layer is not None:
                unknown = set(layer) - valid
                if unknown:
                    raise ValueError(f"unknown settings: {', '.join(sorted(unknown))}")
                values.update(layer)
        return cls(**values)

    @classmethod
    def load(
        cls, path: Path, overrides: Mapping[str, Any] | None = None,
    ) -> "CompilerConfig":
        with path.open("rb") as source:
            document = tomllib.load(source)
        if set(document) != {"qutes"} or not isinstance(document["qutes"], dict):
            raise ValueError("configuration must contain exactly one [qutes] table")
        return cls.resolve(document["qutes"], overrides)
