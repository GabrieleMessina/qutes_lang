"""A Node for the Scope Tree data structure"""
from anytree import NodeMixin, PreOrderIter
from enum import Enum, auto

class ScopeClass(Enum):
    BaseScope = 1
    GlobalScope = auto()
    BlockScope = auto()
    IfElseScope = auto()
    LoopScope = auto()
    BranchScope = auto()
    FunctionScope = auto()

class ScopeTreeNode(NodeMixin):
    """A Node for the Scope Tree data structure"""
        
    def __init__(self, scope_class:ScopeClass, scope_type_detail:str, parent=None, children=None, symbols:list['Symbol']=[]):
        super().__init__()
        self.symbols:list['Symbol'] = symbols.copy() # Contains all the symbols resolvable from this scope, so the symbols from this scope and from the ancestors of this node.
        self.scope_class = scope_class
        self.scope_type_detail = scope_type_detail
        self.parent = parent
        if children:
            self.children = children
    
    def __to_printable__(self) -> str:
        if self.parent:
            return f"{self.scope_class}/{self.scope_type_detail}: {[a for a in self.symbols]}"
        else:
            return f"{self.scope_class}/{self.scope_type_detail}: {self.symbols}"

    def __str__(self) -> str:
        return self.__to_printable__()

    def __repr__(self) -> str:
        return self.__to_printable__()
    
class ScopeStackNode():        
    def __init__(self, scope_node:ScopeTreeNode, scope_iterator:PreOrderIter, current_scope_node:ScopeTreeNode = None):
        self.root_scope_node = scope_node
        self.current_scope_node = current_scope_node
        self.scope_iterator = scope_iterator

    def copy(self):
        iterator = PreOrderIter(self.root_scope_node)
        if self.current_scope_node:
            iterator = PreOrderIter(self.current_scope_node)
            next(iterator)
        return ScopeStackNode(self.root_scope_node, iterator, self.current_scope_node)
    
    def __to_printable__(self) -> str:
        return f"stack:{self.root_scope_node}"

    def __str__(self) -> str:
        return self.__to_printable__()

    def __repr__(self) -> str:
        return self.__to_printable__()