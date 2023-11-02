from symbols.scope_tree_node import ScopeTreeNode, ScopeType, Symbol
from anytree import PreOrderIter

class ScopeHandlerForSymbolsDiscovery():
    # Class that handles the scope for symbol discovery, first step of compilation
    def __init__(self):
        self.symbols_tree:ScopeTreeNode = None
        self.current_symbols_scope:ScopeTreeNode = self.symbols_tree


    def push_scope(self, scope:ScopeType, scope_detail:str, symbols:list[Symbol] = []) -> ScopeTreeNode:
        _symbols:list[Symbol] = symbols.copy()
        if(self.current_symbols_scope):
            _symbols += self.current_symbols_scope.symbols
        new_scope = ScopeTreeNode(scope, scope_detail, self.current_symbols_scope, symbols=_symbols)
        # this cross reference is handled by anytree.
        # if(self.current_symbols_scope):
        #     if(self.current_symbols_scope.children):
        #         self.current_symbols_scope.children = list(self.current_symbols_scope.children) + [new_scope]
        #     else: self.current_symbols_scope.children = [new_scope]

        if(not self.symbols_tree):
            self.symbols_tree = new_scope

        self.current_symbols_scope = new_scope
        return self.current_symbols_scope
    
    def pop_scope(self) -> ScopeTreeNode:
        self.current_symbols_scope = self.current_symbols_scope.parent
        return self.current_symbols_scope

    
class ScopeHandlerForSymbolsUpdate():
    # Class that handles the compilation steps that come after the first(symbol discovery)
    def __init__(self, symbols_tree:ScopeTreeNode):
        if not symbols_tree:
            raise ValueError("A symbols tree must be provided to the scope handler for this step.")
        self.symbols_tree:ScopeTreeNode = symbols_tree
        self.current_symbols_scope:ScopeTreeNode = None
        self.tree_preorder_iterator = PreOrderIter(self.symbols_tree)            

    def push_scope(self) -> ScopeTreeNode:
        self.current_symbols_scope = next(self.tree_preorder_iterator)
        return self.current_symbols_scope
    
    def pop_scope(self) -> ScopeTreeNode:
        return self.current_symbols_scope