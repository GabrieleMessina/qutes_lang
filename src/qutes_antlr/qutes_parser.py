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
        4,1,75,232,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,
        6,2,7,7,7,2,8,7,8,2,9,7,9,2,10,7,10,2,11,7,11,2,12,7,12,2,13,7,13,
        2,14,7,14,2,15,7,15,2,16,7,16,2,17,7,17,2,18,7,18,2,19,7,19,1,0,
        5,0,42,8,0,10,0,12,0,45,9,0,1,0,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,
        1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,5,1,70,8,
        1,10,1,12,1,73,9,1,1,1,1,1,1,1,1,1,1,1,3,1,80,8,1,1,1,1,1,1,1,1,
        1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,
        1,3,1,102,8,1,1,2,1,2,1,2,3,2,107,8,2,1,3,1,3,1,3,1,3,3,3,113,8,
        3,1,4,1,4,1,4,1,4,1,4,1,4,1,4,1,4,1,4,1,4,3,4,125,8,4,1,4,1,4,1,
        4,1,4,1,4,1,4,1,4,1,4,1,4,1,4,1,4,1,4,1,4,1,4,1,4,1,4,1,4,3,4,144,
        8,4,1,4,1,4,1,4,1,4,1,4,1,4,1,4,1,4,1,4,1,4,1,4,1,4,1,4,1,4,1,4,
        1,4,1,4,1,4,1,4,1,4,5,4,166,8,4,10,4,12,4,169,9,4,1,5,1,5,3,5,173,
        8,5,1,5,1,5,3,5,177,8,5,1,6,1,6,3,6,181,8,6,1,6,1,6,3,6,185,8,6,
        1,7,1,7,3,7,189,8,7,1,8,1,8,1,9,1,9,1,9,5,9,196,8,9,10,9,12,9,199,
        9,9,1,9,1,9,3,9,203,8,9,1,10,1,10,1,11,1,11,1,12,1,12,1,12,1,12,
        1,12,1,12,1,12,3,12,216,8,12,1,13,1,13,1,14,1,14,1,15,1,15,1,16,
        1,16,1,17,1,17,1,18,1,18,1,19,1,19,1,19,0,1,8,20,0,2,4,6,8,10,12,
        14,16,18,20,22,24,26,28,30,32,34,36,38,0,11,2,0,28,28,30,30,2,0,
        13,15,38,39,2,0,19,19,23,25,2,0,20,21,27,29,1,0,10,12,1,0,13,14,
        1,0,33,36,1,0,31,32,1,0,38,39,1,0,1,8,2,0,65,65,67,68,257,0,43,1,
        0,0,0,2,101,1,0,0,0,4,103,1,0,0,0,6,108,1,0,0,0,8,143,1,0,0,0,10,
        172,1,0,0,0,12,180,1,0,0,0,14,188,1,0,0,0,16,190,1,0,0,0,18,202,
        1,0,0,0,20,204,1,0,0,0,22,206,1,0,0,0,24,215,1,0,0,0,26,217,1,0,
        0,0,28,219,1,0,0,0,30,221,1,0,0,0,32,223,1,0,0,0,34,225,1,0,0,0,
        36,227,1,0,0,0,38,229,1,0,0,0,40,42,3,2,1,0,41,40,1,0,0,0,42,45,
        1,0,0,0,43,41,1,0,0,0,43,44,1,0,0,0,44,46,1,0,0,0,45,43,1,0,0,0,
        46,47,5,0,0,1,47,1,1,0,0,0,48,49,5,51,0,0,49,50,3,8,4,0,50,51,3,
        2,1,0,51,102,1,0,0,0,52,53,5,51,0,0,53,54,3,8,4,0,54,55,3,2,1,0,
        55,56,5,52,0,0,56,57,3,2,1,0,57,102,1,0,0,0,58,59,5,53,0,0,59,60,
        3,8,4,0,60,61,3,2,1,0,61,102,1,0,0,0,62,63,5,54,0,0,63,64,3,2,1,
        0,64,65,5,53,0,0,65,66,3,8,4,0,66,102,1,0,0,0,67,71,5,55,0,0,68,
        70,3,2,1,0,69,68,1,0,0,0,70,73,1,0,0,0,71,69,1,0,0,0,71,72,1,0,0,
        0,72,74,1,0,0,0,73,71,1,0,0,0,74,102,5,56,0,0,75,76,3,14,7,0,76,
        77,3,22,11,0,77,79,5,57,0,0,78,80,3,4,2,0,79,78,1,0,0,0,79,80,1,
        0,0,0,80,81,1,0,0,0,81,82,5,58,0,0,82,83,3,2,1,0,83,102,1,0,0,0,
        84,85,3,6,3,0,85,86,5,45,0,0,86,102,1,0,0,0,87,88,3,18,9,0,88,89,
        5,37,0,0,89,90,3,8,4,0,90,91,5,45,0,0,91,102,1,0,0,0,92,93,5,9,0,
        0,93,94,3,8,4,0,94,95,5,45,0,0,95,102,1,0,0,0,96,97,3,8,4,0,97,98,
        5,45,0,0,98,102,1,0,0,0,99,102,7,0,0,0,100,102,5,45,0,0,101,48,1,
        0,0,0,101,52,1,0,0,0,101,58,1,0,0,0,101,62,1,0,0,0,101,67,1,0,0,
        0,101,75,1,0,0,0,101,84,1,0,0,0,101,87,1,0,0,0,101,92,1,0,0,0,101,
        96,1,0,0,0,101,99,1,0,0,0,101,100,1,0,0,0,102,3,1,0,0,0,103,106,
        3,6,3,0,104,105,5,63,0,0,105,107,3,4,2,0,106,104,1,0,0,0,106,107,
        1,0,0,0,107,5,1,0,0,0,108,109,3,14,7,0,109,112,3,20,10,0,110,111,
        5,37,0,0,111,113,3,8,4,0,112,110,1,0,0,0,112,113,1,0,0,0,113,7,1,
        0,0,0,114,115,6,4,-1,0,115,116,5,57,0,0,116,117,3,8,4,0,117,118,
        5,58,0,0,118,144,1,0,0,0,119,144,3,24,12,0,120,144,3,18,9,0,121,
        122,3,22,11,0,122,124,5,57,0,0,123,125,3,10,5,0,124,123,1,0,0,0,
        124,125,1,0,0,0,125,126,1,0,0,0,126,127,5,58,0,0,127,144,1,0,0,0,
        128,129,7,1,0,0,129,144,3,8,4,11,130,131,7,2,0,0,131,144,3,12,6,
        0,132,133,7,3,0,0,133,144,3,8,4,3,134,135,5,26,0,0,135,136,3,12,
        6,0,136,137,5,18,0,0,137,138,3,8,4,2,138,144,1,0,0,0,139,140,3,12,
        6,0,140,141,5,49,0,0,141,142,3,18,9,0,142,144,1,0,0,0,143,114,1,
        0,0,0,143,119,1,0,0,0,143,120,1,0,0,0,143,121,1,0,0,0,143,128,1,
        0,0,0,143,130,1,0,0,0,143,132,1,0,0,0,143,134,1,0,0,0,143,139,1,
        0,0,0,144,167,1,0,0,0,145,146,10,10,0,0,146,147,7,4,0,0,147,166,
        3,8,4,11,148,149,10,9,0,0,149,150,7,5,0,0,150,166,3,8,4,10,151,152,
        10,8,0,0,152,153,7,6,0,0,153,166,3,8,4,9,154,155,10,7,0,0,155,156,
        7,7,0,0,156,166,3,8,4,8,157,158,10,6,0,0,158,159,5,16,0,0,159,166,
        3,8,4,7,160,161,10,5,0,0,161,162,5,17,0,0,162,166,3,8,4,6,163,164,
        10,12,0,0,164,166,7,8,0,0,165,145,1,0,0,0,165,148,1,0,0,0,165,151,
        1,0,0,0,165,154,1,0,0,0,165,157,1,0,0,0,165,160,1,0,0,0,165,163,
        1,0,0,0,166,169,1,0,0,0,167,165,1,0,0,0,167,168,1,0,0,0,168,9,1,
        0,0,0,169,167,1,0,0,0,170,173,3,24,12,0,171,173,3,18,9,0,172,170,
        1,0,0,0,172,171,1,0,0,0,173,176,1,0,0,0,174,175,5,63,0,0,175,177,
        3,10,5,0,176,174,1,0,0,0,176,177,1,0,0,0,177,11,1,0,0,0,178,181,
        3,24,12,0,179,181,3,18,9,0,180,178,1,0,0,0,180,179,1,0,0,0,181,184,
        1,0,0,0,182,183,5,63,0,0,183,185,3,12,6,0,184,182,1,0,0,0,184,185,
        1,0,0,0,185,13,1,0,0,0,186,189,3,16,8,0,187,189,3,18,9,0,188,186,
        1,0,0,0,188,187,1,0,0,0,189,15,1,0,0,0,190,191,7,9,0,0,191,17,1,
        0,0,0,192,197,5,72,0,0,193,194,5,61,0,0,194,196,5,72,0,0,195,193,
        1,0,0,0,196,199,1,0,0,0,197,195,1,0,0,0,197,198,1,0,0,0,198,203,
        1,0,0,0,199,197,1,0,0,0,200,203,3,20,10,0,201,203,3,22,11,0,202,
        192,1,0,0,0,202,200,1,0,0,0,202,201,1,0,0,0,203,19,1,0,0,0,204,205,
        5,72,0,0,205,21,1,0,0,0,206,207,5,72,0,0,207,23,1,0,0,0,208,216,
        3,38,19,0,209,216,3,36,18,0,210,216,3,34,17,0,211,216,3,28,14,0,
        212,216,3,30,15,0,213,216,3,32,16,0,214,216,3,26,13,0,215,208,1,
        0,0,0,215,209,1,0,0,0,215,210,1,0,0,0,215,211,1,0,0,0,215,212,1,
        0,0,0,215,213,1,0,0,0,215,214,1,0,0,0,216,25,1,0,0,0,217,218,5,73,
        0,0,218,27,1,0,0,0,219,220,5,69,0,0,220,29,1,0,0,0,221,222,5,70,
        0,0,222,31,1,0,0,0,223,224,5,71,0,0,224,33,1,0,0,0,225,226,5,66,
        0,0,226,35,1,0,0,0,227,228,7,10,0,0,228,37,1,0,0,0,229,230,5,64,
        0,0,230,39,1,0,0,0,18,43,71,79,101,106,112,124,143,165,167,172,176,
        180,184,188,197,202,215
    ]

