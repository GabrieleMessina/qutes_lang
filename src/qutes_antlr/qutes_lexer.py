# Generated from /workspaces/qutes_lang/specification/grammar/qutes_lexer.g4 by ANTLR 4.13.1
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
    from typing import TextIO
else:
    from typing.io import TextIO


def serializedATN():
    return [
        4,0,27,175,6,-1,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,
        2,6,7,6,2,7,7,7,2,8,7,8,2,9,7,9,2,10,7,10,2,11,7,11,2,12,7,12,2,
        13,7,13,2,14,7,14,2,15,7,15,2,16,7,16,2,17,7,17,2,18,7,18,2,19,7,
        19,2,20,7,20,2,21,7,21,2,22,7,22,2,23,7,23,2,24,7,24,2,25,7,25,2,
        26,7,26,2,27,7,27,1,0,1,0,1,0,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,
        2,1,2,1,2,1,2,1,2,1,2,1,3,1,3,1,4,1,4,1,5,1,5,1,5,1,6,1,6,1,7,1,
        7,1,7,1,8,1,8,1,9,1,9,1,9,1,10,1,10,1,11,1,11,1,12,1,12,1,12,1,12,
        1,13,1,13,1,13,1,14,1,14,1,14,1,14,1,14,1,15,1,15,1,15,1,15,1,15,
        1,15,1,16,1,16,1,16,1,17,1,17,1,18,1,18,1,19,1,19,1,20,1,20,1,21,
        1,21,1,22,1,22,1,23,1,23,1,23,1,23,5,23,133,8,23,10,23,12,23,136,
        9,23,1,23,1,23,1,23,1,23,1,23,1,23,5,23,144,8,23,10,23,12,23,147,
        9,23,3,23,149,8,23,1,24,4,24,152,8,24,11,24,12,24,153,1,25,4,25,
        157,8,25,11,25,12,25,158,1,26,4,26,162,8,26,11,26,12,26,163,1,26,
        3,26,167,8,26,1,26,1,26,1,27,3,27,172,8,27,1,27,1,27,1,134,0,28,
        1,1,3,2,5,3,7,4,9,5,11,6,13,7,15,8,17,9,19,10,21,11,23,12,25,13,
        27,14,29,15,31,16,33,17,35,18,37,19,39,20,41,21,43,22,45,23,47,0,
        49,24,51,25,53,26,55,27,1,0,22,2,0,73,73,105,105,2,0,78,78,110,110,
        2,0,84,84,116,116,2,0,83,83,115,115,2,0,82,82,114,114,2,0,71,71,
        103,103,2,0,81,81,113,113,2,0,85,85,117,117,2,0,66,66,98,98,2,0,
        86,86,118,118,2,0,65,65,97,97,2,0,70,70,102,102,2,0,69,69,101,101,
        2,0,76,76,108,108,2,0,87,87,119,119,2,0,72,72,104,104,2,0,68,68,
        100,100,2,0,79,79,111,111,2,0,10,10,13,13,1,0,48,57,2,0,65,90,97,
        122,3,0,9,10,13,13,32,32,181,0,1,1,0,0,0,0,3,1,0,0,0,0,5,1,0,0,0,
        0,7,1,0,0,0,0,9,1,0,0,0,0,11,1,0,0,0,0,13,1,0,0,0,0,15,1,0,0,0,0,
        17,1,0,0,0,0,19,1,0,0,0,0,21,1,0,0,0,0,23,1,0,0,0,0,25,1,0,0,0,0,
        27,1,0,0,0,0,29,1,0,0,0,0,31,1,0,0,0,0,33,1,0,0,0,0,35,1,0,0,0,0,
        37,1,0,0,0,0,39,1,0,0,0,0,41,1,0,0,0,0,43,1,0,0,0,0,45,1,0,0,0,0,
        49,1,0,0,0,0,51,1,0,0,0,0,53,1,0,0,0,0,55,1,0,0,0,1,57,1,0,0,0,3,
        61,1,0,0,0,5,68,1,0,0,0,7,74,1,0,0,0,9,76,1,0,0,0,11,78,1,0,0,0,
        13,81,1,0,0,0,15,83,1,0,0,0,17,86,1,0,0,0,19,88,1,0,0,0,21,91,1,
        0,0,0,23,93,1,0,0,0,25,95,1,0,0,0,27,99,1,0,0,0,29,102,1,0,0,0,31,
        107,1,0,0,0,33,113,1,0,0,0,35,116,1,0,0,0,37,118,1,0,0,0,39,120,
        1,0,0,0,41,122,1,0,0,0,43,124,1,0,0,0,45,126,1,0,0,0,47,148,1,0,
        0,0,49,151,1,0,0,0,51,156,1,0,0,0,53,166,1,0,0,0,55,171,1,0,0,0,
        57,58,7,0,0,0,58,59,7,1,0,0,59,60,7,2,0,0,60,2,1,0,0,0,61,62,7,3,
        0,0,62,63,7,2,0,0,63,64,7,4,0,0,64,65,7,0,0,0,65,66,7,1,0,0,66,67,
        7,5,0,0,67,4,1,0,0,0,68,69,7,6,0,0,69,70,7,7,0,0,70,71,7,8,0,0,71,
        72,7,0,0,0,72,73,7,2,0,0,73,6,1,0,0,0,74,75,5,43,0,0,75,8,1,0,0,
        0,76,77,5,45,0,0,77,10,1,0,0,0,78,79,5,61,0,0,79,80,5,61,0,0,80,
        12,1,0,0,0,81,82,5,62,0,0,82,14,1,0,0,0,83,84,5,62,0,0,84,85,5,61,
        0,0,85,16,1,0,0,0,86,87,5,60,0,0,87,18,1,0,0,0,88,89,5,60,0,0,89,
        90,5,61,0,0,90,20,1,0,0,0,91,92,5,61,0,0,92,22,1,0,0,0,93,94,5,59,
        0,0,94,24,1,0,0,0,95,96,7,9,0,0,96,97,7,10,0,0,97,98,7,4,0,0,98,
        26,1,0,0,0,99,100,7,0,0,0,100,101,7,11,0,0,101,28,1,0,0,0,102,103,
        7,12,0,0,103,104,7,13,0,0,104,105,7,3,0,0,105,106,7,12,0,0,106,30,
        1,0,0,0,107,108,7,14,0,0,108,109,7,15,0,0,109,110,7,0,0,0,110,111,
        7,13,0,0,111,112,7,12,0,0,112,32,1,0,0,0,113,114,7,16,0,0,114,115,
        7,17,0,0,115,34,1,0,0,0,116,117,5,123,0,0,117,36,1,0,0,0,118,119,
        5,125,0,0,119,38,1,0,0,0,120,121,5,40,0,0,121,40,1,0,0,0,122,123,
        5,41,0,0,123,42,1,0,0,0,124,125,5,46,0,0,125,44,1,0,0,0,126,127,
        5,34,0,0,127,46,1,0,0,0,128,129,5,47,0,0,129,130,5,42,0,0,130,134,
        1,0,0,0,131,133,9,0,0,0,132,131,1,0,0,0,133,136,1,0,0,0,134,135,
        1,0,0,0,134,132,1,0,0,0,135,137,1,0,0,0,136,134,1,0,0,0,137,138,
        5,42,0,0,138,149,5,47,0,0,139,140,5,47,0,0,140,141,5,47,0,0,141,
        145,1,0,0,0,142,144,8,18,0,0,143,142,1,0,0,0,144,147,1,0,0,0,145,
        143,1,0,0,0,145,146,1,0,0,0,146,149,1,0,0,0,147,145,1,0,0,0,148,
        128,1,0,0,0,148,139,1,0,0,0,149,48,1,0,0,0,150,152,7,19,0,0,151,
        150,1,0,0,0,152,153,1,0,0,0,153,151,1,0,0,0,153,154,1,0,0,0,154,
        50,1,0,0,0,155,157,7,20,0,0,156,155,1,0,0,0,157,158,1,0,0,0,158,
        156,1,0,0,0,158,159,1,0,0,0,159,52,1,0,0,0,160,162,7,21,0,0,161,
        160,1,0,0,0,162,163,1,0,0,0,163,161,1,0,0,0,163,164,1,0,0,0,164,
        167,1,0,0,0,165,167,3,47,23,0,166,161,1,0,0,0,166,165,1,0,0,0,167,
        168,1,0,0,0,168,169,6,26,0,0,169,54,1,0,0,0,170,172,5,13,0,0,171,
        170,1,0,0,0,171,172,1,0,0,0,172,173,1,0,0,0,173,174,5,10,0,0,174,
        56,1,0,0,0,9,0,134,145,148,153,158,163,166,171,1,6,0,0
    ]

