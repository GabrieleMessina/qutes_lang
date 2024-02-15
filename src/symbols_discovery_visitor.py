"""An antlr listener for the qutes grammar."""

from qutes_antlr.qutes_parserVisitor import qutes_parserVisitor as qutesVisitor
from qutes_antlr.qutes_parser import qutes_parser as qutesParser
from symbols.scope_tree_node import ScopeClass
from symbols.scope_handler import ScopeHandlerForSymbolsDiscovery
from symbols.variables_handler import VariablesHandler
from symbols.types import QutesDataType
from quantum_circuit import QuantumCircuitHandler

class SymbolsDiscoveryVisitor(qutesVisitor):
    """An antlr visitor for the qutes grammar that discovers symbols like variable, function names etc."""

    def __init__(self, quantum_cirtcuit_handler : QuantumCircuitHandler):
        self.quantum_cirtcuit_handler = quantum_cirtcuit_handler
        self.scope_handler = ScopeHandlerForSymbolsDiscovery()
        self.scope_count = 0
        self.if_else_scope_count = 0
        self.loop_scope_count = 0
        self.function_scope_count = 0
        self.variables_handler = VariablesHandler(self.scope_handler, self.quantum_cirtcuit_handler)

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
        if(self.scope_handler.current_symbols_scope.scope_class == ScopeClass.IfElseScope):
            self.scope_handler.push_scope(ScopeClass.BranchScope, f"BranchBlock{self.if_else_scope_count}")
        elif(self.scope_handler.current_symbols_scope.scope_class == ScopeClass.LoopScope):
            self.scope_handler.push_scope(ScopeClass.BranchScope, f"BranchBlock{self.loop_scope_count}")
        elif(self.scope_handler.current_symbols_scope.scope_class == ScopeClass.FunctionScope):
            #self.scope_handler.push_scope(ScopeClass.FunctionBlockScope, f"FunctionBlock{self.function_scope_count}")
            pass
        else:
            self.scope_count += 1
            self.scope_handler.push_scope(ScopeClass.LocalScope, f"Block{self.scope_count}")

        self.visitChildren(ctx)

        if(self.scope_handler.current_symbols_scope.scope_class == ScopeClass.FunctionScope):
            pass
        else:
            self.scope_handler.pop_scope()


    # visit a parse tree produced by qutes_parser#FunctionStatement.
    def visitFunctionStatement(self, ctx:qutesParser.FunctionStatementContext):
        self.function_scope_count += 1
        return_type = ctx.variableType().getText()
        qutes_type = QutesDataType.from_string_type(return_type)
        function_name = ctx.functionName().getText()
        function_body = ctx.statement()

        token_index = ctx.start.tokenIndex
        funtion_symbol = self.variables_handler.create_anonymous_symbol(qutes_type, QutesDataType.get_default_value(qutes_type), token_index)
        funtion_symbol = self.variables_handler.declare_function(funtion_symbol, function_name, [], function_body)
        self.scope_handler.push_inner_scope(ScopeClass.FunctionScope, f"Function{self.function_scope_count}", funtion_symbol)

        input_params_declaration = []
        if(ctx.functionDeclarationParams()):
            input_params_declaration = self.visit(ctx.functionDeclarationParams())
        input_params_declaration.reverse()
        funtion_symbol.function_input_params_definition = input_params_declaration

        self.visitChildren(ctx.statement())
        self.scope_handler.pop_scope()

    # Visit a parse tree produced by qutes_parser#functionParams.
    def visitFunctionDeclarationParams(self, ctx:qutesParser.FunctionDeclarationParamsContext):
        param = self.visit(ctx.variableDeclaration())
        params = []
        if(ctx.functionDeclarationParams()):
            params = self.visit(ctx.functionDeclarationParams())
            if(not isinstance(params, list)):
                params = [params]
        params.append(param)
        return params

    # visit a parse tree produced by qutes_parser#variableDeclaration.
    def visitVariableDeclaration(self, ctx:qutesParser.VariableDeclarationContext):
        var_type = ctx.variableType().getText()
        var_name = ctx.variableName().getText()
        qutes_type = QutesDataType.from_string_type(var_type)
        # This listener should not follow the execution path to understand what was the initial value assigned to the variable.
        # So we assign None and then variables_handler will put in the default value for the type.
        token_index = ctx.start.tokenIndex
        return self.variables_handler.declare_variable(qutes_type, var_name, token_index)
