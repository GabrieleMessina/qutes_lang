from symbols.scope_tree_node import ScopeTreeNode, ScopeClass
from symbols.symbol import Symbol
from anytree import PreOrderIter

class ScopeHandler():
    def __init__(self):
        self.symbols_tree:ScopeTreeNode = None
        self.current_symbols_scope:ScopeTreeNode = self.symbols_tree

class ScopeHandlerForSymbolsDiscovery(ScopeHandler):
    # Class that handles the scope for symbol discovery, first step of compilation
    def __init__(self):
        super().__init__()


    def push_scope(self, scope:ScopeClass, scope_detail:str, symbols:list[Symbol] = []) -> ScopeTreeNode:
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
    
    def push_inner_scope(self, scope:ScopeClass, scope_detail:str, symbol_owner:Symbol, symbols:list[Symbol] = []) -> ScopeTreeNode:
        inner_scope = self.push_scope(scope, scope_detail, symbols)
        symbol_owner.inner_scope = inner_scope
        return inner_scope
    
    def pop_scope(self) -> ScopeTreeNode:
        self.current_symbols_scope = self.current_symbols_scope.parent
        return self.current_symbols_scope

    
class ScopeHandlerForSymbolsUpdate(ScopeHandler):
    # Class that handles the compilation steps that come after the first(symbol discovery)
    def __init__(self, symbols_tree:ScopeTreeNode):
        super().__init__()
        if not symbols_tree:
            raise ValueError("A symbols tree must be provided to the scope handler for this step.")
        self.symbols_tree:ScopeTreeNode = symbols_tree
        self.current_symbols_scope:ScopeTreeNode = self.symbols_tree
        self.tree_preorder_iterator = PreOrderIter(self.symbols_tree)
        self.is_inside_loop = False
        self.is_inside_function = False

    def start_loop(self) -> None:
        self.is_inside_loop = True

    def end_loop(self) -> None:
        self.is_inside_loop = False

    def start_function(self) -> None:
        self.is_inside_function = True

    def end_function(self) -> None:
        self.is_inside_function = False

    #Start visiting scope
    def push_scope(self) -> ScopeTreeNode:
        if(self.is_inside_loop == False and self.is_inside_function == False):
            nextNode = next(self.tree_preorder_iterator)
            if(nextNode != None):
                self.current_symbols_scope = nextNode
        return self.current_symbols_scope
    
    #End visiting scope, return to parent and never(almost, see loops) visit this scope again
    def pop_scope(self) -> ScopeTreeNode:
        if(self.is_inside_loop == False and self.is_inside_function == False):
            parentNode = self.current_symbols_scope.parent
            if(parentNode != None):
                self.tree_preorder_iterator = PreOrderIter(parentNode)
                self.current_symbols_scope = next(self.tree_preorder_iterator)
        return self.current_symbols_scope