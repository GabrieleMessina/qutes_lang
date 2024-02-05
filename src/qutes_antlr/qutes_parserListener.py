# Generated from /workspaces/qutes_lang/specification/grammar/qutes_parser.g4 by ANTLR 4.13.1
from antlr4 import *
if "." in __name__:
    from .qutes_parser import qutes_parser
else:
    from qutes_parser import qutes_parser

# This class defines a complete listener for a parse tree produced by qutes_parser.
class qutes_parserListener(ParseTreeListener):

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


    # Enter a parse tree produced by qutes_parser#expr.
    def enterExpr(self, ctx:qutes_parser.ExprContext):
        pass

    # Exit a parse tree produced by qutes_parser#expr.
    def exitExpr(self, ctx:qutes_parser.ExprContext):
        pass


    # Enter a parse tree produced by qutes_parser#parenExpr.
    def enterParenExpr(self, ctx:qutes_parser.ParenExprContext):
        pass

    # Exit a parse tree produced by qutes_parser#parenExpr.
    def exitParenExpr(self, ctx:qutes_parser.ParenExprContext):
        pass


    # Enter a parse tree produced by qutes_parser#test.
    def enterTest(self, ctx:qutes_parser.TestContext):
        pass

    # Exit a parse tree produced by qutes_parser#test.
    def exitTest(self, ctx:qutes_parser.TestContext):
        pass


    # Enter a parse tree produced by qutes_parser#IdentityOperator.
    def enterIdentityOperator(self, ctx:qutes_parser.IdentityOperatorContext):
        pass

    # Exit a parse tree produced by qutes_parser#IdentityOperator.
    def exitIdentityOperator(self, ctx:qutes_parser.IdentityOperatorContext):
        pass


    # Enter a parse tree produced by qutes_parser#UnaryOperator.
    def enterUnaryOperator(self, ctx:qutes_parser.UnaryOperatorContext):
        pass

    # Exit a parse tree produced by qutes_parser#UnaryOperator.
    def exitUnaryOperator(self, ctx:qutes_parser.UnaryOperatorContext):
        pass


    # Enter a parse tree produced by qutes_parser#BinaryOperator.
    def enterBinaryOperator(self, ctx:qutes_parser.BinaryOperatorContext):
        pass

    # Exit a parse tree produced by qutes_parser#BinaryOperator.
    def exitBinaryOperator(self, ctx:qutes_parser.BinaryOperatorContext):
        pass


    # Enter a parse tree produced by qutes_parser#type.
    def enterType(self, ctx:qutes_parser.TypeContext):
        pass

    # Exit a parse tree produced by qutes_parser#type.
    def exitType(self, ctx:qutes_parser.TypeContext):
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


    # Enter a parse tree produced by qutes_parser#qubit.
    def enterQubit(self, ctx:qutes_parser.QubitContext):
        pass

    # Exit a parse tree produced by qutes_parser#qubit.
    def exitQubit(self, ctx:qutes_parser.QubitContext):
        pass


    # Enter a parse tree produced by qutes_parser#quint.
    def enterQuint(self, ctx:qutes_parser.QuintContext):
        pass

    # Exit a parse tree produced by qutes_parser#quint.
    def exitQuint(self, ctx:qutes_parser.QuintContext):
        pass


    # Enter a parse tree produced by qutes_parser#float.
    def enterFloat(self, ctx:qutes_parser.FloatContext):
        pass

    # Exit a parse tree produced by qutes_parser#float.
    def exitFloat(self, ctx:qutes_parser.FloatContext):
        pass


    # Enter a parse tree produced by qutes_parser#integer.
    def enterInteger(self, ctx:qutes_parser.IntegerContext):
        pass

    # Exit a parse tree produced by qutes_parser#integer.
    def exitInteger(self, ctx:qutes_parser.IntegerContext):
        pass


    # Enter a parse tree produced by qutes_parser#boolean.
    def enterBoolean(self, ctx:qutes_parser.BooleanContext):
        pass

    # Exit a parse tree produced by qutes_parser#boolean.
    def exitBoolean(self, ctx:qutes_parser.BooleanContext):
        pass



del qutes_parser