from qutes_parser import QutesParser
from utils.phase import Phase
import cmath

class Qubit():
    def fromstr(self, literal : str) -> 'Qubit':
        literal = literal.removesuffix(QutesParser.literaltostring(QutesParser.QUBIT_LITERAL_POSTFIX))
        if(literal.startswith(QutesParser.literaltostring(QutesParser.SQUARE_PARENTHESIS_OPEN))):
            literal = literal.removesuffix(QutesParser.literaltostring(QutesParser.SQUARE_PARENTHESIS_CLOSE))
            literal = literal.removeprefix(QutesParser.literaltostring(QutesParser.SQUARE_PARENTHESIS_OPEN))
            values = literal.split(',', 1)
            n_values = len(values)
            if(n_values == 2):
                self.__init__(complex(1/n_values), complex(1/n_values))
            else:
                if(values[0] == '0'):
                    self.__init__(complex(1), complex(0))
                else:
                    self.__init__(complex(0), complex(1))
        elif(len(literal) == 1):
            if(literal.startswith('0')): self.__init__(complex(1), complex(0))
            elif(literal.startswith('1')): self.__init__(complex(0), complex(1))
        elif(len(literal) == 3):
            if(literal.startswith('|0>')): self.__init__(complex(1), complex(0))
            elif(literal.startswith('|1>')): self.__init__(complex(0), complex(1))
            elif(literal.startswith('|+>')): self.__init__(complex(0.5), complex(0.5))
            elif(literal.startswith('|->')): self.__init__(complex(0.5), complex(-0.5))
        else:
            (alpha, beta) = literal.split(',', 1)
            self.__init__(complex(alpha), complex(beta))
        return self
        
    #TODO: implement type casting
    # def __bool__(self, obj):
    #     print("=============", obj)
    
    def __init__(self, alpha : complex = complex(1), beta : complex = complex(0)):
        self.alpha = alpha
        self.beta = beta
        # Qubit has negative phase if alpha and beta have different sign?
        self.phase = Phase.Positive if (alpha * beta).real >= 0 else Phase.Negative 
        self.is_superposition = cmath.isclose(abs(alpha), abs(beta))

    def get_quantum_state(self) -> list[complex]:
        return [self.alpha, self.beta]

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