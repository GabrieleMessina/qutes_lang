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
        4,1,58,224,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,
        6,2,7,7,7,2,8,7,8,2,9,7,9,2,10,7,10,2,11,7,11,2,12,7,12,2,13,7,13,
        2,14,7,14,2,15,7,15,2,16,7,16,2,17,7,17,2,18,7,18,2,19,7,19,2,20,
        7,20,2,21,7,21,2,22,7,22,2,23,7,23,2,24,7,24,1,0,5,0,52,8,0,10,0,
        12,0,55,9,0,1,0,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,
        1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,3,1,83,8,1,1,
        1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,
        1,1,1,1,1,3,1,104,8,1,1,2,1,2,5,2,108,8,2,10,2,12,2,111,9,2,1,2,
        1,2,1,3,1,3,1,3,3,3,118,8,3,1,4,1,4,1,4,1,4,3,4,124,8,4,1,5,1,5,
        1,5,3,5,129,8,5,1,6,1,6,1,6,1,6,1,6,3,6,136,8,6,1,7,1,7,1,7,1,7,
        1,8,1,8,1,8,3,8,145,8,8,1,8,1,8,1,9,1,9,1,9,1,9,1,10,1,10,1,10,1,
        10,1,10,3,10,158,8,10,1,11,1,11,1,11,1,11,1,11,1,11,1,11,1,11,1,
        11,1,11,1,11,1,11,1,11,1,11,1,11,3,11,175,8,11,3,11,177,8,11,1,11,
        1,11,1,11,5,11,182,8,11,10,11,12,11,185,9,11,1,12,1,12,1,12,3,12,
        190,8,12,1,13,1,13,1,14,1,14,3,14,196,8,14,1,15,1,15,1,15,5,15,201,
        8,15,10,15,12,15,204,9,15,1,16,1,16,1,17,1,17,1,18,1,18,1,19,1,19,
        1,20,1,20,1,21,1,21,1,22,1,22,1,23,1,23,1,24,1,24,1,24,0,1,22,25,
        0,2,4,6,8,10,12,14,16,18,20,22,24,26,28,30,32,34,36,38,40,42,44,
        46,48,0,6,1,0,22,26,2,0,10,14,18,20,1,0,16,17,1,0,10,11,1,0,1,8,
        2,0,48,48,50,51,235,0,53,1,0,0,0,2,103,1,0,0,0,4,105,1,0,0,0,6,114,
        1,0,0,0,8,119,1,0,0,0,10,125,1,0,0,0,12,135,1,0,0,0,14,137,1,0,0,
        0,16,141,1,0,0,0,18,148,1,0,0,0,20,157,1,0,0,0,22,176,1,0,0,0,24,
        186,1,0,0,0,26,191,1,0,0,0,28,195,1,0,0,0,30,197,1,0,0,0,32,205,
        1,0,0,0,34,207,1,0,0,0,36,209,1,0,0,0,38,211,1,0,0,0,40,213,1,0,
        0,0,42,215,1,0,0,0,44,217,1,0,0,0,46,219,1,0,0,0,48,221,1,0,0,0,
        50,52,3,2,1,0,51,50,1,0,0,0,52,55,1,0,0,0,53,51,1,0,0,0,53,54,1,
        0,0,0,54,56,1,0,0,0,55,53,1,0,0,0,56,57,5,0,0,1,57,1,1,0,0,0,58,
        59,5,34,0,0,59,60,3,12,6,0,60,61,3,2,1,0,61,104,1,0,0,0,62,63,5,
        34,0,0,63,64,3,12,6,0,64,65,3,2,1,0,65,66,5,35,0,0,66,67,3,2,1,0,
        67,104,1,0,0,0,68,69,5,36,0,0,69,70,3,12,6,0,70,71,3,2,1,0,71,104,
        1,0,0,0,72,73,5,37,0,0,73,74,3,2,1,0,74,75,5,36,0,0,75,76,3,12,6,
        0,76,104,1,0,0,0,77,104,3,4,2,0,78,79,3,28,14,0,79,80,3,34,17,0,
        80,82,5,40,0,0,81,83,3,6,3,0,82,81,1,0,0,0,82,83,1,0,0,0,83,84,1,
        0,0,0,84,85,5,41,0,0,85,86,3,2,1,0,86,104,1,0,0,0,87,88,3,8,4,0,
        88,89,5,28,0,0,89,104,1,0,0,0,90,91,3,30,15,0,91,92,5,27,0,0,92,
        93,3,12,6,0,93,94,5,28,0,0,94,104,1,0,0,0,95,96,5,9,0,0,96,97,3,
        12,6,0,97,98,5,28,0,0,98,104,1,0,0,0,99,100,3,12,6,0,100,101,5,28,
        0,0,101,104,1,0,0,0,102,104,5,28,0,0,103,58,1,0,0,0,103,62,1,0,0,
        0,103,68,1,0,0,0,103,72,1,0,0,0,103,77,1,0,0,0,103,78,1,0,0,0,103,
        87,1,0,0,0,103,90,1,0,0,0,103,95,1,0,0,0,103,99,1,0,0,0,103,102,
        1,0,0,0,104,3,1,0,0,0,105,109,5,38,0,0,106,108,3,2,1,0,107,106,1,
        0,0,0,108,111,1,0,0,0,109,107,1,0,0,0,109,110,1,0,0,0,110,112,1,
        0,0,0,111,109,1,0,0,0,112,113,5,39,0,0,113,5,1,0,0,0,114,117,3,8,
        4,0,115,116,5,46,0,0,116,118,3,6,3,0,117,115,1,0,0,0,117,118,1,0,
        0,0,118,7,1,0,0,0,119,120,3,28,14,0,120,123,3,32,16,0,121,122,5,
        27,0,0,122,124,3,12,6,0,123,121,1,0,0,0,123,124,1,0,0,0,124,9,1,
        0,0,0,125,128,3,30,15,0,126,127,5,46,0,0,127,129,3,10,5,0,128,126,
        1,0,0,0,128,129,1,0,0,0,129,11,1,0,0,0,130,136,3,22,11,0,131,136,
        3,16,8,0,132,136,3,20,10,0,133,136,3,18,9,0,134,136,3,14,7,0,135,
        130,1,0,0,0,135,131,1,0,0,0,135,132,1,0,0,0,135,133,1,0,0,0,135,
        134,1,0,0,0,136,13,1,0,0,0,137,138,3,24,12,0,138,139,5,32,0,0,139,
        140,3,30,15,0,140,15,1,0,0,0,141,142,3,34,17,0,142,144,5,40,0,0,
        143,145,3,10,5,0,144,143,1,0,0,0,144,145,1,0,0,0,145,146,1,0,0,0,
        146,147,5,41,0,0,147,17,1,0,0,0,148,149,5,40,0,0,149,150,3,12,6,
        0,150,151,5,41,0,0,151,19,1,0,0,0,152,158,3,22,11,0,153,154,3,22,
        11,0,154,155,7,0,0,0,155,156,3,22,11,0,156,158,1,0,0,0,157,152,1,
        0,0,0,157,153,1,0,0,0,158,21,1,0,0,0,159,160,6,11,-1,0,160,161,7,
        1,0,0,161,177,3,22,11,3,162,163,7,2,0,0,163,177,3,24,12,0,164,175,
        3,48,24,0,165,175,3,46,23,0,166,175,3,44,22,0,167,175,3,38,19,0,
        168,175,3,40,20,0,169,175,3,42,21,0,170,175,3,30,15,0,171,175,5,
        19,0,0,172,175,5,21,0,0,173,175,3,36,18,0,174,164,1,0,0,0,174,165,
        1,0,0,0,174,166,1,0,0,0,174,167,1,0,0,0,174,168,1,0,0,0,174,169,
        1,0,0,0,174,170,1,0,0,0,174,171,1,0,0,0,174,172,1,0,0,0,174,173,
        1,0,0,0,175,177,1,0,0,0,176,159,1,0,0,0,176,162,1,0,0,0,176,174,
        1,0,0,0,177,183,1,0,0,0,178,179,10,4,0,0,179,180,7,3,0,0,180,182,
        3,22,11,5,181,178,1,0,0,0,182,185,1,0,0,0,183,181,1,0,0,0,183,184,
        1,0,0,0,184,23,1,0,0,0,185,183,1,0,0,0,186,189,3,22,11,0,187,188,
        5,46,0,0,188,190,3,24,12,0,189,187,1,0,0,0,189,190,1,0,0,0,190,25,
        1,0,0,0,191,192,7,4,0,0,192,27,1,0,0,0,193,196,3,26,13,0,194,196,
        3,30,15,0,195,193,1,0,0,0,195,194,1,0,0,0,196,29,1,0,0,0,197,202,
        5,55,0,0,198,199,5,44,0,0,199,201,5,55,0,0,200,198,1,0,0,0,201,204,
        1,0,0,0,202,200,1,0,0,0,202,203,1,0,0,0,203,31,1,0,0,0,204,202,1,
        0,0,0,205,206,5,55,0,0,206,33,1,0,0,0,207,208,5,55,0,0,208,35,1,
        0,0,0,209,210,5,56,0,0,210,37,1,0,0,0,211,212,5,52,0,0,212,39,1,
        0,0,0,213,214,5,53,0,0,214,41,1,0,0,0,215,216,5,54,0,0,216,43,1,
        0,0,0,217,218,5,49,0,0,218,45,1,0,0,0,219,220,7,5,0,0,220,47,1,0,
        0,0,221,222,5,47,0,0,222,49,1,0,0,0,16,53,82,103,109,117,123,128,
        135,144,157,174,176,183,189,195,202
    ]

