"""A compiler for Qutes Lang source file"""

import sys
import argparse
from antlr4 import FileStream, CommonTokenStream, ParseTreeWalker
from anytree import RenderTree
from qutes_antlr.qutes_lexer import qutes_lexer
from qutes_antlr.qutes_parser import qutes_parser
from qutes_grammar_visitor import QutesGrammarVisitor
from symbols_discovery_listener import SymbolsDiscoveryListener

def main(argv):
    """Entrypoint for Qutes Lang compiler"""

    parser = argparse.ArgumentParser(description='Compile Qutes Lang source code.')
    parser.add_argument('file_path', metavar='file_path', help='The file path of the Qutes source code.')
    args = parser.parse_args()

    input_stream = FileStream(args.file_path)
    lexer = qutes_lexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = qutes_parser(stream)
    tree = parser.program()

    if parser.getNumberOfSyntaxErrors() > 0:
        print("syntax errors")
    else:
        grammar_listener = SymbolsDiscoveryListener()
        walker = ParseTreeWalker()
        walker.walk(grammar_listener, tree)
        symbols_tree = grammar_listener.scope_handler.symbols_tree
        
        grammar_visitor = QutesGrammarVisitor(symbols_tree)
        result = str(grammar_visitor.visit(tree))
        
        print()
        print("----Execution result----")
        print(result.replace("\n", "", 1))
        for pre, _, node in RenderTree(symbols_tree):
            print("%s%s(%s) Symbols: %s" % (pre, node.scope_type, node.scope_type_detail, node.symbols))
        print("\n")

    lisp_tree_str = tree.toStringTree(recog=parser)
    print("-------Lisp Tree--------")
    print(lisp_tree_str)
    print()

if __name__ == '__main__':
    main(sys.argv)
