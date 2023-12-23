from qutes_parser import QutesParser
from utils.phase import Phase
import cmath

class Qubit():
    def from_string(literal : str) -> 'Qubit':
        literal = literal.removesuffix(QutesParser.literal_to_string(QutesParser.QUBIT_LITERAL_POSTFIX))
        if(literal.startswith(QutesParser.literal_to_string(QutesParser.SQUARE_PARENTHESIS_OPEN))):
            literal = literal.removesuffix(QutesParser.literal_to_string(QutesParser.SQUARE_PARENTHESIS_CLOSE))
            literal = literal.removeprefix(QutesParser.literal_to_string(QutesParser.SQUARE_PARENTHESIS_OPEN))
            values = literal.split(',', 1)
            n_values = len(values)
            if(n_values == 2):
                return Qubit(complex(1/n_values), complex(1/n_values))
            else:
                if(values[0] == '0'):
                    return Qubit(complex(1), complex(0))
                else:
                    return Qubit(complex(0), complex(1))
        elif(len(literal) == 1):
            if(literal.startswith('0')): return Qubit(complex(1), complex(0))
            elif(literal.startswith('1')): return Qubit(complex(0), complex(1))
        elif(len(literal) == 3):
            if(literal.startswith('|0>')): return Qubit(complex(1), complex(0))
            elif(literal.startswith('|1>')): return Qubit(complex(0), complex(1))
            elif(literal.startswith('|+>')): return Qubit(complex(0.5), complex(0.5))
            elif(literal.startswith('|->')): return Qubit(complex(0.5), complex(-0.5))
        else:
            (alpha, beta) = literal.split(',', 1)
            Qubit(complex(alpha), complex(beta))
        #TODO: try except showing the error:
        # raise TypeError(f"Cannot convert {literal} to qubit.")
    
    def fromValue(var_value : any) -> 'Qubit':
        if(isinstance(var_value, str)):
            return Qubit.from_string(var_value)
        if(isinstance(var_value, bool)):
            return Qubit.from_string(str(var_value))
        raise TypeError(f"Cannot convert {type(var_value)} to qubit.")
    
    def __init__(self, alpha : complex = complex(1), beta : complex = complex(0)):
        self.alpha = alpha
        self.beta = beta
        # Qubit has negative phase if alpha and beta have different sign?
        self.phase = Phase.Positive if (alpha * beta).real >= 0 else Phase.Negative 
        self.is_superposition = cmath.isclose(abs(alpha), abs(beta))

    def get_quantum_state(self) -> list[complex]:
        return [self.alpha, self.beta]

    def update_size_with_padding(self, new_size : int) -> 'Quint':
        from symbols.types import Quint
        return Quint([self]).update_size_with_padding(new_size)

    def __to_printable__(self) -> str:
        spin_str = '+' if self.phase == Phase.Positive else '-'
        if(self.is_superposition):
            return f"|{spin_str}>"
        else:
            return f"[(\u03B1:{self.alpha})|0> {spin_str} (\u03B2:{self.beta})|1>]"

    def __str__(self) -> str:
        return self.__to_printable__()

    def __repr__(self) -> str:
        return self.__to_printable__()