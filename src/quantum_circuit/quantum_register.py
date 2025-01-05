from qiskit import QuantumRegister as qr
from quantum_circuit.classical_register import ClassicalRegister
from qiskit.circuit.quantumregister import Qubit as QiskitQubit #TODO: move, is used weirdly as import in circuit handler


class QuantumRegister(qr):
    def __init__(self, size, var_name:str, bits = None):
        super().__init__(size, var_name, bits)
        if not var_name.replace('_', '').isalnum():
            raise RuntimeError(f"Quantum register names must be valid identifiers, but '{var_name}' is not. Valid identifiers contain only alphanumeric letters (a-z and A-Z), decimal digits (0-9), or underscores (_).")
        self.measured_classical_register:ClassicalRegister | None = None

    def __len__(self):
        return self.size
