from symbols.scope_tree_node import ScopeTreeNode, ScopeClass, ScopeStackNode
from symbols.symbol import Symbol
from anytree import PreOrderIter, RenderTree

class ScopeHandler():
    print_trace = False
    def __init__(self):
        self.symbols_tree:ScopeTreeNode = None
        self.current_symbols_scope:ScopeTreeNode = self.symbols_tree

class ScopeHandlerForSymbolsDiscovery(ScopeHandler):
    print_trace = ScopeHandler.print_trace
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

        # Add the new root
        if(not self.symbols_tree):
            self.symbols_tree = new_scope

        self.current_symbols_scope = new_scope

        if(ScopeHandlerForSymbolsDiscovery.print_trace and self.current_symbols_scope != None):
            print (f"push_scope: \n{RenderTree(self.current_symbols_scope)}")

        return self.current_symbols_scope
    
    def pop_scope(self) -> ScopeTreeNode:
        self.current_symbols_scope = self.current_symbols_scope.parent

        if(ScopeHandlerForSymbolsDiscovery.print_trace and self.current_symbols_scope != None):
            print (f"pop_scope: \n{RenderTree(self.current_symbols_scope)}")
        
        return self.current_symbols_scope

    
class ScopeHandlerForSymbolsUpdate(ScopeHandler):
    # Class that handles the compilation steps that come after the first(symbol discovery)
    # - We need to travers the symbols_tree going orderly like in a breadth first search
    # - Every time we need to create a new scope, we visit instead the next node in the tree
    # - And every time we need to close a scope, we return to the parent of the current node
    # - This way we know, at each moment, what symbols are defined.
    print_trace = ScopeHandler.print_trace
    def __init__(self, symbols_tree:ScopeTreeNode):
        super().__init__()
        if not symbols_tree:
            raise ValueError("A symbols tree must be provided to the scope handler for this step.")
        self.symbols_tree_root:ScopeTreeNode = symbols_tree
        self.current_symbols_scope:ScopeTreeNode = self.symbols_tree_root
        self.scopes_stack:list[ScopeStackNode] = [ScopeStackNode(self.current_symbols_scope, PreOrderIter(self.symbols_tree_root))]

    def restart_visiting_cycle_scope(self) -> None:
        """ This method must be called every time a loop cycle is executed
            It will reset the iterator to the current scope, so the next scope to be visited is the current scope again (otherwise the next sibling will be visited).
            This is achieved by creating a new iterator from the tree root and iterating until the current scope is reached again.
        """
        temp_iterator = PreOrderIter(self.symbols_tree_root)
        temp_node = None
        while temp_node != self.current_symbols_scope:
            temp_node = next(temp_iterator)
        self.scopes_stack[-1].scope_iterator = temp_iterator

    def create_function_inner_scope(self) -> ScopeStackNode:
        if(ScopeHandlerForSymbolsUpdate.print_trace and self.current_symbols_scope != None):
            print (f"create_function_inner_scope")
        return ScopeStackNode(self.current_symbols_scope, PreOrderIter(self.current_symbols_scope))

    def push_function_inner_scope(self, function_inner_scope:ScopeStackNode) -> None:
        self.scopes_stack.append(function_inner_scope)
        self.push_scope()
        if(ScopeHandlerForSymbolsUpdate.print_trace and self.current_symbols_scope != None):
            print (f"push_function_inner_scope")

    def pop_function_inner_scope(self, function_inner_scope:ScopeStackNode) -> None:
        self.pop_scope()
        self.scopes_stack.remove(function_inner_scope)
        if(ScopeHandlerForSymbolsUpdate.print_trace and self.current_symbols_scope != None):
            print (f"pop_function_inner_scope")

    #Start visiting scope
    def push_scope(self) -> ScopeTreeNode:
        nextNode = next(self.scopes_stack[-1].scope_iterator)
        if(ScopeHandlerForSymbolsUpdate.print_trace and nextNode != None):
            print (f"⬇push\n{RenderTree(nextNode)}")
        if(nextNode != None):
            self.current_symbols_scope = nextNode
        return self.current_symbols_scope
    
    #End visiting scope, return to parent and never(almost, see loops) visit this scope again
    def pop_scope(self) -> ScopeTreeNode:
        parentNode = self.current_symbols_scope.parent
        if(parentNode != None):
            self.current_symbols_scope = parentNode
        if(ScopeHandlerForSymbolsUpdate.print_trace and self.current_symbols_scope != None):
            print (f"⬆pop\n{RenderTree(self.current_symbols_scope)}")
        return self.current_symbols_scope