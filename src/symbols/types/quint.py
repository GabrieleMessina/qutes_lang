from qutes_parser import QutesParser
from utils.phase import Phase
import utils 
from symbols.types import Qubit

class Quint():
    default_value = [Qubit(complex(1),complex(0))]

    def init_from_string(literal : str) -> 'Quint':
        qubits = []
        qubit_literal_postfix = QutesParser.literal_to_string(QutesParser.QUBIT_LITERAL_POSTFIX)
        literal = literal.removesuffix(qubit_literal_postfix)
        if(literal.startswith(QutesParser.literal_to_string(QutesParser.SQUARE_PARENTHESIS_OPEN))):
            literal = literal.removesuffix(QutesParser.literal_to_string(QutesParser.SQUARE_PARENTHESIS_CLOSE))
            literal = literal.removeprefix(QutesParser.literal_to_string(QutesParser.SQUARE_PARENTHESIS_OPEN))
            quint_literals = literal.replace(' ', '').split(qubit_literal_postfix)
            #we have an array of integer that this quint can take on
            if(len(quint_literals) == 1):
                int_literals = [int(i) for i in quint_literals[0].replace(' ', '').split(',')]
                max_value_to_represent = max(int_literals)
                number_of_qubits = len(utils.binary(max_value_to_represent))
                counts = [0] * number_of_qubits
                for number in int_literals:
                    binary_number = utils.binary(number, number_of_qubits)
                    for index in range(number_of_qubits):
                        counts[index] += int(binary_number[index])
                for count in counts:
                    prob_of_being_true = (count/number_of_qubits)
                    qubits.append(Qubit(complex(1-prob_of_being_true), complex(prob_of_being_true)))
            #we have an array of qubits that indicates the single qubits state the quint can take on
            else:
                for qubit_literal in quint_literals:
                    if(len(qubit_literal)>0):
                        qubits.append(Qubit.from_string(qubit_literal.removeprefix(',') + qubit_literal_postfix))
        #we have a simple integer that the quint can take on
        else:
            return Quint.init_from_integer(int(literal))
        return Quint(qubits)
    
    def init_from_integer(literal : int | bool) -> 'Quint':
        binary_rapresentation = utils.binary(literal)
        temp_state = []
        for digit in binary_rapresentation:
            if(digit == '0'):
                temp_state.append(Qubit(complex(1),complex(0)))
            else:
                temp_state.append(Qubit(complex(0),complex(1)))
        return Quint(temp_state)

    def init_from_size(size : int) -> 'Quint':
        return Quint(Quint.default_value*size)
    
    def fromValue(var_value : any) -> 'Quint':
        if(isinstance(var_value, Qubit)):
            return Quint([var_value])
        if(isinstance(var_value, str)):
            return Quint.init_from_string(var_value)
        if(isinstance(var_value, int)):
            return Quint.init_from_integer(str(var_value))
        if(isinstance(var_value, bool)):
            return Quint.init_from_integer(str(var_value))
        raise TypeError(f"Cannot convert {type(var_value)} to quint.")
    
    def __init__(self, qubits:list[Qubit] = [Qubit(complex(1),complex(0))]):
        self.qubit_state:list[Qubit] = qubits
        self.size:int = len(self.qubit_state)
        
    def get_quantum_state(self) -> list[complex] :
        quantum_state = [complex(1)] * (2**(self.size))
        for quantum_integer_state in range(2**self.size):
            quantum_binary_state = utils.binary(quantum_integer_state, self.size)
            for index in range(len(self.qubit_state)):
                if quantum_binary_state[index] == '0':
                    quantum_state[quantum_integer_state] *= self.qubit_state[index].alpha
                else:
                    quantum_state[quantum_integer_state] *= self.qubit_state[index].beta
        return quantum_state
    
    def update_size_with_padding(self, new_size : int) -> 'Quint':
        self.qubit_state = (Quint.default_value*(new_size - self.size) + self.qubit_state) if self.size <= new_size else self.qubit_state[:new_size-1]
        self.size = len(self.qubit_state)
        return self
    
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