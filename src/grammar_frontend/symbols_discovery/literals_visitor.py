from grammar_frontend.shared.qutes_parser import QutesParser as qutes_parser
from symbols.scope_tree_node import ScopeTreeNode
from symbols.symbol import Symbol
from symbols.scope_handler import ScopeHandlerForSymbolsUpdate, ScopeHandlerForSymbolsDiscovery
from symbols.variables_handler import VariablesHandler
from quantum_circuit.quantum_circuit_handler import QuantumCircuitHandler
from grammar_frontend.shared.qutes_base_visitor import QutesBaseVisitor

class LiteralsVisitor(QutesBaseVisitor):
    def __init__(self, symbols_tree:ScopeTreeNode, quantum_circuit_handler : QuantumCircuitHandler, scope_handler:ScopeHandlerForSymbolsUpdate|ScopeHandlerForSymbolsDiscovery, variables_handler:VariablesHandler, verbose:bool = False):
        super().__init__(symbols_tree, quantum_circuit_handler, scope_handler, variables_handler, verbose)
    
    def visitType(self, ctx:qutes_parser.TypeContext):
        return ctx.getText()
    
    def visitFunctionDeclarationParams(self, ctx:qutes_parser.FunctionDeclarationParamsContext):
        head = [self.visit(ctx.variableDeclaration())]
        tail = []
        if ctx.functionDeclarationParams():
            tail = self.visit(ctx.functionDeclarationParams()) #recursion
            if not isinstance(tail, list):
                tail = [tail]
            head.extend(tail)
        return head

    def visitTermList(self, ctx:qutes_parser.TermListContext) -> list[Symbol]:
        head = [self.visit(ctx.expr())]
        tail = []
        if ctx.termList():
            tail = self.visit(ctx.termList()) #recursion
            if not isinstance(tail, list):
                tail = [tail]
            head.extend(tail)
        return head

    def visitVariableType(self, ctx:qutes_parser.VariableTypeContext):
        value = str(ctx.getText())
        if self.log_code_structure: print(value, end=None)
        return value

    def visitQualifiedName(self, ctx:qutes_parser.QualifiedNameContext):
        var_name = str(ctx.getText())
        if ctx.variableName():
            var_name = self.visit(ctx.variableName())
        if ctx.functionName():
            var_name = self.visit(ctx.functionName())
        token_index = ctx.start.tokenIndex
        symbol_to_resolve = self.variables_handler.get_variable_symbol(var_name, token_index)
        if self.log_code_structure: print(symbol_to_resolve, end=None)
        return self.variables_handler.get_variable_symbol(var_name, token_index)

    def visitVariableName(self, ctx:qutes_parser.VariableNameContext):
        value = str(ctx.getText())
        if self.log_code_structure: print(value, end=None)
        return value

    def visitFunctionName(self, ctx:qutes_parser.FunctionNameContext):
        value = str(ctx.getText())
        if self.log_code_structure: print(value, end=None)
        return value