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
        4,0,80,680,6,-1,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,
        2,6,7,6,2,7,7,7,2,8,7,8,2,9,7,9,2,10,7,10,2,11,7,11,2,12,7,12,2,
        13,7,13,2,14,7,14,2,15,7,15,2,16,7,16,2,17,7,17,2,18,7,18,2,19,7,
        19,2,20,7,20,2,21,7,21,2,22,7,22,2,23,7,23,2,24,7,24,2,25,7,25,2,
        26,7,26,2,27,7,27,2,28,7,28,2,29,7,29,2,30,7,30,2,31,7,31,2,32,7,
        32,2,33,7,33,2,34,7,34,2,35,7,35,2,36,7,36,2,37,7,37,2,38,7,38,2,
        39,7,39,2,40,7,40,2,41,7,41,2,42,7,42,2,43,7,43,2,44,7,44,2,45,7,
        45,2,46,7,46,2,47,7,47,2,48,7,48,2,49,7,49,2,50,7,50,2,51,7,51,2,
        52,7,52,2,53,7,53,2,54,7,54,2,55,7,55,2,56,7,56,2,57,7,57,2,58,7,
        58,2,59,7,59,2,60,7,60,2,61,7,61,2,62,7,62,2,63,7,63,2,64,7,64,2,
        65,7,65,2,66,7,66,2,67,7,67,2,68,7,68,2,69,7,69,2,70,7,70,2,71,7,
        71,2,72,7,72,2,73,7,73,2,74,7,74,2,75,7,75,2,76,7,76,2,77,7,77,2,
        78,7,78,2,79,7,79,2,80,7,80,2,81,7,81,2,82,7,82,2,83,7,83,2,84,7,
        84,2,85,7,85,1,0,1,0,1,0,1,0,1,1,1,1,1,1,1,1,1,1,1,2,1,2,1,2,1,2,
        1,2,1,2,1,2,1,3,1,3,1,3,1,3,1,3,1,3,1,4,1,4,1,4,1,4,1,4,1,4,1,5,
        1,5,1,5,1,5,1,5,1,5,1,5,1,5,1,5,1,6,1,6,1,6,1,6,1,6,1,6,1,7,1,7,
        1,7,1,7,1,7,1,8,1,8,1,8,1,8,1,8,1,8,1,8,1,9,1,9,1,10,1,10,1,11,1,
        11,1,12,1,12,1,13,1,13,1,14,1,14,1,15,1,15,1,15,1,15,1,16,1,16,1,
        16,1,16,1,17,1,17,1,17,1,18,1,18,1,18,1,19,1,19,1,19,1,19,1,19,1,
        20,1,20,1,20,1,20,1,20,1,20,1,20,1,21,1,21,1,21,1,21,1,21,1,21,1,
        21,1,22,1,22,1,22,1,22,1,22,1,22,1,22,1,23,1,23,1,23,1,23,1,24,1,
        24,1,24,1,24,1,25,1,25,1,25,1,25,1,26,1,26,1,26,1,26,1,27,1,27,1,
        27,1,27,1,27,1,27,1,27,1,27,1,27,1,28,1,28,1,28,1,28,1,28,1,28,1,
        28,1,28,1,29,1,29,1,29,1,29,1,29,1,29,1,30,1,30,1,30,1,30,1,30,1,
        30,1,30,1,30,1,31,1,31,1,31,1,31,1,31,1,31,1,31,1,31,1,32,1,32,1,
        32,1,33,1,33,1,33,1,34,1,34,1,35,1,35,1,35,1,36,1,36,1,37,1,37,1,
        37,1,38,1,38,1,38,1,39,1,39,1,39,1,40,1,40,1,41,1,41,1,41,1,42,1,
        42,1,42,1,43,1,43,1,43,1,44,1,44,1,44,1,45,1,45,1,45,1,46,1,46,1,
        46,1,47,1,47,1,47,1,48,1,48,1,49,1,49,1,49,1,49,1,50,1,50,1,50,1,
        50,1,51,1,51,1,51,1,51,1,51,1,51,1,51,1,51,1,52,1,52,1,52,1,52,1,
        52,1,52,1,52,1,53,1,53,1,53,1,54,1,54,1,54,1,54,1,54,1,54,1,55,1,
        55,1,55,1,56,1,56,1,56,1,56,1,56,1,57,1,57,1,57,1,57,1,57,1,57,1,
        58,1,58,1,58,1,59,1,59,1,60,1,60,1,61,1,61,1,62,1,62,1,63,1,63,1,
        64,1,64,1,65,1,65,1,66,1,66,1,67,1,67,1,68,1,68,1,68,1,68,5,68,454,
        8,68,10,68,12,68,457,9,68,1,68,1,68,1,68,1,68,1,68,1,68,5,68,465,
        8,68,10,68,12,68,468,9,68,3,68,470,8,68,1,69,1,69,1,69,1,69,1,69,
        1,70,1,70,1,70,1,70,1,70,1,70,1,71,1,71,1,72,1,72,1,73,1,73,1,73,
        1,73,1,73,1,73,1,73,1,73,1,73,1,73,1,73,1,73,3,73,499,8,73,1,74,
        1,74,1,74,3,74,504,8,74,1,75,3,75,507,8,75,1,75,4,75,510,8,75,11,
        75,12,75,511,1,76,3,76,515,8,76,1,76,4,76,518,8,76,11,76,12,76,519,
        1,76,1,76,5,76,524,8,76,10,76,12,76,527,9,76,1,76,3,76,530,8,76,
        1,76,1,76,4,76,534,8,76,11,76,12,76,535,3,76,538,8,76,1,77,1,77,
        1,77,1,77,4,77,544,8,77,11,77,12,77,545,1,78,1,78,1,78,4,78,551,
        8,78,11,78,12,78,552,1,79,1,79,1,79,3,79,558,8,79,1,79,1,79,5,79,
        562,8,79,10,79,12,79,565,9,79,1,79,1,79,3,79,569,8,79,3,79,571,8,
        79,1,79,1,79,1,79,1,79,1,79,1,79,1,79,1,79,1,79,1,79,3,79,583,8,
        79,1,79,1,79,3,79,587,8,79,1,79,3,79,590,8,79,1,80,1,80,1,80,1,80,
        1,80,5,80,597,8,80,10,80,12,80,600,9,80,1,80,1,80,5,80,604,8,80,
        10,80,12,80,607,9,80,1,80,1,80,1,80,1,80,1,80,1,80,1,80,5,80,616,
        8,80,10,80,12,80,619,9,80,1,80,1,80,5,80,623,8,80,10,80,12,80,626,
        9,80,1,80,1,80,1,80,1,80,3,80,632,8,80,1,80,4,80,635,8,80,11,80,
        12,80,636,1,80,1,80,3,80,641,8,80,1,81,1,81,1,81,1,82,1,82,5,82,
        648,8,82,10,82,12,82,651,9,82,1,83,1,83,1,83,1,83,1,83,1,83,5,83,
        659,8,83,10,83,12,83,662,9,83,1,83,1,83,1,84,4,84,667,8,84,11,84,
        12,84,668,1,84,3,84,672,8,84,1,84,1,84,1,85,3,85,677,8,85,1,85,1,
        85,1,455,0,86,1,1,3,2,5,3,7,4,9,5,11,6,13,7,15,8,17,9,19,10,21,11,
        23,12,25,13,27,14,29,15,31,16,33,17,35,18,37,19,39,20,41,21,43,22,
        45,23,47,24,49,25,51,26,53,27,55,28,57,29,59,30,61,31,63,32,65,33,
        67,34,69,35,71,36,73,37,75,38,77,39,79,40,81,41,83,42,85,43,87,44,
        89,45,91,46,93,47,95,48,97,49,99,50,101,51,103,52,105,53,107,54,
        109,55,111,56,113,57,115,58,117,59,119,60,121,61,123,62,125,63,127,
        64,129,65,131,66,133,67,135,68,137,0,139,0,141,0,143,0,145,0,147,
        0,149,69,151,70,153,71,155,72,157,73,159,74,161,75,163,76,165,77,
        167,78,169,79,171,80,1,0,33,2,0,73,73,105,105,2,0,78,78,110,110,
        2,0,84,84,116,116,2,0,66,66,98,98,2,0,79,79,111,111,2,0,76,76,108,
        108,2,0,83,83,115,115,2,0,82,82,114,114,2,0,71,71,103,103,2,0,81,
        81,113,113,2,0,85,85,117,117,2,0,70,70,102,102,2,0,65,65,97,97,2,
        0,86,86,118,118,2,0,68,68,100,100,2,0,69,69,101,101,2,0,89,89,121,
        121,2,0,87,87,119,119,2,0,80,80,112,112,2,0,90,90,122,122,2,0,77,
        77,109,109,2,0,67,67,99,99,2,0,88,88,120,120,2,0,72,72,104,104,2,
        0,10,10,13,13,1,0,48,57,2,0,43,43,45,45,2,0,65,70,97,102,1,0,48,
        49,3,0,65,90,95,95,97,122,4,0,48,57,65,90,95,95,97,122,2,0,34,34,
        92,92,3,0,9,10,13,13,32,32,717,0,1,1,0,0,0,0,3,1,0,0,0,0,5,1,0,0,
        0,0,7,1,0,0,0,0,9,1,0,0,0,0,11,1,0,0,0,0,13,1,0,0,0,0,15,1,0,0,0,
        0,17,1,0,0,0,0,19,1,0,0,0,0,21,1,0,0,0,0,23,1,0,0,0,0,25,1,0,0,0,
        0,27,1,0,0,0,0,29,1,0,0,0,0,31,1,0,0,0,0,33,1,0,0,0,0,35,1,0,0,0,
        0,37,1,0,0,0,0,39,1,0,0,0,0,41,1,0,0,0,0,43,1,0,0,0,0,45,1,0,0,0,
        0,47,1,0,0,0,0,49,1,0,0,0,0,51,1,0,0,0,0,53,1,0,0,0,0,55,1,0,0,0,
        0,57,1,0,0,0,0,59,1,0,0,0,0,61,1,0,0,0,0,63,1,0,0,0,0,65,1,0,0,0,
        0,67,1,0,0,0,0,69,1,0,0,0,0,71,1,0,0,0,0,73,1,0,0,0,0,75,1,0,0,0,
        0,77,1,0,0,0,0,79,1,0,0,0,0,81,1,0,0,0,0,83,1,0,0,0,0,85,1,0,0,0,
        0,87,1,0,0,0,0,89,1,0,0,0,0,91,1,0,0,0,0,93,1,0,0,0,0,95,1,0,0,0,
        0,97,1,0,0,0,0,99,1,0,0,0,0,101,1,0,0,0,0,103,1,0,0,0,0,105,1,0,
        0,0,0,107,1,0,0,0,0,109,1,0,0,0,0,111,1,0,0,0,0,113,1,0,0,0,0,115,
        1,0,0,0,0,117,1,0,0,0,0,119,1,0,0,0,0,121,1,0,0,0,0,123,1,0,0,0,
        0,125,1,0,0,0,0,127,1,0,0,0,0,129,1,0,0,0,0,131,1,0,0,0,0,133,1,
        0,0,0,0,135,1,0,0,0,0,149,1,0,0,0,0,151,1,0,0,0,0,153,1,0,0,0,0,
        155,1,0,0,0,0,157,1,0,0,0,0,159,1,0,0,0,0,161,1,0,0,0,0,163,1,0,
        0,0,0,165,1,0,0,0,0,167,1,0,0,0,0,169,1,0,0,0,0,171,1,0,0,0,1,173,
        1,0,0,0,3,177,1,0,0,0,5,182,1,0,0,0,7,189,1,0,0,0,9,195,1,0,0,0,
        11,201,1,0,0,0,13,210,1,0,0,0,15,216,1,0,0,0,17,221,1,0,0,0,19,228,
        1,0,0,0,21,230,1,0,0,0,23,232,1,0,0,0,25,234,1,0,0,0,27,236,1,0,
        0,0,29,238,1,0,0,0,31,240,1,0,0,0,33,244,1,0,0,0,35,248,1,0,0,0,
        37,251,1,0,0,0,39,254,1,0,0,0,41,259,1,0,0,0,43,266,1,0,0,0,45,273,
        1,0,0,0,47,280,1,0,0,0,49,284,1,0,0,0,51,288,1,0,0,0,53,292,1,0,
        0,0,55,296,1,0,0,0,57,305,1,0,0,0,59,313,1,0,0,0,61,319,1,0,0,0,
        63,327,1,0,0,0,65,335,1,0,0,0,67,338,1,0,0,0,69,341,1,0,0,0,71,343,
        1,0,0,0,73,346,1,0,0,0,75,348,1,0,0,0,77,351,1,0,0,0,79,354,1,0,
        0,0,81,357,1,0,0,0,83,359,1,0,0,0,85,362,1,0,0,0,87,365,1,0,0,0,
        89,368,1,0,0,0,91,371,1,0,0,0,93,374,1,0,0,0,95,377,1,0,0,0,97,380,
        1,0,0,0,99,382,1,0,0,0,101,386,1,0,0,0,103,390,1,0,0,0,105,398,1,
        0,0,0,107,405,1,0,0,0,109,408,1,0,0,0,111,414,1,0,0,0,113,417,1,
        0,0,0,115,422,1,0,0,0,117,428,1,0,0,0,119,431,1,0,0,0,121,433,1,
        0,0,0,123,435,1,0,0,0,125,437,1,0,0,0,127,439,1,0,0,0,129,441,1,
        0,0,0,131,443,1,0,0,0,133,445,1,0,0,0,135,447,1,0,0,0,137,469,1,
        0,0,0,139,471,1,0,0,0,141,476,1,0,0,0,143,482,1,0,0,0,145,484,1,
        0,0,0,147,498,1,0,0,0,149,503,1,0,0,0,151,506,1,0,0,0,153,537,1,
        0,0,0,155,539,1,0,0,0,157,547,1,0,0,0,159,589,1,0,0,0,161,640,1,
        0,0,0,163,642,1,0,0,0,165,645,1,0,0,0,167,652,1,0,0,0,169,671,1,
        0,0,0,171,676,1,0,0,0,173,174,7,0,0,0,174,175,7,1,0,0,175,176,7,
        2,0,0,176,2,1,0,0,0,177,178,7,3,0,0,178,179,7,4,0,0,179,180,7,4,
        0,0,180,181,7,5,0,0,181,4,1,0,0,0,182,183,7,6,0,0,183,184,7,2,0,
        0,184,185,7,7,0,0,185,186,7,0,0,0,186,187,7,1,0,0,187,188,7,8,0,
        0,188,6,1,0,0,0,189,190,7,9,0,0,190,191,7,10,0,0,191,192,7,3,0,0,
        192,193,7,0,0,0,193,194,7,2,0,0,194,8,1,0,0,0,195,196,7,9,0,0,196,
        197,7,10,0,0,197,198,7,0,0,0,198,199,7,1,0,0,199,200,7,2,0,0,200,
        10,1,0,0,0,201,202,7,9,0,0,202,203,7,10,0,0,203,204,7,6,0,0,204,
        205,7,2,0,0,205,206,7,7,0,0,206,207,7,0,0,0,207,208,7,1,0,0,208,
        209,7,8,0,0,209,12,1,0,0,0,210,211,7,11,0,0,211,212,7,5,0,0,212,
        213,7,4,0,0,213,214,7,12,0,0,214,215,7,2,0,0,215,14,1,0,0,0,216,
        217,7,13,0,0,217,218,7,4,0,0,218,219,7,0,0,0,219,220,7,14,0,0,220,
        16,1,0,0,0,221,222,7,7,0,0,222,223,7,15,0,0,223,224,7,2,0,0,224,
        225,7,10,0,0,225,226,7,7,0,0,226,227,7,1,0,0,227,18,1,0,0,0,228,
        229,5,94,0,0,229,20,1,0,0,0,230,231,5,42,0,0,231,22,1,0,0,0,232,
        233,5,47,0,0,233,24,1,0,0,0,234,235,5,37,0,0,235,26,1,0,0,0,236,
        237,5,43,0,0,237,28,1,0,0,0,238,239,5,45,0,0,239,30,1,0,0,0,240,
        241,7,1,0,0,241,242,7,4,0,0,242,243,7,2,0,0,243,32,1,0,0,0,244,245,
        7,12,0,0,245,246,7,1,0,0,246,247,7,14,0,0,247,34,1,0,0,0,248,249,
        7,4,0,0,249,250,7,7,0,0,250,36,1,0,0,0,251,252,7,3,0,0,252,253,7,
        16,0,0,253,38,1,0,0,0,254,255,7,6,0,0,255,256,7,17,0,0,256,257,7,
        12,0,0,257,258,7,18,0,0,258,40,1,0,0,0,259,260,7,18,0,0,260,261,
        7,12,0,0,261,262,7,10,0,0,262,263,7,5,0,0,263,264,7,0,0,0,264,265,
        7,16,0,0,265,42,1,0,0,0,266,267,7,18,0,0,267,268,7,12,0,0,268,269,
        7,10,0,0,269,270,7,5,0,0,270,271,7,0,0,0,271,272,7,19,0,0,272,44,
        1,0,0,0,273,274,7,8,0,0,274,275,7,7,0,0,275,276,7,4,0,0,276,277,
        7,13,0,0,277,278,7,15,0,0,278,279,7,7,0,0,279,46,1,0,0,0,280,281,
        7,20,0,0,281,282,7,21,0,0,282,283,7,19,0,0,283,48,1,0,0,0,284,285,
        7,20,0,0,285,286,7,21,0,0,286,287,7,22,0,0,287,50,1,0,0,0,288,289,
        7,20,0,0,289,290,7,21,0,0,290,291,7,16,0,0,291,52,1,0,0,0,292,293,
        7,20,0,0,293,294,7,21,0,0,294,295,7,18,0,0,295,54,1,0,0,0,296,297,
        7,23,0,0,297,298,7,12,0,0,298,299,7,14,0,0,299,300,7,12,0,0,300,
        301,7,20,0,0,301,302,7,12,0,0,302,303,7,7,0,0,303,304,7,14,0,0,304,
        56,1,0,0,0,305,306,7,20,0,0,306,307,7,15,0,0,307,308,7,12,0,0,308,
        309,7,6,0,0,309,310,7,10,0,0,310,311,7,7,0,0,311,312,7,15,0,0,312,
        58,1,0,0,0,313,314,7,18,0,0,314,315,7,7,0,0,315,316,7,0,0,0,316,
        317,7,1,0,0,317,318,7,2,0,0,318,60,1,0,0,0,319,320,7,18,0,0,320,
        321,7,7,0,0,321,322,7,0,0,0,322,323,7,1,0,0,323,324,7,2,0,0,324,
        325,7,5,0,0,325,326,7,1,0,0,326,62,1,0,0,0,327,328,7,3,0,0,328,329,
        7,12,0,0,329,330,7,7,0,0,330,331,7,7,0,0,331,332,7,0,0,0,332,333,
        7,15,0,0,333,334,7,7,0,0,334,64,1,0,0,0,335,336,5,61,0,0,336,337,
        5,61,0,0,337,66,1,0,0,0,338,339,5,33,0,0,339,340,5,61,0,0,340,68,
        1,0,0,0,341,342,5,62,0,0,342,70,1,0,0,0,343,344,5,62,0,0,344,345,
        5,61,0,0,345,72,1,0,0,0,346,347,5,60,0,0,347,74,1,0,0,0,348,349,
        5,60,0,0,349,350,5,61,0,0,350,76,1,0,0,0,351,352,5,60,0,0,352,353,
        5,60,0,0,353,78,1,0,0,0,354,355,5,62,0,0,355,356,5,62,0,0,356,80,
        1,0,0,0,357,358,5,61,0,0,358,82,1,0,0,0,359,360,5,43,0,0,360,361,
        5,43,0,0,361,84,1,0,0,0,362,363,5,45,0,0,363,364,5,45,0,0,364,86,
        1,0,0,0,365,366,5,43,0,0,366,367,5,61,0,0,367,88,1,0,0,0,368,369,
        5,45,0,0,369,370,5,61,0,0,370,90,1,0,0,0,371,372,5,42,0,0,372,373,
        5,61,0,0,373,92,1,0,0,0,374,375,5,47,0,0,375,376,5,61,0,0,376,94,
        1,0,0,0,377,378,5,37,0,0,378,379,5,61,0,0,379,96,1,0,0,0,380,381,
        5,59,0,0,381,98,1,0,0,0,382,383,7,13,0,0,383,384,7,12,0,0,384,385,
        7,7,0,0,385,100,1,0,0,0,386,387,7,11,0,0,387,388,7,4,0,0,388,389,
        7,7,0,0,389,102,1,0,0,0,390,391,7,11,0,0,391,392,7,4,0,0,392,393,
        7,7,0,0,393,394,7,15,0,0,394,395,7,12,0,0,395,396,7,21,0,0,396,397,
        7,23,0,0,397,104,1,0,0,0,398,399,7,6,0,0,399,400,7,15,0,0,400,401,
        7,12,0,0,401,402,7,7,0,0,402,403,7,21,0,0,403,404,7,23,0,0,404,106,
        1,0,0,0,405,406,7,0,0,0,406,407,7,1,0,0,407,108,1,0,0,0,408,409,
        7,17,0,0,409,410,7,23,0,0,410,411,7,15,0,0,411,412,7,7,0,0,412,413,
        7,15,0,0,413,110,1,0,0,0,414,415,7,0,0,0,415,416,7,11,0,0,416,112,
        1,0,0,0,417,418,7,15,0,0,418,419,7,5,0,0,419,420,7,6,0,0,420,421,
        7,15,0,0,421,114,1,0,0,0,422,423,7,17,0,0,423,424,7,23,0,0,424,425,
        7,0,0,0,425,426,7,5,0,0,426,427,7,15,0,0,427,116,1,0,0,0,428,429,
        7,14,0,0,429,430,7,4,0,0,430,118,1,0,0,0,431,432,5,123,0,0,432,120,
        1,0,0,0,433,434,5,125,0,0,434,122,1,0,0,0,435,436,5,40,0,0,436,124,
        1,0,0,0,437,438,5,41,0,0,438,126,1,0,0,0,439,440,5,91,0,0,440,128,
        1,0,0,0,441,442,5,93,0,0,442,130,1,0,0,0,443,444,5,46,0,0,444,132,
        1,0,0,0,445,446,5,34,0,0,446,134,1,0,0,0,447,448,5,44,0,0,448,136,
        1,0,0,0,449,450,5,47,0,0,450,451,5,42,0,0,451,455,1,0,0,0,452,454,
        9,0,0,0,453,452,1,0,0,0,454,457,1,0,0,0,455,456,1,0,0,0,455,453,
        1,0,0,0,456,458,1,0,0,0,457,455,1,0,0,0,458,459,5,42,0,0,459,470,
        5,47,0,0,460,461,5,47,0,0,461,462,5,47,0,0,462,466,1,0,0,0,463,465,
        8,24,0,0,464,463,1,0,0,0,465,468,1,0,0,0,466,464,1,0,0,0,466,467,
        1,0,0,0,467,470,1,0,0,0,468,466,1,0,0,0,469,449,1,0,0,0,469,460,
        1,0,0,0,470,138,1,0,0,0,471,472,7,2,0,0,472,473,7,7,0,0,473,474,
        7,10,0,0,474,475,7,15,0,0,475,140,1,0,0,0,476,477,7,11,0,0,477,478,
        7,12,0,0,478,479,7,5,0,0,479,480,7,6,0,0,480,481,7,15,0,0,481,142,
        1,0,0,0,482,483,7,25,0,0,483,144,1,0,0,0,484,485,7,26,0,0,485,146,
        1,0,0,0,486,487,5,124,0,0,487,488,5,48,0,0,488,499,5,62,0,0,489,
        490,5,124,0,0,490,491,5,49,0,0,491,499,5,62,0,0,492,493,5,124,0,
        0,493,494,5,43,0,0,494,499,5,62,0,0,495,496,5,124,0,0,496,497,5,
        45,0,0,497,499,5,62,0,0,498,486,1,0,0,0,498,489,1,0,0,0,498,492,
        1,0,0,0,498,495,1,0,0,0,499,148,1,0,0,0,500,504,3,139,69,0,501,504,
        3,141,70,0,502,504,2,48,49,0,503,500,1,0,0,0,503,501,1,0,0,0,503,
        502,1,0,0,0,504,150,1,0,0,0,505,507,3,145,72,0,506,505,1,0,0,0,506,
        507,1,0,0,0,507,509,1,0,0,0,508,510,3,143,71,0,509,508,1,0,0,0,510,
        511,1,0,0,0,511,509,1,0,0,0,511,512,1,0,0,0,512,152,1,0,0,0,513,
        515,3,145,72,0,514,513,1,0,0,0,514,515,1,0,0,0,515,517,1,0,0,0,516,
        518,3,143,71,0,517,516,1,0,0,0,518,519,1,0,0,0,519,517,1,0,0,0,519,
        520,1,0,0,0,520,521,1,0,0,0,521,525,5,46,0,0,522,524,3,143,71,0,
        523,522,1,0,0,0,524,527,1,0,0,0,525,523,1,0,0,0,525,526,1,0,0,0,
        526,538,1,0,0,0,527,525,1,0,0,0,528,530,3,145,72,0,529,528,1,0,0,
        0,529,530,1,0,0,0,530,531,1,0,0,0,531,533,5,46,0,0,532,534,3,143,
        71,0,533,532,1,0,0,0,534,535,1,0,0,0,535,533,1,0,0,0,535,536,1,0,
        0,0,536,538,1,0,0,0,537,514,1,0,0,0,537,529,1,0,0,0,538,154,1,0,
        0,0,539,540,5,48,0,0,540,543,7,22,0,0,541,544,7,27,0,0,542,544,3,
        143,71,0,543,541,1,0,0,0,543,542,1,0,0,0,544,545,1,0,0,0,545,543,
        1,0,0,0,545,546,1,0,0,0,546,156,1,0,0,0,547,548,5,48,0,0,548,550,
        7,3,0,0,549,551,7,28,0,0,550,549,1,0,0,0,551,552,1,0,0,0,552,550,
        1,0,0,0,552,553,1,0,0,0,553,158,1,0,0,0,554,557,3,127,63,0,555,558,
        3,149,74,0,556,558,2,48,49,0,557,555,1,0,0,0,557,556,1,0,0,0,558,
        570,1,0,0,0,559,563,3,135,67,0,560,562,5,32,0,0,561,560,1,0,0,0,
        562,565,1,0,0,0,563,561,1,0,0,0,563,564,1,0,0,0,564,568,1,0,0,0,
        565,563,1,0,0,0,566,569,3,149,74,0,567,569,2,48,49,0,568,566,1,0,
        0,0,568,567,1,0,0,0,569,571,1,0,0,0,570,559,1,0,0,0,570,571,1,0,
        0,0,571,572,1,0,0,0,572,573,3,129,64,0,573,574,7,9,0,0,574,590,1,
        0,0,0,575,576,3,153,76,0,576,577,3,135,67,0,577,578,3,153,76,0,578,
        579,7,9,0,0,579,590,1,0,0,0,580,590,3,147,73,0,581,583,3,145,72,
        0,582,581,1,0,0,0,582,583,1,0,0,0,583,586,1,0,0,0,584,587,3,149,
        74,0,585,587,2,48,49,0,586,584,1,0,0,0,586,585,1,0,0,0,587,588,1,
        0,0,0,588,590,7,9,0,0,589,554,1,0,0,0,589,575,1,0,0,0,589,580,1,
        0,0,0,589,582,1,0,0,0,590,160,1,0,0,0,591,641,3,159,79,0,592,593,
        3,127,63,0,593,605,3,159,79,0,594,598,3,135,67,0,595,597,5,32,0,
        0,596,595,1,0,0,0,597,600,1,0,0,0,598,596,1,0,0,0,598,599,1,0,0,
        0,599,601,1,0,0,0,600,598,1,0,0,0,601,602,3,159,79,0,602,604,1,0,
        0,0,603,594,1,0,0,0,604,607,1,0,0,0,605,603,1,0,0,0,605,606,1,0,
        0,0,606,608,1,0,0,0,607,605,1,0,0,0,608,609,3,129,64,0,609,610,7,
        9,0,0,610,641,1,0,0,0,611,612,3,127,63,0,612,624,3,151,75,0,613,
        617,3,135,67,0,614,616,5,32,0,0,615,614,1,0,0,0,616,619,1,0,0,0,
        617,615,1,0,0,0,617,618,1,0,0,0,618,620,1,0,0,0,619,617,1,0,0,0,
        620,621,3,151,75,0,621,623,1,0,0,0,622,613,1,0,0,0,623,626,1,0,0,
        0,624,622,1,0,0,0,624,625,1,0,0,0,625,627,1,0,0,0,626,624,1,0,0,
        0,627,628,3,129,64,0,628,629,7,9,0,0,629,641,1,0,0,0,630,632,3,145,
        72,0,631,630,1,0,0,0,631,632,1,0,0,0,632,634,1,0,0,0,633,635,3,143,
        71,0,634,633,1,0,0,0,635,636,1,0,0,0,636,634,1,0,0,0,636,637,1,0,
        0,0,637,638,1,0,0,0,638,639,7,9,0,0,639,641,1,0,0,0,640,591,1,0,
        0,0,640,592,1,0,0,0,640,611,1,0,0,0,640,631,1,0,0,0,641,162,1,0,
        0,0,642,643,3,167,83,0,643,644,7,9,0,0,644,164,1,0,0,0,645,649,7,
        29,0,0,646,648,7,30,0,0,647,646,1,0,0,0,648,651,1,0,0,0,649,647,
        1,0,0,0,649,650,1,0,0,0,650,166,1,0,0,0,651,649,1,0,0,0,652,660,
        5,34,0,0,653,654,5,92,0,0,654,659,9,0,0,0,655,656,5,34,0,0,656,659,
        5,34,0,0,657,659,8,31,0,0,658,653,1,0,0,0,658,655,1,0,0,0,658,657,
        1,0,0,0,659,662,1,0,0,0,660,658,1,0,0,0,660,661,1,0,0,0,661,663,
        1,0,0,0,662,660,1,0,0,0,663,664,5,34,0,0,664,168,1,0,0,0,665,667,
        7,32,0,0,666,665,1,0,0,0,667,668,1,0,0,0,668,666,1,0,0,0,668,669,
        1,0,0,0,669,672,1,0,0,0,670,672,3,137,68,0,671,666,1,0,0,0,671,670,
        1,0,0,0,672,673,1,0,0,0,673,674,6,84,0,0,674,170,1,0,0,0,675,677,
        5,13,0,0,676,675,1,0,0,0,676,677,1,0,0,0,677,678,1,0,0,0,678,679,
        5,10,0,0,679,172,1,0,0,0,37,0,455,466,469,498,503,506,511,514,519,
        525,529,535,537,543,545,552,557,563,568,570,582,586,589,598,605,
        617,624,631,636,640,649,658,660,668,671,676,1,6,0,0
    ]

