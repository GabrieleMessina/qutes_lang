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
    
    def get_next_sibling(self):
        """ Get the next sibling of the current scope node. """
        current_node_index = self.parent.children.index(self)
        parent_children = self.parent.children
        if len(parent_children) > current_node_index + 1:
            return parent_children[current_node_index + 1]
        return None
    
class ScopeStackNode():        
    def __init__(self, root_scope_node:ScopeTreeNode):
        self.root_scope_node:ScopeTreeNode = root_scope_node
        self._current_scope_node:ScopeTreeNode = None
        self._scope_iterator:PreOrderIter = None
        self.reset()

    def reset(self):
        self._scope_iterator = PreOrderIter(self.root_scope_node)
        self._current_scope_node = None

    def copy(self):
        iterator = PreOrderIter(self.root_scope_node)
        if self._current_scope_node:
            iterator = PreOrderIter(self._current_scope_node)
            next(iterator)
        new_scope = ScopeStackNode(self.root_scope_node)
        new_scope._scope_iterator = iterator
        new_scope._current_scope_node = self._current_scope_node
        return new_scope
    
    def __to_printable__(self) -> str:
        return f"{self.__class__.__qualname__}:{self.root_scope_node}"

    def __str__(self) -> str:
        return self.__to_printable__()

    def __repr__(self) -> str:
        return self.__to_printable__()