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
        4,1,46,203,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,
        6,2,7,7,7,2,8,7,8,2,9,7,9,2,10,7,10,2,11,7,11,2,12,7,12,2,13,7,13,
        2,14,7,14,2,15,7,15,2,16,7,16,2,17,7,17,2,18,7,18,2,19,7,19,2,20,
        7,20,2,21,7,21,1,0,5,0,46,8,0,10,0,12,0,49,9,0,1,0,1,0,1,1,1,1,1,
        1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,
        1,1,1,1,1,1,1,1,1,1,1,3,1,77,8,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,
        1,1,1,1,1,1,1,1,1,1,1,1,1,1,3,1,94,8,1,1,2,1,2,1,2,1,2,3,2,100,8,
        2,1,3,1,3,5,3,104,8,3,10,3,12,3,107,9,3,1,3,1,3,1,4,1,4,1,4,5,4,
        114,8,4,10,4,12,4,117,9,4,1,5,1,5,1,5,5,5,122,8,5,10,5,12,5,125,
        9,5,1,6,1,6,1,6,1,6,3,6,131,8,6,1,7,1,7,1,7,3,7,136,8,7,1,7,1,7,
        1,8,1,8,1,8,1,8,1,9,1,9,1,9,1,9,1,9,3,9,149,8,9,1,10,1,10,1,10,1,
        10,1,10,1,10,1,10,1,10,1,10,1,10,3,10,161,8,10,3,10,163,8,10,1,10,
        1,10,1,10,5,10,168,8,10,10,10,12,10,171,9,10,1,11,1,11,1,12,1,12,
        3,12,177,8,12,1,13,1,13,1,13,5,13,182,8,13,10,13,12,13,185,9,13,
        1,14,1,14,1,15,1,15,1,16,1,16,1,17,1,17,1,18,1,18,1,19,1,19,1,20,
        1,20,1,21,1,21,1,21,0,1,20,22,0,2,4,6,8,10,12,14,16,18,20,22,24,
        26,28,30,32,34,36,38,40,42,0,5,1,0,15,19,1,0,7,14,1,0,7,8,1,0,1,
        6,2,0,37,37,39,40,210,0,47,1,0,0,0,2,93,1,0,0,0,4,95,1,0,0,0,6,101,
        1,0,0,0,8,110,1,0,0,0,10,118,1,0,0,0,12,130,1,0,0,0,14,132,1,0,0,
        0,16,139,1,0,0,0,18,148,1,0,0,0,20,162,1,0,0,0,22,172,1,0,0,0,24,
        176,1,0,0,0,26,178,1,0,0,0,28,186,1,0,0,0,30,188,1,0,0,0,32,190,
        1,0,0,0,34,192,1,0,0,0,36,194,1,0,0,0,38,196,1,0,0,0,40,198,1,0,
        0,0,42,200,1,0,0,0,44,46,3,2,1,0,45,44,1,0,0,0,46,49,1,0,0,0,47,
        45,1,0,0,0,47,48,1,0,0,0,48,50,1,0,0,0,49,47,1,0,0,0,50,51,5,0,0,
        1,51,1,1,0,0,0,52,53,5,23,0,0,53,54,3,12,6,0,54,55,3,2,1,0,55,94,
        1,0,0,0,56,57,5,23,0,0,57,58,3,12,6,0,58,59,3,2,1,0,59,60,5,24,0,
        0,60,61,3,2,1,0,61,94,1,0,0,0,62,63,5,25,0,0,63,64,3,12,6,0,64,65,
        3,2,1,0,65,94,1,0,0,0,66,67,5,26,0,0,67,68,3,2,1,0,68,69,5,25,0,
        0,69,70,3,12,6,0,70,94,1,0,0,0,71,94,3,6,3,0,72,73,3,24,12,0,73,
        74,3,30,15,0,74,76,5,29,0,0,75,77,3,8,4,0,76,75,1,0,0,0,76,77,1,
        0,0,0,77,78,1,0,0,0,78,79,5,30,0,0,79,80,3,2,1,0,80,94,1,0,0,0,81,
        82,3,4,2,0,82,83,5,21,0,0,83,94,1,0,0,0,84,85,3,26,13,0,85,86,5,
        20,0,0,86,87,3,12,6,0,87,88,5,21,0,0,88,94,1,0,0,0,89,90,3,12,6,
        0,90,91,5,21,0,0,91,94,1,0,0,0,92,94,5,21,0,0,93,52,1,0,0,0,93,56,
        1,0,0,0,93,62,1,0,0,0,93,66,1,0,0,0,93,71,1,0,0,0,93,72,1,0,0,0,
        93,81,1,0,0,0,93,84,1,0,0,0,93,89,1,0,0,0,93,92,1,0,0,0,94,3,1,0,
        0,0,95,96,3,24,12,0,96,99,3,28,14,0,97,98,5,20,0,0,98,100,3,12,6,
        0,99,97,1,0,0,0,99,100,1,0,0,0,100,5,1,0,0,0,101,105,5,27,0,0,102,
        104,3,2,1,0,103,102,1,0,0,0,104,107,1,0,0,0,105,103,1,0,0,0,105,
        106,1,0,0,0,106,108,1,0,0,0,107,105,1,0,0,0,108,109,5,28,0,0,109,
        7,1,0,0,0,110,115,3,4,2,0,111,112,5,35,0,0,112,114,3,8,4,0,113,111,
        1,0,0,0,114,117,1,0,0,0,115,113,1,0,0,0,115,116,1,0,0,0,116,9,1,
        0,0,0,117,115,1,0,0,0,118,123,3,26,13,0,119,120,5,35,0,0,120,122,
        3,10,5,0,121,119,1,0,0,0,122,125,1,0,0,0,123,121,1,0,0,0,123,124,
        1,0,0,0,124,11,1,0,0,0,125,123,1,0,0,0,126,131,3,20,10,0,127,131,
        3,14,7,0,128,131,3,18,9,0,129,131,3,16,8,0,130,126,1,0,0,0,130,127,
        1,0,0,0,130,128,1,0,0,0,130,129,1,0,0,0,131,13,1,0,0,0,132,133,3,
        30,15,0,133,135,5,29,0,0,134,136,3,10,5,0,135,134,1,0,0,0,135,136,
        1,0,0,0,136,137,1,0,0,0,137,138,5,30,0,0,138,15,1,0,0,0,139,140,
        5,29,0,0,140,141,3,12,6,0,141,142,5,30,0,0,142,17,1,0,0,0,143,149,
        3,20,10,0,144,145,3,20,10,0,145,146,7,0,0,0,146,147,3,20,10,0,147,
        149,1,0,0,0,148,143,1,0,0,0,148,144,1,0,0,0,149,19,1,0,0,0,150,151,
        6,10,-1,0,151,152,7,1,0,0,152,163,3,20,10,2,153,161,3,42,21,0,154,
        161,3,40,20,0,155,161,3,38,19,0,156,161,3,34,17,0,157,161,3,36,18,
        0,158,161,3,26,13,0,159,161,3,32,16,0,160,153,1,0,0,0,160,154,1,
        0,0,0,160,155,1,0,0,0,160,156,1,0,0,0,160,157,1,0,0,0,160,158,1,
        0,0,0,160,159,1,0,0,0,161,163,1,0,0,0,162,150,1,0,0,0,162,160,1,
        0,0,0,163,169,1,0,0,0,164,165,10,3,0,0,165,166,7,2,0,0,166,168,3,
        20,10,4,167,164,1,0,0,0,168,171,1,0,0,0,169,167,1,0,0,0,169,170,
        1,0,0,0,170,21,1,0,0,0,171,169,1,0,0,0,172,173,7,3,0,0,173,23,1,
        0,0,0,174,177,3,22,11,0,175,177,3,26,13,0,176,174,1,0,0,0,176,175,
        1,0,0,0,177,25,1,0,0,0,178,183,5,43,0,0,179,180,5,33,0,0,180,182,
        5,43,0,0,181,179,1,0,0,0,182,185,1,0,0,0,183,181,1,0,0,0,183,184,
        1,0,0,0,184,27,1,0,0,0,185,183,1,0,0,0,186,187,5,43,0,0,187,29,1,
        0,0,0,188,189,5,43,0,0,189,31,1,0,0,0,190,191,5,44,0,0,191,33,1,
        0,0,0,192,193,5,41,0,0,193,35,1,0,0,0,194,195,5,42,0,0,195,37,1,
        0,0,0,196,197,5,38,0,0,197,39,1,0,0,0,198,199,7,4,0,0,199,41,1,0,
        0,0,200,201,5,36,0,0,201,43,1,0,0,0,15,47,76,93,99,105,115,123,130,
        135,148,160,162,169,176,183
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
    RULE_variableDeclaration = 2
    RULE_block = 3
    RULE_functionDeclarationParams = 4
    RULE_functionCallParams = 5
    RULE_expr = 6
    RULE_functionCall = 7
    RULE_parenExpr = 8
    RULE_test = 9
    RULE_term = 10
    RULE_type = 11
    RULE_variableType = 12
    RULE_qualifiedName = 13
    RULE_variableName = 14
    RULE_functionName = 15
    RULE_string = 16
    RULE_qubit = 17
    RULE_quint = 18
    RULE_float = 19
    RULE_integer = 20
    RULE_boolean = 21

    ruleNames =  [ "program", "statement", "variableDeclaration", "block", 
                   "functionDeclarationParams", "functionCallParams", "expr", 
                   "functionCall", "parenExpr", "test", "term", "type", 
                   "variableType", "qualifiedName", "variableName", "functionName", 
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
            self.state = 47
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 35116434882558) != 0):
                self.state = 44
                self.statement()
                self.state = 49
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 50
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


    class FunctionStatementContext(StatementContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a qutes_parser.StatementContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def variableType(self):
            return self.getTypedRuleContext(qutes_parser.VariableTypeContext,0)

        def functionName(self):
            return self.getTypedRuleContext(qutes_parser.FunctionNameContext,0)

        def ROUND_PARENTHESIS_OPEN(self):
            return self.getToken(qutes_parser.ROUND_PARENTHESIS_OPEN, 0)
        def ROUND_PARENTHESIS_CLOSE(self):
            return self.getToken(qutes_parser.ROUND_PARENTHESIS_CLOSE, 0)
        def statement(self):
            return self.getTypedRuleContext(qutes_parser.StatementContext,0)

        def functionDeclarationParams(self):
            return self.getTypedRuleContext(qutes_parser.FunctionDeclarationParamsContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFunctionStatement" ):
                listener.enterFunctionStatement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFunctionStatement" ):
                listener.exitFunctionStatement(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFunctionStatement" ):
                return visitor.visitFunctionStatement(self)
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

        def block(self):
            return self.getTypedRuleContext(qutes_parser.BlockContext,0)


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

        def variableDeclaration(self):
            return self.getTypedRuleContext(qutes_parser.VariableDeclarationContext,0)

        def END_OF_STATEMENT(self):
            return self.getToken(qutes_parser.END_OF_STATEMENT, 0)

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
            self.state = 93
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,2,self._ctx)
            if la_ == 1:
                localctx = qutes_parser.IfStatementContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 52
                self.match(qutes_parser.IF_STATEMENT)
                self.state = 53
                self.expr()
                self.state = 54
                self.statement()
                pass

            elif la_ == 2:
                localctx = qutes_parser.IfElseStatementContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 56
                self.match(qutes_parser.IF_STATEMENT)
                self.state = 57
                self.expr()
                self.state = 58
                self.statement()
                self.state = 59
                self.match(qutes_parser.ELSE_STATEMENT)
                self.state = 60
                self.statement()
                pass

            elif la_ == 3:
                localctx = qutes_parser.WhileStatementContext(self, localctx)
                self.enterOuterAlt(localctx, 3)
                self.state = 62
                self.match(qutes_parser.WHILE_STATEMENT)
                self.state = 63
                self.expr()
                self.state = 64
                self.statement()
                pass

            elif la_ == 4:
                localctx = qutes_parser.DoWhileStatementContext(self, localctx)
                self.enterOuterAlt(localctx, 4)
                self.state = 66
                self.match(qutes_parser.DO_STATEMENT)
                self.state = 67
                self.statement()
                self.state = 68
                self.match(qutes_parser.WHILE_STATEMENT)
                self.state = 69
                self.expr()
                pass

            elif la_ == 5:
                localctx = qutes_parser.BlockStatementContext(self, localctx)
                self.enterOuterAlt(localctx, 5)
                self.state = 71
                self.block()
                pass

            elif la_ == 6:
                localctx = qutes_parser.FunctionStatementContext(self, localctx)
                self.enterOuterAlt(localctx, 6)
                self.state = 72
                self.variableType()
                self.state = 73
                self.functionName()
                self.state = 74
                self.match(qutes_parser.ROUND_PARENTHESIS_OPEN)
                self.state = 76
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if (((_la) & ~0x3f) == 0 and ((1 << _la) & 8796093022334) != 0):
                    self.state = 75
                    self.functionDeclarationParams()


                self.state = 78
                self.match(qutes_parser.ROUND_PARENTHESIS_CLOSE)
                self.state = 79
                self.statement()
                pass

            elif la_ == 7:
                localctx = qutes_parser.DeclarationStatementContext(self, localctx)
                self.enterOuterAlt(localctx, 7)
                self.state = 81
                self.variableDeclaration()
                self.state = 82
                self.match(qutes_parser.END_OF_STATEMENT)
                pass

            elif la_ == 8:
                localctx = qutes_parser.AssignmentStatementContext(self, localctx)
                self.enterOuterAlt(localctx, 8)
                self.state = 84
                self.qualifiedName()
                self.state = 85
                self.match(qutes_parser.ASSIGN)
                self.state = 86
                self.expr()
                self.state = 87
                self.match(qutes_parser.END_OF_STATEMENT)
                pass

            elif la_ == 9:
                localctx = qutes_parser.ExpressionStatementContext(self, localctx)
                self.enterOuterAlt(localctx, 9)
                self.state = 89
                self.expr()
                self.state = 90
                self.match(qutes_parser.END_OF_STATEMENT)
                pass

            elif la_ == 10:
                localctx = qutes_parser.EmptyStatementContext(self, localctx)
                self.enterOuterAlt(localctx, 10)
                self.state = 92
                self.match(qutes_parser.END_OF_STATEMENT)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class VariableDeclarationContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def variableType(self):
            return self.getTypedRuleContext(qutes_parser.VariableTypeContext,0)


        def variableName(self):
            return self.getTypedRuleContext(qutes_parser.VariableNameContext,0)


        def ASSIGN(self):
            return self.getToken(qutes_parser.ASSIGN, 0)

        def expr(self):
            return self.getTypedRuleContext(qutes_parser.ExprContext,0)


        def getRuleIndex(self):
            return qutes_parser.RULE_variableDeclaration

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterVariableDeclaration" ):
                listener.enterVariableDeclaration(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitVariableDeclaration" ):
                listener.exitVariableDeclaration(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitVariableDeclaration" ):
                return visitor.visitVariableDeclaration(self)
            else:
                return visitor.visitChildren(self)




    def variableDeclaration(self):

        localctx = qutes_parser.VariableDeclarationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_variableDeclaration)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 95
            self.variableType()
            self.state = 96
            self.variableName()
            self.state = 99
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==20:
                self.state = 97
                self.match(qutes_parser.ASSIGN)
                self.state = 98
                self.expr()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class BlockContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def CURLY_PARENTHESIS_OPEN(self):
            return self.getToken(qutes_parser.CURLY_PARENTHESIS_OPEN, 0)

        def CURLY_PARENTHESIS_CLOSE(self):
            return self.getToken(qutes_parser.CURLY_PARENTHESIS_CLOSE, 0)

        def statement(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(qutes_parser.StatementContext)
            else:
                return self.getTypedRuleContext(qutes_parser.StatementContext,i)


        def getRuleIndex(self):
            return qutes_parser.RULE_block

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterBlock" ):
                listener.enterBlock(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitBlock" ):
                listener.exitBlock(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitBlock" ):
                return visitor.visitBlock(self)
            else:
                return visitor.visitChildren(self)




    def block(self):

        localctx = qutes_parser.BlockContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_block)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 101
            self.match(qutes_parser.CURLY_PARENTHESIS_OPEN)
            self.state = 105
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 35116434882558) != 0):
                self.state = 102
                self.statement()
                self.state = 107
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 108
            self.match(qutes_parser.CURLY_PARENTHESIS_CLOSE)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class FunctionDeclarationParamsContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def variableDeclaration(self):
            return self.getTypedRuleContext(qutes_parser.VariableDeclarationContext,0)


        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(qutes_parser.COMMA)
            else:
                return self.getToken(qutes_parser.COMMA, i)

        def functionDeclarationParams(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(qutes_parser.FunctionDeclarationParamsContext)
            else:
                return self.getTypedRuleContext(qutes_parser.FunctionDeclarationParamsContext,i)


        def getRuleIndex(self):
            return qutes_parser.RULE_functionDeclarationParams

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFunctionDeclarationParams" ):
                listener.enterFunctionDeclarationParams(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFunctionDeclarationParams" ):
                listener.exitFunctionDeclarationParams(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFunctionDeclarationParams" ):
                return visitor.visitFunctionDeclarationParams(self)
            else:
                return visitor.visitChildren(self)




    def functionDeclarationParams(self):

        localctx = qutes_parser.FunctionDeclarationParamsContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_functionDeclarationParams)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 110
            self.variableDeclaration()
            self.state = 115
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,5,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 111
                    self.match(qutes_parser.COMMA)
                    self.state = 112
                    self.functionDeclarationParams() 
                self.state = 117
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,5,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class FunctionCallParamsContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def qualifiedName(self):
            return self.getTypedRuleContext(qutes_parser.QualifiedNameContext,0)


        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(qutes_parser.COMMA)
            else:
                return self.getToken(qutes_parser.COMMA, i)

        def functionCallParams(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(qutes_parser.FunctionCallParamsContext)
            else:
                return self.getTypedRuleContext(qutes_parser.FunctionCallParamsContext,i)


        def getRuleIndex(self):
            return qutes_parser.RULE_functionCallParams

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFunctionCallParams" ):
                listener.enterFunctionCallParams(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFunctionCallParams" ):
                listener.exitFunctionCallParams(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFunctionCallParams" ):
                return visitor.visitFunctionCallParams(self)
            else:
                return visitor.visitChildren(self)




    def functionCallParams(self):

        localctx = qutes_parser.FunctionCallParamsContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_functionCallParams)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 118
            self.qualifiedName()
            self.state = 123
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,6,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 119
                    self.match(qutes_parser.COMMA)
                    self.state = 120
                    self.functionCallParams() 
                self.state = 125
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,6,self._ctx)

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


        def functionCall(self):
            return self.getTypedRuleContext(qutes_parser.FunctionCallContext,0)


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
        self.enterRule(localctx, 12, self.RULE_expr)
        try:
            self.state = 130
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,7,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 126
                self.term(0)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 127
                self.functionCall()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 128
                self.test()
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 129
                self.parenExpr()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class FunctionCallContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def functionName(self):
            return self.getTypedRuleContext(qutes_parser.FunctionNameContext,0)


        def ROUND_PARENTHESIS_OPEN(self):
            return self.getToken(qutes_parser.ROUND_PARENTHESIS_OPEN, 0)

        def ROUND_PARENTHESIS_CLOSE(self):
            return self.getToken(qutes_parser.ROUND_PARENTHESIS_CLOSE, 0)

        def functionCallParams(self):
            return self.getTypedRuleContext(qutes_parser.FunctionCallParamsContext,0)


        def getRuleIndex(self):
            return qutes_parser.RULE_functionCall

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFunctionCall" ):
                listener.enterFunctionCall(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFunctionCall" ):
                listener.exitFunctionCall(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFunctionCall" ):
                return visitor.visitFunctionCall(self)
            else:
                return visitor.visitChildren(self)




    def functionCall(self):

        localctx = qutes_parser.FunctionCallContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_functionCall)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 132
            self.functionName()
            self.state = 133
            self.match(qutes_parser.ROUND_PARENTHESIS_OPEN)
            self.state = 135
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==43:
                self.state = 134
                self.functionCallParams()


            self.state = 137
            self.match(qutes_parser.ROUND_PARENTHESIS_CLOSE)
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
        self.enterRule(localctx, 16, self.RULE_parenExpr)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 139
            self.match(qutes_parser.ROUND_PARENTHESIS_OPEN)
            self.state = 140
            self.expr()
            self.state = 141
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
        self.enterRule(localctx, 18, self.RULE_test)
        self._la = 0 # Token type
        try:
            self.state = 148
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,9,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 143
                self.term(0)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 144
                self.term(0)
                self.state = 145
                localctx.op = self._input.LT(1)
                _la = self._input.LA(1)
                if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 1015808) != 0)):
                    localctx.op = self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 146
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
        _startState = 20
        self.enterRecursionRule(localctx, 20, self.RULE_term, _p)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 162
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [7, 8, 9, 10, 11, 12, 13, 14]:
                localctx = qutes_parser.UnaryOperatorContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx

                self.state = 151
                localctx.op = self._input.LT(1)
                _la = self._input.LA(1)
                if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 32640) != 0)):
                    localctx.op = self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 152
                self.term(2)
                pass
            elif token in [36, 37, 38, 39, 40, 41, 42, 43, 44]:
                localctx = qutes_parser.IdentityOperatorContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 160
                self._errHandler.sync(self)
                token = self._input.LA(1)
                if token in [36]:
                    self.state = 153
                    self.boolean()
                    pass
                elif token in [37, 39, 40]:
                    self.state = 154
                    self.integer()
                    pass
                elif token in [38]:
                    self.state = 155
                    self.float_()
                    pass
                elif token in [41]:
                    self.state = 156
                    self.qubit()
                    pass
                elif token in [42]:
                    self.state = 157
                    self.quint()
                    pass
                elif token in [43]:
                    self.state = 158
                    self.qualifiedName()
                    pass
                elif token in [44]:
                    self.state = 159
                    self.string()
                    pass
                else:
                    raise NoViableAltException(self)

                pass
            else:
                raise NoViableAltException(self)

            self._ctx.stop = self._input.LT(-1)
            self.state = 169
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,12,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    localctx = qutes_parser.BinaryOperatorContext(self, qutes_parser.TermContext(self, _parentctx, _parentState))
                    self.pushNewRecursionContext(localctx, _startState, self.RULE_term)
                    self.state = 164
                    if not self.precpred(self._ctx, 3):
                        from antlr4.error.Errors import FailedPredicateException
                        raise FailedPredicateException(self, "self.precpred(self._ctx, 3)")
                    self.state = 165
                    localctx.op = self._input.LT(1)
                    _la = self._input.LA(1)
                    if not(_la==7 or _la==8):
                        localctx.op = self._errHandler.recoverInline(self)
                    else:
                        self._errHandler.reportMatch(self)
                        self.consume()
                    self.state = 166
                    self.term(4) 
                self.state = 171
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,12,self._ctx)

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
        self.enterRule(localctx, 22, self.RULE_type)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 172
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
        self.enterRule(localctx, 24, self.RULE_variableType)
        try:
            self.state = 176
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [1, 2, 3, 4, 5, 6]:
                self.enterOuterAlt(localctx, 1)
                self.state = 174
                self.type_()
                pass
            elif token in [43]:
                self.enterOuterAlt(localctx, 2)
                self.state = 175
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
        self.enterRule(localctx, 26, self.RULE_qualifiedName)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 178
            self.match(qutes_parser.SYMBOL_LITERAL)
            self.state = 183
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,14,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 179
                    self.match(qutes_parser.DOT)
                    self.state = 180
                    self.match(qutes_parser.SYMBOL_LITERAL) 
                self.state = 185
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,14,self._ctx)

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
        self.enterRule(localctx, 28, self.RULE_variableName)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 186
            self.match(qutes_parser.SYMBOL_LITERAL)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class FunctionNameContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def SYMBOL_LITERAL(self):
            return self.getToken(qutes_parser.SYMBOL_LITERAL, 0)

        def getRuleIndex(self):
            return qutes_parser.RULE_functionName

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFunctionName" ):
                listener.enterFunctionName(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFunctionName" ):
                listener.exitFunctionName(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFunctionName" ):
                return visitor.visitFunctionName(self)
            else:
                return visitor.visitChildren(self)




    def functionName(self):

        localctx = qutes_parser.FunctionNameContext(self, self._ctx, self.state)
        self.enterRule(localctx, 30, self.RULE_functionName)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 188
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
        self.enterRule(localctx, 32, self.RULE_string)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 190
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
        self.enterRule(localctx, 34, self.RULE_qubit)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 192
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
        self.enterRule(localctx, 36, self.RULE_quint)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 194
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
        self.enterRule(localctx, 38, self.RULE_float)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 196
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
        self.enterRule(localctx, 40, self.RULE_integer)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 198
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
        self.enterRule(localctx, 42, self.RULE_boolean)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 200
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
        self._predicates[10] = self.term_sempred
        pred = self._predicates.get(ruleIndex, None)
        if pred is None:
            raise Exception("No predicate with index:" + str(ruleIndex))
        else:
            return pred(localctx, predIndex)

    def term_sempred(self, localctx:TermContext, predIndex:int):
            if predIndex == 0:
                return self.precpred(self._ctx, 3)
         




