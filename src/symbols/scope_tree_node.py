"""A Node for the Scope Tree data structure"""
from anytree import NodeMixin
from enum import Enum, auto

class ScopeClass(Enum):
    BaseScope = 1
    GlobalScope = auto()
    LocalScope = auto()

class ScopeTreeNode(NodeMixin): #TODO: rename to ASTNode?
    """A Node for the Scope Tree data structure"""
        
    def __init__(self, scope_class:ScopeClass, scope_type_detail:str, parent=None, children=None, symbols:list['Symbol']=[]):
        super().__init__()
        self.symbols:list['Symbol'] = symbols.copy() # Contains all the symbols resolvable from this scope, so the symbols from this scope and from the ancestors of this node.
        self.scope_class = scope_class
        self.scope_type_detail = scope_type_detail
        self.parent = parent
        if children:
            self.children = children