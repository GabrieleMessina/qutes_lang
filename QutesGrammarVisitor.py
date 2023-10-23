from antlr4 import *
from QutesAntlr.QutesParser import QutesParser
from QutesAntlr.QutesVisitor import QutesVisitor

class QutesGrammarVisitor(QutesVisitor):
    LogTrace = True
    LogStepByStepResults = True

    # Visit a parse tree produced by QutesParser#program.
    def visitProgram(self, ctx:QutesParser.ProgramContext):
        result = str()
        for i in ctx.getChildren():
            newValue = self._visit("visitProgram", lambda : self.visit(i))
            result = f'{result}\n{newValue};'
        return result

    # Visit a parse tree produced by QutesParser#IfStatement.
    def visitIfStatement(self, ctx:QutesParser.IfStatementContext):
        return self._visit("visitIfStatement", lambda : self.visitChildren(ctx))


    # Visit a parse tree produced by QutesParser#IfElseStatement.
    def visitIfElseStatement(self, ctx:QutesParser.IfElseStatementContext):
        return self._visit("visitIfElseStatement", lambda : self.visitChildren(ctx))


    # Visit a parse tree produced by QutesParser#WhileStatement.
    def visitWhileStatement(self, ctx:QutesParser.WhileStatementContext):
        return self._visit("visitWhileStatement", lambda : self.visitChildren(ctx))


    # Visit a parse tree produced by QutesParser#DoWhileStatement.
    def visitDoWhileStatement(self, ctx:QutesParser.DoWhileStatementContext):
        return self._visit("visitDoWhileStatement", lambda : self.visitChildren(ctx))


    # Visit a parse tree produced by QutesParser#AssignmentStatement.
    def visitAssignmentStatement(self, ctx:QutesParser.AssignmentStatementContext):
        return self._visit("visitAssignmentStatement", lambda : self._visitAssignmentStatement(ctx))
    def _visitAssignmentStatement(self, ctx:QutesParser.AssignmentStatementContext):
        varName = ctx.variableName().getText()
        varValue = "default_var_value"
        if(ctx.expr()):
            varValue = self.visitChildren(ctx.expr())
        if(ctx.paren_expr()):
            varValue = self.visitChildren(ctx.paren_expr())
        return str(varName) + " = " + str(varValue)


    # Visit a parse tree produced by QutesParser#ExpressionStatement.
    def visitExpressionStatement(self, ctx:QutesParser.ExpressionStatementContext):
        return self._visit("visitExpressionStatement", lambda : self.visitChildren(ctx))


    # Visit a parse tree produced by QutesParser#EmptyStatement.
    def visitEmptyStatement(self, ctx:QutesParser.EmptyStatementContext):
        return self._visit("visitEmptyStatement", lambda : self.visitChildren(ctx))


    # Visit a parse tree produced by QutesParser#BlockStatement.
    def visitBlockStatement(self, ctx:QutesParser.BlockStatementContext):
        return self._visit("visitBlockStatement", lambda : self.visitChildren(ctx))
    

    # Visit a parse tree produced by QutesParser#ExpressionStatement.
    def visitExpressionStatement(self, ctx:QutesParser.ExpressionStatementContext):
        return self._visit("visitExpressionStatement", lambda : self.visitChildren(ctx.expr()))


    # Visit a parse tree produced by QutesParser#paren_expr.
    def visitParen_expr(self, ctx:QutesParser.Paren_exprContext):
        return self._visit("visitParen_expr", lambda : "( " + str(self.visitChildren(ctx)) + " )")


    # Visit a parse tree produced by QutesParser#expr.
    def visitExpr(self, ctx:QutesParser.ExprContext):
        return self._visit("visitExpr", lambda : self._visitExpr(ctx))
    def _visitExpr(self, ctx:QutesParser.ExprContext):
        result = "visitExpr-default"
        if(ctx.term()):
            if(self.LogTrace): print("visitExpr -> term")
            result = self.visitChildren(ctx)
        if(ctx.test()):
            if(self.LogTrace): print("visitExpr -> test")
            result = self.visitChildren(ctx)
        return result


    # Visit a parse tree produced by QutesParser#test.
    def visitTest(self, ctx:QutesParser.TestContext):
        return self._visit("visitTest", lambda : self._visitTest(ctx))
    def _visitTest(self, ctx:QutesParser.TestContext):
        result = "visitTest-default"
        if(ctx.GREATER()):
            if(self.LogTrace): print("visitTest -> greater")
            result = self.visitChildren(ctx.term(0)) > self.visitChildren(ctx.term(1))
        if(ctx.LOWER()):
            if(self.LogTrace): print("visitTest -> lower")
            result = self.visitChildren(ctx.term(0)) < self.visitChildren(ctx.term(1))
        if(ctx.EQUAL()):
            if(self.LogTrace): print("visitTest -> equal")
            result = self.visitChildren(ctx.term(0)) == self.visitChildren(ctx.term(1))
        if(ctx.GREATEREQUAL()):
            if(self.LogTrace): print("visitTest -> greater equal")
            result = self.visitChildren(ctx.term(0)) >= self.visitChildren(ctx.term(1))
        if(ctx.LOWEREQUAL()):
            if(self.LogTrace): print("visitTest -> lower equal")
            result = self.visitChildren(ctx.term(0)) <= self.visitChildren(ctx.term(1))

        if(self.LogTrace): print("visitTest -> test no operator")
        result = self.visitChildren(ctx.term(0))
        return result


    # Visit a parse tree produced by QutesParser#term.
    def visitTerm(self, ctx:QutesParser.TermContext):
        return self._visit("visitTerm", lambda : self._visitTerm(ctx))
    def _visitTerm(self, ctx:QutesParser.TermContext):
        result = "default_term_result"
        if(ctx.term(0)):
            if(self.LogTrace): print("visitTerm -> operation")
            if(ctx.ADD()):
                result = self.visitChildren(ctx.term(0)) + self.visitChildren(ctx.term(1))
            if(ctx.SUB()):
                result = self.visitChildren(ctx.term(0)) - self.visitChildren(ctx.term(1)) 
        if(ctx.variableName()):
            if(self.LogTrace): print("visitTerm -> variableName")
            result = self.visitChildren(ctx)
        if(ctx.string()):
            if(self.LogTrace): print("visitTerm -> string")
            result = self.visitChildren(ctx)
        if(ctx.integer()):
            if(self.LogTrace): print("visitTerm -> integer")
            result = self.visitChildren(ctx)
        
        return result


    # Visit a parse tree produced by QutesParser#id.
    def visitString(self, ctx:QutesParser.StringContext):
        return self._visit("visitString", lambda : str(ctx.getText()))


    # Visit a parse tree produced by QutesParser#integer.
    def visitInteger(self, ctx:QutesParser.IntegerContext):
        return self._visit("visitInteger", lambda : int(ctx.getText()))
    

    # Visit a parse tree produced by QutesParser#integer.
    def visitVariableName(self, ctx:QutesParser.VariableNameContext):
        return self._visit("visitVariableName", lambda : str(ctx.getText()))
    

    # Utility method for logging and scaffolding operation
    def _visit(self, parentCallerName, func):
        if(self.LogTrace): print("start " + parentCallerName)
        result = func()
        if(self.LogTrace): print("end " + parentCallerName)
        if(self.LogStepByStepResults): print(result)
        return result