class qutes_lexer(Lexer):

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    INT_TYPE = 1
    STRING_TYPE = 2
    QUBIT_TYPE = 3
    ADD = 4
    SUB = 5
    EQUAL = 6
    GREATER = 7
    GREATEREQUAL = 8
    LOWER = 9
    LOWEREQUAL = 10
    ASSIGN = 11
    END_OF_STATEMENT = 12
    VAR_STATEMENT = 13
    IF_STATEMENT = 14
    ELSE_STATEMENT = 15
    WHILE_STATEMENT = 16
    DO_STATEMENT = 17
    CURLY_PARENTHESIS_OPEN = 18
    CURLY_PARENTHESIS_CLOSE = 19
    ROUND_PARENTHESIS_OPEN = 20
    ROUND_PARENTHESIS_CLOSE = 21
    DOT = 22
    STRING_ENCLOSURE = 23
    INT = 24
    STRING = 25
    WS = 26
    NEWLINE = 27

    channelNames = [ u"DEFAULT_TOKEN_CHANNEL", u"HIDDEN" ]

    modeNames = [ "DEFAULT_MODE" ]

    literalNames = [ "<INVALID>",
            "'int'", "'string'", "'qubit'", "'+'", "'-'", "'=='", "'>'", 
            "'>='", "'<'", "'<='", "'='", "';'", "'var'", "'if'", "'else'", 
            "'while'", "'do'", "'{'", "'}'", "'('", "')'", "'.'", "'\"'" ]

    symbolicNames = [ "<INVALID>",
            "INT_TYPE", "STRING_TYPE", "QUBIT_TYPE", "ADD", "SUB", "EQUAL", 
            "GREATER", "GREATEREQUAL", "LOWER", "LOWEREQUAL", "ASSIGN", 
            "END_OF_STATEMENT", "VAR_STATEMENT", "IF_STATEMENT", "ELSE_STATEMENT", 
            "WHILE_STATEMENT", "DO_STATEMENT", "CURLY_PARENTHESIS_OPEN", 
            "CURLY_PARENTHESIS_CLOSE", "ROUND_PARENTHESIS_OPEN", "ROUND_PARENTHESIS_CLOSE", 
            "DOT", "STRING_ENCLOSURE", "INT", "STRING", "WS", "NEWLINE" ]

    ruleNames = [ "INT_TYPE", "STRING_TYPE", "QUBIT_TYPE", "ADD", "SUB", 
                  "EQUAL", "GREATER", "GREATEREQUAL", "LOWER", "LOWEREQUAL", 
                  "ASSIGN", "END_OF_STATEMENT", "VAR_STATEMENT", "IF_STATEMENT", 
                  "ELSE_STATEMENT", "WHILE_STATEMENT", "DO_STATEMENT", "CURLY_PARENTHESIS_OPEN", 
                  "CURLY_PARENTHESIS_CLOSE", "ROUND_PARENTHESIS_OPEN", "ROUND_PARENTHESIS_CLOSE", 
                  "DOT", "STRING_ENCLOSURE", "COMMENT", "INT", "STRING", 
                  "WS", "NEWLINE" ]

    grammarFileName = "qutes_lexer.g4"

    def __init__(self, input=None, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.1")
        self._interp = LexerATNSimulator(self, self.atn, self.decisionsToDFA, PredictionContextCache())
        self._actions = None
        self._predicates = None


