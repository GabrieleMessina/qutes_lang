from symbols.qutes_types import QutesDataType
from symbols.scope_handler import ScopeHandler
from symbols.scope_tree_node import Symbol, SymbolType

class VariablesHandler():

    def __init__(self, scope_handler : ScopeHandler):
        self.scope_handler = scope_handler

    def update_variable_state(self, variable_name : str, new_value):        
        eligible_symbols_to_update = [symbol for symbol in self.scope_handler.current_symbols_scope.symbols if symbol.name == variable_name]
        if len(eligible_symbols_to_update) > 0:
            # In case multiple scopes declare a varialble with the same name we take the last one, that is the one from the nearest scope.
            symbol_index_in_scope = self.scope_handler.current_symbols_scope.symbols.index(eligible_symbols_to_update[-1]) 
            symbol_to_update = self.scope_handler.current_symbols_scope.symbols[symbol_index_in_scope]

        	# check if the type of the varible match the type of the value we are trying to assign. 
            self.__guard_value_and_definition_type_matches(symbol_to_update.symbol_type_detail, variable_name, new_value)

            # Update the variable value if everything is ok.
            self.scope_handler.current_symbols_scope.symbols[symbol_index_in_scope].value = new_value
        else:
            raise SyntaxError(f"No variable declared with name '{variable_name}'.")
        
    def declare_variable(self, declaration_type : str, variable_name : str, value):
        if(value is None):
            value = QutesDataType.get_default_value(QutesDataType.from_declaration_type(declaration_type))

        already_taken_symbol_in_this_scope = [symbol for symbol in self.scope_handler.current_symbols_scope.symbols if symbol.name == value and symbol.scope == self.scope_handler.current_symbols_scope]
        if(len(already_taken_symbol_in_this_scope) == 0):
            self.__guard_value_and_definition_type_matches(declaration_type, variable_name, value)

            self.scope_handler.current_symbols_scope.symbols.append(Symbol(variable_name, SymbolType.VariableSymbol, declaration_type, value, self.scope_handler.current_symbols_scope))
        else:
            raise SyntaxError(f"Variable with name '{value}' already declared.")
        
    def __guard_value_and_definition_type_matches(self, declaration_type, var_name, value) -> bool:
        value_qutes_type = QutesDataType.from_python_type(value)
        definition_qutes_type = QutesDataType.from_declaration_type(declaration_type)

        if(value_qutes_type != definition_qutes_type):
            raise SyntaxError(f"Cannot convert type '{definition_qutes_type}' to '{value_qutes_type}' for '{var_name}'.")

        return True