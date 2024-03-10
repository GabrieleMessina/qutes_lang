from qutes_antlr.qutes_parser import qutes_parser

class QutesParser(qutes_parser):
    QUBIT_LITERAL_POSTFIX = "'q'"
    __custom_literal_names__ = [QUBIT_LITERAL_POSTFIX]
    def literal_to_string(literal) -> str:
        if(literal in QutesParser.__custom_literal_names__): 
            return literal.removeprefix("'").removesuffix("'")
        else: return qutes_parser.literalNames[literal].removeprefix("'").removesuffix("'")