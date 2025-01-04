"""A compiler for Qutes Lang source file"""

import sys, os
import argparse
from antlr4 import FileStream, CommonTokenStream
from anytree import RenderTree
from grammar_frontend.shared.qutes_lexer import QutesLexer
from grammar_frontend.shared.qutes_parser import QutesParser
from grammar_frontend.code_execution.code_execution_visitor import CodeExecutionVisitor
from grammar_frontend.symbols_discovery.symbols_discovery_visitor import SymbolsDiscoveryVisitor
from grammar_frontend.shared.qutes_syntax_error_listener import QutesErrorListener
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

    user_qutes_program_name = os.path.basename(args.file_path)
    input_stream = FileStream(args.file_path, encoding='utf-8')
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

    symbol_discovery_visitor = SymbolsDiscoveryVisitor(quantum_circuit_handler, args.log_verbose)
    symbol_discovery_visitor.visit(tree)

    symbols_tree = symbol_discovery_visitor.scope_handler.get_symbols_tree()
    scopes_stack = symbol_discovery_visitor.scope_handler.get_scopes_stack()
    
    scope_handler = ScopeHandlerForSymbolsUpdate(symbols_tree)
    variables_handler = VariablesHandler(scope_handler, quantum_circuit_handler)

    code_execution_visitor = CodeExecutionVisitor(symbols_tree, quantum_circuit_handler, scope_handler, variables_handler, args.log_verbose)
    result = str(code_execution_visitor.visit(tree))
    
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
    quantum_circuit_handler.print_circuit(circuit, args.save_circuit_as_image, args.log_quantum_circuit, user_qutes_program_name)
    quantum_circuit_handler.run_circuit(circuit, args.number_of_iterations, print_count=True)

    print()

if __name__ == '__main__':
    main(sys.argv)
