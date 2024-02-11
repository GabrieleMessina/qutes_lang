"""An antlr listener for the qutes grammar."""

from qutes_antlr.qutes_parserListener import qutes_parserListener as qutesListener
from qutes_antlr.qutes_parser import qutes_parser as qutesParser
from symbols.scope_tree_node import ScopeClass
from symbols.scope_handler import ScopeHandlerForSymbolsDiscovery
from symbols.variables_handler import VariablesHandler
from symbols.types import QutesDataType
from quantum_circuit import QuantumCircuitHandler

class SymbolsDiscoveryListener(qutesListener):
    """An antlr listener for the qutes grammar that discovers symbols like variable, function names etc."""

    def __init__(self, quantum_cirtcuit_handler : QuantumCircuitHandler):
        self.quantum_cirtcuit_handler = quantum_cirtcuit_handler
        self.scope_handler = ScopeHandlerForSymbolsDiscovery()
        self.scope_count = 0
        self.if_else_scope_count = 0
        self.loop_scope_count = 0
        self.function_scope_count = 0
        self.variables_handler = VariablesHandler(self.scope_handler, self.quantum_cirtcuit_handler)

    # Enter a parse tree produced by qutesParser#program.
    def enterProgram(self, ctx:qutesParser.ProgramContext):
        self.scope_handler.push_scope(ScopeClass.GlobalScope, "GlobalScope")

    # Exit a parse tree produced by qutesParser#program.
    def exitProgram(self, ctx:qutesParser.ProgramContext):
        pass


    # Enter a parse tree produced by qutesParser#IfStatement.
    def enterIfStatement(self, ctx:qutesParser.IfStatementContext):
        self.if_else_scope_count += 1
        self.scope_handler.push_scope(ScopeClass.IfElseScope, f"If{self.if_else_scope_count}")

    # Exit a parse tree produced by qutesParser#IfStatement.
    def exitIfStatement(self, ctx:qutesParser.IfStatementContext):
        self.scope_handler.pop_scope()


    # Enter a parse tree produced by qutesParser#IfElseStatement.
    def enterIfElseStatement(self, ctx:qutesParser.IfElseStatementContext):
        self.if_else_scope_count += 1
        self.scope_handler.push_scope(ScopeClass.IfElseScope, f"IfElse{self.if_else_scope_count}")

    # Exit a parse tree produced by qutesParser#IfElseStatement.
    def exitIfElseStatement(self, ctx:qutesParser.IfElseStatementContext):
        self.scope_handler.pop_scope()


    # Enter a parse tree produced by qutesParser#WhileStatement.
    def enterWhileStatement(self, ctx:qutesParser.WhileStatementContext):
        self.loop_scope_count += 1
        self.scope_handler.push_scope(ScopeClass.LoopScope, f"While{self.if_else_scope_count}")

    # Exit a parse tree produced by qutesParser#WhileStatement.
    def exitWhileStatement(self, ctx:qutesParser.WhileStatementContext):
        self.scope_handler.pop_scope()


    # Enter a parse tree produced by qutesParser#DoWhileStatement.
    def enterDoWhileStatement(self, ctx:qutesParser.DoWhileStatementContext):
        self.loop_scope_count += 1
        self.scope_handler.push_scope(ScopeClass.LoopScope, f"DoWhile{self.if_else_scope_count}")

    # Exit a parse tree produced by qutesParser#DoWhileStatement.
    def exitDoWhileStatement(self, ctx:qutesParser.DoWhileStatementContext):
        self.scope_handler.pop_scope()


    # Enter a parse tree produced by qutesParser#BlockStatement.
    def enterBlockStatement(self, ctx:qutesParser.BlockStatementContext):
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

    # Exit a parse tree produced by qutesParser#BlockStatement.
    def exitBlockStatement(self, ctx:qutesParser.BlockStatementContext):
        if(self.scope_handler.current_symbols_scope.scope_class == ScopeClass.FunctionScope):
            pass
        else:
            self.scope_handler.pop_scope()


    # Enter a parse tree produced by qutes_parser#FunctionStatement.
    def enterFunctionStatement(self, ctx:qutesParser.FunctionStatementContext):
        self.function_scope_count += 1
        return_type = ctx.variableType().getText()
        qutes_type = QutesDataType.from_string_type(return_type)
        function_name = ctx.functionName().getText()
        #TODO: input params should be part of function signature, so they should be retrieved here in order to declare the function
        # but for semplicity we are currently doing this check only on the visitor.
        funtion_symbol = self.variables_handler.declare_function(qutes_type, function_name, [])
        self.scope_handler.push_inner_scope(ScopeClass.FunctionScope, f"Function{self.function_scope_count}", funtion_symbol)

    # Exit a parse tree produced by qutes_parser#FunctionStatement.
    def exitFunctionStatement(self, ctx:qutesParser.FunctionStatementContext):
        self.scope_handler.pop_scope()

    # Enter a parse tree produced by qutes_parser#variableDeclaration.
    def enterVariableDeclaration(self, ctx:qutesParser.VariableDeclarationContext):
        var_type = ctx.variableType().getText()
        var_name = ctx.variableName().getText()
        qutes_type = QutesDataType.from_string_type(var_type)
        # This listener should not follow the execution path to understand what was the initial value assigned to the variable.
        # So we assign None and then variables_handler will put in the default value for the type.
        self.variables_handler.declare_variable(qutes_type, var_name)
