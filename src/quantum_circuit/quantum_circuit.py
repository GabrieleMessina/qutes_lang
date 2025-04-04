from qiskit import QuantumCircuit as qc

class QuantumCircuit(qc):
    def __init__(self, *regs, name=None):
        super().__init__(*regs, name=name)
    def __repr__(self):
        """Return the official string representing the register."""
        self._repr = f"{self.__class__.__qualname__} {self.name}(qubits: {self.num_qubits}, clbits: {self.num_clbits})"
        return self._repr