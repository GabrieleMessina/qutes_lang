"""An antlr visitor for the qutes grammar."""

from qutes_parser import QutesParser as qutesParser
from qutes_antlr.qutes_parserVisitor import qutes_parserVisitor as qutesVisitor
from symbols.scope_tree_node import ScopeTreeNode
from symbols.scope_handler import ScopeHandlerForSymbolsUpdate
from symbols.variables_handler import VariablesHandler
from symbols.qutes_types import Qubit, Quint

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
        self.variables_handler = VariablesHandler(self.scope_handler)

        # Debug flags
        self.log_trace_enabled = False
        self.log_step_by_step_results_enabled = False

    # Visit a parse tree produced by qutesParser#program.
    def visitProgram(self, ctx:qutesParser.ProgramContext):
        self.scope_handler.push_scope()
        result = str()
        statement_count = 0
        for child in ctx.getChildren(lambda child : isinstance(child, qutesParser.StatementContext)):
            statement_count += 1
            new_value = self.__visit("visitProgram", lambda i=child : self.visit(i))
            result = f'{result}\nStatement[{statement_count}]: {new_value}'
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
        self.scope_handler.push_scope()
        result = str()
        statement_count = 0
        for child in ctx.getChildren(lambda child : isinstance(child, qutesParser.StatementContext)):
            statement_count += 1
            new_value = str(self.__visit("visitBlockStatement", lambda i=child : self.visit(i))).replace("\n", "\n\t")
            result = f'{result}\n\tStatement[{statement_count}]: {new_value}'
        self.scope_handler.pop_scope()
        return result
    

    # Visit a parse tree produced by qutesParser#DeclarationStatement.
    def visitDeclarationStatement(self, ctx:qutesParser.DeclarationStatementContext):
        var_type = ctx.variableType().getText() # we already know the variable type thanks to the discovery listener.
        var_name = ctx.variableName().getText()
        var_value = None

        return self.__visit("visitAssignmentStatement", lambda : self.__visit_assignment_statement(var_type, var_name, var_value, ctx))
        

    # Visit a parse tree produced by qutesParser#AssignmentStatement.
    def visitAssignmentStatement(self, ctx:qutesParser.AssignmentStatementContext): 
        var_name = ctx.qualifiedName().getText()
        var_value = None
        return self.__visit("visitAssignmentStatement", lambda : self.__visit_assignment_statement(None, var_name, var_value, ctx))

    def __visit_assignment_statement(self, var_type : str, var_name : str, var_value, ctx:(qutesParser.AssignmentStatementContext | qutesParser.DeclarationStatementContext)):
        if(ctx.expr()):
            var_value = self.visitChildren(ctx.expr())
        if(ctx.parenExpr()):
            var_value = self.visitChildren(ctx.parenExpr())

        if(var_value != None):
            self.variables_handler.update_variable_state(var_name, var_value)

        if(isinstance(ctx, qutesParser.AssignmentStatementContext)):
            return str(var_name) + " = " + str(var_value)
        
        else:
            if(var_value != None):
                self.variables_handler.update_variable_state(var_name, var_value)
                return str(var_type) + " " + str(var_name) + " = " + str(var_value)
            else:
                return str(var_type) + " " + str(var_name)


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
        if(ctx.boolean()):
            if(self.log_trace_enabled): print("visitTerm -> boolean")
            result = self.visitChildren(ctx)
        if(ctx.integer()):
            if(self.log_trace_enabled): print("visitTerm -> integer")
            result = self.visitChildren(ctx)
        if(ctx.float_()):
            if(self.log_trace_enabled): print("visitTerm -> float")
            result = self.visitChildren(ctx)
        if(ctx.qubit()):
            if(self.log_trace_enabled): print("visitTerm -> qubit")
            result = self.visitChildren(ctx)
        if(ctx.quint()):
            if(self.log_trace_enabled): print("visitTerm -> quint")
            result = self.visitChildren(ctx)
        if(ctx.qualifiedName()):
            if(self.log_trace_enabled): print("visitTerm -> qualifiedName")
            result = self.visitChildren(ctx)
        if(ctx.string()):
            if(self.log_trace_enabled): print("visitTerm -> string")
            result = self.visitChildren(ctx)
        return result


    # Visit a parse tree produced by qutesParser#variableType.
    def visitVariableType(self, ctx:qutesParser.VariableTypeContext):
        return self.__visit("visitVariableType", lambda : str(ctx.getText()))


    # Visit a parse tree produced by qutesParser#qualifiedName.
    def visitQualifiedName(self, ctx:qutesParser.QualifiedNameContext):
        var_name = str(ctx.getText());
        symbol_to_resolve = [symbol for symbol in self.scope_handler.current_symbols_scope.symbols if symbol.name == var_name]
        if len(symbol_to_resolve) > 0:
            # Get the last matching symbol (so that we handle symbol hyding in a scope that is a child of another that already has this variable declared)
            return self.__visit("visitQualifiedName", lambda : symbol_to_resolve[-1].value)
        else:
            raise SyntaxError(f"No variable declared with name '{var_name}'.")


    # Visit a parse tree produced by qutesParser#id.
    def visitString(self, ctx:qutesParser.StringContext):
        string_literal_enclosure = qutesParser.literaltostring(qutesParser.STRING_ENCLOSURE)
        return self.__visit("visitString", lambda : str(
            ctx.getText()
                .removeprefix(string_literal_enclosure)
                .removesuffix(string_literal_enclosure)
            )
        )

    
    # Visit a parse tree produced by qutesParser#qubit.
    def visitQubit(self, ctx:qutesParser.QubitContext):
       return self.__visit("visitQubit", lambda : Qubit().fromstr(ctx.getText()))
    
    # Visit a parse tree produced by qutesParser#quint.
    def visitQuint(self, ctx:qutesParser.QuintContext):
       return self.__visit("visitQuint", lambda : Quint().fromstr(ctx.getText()))

    # Visit a parse tree produced by qutesParser#float.
    def visitFloat(self, ctx:qutesParser.FloatContext):
        return self.__visit("visitFloat", lambda : float(ctx.getText()))


    # Visit a parse tree produced by qutesParser#integer.
    def visitInteger(self, ctx:qutesParser.IntegerContext):
        return self.__visit("visitInteger", lambda : int(ctx.getText()))


    # Visit a parse tree produced by qutesParser#integer.
    def visitVariableName(self, ctx:qutesParser.VariableNameContext):
        return self.__visit("visitVariableName", lambda : str(ctx.getText()))

    # Visit a parse tree produced by qutes_parser#boolean.
    def visitBoolean(self, ctx:qutesParser.BooleanContext):
        return self.__visit("visitBoolean", lambda : ctx.getText().lower() == "true" or ctx.getText() == "1")


    # Utility method for logging and scaffolding operation
    def __visit(self, parent_caller_name, func, push_pop_scope:bool = False):
        if(self.log_trace_enabled): print("start " + parent_caller_name)
        if(push_pop_scope): self.scope_handler.push_scope()
        result = func()
        if(push_pop_scope): self.scope_handler.pop_scope()
        if(self.log_trace_enabled): print("end " + parent_caller_name)
        if(self.log_step_by_step_results_enabled): print(result)
        return result
