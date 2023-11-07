from qutes_antlr.qutes_parser import qutes_parser

class QutesParser(qutes_parser):
    def literaltostring(literal) -> str:
        return qutes_parser.literalNames[literal].removeprefix("'").removesuffix("'")