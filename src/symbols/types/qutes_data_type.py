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
    void = auto()

    def is_quantum_type(type:'QutesDataType'):
        return type in [QutesDataType.qubit, QutesDataType.quint]
    
    def is_classical_type(type:'QutesDataType'):
        return type not in [QutesDataType.qubit, QutesDataType.quint]

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
        if isinstance(var_value, None):
            return QutesDataType.void
        if isinstance(var_value, Symbol):
            return var_value.symbol_declaration_static_type
        return QutesDataType.undefined

    def from_string_type(var_definition_type : str) -> 'QutesDataType':
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
            case "void":
                return QutesDataType.void
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
            case QutesDataType.void:
                return None
            case _:
                return QutesDataType.undefined
            
    def promote_type(self : 'QutesDataType', to_type : 'QutesDataType') -> 'QutesDataType':
        if(self in TypeCastingHandler.type_promotable_to[to_type]):
            return to_type
        else:
            return QutesDataType.undefined
        
    def down_cast_type(self : 'QutesDataType', to_type : 'QutesDataType') -> 'QutesDataType':
        if(self in TypeCastingHandler.type_down_castable_to[to_type]):
            return to_type
        else: 
            return QutesDataType.undefined


class TypeCastingHandler():
    def __init__(self, quantum_cirtcuit_handler : 'QuantumCircuitHandler'):
        self.quantum_cirtcuit_handler = quantum_cirtcuit_handler

    type_promotable_to : dict[Enum, list[QutesDataType]] = {
        #TODO: handle nested casting, like (quint a = true) bool->qubit->quint
        #..to this types <- this types can be converted to..
        QutesDataType.bool: [QutesDataType.bool],
        QutesDataType.int: [QutesDataType.int, QutesDataType.bool],
        QutesDataType.float: [QutesDataType.float, QutesDataType.int, QutesDataType.bool],
        QutesDataType.string: [QutesDataType.string, QutesDataType.float, QutesDataType.int, QutesDataType.bool],
        QutesDataType.qubit: [QutesDataType.qubit,  QutesDataType.string, QutesDataType.bool],
        QutesDataType.quint: [QutesDataType.quint, QutesDataType.qubit, QutesDataType.string, QutesDataType.int, QutesDataType.bool],
        QutesDataType.void: [],
    }
    type_down_castable_to : dict[Enum, list[QutesDataType]] = {
        #..to this types <- this types can be converted(loosing information) to..
        QutesDataType.bool: [QutesDataType.quint, QutesDataType.qubit, QutesDataType.int, QutesDataType.float, QutesDataType.string, QutesDataType.bool],
        QutesDataType.int: [QutesDataType.quint, QutesDataType.qubit, QutesDataType.float, QutesDataType.int],
        QutesDataType.float: [QutesDataType.quint, QutesDataType.qubit, QutesDataType.float],
        QutesDataType.string: [QutesDataType.string],
        QutesDataType.qubit: [QutesDataType.quint, QutesDataType.qubit],
        QutesDataType.quint: [QutesDataType.quint],
        QutesDataType.void: [],
    }

    def promote_value_to_type(self, var_value : any, from_type:'QutesDataType', to_type : 'QutesDataType', symbol_or_literal) -> any:
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
            
    def down_cast_value_to_type(self, var_value : any, from_type:'QutesDataType', to_type : 'QutesDataType', symbol_or_literal) -> any:
        from symbols import Symbol
        match to_type:
            case QutesDataType.bool:
                if QutesDataType.is_quantum_type(from_type):
                    if(isinstance(symbol_or_literal, Symbol)):
                        return bool(self.quantum_cirtcuit_handler.run_and_measure(symbol_or_literal.quantum_register))
                    else:
                        return bool() #TODO: handle int classical = [1]q and similar //(downcasting from literal)
                return bool(var_value)
            case QutesDataType.int:
                if QutesDataType.is_quantum_type(from_type):
                    if(isinstance(symbol_or_literal, Symbol)):
                        return int(self.quantum_cirtcuit_handler.run_and_measure(symbol_or_literal.quantum_register), 2)
                    else:
                        return int()
                return int(var_value)
            case QutesDataType.float:
                if QutesDataType.is_quantum_type(from_type):
                    if(isinstance(symbol_or_literal, Symbol)):
                        return float(self.quantum_cirtcuit_handler.run_and_measure(symbol_or_literal.quantum_register))
                    else:
                        return float()
                return float(var_value)
            case QutesDataType.string:
                if QutesDataType.is_quantum_type(from_type):
                    if(isinstance(symbol_or_literal, Symbol)):
                        return str(self.quantum_cirtcuit_handler.run_and_measure(symbol_or_literal.quantum_register))
                    else:
                        return str()
                return str(var_value)
            case QutesDataType.qubit:
                return Qubit.fromValue(var_value)
            case QutesDataType.quint:
                return Quint.fromValue(var_value)
            case _:
                return QutesDataType.undefined