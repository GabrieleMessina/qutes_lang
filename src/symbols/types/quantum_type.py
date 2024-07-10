from symbols.types import Qubit

class QuantumType:
    default_value = [Qubit(complex(1),complex(0))]
    default_size_in_qubit = 1
    default_superposition_value = [Qubit(complex(0.5),complex(0.5))]

    def __init__(self):
        pass

    def __str__(self) -> str:
        return self.__to_printable__()

    def __repr__(self) -> str:
        return self.__to_printable__()