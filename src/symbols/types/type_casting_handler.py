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
        QutesDataType.int: [QutesDataType.int, QutesDataType.bool, QutesDataType.bool_array],
        QutesDataType.float: [QutesDataType.float, QutesDataType.int, QutesDataType.bool, QutesDataType.bool_array],
        QutesDataType.string: [QutesDataType.string, QutesDataType.float, QutesDataType.int, QutesDataType.bool, QutesDataType.bool_array],
        QutesDataType.qubit: [QutesDataType.qubit,  QutesDataType.string, QutesDataType.bool, QutesDataType.bool_array],
        QutesDataType.quint: [QutesDataType.quint, QutesDataType.qubit, QutesDataType.string, QutesDataType.int, QutesDataType.bool, QutesDataType.bool_array],
        QutesDataType.qustring: [QutesDataType.qustring, QutesDataType.quint, QutesDataType.qubit, QutesDataType.string, QutesDataType.int, QutesDataType.bool, QutesDataType.bool_array],
        QutesDataType.void: [],
        QutesDataType.bool_array: [QutesDataType.bool_array],
        QutesDataType.int_array: [QutesDataType.bool_array, QutesDataType.int_array],
        QutesDataType.float_array: [QutesDataType.bool_array, QutesDataType.int_array, QutesDataType.float_array],
        QutesDataType.string_array: [QutesDataType.bool_array, QutesDataType.int_array, QutesDataType.float_array, QutesDataType.string_array],
        QutesDataType.qubit_array: [QutesDataType.bool_array, QutesDataType.qubit_array],
        QutesDataType.quint_array: [QutesDataType.quint_array, QutesDataType.int_array, QutesDataType.qubit_array, QutesDataType.bool_array],
        QutesDataType.qustring_array: [QutesDataType.qustring_array, QutesDataType.quint_array, QutesDataType.qubit_array, QutesDataType.string_array, QutesDataType.int_array, QutesDataType.float_array, QutesDataType.bool_array],
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
        QutesDataType.bool_array: [QutesDataType.qubit_array, QutesDataType.bool_array],
        QutesDataType.int_array: [QutesDataType.qubit_array, QutesDataType.quint_array, QutesDataType.int_array],
        QutesDataType.float_array: [QutesDataType.qubit_array, QutesDataType.quint_array, QutesDataType.float_array, QutesDataType.int_array],
        QutesDataType.string_array: [QutesDataType.qubit_array, QutesDataType.quint_array, QutesDataType.qustring_array, QutesDataType.float_array, QutesDataType.int_array, QutesDataType.string_array],
        QutesDataType.qubit_array: [QutesDataType.qubit_array],
        QutesDataType.quint_array: [QutesDataType.quint_array],
        QutesDataType.qustring_array: [QutesDataType.qustring_array],
    }

    def promote_value_to_type(self, var_value : any, from_type:'QutesDataType', to_type : 'QutesDataType', symbol_or_literal) -> any:
        match to_type:
            case QutesDataType.bool:
                return bool(int(var_value))
            case QutesDataType.int:
                if isinstance(var_value, list):
                    return int(''.join([str(int(value)) for value in var_value]), 2)
                return int(var_value)
            case QutesDataType.float:
                if isinstance(var_value, list):
                    return int(''.join([str(int(value)) for value in var_value]), 2)
                return float(var_value)
            case QutesDataType.string:
                return str(var_value)
            case QutesDataType.qubit:
                return Qubit.fromValue(var_value)
            case QutesDataType.quint:
                return Quint.fromValue(var_value)
            case QutesDataType.qustring:
                return Qustring.fromValue(var_value)
            case QutesDataType.bool_array:
                return [self.promote_value_to_type(value, QutesDataType.type_of(value), QutesDataType.bool) for value in var_value]
            case QutesDataType.int_array:
                return [self.promote_value_to_type(value, QutesDataType.type_of(value), QutesDataType.int) for value in var_value]
            case QutesDataType.float_array:
                return [self.promote_value_to_type(value, QutesDataType.type_of(value), QutesDataType.float) for value in var_value]
            case QutesDataType.string_array:
                return [self.promote_value_to_type(value, QutesDataType.type_of(value), QutesDataType.string) for value in var_value]
            case QutesDataType.qubit_array:
                return [self.promote_value_to_type(value, QutesDataType.type_of(value), QutesDataType.qubit) for value in var_value]
            case QutesDataType.quint_array:
                return [self.promote_value_to_type(value, QutesDataType.type_of(value), QutesDataType.quint) for value in var_value]
            case QutesDataType.qustring_array:
                return [self.promote_value_to_type(value, QutesDataType.type_of(value), QutesDataType.qustring) for value in var_value]
            case _:
                return QutesDataType.undefined

    def __cast_value_to_type(self, var_value : any, from_type:'QutesDataType', to_type : 'QutesDataType') -> any:
        if self.type_promotable_to[to_type].count(from_type) > 0:
            return self.promote_value_to_type(var_value, from_type, to_type, None)
        if self.type_down_castable_to[to_type].count(from_type) > 0:
            return self.down_cast_value_to_type(var_value, from_type, to_type, None)
        raise TypeError(f"Cannot cast type '{from_type}' to '{to_type}'.")

    def down_cast_value_to_type(self, var_value : any, from_type:'QutesDataType', to_type : 'QutesDataType', symbol_or_literal) -> any:
        from symbols import Symbol
        from_type_value = None

        # if the value is a quantum type, we need to get the value from the quantum circuit measuring it.
        if QutesDataType.is_quantum_type(from_type):
            from_type_value = [bool(value == '1') for value in self.quantum_cirtcuit_handler.get_run_and_measure_result_for_quantum_var(symbol_or_literal.quantum_register)]
            if len(from_type_value) > 1:
                from_type_value = self.__cast_value_to_type(from_type_value, QutesDataType.bool_array, to_type)
            else:
                from_type_value = self.__cast_value_to_type(from_type_value[0], QutesDataType.bool, to_type)

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
            case QutesDataType.bool_array:
                return [self.down_cast_value_to_type(value, QutesDataType.type_of(value), QutesDataType.bool, value) for value in var_value]
            case QutesDataType.int_array:
                return [self.down_cast_value_to_type(value, QutesDataType.type_of(value), QutesDataType.int, value) for value in var_value]
            case QutesDataType.float_array:
                return [self.down_cast_value_to_type(value, QutesDataType.type_of(value), QutesDataType.float, value) for value in var_value]
            case QutesDataType.string_array:
                return [self.down_cast_value_to_type(value, QutesDataType.type_of(value), QutesDataType.string, value) for value in var_value]
            case QutesDataType.qubit_array:
                return [self.down_cast_value_to_type(value, QutesDataType.type_of(value), QutesDataType.qubit, value) for value in var_value]
            case QutesDataType.quint_array:
                return [self.down_cast_value_to_type(value, QutesDataType.type_of(value), QutesDataType.quint, value) for value in var_value]
            case QutesDataType.qustring_array:
                return [self.down_cast_value_to_type(value, QutesDataType.type_of(value), QutesDataType.qustring, value) for value in var_value]
            case _:
                return QutesDataType.undefined