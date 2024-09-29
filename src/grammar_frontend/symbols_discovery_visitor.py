"""An antlr listener for the qutes grammar."""

from qutes_antlr.qutes_parserVisitor import qutes_parserVisitor as qutesVisitor
from qutes_antlr.qutes_parser import qutes_parser as qutesParser
from symbols.scope_tree_node import ScopeClass
from symbols.scope_handler import ScopeHandlerForSymbolsDiscovery
from symbols.variables_handler import VariablesHandler
from symbols.types import QutesDataType
from symbols import Symbol
from quantum_circuit import QuantumCircuitHandler

class SymbolsDiscoveryVisitor(qutesVisitor):
    """An antlr visitor for the qutes grammar that discovers symbols like variable, function names etc."""

    def __init__(self, quantum_circuit_handler : QuantumCircuitHandler, verbose:bool = False):
        self.quantum_circuit_handler = quantum_circuit_handler
        self.verbose = verbose
        self.scope_handler = ScopeHandlerForSymbolsDiscovery()
        self.scope_count = 0
        self.if_else_scope_count = 0
        self.loop_scope_count = 0
        self.function_scope_count = 0
        self.variables_handler = VariablesHandler(self.scope_handler, self.quantum_circuit_handler)
        
        ScopeHandlerForSymbolsDiscovery.print_trace = False

    def visitProgram(self, ctx:qutesParser.ProgramContext):
        self.scope_handler.push_scope(ScopeClass.GlobalScope, "GlobalScope")
        self.visitChildren(ctx)
        self.scope_handler.pop_scope()

    # visit a parse tree produced by qutesParser#IfStatement.
    def visitIfStatement(self, ctx:qutesParser.IfStatementContext):
        self.if_else_scope_count += 1
        self.scope_handler.push_scope(ScopeClass.IfElseScope, f"If{self.if_else_scope_count}")
        self.visitChildren(ctx)
        self.scope_handler.pop_scope()


    # visit a parse tree produced by qutesParser#IfElseStatement.
    def visitIfElseStatement(self, ctx:qutesParser.IfElseStatementContext):
        self.if_else_scope_count += 1
        self.scope_handler.push_scope(ScopeClass.IfElseScope, f"IfElse{self.if_else_scope_count}")
        self.visitChildren(ctx)
        self.scope_handler.pop_scope()


    # visit a parse tree produced by qutesParser#ForeachStatement.
    def visitForeachStatement(self, ctx:qutesParser.ForeachStatementContext):
        self.loop_scope_count += 1
        self.scope_handler.push_scope(ScopeClass.LoopScope, f"Foreach{self.loop_scope_count}")
        
        token_index = ctx.start.tokenIndex
        
        array_symbol:Symbol = self.variables_handler.get_variable_symbol(ctx.qualifiedName().getText(), token_index) 
        auxiliary_var_name = ctx.variableName(0).getText()
        auxiliary_qutes_type = QutesDataType.get_unit_type_from_array_type(array_symbol.symbol_declaration_static_type)

        self.variables_handler.declare_variable(auxiliary_qutes_type, auxiliary_var_name, token_index)
        
        if ctx.variableName(1):
            index_var_name = ctx.variableName(1).getText()
            self.variables_handler.declare_variable(QutesDataType.int, index_var_name, token_index)

        self.visitChildren(ctx)
        self.scope_handler.pop_scope()

    # visit a parse tree produced by qutesParser#WhileStatement.
    def visitWhileStatement(self, ctx:qutesParser.WhileStatementContext):
        self.loop_scope_count += 1
        self.scope_handler.push_scope(ScopeClass.LoopScope, f"While{self.loop_scope_count}")
        self.visitChildren(ctx)
        self.scope_handler.pop_scope()


    # visit a parse tree produced by qutesParser#DoWhileStatement.
    def visitDoWhileStatement(self, ctx:qutesParser.DoWhileStatementContext):
        self.loop_scope_count += 1
        self.scope_handler.push_scope(ScopeClass.LoopScope, f"DoWhile{self.loop_scope_count}")
        self.visitChildren(ctx)
        self.scope_handler.pop_scope()


    # visit a parse tree produced by qutesParser#BlockStatement.
    def visitBlockStatement(self, ctx:qutesParser.BlockStatementContext):
        self.scope_count += 1
        self.scope_handler.push_scope(ScopeClass.BlockScope, f"Block{self.scope_count}")
        self.visitChildren(ctx)
        self.scope_handler.pop_scope()


    # visit a parse tree produced by qutes_parser#FunctionStatement.
    def visitFunctionStatement(self, ctx:qutesParser.FunctionStatementContext):
        self.function_scope_count += 1
        return_type = ctx.variableType().getText()
        qutes_type = QutesDataType.from_string_type(return_type)
        function_name = ctx.functionName().getText()
        function_body = ctx.statement()

        token_index = ctx.start.tokenIndex
        function_symbol = self.variables_handler.declare_anonymous_variable(qutes_type, QutesDataType.get_default_value(qutes_type), token_index)
        function_symbol = self.variables_handler.declare_function(function_symbol, function_name, [], function_body)
        self.scope_handler.push_scope(ScopeClass.FunctionScope, f"Function{self.function_scope_count}")

        input_params_declaration = []
        if(ctx.functionDeclarationParams()):
            input_params_declaration = self.visit(ctx.functionDeclarationParams())
        function_symbol.function_input_params_definition = input_params_declaration

        self.visit(ctx.statement())
        self.scope_handler.pop_scope()

    # Visit a parse tree produced by qutes_parser#functionParams.
    def visitFunctionDeclarationParams(self, ctx:qutesParser.FunctionDeclarationParamsContext):
        head = [self.visit(ctx.variableDeclaration())]
        tail = []
        if(ctx.functionDeclarationParams()):
            tail = self.visit(ctx.functionDeclarationParams()) #recursion
            if(not isinstance(tail, list)):
                tail = [tail]
            head.extend(tail)
        return head

    # visit a parse tree produced by qutes_parser#variableDeclaration.
    def visitVariableDeclaration(self, ctx:qutesParser.VariableDeclarationContext):
        var_type = ctx.variableType().getText()
        var_name = ctx.variableName().getText()
        qutes_type = QutesDataType.from_string_type(var_type)
        # This listener should not follow the execution path to understand what was the initial value assigned to the variable.
        # So we assign None and then variables_handler will put in the default value for the type.
        if(ctx.expr()):
            self.visit(ctx.expr())
        

        token_index = ctx.start.tokenIndex
        # Variable should be declared after expr is evaluated.
        result = self.variables_handler.declare_variable(qutes_type, var_name, token_index)
        return result
