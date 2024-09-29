from symbols.types.type_casting_handler import TypeCastingHandler
from symbols.types.qutes_data_type import QutesDataType, QuantumArrayType
from symbols.scope_handler import ScopeHandler
from symbols.symbol import Symbol, SymbolClass
from quantum_circuit import QuantumCircuitHandler

class VariablesHandler():

    def __init__(self, scope_handler : ScopeHandler, quantum_circuit_handler : QuantumCircuitHandler):
        self.scope_handler = scope_handler
        self.quantum_circuit_handler = quantum_circuit_handler
        self.type_casting_handler = TypeCastingHandler(quantum_circuit_handler)

    def update_variable_state(self, variable_name : str, new_state) -> Symbol:
        eligible_symbols_to_update = [symbol for symbol in self.scope_handler.current_symbols_scope.symbols if symbol.name == variable_name]
        if len(eligible_symbols_to_update) > 0:
            # In case multiple scopes declare a variable with the same name we take the last one, that is the one from the nearest scope.
            symbol_index_in_scope = self.scope_handler.current_symbols_scope.symbols.index(eligible_symbols_to_update[-1]) 
            symbol_to_update = self.scope_handler.current_symbols_scope.symbols[symbol_index_in_scope]

            # If new_state is a literal, we create an anonymous symbol to handle only this case from now on.
            if(not isinstance(new_state, Symbol)):
                delete_new_state_register = True
                new_state:Symbol = self.declare_anonymous_variable(QutesDataType.type_of(new_state), new_state, symbol_to_update.ast_token_index)
            delete_new_state_register = new_state.is_anonymous 
            value_to_assign = self.get_value(new_state)

        	# check if the type of the variable match the type of the value we are trying to assign. 
            value_to_assign_qutes_type = QutesDataType.type_of(value_to_assign)
            definition_qutes_type = symbol_to_update.symbol_declaration_static_type
            promoted_type = value_to_assign_qutes_type.promote_type(definition_qutes_type)
            down_cast_type = value_to_assign_qutes_type.down_cast_type(definition_qutes_type)
            final_type = definition_qutes_type

            # check if the type of the varible match the type of the value we are trying to assign. 
            if(value_to_assign_qutes_type != definition_qutes_type):
                # promote the current data type if needed.
                if(promoted_type != QutesDataType.undefined):
                    value_to_assign = self.type_casting_handler.promote_value_to_type(value_to_assign, value_to_assign_qutes_type, promoted_type, new_state)
                    final_type = promoted_type
                elif(down_cast_type != QutesDataType.undefined):
                    value_to_assign = self.type_casting_handler.down_cast_value_to_type(value_to_assign, value_to_assign_qutes_type, down_cast_type, new_state)
                    final_type = down_cast_type
                else:
                    raise TypeError(f"Cannot convert type '{definition_qutes_type}' to '{value_to_assign_qutes_type}' for '{variable_name}'.")

            # Update the variable value if everything is ok.
            symbol_to_update.value = value_to_assign #TODO: in case of arrays, we need to check whether the elements are of the same type, and if any type cast is needed.
            symbol_to_update.promoted_static_type = final_type

            #Handle quantum circuit update
            if(QutesDataType.is_quantum_type(symbol_to_update.symbol_declaration_static_type)):
                if(new_state.quantum_register == None):
                    symbol_to_update.quantum_register = self.quantum_circuit_handler.create_and_assign_quantum_register(variable_name, value_to_assign)
                else:
                    symbol_to_update.quantum_register = self.quantum_circuit_handler.assign_quantum_register_to_variable(variable_name, new_state.quantum_register)
                    if(delete_new_state_register):
                        self.delete_variable(new_state)
            return symbol_to_update
        else:
            raise SyntaxError(f"No variable declared with name '{variable_name}'.")
        
    def declare_variable(self, declaration_type : QutesDataType, variable_name : str, ast_token_index:int, value = None, declare_as_anonymous = False) -> Symbol:
        already_taken_symbol_in_this_scope = [symbol for symbol in self.scope_handler.current_symbols_scope.symbols if symbol.name == variable_name and symbol.parent_scope == self.scope_handler.current_symbols_scope]
        if(len(already_taken_symbol_in_this_scope) == 0):
            if(value is None):
                value = QutesDataType.get_default_value(declaration_type)
            else: 
                value = self.get_value(value)
            
            new_symbol = self.create_symbol(declaration_type, value, ast_token_index)
            new_symbol.name = variable_name
            new_symbol.is_anonymous = declare_as_anonymous
            self.scope_handler.current_symbols_scope.symbols.append(new_symbol)
            #Handle quantum circuit update
            if(QutesDataType.is_quantum_type(declaration_type)):
                new_symbol.quantum_register = self.quantum_circuit_handler.declare_quantum_register(variable_name, new_symbol.value)

            return new_symbol
        else:
            raise SyntaxError(f"Symbol with name '{variable_name}' already declared.")

    def declare_anonymous_variable(self, declaration_type : QutesDataType, value, ast_token_index:int) -> Symbol:
        return self.declare_variable(declaration_type, f"{QuantumCircuitHandler.anon_variable_name_prefix}_{next(QuantumCircuitHandler.anon_counter)}", ast_token_index, value, True)

    def delete_variable(self, symbol:Symbol) -> None:
        if symbol in self.scope_handler.current_symbols_scope.symbols:
            self.scope_handler.current_symbols_scope.symbols.remove(symbol)
        # TODO: check when is needed to delete registers.
        # if symbol.quantum_register != None:
        #     self.quantum_circuit_handler.remove_quantum_register(symbol.quantum_register)

    def create_symbol(self, qutes_type : QutesDataType, value, ast_token_index:int) -> Symbol:
        if(value is None):
            value = QutesDataType.get_default_value(qutes_type)

        #TODO: in case of arrays, we need to check whether the elements are of the same type, and if any type cast is needed.
        #      also we need to create a quantum register for the array if it is a quantum type.
        #      and modify type handler to return true for quantum check even for array types.
        variable_name = None
        value_qutes_type = QutesDataType.type_of(value)
        definition_type = qutes_type
        promoted_type = value_qutes_type.promote_type(definition_type)
        down_cast_type = value_qutes_type.down_cast_type(definition_type)
        final_type = definition_type

        # check if the type of the varible match the type of the value we are trying to assign. 
        if(value_qutes_type != definition_type):
            # promote the current data type if needed.
            if(promoted_type != QutesDataType.undefined):
                value = self.type_casting_handler.promote_value_to_type(value, value_qutes_type, promoted_type, None)
                final_type = promoted_type
            elif(down_cast_type != QutesDataType.undefined):
                value = self.type_casting_handler.down_cast_value_to_type(value, value_qutes_type, down_cast_type, None)
                final_type = down_cast_type
            else:
                raise TypeError(f"Cannot convert type '{definition_type}' to '{value_qutes_type}' for '{variable_name}'.")
            
        new_symbol = Symbol(variable_name, SymbolClass.VariableSymbol, qutes_type, final_type, value, self.scope_handler.current_symbols_scope, ast_token_index)
        return new_symbol
    
    def declare_function(self, anonymous_symbol : Symbol, function_name : str, input_params_definition:list[Symbol] = list(), value = None) -> Symbol:
        already_taken_symbol_in_this_scope = [symbol for symbol in self.scope_handler.current_symbols_scope.symbols if symbol.name == function_name and symbol.parent_scope == self.scope_handler.current_symbols_scope]
        if(len(already_taken_symbol_in_this_scope) == 0):
            anonymous_symbol.name = function_name
            anonymous_symbol.symbol_class = SymbolClass.FunctionSymbol
            anonymous_symbol.value = value
            anonymous_symbol.is_anonymous = False
            anonymous_symbol.function_input_params_definition = input_params_definition.copy()
            self.scope_handler.current_symbols_scope.symbols.append(anonymous_symbol)
            return anonymous_symbol
        else:
            raise SyntaxError(f"Symbol with name '{function_name}' already declared.")
    
    def get_value(self, var_value):
        if(isinstance(var_value, Symbol)):
            return var_value.value
        return var_value

    def get_variable_symbol(self, var_name:str, ast_token_index:int) -> Symbol:
        eligible_symbols = [symbol for symbol in self.scope_handler.current_symbols_scope.symbols if symbol.name == var_name and symbol.ast_token_index <= ast_token_index]
        if len(eligible_symbols) > 0:
            return eligible_symbols[-1]
        else:
            raise SyntaxError(f"No variable declared with name '{var_name}'.")
        
    def get_function_symbol(self, function_name:str, function_params:list[Symbol], ast_token_index:int) -> Symbol:
        eligible_symbols = [symbol for symbol in self.scope_handler.current_symbols_scope.symbols if symbol.function_matches_signature(function_name, function_params)]
        if len(eligible_symbols) > 0:
            return eligible_symbols[-1]
        else:
            raise SyntaxError(f"No function declared with name '{function_name}' and parameters {function_params}.")
    
    def get_type_of(self, var_value):
        if(isinstance(var_value, Symbol)):
            return var_value.symbol_declaration_static_type
        return QutesDataType.type_of(var_value)