from qiskit import QuantumRegister as qr
from quantum_circuit.classical_register import ClassicalRegister

class QuantumRegister(qr):
    def __init__(self, size, var_name: str, bits=None):
        super().__init__(size, var_name, bits)
        if not var_name.replace('_', '').isalnum():
            raise RuntimeError(
                f"Quantum register names must be valid identifiers, but '{var_name}' is not. Valid identifiers contain only alphanumeric letters (a-z and A-Z), decimal digits (0-9), or underscores (_).")
        self.measured_classical_register: ClassicalRegister | None = None
        self.is_anonymous: bool = False

    def __len__(self):
        return self.size

    def __repr__(self):
        """Return the official string representing the register."""
        self._repr = f"{self.__class__.__qualname__}({self.size}, '{self.name}'):{object.__repr__(self)}"
        # return f"{self.__class__.__qualname__}({self.size}, '{self.name}')"
        return self._repr

    def __hash__(self):
        """Make object hashable, based on the name and size to hash."""
        self._hash = hash((type(self), self._name, self._size))
        # self._hash = hash(self._name, self._size))
        return self._hash