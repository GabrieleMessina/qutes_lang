# Generated from /workspaces/qutes_lang/specification/grammar/qutes_parser.g4 by ANTLR 4.13.1
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
        4,1,46,153,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,
        6,2,7,7,7,2,8,7,8,2,9,7,9,2,10,7,10,2,11,7,11,2,12,7,12,2,13,7,13,
        2,14,7,14,2,15,7,15,1,0,5,0,34,8,0,10,0,12,0,37,9,0,1,0,1,0,1,1,
        1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,
        1,1,1,1,1,1,1,1,5,1,62,8,1,10,1,12,1,65,9,1,1,1,1,1,1,1,1,1,1,1,
        3,1,72,8,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,3,1,85,8,
        1,1,2,1,2,1,2,3,2,90,8,2,1,3,1,3,1,3,1,3,1,4,1,4,1,4,1,4,1,4,3,4,
        101,8,4,1,5,1,5,1,5,1,5,1,5,1,5,1,5,1,5,1,5,1,5,3,5,113,8,5,3,5,
        115,8,5,1,5,1,5,1,5,5,5,120,8,5,10,5,12,5,123,9,5,1,6,1,6,1,7,1,
        7,3,7,129,8,7,1,8,1,8,1,8,5,8,134,8,8,10,8,12,8,137,9,8,1,9,1,9,
        1,10,1,10,1,11,1,11,1,12,1,12,1,13,1,13,1,14,1,14,1,15,1,15,1,15,
        0,1,10,16,0,2,4,6,8,10,12,14,16,18,20,22,24,26,28,30,0,5,1,0,15,
        19,1,0,7,14,1,0,7,8,1,0,1,6,2,0,37,37,39,40,160,0,35,1,0,0,0,2,84,
        1,0,0,0,4,89,1,0,0,0,6,91,1,0,0,0,8,100,1,0,0,0,10,114,1,0,0,0,12,
        124,1,0,0,0,14,128,1,0,0,0,16,130,1,0,0,0,18,138,1,0,0,0,20,140,
        1,0,0,0,22,142,1,0,0,0,24,144,1,0,0,0,26,146,1,0,0,0,28,148,1,0,
        0,0,30,150,1,0,0,0,32,34,3,2,1,0,33,32,1,0,0,0,34,37,1,0,0,0,35,
        33,1,0,0,0,35,36,1,0,0,0,36,38,1,0,0,0,37,35,1,0,0,0,38,39,5,0,0,
        1,39,1,1,0,0,0,40,41,5,23,0,0,41,42,3,4,2,0,42,43,3,2,1,0,43,85,
        1,0,0,0,44,45,5,23,0,0,45,46,3,4,2,0,46,47,3,2,1,0,47,48,5,24,0,
        0,48,49,3,2,1,0,49,85,1,0,0,0,50,51,5,25,0,0,51,52,3,4,2,0,52,53,
        3,2,1,0,53,85,1,0,0,0,54,55,5,26,0,0,55,56,3,2,1,0,56,57,5,25,0,
        0,57,58,3,4,2,0,58,85,1,0,0,0,59,63,5,27,0,0,60,62,3,2,1,0,61,60,
        1,0,0,0,62,65,1,0,0,0,63,61,1,0,0,0,63,64,1,0,0,0,64,66,1,0,0,0,
        65,63,1,0,0,0,66,85,5,28,0,0,67,68,3,14,7,0,68,71,3,18,9,0,69,70,
        5,20,0,0,70,72,3,4,2,0,71,69,1,0,0,0,71,72,1,0,0,0,72,73,1,0,0,0,
        73,74,5,21,0,0,74,85,1,0,0,0,75,76,3,16,8,0,76,77,5,20,0,0,77,78,
        3,4,2,0,78,79,5,21,0,0,79,85,1,0,0,0,80,81,3,4,2,0,81,82,5,21,0,
        0,82,85,1,0,0,0,83,85,5,21,0,0,84,40,1,0,0,0,84,44,1,0,0,0,84,50,
        1,0,0,0,84,54,1,0,0,0,84,59,1,0,0,0,84,67,1,0,0,0,84,75,1,0,0,0,
        84,80,1,0,0,0,84,83,1,0,0,0,85,3,1,0,0,0,86,90,3,10,5,0,87,90,3,
        8,4,0,88,90,3,6,3,0,89,86,1,0,0,0,89,87,1,0,0,0,89,88,1,0,0,0,90,
        5,1,0,0,0,91,92,5,29,0,0,92,93,3,4,2,0,93,94,5,30,0,0,94,7,1,0,0,
        0,95,101,3,10,5,0,96,97,3,10,5,0,97,98,7,0,0,0,98,99,3,10,5,0,99,
        101,1,0,0,0,100,95,1,0,0,0,100,96,1,0,0,0,101,9,1,0,0,0,102,103,
        6,5,-1,0,103,104,7,1,0,0,104,115,3,10,5,2,105,113,3,30,15,0,106,
        113,3,28,14,0,107,113,3,26,13,0,108,113,3,22,11,0,109,113,3,24,12,
        0,110,113,3,16,8,0,111,113,3,20,10,0,112,105,1,0,0,0,112,106,1,0,
        0,0,112,107,1,0,0,0,112,108,1,0,0,0,112,109,1,0,0,0,112,110,1,0,
        0,0,112,111,1,0,0,0,113,115,1,0,0,0,114,102,1,0,0,0,114,112,1,0,
        0,0,115,121,1,0,0,0,116,117,10,3,0,0,117,118,7,2,0,0,118,120,3,10,
        5,4,119,116,1,0,0,0,120,123,1,0,0,0,121,119,1,0,0,0,121,122,1,0,
        0,0,122,11,1,0,0,0,123,121,1,0,0,0,124,125,7,3,0,0,125,13,1,0,0,
        0,126,129,3,12,6,0,127,129,3,16,8,0,128,126,1,0,0,0,128,127,1,0,
        0,0,129,15,1,0,0,0,130,135,5,43,0,0,131,132,5,33,0,0,132,134,5,43,
        0,0,133,131,1,0,0,0,134,137,1,0,0,0,135,133,1,0,0,0,135,136,1,0,
        0,0,136,17,1,0,0,0,137,135,1,0,0,0,138,139,5,43,0,0,139,19,1,0,0,
        0,140,141,5,44,0,0,141,21,1,0,0,0,142,143,5,41,0,0,143,23,1,0,0,
        0,144,145,5,42,0,0,145,25,1,0,0,0,146,147,5,38,0,0,147,27,1,0,0,
        0,148,149,7,4,0,0,149,29,1,0,0,0,150,151,5,36,0,0,151,31,1,0,0,0,
        11,35,63,71,84,89,100,112,114,121,128,135
    ]

