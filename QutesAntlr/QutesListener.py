# Generated from d:/Users/gabry/Universita/quantum_computing/qutes_lang/Qutes.g4 by ANTLR 4.13.1
from antlr4 import *
if "." in __name__:
    from .QutesParser import QutesParser
else:
    from QutesParser import QutesParser

# This class defines a complete listener for a parse tree produced by QutesParser.
class QutesListener(ParseTreeListener):

    # Enter a parse tree produced by QutesParser#program.
    def enterProgram(self, ctx:QutesParser.ProgramContext):
        pass

    # Exit a parse tree produced by QutesParser#program.
    def exitProgram(self, ctx:QutesParser.ProgramContext):
        pass


    # Enter a parse tree produced by QutesParser#IfStatement.
    def enterIfStatement(self, ctx:QutesParser.IfStatementContext):
        pass

    # Exit a parse tree produced by QutesParser#IfStatement.
    def exitIfStatement(self, ctx:QutesParser.IfStatementContext):
        pass


    # Enter a parse tree produced by QutesParser#IfElseStatement.
    def enterIfElseStatement(self, ctx:QutesParser.IfElseStatementContext):
        pass

    # Exit a parse tree produced by QutesParser#IfElseStatement.
    def exitIfElseStatement(self, ctx:QutesParser.IfElseStatementContext):
        pass


    # Enter a parse tree produced by QutesParser#WhileStatement.
    def enterWhileStatement(self, ctx:QutesParser.WhileStatementContext):
        pass

    # Exit a parse tree produced by QutesParser#WhileStatement.
    def exitWhileStatement(self, ctx:QutesParser.WhileStatementContext):
        pass


    # Enter a parse tree produced by QutesParser#DoWhileStatement.
    def enterDoWhileStatement(self, ctx:QutesParser.DoWhileStatementContext):
        pass

    # Exit a parse tree produced by QutesParser#DoWhileStatement.
    def exitDoWhileStatement(self, ctx:QutesParser.DoWhileStatementContext):
        pass


    # Enter a parse tree produced by QutesParser#BlockStatement.
    def enterBlockStatement(self, ctx:QutesParser.BlockStatementContext):
        pass

    # Exit a parse tree produced by QutesParser#BlockStatement.
    def exitBlockStatement(self, ctx:QutesParser.BlockStatementContext):
        pass


    # Enter a parse tree produced by QutesParser#AssignmentStatement.
    def enterAssignmentStatement(self, ctx:QutesParser.AssignmentStatementContext):
        pass

    # Exit a parse tree produced by QutesParser#AssignmentStatement.
    def exitAssignmentStatement(self, ctx:QutesParser.AssignmentStatementContext):
        pass


    # Enter a parse tree produced by QutesParser#ExpressionStatement.
    def enterExpressionStatement(self, ctx:QutesParser.ExpressionStatementContext):
        pass

    # Exit a parse tree produced by QutesParser#ExpressionStatement.
    def exitExpressionStatement(self, ctx:QutesParser.ExpressionStatementContext):
        pass


    # Enter a parse tree produced by QutesParser#EmptyStatement.
    def enterEmptyStatement(self, ctx:QutesParser.EmptyStatementContext):
        pass

    # Exit a parse tree produced by QutesParser#EmptyStatement.
    def exitEmptyStatement(self, ctx:QutesParser.EmptyStatementContext):
        pass


    # Enter a parse tree produced by QutesParser#paren_expr.
    def enterParen_expr(self, ctx:QutesParser.Paren_exprContext):
        pass

    # Exit a parse tree produced by QutesParser#paren_expr.
    def exitParen_expr(self, ctx:QutesParser.Paren_exprContext):
        pass


    # Enter a parse tree produced by QutesParser#expr.
    def enterExpr(self, ctx:QutesParser.ExprContext):
        pass

    # Exit a parse tree produced by QutesParser#expr.
    def exitExpr(self, ctx:QutesParser.ExprContext):
        pass


    # Enter a parse tree produced by QutesParser#test.
    def enterTest(self, ctx:QutesParser.TestContext):
        pass

    # Exit a parse tree produced by QutesParser#test.
    def exitTest(self, ctx:QutesParser.TestContext):
        pass


    # Enter a parse tree produced by QutesParser#term.
    def enterTerm(self, ctx:QutesParser.TermContext):
        pass

    # Exit a parse tree produced by QutesParser#term.
    def exitTerm(self, ctx:QutesParser.TermContext):
        pass


    # Enter a parse tree produced by QutesParser#variableName.
    def enterVariableName(self, ctx:QutesParser.VariableNameContext):
        pass

    # Exit a parse tree produced by QutesParser#variableName.
    def exitVariableName(self, ctx:QutesParser.VariableNameContext):
        pass


    # Enter a parse tree produced by QutesParser#string.
    def enterString(self, ctx:QutesParser.StringContext):
        pass

    # Exit a parse tree produced by QutesParser#string.
    def exitString(self, ctx:QutesParser.StringContext):
        pass


    # Enter a parse tree produced by QutesParser#integer.
    def enterInteger(self, ctx:QutesParser.IntegerContext):
        pass

    # Exit a parse tree produced by QutesParser#integer.
    def exitInteger(self, ctx:QutesParser.IntegerContext):
        pass



del QutesParser