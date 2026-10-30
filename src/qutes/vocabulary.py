"""Central source-language vocabulary; working builtin names have no aliases."""

from enum import StrEnum


class Builtin(StrEnum):
    SUPERPOSITION = "superposition"
    MEASURE = "measure"
    ROTATE_LEFT = "rotateLeft"
    ROTATE_RIGHT = "rotateRight"


CLASSICAL_TYPES = frozenset({"bool", "int", "char", "string", "void"})
QUANTUM_TYPES = frozenset({"qubit", "quint", "quchar", "qustring"})
TYPES = CLASSICAL_TYPES | QUANTUM_TYPES
KEYWORDS = TYPES | frozenset(
    {"if", "else", "while", "for", "foreach", "in", "return", "new", "true", "false"}
)
