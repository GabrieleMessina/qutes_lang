"""An antlr listener for the qutes grammar."""

from qutes_antlr.qutes_parserListener import qutes_parserListener as qutesListener
from qutes_antlr.qutes_parser import qutes_parser as qutesParser
from symbols.scope_tree_node import ScopeType, SymbolType, Symbol
from symbols.scope_handler import ScopeHandlerForSymbolsDiscovery

class SymbolsDiscoveryListener(qutesListener):
    """An antlr listener for the qutes grammar that discovers symbols like variable, function names etc."""

    def __init__(self):
        self.scope_handler = ScopeHandlerForSymbolsDiscovery()

    # Enter a parse tree produced by qutesParser#program.
    def enterProgram(self, ctx:qutesParser.ProgramContext):
        self.scope_handler.push_scope(ScopeType.GlobalScope, "Init")

    # Exit a parse tree produced by qutesParser#program.
    def exitProgram(self, ctx:qutesParser.ProgramContext):
        pass


    # Enter a parse tree produced by qutesParser#IfStatement.
    def enterIfStatement(self, ctx:qutesParser.IfStatementContext):
        pass

    # Exit a parse tree produced by qutesParser#IfStatement.
    def exitIfStatement(self, ctx:qutesParser.IfStatementContext):
        pass


    # Enter a parse tree produced by qutesParser#IfElseStatement.
    def enterIfElseStatement(self, ctx:qutesParser.IfElseStatementContext):
        pass

    # Exit a parse tree produced by qutesParser#IfElseStatement.
    def exitIfElseStatement(self, ctx:qutesParser.IfElseStatementContext):
        pass


    # Enter a parse tree produced by qutesParser#WhileStatement.
    def enterWhileStatement(self, ctx:qutesParser.WhileStatementContext):
        pass

    # Exit a parse tree produced by qutesParser#WhileStatement.
    def exitWhileStatement(self, ctx:qutesParser.WhileStatementContext):
        pass


    # Enter a parse tree produced by qutesParser#DoWhileStatement.
    def enterDoWhileStatement(self, ctx:qutesParser.DoWhileStatementContext):
        pass

    # Exit a parse tree produced by qutesParser#DoWhileStatement.
    def exitDoWhileStatement(self, ctx:qutesParser.DoWhileStatementContext):
        pass


    # Enter a parse tree produced by qutesParser#BlockStatement.
    def enterBlockStatement(self, ctx:qutesParser.BlockStatementContext):
        self.scope_handler.push_scope(ScopeType.LocalScope, "Block")

    # Exit a parse tree produced by qutesParser#BlockStatement.
    def exitBlockStatement(self, ctx:qutesParser.BlockStatementContext):
        self.scope_handler.pop_scope()


    # Enter a parse tree produced by qutesParser#DeclarationStatement.
    def enterDeclarationStatement(self, ctx:qutesParser.DeclarationStatementContext):
        new_var_name = ctx.variableName().getText()
        already_taken_symbol = any(symbol.name == new_var_name for symbol in self.scope_handler.current_symbols_scope.symbols)
        if(not already_taken_symbol):
            self.scope_handler.current_symbols_scope.symbols.append(Symbol(new_var_name, SymbolType.VariableSymbol, "NA", None, self.scope_handler.current_symbols_scope))
        else:
            raise SyntaxError(f"Variable with name '{new_var_name}' already declared.")

    # Exit a parse tree produced by qutesParser#DeclarationStatement.
    def exitDeclarationStatement(self, ctx:qutesParser.DeclarationStatementContext):
        pass


    # Enter a parse tree produced by qutesParser#AssignmentStatement.
    def enterAssignmentStatement(self, ctx:qutesParser.AssignmentStatementContext):
        pass

    # Exit a parse tree produced by qutesParser#AssignmentStatement.
    def exitAssignmentStatement(self, ctx:qutesParser.AssignmentStatementContext):
        pass


    # Enter a parse tree produced by qutesParser#ExpressionStatement.
    def enterExpressionStatement(self, ctx:qutesParser.ExpressionStatementContext):
        pass

    # Exit a parse tree produced by qutesParser#ExpressionStatement.
    def exitExpressionStatement(self, ctx:qutesParser.ExpressionStatementContext):
        pass


    # Enter a parse tree produced by qutesParser#EmptyStatement.
    def enterEmptyStatement(self, ctx:qutesParser.EmptyStatementContext):
        pass

    # Exit a parse tree produced by qutesParser#EmptyStatement.
    def exitEmptyStatement(self, ctx:qutesParser.EmptyStatementContext):
        pass


    # Enter a parse tree produced by qutesParser#ParenExpr.
    def enterParenExpr(self, ctx:qutesParser.ParenExprContext):
        pass

    # Exit a parse tree produced by qutesParser#ParenExpr.
    def exitParenExpr(self, ctx:qutesParser.ParenExprContext):
        pass


    # Enter a parse tree produced by qutesParser#expr.
    def enterExpr(self, ctx:qutesParser.ExprContext):
        pass

    # Exit a parse tree produced by qutesParser#expr.
    def exitExpr(self, ctx:qutesParser.ExprContext):
        pass


    # Enter a parse tree produced by qutesParser#test.
    def enterTest(self, ctx:qutesParser.TestContext):
        pass

    # Exit a parse tree produced by qutesParser#test.
    def exitTest(self, ctx:qutesParser.TestContext):
        pass


    # Enter a parse tree produced by qutesParser#term.
    def enterTerm(self, ctx:qutesParser.TermContext):
        pass

    # Exit a parse tree produced by qutesParser#term.
    def exitTerm(self, ctx:qutesParser.TermContext):
        pass


    # Enter a parse tree produced by qutes_parser#type.
    def enterType(self, ctx:qutesParser.TypeContext):
        pass

    # Exit a parse tree produced by qutes_parser#type.
    def exitType(self, ctx:qutesParser.TypeContext):
        pass


    # Enter a parse tree produced by qutesParser#variableType.
    def enterVariableType(self, ctx:qutesParser.VariableTypeContext):
        pass

    # Exit a parse tree produced by qutesParser#variableType.
    def exitVariableType(self, ctx:qutesParser.VariableTypeContext):
        pass


    # Enter a parse tree produced by qutesParser#qualifiedName.
    def enterQualifiedName(self, ctx:qutesParser.QualifiedNameContext):
        pass

    # Exit a parse tree produced by qutesParser#qualifiedName.
    def exitQualifiedName(self, ctx:qutesParser.QualifiedNameContext):
        pass


    # Enter a parse tree produced by qutesParser#variableName.
    def enterVariableName(self, ctx:qutesParser.VariableNameContext):
        pass

    # Exit a parse tree produced by qutesParser#variableName.
    def exitVariableName(self, ctx:qutesParser.VariableNameContext):
        pass


    # Enter a parse tree produced by qutesParser#string.
    def enterString(self, ctx:qutesParser.StringContext):
        pass

    # Exit a parse tree produced by qutesParser#string.
    def exitString(self, ctx:qutesParser.StringContext):
        pass


    # Enter a parse tree produced by qutesParser#integer.
    def enterInteger(self, ctx:qutesParser.IntegerContext):
        pass

    # Exit a parse tree produced by qutesParser#integer.
    def exitInteger(self, ctx:qutesParser.IntegerContext):
        pass
