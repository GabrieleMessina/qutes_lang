# Generated from d:/Users/gabry/Universita/quantum_computing/qutes_lang/Qutes.g4 by ANTLR 4.13.1
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO

def serializedATN():
    return [
        4,1,23,103,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,
        6,2,7,7,7,2,8,7,8,1,0,4,0,20,8,0,11,0,12,0,21,1,1,1,1,1,1,1,1,1,
        1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,
        1,5,1,45,8,1,10,1,12,1,48,9,1,1,1,1,1,1,1,1,1,1,1,3,1,55,8,1,1,1,
        1,1,1,1,1,1,1,1,1,1,3,1,63,8,1,1,2,1,2,1,2,1,2,1,3,1,3,1,3,3,3,72,
        8,3,1,4,1,4,1,4,1,4,1,4,3,4,79,8,4,1,5,1,5,1,5,1,5,3,5,85,8,5,1,
        5,1,5,1,5,5,5,90,8,5,10,5,12,5,93,9,5,1,6,1,6,1,7,1,7,1,7,1,7,1,
        8,1,8,1,8,0,1,10,9,0,2,4,6,8,10,12,14,16,0,2,1,0,5,9,1,0,3,4,109,
        0,19,1,0,0,0,2,62,1,0,0,0,4,64,1,0,0,0,6,71,1,0,0,0,8,78,1,0,0,0,
        10,84,1,0,0,0,12,94,1,0,0,0,14,96,1,0,0,0,16,100,1,0,0,0,18,20,3,
        2,1,0,19,18,1,0,0,0,20,21,1,0,0,0,21,19,1,0,0,0,21,22,1,0,0,0,22,
        1,1,0,0,0,23,24,5,12,0,0,24,25,3,4,2,0,25,26,3,2,1,0,26,63,1,0,0,
        0,27,28,5,12,0,0,28,29,3,4,2,0,29,30,3,2,1,0,30,31,5,13,0,0,31,32,
        3,2,1,0,32,63,1,0,0,0,33,34,5,14,0,0,34,35,3,4,2,0,35,36,3,2,1,0,
        36,63,1,0,0,0,37,38,5,15,0,0,38,39,3,2,1,0,39,40,5,14,0,0,40,41,
        3,4,2,0,41,63,1,0,0,0,42,46,5,16,0,0,43,45,3,2,1,0,44,43,1,0,0,0,
        45,48,1,0,0,0,46,44,1,0,0,0,46,47,1,0,0,0,47,49,1,0,0,0,48,46,1,
        0,0,0,49,63,5,17,0,0,50,51,3,12,6,0,51,54,5,10,0,0,52,55,3,6,3,0,
        53,55,3,4,2,0,54,52,1,0,0,0,54,53,1,0,0,0,55,56,1,0,0,0,56,57,5,
        11,0,0,57,63,1,0,0,0,58,59,3,6,3,0,59,60,5,11,0,0,60,63,1,0,0,0,
        61,63,5,11,0,0,62,23,1,0,0,0,62,27,1,0,0,0,62,33,1,0,0,0,62,37,1,
        0,0,0,62,42,1,0,0,0,62,50,1,0,0,0,62,58,1,0,0,0,62,61,1,0,0,0,63,
        3,1,0,0,0,64,65,5,1,0,0,65,66,3,6,3,0,66,67,5,2,0,0,67,5,1,0,0,0,
        68,72,3,10,5,0,69,72,3,8,4,0,70,72,3,4,2,0,71,68,1,0,0,0,71,69,1,
        0,0,0,71,70,1,0,0,0,72,7,1,0,0,0,73,79,3,10,5,0,74,75,3,10,5,0,75,
        76,7,0,0,0,76,77,3,10,5,0,77,79,1,0,0,0,78,73,1,0,0,0,78,74,1,0,
        0,0,79,9,1,0,0,0,80,81,6,5,-1,0,81,85,3,14,7,0,82,85,3,16,8,0,83,
        85,3,12,6,0,84,80,1,0,0,0,84,82,1,0,0,0,84,83,1,0,0,0,85,91,1,0,
        0,0,86,87,10,3,0,0,87,88,7,1,0,0,88,90,3,10,5,4,89,86,1,0,0,0,90,
        93,1,0,0,0,91,89,1,0,0,0,91,92,1,0,0,0,92,11,1,0,0,0,93,91,1,0,0,
        0,94,95,5,21,0,0,95,13,1,0,0,0,96,97,5,18,0,0,97,98,5,21,0,0,98,
        99,5,18,0,0,99,15,1,0,0,0,100,101,5,20,0,0,101,17,1,0,0,0,8,21,46,
        54,62,71,78,84,91
    ]