class qutes_parser ( Parser ):

    grammarFileName = "qutes_parser.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'int'", "'bool'", "'string'", "'qubit'", 
                     "'quint'", "'qustring'", "'float'", "'void'", "'return'", 
                     "'+'", "'-'", "'not'", "'pauliy'", "'pauliz'", "'grover'", 
                     "'mcz'", "'mcx'", "'hadamard'", "'measure'", "'print'", 
                     "'barrier'", "'=='", "'>'", "'>='", "'<'", "'<='", 
                     "'='", "';'", "'var'", "'for'", "'search'", "'in'", 
                     "'where'", "'if'", "'else'", "'while'", "'do'", "'{'", 
                     "'}'", "'('", "')'", "'['", "']'", "'.'", "'\"'", "','" ]

    symbolicNames = [ "<INVALID>", "INT_TYPE", "BOOL_TYPE", "STRING_TYPE", 
                      "QUBIT_TYPE", "QUINT_TYPE", "QUSTRING_TYPE", "FLOAT_TYPE", 
                      "VOID_TYPE", "RETURN", "ADD", "SUB", "NOT", "PAULIY", 
                      "PAULIZ", "GROVER", "MCZ", "MCX", "HADAMARD", "MEASURE", 
                      "PRINT", "BARRIER", "EQUAL", "GREATER", "GREATEREQUAL", 
                      "LOWER", "LOWEREQUAL", "ASSIGN", "END_OF_STATEMENT", 
                      "VAR_STATEMENT", "FOR_STATEMENT", "SEARCH_STATEMENT", 
                      "IN_STATEMENT", "WHERE_STATEMENT", "IF_STATEMENT", 
                      "ELSE_STATEMENT", "WHILE_STATEMENT", "DO_STATEMENT", 
                      "CURLY_PARENTHESIS_OPEN", "CURLY_PARENTHESIS_CLOSE", 
                      "ROUND_PARENTHESIS_OPEN", "ROUND_PARENTHESIS_CLOSE", 
                      "SQUARE_PARENTHESIS_OPEN", "SQUARE_PARENTHESIS_CLOSE", 
                      "DOT", "STRING_ENCLOSURE", "COMMA", "BOOL_LITERAL", 
                      "INT_LITERAL", "FLOAT_LITERAL", "HEX_LITERAL", "BIN_LITERAL", 
                      "QUBIT_LITERAL", "QUINT_LITERAL", "QUSTRING_LITERAL", 
                      "SYMBOL_LITERAL", "STRING_LITERAL", "WS", "NEWLINE" ]

    RULE_program = 0
    RULE_statement = 1
    RULE_block = 2
    RULE_functionDeclarationParams = 3
    RULE_variableDeclaration = 4
    RULE_functionCallParams = 5
    RULE_expr = 6
    RULE_groverExpr = 7
    RULE_functionCall = 8
    RULE_parenExpr = 9
    RULE_test = 10
    RULE_term = 11
    RULE_termList = 12
    RULE_type = 13
    RULE_variableType = 14
    RULE_qualifiedName = 15
    RULE_variableName = 16
    RULE_functionName = 17
    RULE_string = 18
    RULE_qubit = 19
    RULE_quint = 20
    RULE_qustring = 21
    RULE_float = 22
    RULE_integer = 23
    RULE_boolean = 24

    ruleNames =  [ "program", "statement", "block", "functionDeclarationParams", 
                   "variableDeclaration", "functionCallParams", "expr", 
                   "groverExpr", "functionCall", "parenExpr", "test", "term", 
                   "termList", "type", "variableType", "qualifiedName", 
                   "variableName", "functionName", "string", "qubit", "quint", 
                   "qustring", "float", "integer", "boolean" ]

    EOF = Token.EOF
    INT_TYPE=1
    BOOL_TYPE=2
    STRING_TYPE=3
    QUBIT_TYPE=4
    QUINT_TYPE=5
    QUSTRING_TYPE=6
    FLOAT_TYPE=7
    VOID_TYPE=8
    RETURN=9
    ADD=10
    SUB=11
    NOT=12
    PAULIY=13
    PAULIZ=14
    GROVER=15
    MCZ=16
    MCX=17
    HADAMARD=18
    MEASURE=19
    PRINT=20
    BARRIER=21
    EQUAL=22
    GREATER=23
    GREATEREQUAL=24
    LOWER=25
    LOWEREQUAL=26
    ASSIGN=27
    END_OF_STATEMENT=28
    VAR_STATEMENT=29
    FOR_STATEMENT=30
    SEARCH_STATEMENT=31
    IN_STATEMENT=32
    WHERE_STATEMENT=33
    IF_STATEMENT=34
    ELSE_STATEMENT=35
    WHILE_STATEMENT=36
    DO_STATEMENT=37
    CURLY_PARENTHESIS_OPEN=38
    CURLY_PARENTHESIS_CLOSE=39
    ROUND_PARENTHESIS_OPEN=40
    ROUND_PARENTHESIS_CLOSE=41
    SQUARE_PARENTHESIS_OPEN=42
    SQUARE_PARENTHESIS_CLOSE=43
    DOT=44
    STRING_ENCLOSURE=45
    COMMA=46
    BOOL_LITERAL=47
    INT_LITERAL=48
    FLOAT_LITERAL=49
    HEX_LITERAL=50
    BIN_LITERAL=51
    QUBIT_LITERAL=52
    QUINT_LITERAL=53
    QUSTRING_LITERAL=54
    SYMBOL_LITERAL=55
    STRING_LITERAL=56
    WS=57
    NEWLINE=58

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
            self.state = 53
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 143976048587931646) != 0):
                self.state = 50
                self.statement()
                self.state = 55
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 56
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


    class ReturnStatementContext(StatementContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a qutes_parser.StatementContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def RETURN(self):
            return self.getToken(qutes_parser.RETURN, 0)
        def expr(self):
            return self.getTypedRuleContext(qutes_parser.ExprContext,0)

        def END_OF_STATEMENT(self):
            return self.getToken(qutes_parser.END_OF_STATEMENT, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterReturnStatement" ):
                listener.enterReturnStatement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitReturnStatement" ):
                listener.exitReturnStatement(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitReturnStatement" ):
                return visitor.visitReturnStatement(self)
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
            self.state = 103
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,2,self._ctx)
            if la_ == 1:
                localctx = qutes_parser.IfStatementContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 58
                self.match(qutes_parser.IF_STATEMENT)
                self.state = 59
                self.expr()
                self.state = 60
                self.statement()
                pass

            elif la_ == 2:
                localctx = qutes_parser.IfElseStatementContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 62
                self.match(qutes_parser.IF_STATEMENT)
                self.state = 63
                self.expr()
                self.state = 64
                self.statement()
                self.state = 65
                self.match(qutes_parser.ELSE_STATEMENT)
                self.state = 66
                self.statement()
                pass

            elif la_ == 3:
                localctx = qutes_parser.WhileStatementContext(self, localctx)
                self.enterOuterAlt(localctx, 3)
                self.state = 68
                self.match(qutes_parser.WHILE_STATEMENT)
                self.state = 69
                self.expr()
                self.state = 70
                self.statement()
                pass

            elif la_ == 4:
                localctx = qutes_parser.DoWhileStatementContext(self, localctx)
                self.enterOuterAlt(localctx, 4)
                self.state = 72
                self.match(qutes_parser.DO_STATEMENT)
                self.state = 73
                self.statement()
                self.state = 74
                self.match(qutes_parser.WHILE_STATEMENT)
                self.state = 75
                self.expr()
                pass

            elif la_ == 5:
                localctx = qutes_parser.BlockStatementContext(self, localctx)
                self.enterOuterAlt(localctx, 5)
                self.state = 77
                self.block()
                pass

            elif la_ == 6:
                localctx = qutes_parser.FunctionStatementContext(self, localctx)
                self.enterOuterAlt(localctx, 6)
                self.state = 78
                self.variableType()
                self.state = 79
                self.functionName()
                self.state = 80
                self.match(qutes_parser.ROUND_PARENTHESIS_OPEN)
                self.state = 82
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if (((_la) & ~0x3f) == 0 and ((1 << _la) & 36028797018964478) != 0):
                    self.state = 81
                    self.functionDeclarationParams()


                self.state = 84
                self.match(qutes_parser.ROUND_PARENTHESIS_CLOSE)
                self.state = 85
                self.statement()
                pass

            elif la_ == 7:
                localctx = qutes_parser.DeclarationStatementContext(self, localctx)
                self.enterOuterAlt(localctx, 7)
                self.state = 87
                self.variableDeclaration()
                self.state = 88
                self.match(qutes_parser.END_OF_STATEMENT)
                pass

            elif la_ == 8:
                localctx = qutes_parser.AssignmentStatementContext(self, localctx)
                self.enterOuterAlt(localctx, 8)
                self.state = 90
                self.qualifiedName()
                self.state = 91
                self.match(qutes_parser.ASSIGN)
                self.state = 92
                self.expr()
                self.state = 93
                self.match(qutes_parser.END_OF_STATEMENT)
                pass

            elif la_ == 9:
                localctx = qutes_parser.ReturnStatementContext(self, localctx)
                self.enterOuterAlt(localctx, 9)
                self.state = 95
                self.match(qutes_parser.RETURN)
                self.state = 96
                self.expr()
                self.state = 97
                self.match(qutes_parser.END_OF_STATEMENT)
                pass

            elif la_ == 10:
                localctx = qutes_parser.ExpressionStatementContext(self, localctx)
                self.enterOuterAlt(localctx, 10)
                self.state = 99
                self.expr()
                self.state = 100
                self.match(qutes_parser.END_OF_STATEMENT)
                pass

            elif la_ == 11:
                localctx = qutes_parser.EmptyStatementContext(self, localctx)
                self.enterOuterAlt(localctx, 11)
                self.state = 102
                self.match(qutes_parser.END_OF_STATEMENT)
                pass


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
        self.enterRule(localctx, 4, self.RULE_block)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 105
            self.match(qutes_parser.CURLY_PARENTHESIS_OPEN)
            self.state = 109
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 143976048587931646) != 0):
                self.state = 106
                self.statement()
                self.state = 111
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 112
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


        def COMMA(self):
            return self.getToken(qutes_parser.COMMA, 0)

        def functionDeclarationParams(self):
            return self.getTypedRuleContext(qutes_parser.FunctionDeclarationParamsContext,0)


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
        self.enterRule(localctx, 6, self.RULE_functionDeclarationParams)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 114
            self.variableDeclaration()
            self.state = 117
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==46:
                self.state = 115
                self.match(qutes_parser.COMMA)
                self.state = 116
                self.functionDeclarationParams()


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
        self.enterRule(localctx, 8, self.RULE_variableDeclaration)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 119
            self.variableType()
            self.state = 120
            self.variableName()
            self.state = 123
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==27:
                self.state = 121
                self.match(qutes_parser.ASSIGN)
                self.state = 122
                self.expr()


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


        def COMMA(self):
            return self.getToken(qutes_parser.COMMA, 0)

        def functionCallParams(self):
            return self.getTypedRuleContext(qutes_parser.FunctionCallParamsContext,0)


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
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 125
            self.qualifiedName()
            self.state = 128
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==46:
                self.state = 126
                self.match(qutes_parser.COMMA)
                self.state = 127
                self.functionCallParams()


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


        def groverExpr(self):
            return self.getTypedRuleContext(qutes_parser.GroverExprContext,0)


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
            self.state = 135
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,7,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 130
                self.term(0)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 131
                self.functionCall()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 132
                self.test()
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 133
                self.parenExpr()
                pass

            elif la_ == 5:
                self.enterOuterAlt(localctx, 5)
                self.state = 134
                self.groverExpr()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class GroverExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.op = None # Token

        def termList(self):
            return self.getTypedRuleContext(qutes_parser.TermListContext,0)


        def qualifiedName(self):
            return self.getTypedRuleContext(qutes_parser.QualifiedNameContext,0)


        def IN_STATEMENT(self):
            return self.getToken(qutes_parser.IN_STATEMENT, 0)

        def getRuleIndex(self):
            return qutes_parser.RULE_groverExpr

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterGroverExpr" ):
                listener.enterGroverExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitGroverExpr" ):
                listener.exitGroverExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitGroverExpr" ):
                return visitor.visitGroverExpr(self)
            else:
                return visitor.visitChildren(self)




    def groverExpr(self):

        localctx = qutes_parser.GroverExprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_groverExpr)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 137
            self.termList()
            self.state = 138
            localctx.op = self.match(qutes_parser.IN_STATEMENT)
            self.state = 139
            self.qualifiedName()
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
        self.enterRule(localctx, 16, self.RULE_functionCall)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 141
            self.functionName()
            self.state = 142
            self.match(qutes_parser.ROUND_PARENTHESIS_OPEN)
            self.state = 144
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==55:
                self.state = 143
                self.functionCallParams()


            self.state = 146
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
        self.enterRule(localctx, 18, self.RULE_parenExpr)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 148
            self.match(qutes_parser.ROUND_PARENTHESIS_OPEN)
            self.state = 149
            self.expr()
            self.state = 150
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
        self.enterRule(localctx, 20, self.RULE_test)
        self._la = 0 # Token type
        try:
            self.state = 157
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,9,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 152
                self.term(0)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 153
                self.term(0)
                self.state = 154
                localctx.op = self._input.LT(1)
                _la = self._input.LA(1)
                if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 130023424) != 0)):
                    localctx.op = self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 155
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


    class MultipleUnaryOperatorContext(TermContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a qutes_parser.TermContext
            super().__init__(parser)
            self.op = None # Token
            self.copyFrom(ctx)

        def termList(self):
            return self.getTypedRuleContext(qutes_parser.TermListContext,0)

        def MCX(self):
            return self.getToken(qutes_parser.MCX, 0)
        def MCZ(self):
            return self.getToken(qutes_parser.MCZ, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterMultipleUnaryOperator" ):
                listener.enterMultipleUnaryOperator(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitMultipleUnaryOperator" ):
                listener.exitMultipleUnaryOperator(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitMultipleUnaryOperator" ):
                return visitor.visitMultipleUnaryOperator(self)
            else:
                return visitor.visitChildren(self)


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

        def qustring(self):
            return self.getTypedRuleContext(qutes_parser.QustringContext,0)

        def qualifiedName(self):
            return self.getTypedRuleContext(qutes_parser.QualifiedNameContext,0)

        def MEASURE(self):
            return self.getToken(qutes_parser.MEASURE, 0)
        def BARRIER(self):
            return self.getToken(qutes_parser.BARRIER, 0)
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
        _startState = 22
        self.enterRecursionRule(localctx, 22, self.RULE_term, _p)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 176
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,11,self._ctx)
            if la_ == 1:
                localctx = qutes_parser.UnaryOperatorContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx

                self.state = 160
                localctx.op = self._input.LT(1)
                _la = self._input.LA(1)
                if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 1866752) != 0)):
                    localctx.op = self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 161
                self.term(3)
                pass

            elif la_ == 2:
                localctx = qutes_parser.MultipleUnaryOperatorContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 162
                localctx.op = self._input.LT(1)
                _la = self._input.LA(1)
                if not(_la==16 or _la==17):
                    localctx.op = self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 163
                self.termList()
                pass

            elif la_ == 3:
                localctx = qutes_parser.IdentityOperatorContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 174
                self._errHandler.sync(self)
                token = self._input.LA(1)
                if token in [47]:
                    self.state = 164
                    self.boolean()
                    pass
                elif token in [48, 50, 51]:
                    self.state = 165
                    self.integer()
                    pass
                elif token in [49]:
                    self.state = 166
                    self.float_()
                    pass
                elif token in [52]:
                    self.state = 167
                    self.qubit()
                    pass
                elif token in [53]:
                    self.state = 168
                    self.quint()
                    pass
                elif token in [54]:
                    self.state = 169
                    self.qustring()
                    pass
                elif token in [55]:
                    self.state = 170
                    self.qualifiedName()
                    pass
                elif token in [19]:
                    self.state = 171
                    self.match(qutes_parser.MEASURE)
                    pass
                elif token in [21]:
                    self.state = 172
                    self.match(qutes_parser.BARRIER)
                    pass
                elif token in [56]:
                    self.state = 173
                    self.string()
                    pass
                else:
                    raise NoViableAltException(self)

                pass


            self._ctx.stop = self._input.LT(-1)
            self.state = 183
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,12,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    localctx = qutes_parser.BinaryOperatorContext(self, qutes_parser.TermContext(self, _parentctx, _parentState))
                    self.pushNewRecursionContext(localctx, _startState, self.RULE_term)
                    self.state = 178
                    if not self.precpred(self._ctx, 4):
                        from antlr4.error.Errors import FailedPredicateException
                        raise FailedPredicateException(self, "self.precpred(self._ctx, 4)")
                    self.state = 179
                    localctx.op = self._input.LT(1)
                    _la = self._input.LA(1)
                    if not(_la==10 or _la==11):
                        localctx.op = self._errHandler.recoverInline(self)
                    else:
                        self._errHandler.reportMatch(self)
                        self.consume()
                    self.state = 180
                    self.term(5) 
                self.state = 185
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,12,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.unrollRecursionContexts(_parentctx)
        return localctx


    class TermListContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def term(self):
            return self.getTypedRuleContext(qutes_parser.TermContext,0)


        def COMMA(self):
            return self.getToken(qutes_parser.COMMA, 0)

        def termList(self):
            return self.getTypedRuleContext(qutes_parser.TermListContext,0)


        def getRuleIndex(self):
            return qutes_parser.RULE_termList

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTermList" ):
                listener.enterTermList(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTermList" ):
                listener.exitTermList(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitTermList" ):
                return visitor.visitTermList(self)
            else:
                return visitor.visitChildren(self)




    def termList(self):

        localctx = qutes_parser.TermListContext(self, self._ctx, self.state)
        self.enterRule(localctx, 24, self.RULE_termList)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 186
            self.term(0)
            self.state = 189
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,13,self._ctx)
            if la_ == 1:
                self.state = 187
                self.match(qutes_parser.COMMA)
                self.state = 188
                self.termList()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
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

        def QUSTRING_TYPE(self):
            return self.getToken(qutes_parser.QUSTRING_TYPE, 0)

        def VOID_TYPE(self):
            return self.getToken(qutes_parser.VOID_TYPE, 0)

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
        self.enterRule(localctx, 26, self.RULE_type)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 191
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 510) != 0)):
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
        self.enterRule(localctx, 28, self.RULE_variableType)
        try:
            self.state = 195
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [1, 2, 3, 4, 5, 6, 7, 8]:
                self.enterOuterAlt(localctx, 1)
                self.state = 193
                self.type_()
                pass
            elif token in [55]:
                self.enterOuterAlt(localctx, 2)
                self.state = 194
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
        self.enterRule(localctx, 30, self.RULE_qualifiedName)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 197
            self.match(qutes_parser.SYMBOL_LITERAL)
            self.state = 202
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,15,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 198
                    self.match(qutes_parser.DOT)
                    self.state = 199
                    self.match(qutes_parser.SYMBOL_LITERAL) 
                self.state = 204
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,15,self._ctx)

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
        self.enterRule(localctx, 32, self.RULE_variableName)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 205
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
        self.enterRule(localctx, 34, self.RULE_functionName)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 207
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
        self.enterRule(localctx, 36, self.RULE_string)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 209
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
        self.enterRule(localctx, 38, self.RULE_qubit)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 211
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
        self.enterRule(localctx, 40, self.RULE_quint)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 213
            self.match(qutes_parser.QUINT_LITERAL)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class QustringContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def QUSTRING_LITERAL(self):
            return self.getToken(qutes_parser.QUSTRING_LITERAL, 0)

        def getRuleIndex(self):
            return qutes_parser.RULE_qustring

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterQustring" ):
                listener.enterQustring(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitQustring" ):
                listener.exitQustring(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitQustring" ):
                return visitor.visitQustring(self)
            else:
                return visitor.visitChildren(self)




    def qustring(self):

        localctx = qutes_parser.QustringContext(self, self._ctx, self.state)
        self.enterRule(localctx, 42, self.RULE_qustring)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 215
            self.match(qutes_parser.QUSTRING_LITERAL)
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
        self.enterRule(localctx, 44, self.RULE_float)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 217
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
        self.enterRule(localctx, 46, self.RULE_integer)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 219
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 3659174697238528) != 0)):
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
        self.enterRule(localctx, 48, self.RULE_boolean)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 221
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
        self._predicates[11] = self.term_sempred
        pred = self._predicates.get(ruleIndex, None)
        if pred is None:
            raise Exception("No predicate with index:" + str(ruleIndex))
        else:
            return pred(localctx, predIndex)

    def term_sempred(self, localctx:TermContext, predIndex:int):
            if predIndex == 0:
                return self.precpred(self._ctx, 4)
         




