import sys
from antlr4 import *
from QutesAntlr.QutesLexer import QutesLexer
from QutesAntlr.QutesParser import QutesParser
from QutesGrammarVisitor import QutesGrammarVisitor
from QutesGrammarListener import QutesGrammarListener

def main(argv):
    input_stream = FileStream(argv[1])
    lexer = QutesLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = QutesParser(stream)
    tree = parser.program()

    if parser.getNumberOfSyntaxErrors() > 0:
        print("syntax errors")
    else:
        grammarVisitor = QutesGrammarVisitor()
        result = grammarVisitor.visit(tree)
        print("Execution result:", result)

        # grammarListener = QutesGrammarListener()
        # walker = ParseTreeWalker()
        # walker.walk(grammarListener, tree)
        # print('result_at_top =', grammarListener.getValue(tree))

    lisp_tree_str = tree.toStringTree(recog=parser)
    print(lisp_tree_str)

if __name__ == '__main__':
    main(sys.argv)