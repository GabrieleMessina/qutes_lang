"""An antlr visitor for the qutes grammar."""

from qutes_antlr.qutesParser import qutesParser
from qutes_antlr.qutesVisitor import qutesVisitor

class QutesGrammarVisitor(qutesVisitor):
    """An antlr visitor for the qutes grammar."""

    # Debug flags
    __log_trace = False
    __log_step_by_step_results = False

    # Visit a parse tree produced by qutesParser#program.
    def visitProgram(self, ctx:qutesParser.ProgramContext):
        result = str()
        expression_count = 0
        for child in ctx.getChildren():
            expression_count += 1
            new_value = self.__visit("visitProgram", lambda i=child : self.visit(i))
            result = f'{result}\nExpression[{expression_count}]: {new_value};'
        return result

    # Visit a parse tree produced by qutesParser#IfStatement.
    def visitIfStatement(self, ctx:qutesParser.IfStatementContext):
        return self.__visit("visitIfStatement", lambda : self.visitChildren(ctx))


    # Visit a parse tree produced by qutesParser#IfElseStatement.
    def visitIfElseStatement(self, ctx:qutesParser.IfElseStatementContext):
        return self.__visit("visitIfElseStatement", lambda : self.visitChildren(ctx))


    # Visit a parse tree produced by qutesParser#WhileStatement.
    def visitWhileStatement(self, ctx:qutesParser.WhileStatementContext):
        return self.__visit("visitWhileStatement", lambda : self.visitChildren(ctx))


    # Visit a parse tree produced by qutesParser#DoWhileStatement.
    def visitDoWhileStatement(self, ctx:qutesParser.DoWhileStatementContext):
        return self.__visit("visitDoWhileStatement", lambda : self.visitChildren(ctx))


    # Visit a parse tree produced by qutesParser#AssignmentStatement.
    def visitAssignmentStatement(self, ctx:qutesParser.AssignmentStatementContext):
        return self.__visit("visitAssignmentStatement", lambda : self.__visit_assignment_statement(ctx))

    def __visit_assignment_statement(self, ctx:qutesParser.AssignmentStatementContext):
        var_name = ctx.variableName().getText()
        var_value = "default_var_value"
        if(ctx.expr()):
            var_value = self.visitChildren(ctx.expr())
        if(ctx.parenExpr()):
            var_value = self.visitChildren(ctx.parenExpr())
        return str(var_name) + " = " + str(var_value)


    # Visit a parse tree produced by qutesParser#ExpressionStatement.
    def visitExpressionStatement(self, ctx:qutesParser.ExpressionStatementContext):
        return self.__visit("visitExpressionStatement", lambda : self.visitChildren(ctx.expr()))


    # Visit a parse tree produced by qutesParser#EmptyStatement.
    def visitEmptyStatement(self, ctx:qutesParser.EmptyStatementContext):
        return self.__visit("visitEmptyStatement", lambda : self.visitChildren(ctx))


    # Visit a parse tree produced by qutesParser#BlockStatement.
    def visitBlockStatement(self, ctx:qutesParser.BlockStatementContext):
        return self.__visit("visitBlockStatement", lambda : self.visitChildren(ctx))


    # Visit a parse tree produced by qutesParser#DeclarationStatement.
    def visitDeclarationStatement(self, ctx:qutesParser.DeclarationStatementContext):
        var_type = ctx.variableType().getText()
        var_name = ctx.variableName().getText()
        var_value = "default_var_value"
        if(ctx.expr()):
            var_value = self.visitChildren(ctx.expr())
        if(ctx.parenExpr()):
            var_value = self.visitChildren(ctx.parenExpr())
        return str(var_type) + " " + str(var_name) + " = " + str(var_value)
    

    # Visit a parse tree produced by qutesParser#parenExpr.
    def visitParenExpr(self, ctx:qutesParser.ParenExprContext):
        return self.__visit("visitparenExpr", lambda : "( " + str(self.visitChildren(ctx)) + " )")


    # Visit a parse tree produced by qutesParser#expr.
    def visitExpr(self, ctx:qutesParser.ExprContext):
        return self.__visit("visitExpr", lambda : self.__visit_expr(ctx))
    def __visit_expr(self, ctx:qutesParser.ExprContext):
        result = "visitExpr-default"
        if(ctx.term()):
            if(self.__log_trace): print("visitExpr -> term")
            result = self.visitChildren(ctx)
        if(ctx.test()):
            if(self.__log_trace): print("visitExpr -> test")
            result = self.visitChildren(ctx)
        return result


    # Visit a parse tree produced by qutesParser#test.
    def visitTest(self, ctx:qutesParser.TestContext):
        return self.__visit("visitTest", lambda : self.__visit_test(ctx))

    def __visit_test(self, ctx:qutesParser.TestContext):
        result = "visitTest-default"
        if(ctx.GREATER()):
            if(self.__log_trace): print("visitTest -> greater")
            result = self.visitChildren(ctx.term(0)) > self.visitChildren(ctx.term(1))
        if(ctx.LOWER()):
            if(self.__log_trace): print("visitTest -> lower")
            result = self.visitChildren(ctx.term(0)) < self.visitChildren(ctx.term(1))
        if(ctx.EQUAL()):
            if(self.__log_trace): print("visitTest -> equal")
            result = self.visitChildren(ctx.term(0)) == self.visitChildren(ctx.term(1))
        if(ctx.GREATEREQUAL()):
            if(self.__log_trace): print("visitTest -> greater equal")
            result = self.visitChildren(ctx.term(0)) >= self.visitChildren(ctx.term(1))
        if(ctx.LOWEREQUAL()):
            if(self.__log_trace): print("visitTest -> lower equal")
            result = self.visitChildren(ctx.term(0)) <= self.visitChildren(ctx.term(1))

        if(self.__log_trace): print("visitTest -> test no operator")
        result = self.visitChildren(ctx.term(0))
        return result


    # Visit a parse tree produced by qutesParser#term.
    def visitTerm(self, ctx:qutesParser.TermContext):
        return self.__visit("visitTerm", lambda : self.__visit_term(ctx))
    def __visit_term(self, ctx:qutesParser.TermContext):
        result = "default_term_result"
        if(ctx.term(0)):
            if(self.__log_trace): print("visitTerm -> operation")
            if(ctx.ADD()):
                result = self.visitChildren(ctx.term(0)) + self.visitChildren(ctx.term(1))
            if(ctx.SUB()):
                result = self.visitChildren(ctx.term(0)) - self.visitChildren(ctx.term(1))
        if(ctx.qualifiedName()):
            if(self.__log_trace): print("visitTerm -> qualifiedName")
            result = self.visitChildren(ctx)
        if(ctx.string()):
            if(self.__log_trace): print("visitTerm -> string")
            result = self.visitChildren(ctx)
        if(ctx.integer()):
            if(self.__log_trace): print("visitTerm -> integer")
            result = self.visitChildren(ctx)
        return result


    # Visit a parse tree produced by qutesParser#variableType.
    def visitVariableType(self, ctx:qutesParser.VariableTypeContext):
        return self.__visit("visitVariableType", lambda : str(ctx.getText()))


    # Visit a parse tree produced by qutesParser#qualifiedName.
    def visitQualifiedName(self, ctx:qutesParser.QualifiedNameContext):
        return self.__visit("visitQualifiedName", lambda : str(ctx.getText()))


    # Visit a parse tree produced by qutesParser#id.
    def visitString(self, ctx:qutesParser.StringContext):
        return self.__visit("visitString", lambda : str(ctx.getText()))


    # Visit a parse tree produced by qutesParser#integer.
    def visitInteger(self, ctx:qutesParser.IntegerContext):
        return self.__visit("visitInteger", lambda : int(ctx.getText()))


    # Visit a parse tree produced by qutesParser#integer.
    def visitVariableName(self, ctx:qutesParser.VariableNameContext):
        return self.__visit("visitVariableName", lambda : str(ctx.getText()))


    # Utility method for logging and scaffolding operation
    def __visit(self, parent_caller_name, func):
        if(self.__log_trace): print("start " + parent_caller_name)
        result = func()
        if(self.__log_trace): print("end " + parent_caller_name)
        if(self.__log_step_by_step_results): print(result)
        return result
