from symbols.types.qubit import Qubit
from symbols.types.quint import Quint
from enum import Enum, auto

class QutesDataType(Enum):
    undefined = -1
    bool = 1
    int = auto()
    float = auto()
    string = auto()
    qubit = auto()
    quint = auto()

    def promote_type(self : 'QutesDataType', to_type : 'QutesDataType') -> 'QutesDataType':
        if(self in TypeCastingHandler.type_compatibility[to_type]):
            return to_type
        else: 
            return QutesDataType.undefined 

    def cast_value_to_type(var_value : any, to_type : 'QutesDataType') -> any:
        match to_type:
            case QutesDataType.bool:
                return bool(var_value)
            case QutesDataType.int:
                return int(var_value)
            case QutesDataType.float:
                return float(var_value)
            case QutesDataType.string:
                return str(var_value)
            case QutesDataType.qubit:
                return Qubit.fromValue(var_value)
            case QutesDataType.quint:
                return Quint.fromValue(var_value)
            case _:
                return QutesDataType.undefined

    def type_of(var_value : any) -> 'QutesDataType':
        from symbols import Symbol
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
        if isinstance(var_value, Symbol):
            return QutesDataType.from_declaration_type(var_value.symbol_declaration_static_type)
        return QutesDataType.undefined

    def from_declaration_type(var_definition_type : str) -> 'QutesDataType':
        to_match = var_definition_type.lower()
        match to_match:
            case "bool":
                return QutesDataType.bool
            case "int":
                return QutesDataType.int
            case "float":
                return QutesDataType.float
            case "string":
                return QutesDataType.string
            case "qubit":
                return QutesDataType.qubit
            case "quint":
                return QutesDataType.quint
            case _:
                return QutesDataType.undefined

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
                return Quint()
            case _:
                return QutesDataType.undefined
            

class TypeCastingHandler():
    type_compatibility : dict[Enum, list[QutesDataType]] = {
        QutesDataType.bool: [QutesDataType.bool],
        QutesDataType.int: [QutesDataType.int, QutesDataType.bool],
        QutesDataType.float: [QutesDataType.float, QutesDataType.int, QutesDataType.bool],
        QutesDataType.string: [QutesDataType.string, QutesDataType.float, QutesDataType.int, QutesDataType.bool],
        QutesDataType.qubit: [QutesDataType.qubit, QutesDataType.bool],
        QutesDataType.quint: [QutesDataType.quint, QutesDataType.qubit, QutesDataType.int, QutesDataType.bool],
    }