class QutesParser ( Parser ):

    grammarFileName = "Qutes.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'('", "')'", "'+'", "'-'", "'=='", "'>'", 
                     "'>='", "'<'", "'<='", "'='", "';'", "'if'", "'else'", 
                     "'while'", "'do'", "'{'", "'}'", "'\"'" ]

    symbolicNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "ADD", "SUB", 
                      "EQUAL", "GREATER", "GREATEREQUAL", "LOWER", "LOWEREQUAL", 
                      "ASSIGN", "END_OF_STATEMENT", "IF_STATEMENT", "ELSE_STATEMENT", 
                      "WHILE_STATEMENT", "DO_STATEMENT", "BLOCK_STATEMENT_START", 
                      "BLOCK_STATEMENT_END", "STRING_ENCLOSURE", "END_OF_PROGRAM", 
                      "INT", "STRING", "WS", "NEWLINE" ]

    RULE_program = 0
    RULE_statement = 1
    RULE_paren_expr = 2
    RULE_expr = 3
    RULE_test = 4
    RULE_term = 5
    RULE_variableName = 6
    RULE_string = 7
    RULE_integer = 8

    ruleNames =  [ "program", "statement", "paren_expr", "expr", "test", 
                   "term", "variableName", "string", "integer" ]

    EOF = Token.EOF
    T__0=1
    T__1=2
    ADD=3
    SUB=4
    EQUAL=5
    GREATER=6
    GREATEREQUAL=7
    LOWER=8
    LOWEREQUAL=9
    ASSIGN=10
    END_OF_STATEMENT=11
    IF_STATEMENT=12
    ELSE_STATEMENT=13
    WHILE_STATEMENT=14
    DO_STATEMENT=15
    BLOCK_STATEMENT_START=16
    BLOCK_STATEMENT_END=17
    STRING_ENCLOSURE=18
    END_OF_PROGRAM=19
    INT=20
    STRING=21
    WS=22
    NEWLINE=23

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.1")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class ProgramContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def statement(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(QutesParser.StatementContext)
            else:
                return self.getTypedRuleContext(QutesParser.StatementContext,i)


        def getRuleIndex(self):
            return QutesParser.RULE_program

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterProgram" ):
                listener.enterProgram(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitProgram" ):
                listener.exitProgram(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitProgram" ):
                return visitor.visitProgram(self)
            else:
                return visitor.visitChildren(self)




    def program(self):

        localctx = QutesParser.ProgramContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_program)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 19 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 18
                self.statement()
                self.state = 21 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not ((((_la) & ~0x3f) == 0 and ((1 << _la) & 3528706) != 0)):
                    break

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class StatementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return QutesParser.RULE_statement

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class IfStatementContext(StatementContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a QutesParser.StatementContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def IF_STATEMENT(self):
            return self.getToken(QutesParser.IF_STATEMENT, 0)
        def paren_expr(self):
            return self.getTypedRuleContext(QutesParser.Paren_exprContext,0)

        def statement(self):
            return self.getTypedRuleContext(QutesParser.StatementContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterIfStatement" ):
                listener.enterIfStatement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitIfStatement" ):
                listener.exitIfStatement(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitIfStatement" ):
                return visitor.visitIfStatement(self)
            else:
                return visitor.visitChildren(self)


    class AssignmentStatementContext(StatementContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a QutesParser.StatementContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def variableName(self):
            return self.getTypedRuleContext(QutesParser.VariableNameContext,0)

        def ASSIGN(self):
            return self.getToken(QutesParser.ASSIGN, 0)
        def END_OF_STATEMENT(self):
            return self.getToken(QutesParser.END_OF_STATEMENT, 0)
        def expr(self):
            return self.getTypedRuleContext(QutesParser.ExprContext,0)

        def paren_expr(self):
            return self.getTypedRuleContext(QutesParser.Paren_exprContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAssignmentStatement" ):
                listener.enterAssignmentStatement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAssignmentStatement" ):
                listener.exitAssignmentStatement(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAssignmentStatement" ):
                return visitor.visitAssignmentStatement(self)
            else:
                return visitor.visitChildren(self)


    class ExpressionStatementContext(StatementContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a QutesParser.StatementContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self):
            return self.getTypedRuleContext(QutesParser.ExprContext,0)

        def END_OF_STATEMENT(self):
            return self.getToken(QutesParser.END_OF_STATEMENT, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterExpressionStatement" ):
                listener.enterExpressionStatement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitExpressionStatement" ):
                listener.exitExpressionStatement(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitExpressionStatement" ):
                return visitor.visitExpressionStatement(self)
            else:
                return visitor.visitChildren(self)


    class IfElseStatementContext(StatementContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a QutesParser.StatementContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def IF_STATEMENT(self):
            return self.getToken(QutesParser.IF_STATEMENT, 0)
        def paren_expr(self):
            return self.getTypedRuleContext(QutesParser.Paren_exprContext,0)

        def statement(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(QutesParser.StatementContext)
            else:
                return self.getTypedRuleContext(QutesParser.StatementContext,i)

        def ELSE_STATEMENT(self):
            return self.getToken(QutesParser.ELSE_STATEMENT, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterIfElseStatement" ):
                listener.enterIfElseStatement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitIfElseStatement" ):
                listener.exitIfElseStatement(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitIfElseStatement" ):
                return visitor.visitIfElseStatement(self)
            else:
                return visitor.visitChildren(self)


    class EmptyStatementContext(StatementContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a QutesParser.StatementContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def END_OF_STATEMENT(self):
            return self.getToken(QutesParser.END_OF_STATEMENT, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterEmptyStatement" ):
                listener.enterEmptyStatement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitEmptyStatement" ):
                listener.exitEmptyStatement(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitEmptyStatement" ):
                return visitor.visitEmptyStatement(self)
            else:
                return visitor.visitChildren(self)


    class BlockStatementContext(StatementContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a QutesParser.StatementContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def BLOCK_STATEMENT_START(self):
            return self.getToken(QutesParser.BLOCK_STATEMENT_START, 0)
        def BLOCK_STATEMENT_END(self):
            return self.getToken(QutesParser.BLOCK_STATEMENT_END, 0)
        def statement(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(QutesParser.StatementContext)
            else:
                return self.getTypedRuleContext(QutesParser.StatementContext,i)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterBlockStatement" ):
                listener.enterBlockStatement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitBlockStatement" ):
                listener.exitBlockStatement(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitBlockStatement" ):
                return visitor.visitBlockStatement(self)
            else:
                return visitor.visitChildren(self)


    class WhileStatementContext(StatementContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a QutesParser.StatementContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def WHILE_STATEMENT(self):
            return self.getToken(QutesParser.WHILE_STATEMENT, 0)
        def paren_expr(self):
            return self.getTypedRuleContext(QutesParser.Paren_exprContext,0)

        def statement(self):
            return self.getTypedRuleContext(QutesParser.StatementContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterWhileStatement" ):
                listener.enterWhileStatement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitWhileStatement" ):
                listener.exitWhileStatement(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitWhileStatement" ):
                return visitor.visitWhileStatement(self)
            else:
                return visitor.visitChildren(self)


    class DoWhileStatementContext(StatementContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a QutesParser.StatementContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def DO_STATEMENT(self):
            return self.getToken(QutesParser.DO_STATEMENT, 0)
        def statement(self):
            return self.getTypedRuleContext(QutesParser.StatementContext,0)

        def WHILE_STATEMENT(self):
            return self.getToken(QutesParser.WHILE_STATEMENT, 0)
        def paren_expr(self):
            return self.getTypedRuleContext(QutesParser.Paren_exprContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDoWhileStatement" ):
                listener.enterDoWhileStatement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDoWhileStatement" ):
                listener.exitDoWhileStatement(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitDoWhileStatement" ):
                return visitor.visitDoWhileStatement(self)
            else:
                return visitor.visitChildren(self)



    def statement(self):

        localctx = QutesParser.StatementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_statement)
        self._la = 0 # Token type
        try:
            self.state = 62
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,3,self._ctx)
            if la_ == 1:
                localctx = QutesParser.IfStatementContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 23
                self.match(QutesParser.IF_STATEMENT)
                self.state = 24
                self.paren_expr()
                self.state = 25
                self.statement()
                pass

            elif la_ == 2:
                localctx = QutesParser.IfElseStatementContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 27
                self.match(QutesParser.IF_STATEMENT)
                self.state = 28
                self.paren_expr()
                self.state = 29
                self.statement()
                self.state = 30
                self.match(QutesParser.ELSE_STATEMENT)
                self.state = 31
                self.statement()
                pass

            elif la_ == 3:
                localctx = QutesParser.WhileStatementContext(self, localctx)
                self.enterOuterAlt(localctx, 3)
                self.state = 33
                self.match(QutesParser.WHILE_STATEMENT)
                self.state = 34
                self.paren_expr()
                self.state = 35
                self.statement()
                pass

            elif la_ == 4:
                localctx = QutesParser.DoWhileStatementContext(self, localctx)
                self.enterOuterAlt(localctx, 4)
                self.state = 37
                self.match(QutesParser.DO_STATEMENT)
                self.state = 38
                self.statement()
                self.state = 39
                self.match(QutesParser.WHILE_STATEMENT)
                self.state = 40
                self.paren_expr()
                pass

            elif la_ == 5:
                localctx = QutesParser.BlockStatementContext(self, localctx)
                self.enterOuterAlt(localctx, 5)
                self.state = 42
                self.match(QutesParser.BLOCK_STATEMENT_START)
                self.state = 46
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while (((_la) & ~0x3f) == 0 and ((1 << _la) & 3528706) != 0):
                    self.state = 43
                    self.statement()
                    self.state = 48
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 49
                self.match(QutesParser.BLOCK_STATEMENT_END)
                pass

            elif la_ == 6:
                localctx = QutesParser.AssignmentStatementContext(self, localctx)
                self.enterOuterAlt(localctx, 6)
                self.state = 50
                self.variableName()
                self.state = 51
                self.match(QutesParser.ASSIGN)
                self.state = 54
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input,2,self._ctx)
                if la_ == 1:
                    self.state = 52
                    self.expr()
                    pass

                elif la_ == 2:
                    self.state = 53
                    self.paren_expr()
                    pass


                self.state = 56
                self.match(QutesParser.END_OF_STATEMENT)
                pass

            elif la_ == 7:
                localctx = QutesParser.ExpressionStatementContext(self, localctx)
                self.enterOuterAlt(localctx, 7)
                self.state = 58
                self.expr()
                self.state = 59
                self.match(QutesParser.END_OF_STATEMENT)
                pass

            elif la_ == 8:
                localctx = QutesParser.EmptyStatementContext(self, localctx)
                self.enterOuterAlt(localctx, 8)
                self.state = 61
                self.match(QutesParser.END_OF_STATEMENT)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Paren_exprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def expr(self):
            return self.getTypedRuleContext(QutesParser.ExprContext,0)


        def getRuleIndex(self):
            return QutesParser.RULE_paren_expr

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterParen_expr" ):
                listener.enterParen_expr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitParen_expr" ):
                listener.exitParen_expr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitParen_expr" ):
                return visitor.visitParen_expr(self)
            else:
                return visitor.visitChildren(self)




    def paren_expr(self):

        localctx = QutesParser.Paren_exprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_paren_expr)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 64
            self.match(QutesParser.T__0)
            self.state = 65
            self.expr()
            self.state = 66
            self.match(QutesParser.T__1)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def term(self):
            return self.getTypedRuleContext(QutesParser.TermContext,0)


        def test(self):
            return self.getTypedRuleContext(QutesParser.TestContext,0)


        def paren_expr(self):
            return self.getTypedRuleContext(QutesParser.Paren_exprContext,0)


        def getRuleIndex(self):
            return QutesParser.RULE_expr

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterExpr" ):
                listener.enterExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitExpr" ):
                listener.exitExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitExpr" ):
                return visitor.visitExpr(self)
            else:
                return visitor.visitChildren(self)




    def expr(self):

        localctx = QutesParser.ExprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_expr)
        try:
            self.state = 71
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,4,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 68
                self.term(0)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 69
                self.test()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 70
                self.paren_expr()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class TestContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.op = None # Token

        def term(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(QutesParser.TermContext)
            else:
                return self.getTypedRuleContext(QutesParser.TermContext,i)


        def GREATER(self):
            return self.getToken(QutesParser.GREATER, 0)

        def LOWER(self):
            return self.getToken(QutesParser.LOWER, 0)

        def EQUAL(self):
            return self.getToken(QutesParser.EQUAL, 0)

        def GREATEREQUAL(self):
            return self.getToken(QutesParser.GREATEREQUAL, 0)

        def LOWEREQUAL(self):
            return self.getToken(QutesParser.LOWEREQUAL, 0)

        def getRuleIndex(self):
            return QutesParser.RULE_test

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTest" ):
                listener.enterTest(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTest" ):
                listener.exitTest(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitTest" ):
                return visitor.visitTest(self)
            else:
                return visitor.visitChildren(self)




    def test(self):

        localctx = QutesParser.TestContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_test)
        self._la = 0 # Token type
        try:
            self.state = 78
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,5,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 73
                self.term(0)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 74
                self.term(0)
                self.state = 75
                localctx.op = self._input.LT(1)
                _la = self._input.LA(1)
                if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 992) != 0)):
                    localctx.op = self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 76
                self.term(0)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class TermContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.op = None # Token

        def string(self):
            return self.getTypedRuleContext(QutesParser.StringContext,0)


        def integer(self):
            return self.getTypedRuleContext(QutesParser.IntegerContext,0)


        def variableName(self):
            return self.getTypedRuleContext(QutesParser.VariableNameContext,0)


        def term(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(QutesParser.TermContext)
            else:
                return self.getTypedRuleContext(QutesParser.TermContext,i)


        def ADD(self):
            return self.getToken(QutesParser.ADD, 0)

        def SUB(self):
            return self.getToken(QutesParser.SUB, 0)

        def getRuleIndex(self):
            return QutesParser.RULE_term

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTerm" ):
                listener.enterTerm(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTerm" ):
                listener.exitTerm(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitTerm" ):
                return visitor.visitTerm(self)
            else:
                return visitor.visitChildren(self)



    def term(self, _p:int=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = QutesParser.TermContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 10
        self.enterRecursionRule(localctx, 10, self.RULE_term, _p)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 84
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [18]:
                self.state = 81
                self.string()
                pass
            elif token in [20]:
                self.state = 82
                self.integer()
                pass
            elif token in [21]:
                self.state = 83
                self.variableName()
                pass
            else:
                raise NoViableAltException(self)

            self._ctx.stop = self._input.LT(-1)
            self.state = 91
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,7,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    localctx = QutesParser.TermContext(self, _parentctx, _parentState)
                    self.pushNewRecursionContext(localctx, _startState, self.RULE_term)
                    self.state = 86
                    if not self.precpred(self._ctx, 3):
                        from antlr4.error.Errors import FailedPredicateException
                        raise FailedPredicateException(self, "self.precpred(self._ctx, 3)")
                    self.state = 87
                    localctx.op = self._input.LT(1)
                    _la = self._input.LA(1)
                    if not(_la==3 or _la==4):
                        localctx.op = self._errHandler.recoverInline(self)
                    else:
                        self._errHandler.reportMatch(self)
                        self.consume()
                    self.state = 88
                    self.term(4) 
                self.state = 93
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,7,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.unrollRecursionContexts(_parentctx)
        return localctx


    class VariableNameContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def STRING(self):
            return self.getToken(QutesParser.STRING, 0)

        def getRuleIndex(self):
            return QutesParser.RULE_variableName

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterVariableName" ):
                listener.enterVariableName(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitVariableName" ):
                listener.exitVariableName(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitVariableName" ):
                return visitor.visitVariableName(self)
            else:
                return visitor.visitChildren(self)




    def variableName(self):

        localctx = QutesParser.VariableNameContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_variableName)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 94
            self.match(QutesParser.STRING)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class StringContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def STRING_ENCLOSURE(self, i:int=None):
            if i is None:
                return self.getTokens(QutesParser.STRING_ENCLOSURE)
            else:
                return self.getToken(QutesParser.STRING_ENCLOSURE, i)

        def STRING(self):
            return self.getToken(QutesParser.STRING, 0)

        def getRuleIndex(self):
            return QutesParser.RULE_string

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterString" ):
                listener.enterString(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitString" ):
                listener.exitString(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitString" ):
                return visitor.visitString(self)
            else:
                return visitor.visitChildren(self)




    def string(self):

        localctx = QutesParser.StringContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_string)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 96
            self.match(QutesParser.STRING_ENCLOSURE)
            self.state = 97
            self.match(QutesParser.STRING)
            self.state = 98
            self.match(QutesParser.STRING_ENCLOSURE)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class IntegerContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def INT(self):
            return self.getToken(QutesParser.INT, 0)

        def getRuleIndex(self):
            return QutesParser.RULE_integer

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterInteger" ):
                listener.enterInteger(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitInteger" ):
                listener.exitInteger(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitInteger" ):
                return visitor.visitInteger(self)
            else:
                return visitor.visitChildren(self)




    def integer(self):

        localctx = QutesParser.IntegerContext(self, self._ctx, self.state)
        self.enterRule(localctx, 16, self.RULE_integer)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 100
            self.match(QutesParser.INT)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx



    def sempred(self, localctx:RuleContext, ruleIndex:int, predIndex:int):
        if self._predicates == None:
            self._predicates = dict()
        self._predicates[5] = self.term_sempred
        pred = self._predicates.get(ruleIndex, None)
        if pred is None:
            raise Exception("No predicate with index:" + str(ruleIndex))
        else:
            return pred(localctx, predIndex)

    def term_sempred(self, localctx:TermContext, predIndex:int):
            if predIndex == 0:
                return self.precpred(self._ctx, 3)
         




