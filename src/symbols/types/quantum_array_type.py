from typing import TypeVar
from symbols.types import QuantumType
from symbols.types.qubit import Qubit
from quantum_circuit.state_preparation import StatePreparation

T = TypeVar("T")

class QuantumArrayType(QuantumType[T]):
    def __init__(self, unit_type: QuantumType[T], array:list[QuantumType]): #array is a list of Symbol
        super().__init__(unit_type, sum([a.size for a in array]))
        self.unit_type = unit_type
        self.array = array
        self.size = sum([a.size for a in array])
        state_preparation = str()
        array_elements_state_preparation = [a.qubit_state._params_arg for a in array]
        for element in array_elements_state_preparation:
            state_preparation = state_preparation + element
        self.qubit_state = StatePreparation(state_preparation)

    def get_default_value():
        return QuantumArrayType(Qubit, [Qubit.get_default_value()])
    
    def get_default_superposition_value():
        return QuantumArrayType(Qubit, [Qubit.get_default_superposition_value()])
    
    def get_default_size_in_qubit():
        return Qubit.get_default_size_in_qubit()

    def __to_printable__(self) -> str:
        return f"{self.unit_type.__name__}[{self.size}]"