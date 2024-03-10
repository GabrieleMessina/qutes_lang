from grammar_frontend.qutes_parser import QutesParser
import utils, math
from symbols.types import Qubit, Quint

class Qustring():
    # note: chr and ord, parse int and char in ASCII for char of size 7 bits
    default_value = [Qubit(complex(1),complex(0))]
    superposition_char = '*'
    not_valid_char = 'X'
    # allowed_chars = ['a', 'b', 'c', 'd', superposition_char, not_valid_char]
    # allowed_chars = ['0', '1', superposition_char, not_valid_char]
    allowed_chars = ['0', '1']
    default_char_size = math.ceil(math.log2(len(allowed_chars)))
    default_block_size = default_char_size

    def get_char_from_int(int_value:int):
        if(int_value > len(Qustring.allowed_chars)):
            return Qustring.allowed_chars[-1]
        return Qustring.allowed_chars[int_value]

    def get_int_from_char(char_value:str):
        try:
            return Qustring.allowed_chars.index(char_value)
        except:
            return len(Qustring.allowed_chars)-1
        

    def init_from_string(literal : str) -> 'Qustring':
        qubits = []
        qubit_literal_postfix = QutesParser.literal_to_string(QutesParser.QUBIT_LITERAL_POSTFIX)
        literal = literal.removesuffix(qubit_literal_postfix)
        literal = literal.removesuffix('"')
        literal = literal.removeprefix('"')

        for char in literal:
            if(char == Qustring.superposition_char):
                qubyte:Quint = Quint.init_from_integer(Qustring.get_int_from_char(char), Qustring.default_char_size, True)
            else:
                qubyte:Quint = Quint.init_from_integer(Qustring.get_int_from_char(char), Qustring.default_char_size)
            qubits.extend(qubyte.qubit_state)
        return Qustring(qubits)

    def init_from_size(number_of_bits : int) -> 'Qustring':
        return Qustring(Qustring.default_value*number_of_bits)
    
    def fromValue(var_value : any) -> 'Qustring':
        if(isinstance(var_value, Qubit)):
            return Qustring([var_value])
        if(isinstance(var_value, str)):
            return Qustring.init_from_string(var_value)
        raise TypeError(f"Cannot convert {type(var_value)} to quint.")
    
    def __init__(self, qubits:list[Qubit] = [Qubit(complex(1),complex(0))]):
        self.qubit_state:list[Qubit] = qubits
        self.size:int = len(self.qubit_state)
        self.number_of_chars:int = int(self.size / Qustring.default_char_size)
        
    def get_quantum_state(self) -> list[complex] :
        #TODO: this doesn't make any sense, outside of the initialization phase we should not rely on the quantum state.
        quantum_state = [complex(1)] * (2**(self.size))
        for quantum_integer_state in range(2**self.size):
            quantum_binary_state = utils.binary(quantum_integer_state, self.size)
            for index in range(len(self.qubit_state)):
                if quantum_binary_state[index] == '0':
                    quantum_state[quantum_integer_state] *= self.qubit_state[index].alpha
                else:
                    quantum_state[quantum_integer_state] *= self.qubit_state[index].beta
        return quantum_state
    
    def to_classical_type(self) -> int:
        bin_number = str.join("", [str(int(qubit.alpha.real)) for qubit in self.qubit_state])[::-1]
        return int(bin_number, 2) #TODO: this is not the correct way to convert a qustring to a classical type.
    
    def __to_printable__(self) -> str:
        str = '['
        for qubit in self.qubit_state:
            str += f"{qubit}, "
        str += ']'
        return str

    def __str__(self) -> str:
        return self.__to_printable__()

    def __repr__(self) -> str:
        return self.__to_printable__()