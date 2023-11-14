from symbols.types.qubit import Qubit
from symbols.types.quint import Quint
from enum import Enum, auto

class QutesDataType(Enum):
    Undefined = -1
    bool = 1
    int = auto()
    string = auto()
    qubit = auto()
    float = auto()
    quint = auto()

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
        if isinstance(var_value, Quint):
            return QutesDataType.quint
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
            case "quint":
                return QutesDataType.quint
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
            case QutesDataType.quint:
                return Quint(int())
            case _:
                return QutesDataType.Undefined