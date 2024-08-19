from symbols.scope_tree_node import ScopeTreeNode, ScopeClass
from symbols.symbol import Symbol
from anytree import PreOrderIter, RenderTree

class ScopeHandler():
    print_trace = False
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

        if(ScopeHandler.print_trace and self.current_symbols_scope != None):
            print (f"push_scope: \n{RenderTree(self.current_symbols_scope)}")

        return self.current_symbols_scope
    
    def push_inner_scope(self, scope:ScopeClass, scope_detail:str, symbol_owner:Symbol, symbols:list[Symbol] = []) -> ScopeTreeNode:
        inner_scope = self.push_scope(scope, scope_detail, symbols)
        symbol_owner.inner_scope = inner_scope
        return inner_scope
    
    def pop_scope(self) -> ScopeTreeNode:
        self.current_symbols_scope = self.current_symbols_scope.parent

        if(ScopeHandler.print_trace and self.current_symbols_scope != None):
            print (f"pop_scope: \n{RenderTree(self.current_symbols_scope)}")
        
        return self.current_symbols_scope

    
class ScopeHandlerForSymbolsUpdate(ScopeHandler):
    # Class that handles the compilation steps that come after the first(symbol discovery)
    # - We need to travers the symbols_tree going orderly like in a breadth first search
    # - Every time we need to create a new scope, we visit instead the next node in the tree
    # - And every time we need to close a scope, we return to the parent of the current node
    # - This way we know, at each moment, what symbols are defined.
    def __init__(self, symbols_tree:ScopeTreeNode):
        super().__init__()
        if not symbols_tree:
            raise ValueError("A symbols tree must be provided to the scope handler for this step.")
        self.symbols_tree:ScopeTreeNode = symbols_tree
        self.current_symbols_scope:ScopeTreeNode = self.symbols_tree
        self.tree_preorder_iterator = PreOrderIter(self.symbols_tree)
        self.is_inside_loop = False
        self.loop_inner_scope = None
        self.is_inside_function = False

    def start_loop(self) -> None:
        self.is_inside_loop = True
        self.loop_inner_scope = self.current_symbols_scope

    def handle_loop_cycle(self) -> None:
        temp_iterator = PreOrderIter(self.symbols_tree)
        temp_node = None
        while temp_node != self.current_symbols_scope:
            temp_node = next(temp_iterator)
        self.tree_preorder_iterator = temp_iterator

    def end_loop(self) -> None:
        self.is_inside_loop = False
        self.loop_inner_scope = None

    def start_function(self) -> None:
        self.is_inside_function = True

    def end_function(self) -> None:
        self.is_inside_function = False

    #Start visiting scope
    def push_scope(self, tree_iterator = None) -> ScopeTreeNode:
        if tree_iterator != None:
            self.tree_preorder_iterator = tree_iterator
        if(self.is_inside_function == False):
            nextNode = next(self.tree_preorder_iterator)
            if(ScopeHandler.print_trace and nextNode != None):
                print (f"push_scope: \n{RenderTree(nextNode)}")
            if(nextNode != None):
                self.current_symbols_scope = nextNode
        return self.current_symbols_scope
    
    #End visiting scope, return to parent and never(almost, see loops) visit this scope again
    def pop_scope(self) -> ScopeTreeNode:
        if(self.is_inside_function == False):
            parentNode = self.current_symbols_scope.parent
            if(parentNode != None):
                self.current_symbols_scope = parentNode
            if(ScopeHandler.print_trace and self.current_symbols_scope != None):
                print (f"pop_scope: \n{RenderTree(self.current_symbols_scope)}")
        return self.current_symbols_scope