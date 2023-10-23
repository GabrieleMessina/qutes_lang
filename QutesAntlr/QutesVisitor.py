# Generated from d:/Users/gabry/Universita/quantum_computing/qutes_lang/Qutes.g4 by ANTLR 4.13.1
from antlr4 import *
if "." in __name__:
    from .QutesParser import QutesParser
else:
    from QutesParser import QutesParser

# This class defines a complete generic visitor for a parse tree produced by QutesParser.

class QutesVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by QutesParser#program.
    def visitProgram(self, ctx:QutesParser.ProgramContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QutesParser#IfStatement.
    def visitIfStatement(self, ctx:QutesParser.IfStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QutesParser#IfElseStatement.
    def visitIfElseStatement(self, ctx:QutesParser.IfElseStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QutesParser#WhileStatement.
    def visitWhileStatement(self, ctx:QutesParser.WhileStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QutesParser#DoWhileStatement.
    def visitDoWhileStatement(self, ctx:QutesParser.DoWhileStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QutesParser#BlockStatement.
    def visitBlockStatement(self, ctx:QutesParser.BlockStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QutesParser#AssignmentStatement.
    def visitAssignmentStatement(self, ctx:QutesParser.AssignmentStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QutesParser#ExpressionStatement.
    def visitExpressionStatement(self, ctx:QutesParser.ExpressionStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QutesParser#EmptyStatement.
    def visitEmptyStatement(self, ctx:QutesParser.EmptyStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QutesParser#paren_expr.
    def visitParen_expr(self, ctx:QutesParser.Paren_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QutesParser#expr.
    def visitExpr(self, ctx:QutesParser.ExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QutesParser#test.
    def visitTest(self, ctx:QutesParser.TestContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QutesParser#term.
    def visitTerm(self, ctx:QutesParser.TermContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QutesParser#variableName.
    def visitVariableName(self, ctx:QutesParser.VariableNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QutesParser#string.
    def visitString(self, ctx:QutesParser.StringContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QutesParser#integer.
    def visitInteger(self, ctx:QutesParser.IntegerContext):
        return self.visitChildren(ctx)



del QutesParser