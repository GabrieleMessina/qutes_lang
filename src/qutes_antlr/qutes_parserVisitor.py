# Generated from /workspaces/qutes_lang/specification/grammar/qutes_parser.g4 by ANTLR 4.13.1
from antlr4 import *
if "." in __name__:
    from .qutes_parser import qutes_parser
else:
    from qutes_parser import qutes_parser

# This class defines a complete generic visitor for a parse tree produced by qutes_parser.

class qutes_parserVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by qutes_parser#type.
    def visitType(self, ctx:qutes_parser.TypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by qutes_parser#program.
    def visitProgram(self, ctx:qutes_parser.ProgramContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by qutes_parser#IfStatement.
    def visitIfStatement(self, ctx:qutes_parser.IfStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by qutes_parser#IfElseStatement.
    def visitIfElseStatement(self, ctx:qutes_parser.IfElseStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by qutes_parser#WhileStatement.
    def visitWhileStatement(self, ctx:qutes_parser.WhileStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by qutes_parser#DoWhileStatement.
    def visitDoWhileStatement(self, ctx:qutes_parser.DoWhileStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by qutes_parser#BlockStatement.
    def visitBlockStatement(self, ctx:qutes_parser.BlockStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by qutes_parser#DeclarationStatement.
    def visitDeclarationStatement(self, ctx:qutes_parser.DeclarationStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by qutes_parser#AssignmentStatement.
    def visitAssignmentStatement(self, ctx:qutes_parser.AssignmentStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by qutes_parser#ExpressionStatement.
    def visitExpressionStatement(self, ctx:qutes_parser.ExpressionStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by qutes_parser#EmptyStatement.
    def visitEmptyStatement(self, ctx:qutes_parser.EmptyStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by qutes_parser#parenExpr.
    def visitParenExpr(self, ctx:qutes_parser.ParenExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by qutes_parser#expr.
    def visitExpr(self, ctx:qutes_parser.ExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by qutes_parser#test.
    def visitTest(self, ctx:qutes_parser.TestContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by qutes_parser#term.
    def visitTerm(self, ctx:qutes_parser.TermContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by qutes_parser#variableType.
    def visitVariableType(self, ctx:qutes_parser.VariableTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by qutes_parser#qualifiedName.
    def visitQualifiedName(self, ctx:qutes_parser.QualifiedNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by qutes_parser#variableName.
    def visitVariableName(self, ctx:qutes_parser.VariableNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by qutes_parser#string.
    def visitString(self, ctx:qutes_parser.StringContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by qutes_parser#integer.
    def visitInteger(self, ctx:qutes_parser.IntegerContext):
        return self.visitChildren(ctx)



del qutes_parser