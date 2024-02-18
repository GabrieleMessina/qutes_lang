from qutes_parser import QutesParser
import utils 
from symbols.types import Qubit, Quint

class Qustring():
    default_value = [Qubit(complex(1),complex(0))]
    default_char_size = 7

    def init_from_string(literal : str) -> 'Qustring':
        qubits = []
        qubit_literal_postfix = QutesParser.literal_to_string(QutesParser.QUBIT_LITERAL_POSTFIX)
        literal = literal.removesuffix(qubit_literal_postfix)
        literal = literal.removesuffix('"')
        literal = literal.removeprefix('"')
        
        # byte_literal = literal.encode('ascii')
        # for byte in byte_literal:
        #     qubyte:Quint = Quint.init_from_integer(byte, Qustring.default_char_size)
        #     qubits.extend(qubyte.qubit_state)

        #TODO: chr and ord, works only for char of size 7 bits
        for char in literal:
            qubyte:Quint = Quint.init_from_integer(ord(char), Qustring.default_char_size)
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
        self.qubit_state:list[Qubit] = qubits[::-1]
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