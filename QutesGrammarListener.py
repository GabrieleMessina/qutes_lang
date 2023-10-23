from QutesAntlr.QutesListener import QutesListener
from QutesAntlr.QutesParser import QutesParser

class QutesGrammarListener(QutesListener):

    def __init__(self):
        self.tree_property = {}

    def getValue(self, node):
        return self.tree_property[node]

    def setValue(self, node, value):
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
        print("expre listenerrrrr")
        pass

    # Exit a parse tree produced by QutesParser#expr.
    def exitExpr(self, ctx:QutesParser.ExprContext):
        print("expre2 listenerrrrr")
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