"""An antlr listener for the qutes grammar."""

from qutes_antlr.qutesListener import qutesListener
from qutes_antlr.qutesParser import qutesParser
from symbols.scope_tree_node import ScopeTreeNode, ScopeType, SymbolType, Symbol
from anytree import RenderTree

class SymbolsDiscoveryListener(qutesListener):
    """An antlr listener for the qutes grammar that discovers symbols like variable, function names etc."""

    def __init__(self):
        # Symbol Resolving Tree
        self.symbols_tree:ScopeTreeNode = None
        self.current_symbols_scope:ScopeTreeNode = None


    def __push_scope__(self, scope:ScopeType, scope_detail:str) -> ScopeTreeNode:
        new_scope = ScopeTreeNode(scope, scope_detail, self.current_symbols_scope)
        # this cross reference is handled by anytree.
        # if(self.current_symbols_scope):
        #     if(self.current_symbols_scope.children):
        #         self.current_symbols_scope.children = list(self.current_symbols_scope.children) + [new_scope]
        #     else: self.current_symbols_scope.children = [new_scope]
        self.current_symbols_scope = new_scope
        return self.current_symbols_scope
    
    def __pop_scope__(self) -> ScopeTreeNode:
        self.current_symbols_scope = self.current_symbols_scope.parent
        return self.current_symbols_scope

    # Enter a parse tree produced by qutesParser#program.
    def enterProgram(self, ctx:qutesParser.ProgramContext):
        self.__push_scope__(ScopeType.GlobalScope, "Init")
        self.symbols_tree = self.current_symbols_scope

    # Exit a parse tree produced by qutesParser#program.
    def exitProgram(self, ctx:qutesParser.ProgramContext):
        for pre, _, node in RenderTree(self.symbols_tree):
            print("%s%s Symbols: %s" % (pre, node.scope_type, node.symbols))
        self.symbols_tree = None
        self.current_symbols_scope = None


    # Enter a parse tree produced by qutesParser#IfStatement.
    def enterIfStatement(self, ctx:qutesParser.IfStatementContext):
        self.__push_scope__(ScopeType.LocalScope, "If")

    # Exit a parse tree produced by qutesParser#IfStatement.
    def exitIfStatement(self, ctx:qutesParser.IfStatementContext):
        self.__pop_scope__()


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
        self.__push_scope__(ScopeType.LocalScope, "If")

    # Exit a parse tree produced by qutesParser#BlockStatement.
    def exitBlockStatement(self, ctx:qutesParser.BlockStatementContext):
        self.__pop_scope__()


    # Enter a parse tree produced by qutesParser#AssignmentStatement.
    def enterAssignmentStatement(self, ctx:qutesParser.AssignmentStatementContext):
        self.current_symbols_scope.symbols.append(Symbol(ctx.variableName().getText(), SymbolType.VariableSymbol, "NA", self.current_symbols_scope))

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
