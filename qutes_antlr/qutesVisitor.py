# Generated from /workspaces/qutes_lang/qutes.g4 by ANTLR 4.13.1
from antlr4 import *
if "." in __name__:
    from .qutesParser import qutesParser
else:
    from qutesParser import qutesParser

# This class defines a complete generic visitor for a parse tree produced by qutesParser.

class qutesVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by qutesParser#program.
    def visitProgram(self, ctx:qutesParser.ProgramContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by qutesParser#IfStatement.
    def visitIfStatement(self, ctx:qutesParser.IfStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by qutesParser#IfElseStatement.
    def visitIfElseStatement(self, ctx:qutesParser.IfElseStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by qutesParser#WhileStatement.
    def visitWhileStatement(self, ctx:qutesParser.WhileStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by qutesParser#DoWhileStatement.
    def visitDoWhileStatement(self, ctx:qutesParser.DoWhileStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by qutesParser#BlockStatement.
    def visitBlockStatement(self, ctx:qutesParser.BlockStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by qutesParser#AssignmentStatement.
    def visitAssignmentStatement(self, ctx:qutesParser.AssignmentStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by qutesParser#ExpressionStatement.
    def visitExpressionStatement(self, ctx:qutesParser.ExpressionStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by qutesParser#EmptyStatement.
    def visitEmptyStatement(self, ctx:qutesParser.EmptyStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by qutesParser#paren_expr.
    def visitParen_expr(self, ctx:qutesParser.Paren_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by qutesParser#expr.
    def visitExpr(self, ctx:qutesParser.ExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by qutesParser#test.
    def visitTest(self, ctx:qutesParser.TestContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by qutesParser#term.
    def visitTerm(self, ctx:qutesParser.TermContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by qutesParser#variableName.
    def visitVariableName(self, ctx:qutesParser.VariableNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by qutesParser#string.
    def visitString(self, ctx:qutesParser.StringContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by qutesParser#integer.
    def visitInteger(self, ctx:qutesParser.IntegerContext):
        return self.visitChildren(ctx)



del qutesParser