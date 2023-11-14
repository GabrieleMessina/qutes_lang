from enum import Enum, auto
from quantum_circuit import QuantumRegister

class SymbolClass(Enum):
    BaseSymbol = 1
    FunctionSymbol = auto()
    VariableSymbol = auto()

class Symbol():    
    def __init__(self, name:str, symbol_class:SymbolClass, symbol_declaration_static_type:str, value, scope:'ScopeNode', quantum_register : QuantumRegister | None = None):
        super().__init__()
        self.name = name
        self.symbol_class = symbol_class
        self.symbol_declaration_static_type = symbol_declaration_static_type
        self.value = value
        self.scope = scope
        self.quantum_register = quantum_register

    def __to_printable__(self) -> str:
        return f"{self.scope.scope_type_detail}.{self.name}={self.value}"

    def __str__(self) -> str:
        return self.__to_printable__()

    def __repr__(self) -> str:
        return self.__to_printable__()