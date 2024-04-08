import unittest
from antlr4 import CommonTokenStream, InputStream
from grammar_frontend.qutes_lexer import QutesLexer
from grammar_frontend.qutes_parser import QutesParser
from grammar_frontend.qutes_grammar_visitor import QutesGrammarVisitor
from grammar_frontend.symbols_discovery_visitor import SymbolsDiscoveryVisitor
from grammar_frontend.qutes_syntax_error_listener import QutesErrorListener
from symbols.scope_handler import ScopeHandlerForSymbolsUpdate
from symbols.variables_handler import VariablesHandler
from quantum_circuit import QuantumCircuitHandler

class QutesTestResult:
    def __init__(self, result, scope_handler:ScopeHandlerForSymbolsUpdate, variables_handler:VariablesHandler, quantum_circuit_handler:QuantumCircuitHandler):
        self.result = result
        self.scope_handler:ScopeHandlerForSymbolsUpdate = scope_handler
        self.variables_handler:VariablesHandler = variables_handler
        self.quantum_circuit_handler:QuantumCircuitHandler = quantum_circuit_handler

class QutesBaseTest(unittest.TestCase):
    TOKEN_AST_INDEX_FOR_TESTS = 100000

    def parse_qutes_code(self, code:str) -> QutesTestResult:
        input_stream = InputStream(code)
        lexer = QutesLexer(input_stream)
        lexer.removeErrorListeners()
        lexer.addErrorListener(QutesErrorListener())
        
        stream = CommonTokenStream(lexer)
        parser = QutesParser(stream)
        parser.removeErrorListeners()
        parser.addErrorListener(QutesErrorListener())
        tree = parser.program()

        quantum_circuit_handler = QuantumCircuitHandler()
        grammar_listener = SymbolsDiscoveryVisitor(quantum_circuit_handler)
        grammar_listener.visit(tree)
        symbols_tree = grammar_listener.scope_handler.symbols_tree

        scope_handler = ScopeHandlerForSymbolsUpdate(symbols_tree)
        variables_handler = VariablesHandler(scope_handler, quantum_circuit_handler)

        grammar_visitor = QutesGrammarVisitor(symbols_tree, quantum_circuit_handler, scope_handler, variables_handler)
        result = grammar_visitor.visit(tree)

        return QutesTestResult(result, scope_handler, variables_handler, quantum_circuit_handler)

if __name__ == '__main__':
    unittest.main()