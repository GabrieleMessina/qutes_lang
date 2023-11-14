from qiskit import QuantumRegister as qr

class QuantumRegister(qr):
    def __init__(self, size, var_name, value):
        super().__init__(size, var_name)
        self.value = value