class qutes_parser ( Parser ):

    grammarFileName = "qutes_parser.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'int'", "'bool'", "'string'", "'qubit'", 
                     "'quint'", "'float'", "'+'", "'-'", "'not'", "'pauliy'", 
                     "'pauliz'", "'hadamard'", "'measure'", "'print'", "'=='", 
                     "'>'", "'>='", "'<'", "'<='", "'='", "';'", "'var'", 
                     "'if'", "'else'", "'while'", "'do'", "'{'", "'}'", 
                     "'('", "')'", "'['", "']'", "'.'", "'\"'", "','" ]

    symbolicNames = [ "<INVALID>", "INT_TYPE", "BOOL_TYPE", "STRING_TYPE", 
                      "QUBIT_TYPE", "QUINT_TYPE", "FLOAT_TYPE", "ADD", "SUB", 
                      "NOT", "PAULIY", "PAULIZ", "HADAMARD", "MEASURE", 
                      "PRINT", "EQUAL", "GREATER", "GREATEREQUAL", "LOWER", 
                      "LOWEREQUAL", "ASSIGN", "END_OF_STATEMENT", "VAR_STATEMENT", 
                      "IF_STATEMENT", "ELSE_STATEMENT", "WHILE_STATEMENT", 
                      "DO_STATEMENT", "CURLY_PARENTHESIS_OPEN", "CURLY_PARENTHESIS_CLOSE", 
                      "ROUND_PARENTHESIS_OPEN", "ROUND_PARENTHESIS_CLOSE", 
                      "SQUARE_PARENTHESIS_OPEN", "SQUARE_PARENTHESIS_CLOSE", 
                      "DOT", "STRING_ENCLOSURE", "COMMA", "BOOL_LITERAL", 
                      "INT_LITERAL", "FLOAT_LITERAL", "HEX_LITERAL", "BIN_LITERAL", 
                      "QUBIT_LITERAL", "QUINT_LITERAL", "SYMBOL_LITERAL", 
                      "STRING_LITERAL", "WS", "NEWLINE" ]

    RULE_program = 0
    RULE_statement = 1
    RULE_expr = 2
    RULE_parenExpr = 3
    RULE_test = 4
    RULE_term = 5
    RULE_type = 6
    RULE_variableType = 7
    RULE_qualifiedName = 8
    RULE_variableName = 9
    RULE_string = 10
    RULE_qubit = 11
    RULE_quint = 12
    RULE_float = 13
    RULE_integer = 14
    RULE_boolean = 15

    ruleNames =  [ "program", "statement", "expr", "parenExpr", "test", 
                   "term", "type", "variableType", "qualifiedName", "variableName", 
                   "string", "qubit", "quint", "float", "integer", "boolean" ]

    EOF = Token.EOF
    INT_TYPE=1
    BOOL_TYPE=2
    STRING_TYPE=3
    QUBIT_TYPE=4
    QUINT_TYPE=5
    FLOAT_TYPE=6
    ADD=7
    SUB=8
    NOT=9
    PAULIY=10
    PAULIZ=11
    HADAMARD=12
    MEASURE=13
    PRINT=14
    EQUAL=15
    GREATER=16
    GREATEREQUAL=17
    LOWER=18
    LOWEREQUAL=19
    ASSIGN=20
    END_OF_STATEMENT=21
    VAR_STATEMENT=22
    IF_STATEMENT=23
    ELSE_STATEMENT=24
    WHILE_STATEMENT=25
    DO_STATEMENT=26
    CURLY_PARENTHESIS_OPEN=27
    CURLY_PARENTHESIS_CLOSE=28
    ROUND_PARENTHESIS_OPEN=29
    ROUND_PARENTHESIS_CLOSE=30
    SQUARE_PARENTHESIS_OPEN=31
    SQUARE_PARENTHESIS_CLOSE=32
    DOT=33
    STRING_ENCLOSURE=34
    COMMA=35
    BOOL_LITERAL=36
    INT_LITERAL=37
    FLOAT_LITERAL=38
    HEX_LITERAL=39
    BIN_LITERAL=40
    QUBIT_LITERAL=41
    QUINT_LITERAL=42
    SYMBOL_LITERAL=43
    STRING_LITERAL=44
    WS=45
    NEWLINE=46

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

        def EOF(self):
            return self.getToken(qutes_parser.EOF, 0)

        def statement(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(qutes_parser.StatementContext)
            else:
                return self.getTypedRuleContext(qutes_parser.StatementContext,i)


        def getRuleIndex(self):
            return qutes_parser.RULE_program

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

        localctx = qutes_parser.ProgramContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_program)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 35
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 35116434882558) != 0):
                self.state = 32
                self.statement()
                self.state = 37
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 38
            self.match(qutes_parser.EOF)
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
            return qutes_parser.RULE_statement

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class IfStatementContext(StatementContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a qutes_parser.StatementContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def IF_STATEMENT(self):
            return self.getToken(qutes_parser.IF_STATEMENT, 0)
        def expr(self):
            return self.getTypedRuleContext(qutes_parser.ExprContext,0)

        def statement(self):
            return self.getTypedRuleContext(qutes_parser.StatementContext,0)


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

        def __init__(self, parser, ctx:ParserRuleContext): # actually a qutes_parser.StatementContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def qualifiedName(self):
            return self.getTypedRuleContext(qutes_parser.QualifiedNameContext,0)

        def ASSIGN(self):
            return self.getToken(qutes_parser.ASSIGN, 0)
        def expr(self):
            return self.getTypedRuleContext(qutes_parser.ExprContext,0)

        def END_OF_STATEMENT(self):
            return self.getToken(qutes_parser.END_OF_STATEMENT, 0)

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

        def __init__(self, parser, ctx:ParserRuleContext): # actually a qutes_parser.StatementContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self):
            return self.getTypedRuleContext(qutes_parser.ExprContext,0)

        def END_OF_STATEMENT(self):
            return self.getToken(qutes_parser.END_OF_STATEMENT, 0)

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

        def __init__(self, parser, ctx:ParserRuleContext): # actually a qutes_parser.StatementContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def IF_STATEMENT(self):
            return self.getToken(qutes_parser.IF_STATEMENT, 0)
        def expr(self):
            return self.getTypedRuleContext(qutes_parser.ExprContext,0)

        def statement(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(qutes_parser.StatementContext)
            else:
                return self.getTypedRuleContext(qutes_parser.StatementContext,i)

        def ELSE_STATEMENT(self):
            return self.getToken(qutes_parser.ELSE_STATEMENT, 0)

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

        def __init__(self, parser, ctx:ParserRuleContext): # actually a qutes_parser.StatementContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def END_OF_STATEMENT(self):
            return self.getToken(qutes_parser.END_OF_STATEMENT, 0)

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

        def __init__(self, parser, ctx:ParserRuleContext): # actually a qutes_parser.StatementContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def CURLY_PARENTHESIS_OPEN(self):
            return self.getToken(qutes_parser.CURLY_PARENTHESIS_OPEN, 0)
        def CURLY_PARENTHESIS_CLOSE(self):
            return self.getToken(qutes_parser.CURLY_PARENTHESIS_CLOSE, 0)
        def statement(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(qutes_parser.StatementContext)
            else:
                return self.getTypedRuleContext(qutes_parser.StatementContext,i)


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

        def __init__(self, parser, ctx:ParserRuleContext): # actually a qutes_parser.StatementContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def WHILE_STATEMENT(self):
            return self.getToken(qutes_parser.WHILE_STATEMENT, 0)
        def expr(self):
            return self.getTypedRuleContext(qutes_parser.ExprContext,0)

        def statement(self):
            return self.getTypedRuleContext(qutes_parser.StatementContext,0)


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

        def __init__(self, parser, ctx:ParserRuleContext): # actually a qutes_parser.StatementContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def DO_STATEMENT(self):
            return self.getToken(qutes_parser.DO_STATEMENT, 0)
        def statement(self):
            return self.getTypedRuleContext(qutes_parser.StatementContext,0)

        def WHILE_STATEMENT(self):
            return self.getToken(qutes_parser.WHILE_STATEMENT, 0)
        def expr(self):
            return self.getTypedRuleContext(qutes_parser.ExprContext,0)


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

        def __init__(self, parser, ctx:ParserRuleContext): # actually a qutes_parser.StatementContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def variableType(self):
            return self.getTypedRuleContext(qutes_parser.VariableTypeContext,0)

        def variableName(self):
            return self.getTypedRuleContext(qutes_parser.VariableNameContext,0)

        def END_OF_STATEMENT(self):
            return self.getToken(qutes_parser.END_OF_STATEMENT, 0)
        def ASSIGN(self):
            return self.getToken(qutes_parser.ASSIGN, 0)
        def expr(self):
            return self.getTypedRuleContext(qutes_parser.ExprContext,0)


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

        localctx = qutes_parser.StatementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_statement)
        self._la = 0 # Token type
        try:
            self.state = 84
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,3,self._ctx)
            if la_ == 1:
                localctx = qutes_parser.IfStatementContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 40
                self.match(qutes_parser.IF_STATEMENT)
                self.state = 41
                self.expr()
                self.state = 42
                self.statement()
                pass

            elif la_ == 2:
                localctx = qutes_parser.IfElseStatementContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 44
                self.match(qutes_parser.IF_STATEMENT)
                self.state = 45
                self.expr()
                self.state = 46
                self.statement()
                self.state = 47
                self.match(qutes_parser.ELSE_STATEMENT)
                self.state = 48
                self.statement()
                pass

            elif la_ == 3:
                localctx = qutes_parser.WhileStatementContext(self, localctx)
                self.enterOuterAlt(localctx, 3)
                self.state = 50
                self.match(qutes_parser.WHILE_STATEMENT)
                self.state = 51
                self.expr()
                self.state = 52
                self.statement()
                pass

            elif la_ == 4:
                localctx = qutes_parser.DoWhileStatementContext(self, localctx)
                self.enterOuterAlt(localctx, 4)
                self.state = 54
                self.match(qutes_parser.DO_STATEMENT)
                self.state = 55
                self.statement()
                self.state = 56
                self.match(qutes_parser.WHILE_STATEMENT)
                self.state = 57
                self.expr()
                pass

            elif la_ == 5:
                localctx = qutes_parser.BlockStatementContext(self, localctx)
                self.enterOuterAlt(localctx, 5)
                self.state = 59
                self.match(qutes_parser.CURLY_PARENTHESIS_OPEN)
                self.state = 63
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while (((_la) & ~0x3f) == 0 and ((1 << _la) & 35116434882558) != 0):
                    self.state = 60
                    self.statement()
                    self.state = 65
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 66
                self.match(qutes_parser.CURLY_PARENTHESIS_CLOSE)
                pass

            elif la_ == 6:
                localctx = qutes_parser.DeclarationStatementContext(self, localctx)
                self.enterOuterAlt(localctx, 6)
                self.state = 67
                self.variableType()
                self.state = 68
                self.variableName()
                self.state = 71
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==20:
                    self.state = 69
                    self.match(qutes_parser.ASSIGN)
                    self.state = 70
                    self.expr()


                self.state = 73
                self.match(qutes_parser.END_OF_STATEMENT)
                pass

            elif la_ == 7:
                localctx = qutes_parser.AssignmentStatementContext(self, localctx)
                self.enterOuterAlt(localctx, 7)
                self.state = 75
                self.qualifiedName()
                self.state = 76
                self.match(qutes_parser.ASSIGN)
                self.state = 77
                self.expr()
                self.state = 78
                self.match(qutes_parser.END_OF_STATEMENT)
                pass

            elif la_ == 8:
                localctx = qutes_parser.ExpressionStatementContext(self, localctx)
                self.enterOuterAlt(localctx, 8)
                self.state = 80
                self.expr()
                self.state = 81
                self.match(qutes_parser.END_OF_STATEMENT)
                pass

            elif la_ == 9:
                localctx = qutes_parser.EmptyStatementContext(self, localctx)
                self.enterOuterAlt(localctx, 9)
                self.state = 83
                self.match(qutes_parser.END_OF_STATEMENT)
                pass


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
            return self.getTypedRuleContext(qutes_parser.TermContext,0)


        def test(self):
            return self.getTypedRuleContext(qutes_parser.TestContext,0)


        def parenExpr(self):
            return self.getTypedRuleContext(qutes_parser.ParenExprContext,0)


        def getRuleIndex(self):
            return qutes_parser.RULE_expr

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

        localctx = qutes_parser.ExprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_expr)
        try:
            self.state = 89
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,4,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 86
                self.term(0)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 87
                self.test()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 88
                self.parenExpr()
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

        def ROUND_PARENTHESIS_OPEN(self):
            return self.getToken(qutes_parser.ROUND_PARENTHESIS_OPEN, 0)

        def expr(self):
            return self.getTypedRuleContext(qutes_parser.ExprContext,0)


        def ROUND_PARENTHESIS_CLOSE(self):
            return self.getToken(qutes_parser.ROUND_PARENTHESIS_CLOSE, 0)

        def getRuleIndex(self):
            return qutes_parser.RULE_parenExpr

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

        localctx = qutes_parser.ParenExprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_parenExpr)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 91
            self.match(qutes_parser.ROUND_PARENTHESIS_OPEN)
            self.state = 92
            self.expr()
            self.state = 93
            self.match(qutes_parser.ROUND_PARENTHESIS_CLOSE)
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
                return self.getTypedRuleContexts(qutes_parser.TermContext)
            else:
                return self.getTypedRuleContext(qutes_parser.TermContext,i)


        def GREATER(self):
            return self.getToken(qutes_parser.GREATER, 0)

        def LOWER(self):
            return self.getToken(qutes_parser.LOWER, 0)

        def EQUAL(self):
            return self.getToken(qutes_parser.EQUAL, 0)

        def GREATEREQUAL(self):
            return self.getToken(qutes_parser.GREATEREQUAL, 0)

        def LOWEREQUAL(self):
            return self.getToken(qutes_parser.LOWEREQUAL, 0)

        def getRuleIndex(self):
            return qutes_parser.RULE_test

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

        localctx = qutes_parser.TestContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_test)
        self._la = 0 # Token type
        try:
            self.state = 100
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,5,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 95
                self.term(0)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 96
                self.term(0)
                self.state = 97
                localctx.op = self._input.LT(1)
                _la = self._input.LA(1)
                if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 1015808) != 0)):
                    localctx.op = self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 98
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


        def getRuleIndex(self):
            return qutes_parser.RULE_term

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)


    class IdentityOperatorContext(TermContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a qutes_parser.TermContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def boolean(self):
            return self.getTypedRuleContext(qutes_parser.BooleanContext,0)

        def integer(self):
            return self.getTypedRuleContext(qutes_parser.IntegerContext,0)

        def float_(self):
            return self.getTypedRuleContext(qutes_parser.FloatContext,0)

        def qubit(self):
            return self.getTypedRuleContext(qutes_parser.QubitContext,0)

        def quint(self):
            return self.getTypedRuleContext(qutes_parser.QuintContext,0)

        def qualifiedName(self):
            return self.getTypedRuleContext(qutes_parser.QualifiedNameContext,0)

        def string(self):
            return self.getTypedRuleContext(qutes_parser.StringContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterIdentityOperator" ):
                listener.enterIdentityOperator(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitIdentityOperator" ):
                listener.exitIdentityOperator(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitIdentityOperator" ):
                return visitor.visitIdentityOperator(self)
            else:
                return visitor.visitChildren(self)


    class UnaryOperatorContext(TermContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a qutes_parser.TermContext
            super().__init__(parser)
            self.op = None # Token
            self.copyFrom(ctx)

        def term(self):
            return self.getTypedRuleContext(qutes_parser.TermContext,0)

        def PRINT(self):
            return self.getToken(qutes_parser.PRINT, 0)
        def NOT(self):
            return self.getToken(qutes_parser.NOT, 0)
        def PAULIY(self):
            return self.getToken(qutes_parser.PAULIY, 0)
        def PAULIZ(self):
            return self.getToken(qutes_parser.PAULIZ, 0)
        def HADAMARD(self):
            return self.getToken(qutes_parser.HADAMARD, 0)
        def MEASURE(self):
            return self.getToken(qutes_parser.MEASURE, 0)
        def ADD(self):
            return self.getToken(qutes_parser.ADD, 0)
        def SUB(self):
            return self.getToken(qutes_parser.SUB, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterUnaryOperator" ):
                listener.enterUnaryOperator(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitUnaryOperator" ):
                listener.exitUnaryOperator(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitUnaryOperator" ):
                return visitor.visitUnaryOperator(self)
            else:
                return visitor.visitChildren(self)


    class BinaryOperatorContext(TermContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a qutes_parser.TermContext
            super().__init__(parser)
            self.op = None # Token
            self.copyFrom(ctx)

        def term(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(qutes_parser.TermContext)
            else:
                return self.getTypedRuleContext(qutes_parser.TermContext,i)

        def ADD(self):
            return self.getToken(qutes_parser.ADD, 0)
        def SUB(self):
            return self.getToken(qutes_parser.SUB, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterBinaryOperator" ):
                listener.enterBinaryOperator(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitBinaryOperator" ):
                listener.exitBinaryOperator(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitBinaryOperator" ):
                return visitor.visitBinaryOperator(self)
            else:
                return visitor.visitChildren(self)



    def term(self, _p:int=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = qutes_parser.TermContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 10
        self.enterRecursionRule(localctx, 10, self.RULE_term, _p)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 114
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [7, 8, 9, 10, 11, 12, 13, 14]:
                localctx = qutes_parser.UnaryOperatorContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx

                self.state = 103
                localctx.op = self._input.LT(1)
                _la = self._input.LA(1)
                if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 32640) != 0)):
                    localctx.op = self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 104
                self.term(2)
                pass
            elif token in [36, 37, 38, 39, 40, 41, 42, 43, 44]:
                localctx = qutes_parser.IdentityOperatorContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 112
                self._errHandler.sync(self)
                token = self._input.LA(1)
                if token in [36]:
                    self.state = 105
                    self.boolean()
                    pass
                elif token in [37, 39, 40]:
                    self.state = 106
                    self.integer()
                    pass
                elif token in [38]:
                    self.state = 107
                    self.float_()
                    pass
                elif token in [41]:
                    self.state = 108
                    self.qubit()
                    pass
                elif token in [42]:
                    self.state = 109
                    self.quint()
                    pass
                elif token in [43]:
                    self.state = 110
                    self.qualifiedName()
                    pass
                elif token in [44]:
                    self.state = 111
                    self.string()
                    pass
                else:
                    raise NoViableAltException(self)

                pass
            else:
                raise NoViableAltException(self)

            self._ctx.stop = self._input.LT(-1)
            self.state = 121
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,8,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    localctx = qutes_parser.BinaryOperatorContext(self, qutes_parser.TermContext(self, _parentctx, _parentState))
                    self.pushNewRecursionContext(localctx, _startState, self.RULE_term)
                    self.state = 116
                    if not self.precpred(self._ctx, 3):
                        from antlr4.error.Errors import FailedPredicateException
                        raise FailedPredicateException(self, "self.precpred(self._ctx, 3)")
                    self.state = 117
                    localctx.op = self._input.LT(1)
                    _la = self._input.LA(1)
                    if not(_la==7 or _la==8):
                        localctx.op = self._errHandler.recoverInline(self)
                    else:
                        self._errHandler.reportMatch(self)
                        self.consume()
                    self.state = 118
                    self.term(4) 
                self.state = 123
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,8,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.unrollRecursionContexts(_parentctx)
        return localctx


    class TypeContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def INT_TYPE(self):
            return self.getToken(qutes_parser.INT_TYPE, 0)

        def BOOL_TYPE(self):
            return self.getToken(qutes_parser.BOOL_TYPE, 0)

        def FLOAT_TYPE(self):
            return self.getToken(qutes_parser.FLOAT_TYPE, 0)

        def STRING_TYPE(self):
            return self.getToken(qutes_parser.STRING_TYPE, 0)

        def QUBIT_TYPE(self):
            return self.getToken(qutes_parser.QUBIT_TYPE, 0)

        def QUINT_TYPE(self):
            return self.getToken(qutes_parser.QUINT_TYPE, 0)

        def getRuleIndex(self):
            return qutes_parser.RULE_type

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

        localctx = qutes_parser.TypeContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_type)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 124
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 126) != 0)):
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


    class VariableTypeContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def type_(self):
            return self.getTypedRuleContext(qutes_parser.TypeContext,0)


        def qualifiedName(self):
            return self.getTypedRuleContext(qutes_parser.QualifiedNameContext,0)


        def getRuleIndex(self):
            return qutes_parser.RULE_variableType

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

        localctx = qutes_parser.VariableTypeContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_variableType)
        try:
            self.state = 128
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [1, 2, 3, 4, 5, 6]:
                self.enterOuterAlt(localctx, 1)
                self.state = 126
                self.type_()
                pass
            elif token in [43]:
                self.enterOuterAlt(localctx, 2)
                self.state = 127
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

        def SYMBOL_LITERAL(self, i:int=None):
            if i is None:
                return self.getTokens(qutes_parser.SYMBOL_LITERAL)
            else:
                return self.getToken(qutes_parser.SYMBOL_LITERAL, i)

        def DOT(self, i:int=None):
            if i is None:
                return self.getTokens(qutes_parser.DOT)
            else:
                return self.getToken(qutes_parser.DOT, i)

        def getRuleIndex(self):
            return qutes_parser.RULE_qualifiedName

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

        localctx = qutes_parser.QualifiedNameContext(self, self._ctx, self.state)
        self.enterRule(localctx, 16, self.RULE_qualifiedName)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 130
            self.match(qutes_parser.SYMBOL_LITERAL)
            self.state = 135
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,10,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 131
                    self.match(qutes_parser.DOT)
                    self.state = 132
                    self.match(qutes_parser.SYMBOL_LITERAL) 
                self.state = 137
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

        def SYMBOL_LITERAL(self):
            return self.getToken(qutes_parser.SYMBOL_LITERAL, 0)

        def getRuleIndex(self):
            return qutes_parser.RULE_variableName

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

        localctx = qutes_parser.VariableNameContext(self, self._ctx, self.state)
        self.enterRule(localctx, 18, self.RULE_variableName)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 138
            self.match(qutes_parser.SYMBOL_LITERAL)
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

        def STRING_LITERAL(self):
            return self.getToken(qutes_parser.STRING_LITERAL, 0)

        def getRuleIndex(self):
            return qutes_parser.RULE_string

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

        localctx = qutes_parser.StringContext(self, self._ctx, self.state)
        self.enterRule(localctx, 20, self.RULE_string)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 140
            self.match(qutes_parser.STRING_LITERAL)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class QubitContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def QUBIT_LITERAL(self):
            return self.getToken(qutes_parser.QUBIT_LITERAL, 0)

        def getRuleIndex(self):
            return qutes_parser.RULE_qubit

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterQubit" ):
                listener.enterQubit(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitQubit" ):
                listener.exitQubit(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitQubit" ):
                return visitor.visitQubit(self)
            else:
                return visitor.visitChildren(self)




    def qubit(self):

        localctx = qutes_parser.QubitContext(self, self._ctx, self.state)
        self.enterRule(localctx, 22, self.RULE_qubit)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 142
            self.match(qutes_parser.QUBIT_LITERAL)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class QuintContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def QUINT_LITERAL(self):
            return self.getToken(qutes_parser.QUINT_LITERAL, 0)

        def getRuleIndex(self):
            return qutes_parser.RULE_quint

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterQuint" ):
                listener.enterQuint(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitQuint" ):
                listener.exitQuint(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitQuint" ):
                return visitor.visitQuint(self)
            else:
                return visitor.visitChildren(self)




    def quint(self):

        localctx = qutes_parser.QuintContext(self, self._ctx, self.state)
        self.enterRule(localctx, 24, self.RULE_quint)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 144
            self.match(qutes_parser.QUINT_LITERAL)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class FloatContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def FLOAT_LITERAL(self):
            return self.getToken(qutes_parser.FLOAT_LITERAL, 0)

        def getRuleIndex(self):
            return qutes_parser.RULE_float

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFloat" ):
                listener.enterFloat(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFloat" ):
                listener.exitFloat(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFloat" ):
                return visitor.visitFloat(self)
            else:
                return visitor.visitChildren(self)




    def float_(self):

        localctx = qutes_parser.FloatContext(self, self._ctx, self.state)
        self.enterRule(localctx, 26, self.RULE_float)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 146
            self.match(qutes_parser.FLOAT_LITERAL)
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

        def INT_LITERAL(self):
            return self.getToken(qutes_parser.INT_LITERAL, 0)

        def BIN_LITERAL(self):
            return self.getToken(qutes_parser.BIN_LITERAL, 0)

        def HEX_LITERAL(self):
            return self.getToken(qutes_parser.HEX_LITERAL, 0)

        def getRuleIndex(self):
            return qutes_parser.RULE_integer

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

        localctx = qutes_parser.IntegerContext(self, self._ctx, self.state)
        self.enterRule(localctx, 28, self.RULE_integer)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 148
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 1786706395136) != 0)):
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


    class BooleanContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def BOOL_LITERAL(self):
            return self.getToken(qutes_parser.BOOL_LITERAL, 0)

        def getRuleIndex(self):
            return qutes_parser.RULE_boolean

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterBoolean" ):
                listener.enterBoolean(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitBoolean" ):
                listener.exitBoolean(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitBoolean" ):
                return visitor.visitBoolean(self)
            else:
                return visitor.visitChildren(self)




    def boolean(self):

        localctx = qutes_parser.BooleanContext(self, self._ctx, self.state)
        self.enterRule(localctx, 30, self.RULE_boolean)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 150
            self.match(qutes_parser.BOOL_LITERAL)
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
         




