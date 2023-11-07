from enum import Enum

class Qubit():
    def __init__(self, alpha : complex, beta : complex):
        self.alpha = alpha
        self.beta = beta

    def __to_printable__(self) -> str:
        return f"[(\u03B1:{self.alpha})|0> + (\u03B2:{self.beta})|1>]"

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

    def from_python_type(var_value) -> 'QutesDataType':
        if isinstance(var_value, bool):
            return QutesDataType.bool
        if isinstance(var_value, int):
            return QutesDataType.int
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
            case QutesDataType.string:
                return str()
            case QutesDataType.qubit:
                return Qubit(complex(), complex())
            case _:
                return QutesDataType.Undefined