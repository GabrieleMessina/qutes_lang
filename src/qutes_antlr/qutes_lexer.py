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
        4,0,46,458,6,-1,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,
        2,6,7,6,2,7,7,7,2,8,7,8,2,9,7,9,2,10,7,10,2,11,7,11,2,12,7,12,2,
        13,7,13,2,14,7,14,2,15,7,15,2,16,7,16,2,17,7,17,2,18,7,18,2,19,7,
        19,2,20,7,20,2,21,7,21,2,22,7,22,2,23,7,23,2,24,7,24,2,25,7,25,2,
        26,7,26,2,27,7,27,2,28,7,28,2,29,7,29,2,30,7,30,2,31,7,31,2,32,7,
        32,2,33,7,33,2,34,7,34,2,35,7,35,2,36,7,36,2,37,7,37,2,38,7,38,2,
        39,7,39,2,40,7,40,2,41,7,41,2,42,7,42,2,43,7,43,2,44,7,44,2,45,7,
        45,2,46,7,46,2,47,7,47,2,48,7,48,2,49,7,49,2,50,7,50,2,51,7,51,1,
        0,1,0,1,0,1,0,1,1,1,1,1,1,1,1,1,1,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,
        3,1,3,1,3,1,3,1,3,1,3,1,4,1,4,1,4,1,4,1,4,1,4,1,5,1,5,1,5,1,5,1,
        5,1,5,1,6,1,6,1,7,1,7,1,8,1,8,1,8,1,8,1,9,1,9,1,9,1,9,1,9,1,9,1,
        9,1,10,1,10,1,10,1,10,1,10,1,10,1,10,1,11,1,11,1,11,1,11,1,11,1,
        11,1,11,1,11,1,11,1,12,1,12,1,12,1,12,1,12,1,12,1,12,1,12,1,13,1,
        13,1,13,1,13,1,13,1,13,1,14,1,14,1,14,1,15,1,15,1,16,1,16,1,16,1,
        17,1,17,1,18,1,18,1,18,1,19,1,19,1,20,1,20,1,21,1,21,1,21,1,21,1,
        22,1,22,1,22,1,23,1,23,1,23,1,23,1,23,1,24,1,24,1,24,1,24,1,24,1,
        24,1,25,1,25,1,25,1,26,1,26,1,27,1,27,1,28,1,28,1,29,1,29,1,30,1,
        30,1,31,1,31,1,32,1,32,1,33,1,33,1,34,1,34,1,35,1,35,1,35,1,35,5,
        35,245,8,35,10,35,12,35,248,9,35,1,35,1,35,1,35,1,35,1,35,1,35,5,
        35,256,8,35,10,35,12,35,259,9,35,3,35,261,8,35,1,36,1,36,1,36,1,
        36,1,36,1,37,1,37,1,37,1,37,1,37,1,37,1,38,1,38,1,39,1,39,1,40,1,
        40,1,40,1,40,1,40,1,40,1,40,1,40,1,40,1,40,1,40,1,40,3,40,290,8,
        40,1,41,1,41,3,41,294,8,41,1,42,4,42,297,8,42,11,42,12,42,298,1,
        43,3,43,302,8,43,1,43,4,43,305,8,43,11,43,12,43,306,1,43,1,43,5,
        43,311,8,43,10,43,12,43,314,9,43,1,43,3,43,317,8,43,1,43,1,43,4,
        43,321,8,43,11,43,12,43,322,3,43,325,8,43,1,44,1,44,1,44,1,44,4,
        44,331,8,44,11,44,12,44,332,1,45,1,45,1,45,4,45,338,8,45,11,45,12,
        45,339,1,46,1,46,1,46,3,46,345,8,46,1,46,1,46,5,46,349,8,46,10,46,
        12,46,352,9,46,1,46,1,46,3,46,356,8,46,3,46,358,8,46,1,46,1,46,1,
        46,1,46,1,46,1,46,1,46,1,46,1,46,1,46,3,46,370,8,46,1,46,1,46,3,
        46,374,8,46,1,46,3,46,377,8,46,1,47,1,47,1,47,1,47,1,47,5,47,384,
        8,47,10,47,12,47,387,9,47,1,47,1,47,5,47,391,8,47,10,47,12,47,394,
        9,47,1,47,1,47,1,47,1,47,1,47,1,47,5,47,402,8,47,10,47,12,47,405,
        9,47,1,47,1,47,3,47,409,8,47,1,47,1,47,1,47,1,47,3,47,415,8,47,1,
        47,4,47,418,8,47,11,47,12,47,419,1,47,1,47,3,47,424,8,47,1,48,4,
        48,427,8,48,11,48,12,48,428,1,49,1,49,1,49,1,49,1,49,1,49,5,49,437,
        8,49,10,49,12,49,440,9,49,1,49,1,49,1,50,4,50,445,8,50,11,50,12,
        50,446,1,50,3,50,450,8,50,1,50,1,50,1,51,3,51,455,8,51,1,51,1,51,
        1,246,0,52,1,1,3,2,5,3,7,4,9,5,11,6,13,7,15,8,17,9,19,10,21,11,23,
        12,25,13,27,14,29,15,31,16,33,17,35,18,37,19,39,20,41,21,43,22,45,
        23,47,24,49,25,51,26,53,27,55,28,57,29,59,30,61,31,63,32,65,33,67,
        34,69,35,71,0,73,0,75,0,77,0,79,0,81,0,83,36,85,37,87,38,89,39,91,
        40,93,41,95,42,97,43,99,44,101,45,103,46,1,0,31,2,0,73,73,105,105,
        2,0,78,78,110,110,2,0,84,84,116,116,2,0,66,66,98,98,2,0,79,79,111,
        111,2,0,76,76,108,108,2,0,83,83,115,115,2,0,82,82,114,114,2,0,71,
        71,103,103,2,0,81,81,113,113,2,0,85,85,117,117,2,0,70,70,102,102,
        2,0,65,65,97,97,2,0,80,80,112,112,2,0,89,89,121,121,2,0,90,90,122,
        122,2,0,72,72,104,104,2,0,68,68,100,100,2,0,77,77,109,109,2,0,69,
        69,101,101,2,0,86,86,118,118,2,0,87,87,119,119,2,0,10,10,13,13,1,
        0,48,57,2,0,43,43,45,45,2,0,88,88,120,120,2,0,65,70,97,102,1,0,48,
        49,3,0,48,57,65,90,97,122,2,0,34,34,92,92,3,0,9,10,13,13,32,32,493,
        0,1,1,0,0,0,0,3,1,0,0,0,0,5,1,0,0,0,0,7,1,0,0,0,0,9,1,0,0,0,0,11,
        1,0,0,0,0,13,1,0,0,0,0,15,1,0,0,0,0,17,1,0,0,0,0,19,1,0,0,0,0,21,
        1,0,0,0,0,23,1,0,0,0,0,25,1,0,0,0,0,27,1,0,0,0,0,29,1,0,0,0,0,31,
        1,0,0,0,0,33,1,0,0,0,0,35,1,0,0,0,0,37,1,0,0,0,0,39,1,0,0,0,0,41,
        1,0,0,0,0,43,1,0,0,0,0,45,1,0,0,0,0,47,1,0,0,0,0,49,1,0,0,0,0,51,
        1,0,0,0,0,53,1,0,0,0,0,55,1,0,0,0,0,57,1,0,0,0,0,59,1,0,0,0,0,61,
        1,0,0,0,0,63,1,0,0,0,0,65,1,0,0,0,0,67,1,0,0,0,0,69,1,0,0,0,0,83,
        1,0,0,0,0,85,1,0,0,0,0,87,1,0,0,0,0,89,1,0,0,0,0,91,1,0,0,0,0,93,
        1,0,0,0,0,95,1,0,0,0,0,97,1,0,0,0,0,99,1,0,0,0,0,101,1,0,0,0,0,103,
        1,0,0,0,1,105,1,0,0,0,3,109,1,0,0,0,5,114,1,0,0,0,7,121,1,0,0,0,
        9,127,1,0,0,0,11,133,1,0,0,0,13,139,1,0,0,0,15,141,1,0,0,0,17,143,
        1,0,0,0,19,147,1,0,0,0,21,154,1,0,0,0,23,161,1,0,0,0,25,170,1,0,
        0,0,27,178,1,0,0,0,29,184,1,0,0,0,31,187,1,0,0,0,33,189,1,0,0,0,
        35,192,1,0,0,0,37,194,1,0,0,0,39,197,1,0,0,0,41,199,1,0,0,0,43,201,
        1,0,0,0,45,205,1,0,0,0,47,208,1,0,0,0,49,213,1,0,0,0,51,219,1,0,
        0,0,53,222,1,0,0,0,55,224,1,0,0,0,57,226,1,0,0,0,59,228,1,0,0,0,
        61,230,1,0,0,0,63,232,1,0,0,0,65,234,1,0,0,0,67,236,1,0,0,0,69,238,
        1,0,0,0,71,260,1,0,0,0,73,262,1,0,0,0,75,267,1,0,0,0,77,273,1,0,
        0,0,79,275,1,0,0,0,81,289,1,0,0,0,83,293,1,0,0,0,85,296,1,0,0,0,
        87,324,1,0,0,0,89,326,1,0,0,0,91,334,1,0,0,0,93,376,1,0,0,0,95,423,
        1,0,0,0,97,426,1,0,0,0,99,430,1,0,0,0,101,449,1,0,0,0,103,454,1,
        0,0,0,105,106,7,0,0,0,106,107,7,1,0,0,107,108,7,2,0,0,108,2,1,0,
        0,0,109,110,7,3,0,0,110,111,7,4,0,0,111,112,7,4,0,0,112,113,7,5,
        0,0,113,4,1,0,0,0,114,115,7,6,0,0,115,116,7,2,0,0,116,117,7,7,0,
        0,117,118,7,0,0,0,118,119,7,1,0,0,119,120,7,8,0,0,120,6,1,0,0,0,
        121,122,7,9,0,0,122,123,7,10,0,0,123,124,7,3,0,0,124,125,7,0,0,0,
        125,126,7,2,0,0,126,8,1,0,0,0,127,128,7,9,0,0,128,129,7,10,0,0,129,
        130,7,0,0,0,130,131,7,1,0,0,131,132,7,2,0,0,132,10,1,0,0,0,133,134,
        7,11,0,0,134,135,7,5,0,0,135,136,7,4,0,0,136,137,7,12,0,0,137,138,
        7,2,0,0,138,12,1,0,0,0,139,140,5,43,0,0,140,14,1,0,0,0,141,142,5,
        45,0,0,142,16,1,0,0,0,143,144,7,1,0,0,144,145,7,4,0,0,145,146,7,
        2,0,0,146,18,1,0,0,0,147,148,7,13,0,0,148,149,7,12,0,0,149,150,7,
        10,0,0,150,151,7,5,0,0,151,152,7,0,0,0,152,153,7,14,0,0,153,20,1,
        0,0,0,154,155,7,13,0,0,155,156,7,12,0,0,156,157,7,10,0,0,157,158,
        7,5,0,0,158,159,7,0,0,0,159,160,7,15,0,0,160,22,1,0,0,0,161,162,
        7,16,0,0,162,163,7,12,0,0,163,164,7,17,0,0,164,165,7,12,0,0,165,
        166,7,18,0,0,166,167,7,12,0,0,167,168,7,7,0,0,168,169,7,17,0,0,169,
        24,1,0,0,0,170,171,7,18,0,0,171,172,7,19,0,0,172,173,7,12,0,0,173,
        174,7,6,0,0,174,175,7,10,0,0,175,176,7,7,0,0,176,177,7,19,0,0,177,
        26,1,0,0,0,178,179,7,13,0,0,179,180,7,7,0,0,180,181,7,0,0,0,181,
        182,7,1,0,0,182,183,7,2,0,0,183,28,1,0,0,0,184,185,5,61,0,0,185,
        186,5,61,0,0,186,30,1,0,0,0,187,188,5,62,0,0,188,32,1,0,0,0,189,
        190,5,62,0,0,190,191,5,61,0,0,191,34,1,0,0,0,192,193,5,60,0,0,193,
        36,1,0,0,0,194,195,5,60,0,0,195,196,5,61,0,0,196,38,1,0,0,0,197,
        198,5,61,0,0,198,40,1,0,0,0,199,200,5,59,0,0,200,42,1,0,0,0,201,
        202,7,20,0,0,202,203,7,12,0,0,203,204,7,7,0,0,204,44,1,0,0,0,205,
        206,7,0,0,0,206,207,7,11,0,0,207,46,1,0,0,0,208,209,7,19,0,0,209,
        210,7,5,0,0,210,211,7,6,0,0,211,212,7,19,0,0,212,48,1,0,0,0,213,
        214,7,21,0,0,214,215,7,16,0,0,215,216,7,0,0,0,216,217,7,5,0,0,217,
        218,7,19,0,0,218,50,1,0,0,0,219,220,7,17,0,0,220,221,7,4,0,0,221,
        52,1,0,0,0,222,223,5,123,0,0,223,54,1,0,0,0,224,225,5,125,0,0,225,
        56,1,0,0,0,226,227,5,40,0,0,227,58,1,0,0,0,228,229,5,41,0,0,229,
        60,1,0,0,0,230,231,5,91,0,0,231,62,1,0,0,0,232,233,5,93,0,0,233,
        64,1,0,0,0,234,235,5,46,0,0,235,66,1,0,0,0,236,237,5,34,0,0,237,
        68,1,0,0,0,238,239,5,44,0,0,239,70,1,0,0,0,240,241,5,47,0,0,241,
        242,5,42,0,0,242,246,1,0,0,0,243,245,9,0,0,0,244,243,1,0,0,0,245,
        248,1,0,0,0,246,247,1,0,0,0,246,244,1,0,0,0,247,249,1,0,0,0,248,
        246,1,0,0,0,249,250,5,42,0,0,250,261,5,47,0,0,251,252,5,47,0,0,252,
        253,5,47,0,0,253,257,1,0,0,0,254,256,8,22,0,0,255,254,1,0,0,0,256,
        259,1,0,0,0,257,255,1,0,0,0,257,258,1,0,0,0,258,261,1,0,0,0,259,
        257,1,0,0,0,260,240,1,0,0,0,260,251,1,0,0,0,261,72,1,0,0,0,262,263,
        7,2,0,0,263,264,7,7,0,0,264,265,7,10,0,0,265,266,7,19,0,0,266,74,
        1,0,0,0,267,268,7,11,0,0,268,269,7,12,0,0,269,270,7,5,0,0,270,271,
        7,6,0,0,271,272,7,19,0,0,272,76,1,0,0,0,273,274,7,23,0,0,274,78,
        1,0,0,0,275,276,7,24,0,0,276,80,1,0,0,0,277,278,5,124,0,0,278,279,
        5,48,0,0,279,290,5,62,0,0,280,281,5,124,0,0,281,282,5,49,0,0,282,
        290,5,62,0,0,283,284,5,124,0,0,284,285,5,43,0,0,285,290,5,62,0,0,
        286,287,5,124,0,0,287,288,5,45,0,0,288,290,5,62,0,0,289,277,1,0,
        0,0,289,280,1,0,0,0,289,283,1,0,0,0,289,286,1,0,0,0,290,82,1,0,0,
        0,291,294,3,73,36,0,292,294,3,75,37,0,293,291,1,0,0,0,293,292,1,
        0,0,0,294,84,1,0,0,0,295,297,3,77,38,0,296,295,1,0,0,0,297,298,1,
        0,0,0,298,296,1,0,0,0,298,299,1,0,0,0,299,86,1,0,0,0,300,302,3,79,
        39,0,301,300,1,0,0,0,301,302,1,0,0,0,302,304,1,0,0,0,303,305,3,77,
        38,0,304,303,1,0,0,0,305,306,1,0,0,0,306,304,1,0,0,0,306,307,1,0,
        0,0,307,308,1,0,0,0,308,312,5,46,0,0,309,311,3,77,38,0,310,309,1,
        0,0,0,311,314,1,0,0,0,312,310,1,0,0,0,312,313,1,0,0,0,313,325,1,
        0,0,0,314,312,1,0,0,0,315,317,3,79,39,0,316,315,1,0,0,0,316,317,
        1,0,0,0,317,318,1,0,0,0,318,320,5,46,0,0,319,321,3,77,38,0,320,319,
        1,0,0,0,321,322,1,0,0,0,322,320,1,0,0,0,322,323,1,0,0,0,323,325,
        1,0,0,0,324,301,1,0,0,0,324,316,1,0,0,0,325,88,1,0,0,0,326,327,5,
        48,0,0,327,330,7,25,0,0,328,331,7,26,0,0,329,331,3,77,38,0,330,328,
        1,0,0,0,330,329,1,0,0,0,331,332,1,0,0,0,332,330,1,0,0,0,332,333,
        1,0,0,0,333,90,1,0,0,0,334,335,5,48,0,0,335,337,7,3,0,0,336,338,
        7,27,0,0,337,336,1,0,0,0,338,339,1,0,0,0,339,337,1,0,0,0,339,340,
        1,0,0,0,340,92,1,0,0,0,341,344,3,61,30,0,342,345,3,83,41,0,343,345,
        2,48,49,0,344,342,1,0,0,0,344,343,1,0,0,0,345,357,1,0,0,0,346,350,
        3,69,34,0,347,349,5,32,0,0,348,347,1,0,0,0,349,352,1,0,0,0,350,348,
        1,0,0,0,350,351,1,0,0,0,351,355,1,0,0,0,352,350,1,0,0,0,353,356,
        3,83,41,0,354,356,2,48,49,0,355,353,1,0,0,0,355,354,1,0,0,0,356,
        358,1,0,0,0,357,346,1,0,0,0,357,358,1,0,0,0,358,359,1,0,0,0,359,
        360,3,63,31,0,360,361,7,9,0,0,361,377,1,0,0,0,362,363,3,87,43,0,
        363,364,3,69,34,0,364,365,3,87,43,0,365,366,7,9,0,0,366,377,1,0,
        0,0,367,377,3,81,40,0,368,370,3,79,39,0,369,368,1,0,0,0,369,370,
        1,0,0,0,370,373,1,0,0,0,371,374,3,83,41,0,372,374,2,48,49,0,373,
        371,1,0,0,0,373,372,1,0,0,0,374,375,1,0,0,0,375,377,7,9,0,0,376,
        341,1,0,0,0,376,362,1,0,0,0,376,367,1,0,0,0,376,369,1,0,0,0,377,
        94,1,0,0,0,378,424,3,93,46,0,379,380,3,61,30,0,380,392,3,93,46,0,
        381,385,3,69,34,0,382,384,5,32,0,0,383,382,1,0,0,0,384,387,1,0,0,
        0,385,383,1,0,0,0,385,386,1,0,0,0,386,388,1,0,0,0,387,385,1,0,0,
        0,388,389,3,93,46,0,389,391,1,0,0,0,390,381,1,0,0,0,391,394,1,0,
        0,0,392,390,1,0,0,0,392,393,1,0,0,0,393,395,1,0,0,0,394,392,1,0,
        0,0,395,396,3,63,31,0,396,424,1,0,0,0,397,398,3,61,30,0,398,408,
        3,85,42,0,399,403,3,69,34,0,400,402,5,32,0,0,401,400,1,0,0,0,402,
        405,1,0,0,0,403,401,1,0,0,0,403,404,1,0,0,0,404,406,1,0,0,0,405,
        403,1,0,0,0,406,407,3,85,42,0,407,409,1,0,0,0,408,399,1,0,0,0,408,
        409,1,0,0,0,409,410,1,0,0,0,410,411,3,63,31,0,411,412,7,9,0,0,412,
        424,1,0,0,0,413,415,3,79,39,0,414,413,1,0,0,0,414,415,1,0,0,0,415,
        417,1,0,0,0,416,418,3,77,38,0,417,416,1,0,0,0,418,419,1,0,0,0,419,
        417,1,0,0,0,419,420,1,0,0,0,420,421,1,0,0,0,421,422,7,9,0,0,422,
        424,1,0,0,0,423,378,1,0,0,0,423,379,1,0,0,0,423,397,1,0,0,0,423,
        414,1,0,0,0,424,96,1,0,0,0,425,427,7,28,0,0,426,425,1,0,0,0,427,
        428,1,0,0,0,428,426,1,0,0,0,428,429,1,0,0,0,429,98,1,0,0,0,430,438,
        5,34,0,0,431,432,5,92,0,0,432,437,9,0,0,0,433,434,5,34,0,0,434,437,
        5,34,0,0,435,437,8,29,0,0,436,431,1,0,0,0,436,433,1,0,0,0,436,435,
        1,0,0,0,437,440,1,0,0,0,438,436,1,0,0,0,438,439,1,0,0,0,439,441,
        1,0,0,0,440,438,1,0,0,0,441,442,5,34,0,0,442,100,1,0,0,0,443,445,
        7,30,0,0,444,443,1,0,0,0,445,446,1,0,0,0,446,444,1,0,0,0,446,447,
        1,0,0,0,447,450,1,0,0,0,448,450,3,71,35,0,449,444,1,0,0,0,449,448,
        1,0,0,0,450,451,1,0,0,0,451,452,6,50,0,0,452,102,1,0,0,0,453,455,
        5,13,0,0,454,453,1,0,0,0,454,455,1,0,0,0,455,456,1,0,0,0,456,457,
        5,10,0,0,457,104,1,0,0,0,36,0,246,257,260,289,293,298,301,306,312,
        316,322,324,330,332,339,344,350,355,357,369,373,376,385,392,403,
        408,414,419,423,428,436,438,446,449,454,1,6,0,0
    ]

