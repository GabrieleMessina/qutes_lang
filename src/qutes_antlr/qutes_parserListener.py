# Generated from /workspaces/qutes_lang/specification/grammar/qutes_parser.g4 by ANTLR 4.13.1
from antlr4 import *
if "." in __name__:
    from .qutes_parser import qutes_parser
else:
    from qutes_parser import qutes_parser

# This class defines a complete listener for a parse tree produced by qutes_parser.
class qutes_parserListener(ParseTreeListener):

    # Enter a parse tree produced by qutes_parser#type.
    def enterType(self, ctx:qutes_parser.TypeContext):
        pass

    # Exit a parse tree produced by qutes_parser#type.
    def exitType(self, ctx:qutes_parser.TypeContext):
        pass


    # Enter a parse tree produced by qutes_parser#program.
    def enterProgram(self, ctx:qutes_parser.ProgramContext):
        pass

    # Exit a parse tree produced by qutes_parser#program.
    def exitProgram(self, ctx:qutes_parser.ProgramContext):
        pass


    # Enter a parse tree produced by qutes_parser#IfStatement.
    def enterIfStatement(self, ctx:qutes_parser.IfStatementContext):
        pass

    # Exit a parse tree produced by qutes_parser#IfStatement.
    def exitIfStatement(self, ctx:qutes_parser.IfStatementContext):
        pass


    # Enter a parse tree produced by qutes_parser#IfElseStatement.
    def enterIfElseStatement(self, ctx:qutes_parser.IfElseStatementContext):
        pass

    # Exit a parse tree produced by qutes_parser#IfElseStatement.
    def exitIfElseStatement(self, ctx:qutes_parser.IfElseStatementContext):
        pass


    # Enter a parse tree produced by qutes_parser#WhileStatement.
    def enterWhileStatement(self, ctx:qutes_parser.WhileStatementContext):
        pass

    # Exit a parse tree produced by qutes_parser#WhileStatement.
    def exitWhileStatement(self, ctx:qutes_parser.WhileStatementContext):
        pass


    # Enter a parse tree produced by qutes_parser#DoWhileStatement.
    def enterDoWhileStatement(self, ctx:qutes_parser.DoWhileStatementContext):
        pass

    # Exit a parse tree produced by qutes_parser#DoWhileStatement.
    def exitDoWhileStatement(self, ctx:qutes_parser.DoWhileStatementContext):
        pass


    # Enter a parse tree produced by qutes_parser#BlockStatement.
    def enterBlockStatement(self, ctx:qutes_parser.BlockStatementContext):
        pass

    # Exit a parse tree produced by qutes_parser#BlockStatement.
    def exitBlockStatement(self, ctx:qutes_parser.BlockStatementContext):
        pass


    # Enter a parse tree produced by qutes_parser#DeclarationStatement.
    def enterDeclarationStatement(self, ctx:qutes_parser.DeclarationStatementContext):
        pass

    # Exit a parse tree produced by qutes_parser#DeclarationStatement.
    def exitDeclarationStatement(self, ctx:qutes_parser.DeclarationStatementContext):
        pass


    # Enter a parse tree produced by qutes_parser#AssignmentStatement.
    def enterAssignmentStatement(self, ctx:qutes_parser.AssignmentStatementContext):
        pass

    # Exit a parse tree produced by qutes_parser#AssignmentStatement.
    def exitAssignmentStatement(self, ctx:qutes_parser.AssignmentStatementContext):
        pass


    # Enter a parse tree produced by qutes_parser#ExpressionStatement.
    def enterExpressionStatement(self, ctx:qutes_parser.ExpressionStatementContext):
        pass

    # Exit a parse tree produced by qutes_parser#ExpressionStatement.
    def exitExpressionStatement(self, ctx:qutes_parser.ExpressionStatementContext):
        pass


    # Enter a parse tree produced by qutes_parser#EmptyStatement.
    def enterEmptyStatement(self, ctx:qutes_parser.EmptyStatementContext):
        pass

    # Exit a parse tree produced by qutes_parser#EmptyStatement.
    def exitEmptyStatement(self, ctx:qutes_parser.EmptyStatementContext):
        pass


    # Enter a parse tree produced by qutes_parser#parenExpr.
    def enterParenExpr(self, ctx:qutes_parser.ParenExprContext):
        pass

    # Exit a parse tree produced by qutes_parser#parenExpr.
    def exitParenExpr(self, ctx:qutes_parser.ParenExprContext):
        pass


    # Enter a parse tree produced by qutes_parser#expr.
    def enterExpr(self, ctx:qutes_parser.ExprContext):
        pass

    # Exit a parse tree produced by qutes_parser#expr.
    def exitExpr(self, ctx:qutes_parser.ExprContext):
        pass


    # Enter a parse tree produced by qutes_parser#test.
    def enterTest(self, ctx:qutes_parser.TestContext):
        pass

    # Exit a parse tree produced by qutes_parser#test.
    def exitTest(self, ctx:qutes_parser.TestContext):
        pass


    # Enter a parse tree produced by qutes_parser#term.
    def enterTerm(self, ctx:qutes_parser.TermContext):
        pass

    # Exit a parse tree produced by qutes_parser#term.
    def exitTerm(self, ctx:qutes_parser.TermContext):
        pass


    # Enter a parse tree produced by qutes_parser#variableType.
    def enterVariableType(self, ctx:qutes_parser.VariableTypeContext):
        pass

    # Exit a parse tree produced by qutes_parser#variableType.
    def exitVariableType(self, ctx:qutes_parser.VariableTypeContext):
        pass


    # Enter a parse tree produced by qutes_parser#qualifiedName.
    def enterQualifiedName(self, ctx:qutes_parser.QualifiedNameContext):
        pass

    # Exit a parse tree produced by qutes_parser#qualifiedName.
    def exitQualifiedName(self, ctx:qutes_parser.QualifiedNameContext):
        pass


    # Enter a parse tree produced by qutes_parser#variableName.
    def enterVariableName(self, ctx:qutes_parser.VariableNameContext):
        pass

    # Exit a parse tree produced by qutes_parser#variableName.
    def exitVariableName(self, ctx:qutes_parser.VariableNameContext):
        pass


    # Enter a parse tree produced by qutes_parser#string.
    def enterString(self, ctx:qutes_parser.StringContext):
        pass

    # Exit a parse tree produced by qutes_parser#string.
    def exitString(self, ctx:qutes_parser.StringContext):
        pass


    # Enter a parse tree produced by qutes_parser#integer.
    def enterInteger(self, ctx:qutes_parser.IntegerContext):
        pass

    # Exit a parse tree produced by qutes_parser#integer.
    def exitInteger(self, ctx:qutes_parser.IntegerContext):
        pass



del qutes_parser