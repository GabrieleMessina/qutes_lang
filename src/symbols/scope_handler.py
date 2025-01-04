from symbols.scope_tree_node import ScopeTreeNode, ScopeClass, ScopeStackNode
from symbols.symbol import Symbol, SymbolClass
from anytree import PreOrderIter, RenderTree

class ScopeHandler():
    print_trace = False
    def __init__(self):
        self.current_symbols_scope:ScopeTreeNode = None

class ScopeHandlerForSymbolsDiscovery(ScopeHandler):
    print_trace = ScopeHandler.print_trace
    # Class that handles the scope for symbol discovery, first step of compilation
    def __init__(self):
        super().__init__()
        self._symbols_tree_root:ScopeTreeNode = None

    def push_scope(self, scope:ScopeClass, scope_detail:str) -> ScopeTreeNode:
        symbols:list[Symbol] = []
        if(self.current_symbols_scope):
            symbols += self.current_symbols_scope.symbols
        new_scope = ScopeTreeNode(scope, scope_detail, self.current_symbols_scope, symbols=symbols)
        # this cross reference is handled by anytree.
        # if(self.current_symbols_scope):
        #     if(self.current_symbols_scope.children):
        #         self.current_symbols_scope.children = list(self.current_symbols_scope.children) + [new_scope]
        #     else: self.current_symbols_scope.children = [new_scope]

        # Add the new root
        if(not self._symbols_tree_root):
            self._symbols_tree_root = new_scope

        self.current_symbols_scope = new_scope

        if(ScopeHandlerForSymbolsDiscovery.print_trace and self.current_symbols_scope != None):
            print (f"push_scope: \n{RenderTree(self.current_symbols_scope)}")

        return self.current_symbols_scope
    
    def pop_scope(self) -> ScopeTreeNode:
        self.current_symbols_scope = self.current_symbols_scope.parent

        if(ScopeHandlerForSymbolsDiscovery.print_trace and self.current_symbols_scope != None):
            print (f"pop_scope: \n{RenderTree(self.current_symbols_scope)}")
        
        return self.current_symbols_scope
    
    def get_symbols_tree(self) -> ScopeTreeNode:
        iter = PreOrderIter(self._symbols_tree_root)
        node = next(iter, None)
        while (node):
            if(node.children):
                for child in node.children:
                    for symbol in node.symbols:
                        if symbol not in child.symbols and symbol.symbol_class == SymbolClass.FunctionSymbol:
                            # we allow only function to be used before declaration
                            # and we don't want duplicates
                            child.symbols.append(symbol)
            node = next(iter, None)

        return self._symbols_tree_root
    
    
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
        self._symbols_tree_root:ScopeTreeNode = symbols_tree
        self.current_symbols_scope:ScopeTreeNode = self._symbols_tree_root
        self._scopes_stack:list[ScopeStackNode] = [ScopeStackNode(self.current_symbols_scope, PreOrderIter(self._symbols_tree_root))]

    def restart_visiting_cycle_scope(self) -> None:
        """ This method must be called every time a loop cycle is executed
            It will reset the iterator to the current scope, so the next scope to be visited is the current scope again (otherwise the next sibling will be visited).
            This is achieved by creating a new iterator from the tree root and iterating until the current scope is reached again.
        """
        temp_iterator = PreOrderIter(self._symbols_tree_root)
        temp_node = None
        while temp_node != self.current_symbols_scope:
            temp_node = next(temp_iterator)
        self._scopes_stack[-1].scope_iterator = temp_iterator

    def create_function_inner_scope(self) -> ScopeStackNode:
        if(ScopeHandlerForSymbolsUpdate.print_trace and self.current_symbols_scope != None):
            print (f"create_function_inner_scope")
        # Skip function scope visiting (deferred to the function call) jumping directly to next sibling
        parent_children = list(self.current_symbols_scope.parent.children)
        function_index_in_parent = parent_children.index(self.current_symbols_scope)
        next_child = parent_children[function_index_in_parent + 1] if function_index_in_parent + 1 < len(parent_children) else None
        self._scopes_stack[-1].scope_iterator = PreOrderIter(next_child) if next_child else None
        return ScopeStackNode(self.current_symbols_scope, PreOrderIter(self.current_symbols_scope))

    def push_function_inner_scope(self, function_inner_scope:ScopeStackNode) -> None:
        self._scopes_stack[-1].current_scope_node = self.current_symbols_scope
        self._scopes_stack.append(function_inner_scope.copy())
        self.push_scope()
        if(ScopeHandlerForSymbolsUpdate.print_trace and self.current_symbols_scope != None):
            print (f"push_function_inner_scope")

    def pop_function_inner_scope(self, function_inner_scope:ScopeStackNode) -> None:
        self.pop_scope()
        self._scopes_stack.pop()
        self.current_symbols_scope = self._scopes_stack[-1].current_scope_node
        if(ScopeHandlerForSymbolsUpdate.print_trace and self.current_symbols_scope != None):
            print (f"pop_function_inner_scope")

    #Start visiting scope
    def push_scope(self) -> ScopeTreeNode:
        nextNode = next(self._scopes_stack[-1].scope_iterator)
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