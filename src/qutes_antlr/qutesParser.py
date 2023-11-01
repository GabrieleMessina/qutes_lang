# Generated from /workspaces/qutes_lang/specification/grammar/qutes.g4 by ANTLR 4.13.1
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
        4,1,28,132,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,
        6,2,7,7,7,2,8,7,8,2,9,7,9,2,10,7,10,2,11,7,11,1,0,1,0,1,1,4,1,28,
        8,1,11,1,12,1,29,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,
        1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,5,2,53,8,2,10,2,12,2,56,9,2,
        1,2,1,2,1,2,1,2,1,2,1,2,3,2,64,8,2,1,2,1,2,1,2,1,2,1,2,1,2,3,2,72,
        8,2,1,2,1,2,1,2,1,2,1,2,1,2,3,2,80,8,2,1,3,1,3,1,3,1,3,1,4,1,4,1,
        4,3,4,89,8,4,1,5,1,5,1,5,1,5,1,5,3,5,96,8,5,1,6,1,6,1,6,1,6,3,6,
        102,8,6,1,6,1,6,1,6,5,6,107,8,6,10,6,12,6,110,9,6,1,7,1,7,3,7,114,
        8,7,1,8,1,8,1,8,5,8,119,8,8,10,8,12,8,122,9,8,1,9,1,9,1,10,1,10,
        1,10,1,10,1,11,1,11,1,11,0,1,12,12,0,2,4,6,8,10,12,14,16,18,20,22,
        0,3,1,0,4,6,1,0,9,13,1,0,7,8,139,0,24,1,0,0,0,2,27,1,0,0,0,4,79,
        1,0,0,0,6,81,1,0,0,0,8,88,1,0,0,0,10,95,1,0,0,0,12,101,1,0,0,0,14,
        113,1,0,0,0,16,115,1,0,0,0,18,123,1,0,0,0,20,125,1,0,0,0,22,129,
        1,0,0,0,24,25,7,0,0,0,25,1,1,0,0,0,26,28,3,4,2,0,27,26,1,0,0,0,28,
        29,1,0,0,0,29,27,1,0,0,0,29,30,1,0,0,0,30,3,1,0,0,0,31,32,5,17,0,
        0,32,33,3,6,3,0,33,34,3,4,2,0,34,80,1,0,0,0,35,36,5,17,0,0,36,37,
        3,6,3,0,37,38,3,4,2,0,38,39,5,18,0,0,39,40,3,4,2,0,40,80,1,0,0,0,
        41,42,5,19,0,0,42,43,3,6,3,0,43,44,3,4,2,0,44,80,1,0,0,0,45,46,5,
        20,0,0,46,47,3,4,2,0,47,48,5,19,0,0,48,49,3,6,3,0,49,80,1,0,0,0,
        50,54,5,21,0,0,51,53,3,4,2,0,52,51,1,0,0,0,53,56,1,0,0,0,54,52,1,
        0,0,0,54,55,1,0,0,0,55,57,1,0,0,0,56,54,1,0,0,0,57,80,5,22,0,0,58,
        59,3,14,7,0,59,60,3,18,9,0,60,63,5,14,0,0,61,64,3,8,4,0,62,64,3,
        6,3,0,63,61,1,0,0,0,63,62,1,0,0,0,64,65,1,0,0,0,65,66,5,15,0,0,66,
        80,1,0,0,0,67,68,3,16,8,0,68,71,5,14,0,0,69,72,3,8,4,0,70,72,3,6,
        3,0,71,69,1,0,0,0,71,70,1,0,0,0,72,73,1,0,0,0,73,74,5,15,0,0,74,
        80,1,0,0,0,75,76,3,8,4,0,76,77,5,15,0,0,77,80,1,0,0,0,78,80,5,15,
        0,0,79,31,1,0,0,0,79,35,1,0,0,0,79,41,1,0,0,0,79,45,1,0,0,0,79,50,
        1,0,0,0,79,58,1,0,0,0,79,67,1,0,0,0,79,75,1,0,0,0,79,78,1,0,0,0,
        80,5,1,0,0,0,81,82,5,1,0,0,82,83,3,8,4,0,83,84,5,2,0,0,84,7,1,0,
        0,0,85,89,3,12,6,0,86,89,3,10,5,0,87,89,3,6,3,0,88,85,1,0,0,0,88,
        86,1,0,0,0,88,87,1,0,0,0,89,9,1,0,0,0,90,96,3,12,6,0,91,92,3,12,
        6,0,92,93,7,1,0,0,93,94,3,12,6,0,94,96,1,0,0,0,95,90,1,0,0,0,95,
        91,1,0,0,0,96,11,1,0,0,0,97,98,6,6,-1,0,98,102,3,20,10,0,99,102,
        3,22,11,0,100,102,3,16,8,0,101,97,1,0,0,0,101,99,1,0,0,0,101,100,
        1,0,0,0,102,108,1,0,0,0,103,104,10,3,0,0,104,105,7,2,0,0,105,107,
        3,12,6,4,106,103,1,0,0,0,107,110,1,0,0,0,108,106,1,0,0,0,108,109,
        1,0,0,0,109,13,1,0,0,0,110,108,1,0,0,0,111,114,3,0,0,0,112,114,3,
        16,8,0,113,111,1,0,0,0,113,112,1,0,0,0,114,15,1,0,0,0,115,120,5,
        26,0,0,116,117,5,3,0,0,117,119,5,26,0,0,118,116,1,0,0,0,119,122,
        1,0,0,0,120,118,1,0,0,0,120,121,1,0,0,0,121,17,1,0,0,0,122,120,1,
        0,0,0,123,124,5,26,0,0,124,19,1,0,0,0,125,126,5,23,0,0,126,127,5,
        26,0,0,127,128,5,23,0,0,128,21,1,0,0,0,129,130,5,25,0,0,130,23,1,
        0,0,0,11,29,54,63,71,79,88,95,101,108,113,120
    ]

