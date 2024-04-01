"""A compiler for Qutes Lang source file"""

import sys
import argparse
from antlr4 import FileStream, CommonTokenStream
from anytree import RenderTree
from grammar_frontend.qutes_lexer import QutesLexer
from grammar_frontend.qutes_parser import QutesParser
from grammar_frontend.qutes_grammar_visitor import QutesGrammarVisitor
from grammar_frontend.symbols_discovery_visitor import SymbolsDiscoveryVisitor
from grammar_frontend.qutes_syntax_error_listener import QutesErrorListener
from symbols.scope_handler import ScopeHandlerForSymbolsUpdate
from symbols.variables_handler import VariablesHandler
from quantum_circuit import QuantumCircuitHandler

def main(argv):
    """Entrypoint for Qutes Lang compiler"""

    parser = argparse.ArgumentParser(description='Compile Qutes Lang source code.')
    parser.add_argument('-scope', '--log_symbols_scope', dest='log_symbols_scope', action='store_true', help='Toggle symbols scope print on console.')
    parser.add_argument('-tree', '--log_ast_tree', dest='log_ast_tree', action='store_true', help='Toggle syntax tree print on console.')
    parser.add_argument('-circuit', '--log_quantum_circuit', dest='log_quantum_circuit', action='store_true', help='Toggle quantum cicuit print on console.')
    parser.add_argument('-image', '--print_circuit_as_image', dest='save_circuit_as_image', action='store_true', help='Toggle circuit export as image instead of console print as text.')
    parser.add_argument('-v', '--verbose', dest='log_verbose', action='store_true', help='Print all log as verbose on console.')
    parser.add_argument('-iter', '--number_of_iterations', dest='number_of_iterations', default='100', action='store', type=int, help='Set number of iteration for quauntum circuit run.')
    parser.add_argument('file_path', metavar='file_path', help='The file path of the Qutes source code.')
    args = parser.parse_args()

    input_stream = FileStream(args.file_path)
    lexer = QutesLexer(input_stream)
    lexer.removeErrorListeners()
    lexer.addErrorListener(QutesErrorListener())
    
    stream = CommonTokenStream(lexer)
    parser = QutesParser(stream)
    parser.removeErrorListeners()
    parser.addErrorListener(QutesErrorListener())

    tree = parser.program()

    if parser.getNumberOfSyntaxErrors() > 0:
        raise SyntaxError()

    quantum_circuit_handler = QuantumCircuitHandler()

    grammar_listener = SymbolsDiscoveryVisitor(quantum_circuit_handler)
    grammar_listener.visit(tree)

    symbols_tree = grammar_listener.scope_handler.symbols_tree
    
    scope_handler = ScopeHandlerForSymbolsUpdate(symbols_tree)
    variables_handler = VariablesHandler(scope_handler, quantum_circuit_handler)

    grammar_visitor = QutesGrammarVisitor(symbols_tree, quantum_circuit_handler, scope_handler, variables_handler, args.log_verbose)
    result = str(grammar_visitor.visit(tree))
    
    print()
    print("----Result----")
    print(result.replace("\n", "", 1))
    
    if(args.log_symbols_scope):
        print()
        print("----Symbols Scope----")
        for pre, _, node in RenderTree(symbols_tree):
            print("%s%s(%s) Symbols: %s" % (pre, node.scope_class, node.scope_type_detail, node.symbols))

    if(args.log_ast_tree):
        print()
        ast_tree_str = tree.toStringTree(recog=parser)
        print("-------Abstract Syntax Tree--------")
        print(ast_tree_str)
    
    print()
    print("----Quantum Circuit----")
    circuit = quantum_circuit_handler.create_circuit()
    quantum_circuit_handler.print_circuit(circuit, args.save_circuit_as_image, args.log_quantum_circuit)
    quantum_circuit_handler.run_circuit(circuit, args.number_of_iterations, print_count=True)

    print()

if __name__ == '__main__':
    main(sys.argv)
