from enum import Enum
from qutes_parser import QutesParser
import cmath

from enum import Enum

class Spin(Enum):
    Positive = 0
    Negative = 1

class Qubit():
    def fromstr(self, literal : str) -> 'Qubit':
        if(literal.startswith(QutesParser.literaltostring(QutesParser.SQUARE_PARENTHESIS_OPEN))):
            literal = literal.removesuffix(QutesParser.literaltostring(QutesParser.QUBIT_LITERAL_POSTFIX))
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
        elif(len(literal) == 2):
            if(literal.startswith('0')): self.__init__(complex(1), complex(0))
            elif(literal.startswith('1')): self.__init__(complex(0), complex(1))
            elif(literal.startswith('+')): self.__init__(complex(0.5), complex(0.5))
            elif(literal.startswith('-')): self.__init__(complex(0.5), complex(-0.5))
        elif(len(literal) == 3):
            if(literal.startswith('+0')): self.__init__(complex(1), complex(0))
            elif(literal.startswith('+1')): self.__init__(complex(0), complex(1))
            elif(literal.startswith('-0')): self.__init__(complex(-1), complex(0))
            elif(literal.startswith('-1')): self.__init__(complex(0), complex(-1))
        else:
            literal = literal.removesuffix(QutesParser.literaltostring(QutesParser.QUBIT_LITERAL_POSTFIX))
            (alpha, beta) = literal.split(',', 1)
            self.__init__(complex(alpha), complex(beta))
        return self
    
    def __init__(self, alpha : complex = complex(), beta : complex = complex()):
        self.alpha = alpha
        self.beta = beta
        # Qubit has negative phase if alpha and beta have different sign?
        self.phase = Spin.Positive if (alpha * beta).real < 0 else Spin.Negative 
        self.is_superposition = cmath.isclose(abs(alpha), abs(beta))

    def __to_printable__(self) -> str:
        spin_str = '+' if self.phase == Spin.Positive else '-'
        if(self.is_superposition):
            return f"|{spin_str}>"
        else:
            return f"[(\u03B1:{self.alpha})|0> {spin_str} (\u03B2:{self.beta})|1>]"

    def __str__(self) -> str:
        return self.__to_printable__()

    def __repr__(self) -> str:
        return self.__to_printable__()
    

class QutesDataType(Enum):
    Undefined = -1
    bool = 1
    int = 2
    string = 3
    qubit = 4
    float = 5

    def from_python_type(var_value) -> 'QutesDataType':
        if isinstance(var_value, bool):
            return QutesDataType.bool
        if isinstance(var_value, int):
            return QutesDataType.int
        if isinstance(var_value, float):
            return QutesDataType.float
        if isinstance(var_value, str):
            return QutesDataType.string
        if isinstance(var_value, Qubit):
            return QutesDataType.qubit
        return QutesDataType.Undefined
            
    def from_declaration_type(var_definition_type : str) -> 'QutesDataType':
        to_match = var_definition_type.lower()
        match to_match:
            case "bool":
                return QutesDataType.bool
            case "int":
                return QutesDataType.int
            case "string":
                return QutesDataType.string
            case "float":
                return QutesDataType.float
            case "qubit":
                return QutesDataType.qubit
            case _:
                return QutesDataType.Undefined
            
    def get_default_value(var_type : 'QutesDataType'):
        match var_type:
            case QutesDataType.bool:
                return bool()
            case QutesDataType.int:
                return int()
            case QutesDataType.float:
                return float()
            case QutesDataType.string:
                return str()
            case QutesDataType.qubit:
                return Qubit()
            case _:
                return QutesDataType.Undefined