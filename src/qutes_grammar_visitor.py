"""An antlr visitor for the qutes grammar."""

from qutes_antlr.qutes_parser import qutes_parser as qutesParser
from qutes_antlr.qutes_parserVisitor import qutes_parserVisitor as qutesVisitor
from symbols.scope_tree_node import ScopeTreeNode
from symbols.scope_handler import ScopeHandlerForSymbolsUpdate

class QutesGrammarVisitor(qutesVisitor):
    """An antlr visitor for the qutes grammar."""

    def __init__(self, symbols_tree:ScopeTreeNode):
        if not symbols_tree:
            raise ValueError("A symbols tree must be provided to the QutesGrammarVisitor.")
        self.symbols_tree = symbols_tree
        #We need to travers the symbols_tree going orderly like in a breadth first search
        #Every time we need to create a new scope, we visit instead the next node in the tree
        #And every time we need to close a scope, we return to the parent of the current node
        #This way we know, at each moment, what symbols are defined.
        self.scope_handler = ScopeHandlerForSymbolsUpdate(self.symbols_tree)

        # Debug flags
        self.log_trace_enabled = False
        self.log_step_by_step_results_enabled = False

    # Visit a parse tree produced by qutesParser#program.
    def visitProgram(self, ctx:qutesParser.ProgramContext):
        self.scope_handler.push_scope()
        result = str()
        expression_count = 0
        for child in ctx.getChildren():
            expression_count += 1
            new_value = self.__visit("visitProgram", lambda i=child : self.visit(i))
            result = f'{result}\nExpression[{expression_count}]: {new_value};'
        self.scope_handler.pop_scope()
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


    # Visit a parse tree produced by qutesParser#ExpressionStatement.
    def visitExpressionStatement(self, ctx:qutesParser.ExpressionStatementContext):
        return self.__visit("visitExpressionStatement", lambda : self.visitChildren(ctx.expr()))


    # Visit a parse tree produced by qutesParser#EmptyStatement.
    def visitEmptyStatement(self, ctx:qutesParser.EmptyStatementContext):
        return self.__visit("visitEmptyStatement", lambda : self.visitChildren(ctx))


    # Visit a parse tree produced by qutesParser#BlockStatement.
    def visitBlockStatement(self, ctx:qutesParser.BlockStatementContext):
        return self.__visit("visitBlockStatement", lambda : self.visitChildren(ctx), push_pop_scope=True)


    # Visit a parse tree produced by qutesParser#DeclarationStatement.
    def visitDeclarationStatement(self, ctx:qutesParser.DeclarationStatementContext):
        var_type = ctx.variableType().getText()
        var_name = ctx.variableName().getText()
        var_value = "default_var_value"
        if(ctx.expr()):
            var_value = self.visitChildren(ctx.expr())
        if(ctx.parenExpr()):
            var_value = self.visitChildren(ctx.parenExpr())

        self.__update_variable_state(var_name, var_value)

        return str(var_type) + " " + str(var_name) + " = " + str(var_value)
    

    # Visit a parse tree produced by qutesParser#AssignmentStatement.
    def visitAssignmentStatement(self, ctx:qutesParser.AssignmentStatementContext): 
        return self.__visit("visitAssignmentStatement", lambda : self.__visit_assignment_statement(ctx))

    def __visit_assignment_statement(self, ctx:qutesParser.AssignmentStatementContext):
        var_name = ctx.qualifiedName().getText()
        var_value = "default_var_value"
        if(ctx.expr()):
            var_value = self.visitChildren(ctx.expr())
        if(ctx.parenExpr()):
            var_value = self.visitChildren(ctx.parenExpr())

        self.__update_variable_state(var_name, var_value)

        return str(var_name) + " = " + str(var_value)

    def __update_variable_state(self, var_name, new_value):
        #TODO: check if type is compatible        
        # symbol_to_update = list[Symbol](filter(lambda symbol : symbol.name == var_name, self.scope_handler.current_symbols_scope.symbols))
        symbol_to_update = [symbol for symbol in self.scope_handler.current_symbols_scope.symbols if symbol.name == var_name ]
        if len(symbol_to_update) == 1:
            symbol_index_in_scope = self.scope_handler.current_symbols_scope.symbols.index(symbol_to_update[0])
            self.scope_handler.current_symbols_scope.symbols[symbol_index_in_scope].value = new_value
        elif len(symbol_to_update) > 1:
            raise SyntaxError(f"Multiple declaration of variable with name '{var_name}'.")
        else:
            raise SyntaxError(f"No variable declared with name '{var_name}'.")


    # Visit a parse tree produced by qutesParser#parenExpr.
    def visitParenExpr(self, ctx:qutesParser.ParenExprContext):
        return self.__visit("visitparenExpr", lambda : "( " + str(self.visitChildren(ctx)) + " )")


    # Visit a parse tree produced by qutesParser#expr.
    def visitExpr(self, ctx:qutesParser.ExprContext):
        return self.__visit("visitExpr", lambda : self.__visit_expr(ctx))
    def __visit_expr(self, ctx:qutesParser.ExprContext):
        result = "visitExpr-default"
        if(ctx.term()):
            if(self.log_trace_enabled): print("visitExpr -> term")
            result = self.visitChildren(ctx)
        if(ctx.test()):
            if(self.log_trace_enabled): print("visitExpr -> test")
            result = self.visitChildren(ctx)
        return result


    # Visit a parse tree produced by qutesParser#test.
    def visitTest(self, ctx:qutesParser.TestContext):
        return self.__visit("visitTest", lambda : self.__visit_test(ctx))

    def __visit_test(self, ctx:qutesParser.TestContext):
        result = "visitTest-default"
        if(ctx.GREATER()):
            if(self.log_trace_enabled): print("visitTest -> greater")
            result = self.visitChildren(ctx.term(0)) > self.visitChildren(ctx.term(1))
        if(ctx.LOWER()):
            if(self.log_trace_enabled): print("visitTest -> lower")
            result = self.visitChildren(ctx.term(0)) < self.visitChildren(ctx.term(1))
        if(ctx.EQUAL()):
            if(self.log_trace_enabled): print("visitTest -> equal")
            result = self.visitChildren(ctx.term(0)) == self.visitChildren(ctx.term(1))
        if(ctx.GREATEREQUAL()):
            if(self.log_trace_enabled): print("visitTest -> greater equal")
            result = self.visitChildren(ctx.term(0)) >= self.visitChildren(ctx.term(1))
        if(ctx.LOWEREQUAL()):
            if(self.log_trace_enabled): print("visitTest -> lower equal")
            result = self.visitChildren(ctx.term(0)) <= self.visitChildren(ctx.term(1))

        if(self.log_trace_enabled): print("visitTest -> test no operator")
        result = self.visitChildren(ctx.term(0))
        return result


    # Visit a parse tree produced by qutesParser#term.
    def visitTerm(self, ctx:qutesParser.TermContext):
        return self.__visit("visitTerm", lambda : self.__visit_term(ctx))
    def __visit_term(self, ctx:qutesParser.TermContext):
        result = "default_term_result"
        if(ctx.term(0)):
            if(self.log_trace_enabled): print("visitTerm -> operation")
            if(ctx.ADD()):
                result = self.visitChildren(ctx.term(0)) + self.visitChildren(ctx.term(1))
            if(ctx.SUB()):
                result = self.visitChildren(ctx.term(0)) - self.visitChildren(ctx.term(1))
        if(ctx.qualifiedName()):
            if(self.log_trace_enabled): print("visitTerm -> qualifiedName")
            result = self.visitChildren(ctx)
        if(ctx.string()):
            if(self.log_trace_enabled): print("visitTerm -> string")
            result = self.visitChildren(ctx)
        if(ctx.integer()):
            if(self.log_trace_enabled): print("visitTerm -> integer")
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
    def __visit(self, parent_caller_name, func, push_pop_scope:bool = False):
        if(self.log_trace_enabled): print("start " + parent_caller_name)
        if(push_pop_scope): self.scope_handler.push_scope()
        result = func()
        if(push_pop_scope): self.scope_handler.pop_scope()
        if(self.log_trace_enabled): print("end " + parent_caller_name)
        if(self.log_step_by_step_results_enabled): print(result)
        return result
