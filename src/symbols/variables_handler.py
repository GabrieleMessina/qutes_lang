from symbols.types.qutes_data_type import QutesDataType
from symbols.scope_handler import ScopeHandler
from symbols.symbol import Symbol, SymbolClass
from quantum_circuit import QuantumCircuitHandler

class VariablesHandler():

    def __init__(self, scope_handler : ScopeHandler, quantum_cirtcuit_handler : QuantumCircuitHandler):
        self.scope_handler = scope_handler
        self.quantum_cirtcuit_handler = quantum_cirtcuit_handler

    def update_variable_state(self, variable_name : str, new_value) -> Symbol:       
        new_value = self.get_value(new_value)
        eligible_symbols_to_update = [symbol for symbol in self.scope_handler.current_symbols_scope.symbols if symbol.name == variable_name]
        if len(eligible_symbols_to_update) > 0:
            # In case multiple scopes declare a varialble with the same name we take the last one, that is the one from the nearest scope.
            symbol_index_in_scope = self.scope_handler.current_symbols_scope.symbols.index(eligible_symbols_to_update[-1]) 
            symbol_to_update = self.scope_handler.current_symbols_scope.symbols[symbol_index_in_scope]

        	# check if the type of the varible match the type of the value we are trying to assign. 
            promoted_type = self.__guard_value_and_definition_type_matches_or_promoted(symbol_to_update.symbol_declaration_static_type, variable_name, new_value)

            # Update the variable value if everything is ok.
            symbol_to_update.value = new_value #python treats everything as a reference type
            symbol_to_update.promoted_static_type = promoted_type

            #Handle quantum circuit update
            if(self.is_quantum_type(symbol_to_update.symbol_declaration_static_type)):
                self.quantum_cirtcuit_handler.replace_quantum_register(variable_name, symbol_to_update.value)
            return symbol_to_update
        else:
            raise SyntaxError(f"No variable declared with name '{variable_name}'.")
        
    def declare_variable(self, declaration_type : str, variable_name : str, value) -> Symbol:
        if(value is None):
            value = QutesDataType.get_default_value(QutesDataType.from_declaration_type(declaration_type))
        else: 
             value = self.get_value(value) 
        already_taken_symbol_in_this_scope = [symbol for symbol in self.scope_handler.current_symbols_scope.symbols if symbol.name == variable_name and symbol.scope == self.scope_handler.current_symbols_scope]
        if(len(already_taken_symbol_in_this_scope) == 0):
            promoted_type = self.__guard_value_and_definition_type_matches_or_promoted(declaration_type, variable_name, value)

            new_symbol = Symbol(variable_name, SymbolClass.VariableSymbol, declaration_type, promoted_type.name, value, self.scope_handler.current_symbols_scope)
            self.scope_handler.current_symbols_scope.symbols.append(new_symbol)
            #Handle quantum circuit update
            if(self.is_quantum_type(declaration_type)):
                new_symbol.quantum_register = self.quantum_cirtcuit_handler.declare_quantum_register(variable_name, new_symbol.value)

            return new_symbol
        else:
            raise SyntaxError(f"Variable with name '{variable_name}' already declared.")
        
    def __guard_value_and_definition_type_matches_or_promoted(self, declaration_type, var_name, value) -> QutesDataType:
        value_qutes_type = QutesDataType.type_of(value)
        definition_qutes_type = QutesDataType.from_declaration_type(declaration_type)

        if(value_qutes_type != definition_qutes_type and value_qutes_type.promote_type(definition_qutes_type) == QutesDataType.undefined):
            raise SyntaxError(f"Cannot convert type '{definition_qutes_type}' to '{value_qutes_type}' for '{var_name}'.")

        promoted_type = value_qutes_type.promote_type(definition_qutes_type)

        if(value_qutes_type != promoted_type):
            value = QutesDataType.cast_value_to_type(value, promoted_type)

        return promoted_type
    
    def get_value(self, var_value):
        if(isinstance(var_value, Symbol)):
            return var_value.value
        return var_value
    
    def get_type_of(self, var_value):
        if(isinstance(var_value, Symbol)):
            return var_value.symbol_declaration_static_type
        return QutesDataType.type_of(var_value)
    
    def is_quantum_type(self, declaration_type:str) -> bool:
        return QutesDataType.from_declaration_type(declaration_type) in [QutesDataType.qubit, QutesDataType.quint]