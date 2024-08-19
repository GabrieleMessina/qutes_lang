from grammar_frontend.qutes_parser import QutesParser as qutes_parser
from symbols.scope_tree_node import ScopeTreeNode
from symbols.symbol import Symbol, SymbolClass
from symbols.scope_handler import ScopeHandlerForSymbolsUpdate
from symbols.variables_handler import VariablesHandler
from quantum_circuit import QuantumCircuitHandler
from grammar_frontend.qutes_base_visitor import QutesBaseVisitor
from symbols.types import QutesDataType

class QutesGrammarExpressionVisitor(QutesBaseVisitor):
    def __init__(self, symbols_tree:ScopeTreeNode, quantum_circuit_handler : QuantumCircuitHandler, scope_handler:ScopeHandlerForSymbolsUpdate, variables_handler:VariablesHandler, verbose:bool = False):
        super().__init__(symbols_tree, quantum_circuit_handler, scope_handler, variables_handler, verbose)

    def visitExpr(self, ctx:qutes_parser.ExprContext):
        return self.visitChildren(ctx)
    
    def visitParentesizeExpression(self, ctx:qutes_parser.ParentesizeExpressionContext):
        return self.visit(ctx.expr())

    def visitLiteralExpression(self, ctx:qutes_parser.LiteralExpressionContext):
        return self.visit(ctx.literal())
    
    def visitQualifiedNameExpression(self, ctx:qutes_parser.QualifiedNameExpressionContext):
        return self.visit(ctx.qualifiedName())
    
    def visitArrayExpression(self, ctx:qutes_parser.ArrayExpressionContext):
        return self.visit(ctx.array())

    def visitFunctionCallExpression(self, ctx:qutes_parser.FunctionCallExpressionContext):
        function_name = self.visit(ctx.functionName())
        function_params:list[Symbol] = []
        if(ctx.termList()):
            function_params = self.visit(ctx.termList())
        result:Symbol = self.__visitFunctionCall(function_name, function_params, ctx.start.tokenIndex)
        #TODO: staff commented for make return value work for quantum variable, do some tests to assure the behaviour is correct
        # function_symbol = self.variables_handler.get_function_symbol(function_name, ctx.start.tokenIndex, function_params)
        # self.quantum_cirtcuit_handler.push_compose_circuit_operation(function_symbol.quantum_function)
        return result

    def __visitFunctionCall(self, function_name, function_params, tokenIndex):
        self.scope_handler.start_function() #To avoid block statement to push its scope

        function_symbol = self.variables_handler.get_function_symbol(function_name, tokenIndex, function_params)  

        scope_to_restore_on_exit = self.scope_handler.current_symbols_scope
        self.scope_handler.current_symbols_scope = function_symbol.inner_scope
        
        default_params_to_restore_on_exit = function_symbol.function_input_params_definition.copy()

        symbol_params_to_push = []
        for index in range(len(function_params)):
            symbol_to_push = default_params_to_restore_on_exit[index]
            symbol_to_push.value = function_params[index].value
            symbol_to_push.quantum_register = function_params[index].quantum_register
            symbol_params_to_push.append(symbol_to_push)
        [symbol for symbol in function_symbol.inner_scope.symbols if symbol.symbol_class == SymbolClass.FunctionSymbol][:len(function_params)] = symbol_params_to_push

        #TODO: staff commented for make return value work for quantum variable, do some tests to assure the behaviour is correct
        # self.quantum_cirtcuit_handler.start_quantum_function()
        result = self.visitChildren(function_symbol.value)
        # gate = self.quantum_cirtcuit_handler.end_quantum_function(function_symbol.name)
        # function_symbol.quantum_function = gate

        self.scope_handler.current_symbols_scope = scope_to_restore_on_exit
        [symbol for symbol in function_symbol.inner_scope.symbols if symbol.symbol_class == SymbolClass.FunctionSymbol][:len(function_params)] = default_params_to_restore_on_exit

        self.scope_handler.end_function()
        return result
    
    def visitArrayAccessExpression(self, ctx:qutes_parser.ArrayAccessExpressionContext):
        array_symbol:Symbol = self.visit(ctx.expr(0))
        index_symbol:Symbol = self.visit(ctx.expr(1))

        array_value = self.variables_handler.get_value(array_symbol)
        index_value = self.variables_handler.get_value(index_symbol)
        
        value = array_value[index_value] 
        if not isinstance(value, Symbol):
            value = self.variables_handler.declare_anonymous_variable(QutesDataType.get_unit_type_from_array_type(array_symbol.casted_static_type), value, array_symbol.ast_token_index)
        return value