class qutes_lexer(Lexer):

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    INT_TYPE = 1
    BOOL_TYPE = 2
    STRING_TYPE = 3
    QUBIT_TYPE = 4
    QUINT_TYPE = 5
    FLOAT_TYPE = 6
    ADD = 7
    SUB = 8
    NOT = 9
    PAULIY = 10
    PAULIZ = 11
    HADAMARD = 12
    MEASURE = 13
    PRINT = 14
    EQUAL = 15
    GREATER = 16
    GREATEREQUAL = 17
    LOWER = 18
    LOWEREQUAL = 19
    ASSIGN = 20
    END_OF_STATEMENT = 21
    VAR_STATEMENT = 22
    IF_STATEMENT = 23
    ELSE_STATEMENT = 24
    WHILE_STATEMENT = 25
    DO_STATEMENT = 26
    CURLY_PARENTHESIS_OPEN = 27
    CURLY_PARENTHESIS_CLOSE = 28
    ROUND_PARENTHESIS_OPEN = 29
    ROUND_PARENTHESIS_CLOSE = 30
    SQUARE_PARENTHESIS_OPEN = 31
    SQUARE_PARENTHESIS_CLOSE = 32
    DOT = 33
    STRING_ENCLOSURE = 34
    COMMA = 35
    BOOL_LITERAL = 36
    INT_LITERAL = 37
    FLOAT_LITERAL = 38
    HEX_LITERAL = 39
    BIN_LITERAL = 40
    QUBIT_LITERAL = 41
    QUINT_LITERAL = 42
    SYMBOL_LITERAL = 43
    STRING_LITERAL = 44
    WS = 45
    NEWLINE = 46

    channelNames = [ u"DEFAULT_TOKEN_CHANNEL", u"HIDDEN" ]

    modeNames = [ "DEFAULT_MODE" ]

    literalNames = [ "<INVALID>",
            "'int'", "'bool'", "'string'", "'qubit'", "'quint'", "'float'", 
            "'+'", "'-'", "'not'", "'pauliy'", "'pauliz'", "'hadamard'", 
            "'measure'", "'print'", "'=='", "'>'", "'>='", "'<'", "'<='", 
            "'='", "';'", "'var'", "'if'", "'else'", "'while'", "'do'", 
            "'{'", "'}'", "'('", "')'", "'['", "']'", "'.'", "'\"'", "','" ]

    symbolicNames = [ "<INVALID>",
            "INT_TYPE", "BOOL_TYPE", "STRING_TYPE", "QUBIT_TYPE", "QUINT_TYPE", 
            "FLOAT_TYPE", "ADD", "SUB", "NOT", "PAULIY", "PAULIZ", "HADAMARD", 
            "MEASURE", "PRINT", "EQUAL", "GREATER", "GREATEREQUAL", "LOWER", 
            "LOWEREQUAL", "ASSIGN", "END_OF_STATEMENT", "VAR_STATEMENT", 
            "IF_STATEMENT", "ELSE_STATEMENT", "WHILE_STATEMENT", "DO_STATEMENT", 
            "CURLY_PARENTHESIS_OPEN", "CURLY_PARENTHESIS_CLOSE", "ROUND_PARENTHESIS_OPEN", 
            "ROUND_PARENTHESIS_CLOSE", "SQUARE_PARENTHESIS_OPEN", "SQUARE_PARENTHESIS_CLOSE", 
            "DOT", "STRING_ENCLOSURE", "COMMA", "BOOL_LITERAL", "INT_LITERAL", 
            "FLOAT_LITERAL", "HEX_LITERAL", "BIN_LITERAL", "QUBIT_LITERAL", 
            "QUINT_LITERAL", "SYMBOL_LITERAL", "STRING_LITERAL", "WS", "NEWLINE" ]

    ruleNames = [ "INT_TYPE", "BOOL_TYPE", "STRING_TYPE", "QUBIT_TYPE", 
                  "QUINT_TYPE", "FLOAT_TYPE", "ADD", "SUB", "NOT", "PAULIY", 
                  "PAULIZ", "HADAMARD", "MEASURE", "PRINT", "EQUAL", "GREATER", 
                  "GREATEREQUAL", "LOWER", "LOWEREQUAL", "ASSIGN", "END_OF_STATEMENT", 
                  "VAR_STATEMENT", "IF_STATEMENT", "ELSE_STATEMENT", "WHILE_STATEMENT", 
                  "DO_STATEMENT", "CURLY_PARENTHESIS_OPEN", "CURLY_PARENTHESIS_CLOSE", 
                  "ROUND_PARENTHESIS_OPEN", "ROUND_PARENTHESIS_CLOSE", "SQUARE_PARENTHESIS_OPEN", 
                  "SQUARE_PARENTHESIS_CLOSE", "DOT", "STRING_ENCLOSURE", 
                  "COMMA", "COMMENT", "TRUE", "FALSE", "DIGIT", "MATH_SIGN", 
                  "QUBIT_STANDARD", "BOOL_LITERAL", "INT_LITERAL", "FLOAT_LITERAL", 
                  "HEX_LITERAL", "BIN_LITERAL", "QUBIT_LITERAL", "QUINT_LITERAL", 
                  "SYMBOL_LITERAL", "STRING_LITERAL", "WS", "NEWLINE" ]

    grammarFileName = "qutes_lexer.g4"

    def __init__(self, input=None, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.1")
        self._interp = LexerATNSimulator(self, self.atn, self.decisionsToDFA, PredictionContextCache())
        self._actions = None
        self._predicates = None


