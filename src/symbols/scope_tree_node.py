"""A Node for the Scope Tree data structure"""
from anytree import NodeMixin
from enum import Enum
from symbols.quantum_circuit_handler import QuantumRegister

class ScopeType(Enum):
    BaseScope = 1
    GlobalScope = 2
    LocalScope = 3

class SymbolType(Enum):
    Symbol = 1
    FunctionSymbol = 2
    VariableSymbol = 3

class Symbol(): # TODO: extract from this file.
    name:str = None
    def __init__(self, name:str, symbol_type:SymbolType, symbol_type_detail:str, value, scope:"ScopeTreeNode", quantum_register : QuantumRegister | None = None):
        super().__init__()
        self.name = name
        self.symbol_type = symbol_type
        self.symbol_type_detail = symbol_type_detail
        self.value = value
        self.scope = scope
        self.quantum_register = quantum_register

    def __to_printable__(self) -> str:
        return f"{self.scope.scope_type_detail}.{self.name}={self.value}"

    def __str__(self) -> str:
        return self.__to_printable__()

    def __repr__(self) -> str:
        return self.__to_printable__()


class ScopeTreeNode(NodeMixin):
    """A Node for the Scope Tree data structure"""
    def __init__(self, scope_type:ScopeType, scope_type_detail:str, parent=None, children=None, symbols:list[Symbol]=[]):
        super().__init__()
        self.symbols:list[Symbol] = symbols.copy() # Contains all the symbols resolvable from this scope, so the symbols from this scope and from the ancestors of this node.
        self.scope_type = scope_type
        self.scope_type_detail = scope_type_detail
        self.parent = parent
        if children:
            self.children = children