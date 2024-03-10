from qiskit import QuantumRegister as qr

class QuantumRegister(qr):
    def __init__(self, size, var_name, value, bits = None):
        super().__init__(size, var_name, bits)
        self.value = value

    def __len__(self):
        return self.size
    