"""Central source-language vocabulary; working builtin names have no aliases."""

from enum import StrEnum


class Builtin(StrEnum):
    SUPERPOSITION = "superposition"
    MEASURE = "measure"
    ROTATE_LEFT = "rotateLeft"
    ROTATE_RIGHT = "rotateRight"
    SEARCH = "search"
    COPY = "copy"
    COMPLEX = "complex"
    HADAMARD = "hadamard"
    NOT = "not"
    PHASE_FLIP = "phaseFlip"
    PHASE = "phase"
    SWAP = "swap"


CLASSICAL_TYPES = frozenset({"bool", "int", "float", "complex", "char", "string", "void"})
QUANTUM_TYPES = frozenset({"qubit", "quint", "quchar", "qustring"})
TYPES = CLASSICAL_TYPES | QUANTUM_TYPES
KEYWORDS = TYPES | frozenset(
    {"if", "else", "while", "for", "foreach", "in", "return", "new", "true", "false", "input", "readonly", "mut"}
)
