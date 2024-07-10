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


    # Enter a parse tree produced by qutes_parser#FunctionStatement.
    def enterFunctionStatement(self, ctx:qutes_parser.FunctionStatementContext):
        pass

    # Exit a parse tree produced by qutes_parser#FunctionStatement.
    def exitFunctionStatement(self, ctx:qutes_parser.FunctionStatementContext):
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


    # Enter a parse tree produced by qutes_parser#ReturnStatement.
    def enterReturnStatement(self, ctx:qutes_parser.ReturnStatementContext):
        pass

    # Exit a parse tree produced by qutes_parser#ReturnStatement.
    def exitReturnStatement(self, ctx:qutes_parser.ReturnStatementContext):
        pass


    # Enter a parse tree produced by qutes_parser#ExpressionStatement.
    def enterExpressionStatement(self, ctx:qutes_parser.ExpressionStatementContext):
        pass

    # Exit a parse tree produced by qutes_parser#ExpressionStatement.
    def exitExpressionStatement(self, ctx:qutes_parser.ExpressionStatementContext):
        pass


    # Enter a parse tree produced by qutes_parser#FactStatement.
    def enterFactStatement(self, ctx:qutes_parser.FactStatementContext):
        pass

    # Exit a parse tree produced by qutes_parser#FactStatement.
    def exitFactStatement(self, ctx:qutes_parser.FactStatementContext):
        pass


    # Enter a parse tree produced by qutes_parser#EmptyStatement.
    def enterEmptyStatement(self, ctx:qutes_parser.EmptyStatementContext):
        pass

    # Exit a parse tree produced by qutes_parser#EmptyStatement.
    def exitEmptyStatement(self, ctx:qutes_parser.EmptyStatementContext):
        pass


    # Enter a parse tree produced by qutes_parser#functionDeclarationParams.
    def enterFunctionDeclarationParams(self, ctx:qutes_parser.FunctionDeclarationParamsContext):
        pass

    # Exit a parse tree produced by qutes_parser#functionDeclarationParams.
    def exitFunctionDeclarationParams(self, ctx:qutes_parser.FunctionDeclarationParamsContext):
        pass


    # Enter a parse tree produced by qutes_parser#variableDeclaration.
    def enterVariableDeclaration(self, ctx:qutes_parser.VariableDeclarationContext):
        pass

    # Exit a parse tree produced by qutes_parser#variableDeclaration.
    def exitVariableDeclaration(self, ctx:qutes_parser.VariableDeclarationContext):
        pass


    # Enter a parse tree produced by qutes_parser#QualifiedNameExpression.
    def enterQualifiedNameExpression(self, ctx:qutes_parser.QualifiedNameExpressionContext):
        pass

    # Exit a parse tree produced by qutes_parser#QualifiedNameExpression.
    def exitQualifiedNameExpression(self, ctx:qutes_parser.QualifiedNameExpressionContext):
        pass


    # Enter a parse tree produced by qutes_parser#RelationalOperator.
    def enterRelationalOperator(self, ctx:qutes_parser.RelationalOperatorContext):
        pass

    # Exit a parse tree produced by qutes_parser#RelationalOperator.
    def exitRelationalOperator(self, ctx:qutes_parser.RelationalOperatorContext):
        pass


    # Enter a parse tree produced by qutes_parser#LogicAndOperator.
    def enterLogicAndOperator(self, ctx:qutes_parser.LogicAndOperatorContext):
        pass

    # Exit a parse tree produced by qutes_parser#LogicAndOperator.
    def exitLogicAndOperator(self, ctx:qutes_parser.LogicAndOperatorContext):
        pass


    # Enter a parse tree produced by qutes_parser#PrefixOperator.
    def enterPrefixOperator(self, ctx:qutes_parser.PrefixOperatorContext):
        pass

    # Exit a parse tree produced by qutes_parser#PrefixOperator.
    def exitPrefixOperator(self, ctx:qutes_parser.PrefixOperatorContext):
        pass


    # Enter a parse tree produced by qutes_parser#LiteralExpression.
    def enterLiteralExpression(self, ctx:qutes_parser.LiteralExpressionContext):
        pass

    # Exit a parse tree produced by qutes_parser#LiteralExpression.
    def exitLiteralExpression(self, ctx:qutes_parser.LiteralExpressionContext):
        pass


    # Enter a parse tree produced by qutes_parser#GroverOperator.
    def enterGroverOperator(self, ctx:qutes_parser.GroverOperatorContext):
        pass

    # Exit a parse tree produced by qutes_parser#GroverOperator.
    def exitGroverOperator(self, ctx:qutes_parser.GroverOperatorContext):
        pass


    # Enter a parse tree produced by qutes_parser#FunctionCallExpression.
    def enterFunctionCallExpression(self, ctx:qutes_parser.FunctionCallExpressionContext):
        pass

    # Exit a parse tree produced by qutes_parser#FunctionCallExpression.
    def exitFunctionCallExpression(self, ctx:qutes_parser.FunctionCallExpressionContext):
        pass


    # Enter a parse tree produced by qutes_parser#EqualityOperator.
    def enterEqualityOperator(self, ctx:qutes_parser.EqualityOperatorContext):
        pass

    # Exit a parse tree produced by qutes_parser#EqualityOperator.
    def exitEqualityOperator(self, ctx:qutes_parser.EqualityOperatorContext):
        pass


    # Enter a parse tree produced by qutes_parser#MultipleUnaryOperator.
    def enterMultipleUnaryOperator(self, ctx:qutes_parser.MultipleUnaryOperatorContext):
        pass

    # Exit a parse tree produced by qutes_parser#MultipleUnaryOperator.
    def exitMultipleUnaryOperator(self, ctx:qutes_parser.MultipleUnaryOperatorContext):
        pass


    # Enter a parse tree produced by qutes_parser#SumOperator.
    def enterSumOperator(self, ctx:qutes_parser.SumOperatorContext):
        pass

    # Exit a parse tree produced by qutes_parser#SumOperator.
    def exitSumOperator(self, ctx:qutes_parser.SumOperatorContext):
        pass


    # Enter a parse tree produced by qutes_parser#PostfixOperator.
    def enterPostfixOperator(self, ctx:qutes_parser.PostfixOperatorContext):
        pass

    # Exit a parse tree produced by qutes_parser#PostfixOperator.
    def exitPostfixOperator(self, ctx:qutes_parser.PostfixOperatorContext):
        pass


    # Enter a parse tree produced by qutes_parser#ParentesizeExpression.
    def enterParentesizeExpression(self, ctx:qutes_parser.ParentesizeExpressionContext):
        pass

    # Exit a parse tree produced by qutes_parser#ParentesizeExpression.
    def exitParentesizeExpression(self, ctx:qutes_parser.ParentesizeExpressionContext):
        pass


    # Enter a parse tree produced by qutes_parser#ArrayExpression.
    def enterArrayExpression(self, ctx:qutes_parser.ArrayExpressionContext):
        pass

    # Exit a parse tree produced by qutes_parser#ArrayExpression.
    def exitArrayExpression(self, ctx:qutes_parser.ArrayExpressionContext):
        pass


    # Enter a parse tree produced by qutes_parser#MultipleUnaryPhaseOperator.
    def enterMultipleUnaryPhaseOperator(self, ctx:qutes_parser.MultipleUnaryPhaseOperatorContext):
        pass

    # Exit a parse tree produced by qutes_parser#MultipleUnaryPhaseOperator.
    def exitMultipleUnaryPhaseOperator(self, ctx:qutes_parser.MultipleUnaryPhaseOperatorContext):
        pass


    # Enter a parse tree produced by qutes_parser#MultiplicativeOperator.
    def enterMultiplicativeOperator(self, ctx:qutes_parser.MultiplicativeOperatorContext):
        pass

    # Exit a parse tree produced by qutes_parser#MultiplicativeOperator.
    def exitMultiplicativeOperator(self, ctx:qutes_parser.MultiplicativeOperatorContext):
        pass


    # Enter a parse tree produced by qutes_parser#ShiftOperator.
    def enterShiftOperator(self, ctx:qutes_parser.ShiftOperatorContext):
        pass

    # Exit a parse tree produced by qutes_parser#ShiftOperator.
    def exitShiftOperator(self, ctx:qutes_parser.ShiftOperatorContext):
        pass


    # Enter a parse tree produced by qutes_parser#UnaryOperator.
    def enterUnaryOperator(self, ctx:qutes_parser.UnaryOperatorContext):
        pass

    # Exit a parse tree produced by qutes_parser#UnaryOperator.
    def exitUnaryOperator(self, ctx:qutes_parser.UnaryOperatorContext):
        pass


    # Enter a parse tree produced by qutes_parser#ArrayAccessExpression.
    def enterArrayAccessExpression(self, ctx:qutes_parser.ArrayAccessExpressionContext):
        pass

    # Exit a parse tree produced by qutes_parser#ArrayAccessExpression.
    def exitArrayAccessExpression(self, ctx:qutes_parser.ArrayAccessExpressionContext):
        pass


    # Enter a parse tree produced by qutes_parser#LogicOrOperator.
    def enterLogicOrOperator(self, ctx:qutes_parser.LogicOrOperatorContext):
        pass

    # Exit a parse tree produced by qutes_parser#LogicOrOperator.
    def exitLogicOrOperator(self, ctx:qutes_parser.LogicOrOperatorContext):
        pass


    # Enter a parse tree produced by qutes_parser#termList.
    def enterTermList(self, ctx:qutes_parser.TermListContext):
        pass

    # Exit a parse tree produced by qutes_parser#termList.
    def exitTermList(self, ctx:qutes_parser.TermListContext):
        pass


    # Enter a parse tree produced by qutes_parser#array.
    def enterArray(self, ctx:qutes_parser.ArrayContext):
        pass

    # Exit a parse tree produced by qutes_parser#array.
    def exitArray(self, ctx:qutes_parser.ArrayContext):
        pass


    # Enter a parse tree produced by qutes_parser#variableType.
    def enterVariableType(self, ctx:qutes_parser.VariableTypeContext):
        pass

    # Exit a parse tree produced by qutes_parser#variableType.
    def exitVariableType(self, ctx:qutes_parser.VariableTypeContext):
        pass


    # Enter a parse tree produced by qutes_parser#type.
    def enterType(self, ctx:qutes_parser.TypeContext):
        pass

    # Exit a parse tree produced by qutes_parser#type.
    def exitType(self, ctx:qutes_parser.TypeContext):
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


    # Enter a parse tree produced by qutes_parser#functionName.
    def enterFunctionName(self, ctx:qutes_parser.FunctionNameContext):
        pass

    # Exit a parse tree produced by qutes_parser#functionName.
    def exitFunctionName(self, ctx:qutes_parser.FunctionNameContext):
        pass


    # Enter a parse tree produced by qutes_parser#literal.
    def enterLiteral(self, ctx:qutes_parser.LiteralContext):
        pass

    # Exit a parse tree produced by qutes_parser#literal.
    def exitLiteral(self, ctx:qutes_parser.LiteralContext):
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


    # Enter a parse tree produced by qutes_parser#qustring.
    def enterQustring(self, ctx:qutes_parser.QustringContext):
        pass

    # Exit a parse tree produced by qutes_parser#qustring.
    def exitQustring(self, ctx:qutes_parser.QustringContext):
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