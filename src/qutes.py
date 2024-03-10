"""A compiler for Qutes Lang source file"""

import sys
import argparse
from antlr4 import FileStream, CommonTokenStream
from anytree import RenderTree
from qutes_lexer import QutesLexer
from qutes_parser import QutesParser
from qutes_grammar_visitor import QutesGrammarVisitor
from symbols_discovery_visitor import SymbolsDiscoveryVisitor
from quantum_circuit import QuantumCircuitHandler

def main(argv):
    """Entrypoint for Qutes Lang compiler"""

    log_symbols_scope = True
    log_lisp_tree = False
    log_quantum_circuit = True
    number_of_iterations = 1000

    parser = argparse.ArgumentParser(description='Compile Qutes Lang source code.')
    parser.add_argument('file_path', metavar='file_path', help='The file path of the Qutes source code.')
    args = parser.parse_args()

    input_stream = FileStream(args.file_path)
    lexer = QutesLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = QutesParser(stream)
    tree = parser.program()

    if parser.getNumberOfSyntaxErrors() > 0:
        print("syntax errors")
    else:
        quantum_circuit_handler = QuantumCircuitHandler()

        grammar_listener = SymbolsDiscoveryVisitor(quantum_circuit_handler)
        grammar_listener.visit(tree)

        symbols_tree = grammar_listener.scope_handler.symbols_tree
        
        grammar_visitor = QutesGrammarVisitor(symbols_tree, quantum_circuit_handler)
        result = str(grammar_visitor.visit(tree))
        
        print()
        print("----Result----")
        print(result.replace("\n", "", 1))
        
        if(log_symbols_scope):
            print()
            print("----Symbols Scope----")
            for pre, _, node in RenderTree(symbols_tree):
                print("%s%s(%s) Symbols: %s" % (pre, node.scope_class, node.scope_type_detail, node.symbols))

        if(log_lisp_tree):
            print()
            lisp_tree_str = tree.toStringTree(recog=parser)
            print("-------Lisp Tree--------")
            print(lisp_tree_str)
        
        if(log_quantum_circuit):
            print()
            print("----Quantum Circuit----")
            circuit = quantum_circuit_handler.create_circuit()
            quantum_circuit_handler.print_circuit(circuit)
            quantum_circuit_handler.run_circuit(circuit, number_of_iterations)

        print()

if __name__ == '__main__':
    main(sys.argv)
