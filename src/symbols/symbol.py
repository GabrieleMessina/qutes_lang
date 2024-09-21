from enum import Enum, auto
from quantum_circuit import QuantumRegister, QuantumCircuit
from symbols.scope_tree_node import ScopeTreeNode
from symbols.types import QutesDataType

class SymbolClass(Enum):
    BaseSymbol = 1
    FunctionSymbol = auto()
    VariableSymbol = auto()

class Symbol():    
    verbose_print = False
    def __init__(self, 
                 name:str, 
                 symbol_class:SymbolClass, 
                 symbol_declaration_static_type:QutesDataType, 
                 casted_static_type:QutesDataType, 
                 value:any, 
                 parent_scope:ScopeTreeNode, 
                 ast_token_index:int, 
                 quantum_register : QuantumRegister | None = None, 
                 params = []):
        self.name:str = name
        self.symbol_class:SymbolClass = symbol_class
        self.symbol_declaration_static_type:QutesDataType = symbol_declaration_static_type
        self.casted_static_type:QutesDataType = casted_static_type #Promoted or Down Casted
        self.value = value #value is not reliable on quantum types, in case of arrays it contains an array of symbols. In case of functions it contains the ANTLR Function Body Context
        self.parent_scope:ScopeTreeNode = parent_scope
        self.inner_scope:ScopeTreeNode = None
        self.ast_token_index:int = ast_token_index
        self.is_return_value_of_function:bool = False
        self.is_anonymous:bool = False
        self.function_input_params_definition:list[Symbol] = params
        self.quantum_register:QuantumRegister | None = quantum_register #quantum_register is not used for classical variables,in case of array is None, in case of functions it contains the quantum register of the return value
        self.quantum_function:QuantumCircuit | None = None #quantum_function is not used for classical variables

    def function_matches_signature(self, function_name:str, function_params:list['Symbol']) -> bool:
        if self.symbol_class is not SymbolClass.FunctionSymbol:
            return False
        
        if(self.name == function_name and (len(function_params) == len(self.function_input_params_definition))):
            for index in range(len(function_params)):
                #TODO: if are not the same check if the second can be automaticly casted to the other.
                if(function_params[index].casted_static_type.value != self.function_input_params_definition[index].casted_static_type.value):
                    return False
            return True
        return False
    
    def is_classical(self) -> bool:
        return not QutesDataType.is_quantum_type(self.symbol_declaration_static_type)
    
    def is_quantum(self) -> bool:
        return QutesDataType.is_quantum_type(self.symbol_declaration_static_type)

    def is_array(self) -> bool:
        return QutesDataType.is_array_type(self.symbol_declaration_static_type)
    
    def __to_printable__(self) -> str:
        if(Symbol.verbose_print):
            if self.symbol_class is SymbolClass.FunctionSymbol:
                return f"{self.parent_scope.scope_type_detail}.{self.name}({self.function_input_params_definition}) -> {self.symbol_declaration_static_type.name}"
            else:
                return f"{self.symbol_declaration_static_type.name} {self.parent_scope.scope_type_detail}.{self.name} = {self.value}"
        else:
            if self.symbol_class is SymbolClass.FunctionSymbol:
                return f"{self.parent_scope.scope_type_detail}.{self.name}({self.function_input_params_definition}) -> {self.symbol_declaration_static_type.name}"
            else:
                return f"{self.value}"

    def __str__(self) -> str:
        return self.__to_printable__()

    def __repr__(self) -> str:
        return self.__to_printable__()