class qutes_lexer(Lexer):

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    INT_TYPE = 1
    BOOL_TYPE = 2
    STRING_TYPE = 3
    QUBIT_TYPE = 4
    QUINT_TYPE = 5
    QUSTRING_TYPE = 6
    FLOAT_TYPE = 7
    VOID_TYPE = 8
    RETURN = 9
    EXP = 10
    MULTIPLY = 11
    DIVIDE = 12
    MODULE = 13
    ADD = 14
    SUB = 15
    NOT = 16
    AND = 17
    OR = 18
    BY = 19
    SWAP = 20
    PAULIY = 21
    PAULIZ = 22
    GROVER = 23
    MCZ = 24
    MCX = 25
    MCY = 26
    MCP = 27
    HADAMARD = 28
    MEASURE = 29
    PRINT = 30
    PRINT_LN = 31
    BARRIER = 32
    EQUAL = 33
    NOT_EQUAL = 34
    GREATER = 35
    GREATEREQUAL = 36
    LOWER = 37
    LOWEREQUAL = 38
    LSHIFT = 39
    RSHIFT = 40
    ASSIGN = 41
    AUTO_INCREMENT = 42
    AUTO_DECREMENT = 43
    AUTO_SUM = 44
    AUTO_SUB = 45
    AUTO_MULTIPLY = 46
    AUTO_DIVIDE = 47
    AUTO_MODULE = 48
    END_OF_STATEMENT = 49
    VAR_STATEMENT = 50
    FOR_STATEMENT = 51
    FOREACH_STATEMENT = 52
    SEARCH_STATEMENT = 53
    IN_STATEMENT = 54
    WHERE_STATEMENT = 55
    IF_STATEMENT = 56
    ELSE_STATEMENT = 57
    WHILE_STATEMENT = 58
    DO_STATEMENT = 59
    CURLY_PARENTHESIS_OPEN = 60
    CURLY_PARENTHESIS_CLOSE = 61
    ROUND_PARENTHESIS_OPEN = 62
    ROUND_PARENTHESIS_CLOSE = 63
    SQUARE_PARENTHESIS_OPEN = 64
    SQUARE_PARENTHESIS_CLOSE = 65
    DOT = 66
    STRING_ENCLOSURE = 67
    COMMA = 68
    BOOL_LITERAL = 69
    INT_LITERAL = 70
    FLOAT_LITERAL = 71
    HEX_LITERAL = 72
    BIN_LITERAL = 73
    QUBIT_LITERAL = 74
    QUINT_LITERAL = 75
    QUSTRING_LITERAL = 76
    SYMBOL_LITERAL = 77
    STRING_LITERAL = 78
    WS = 79
    NEWLINE = 80

    channelNames = [ u"DEFAULT_TOKEN_CHANNEL", u"HIDDEN" ]

    modeNames = [ "DEFAULT_MODE" ]

    literalNames = [ "<INVALID>",
            "'int'", "'bool'", "'string'", "'qubit'", "'quint'", "'qustring'", 
            "'float'", "'void'", "'return'", "'^'", "'*'", "'/'", "'%'", 
            "'+'", "'-'", "'not'", "'and'", "'or'", "'by'", "'swap'", "'pauliy'", 
            "'pauliz'", "'grover'", "'mcz'", "'mcx'", "'mcy'", "'mcp'", 
            "'hadamard'", "'measure'", "'print'", "'println'", "'barrier'", 
            "'=='", "'!='", "'>'", "'>='", "'<'", "'<='", "'<<'", "'>>'", 
            "'='", "'++'", "'--'", "'+='", "'-='", "'*='", "'/='", "'%='", 
            "';'", "'var'", "'for'", "'foreach'", "'search'", "'in'", "'where'", 
            "'if'", "'else'", "'while'", "'do'", "'{'", "'}'", "'('", "')'", 
            "'['", "']'", "'.'", "'\"'", "','" ]

    symbolicNames = [ "<INVALID>",
            "INT_TYPE", "BOOL_TYPE", "STRING_TYPE", "QUBIT_TYPE", "QUINT_TYPE", 
            "QUSTRING_TYPE", "FLOAT_TYPE", "VOID_TYPE", "RETURN", "EXP", 
            "MULTIPLY", "DIVIDE", "MODULE", "ADD", "SUB", "NOT", "AND", 
            "OR", "BY", "SWAP", "PAULIY", "PAULIZ", "GROVER", "MCZ", "MCX", 
            "MCY", "MCP", "HADAMARD", "MEASURE", "PRINT", "PRINT_LN", "BARRIER", 
            "EQUAL", "NOT_EQUAL", "GREATER", "GREATEREQUAL", "LOWER", "LOWEREQUAL", 
            "LSHIFT", "RSHIFT", "ASSIGN", "AUTO_INCREMENT", "AUTO_DECREMENT", 
            "AUTO_SUM", "AUTO_SUB", "AUTO_MULTIPLY", "AUTO_DIVIDE", "AUTO_MODULE", 
            "END_OF_STATEMENT", "VAR_STATEMENT", "FOR_STATEMENT", "FOREACH_STATEMENT", 
            "SEARCH_STATEMENT", "IN_STATEMENT", "WHERE_STATEMENT", "IF_STATEMENT", 
            "ELSE_STATEMENT", "WHILE_STATEMENT", "DO_STATEMENT", "CURLY_PARENTHESIS_OPEN", 
            "CURLY_PARENTHESIS_CLOSE", "ROUND_PARENTHESIS_OPEN", "ROUND_PARENTHESIS_CLOSE", 
            "SQUARE_PARENTHESIS_OPEN", "SQUARE_PARENTHESIS_CLOSE", "DOT", 
            "STRING_ENCLOSURE", "COMMA", "BOOL_LITERAL", "INT_LITERAL", 
            "FLOAT_LITERAL", "HEX_LITERAL", "BIN_LITERAL", "QUBIT_LITERAL", 
            "QUINT_LITERAL", "QUSTRING_LITERAL", "SYMBOL_LITERAL", "STRING_LITERAL", 
            "WS", "NEWLINE" ]

    ruleNames = [ "INT_TYPE", "BOOL_TYPE", "STRING_TYPE", "QUBIT_TYPE", 
                  "QUINT_TYPE", "QUSTRING_TYPE", "FLOAT_TYPE", "VOID_TYPE", 
                  "RETURN", "EXP", "MULTIPLY", "DIVIDE", "MODULE", "ADD", 
                  "SUB", "NOT", "AND", "OR", "BY", "SWAP", "PAULIY", "PAULIZ", 
                  "GROVER", "MCZ", "MCX", "MCY", "MCP", "HADAMARD", "MEASURE", 
                  "PRINT", "PRINT_LN", "BARRIER", "EQUAL", "NOT_EQUAL", 
                  "GREATER", "GREATEREQUAL", "LOWER", "LOWEREQUAL", "LSHIFT", 
                  "RSHIFT", "ASSIGN", "AUTO_INCREMENT", "AUTO_DECREMENT", 
                  "AUTO_SUM", "AUTO_SUB", "AUTO_MULTIPLY", "AUTO_DIVIDE", 
                  "AUTO_MODULE", "END_OF_STATEMENT", "VAR_STATEMENT", "FOR_STATEMENT", 
                  "FOREACH_STATEMENT", "SEARCH_STATEMENT", "IN_STATEMENT", 
                  "WHERE_STATEMENT", "IF_STATEMENT", "ELSE_STATEMENT", "WHILE_STATEMENT", 
                  "DO_STATEMENT", "CURLY_PARENTHESIS_OPEN", "CURLY_PARENTHESIS_CLOSE", 
                  "ROUND_PARENTHESIS_OPEN", "ROUND_PARENTHESIS_CLOSE", "SQUARE_PARENTHESIS_OPEN", 
                  "SQUARE_PARENTHESIS_CLOSE", "DOT", "STRING_ENCLOSURE", 
                  "COMMA", "COMMENT", "TRUE", "FALSE", "DIGIT", "MATH_SIGN", 
                  "QUBIT_STANDARD", "BOOL_LITERAL", "INT_LITERAL", "FLOAT_LITERAL", 
                  "HEX_LITERAL", "BIN_LITERAL", "QUBIT_LITERAL", "QUINT_LITERAL", 
                  "QUSTRING_LITERAL", "SYMBOL_LITERAL", "STRING_LITERAL", 
                  "WS", "NEWLINE" ]

    grammarFileName = "qutes_lexer.g4"

    def __init__(self, input=None, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.1")
        self._interp = LexerATNSimulator(self, self.atn, self.decisionsToDFA, PredictionContextCache())
        self._actions = None
        self._predicates = None


