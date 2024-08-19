from grammar_frontend.qutes_parser import QutesParser
from symbols.types import Qubit, Quint
from symbols.types import QuantumType
from quantum_circuit.state_preparation import StatePreparation, Statevector
import utils, math

class Qustring(QuantumType['Qustring']):
    # note: chr and ord, parse int and char in ASCII for char of size 7 bits
    # allowed_chars = ['a', 'b', 'c', 'd', superposition_char, __not_valid_char]
    # allowed_chars = ['0', '1', superposition_char, __not_valid_char]
    __superposition_char = '*'
    __not_valid_char = 'X'
    __allowed_chars = ['0', '1']

    def __init__(self, qubits:StatePreparation = StatePreparation("0")):
        super().__init__(Qustring)
        self.qubit_state:StatePreparation = qubits
        self.size:int = len(self.qubit_state)
        self.number_of_chars:int = int(self.size / Qustring.get_default_size_in_qubit())

    def get_default_value():
        return [complex(1),complex(0)] * Qustring.get_default_size_in_qubit()
    
    def get_default_superposition_value():
        return [complex(0.5),complex(0.5)] * Qustring.get_default_size_in_qubit()
    
    def get_default_size_in_qubit():
        return math.ceil(math.log2(len(Qustring.__allowed_chars)))

    def get_char_from_int(int_value:int):
        if(int_value > len(Qustring.__allowed_chars)):
            return Qustring.__allowed_chars[-1]
        return Qustring.__allowed_chars[int_value]

    def get_int_from_char(char_value:str):
        try:
            return Qustring.__allowed_chars.index(char_value)
        except:
            return len(Qustring.__allowed_chars)-1    

    def init_from_string(literal : str) -> 'Qustring':
        init_state = None
        qubit_literal_postfix = QutesParser.literal_to_string(QutesParser.QUBIT_LITERAL_POSTFIX)
        literal = literal.removesuffix(qubit_literal_postfix)
        literal = literal.removesuffix('"')
        literal = literal.removeprefix('"')

        for char in literal:
            if(char == Qustring.__superposition_char):
                qubyte:Quint = Quint.init_from_size(Qustring.get_default_size_in_qubit(), True)
            else:
                qubyte:Quint = Quint.init_from_integer(Qustring.get_int_from_char(char), Qustring.get_default_size_in_qubit())
            char_init_state = Statevector(qubyte.qubit_state)
            if(init_state == None):
                init_state = char_init_state
            else:
                init_state = init_state.tensor(char_init_state)

        init_state = StatePreparation(init_state)
        return Qustring(init_state)

    def fromValue(var_value : any) -> 'Qustring':
        if(isinstance(var_value, Qubit)):
            return Qustring(var_value.qubit_state)
        if(isinstance(var_value, str)):
            return Qustring.init_from_string(var_value)
        if(isinstance(var_value, list)):
            return Quint.init_from_string("".join([str(int(i)) for i in var_value]))
        raise TypeError(f"Cannot convert {type(var_value)} to quint.")
    
    def to_classical_type(self) -> int:
        bin_number = str.join("", [str(value) for value in self.qubit_state.params])
        return int(bin_number, 2) #TODO: this is not the correct way to convert a qustring to a classical type.
    
    def __to_printable__(self) -> str:
        return f"{self.qubit_state}"