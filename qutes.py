"""A compiler for Qutes Lang source file"""

import sys
import argparse
from antlr4 import FileStream, CommonTokenStream
from qutes_antlr.qutesLexer import qutesLexer
from qutes_antlr.qutesParser import qutesParser
from qutes_grammar_visitor import QutesGrammarVisitor
from qutes_grammar_listener import QutesGrammarListener

def main(argv):
    """Entrypoint for Qutes Lang compiler"""

    parser = argparse.ArgumentParser(description='Compile Qutes Lang source code.')
    parser.add_argument('file_path', metavar='file_path', help='The file path of the Qutes source code.')
    args = parser.parse_args()

    input_stream = FileStream(args.file_path)
    lexer = qutesLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = qutesParser(stream)
    tree = parser.program()

    if parser.getNumberOfSyntaxErrors() > 0:
        print("syntax errors")
    else:
        grammar_visitor = QutesGrammarVisitor()
        result = grammar_visitor.visit(tree)
        print("----Execution result----", result)

        # grammarListener = QutesGrammarListener()
        # walker = ParseTreeWalker()
        # walker.walk(grammarListener, tree)
        # print('result_at_top =', grammarListener.getValue(tree))

    lisp_tree_str = tree.toStringTree(recog=parser)
    print("-------Lisp Tree--------\n", lisp_tree_str)

if __name__ == '__main__':
    main(sys.argv)
