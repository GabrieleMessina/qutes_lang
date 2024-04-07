from qiskit import QuantumRegister as qr
from quantum_circuit.classical_register import ClassicalRegister

class QuantumRegister(qr):
    def __init__(self, size, var_name, bits = None):
        super().__init__(size, var_name, bits)
        self.measured_classical_register:ClassicalRegister | None = None

    def __len__(self):
        return self.size
    