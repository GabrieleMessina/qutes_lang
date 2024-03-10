import unittest
from parameterized import parameterized
from antlr4 import CommonTokenStream, InputStream
from grammar_frontend.qutes_lexer import QutesLexer
from grammar_frontend.qutes_parser import QutesParser
from grammar_frontend.qutes_grammar_visitor import QutesGrammarVisitor
from grammar_frontend.symbols_discovery_visitor import SymbolsDiscoveryVisitor
from symbols.scope_handler import ScopeHandlerForSymbolsUpdate
from symbols.variables_handler import VariablesHandler
from symbols.types import Qubit, Quint, Qustring
from quantum_circuit import QuantumCircuitHandler

class TestGrammarResult:
    def __init__(self, result, scope_handler:ScopeHandlerForSymbolsUpdate, variables_handler:VariablesHandler, quantum_circuit_handler:QuantumCircuitHandler):
        self.result = result
        self.scope_handler:ScopeHandlerForSymbolsUpdate = scope_handler
        self.variables_handler:VariablesHandler = variables_handler
        self.quantum_circuit_handler:QuantumCircuitHandler = quantum_circuit_handler

class TestGrammar(unittest.TestCase):
    def run_qutes_code(self, code:str) -> TestGrammarResult:
        input_stream = InputStream(code)
        lexer = QutesLexer(input_stream)
        stream = CommonTokenStream(lexer)
        parser = QutesParser(stream)
        tree = parser.program()

        quantum_circuit_handler = QuantumCircuitHandler()
        grammar_listener = SymbolsDiscoveryVisitor(quantum_circuit_handler)
        grammar_listener.visit(tree)
        symbols_tree = grammar_listener.scope_handler.symbols_tree

        scope_handler = ScopeHandlerForSymbolsUpdate(symbols_tree)
        #TODO: This is a workaround to avoid the variable scope to be destroyed after program execution.
        scope_handler_to_work_on = ScopeHandlerForSymbolsUpdate(symbols_tree)
        variables_handler = VariablesHandler(scope_handler, quantum_circuit_handler)

        grammar_visitor = QutesGrammarVisitor(symbols_tree, quantum_circuit_handler, scope_handler_to_work_on, variables_handler)
        result = grammar_visitor.visit(tree)
        return TestGrammarResult(result, scope_handler, variables_handler, quantum_circuit_handler)

    @parameterized.expand([
        ["bool", "foo", "false", False],
        ["bool", "foo", "0", False],
        ["bool", "foo", "TRUE", True],
        ["bool", "foo", "1", True],
        ["bool", "foo", "1q", True],
        ["bool", "foo", "0q", False],
        ["int", "foo", "10", 10],
        ["int", "foo", "false+false", 0],
        ["int", "foo", "true+true", 2],
        ["int", "foo", "10q", 10],
        ["string", "foo", "\"test\"", "test"],
        ["string", "foo", "\"test\" + \"sum\"", "testsum"],
        ["string", "foo", "1", "True"], #TODO: We should expect "1" not "True"
        ["string", "foo", "2", "2"],
    ])
    def test_classic_type_declaration_succeed(self, var_type, var_name, declaration_value, expected_value_of_var):
        code =  f"""
                {var_type} {var_name} = {declaration_value};
                """
        result = self.run_qutes_code(code)
        actual_value_of_var = result.variables_handler.get_variable_symbol(var_name, 0).value
        self.assertEquals(actual_value_of_var, expected_value_of_var, f"Expected value: {expected_value_of_var}, actual value: {actual_value_of_var}")

    
    @parameterized.expand([
        ["bool", "foo", "10"],
        ["bool", "foo", "\"test\""],
        ["bool", "foo", "10q"],
        ["int", "foo", "\"test\""],
        ["string", "foo", "0q"],
        ["string", "foo", "2q"],
    ])
    def test_classic_type_declaration_fail(self, var_type, var_name, declaration_value):
        code =  f"""
                {var_type} {var_name} = {declaration_value};
                """
        with self.assertRaises(SyntaxError):
            result = self.run_qutes_code(code)


    @parameterized.expand([
        ["qubit", "foo", "0q", Qubit()],
        ["qubit", "foo", "0", Qubit()],
        ["qubit", "foo", "true", Qubit(0,1)],
        ["qubit", "foo", "|+>", Qubit(0.5, 0.5)],
        ["qubit", "foo", "|->", Qubit(0.5, -0.5)],
        ["quint", "foo", "10q", Quint.fromValue(10)],
        ["quint", "foo", "false", Quint.fromValue(0)],
        ["quint", "foo", "[[0,1]q, 1q]", Quint([Qubit(0.5, 0.5), Qubit(0, 1)])],
        ["qustring", "foo", "\"test\"", Qustring.fromValue("test")],
        ["qustring", "foo", "\"t*st\"", Qustring.fromValue("t*st")],
    ])
    def test_quantum_type_declaration_succeed(self, var_type, var_name, declaration_value, expected_value_of_var):
        code =  f"""
                {var_type} {var_name} = {declaration_value};
                """
        result = self.run_qutes_code(code)
        actual_value_of_var = str(result.variables_handler.get_variable_symbol(var_name, 0).value)
        self.assertEquals(actual_value_of_var, str(expected_value_of_var), f"Expected value: {expected_value_of_var}, actual value: {actual_value_of_var}")

if __name__ == '__main__':
    unittest.main()