class qutesParser ( Parser ):

    grammarFileName = "qutes.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'('", "')'", "'.'", "'int'", "'string'", 
                     "'qubit'", "'+'", "'-'", "'=='", "'>'", "'>='", "'<'", 
                     "'<='", "'='", "';'", "'var'", "'if'", "'else'", "'while'", 
                     "'do'", "'{'", "'}'", "'\"'" ]

    symbolicNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "INT_TYPE", "STRING_TYPE", "QUBIT_TYPE", "ADD", "SUB", 
                      "EQUAL", "GREATER", "GREATEREQUAL", "LOWER", "LOWEREQUAL", 
                      "ASSIGN", "END_OF_STATEMENT", "VAR_STATEMENT", "IF_STATEMENT", 
                      "ELSE_STATEMENT", "WHILE_STATEMENT", "DO_STATEMENT", 
                      "BLOCK_STATEMENT_START", "BLOCK_STATEMENT_END", "STRING_ENCLOSURE", 
                      "END_OF_PROGRAM", "INT", "STRING", "WS", "NEWLINE" ]

    RULE_type = 0
    RULE_program = 1
    RULE_statement = 2
    RULE_parenExpr = 3
    RULE_expr = 4
    RULE_test = 5
    RULE_term = 6
    RULE_variableType = 7
    RULE_qualifiedName = 8
    RULE_variableName = 9
    RULE_string = 10
    RULE_integer = 11

    ruleNames =  [ "type", "program", "statement", "parenExpr", "expr", 
                   "test", "term", "variableType", "qualifiedName", "variableName", 
                   "string", "integer" ]

    EOF = Token.EOF
    T__0=1
    T__1=2
    T__2=3
    INT_TYPE=4
    STRING_TYPE=5
    QUBIT_TYPE=6
    ADD=7
    SUB=8
    EQUAL=9
    GREATER=10
    GREATEREQUAL=11
    LOWER=12
    LOWEREQUAL=13
    ASSIGN=14
    END_OF_STATEMENT=15
    VAR_STATEMENT=16
    IF_STATEMENT=17
    ELSE_STATEMENT=18
    WHILE_STATEMENT=19
    DO_STATEMENT=20
    BLOCK_STATEMENT_START=21
    BLOCK_STATEMENT_END=22
    STRING_ENCLOSURE=23
    END_OF_PROGRAM=24
    INT=25
    STRING=26
    WS=27
    NEWLINE=28

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.1")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class TypeContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def INT_TYPE(self):
            return self.getToken(qutesParser.INT_TYPE, 0)

        def STRING_TYPE(self):
            return self.getToken(qutesParser.STRING_TYPE, 0)

        def QUBIT_TYPE(self):
            return self.getToken(qutesParser.QUBIT_TYPE, 0)

        def getRuleIndex(self):
            return qutesParser.RULE_type

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterType" ):
                listener.enterType(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitType" ):
                listener.exitType(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitType" ):
                return visitor.visitType(self)
            else:
                return visitor.visitChildren(self)




    def type_(self):

        localctx = qutesParser.TypeContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_type)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 24
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 112) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ProgramContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def statement(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(qutesParser.StatementContext)
            else:
                return self.getTypedRuleContext(qutesParser.StatementContext,i)


        def getRuleIndex(self):
            return qutesParser.RULE_program

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

        localctx = qutesParser.ProgramContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_program)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 27 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 26
                self.statement()
                self.state = 29 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not ((((_la) & ~0x3f) == 0 and ((1 << _la) & 112885874) != 0)):
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
            return qutesParser.RULE_statement

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class IfStatementContext(StatementContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a qutesParser.StatementContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def IF_STATEMENT(self):
            return self.getToken(qutesParser.IF_STATEMENT, 0)
        def parenExpr(self):
            return self.getTypedRuleContext(qutesParser.ParenExprContext,0)

        def statement(self):
            return self.getTypedRuleContext(qutesParser.StatementContext,0)


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

        def __init__(self, parser, ctx:ParserRuleContext): # actually a qutesParser.StatementContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def qualifiedName(self):
            return self.getTypedRuleContext(qutesParser.QualifiedNameContext,0)

        def ASSIGN(self):
            return self.getToken(qutesParser.ASSIGN, 0)
        def END_OF_STATEMENT(self):
            return self.getToken(qutesParser.END_OF_STATEMENT, 0)
        def expr(self):
            return self.getTypedRuleContext(qutesParser.ExprContext,0)

        def parenExpr(self):
            return self.getTypedRuleContext(qutesParser.ParenExprContext,0)


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

        def __init__(self, parser, ctx:ParserRuleContext): # actually a qutesParser.StatementContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self):
            return self.getTypedRuleContext(qutesParser.ExprContext,0)

        def END_OF_STATEMENT(self):
            return self.getToken(qutesParser.END_OF_STATEMENT, 0)

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

        def __init__(self, parser, ctx:ParserRuleContext): # actually a qutesParser.StatementContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def IF_STATEMENT(self):
            return self.getToken(qutesParser.IF_STATEMENT, 0)
        def parenExpr(self):
            return self.getTypedRuleContext(qutesParser.ParenExprContext,0)

        def statement(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(qutesParser.StatementContext)
            else:
                return self.getTypedRuleContext(qutesParser.StatementContext,i)

        def ELSE_STATEMENT(self):
            return self.getToken(qutesParser.ELSE_STATEMENT, 0)

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

        def __init__(self, parser, ctx:ParserRuleContext): # actually a qutesParser.StatementContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def END_OF_STATEMENT(self):
            return self.getToken(qutesParser.END_OF_STATEMENT, 0)

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

        def __init__(self, parser, ctx:ParserRuleContext): # actually a qutesParser.StatementContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def BLOCK_STATEMENT_START(self):
            return self.getToken(qutesParser.BLOCK_STATEMENT_START, 0)
        def BLOCK_STATEMENT_END(self):
            return self.getToken(qutesParser.BLOCK_STATEMENT_END, 0)
        def statement(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(qutesParser.StatementContext)
            else:
                return self.getTypedRuleContext(qutesParser.StatementContext,i)


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

        def __init__(self, parser, ctx:ParserRuleContext): # actually a qutesParser.StatementContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def WHILE_STATEMENT(self):
            return self.getToken(qutesParser.WHILE_STATEMENT, 0)
        def parenExpr(self):
            return self.getTypedRuleContext(qutesParser.ParenExprContext,0)

        def statement(self):
            return self.getTypedRuleContext(qutesParser.StatementContext,0)


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

        def __init__(self, parser, ctx:ParserRuleContext): # actually a qutesParser.StatementContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def DO_STATEMENT(self):
            return self.getToken(qutesParser.DO_STATEMENT, 0)
        def statement(self):
            return self.getTypedRuleContext(qutesParser.StatementContext,0)

        def WHILE_STATEMENT(self):
            return self.getToken(qutesParser.WHILE_STATEMENT, 0)
        def parenExpr(self):
            return self.getTypedRuleContext(qutesParser.ParenExprContext,0)


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


    class DeclarationStatementContext(StatementContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a qutesParser.StatementContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def variableType(self):
            return self.getTypedRuleContext(qutesParser.VariableTypeContext,0)

        def variableName(self):
            return self.getTypedRuleContext(qutesParser.VariableNameContext,0)

        def ASSIGN(self):
            return self.getToken(qutesParser.ASSIGN, 0)
        def END_OF_STATEMENT(self):
            return self.getToken(qutesParser.END_OF_STATEMENT, 0)
        def expr(self):
            return self.getTypedRuleContext(qutesParser.ExprContext,0)

        def parenExpr(self):
            return self.getTypedRuleContext(qutesParser.ParenExprContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDeclarationStatement" ):
                listener.enterDeclarationStatement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDeclarationStatement" ):
                listener.exitDeclarationStatement(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitDeclarationStatement" ):
                return visitor.visitDeclarationStatement(self)
            else:
                return visitor.visitChildren(self)



    def statement(self):

        localctx = qutesParser.StatementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_statement)
        self._la = 0 # Token type
        try:
            self.state = 79
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,4,self._ctx)
            if la_ == 1:
                localctx = qutesParser.IfStatementContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 31
                self.match(qutesParser.IF_STATEMENT)
                self.state = 32
                self.parenExpr()
                self.state = 33
                self.statement()
                pass

            elif la_ == 2:
                localctx = qutesParser.IfElseStatementContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 35
                self.match(qutesParser.IF_STATEMENT)
                self.state = 36
                self.parenExpr()
                self.state = 37
                self.statement()
                self.state = 38
                self.match(qutesParser.ELSE_STATEMENT)
                self.state = 39
                self.statement()
                pass

            elif la_ == 3:
                localctx = qutesParser.WhileStatementContext(self, localctx)
                self.enterOuterAlt(localctx, 3)
                self.state = 41
                self.match(qutesParser.WHILE_STATEMENT)
                self.state = 42
                self.parenExpr()
                self.state = 43
                self.statement()
                pass

            elif la_ == 4:
                localctx = qutesParser.DoWhileStatementContext(self, localctx)
                self.enterOuterAlt(localctx, 4)
                self.state = 45
                self.match(qutesParser.DO_STATEMENT)
                self.state = 46
                self.statement()
                self.state = 47
                self.match(qutesParser.WHILE_STATEMENT)
                self.state = 48
                self.parenExpr()
                pass

            elif la_ == 5:
                localctx = qutesParser.BlockStatementContext(self, localctx)
                self.enterOuterAlt(localctx, 5)
                self.state = 50
                self.match(qutesParser.BLOCK_STATEMENT_START)
                self.state = 54
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while (((_la) & ~0x3f) == 0 and ((1 << _la) & 112885874) != 0):
                    self.state = 51
                    self.statement()
                    self.state = 56
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 57
                self.match(qutesParser.BLOCK_STATEMENT_END)
                pass

            elif la_ == 6:
                localctx = qutesParser.DeclarationStatementContext(self, localctx)
                self.enterOuterAlt(localctx, 6)
                self.state = 58
                self.variableType()
                self.state = 59
                self.variableName()
                self.state = 60
                self.match(qutesParser.ASSIGN)
                self.state = 63
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input,2,self._ctx)
                if la_ == 1:
                    self.state = 61
                    self.expr()
                    pass

                elif la_ == 2:
                    self.state = 62
                    self.parenExpr()
                    pass


                self.state = 65
                self.match(qutesParser.END_OF_STATEMENT)
                pass

            elif la_ == 7:
                localctx = qutesParser.AssignmentStatementContext(self, localctx)
                self.enterOuterAlt(localctx, 7)
                self.state = 67
                self.qualifiedName()
                self.state = 68
                self.match(qutesParser.ASSIGN)
                self.state = 71
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input,3,self._ctx)
                if la_ == 1:
                    self.state = 69
                    self.expr()
                    pass

                elif la_ == 2:
                    self.state = 70
                    self.parenExpr()
                    pass


                self.state = 73
                self.match(qutesParser.END_OF_STATEMENT)
                pass

            elif la_ == 8:
                localctx = qutesParser.ExpressionStatementContext(self, localctx)
                self.enterOuterAlt(localctx, 8)
                self.state = 75
                self.expr()
                self.state = 76
                self.match(qutesParser.END_OF_STATEMENT)
                pass

            elif la_ == 9:
                localctx = qutesParser.EmptyStatementContext(self, localctx)
                self.enterOuterAlt(localctx, 9)
                self.state = 78
                self.match(qutesParser.END_OF_STATEMENT)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ParenExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def expr(self):
            return self.getTypedRuleContext(qutesParser.ExprContext,0)


        def getRuleIndex(self):
            return qutesParser.RULE_parenExpr

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterParenExpr" ):
                listener.enterParenExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitParenExpr" ):
                listener.exitParenExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitParenExpr" ):
                return visitor.visitParenExpr(self)
            else:
                return visitor.visitChildren(self)




    def parenExpr(self):

        localctx = qutesParser.ParenExprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_parenExpr)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 81
            self.match(qutesParser.T__0)
            self.state = 82
            self.expr()
            self.state = 83
            self.match(qutesParser.T__1)
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
            return self.getTypedRuleContext(qutesParser.TermContext,0)


        def test(self):
            return self.getTypedRuleContext(qutesParser.TestContext,0)


        def parenExpr(self):
            return self.getTypedRuleContext(qutesParser.ParenExprContext,0)


        def getRuleIndex(self):
            return qutesParser.RULE_expr

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

        localctx = qutesParser.ExprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_expr)
        try:
            self.state = 88
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,5,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 85
                self.term(0)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 86
                self.test()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 87
                self.parenExpr()
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
                return self.getTypedRuleContexts(qutesParser.TermContext)
            else:
                return self.getTypedRuleContext(qutesParser.TermContext,i)


        def GREATER(self):
            return self.getToken(qutesParser.GREATER, 0)

        def LOWER(self):
            return self.getToken(qutesParser.LOWER, 0)

        def EQUAL(self):
            return self.getToken(qutesParser.EQUAL, 0)

        def GREATEREQUAL(self):
            return self.getToken(qutesParser.GREATEREQUAL, 0)

        def LOWEREQUAL(self):
            return self.getToken(qutesParser.LOWEREQUAL, 0)

        def getRuleIndex(self):
            return qutesParser.RULE_test

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

        localctx = qutesParser.TestContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_test)
        self._la = 0 # Token type
        try:
            self.state = 95
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,6,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 90
                self.term(0)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 91
                self.term(0)
                self.state = 92
                localctx.op = self._input.LT(1)
                _la = self._input.LA(1)
                if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 15872) != 0)):
                    localctx.op = self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 93
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
            return self.getTypedRuleContext(qutesParser.StringContext,0)


        def integer(self):
            return self.getTypedRuleContext(qutesParser.IntegerContext,0)


        def qualifiedName(self):
            return self.getTypedRuleContext(qutesParser.QualifiedNameContext,0)


        def term(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(qutesParser.TermContext)
            else:
                return self.getTypedRuleContext(qutesParser.TermContext,i)


        def ADD(self):
            return self.getToken(qutesParser.ADD, 0)

        def SUB(self):
            return self.getToken(qutesParser.SUB, 0)

        def getRuleIndex(self):
            return qutesParser.RULE_term

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
        localctx = qutesParser.TermContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 12
        self.enterRecursionRule(localctx, 12, self.RULE_term, _p)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 101
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [23]:
                self.state = 98
                self.string()
                pass
            elif token in [25]:
                self.state = 99
                self.integer()
                pass
            elif token in [26]:
                self.state = 100
                self.qualifiedName()
                pass
            else:
                raise NoViableAltException(self)

            self._ctx.stop = self._input.LT(-1)
            self.state = 108
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,8,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    localctx = qutesParser.TermContext(self, _parentctx, _parentState)
                    self.pushNewRecursionContext(localctx, _startState, self.RULE_term)
                    self.state = 103
                    if not self.precpred(self._ctx, 3):
                        from antlr4.error.Errors import FailedPredicateException
                        raise FailedPredicateException(self, "self.precpred(self._ctx, 3)")
                    self.state = 104
                    localctx.op = self._input.LT(1)
                    _la = self._input.LA(1)
                    if not(_la==7 or _la==8):
                        localctx.op = self._errHandler.recoverInline(self)
                    else:
                        self._errHandler.reportMatch(self)
                        self.consume()
                    self.state = 105
                    self.term(4) 
                self.state = 110
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,8,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.unrollRecursionContexts(_parentctx)
        return localctx


    class VariableTypeContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def type_(self):
            return self.getTypedRuleContext(qutesParser.TypeContext,0)


        def qualifiedName(self):
            return self.getTypedRuleContext(qutesParser.QualifiedNameContext,0)


        def getRuleIndex(self):
            return qutesParser.RULE_variableType

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterVariableType" ):
                listener.enterVariableType(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitVariableType" ):
                listener.exitVariableType(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitVariableType" ):
                return visitor.visitVariableType(self)
            else:
                return visitor.visitChildren(self)




    def variableType(self):

        localctx = qutesParser.VariableTypeContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_variableType)
        try:
            self.state = 113
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [4, 5, 6]:
                self.enterOuterAlt(localctx, 1)
                self.state = 111
                self.type_()
                pass
            elif token in [26]:
                self.enterOuterAlt(localctx, 2)
                self.state = 112
                self.qualifiedName()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class QualifiedNameContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def STRING(self, i:int=None):
            if i is None:
                return self.getTokens(qutesParser.STRING)
            else:
                return self.getToken(qutesParser.STRING, i)

        def getRuleIndex(self):
            return qutesParser.RULE_qualifiedName

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterQualifiedName" ):
                listener.enterQualifiedName(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitQualifiedName" ):
                listener.exitQualifiedName(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitQualifiedName" ):
                return visitor.visitQualifiedName(self)
            else:
                return visitor.visitChildren(self)




    def qualifiedName(self):

        localctx = qutesParser.QualifiedNameContext(self, self._ctx, self.state)
        self.enterRule(localctx, 16, self.RULE_qualifiedName)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 115
            self.match(qutesParser.STRING)
            self.state = 120
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,10,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 116
                    self.match(qutesParser.T__2)
                    self.state = 117
                    self.match(qutesParser.STRING) 
                self.state = 122
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,10,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class VariableNameContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def STRING(self):
            return self.getToken(qutesParser.STRING, 0)

        def getRuleIndex(self):
            return qutesParser.RULE_variableName

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

        localctx = qutesParser.VariableNameContext(self, self._ctx, self.state)
        self.enterRule(localctx, 18, self.RULE_variableName)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 123
            self.match(qutesParser.STRING)
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
                return self.getTokens(qutesParser.STRING_ENCLOSURE)
            else:
                return self.getToken(qutesParser.STRING_ENCLOSURE, i)

        def STRING(self):
            return self.getToken(qutesParser.STRING, 0)

        def getRuleIndex(self):
            return qutesParser.RULE_string

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

        localctx = qutesParser.StringContext(self, self._ctx, self.state)
        self.enterRule(localctx, 20, self.RULE_string)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 125
            self.match(qutesParser.STRING_ENCLOSURE)
            self.state = 126
            self.match(qutesParser.STRING)
            self.state = 127
            self.match(qutesParser.STRING_ENCLOSURE)
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
            return self.getToken(qutesParser.INT, 0)

        def getRuleIndex(self):
            return qutesParser.RULE_integer

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

        localctx = qutesParser.IntegerContext(self, self._ctx, self.state)
        self.enterRule(localctx, 22, self.RULE_integer)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 129
            self.match(qutesParser.INT)
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
        self._predicates[6] = self.term_sempred
        pred = self._predicates.get(ruleIndex, None)
        if pred is None:
            raise Exception("No predicate with index:" + str(ruleIndex))
        else:
            return pred(localctx, predIndex)

    def term_sempred(self, localctx:TermContext, predIndex:int):
            if predIndex == 0:
                return self.precpred(self._ctx, 3)
         




