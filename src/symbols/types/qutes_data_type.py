#TODO: try refactor import directly from symbols.types
from symbols.types.qubit import Qubit
from symbols.types.quint import Quint
from symbols.types.qustring import Qustring
from symbols.types.quantum_array_type import QuantumArrayType
from enum import Enum, auto

class QutesDataType(Enum):
    # Primitive types
    undefined = -1
    bool = 1
    int = auto()
    float = auto()
    string = auto()
    qubit = auto()
    quint = auto()
    qustring = auto()
    void = auto()
    # Array types
    bool_array = auto()
    int_array = auto()
    float_array = auto()
    string_array = auto()
    qubit_array = auto()
    quint_array = auto()
    qustring_array = auto()

    def is_quantum_type(type:str):
        return QutesDataType.is_quantum_type(QutesDataType.from_string_type(type))

    def is_quantum_type(type:'QutesDataType'):
        return type in [QutesDataType.qubit, QutesDataType.quint, QutesDataType.qustring]
    
    def is_classical_type(type:str):
        return QutesDataType.is_classical_type(QutesDataType.from_string_type(type))

    def is_classical_type(type:'QutesDataType'):
        return type not in [QutesDataType.qubit, QutesDataType.quint, QutesDataType.qustring]
    
    def is_array_type(type:str):
        return QutesDataType.is_array_type(QutesDataType.from_string_type(type))
    
    def is_array_type(type:'QutesDataType'):
        return type in [
            QutesDataType.qustring, QutesDataType.quint, QutesDataType.string, # Can be access by [] operator but not really array types  
            QutesDataType.bool_array, QutesDataType.int_array, QutesDataType.float_array, QutesDataType.string_array, QutesDataType.qubit_array, QutesDataType.quint_array, QutesDataType.qustring_array]

    def type_of(var_value : any) -> 'QutesDataType':
        from symbols import Symbol
        if var_value is None:
            return QutesDataType.void
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
        if isinstance(var_value, Qustring):
            return QutesDataType.qustring
        if isinstance(var_value, list):
            if(len(var_value) == 0):
                return QutesDataType.bool_array 
            return QutesDataType.promote_unit_to_array_type(QutesDataType.type_of(var_value[0]))
        if isinstance(var_value, QuantumArrayType):
            return QutesDataType.qubit_array
        # TODO: Subscripted generics cannot be used with class and instance checks
        # if isinstance(var_value, QuantumArrayType[Qubit]):
        #     return QutesDataType.qubit_array
        # if isinstance(var_value, QuantumArrayType[Quint]):
        #     return QutesDataType.quint_array
        # if isinstance(var_value, QuantumArrayType[Qustring]):
        #     return QutesDataType.qustring_array
        if isinstance(var_value, Symbol):
            return var_value.symbol_declaration_static_type
        return QutesDataType.undefined

    def from_string_type(var_definition_type : str) -> 'QutesDataType':
        to_match = var_definition_type.lower()
        is_array_type = False
        if(to_match.endswith("[]")):
            to_match = to_match.removesuffix("[]")
            is_array_type = True

        match to_match:
            case "bool":
                return QutesDataType.bool if not is_array_type else QutesDataType.bool_array
            case "int":
                return QutesDataType.int if not is_array_type else QutesDataType.int_array
            case "float":
                return QutesDataType.float if not is_array_type else QutesDataType.float_array
            case "string":
                return QutesDataType.string if not is_array_type else QutesDataType.string_array
            case "qubit":
                return QutesDataType.qubit if not is_array_type else QutesDataType.qubit_array
            case "quint":
                return QutesDataType.quint if not is_array_type else QutesDataType.quint_array
            case "qustring":
                return QutesDataType.qustring if not is_array_type else QutesDataType.qustring_array
            case "void":
                return QutesDataType.void
            case _:
                return QutesDataType.undefined

    def promote_classical_to_quantum_value(classical_value: any) -> Qubit | Quint | Qustring:
        type = QutesDataType.type_of(classical_value)
        match type:
            case QutesDataType.bool:
                return Qubit.fromValue(classical_value)
            case QutesDataType.int:
                return Quint.fromValue(classical_value)
            case QutesDataType.float:
                raise NotImplementedError()
            case QutesDataType.string:
                return Qustring.fromValue(classical_value)
            case QutesDataType.qubit:
                return classical_value
            case QutesDataType.quint:
                return classical_value
            case QutesDataType.qustring:
                return classical_value
            case QutesDataType.void:
                return None
            case _:
                return QutesDataType.undefined

    def promote_unit_to_array_type(unit_type : 'QutesDataType') -> 'QutesDataType':
        match unit_type:
            case QutesDataType.bool:
                return QutesDataType.bool_array
            case QutesDataType.int:
                return QutesDataType.int_array
            case QutesDataType.float:
                return QutesDataType.float_array
            case QutesDataType.string:
                return QutesDataType.string_array
            case QutesDataType.qubit:
                return QutesDataType.qubit_array
            case QutesDataType.quint:
                return QutesDataType.quint_array
            case QutesDataType.qustring:
                return QutesDataType.qustring_array
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
            case QutesDataType.qustring:
                return Qustring()
            case QutesDataType.bool_array:
                return []
            case QutesDataType.int_array:
                return []
            case QutesDataType.float_array:
                return []
            case QutesDataType.string_array:
                return []
            case QutesDataType.qubit_array:
                return QuantumArrayType[Qubit]()
            case QutesDataType.quint_array:
                return QuantumArrayType[Quint]()
            case QutesDataType.qustring_array:
                return QuantumArrayType[Qustring]()
            case QutesDataType.void:
                return None
            case _:
                return None
            
    def get_size_in_qubit(var_type : 'QutesDataType'):
        match var_type:
            case QutesDataType.bool:
                return 1
            case QutesDataType.qubit:
                return 1
            case QutesDataType.int:
                return Quint.default_size_in_qubit
            case QutesDataType.quint:
                return Quint.default_size_in_qubit
            case QutesDataType.string:
                return Qustring.default_size_in_qubit
            case QutesDataType.qustring:
                return Qustring.default_size_in_qubit
            case QutesDataType.void:
                return 0
            case QutesDataType.float:
                return 1
            case _:
                return 1
            
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
        QutesDataType.qustring: [QutesDataType.qustring, QutesDataType.quint, QutesDataType.qubit, QutesDataType.string, QutesDataType.int, QutesDataType.bool],
        QutesDataType.void: [],
        QutesDataType.bool_array: [],
        QutesDataType.int_array: [],
        QutesDataType.float_array: [],
        QutesDataType.string_array: [],
        QutesDataType.qubit_array: [],
        QutesDataType.quint_array: [],
        QutesDataType.qustring_array: [],
    }
    type_down_castable_to : dict[Enum, list[QutesDataType]] = {
        #..to this types <- this types can be converted(loosing information) to..
        QutesDataType.bool: [QutesDataType.qubit, QutesDataType.bool],
        QutesDataType.int: [QutesDataType.quint, QutesDataType.qubit, QutesDataType.int],
        QutesDataType.float: [QutesDataType.quint, QutesDataType.qubit, QutesDataType.float, QutesDataType.int],
        QutesDataType.string: [QutesDataType.qustring, QutesDataType.string],
        QutesDataType.qubit: [QutesDataType.qubit],
        QutesDataType.quint: [QutesDataType.quint],
        QutesDataType.qustring: [QutesDataType.qustring],
        QutesDataType.void: [],
        QutesDataType.bool_array: [],
        QutesDataType.int_array: [],
        QutesDataType.float_array: [],
        QutesDataType.string_array: [],
        QutesDataType.qubit_array: [],
        QutesDataType.quint_array: [],
        QutesDataType.qustring_array: [],
    }

    def promote_value_to_type(self, var_value : any, from_type:'QutesDataType', to_type : 'QutesDataType', symbol_or_literal) -> any:
        match to_type:
            case QutesDataType.bool:
                return bool(int(var_value))
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
            case QutesDataType.qustring:
                return Qustring.fromValue(var_value)
            case _:
                return QutesDataType.undefined
            
    def down_cast_value_to_type(self, var_value : any, from_type:'QutesDataType', to_type : 'QutesDataType', symbol_or_literal) -> any:
        from symbols import Symbol
        from_type_value = None
        if QutesDataType.is_quantum_type(from_type):
            if(isinstance(symbol_or_literal, Symbol) and symbol_or_literal.is_anonymous):
                from_type_value = symbol_or_literal.value.to_classical_type()
            else:
                from_type_value, _ = self.quantum_cirtcuit_handler.get_run_and_measure_result_for_quantum_var(symbol_or_literal.quantum_register)
            
            if from_type_value == None and isinstance(symbol_or_literal, Symbol):
                from_type_value = symbol_or_literal.value.to_classical_type()

        if(from_type_value == None):
            from_type_value = var_value

        match to_type:
            case QutesDataType.bool:
                return bool(int(from_type_value))
            case QutesDataType.int:
               return int(from_type_value)
            case QutesDataType.float:
                return float(from_type_value)
            case QutesDataType.string:
                return str(from_type_value)
            case QutesDataType.qubit:
                return Qubit.fromValue(var_value)
            case QutesDataType.quint:
                return Quint.fromValue(var_value)
            case QutesDataType.qustring:
                return Qustring.fromValue(var_value)
            case _:
                return QutesDataType.undefined