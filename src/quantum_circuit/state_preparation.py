from typing import Union, Optional
from qiskit.circuit.library import StatePreparation as QiskitStatePreparation
from qiskit.quantum_info import Statevector

class StatePreparation(QiskitStatePreparation):
    def __init__(
        self,
        params: Union[str, list, int, Statevector],
        num_qubits: Optional[int] = None,
        inverse: bool = False,
        label: Optional[str] = None,
        normalize: bool = True,
    ):
        super().__init__(params, num_qubits, inverse, label, normalize)

    def __len__(self):
        return self.num_qubits
    
    def __to_printable__(self) -> str:
        return f"{self.params}"

    def __str__(self) -> str:
        return self.__to_printable__()

    def __repr__(self) -> str:
        return self.__to_printable__()