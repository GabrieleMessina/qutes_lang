import unittest
from antlr4 import CommonTokenStream, InputStream
from qutes_lexer import QutesLexer
from qutes_parser import QutesParser
from qutes_grammar_visitor import QutesGrammarVisitor
from symbols_discovery_visitor import SymbolsDiscoveryVisitor
from quantum_circuit import QuantumCircuitHandler

class TestGrammar(unittest.TestCase):
    def run_qutes_code(self, code:str) -> any:
        input_stream = InputStream(code)
        lexer = QutesLexer(input_stream)
        stream = CommonTokenStream(lexer)
        parser = QutesParser(stream)
        tree = parser.program()

        quantum_circuit_handler = QuantumCircuitHandler()
        grammar_listener = SymbolsDiscoveryVisitor(quantum_circuit_handler)
        grammar_listener.visit(tree)
        symbols_tree = grammar_listener.scope_handler.symbols_tree
        grammar_visitor = QutesGrammarVisitor(symbols_tree, quantum_circuit_handler)
        return grammar_visitor.visit(tree)

    def test_upper(self):
        code =  """
                int a = 10;
                """
        result = self.run_qutes_code(code)
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

if __name__ == '__main__':
    unittest.main()