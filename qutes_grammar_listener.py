"""An antlr listener for the qutes frammar."""

from qutes_antlr.qutesListener import qutesListener
from qutes_antlr.qutesParser import qutesParser

class QutesGrammarListener(qutesListener):
    """An antlr listener for the qutes frammar."""

    def __init__(self):
        self.tree_property = {}

    def get_value(self, node):
        return self.tree_property[node]

    def set_value(self, node, value):
        self.tree_property[node] = value

    # def exitInt(self, ctx):
    #     self.setValue(ctx, int(ctx.INT().getText()))

    # def exitAdd(self, ctx):
    #     left = self.getValue(ctx.e(0))
    #     right= self.getValue(ctx.e(1))
    #     self.setValue(ctx, left+right)

    # def exitMult(self, ctx):
    #     left = self.getValue(ctx.e(0))
    #     right= self.getValue(ctx.e(1))
    #     self.setValue(ctx, left*right)

    # def exitS(self, ctx):
    #     self.setValue(ctx, self.getValue(ctx.e()))

    # Enter a parse tree produced by qutesParser#program.
    def enterProgram(self, ctx:qutesParser.ProgramContext):
        pass

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
        pass

    # Exit a parse tree produced by qutesParser#BlockStatement.
    def exitBlockStatement(self, ctx:qutesParser.BlockStatementContext):
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


    # Enter a parse tree produced by qutesParser#paren_expr.
    def enterParen_expr(self, ctx:qutesParser.Paren_exprContext):
        pass

    # Exit a parse tree produced by qutesParser#paren_expr.
    def exitParen_expr(self, ctx:qutesParser.Paren_exprContext):
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