class qutes_parser ( Parser ):

    grammarFileName = "qutes_parser.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'int'", "'bool'", "'string'", "'qubit'", 
                     "'quint'", "'qustring'", "'float'", "'void'", "'return'", 
                     "'*'", "'/'", "'%'", "'+'", "'-'", "'not'", "'and'", 
                     "'or'", "'by'", "'swap'", "'pauliy'", "'pauliz'", "'grover'", 
                     "'mcz'", "'mcx'", "'mcy'", "'mcp'", "'hadamard'", "'measure'", 
                     "'print'", "'barrier'", "'=='", "'!='", "'>'", "'>='", 
                     "'<'", "'<='", "'='", "'++'", "'--'", "'+='", "'-='", 
                     "'*='", "'/='", "'%='", "';'", "'var'", "'for'", "'search'", 
                     "'in'", "'where'", "'if'", "'else'", "'while'", "'do'", 
                     "'{'", "'}'", "'('", "')'", "'['", "']'", "'.'", "'\"'", 
                     "','" ]

    symbolicNames = [ "<INVALID>", "INT_TYPE", "BOOL_TYPE", "STRING_TYPE", 
                      "QUBIT_TYPE", "QUINT_TYPE", "QUSTRING_TYPE", "FLOAT_TYPE", 
                      "VOID_TYPE", "RETURN", "MULTIPLY", "DIVIDE", "MODULE", 
                      "ADD", "SUB", "NOT", "AND", "OR", "BY", "SWAP", "PAULIY", 
                      "PAULIZ", "GROVER", "MCZ", "MCX", "MCY", "MCP", "HADAMARD", 
                      "MEASURE", "PRINT", "BARRIER", "EQUAL", "NOT_EQUAL", 
                      "GREATER", "GREATEREQUAL", "LOWER", "LOWEREQUAL", 
                      "ASSIGN", "AUTO_INCREMENT", "AUTO_DECREMENT", "AUTO_SUM", 
                      "AUTO_SUB", "AUTO_MULTIPLY", "AUTO_DIVIDE", "AUTO_MODULE", 
                      "END_OF_STATEMENT", "VAR_STATEMENT", "FOR_STATEMENT", 
                      "SEARCH_STATEMENT", "IN_STATEMENT", "WHERE_STATEMENT", 
                      "IF_STATEMENT", "ELSE_STATEMENT", "WHILE_STATEMENT", 
                      "DO_STATEMENT", "CURLY_PARENTHESIS_OPEN", "CURLY_PARENTHESIS_CLOSE", 
                      "ROUND_PARENTHESIS_OPEN", "ROUND_PARENTHESIS_CLOSE", 
                      "SQUARE_PARENTHESIS_OPEN", "SQUARE_PARENTHESIS_CLOSE", 
                      "DOT", "STRING_ENCLOSURE", "COMMA", "BOOL_LITERAL", 
                      "INT_LITERAL", "FLOAT_LITERAL", "HEX_LITERAL", "BIN_LITERAL", 
                      "QUBIT_LITERAL", "QUINT_LITERAL", "QUSTRING_LITERAL", 
                      "SYMBOL_LITERAL", "STRING_LITERAL", "WS", "NEWLINE" ]

    RULE_program = 0
    RULE_statement = 1
    RULE_functionDeclarationParams = 2
    RULE_variableDeclaration = 3
    RULE_expr = 4
    RULE_functionCallParams = 5
    RULE_termList = 6
    RULE_variableType = 7
    RULE_type = 8
    RULE_qualifiedName = 9
    RULE_variableName = 10
    RULE_functionName = 11
    RULE_literal = 12
    RULE_string = 13
    RULE_qubit = 14
    RULE_quint = 15
    RULE_qustring = 16
    RULE_float = 17
    RULE_integer = 18
    RULE_boolean = 19

    ruleNames =  [ "program", "statement", "functionDeclarationParams", 
                   "variableDeclaration", "expr", "functionCallParams", 
                   "termList", "variableType", "type", "qualifiedName", 
                   "variableName", "functionName", "literal", "string", 
                   "qubit", "quint", "qustring", "float", "integer", "boolean" ]

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
    MULTIPLY=10
    DIVIDE=11
    MODULE=12
    ADD=13
    SUB=14
    NOT=15
    AND=16
    OR=17
    BY=18
    SWAP=19
    PAULIY=20
    PAULIZ=21
    GROVER=22
    MCZ=23
    MCX=24
    MCY=25
    MCP=26
    HADAMARD=27
    MEASURE=28
    PRINT=29
    BARRIER=30
    EQUAL=31
    NOT_EQUAL=32
    GREATER=33
    GREATEREQUAL=34
    LOWER=35
    LOWEREQUAL=36
    ASSIGN=37
    AUTO_INCREMENT=38
    AUTO_DECREMENT=39
    AUTO_SUM=40
    AUTO_SUB=41
    AUTO_MULTIPLY=42
    AUTO_DIVIDE=43
    AUTO_MODULE=44
    END_OF_STATEMENT=45
    VAR_STATEMENT=46
    FOR_STATEMENT=47
    SEARCH_STATEMENT=48
    IN_STATEMENT=49
    WHERE_STATEMENT=50
    IF_STATEMENT=51
    ELSE_STATEMENT=52
    WHILE_STATEMENT=53
    DO_STATEMENT=54
    CURLY_PARENTHESIS_OPEN=55
    CURLY_PARENTHESIS_CLOSE=56
    ROUND_PARENTHESIS_OPEN=57
    ROUND_PARENTHESIS_CLOSE=58
    SQUARE_PARENTHESIS_OPEN=59
    SQUARE_PARENTHESIS_CLOSE=60
    DOT=61
    STRING_ENCLOSURE=62
    COMMA=63
    BOOL_LITERAL=64
    INT_LITERAL=65
    FLOAT_LITERAL=66
    HEX_LITERAL=67
    BIN_LITERAL=68
    QUBIT_LITERAL=69
    QUINT_LITERAL=70
    QUSTRING_LITERAL=71
    SYMBOL_LITERAL=72
    STRING_LITERAL=73
    WS=74
    NEWLINE=75

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
            self.state = 43
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 209453393821361150) != 0) or ((((_la - 64)) & ~0x3f) == 0 and ((1 << (_la - 64)) & 1023) != 0):
                self.state = 40
                self.statement()
                self.state = 45
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 46
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


    class FactStatementContext(StatementContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a qutes_parser.StatementContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def MEASURE(self):
            return self.getToken(qutes_parser.MEASURE, 0)
        def BARRIER(self):
            return self.getToken(qutes_parser.BARRIER, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFactStatement" ):
                listener.enterFactStatement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFactStatement" ):
                listener.exitFactStatement(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFactStatement" ):
                return visitor.visitFactStatement(self)
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
            self.state = 101
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,3,self._ctx)
            if la_ == 1:
                localctx = qutes_parser.IfStatementContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 48
                self.match(qutes_parser.IF_STATEMENT)
                self.state = 49
                self.expr(0)
                self.state = 50
                self.statement()
                pass

            elif la_ == 2:
                localctx = qutes_parser.IfElseStatementContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 52
                self.match(qutes_parser.IF_STATEMENT)
                self.state = 53
                self.expr(0)
                self.state = 54
                self.statement()
                self.state = 55
                self.match(qutes_parser.ELSE_STATEMENT)
                self.state = 56
                self.statement()
                pass

            elif la_ == 3:
                localctx = qutes_parser.WhileStatementContext(self, localctx)
                self.enterOuterAlt(localctx, 3)
                self.state = 58
                self.match(qutes_parser.WHILE_STATEMENT)
                self.state = 59
                self.expr(0)
                self.state = 60
                self.statement()
                pass

            elif la_ == 4:
                localctx = qutes_parser.DoWhileStatementContext(self, localctx)
                self.enterOuterAlt(localctx, 4)
                self.state = 62
                self.match(qutes_parser.DO_STATEMENT)
                self.state = 63
                self.statement()
                self.state = 64
                self.match(qutes_parser.WHILE_STATEMENT)
                self.state = 65
                self.expr(0)
                pass

            elif la_ == 5:
                localctx = qutes_parser.BlockStatementContext(self, localctx)
                self.enterOuterAlt(localctx, 5)
                self.state = 67
                self.match(qutes_parser.CURLY_PARENTHESIS_OPEN)
                self.state = 71
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while (((_la) & ~0x3f) == 0 and ((1 << _la) & 209453393821361150) != 0) or ((((_la - 64)) & ~0x3f) == 0 and ((1 << (_la - 64)) & 1023) != 0):
                    self.state = 68
                    self.statement()
                    self.state = 73
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 74
                self.match(qutes_parser.CURLY_PARENTHESIS_CLOSE)
                pass

            elif la_ == 6:
                localctx = qutes_parser.FunctionStatementContext(self, localctx)
                self.enterOuterAlt(localctx, 6)
                self.state = 75
                self.variableType()
                self.state = 76
                self.functionName()
                self.state = 77
                self.match(qutes_parser.ROUND_PARENTHESIS_OPEN)
                self.state = 79
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if (((_la) & ~0x3f) == 0 and ((1 << _la) & 510) != 0) or _la==72:
                    self.state = 78
                    self.functionDeclarationParams()


                self.state = 81
                self.match(qutes_parser.ROUND_PARENTHESIS_CLOSE)
                self.state = 82
                self.statement()
                pass

            elif la_ == 7:
                localctx = qutes_parser.DeclarationStatementContext(self, localctx)
                self.enterOuterAlt(localctx, 7)
                self.state = 84
                self.variableDeclaration()
                self.state = 85
                self.match(qutes_parser.END_OF_STATEMENT)
                pass

            elif la_ == 8:
                localctx = qutes_parser.AssignmentStatementContext(self, localctx)
                self.enterOuterAlt(localctx, 8)
                self.state = 87
                self.qualifiedName()
                self.state = 88
                self.match(qutes_parser.ASSIGN)
                self.state = 89
                self.expr(0)
                self.state = 90
                self.match(qutes_parser.END_OF_STATEMENT)
                pass

            elif la_ == 9:
                localctx = qutes_parser.ReturnStatementContext(self, localctx)
                self.enterOuterAlt(localctx, 9)
                self.state = 92
                self.match(qutes_parser.RETURN)
                self.state = 93
                self.expr(0)
                self.state = 94
                self.match(qutes_parser.END_OF_STATEMENT)
                pass

            elif la_ == 10:
                localctx = qutes_parser.ExpressionStatementContext(self, localctx)
                self.enterOuterAlt(localctx, 10)
                self.state = 96
                self.expr(0)
                self.state = 97
                self.match(qutes_parser.END_OF_STATEMENT)
                pass

            elif la_ == 11:
                localctx = qutes_parser.FactStatementContext(self, localctx)
                self.enterOuterAlt(localctx, 11)
                self.state = 99
                _la = self._input.LA(1)
                if not(_la==28 or _la==30):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                pass

            elif la_ == 12:
                localctx = qutes_parser.EmptyStatementContext(self, localctx)
                self.enterOuterAlt(localctx, 12)
                self.state = 100
                self.match(qutes_parser.END_OF_STATEMENT)
                pass


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
        self.enterRule(localctx, 4, self.RULE_functionDeclarationParams)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 103
            self.variableDeclaration()
            self.state = 106
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==63:
                self.state = 104
                self.match(qutes_parser.COMMA)
                self.state = 105
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
        self.enterRule(localctx, 6, self.RULE_variableDeclaration)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 108
            self.variableType()
            self.state = 109
            self.variableName()
            self.state = 112
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==37:
                self.state = 110
                self.match(qutes_parser.ASSIGN)
                self.state = 111
                self.expr(0)


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


        def getRuleIndex(self):
            return qutes_parser.RULE_expr

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)


    class QualifiedNameExpressionContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a qutes_parser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def qualifiedName(self):
            return self.getTypedRuleContext(qutes_parser.QualifiedNameContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterQualifiedNameExpression" ):
                listener.enterQualifiedNameExpression(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitQualifiedNameExpression" ):
                listener.exitQualifiedNameExpression(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitQualifiedNameExpression" ):
                return visitor.visitQualifiedNameExpression(self)
            else:
                return visitor.visitChildren(self)


    class RelationalOperatorContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a qutes_parser.ExprContext
            super().__init__(parser)
            self.op = None # Token
            self.copyFrom(ctx)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(qutes_parser.ExprContext)
            else:
                return self.getTypedRuleContext(qutes_parser.ExprContext,i)

        def GREATEREQUAL(self):
            return self.getToken(qutes_parser.GREATEREQUAL, 0)
        def LOWEREQUAL(self):
            return self.getToken(qutes_parser.LOWEREQUAL, 0)
        def GREATER(self):
            return self.getToken(qutes_parser.GREATER, 0)
        def LOWER(self):
            return self.getToken(qutes_parser.LOWER, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterRelationalOperator" ):
                listener.enterRelationalOperator(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitRelationalOperator" ):
                listener.exitRelationalOperator(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitRelationalOperator" ):
                return visitor.visitRelationalOperator(self)
            else:
                return visitor.visitChildren(self)


    class LogicAndOperatorContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a qutes_parser.ExprContext
            super().__init__(parser)
            self.op = None # Token
            self.copyFrom(ctx)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(qutes_parser.ExprContext)
            else:
                return self.getTypedRuleContext(qutes_parser.ExprContext,i)

        def AND(self):
            return self.getToken(qutes_parser.AND, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterLogicAndOperator" ):
                listener.enterLogicAndOperator(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitLogicAndOperator" ):
                listener.exitLogicAndOperator(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitLogicAndOperator" ):
                return visitor.visitLogicAndOperator(self)
            else:
                return visitor.visitChildren(self)


    class PrefixOperatorContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a qutes_parser.ExprContext
            super().__init__(parser)
            self.op = None # Token
            self.copyFrom(ctx)

        def expr(self):
            return self.getTypedRuleContext(qutes_parser.ExprContext,0)

        def NOT(self):
            return self.getToken(qutes_parser.NOT, 0)
        def ADD(self):
            return self.getToken(qutes_parser.ADD, 0)
        def SUB(self):
            return self.getToken(qutes_parser.SUB, 0)
        def AUTO_INCREMENT(self):
            return self.getToken(qutes_parser.AUTO_INCREMENT, 0)
        def AUTO_DECREMENT(self):
            return self.getToken(qutes_parser.AUTO_DECREMENT, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPrefixOperator" ):
                listener.enterPrefixOperator(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPrefixOperator" ):
                listener.exitPrefixOperator(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPrefixOperator" ):
                return visitor.visitPrefixOperator(self)
            else:
                return visitor.visitChildren(self)


    class LiteralExpressionContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a qutes_parser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def literal(self):
            return self.getTypedRuleContext(qutes_parser.LiteralContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterLiteralExpression" ):
                listener.enterLiteralExpression(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitLiteralExpression" ):
                listener.exitLiteralExpression(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitLiteralExpression" ):
                return visitor.visitLiteralExpression(self)
            else:
                return visitor.visitChildren(self)


    class GroverOperatorContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a qutes_parser.ExprContext
            super().__init__(parser)
            self.op = None # Token
            self.copyFrom(ctx)

        def termList(self):
            return self.getTypedRuleContext(qutes_parser.TermListContext,0)

        def qualifiedName(self):
            return self.getTypedRuleContext(qutes_parser.QualifiedNameContext,0)

        def IN_STATEMENT(self):
            return self.getToken(qutes_parser.IN_STATEMENT, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterGroverOperator" ):
                listener.enterGroverOperator(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitGroverOperator" ):
                listener.exitGroverOperator(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitGroverOperator" ):
                return visitor.visitGroverOperator(self)
            else:
                return visitor.visitChildren(self)


    class FunctionCallExpressionContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a qutes_parser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def functionName(self):
            return self.getTypedRuleContext(qutes_parser.FunctionNameContext,0)

        def ROUND_PARENTHESIS_OPEN(self):
            return self.getToken(qutes_parser.ROUND_PARENTHESIS_OPEN, 0)
        def ROUND_PARENTHESIS_CLOSE(self):
            return self.getToken(qutes_parser.ROUND_PARENTHESIS_CLOSE, 0)
        def functionCallParams(self):
            return self.getTypedRuleContext(qutes_parser.FunctionCallParamsContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFunctionCallExpression" ):
                listener.enterFunctionCallExpression(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFunctionCallExpression" ):
                listener.exitFunctionCallExpression(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFunctionCallExpression" ):
                return visitor.visitFunctionCallExpression(self)
            else:
                return visitor.visitChildren(self)


    class EqualityOperatorContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a qutes_parser.ExprContext
            super().__init__(parser)
            self.op = None # Token
            self.copyFrom(ctx)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(qutes_parser.ExprContext)
            else:
                return self.getTypedRuleContext(qutes_parser.ExprContext,i)

        def EQUAL(self):
            return self.getToken(qutes_parser.EQUAL, 0)
        def NOT_EQUAL(self):
            return self.getToken(qutes_parser.NOT_EQUAL, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterEqualityOperator" ):
                listener.enterEqualityOperator(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitEqualityOperator" ):
                listener.exitEqualityOperator(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitEqualityOperator" ):
                return visitor.visitEqualityOperator(self)
            else:
                return visitor.visitChildren(self)


    class MultipleUnaryOperatorContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a qutes_parser.ExprContext
            super().__init__(parser)
            self.op = None # Token
            self.copyFrom(ctx)

        def termList(self):
            return self.getTypedRuleContext(qutes_parser.TermListContext,0)

        def MCX(self):
            return self.getToken(qutes_parser.MCX, 0)
        def MCZ(self):
            return self.getToken(qutes_parser.MCZ, 0)
        def MCY(self):
            return self.getToken(qutes_parser.MCY, 0)
        def SWAP(self):
            return self.getToken(qutes_parser.SWAP, 0)

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


    class SumOperatorContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a qutes_parser.ExprContext
            super().__init__(parser)
            self.op = None # Token
            self.copyFrom(ctx)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(qutes_parser.ExprContext)
            else:
                return self.getTypedRuleContext(qutes_parser.ExprContext,i)

        def ADD(self):
            return self.getToken(qutes_parser.ADD, 0)
        def SUB(self):
            return self.getToken(qutes_parser.SUB, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSumOperator" ):
                listener.enterSumOperator(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSumOperator" ):
                listener.exitSumOperator(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSumOperator" ):
                return visitor.visitSumOperator(self)
            else:
                return visitor.visitChildren(self)


    class PostfixOperatorContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a qutes_parser.ExprContext
            super().__init__(parser)
            self.op = None # Token
            self.copyFrom(ctx)

        def expr(self):
            return self.getTypedRuleContext(qutes_parser.ExprContext,0)

        def AUTO_INCREMENT(self):
            return self.getToken(qutes_parser.AUTO_INCREMENT, 0)
        def AUTO_DECREMENT(self):
            return self.getToken(qutes_parser.AUTO_DECREMENT, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPostfixOperator" ):
                listener.enterPostfixOperator(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPostfixOperator" ):
                listener.exitPostfixOperator(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPostfixOperator" ):
                return visitor.visitPostfixOperator(self)
            else:
                return visitor.visitChildren(self)


    class ParentesizeExpressionContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a qutes_parser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def ROUND_PARENTHESIS_OPEN(self):
            return self.getToken(qutes_parser.ROUND_PARENTHESIS_OPEN, 0)
        def expr(self):
            return self.getTypedRuleContext(qutes_parser.ExprContext,0)

        def ROUND_PARENTHESIS_CLOSE(self):
            return self.getToken(qutes_parser.ROUND_PARENTHESIS_CLOSE, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterParentesizeExpression" ):
                listener.enterParentesizeExpression(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitParentesizeExpression" ):
                listener.exitParentesizeExpression(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitParentesizeExpression" ):
                return visitor.visitParentesizeExpression(self)
            else:
                return visitor.visitChildren(self)


    class MultipleUnaryPhaseOperatorContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a qutes_parser.ExprContext
            super().__init__(parser)
            self.op = None # Token
            self.copyFrom(ctx)

        def termList(self):
            return self.getTypedRuleContext(qutes_parser.TermListContext,0)

        def BY(self):
            return self.getToken(qutes_parser.BY, 0)
        def expr(self):
            return self.getTypedRuleContext(qutes_parser.ExprContext,0)

        def MCP(self):
            return self.getToken(qutes_parser.MCP, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterMultipleUnaryPhaseOperator" ):
                listener.enterMultipleUnaryPhaseOperator(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitMultipleUnaryPhaseOperator" ):
                listener.exitMultipleUnaryPhaseOperator(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitMultipleUnaryPhaseOperator" ):
                return visitor.visitMultipleUnaryPhaseOperator(self)
            else:
                return visitor.visitChildren(self)


    class MultiplicativeOperatorContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a qutes_parser.ExprContext
            super().__init__(parser)
            self.op = None # Token
            self.copyFrom(ctx)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(qutes_parser.ExprContext)
            else:
                return self.getTypedRuleContext(qutes_parser.ExprContext,i)

        def MULTIPLY(self):
            return self.getToken(qutes_parser.MULTIPLY, 0)
        def DIVIDE(self):
            return self.getToken(qutes_parser.DIVIDE, 0)
        def MODULE(self):
            return self.getToken(qutes_parser.MODULE, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterMultiplicativeOperator" ):
                listener.enterMultiplicativeOperator(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitMultiplicativeOperator" ):
                listener.exitMultiplicativeOperator(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitMultiplicativeOperator" ):
                return visitor.visitMultiplicativeOperator(self)
            else:
                return visitor.visitChildren(self)


    class UnaryOperatorContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a qutes_parser.ExprContext
            super().__init__(parser)
            self.op = None # Token
            self.copyFrom(ctx)

        def expr(self):
            return self.getTypedRuleContext(qutes_parser.ExprContext,0)

        def PRINT(self):
            return self.getToken(qutes_parser.PRINT, 0)
        def PAULIY(self):
            return self.getToken(qutes_parser.PAULIY, 0)
        def PAULIZ(self):
            return self.getToken(qutes_parser.PAULIZ, 0)
        def HADAMARD(self):
            return self.getToken(qutes_parser.HADAMARD, 0)
        def MEASURE(self):
            return self.getToken(qutes_parser.MEASURE, 0)

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


    class LogicOrOperatorContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a qutes_parser.ExprContext
            super().__init__(parser)
            self.op = None # Token
            self.copyFrom(ctx)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(qutes_parser.ExprContext)
            else:
                return self.getTypedRuleContext(qutes_parser.ExprContext,i)

        def OR(self):
            return self.getToken(qutes_parser.OR, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterLogicOrOperator" ):
                listener.enterLogicOrOperator(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitLogicOrOperator" ):
                listener.exitLogicOrOperator(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitLogicOrOperator" ):
                return visitor.visitLogicOrOperator(self)
            else:
                return visitor.visitChildren(self)



    def expr(self, _p:int=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = qutes_parser.ExprContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 8
        self.enterRecursionRule(localctx, 8, self.RULE_expr, _p)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 143
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,7,self._ctx)
            if la_ == 1:
                localctx = qutes_parser.ParentesizeExpressionContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx

                self.state = 115
                self.match(qutes_parser.ROUND_PARENTHESIS_OPEN)
                self.state = 116
                self.expr(0)
                self.state = 117
                self.match(qutes_parser.ROUND_PARENTHESIS_CLOSE)
                pass

            elif la_ == 2:
                localctx = qutes_parser.LiteralExpressionContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 119
                self.literal()
                pass

            elif la_ == 3:
                localctx = qutes_parser.QualifiedNameExpressionContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 120
                self.qualifiedName()
                pass

            elif la_ == 4:
                localctx = qutes_parser.FunctionCallExpressionContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 121
                self.functionName()
                self.state = 122
                self.match(qutes_parser.ROUND_PARENTHESIS_OPEN)
                self.state = 124
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if ((((_la - 64)) & ~0x3f) == 0 and ((1 << (_la - 64)) & 1023) != 0):
                    self.state = 123
                    self.functionCallParams()


                self.state = 126
                self.match(qutes_parser.ROUND_PARENTHESIS_CLOSE)
                pass

            elif la_ == 5:
                localctx = qutes_parser.PrefixOperatorContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 128
                localctx.op = self._input.LT(1)
                _la = self._input.LA(1)
                if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 824633778176) != 0)):
                    localctx.op = self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 129
                self.expr(11)
                pass

            elif la_ == 6:
                localctx = qutes_parser.MultipleUnaryOperatorContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 130
                localctx.op = self._input.LT(1)
                _la = self._input.LA(1)
                if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 59244544) != 0)):
                    localctx.op = self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 131
                self.termList()
                pass

            elif la_ == 7:
                localctx = qutes_parser.UnaryOperatorContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 132
                localctx.op = self._input.LT(1)
                _la = self._input.LA(1)
                if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 942669824) != 0)):
                    localctx.op = self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 133
                self.expr(3)
                pass

            elif la_ == 8:
                localctx = qutes_parser.MultipleUnaryPhaseOperatorContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 134
                localctx.op = self.match(qutes_parser.MCP)
                self.state = 135
                self.termList()
                self.state = 136
                self.match(qutes_parser.BY)
                self.state = 137
                self.expr(2)
                pass

            elif la_ == 9:
                localctx = qutes_parser.GroverOperatorContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 139
                self.termList()
                self.state = 140
                localctx.op = self.match(qutes_parser.IN_STATEMENT)
                self.state = 141
                self.qualifiedName()
                pass


            self._ctx.stop = self._input.LT(-1)
            self.state = 167
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,9,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    self.state = 165
                    self._errHandler.sync(self)
                    la_ = self._interp.adaptivePredict(self._input,8,self._ctx)
                    if la_ == 1:
                        localctx = qutes_parser.MultiplicativeOperatorContext(self, qutes_parser.ExprContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 145
                        if not self.precpred(self._ctx, 10):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 10)")
                        self.state = 146
                        localctx.op = self._input.LT(1)
                        _la = self._input.LA(1)
                        if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 7168) != 0)):
                            localctx.op = self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 147
                        self.expr(11)
                        pass

                    elif la_ == 2:
                        localctx = qutes_parser.SumOperatorContext(self, qutes_parser.ExprContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 148
                        if not self.precpred(self._ctx, 9):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 9)")
                        self.state = 149
                        localctx.op = self._input.LT(1)
                        _la = self._input.LA(1)
                        if not(_la==13 or _la==14):
                            localctx.op = self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 150
                        self.expr(10)
                        pass

                    elif la_ == 3:
                        localctx = qutes_parser.RelationalOperatorContext(self, qutes_parser.ExprContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 151
                        if not self.precpred(self._ctx, 8):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 8)")
                        self.state = 152
                        localctx.op = self._input.LT(1)
                        _la = self._input.LA(1)
                        if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 128849018880) != 0)):
                            localctx.op = self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 153
                        self.expr(9)
                        pass

                    elif la_ == 4:
                        localctx = qutes_parser.EqualityOperatorContext(self, qutes_parser.ExprContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 154
                        if not self.precpred(self._ctx, 7):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 7)")
                        self.state = 155
                        localctx.op = self._input.LT(1)
                        _la = self._input.LA(1)
                        if not(_la==31 or _la==32):
                            localctx.op = self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 156
                        self.expr(8)
                        pass

                    elif la_ == 5:
                        localctx = qutes_parser.LogicAndOperatorContext(self, qutes_parser.ExprContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 157
                        if not self.precpred(self._ctx, 6):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 6)")
                        self.state = 158
                        localctx.op = self.match(qutes_parser.AND)
                        self.state = 159
                        self.expr(7)
                        pass

                    elif la_ == 6:
                        localctx = qutes_parser.LogicOrOperatorContext(self, qutes_parser.ExprContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 160
                        if not self.precpred(self._ctx, 5):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 5)")
                        self.state = 161
                        localctx.op = self.match(qutes_parser.OR)
                        self.state = 162
                        self.expr(6)
                        pass

                    elif la_ == 7:
                        localctx = qutes_parser.PostfixOperatorContext(self, qutes_parser.ExprContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 163
                        if not self.precpred(self._ctx, 12):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 12)")
                        self.state = 164
                        localctx.op = self._input.LT(1)
                        _la = self._input.LA(1)
                        if not(_la==38 or _la==39):
                            localctx.op = self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        pass

             
                self.state = 169
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,9,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.unrollRecursionContexts(_parentctx)
        return localctx


    class FunctionCallParamsContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def literal(self):
            return self.getTypedRuleContext(qutes_parser.LiteralContext,0)


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
            self.state = 172
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [64, 65, 66, 67, 68, 69, 70, 71, 73]:
                self.state = 170
                self.literal()
                pass
            elif token in [72]:
                self.state = 171
                self.qualifiedName()
                pass
            else:
                raise NoViableAltException(self)

            self.state = 176
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==63:
                self.state = 174
                self.match(qutes_parser.COMMA)
                self.state = 175
                self.functionCallParams()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class TermListContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def literal(self):
            return self.getTypedRuleContext(qutes_parser.LiteralContext,0)


        def qualifiedName(self):
            return self.getTypedRuleContext(qutes_parser.QualifiedNameContext,0)


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
        self.enterRule(localctx, 12, self.RULE_termList)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 180
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [64, 65, 66, 67, 68, 69, 70, 71, 73]:
                self.state = 178
                self.literal()
                pass
            elif token in [72]:
                self.state = 179
                self.qualifiedName()
                pass
            else:
                raise NoViableAltException(self)

            self.state = 184
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,13,self._ctx)
            if la_ == 1:
                self.state = 182
                self.match(qutes_parser.COMMA)
                self.state = 183
                self.termList()


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
            self.state = 188
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [1, 2, 3, 4, 5, 6, 7, 8]:
                self.enterOuterAlt(localctx, 1)
                self.state = 186
                self.type_()
                pass
            elif token in [72]:
                self.enterOuterAlt(localctx, 2)
                self.state = 187
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
        self.enterRule(localctx, 16, self.RULE_type)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 190
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

        def variableName(self):
            return self.getTypedRuleContext(qutes_parser.VariableNameContext,0)


        def functionName(self):
            return self.getTypedRuleContext(qutes_parser.FunctionNameContext,0)


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
        self.enterRule(localctx, 18, self.RULE_qualifiedName)
        try:
            self.state = 202
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,16,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 192
                self.match(qutes_parser.SYMBOL_LITERAL)
                self.state = 197
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,15,self._ctx)
                while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                    if _alt==1:
                        self.state = 193
                        self.match(qutes_parser.DOT)
                        self.state = 194
                        self.match(qutes_parser.SYMBOL_LITERAL) 
                    self.state = 199
                    self._errHandler.sync(self)
                    _alt = self._interp.adaptivePredict(self._input,15,self._ctx)

                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 200
                self.variableName()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 201
                self.functionName()
                pass


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
        self.enterRule(localctx, 20, self.RULE_variableName)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 204
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
        self.enterRule(localctx, 22, self.RULE_functionName)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 206
            self.match(qutes_parser.SYMBOL_LITERAL)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class LiteralContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

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


        def string(self):
            return self.getTypedRuleContext(qutes_parser.StringContext,0)


        def getRuleIndex(self):
            return qutes_parser.RULE_literal

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterLiteral" ):
                listener.enterLiteral(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitLiteral" ):
                listener.exitLiteral(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitLiteral" ):
                return visitor.visitLiteral(self)
            else:
                return visitor.visitChildren(self)




    def literal(self):

        localctx = qutes_parser.LiteralContext(self, self._ctx, self.state)
        self.enterRule(localctx, 24, self.RULE_literal)
        try:
            self.state = 215
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [64]:
                self.enterOuterAlt(localctx, 1)
                self.state = 208
                self.boolean()
                pass
            elif token in [65, 67, 68]:
                self.enterOuterAlt(localctx, 2)
                self.state = 209
                self.integer()
                pass
            elif token in [66]:
                self.enterOuterAlt(localctx, 3)
                self.state = 210
                self.float_()
                pass
            elif token in [69]:
                self.enterOuterAlt(localctx, 4)
                self.state = 211
                self.qubit()
                pass
            elif token in [70]:
                self.enterOuterAlt(localctx, 5)
                self.state = 212
                self.quint()
                pass
            elif token in [71]:
                self.enterOuterAlt(localctx, 6)
                self.state = 213
                self.qustring()
                pass
            elif token in [73]:
                self.enterOuterAlt(localctx, 7)
                self.state = 214
                self.string()
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
        self.enterRule(localctx, 26, self.RULE_string)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 217
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
        self.enterRule(localctx, 28, self.RULE_qubit)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 219
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
        self.enterRule(localctx, 30, self.RULE_quint)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 221
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
        self.enterRule(localctx, 32, self.RULE_qustring)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 223
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
        self.enterRule(localctx, 34, self.RULE_float)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 225
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
        self.enterRule(localctx, 36, self.RULE_integer)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 227
            _la = self._input.LA(1)
            if not(((((_la - 65)) & ~0x3f) == 0 and ((1 << (_la - 65)) & 13) != 0)):
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
        self.enterRule(localctx, 38, self.RULE_boolean)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 229
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
        self._predicates[4] = self.expr_sempred
        pred = self._predicates.get(ruleIndex, None)
        if pred is None:
            raise Exception("No predicate with index:" + str(ruleIndex))
        else:
            return pred(localctx, predIndex)

    def expr_sempred(self, localctx:ExprContext, predIndex:int):
            if predIndex == 0:
                return self.precpred(self._ctx, 10)
         

            if predIndex == 1:
                return self.precpred(self._ctx, 9)
         

            if predIndex == 2:
                return self.precpred(self._ctx, 8)
         

            if predIndex == 3:
                return self.precpred(self._ctx, 7)
         

            if predIndex == 4:
                return self.precpred(self._ctx, 6)
         

            if predIndex == 5:
                return self.precpred(self._ctx, 5)
         

            if predIndex == 6:
                return self.precpred(self._ctx, 12)
         




