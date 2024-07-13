from symbols.types.qubit import Qubit
from symbols.types.quint import Quint
from symbols.types.qustring import Qustring
from symbols.types.qutes_data_type import QutesDataType
from enum import Enum

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