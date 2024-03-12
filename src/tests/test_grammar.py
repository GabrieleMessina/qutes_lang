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
    TOKEN_AST_INDEX_FOR_TESTS = 100000

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
        variables_handler = VariablesHandler(scope_handler, quantum_circuit_handler)

        grammar_visitor = QutesGrammarVisitor(symbols_tree, quantum_circuit_handler, scope_handler, variables_handler)
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
        actual_value_of_var = result.variables_handler.get_variable_symbol(var_name, self.TOKEN_AST_INDEX_FOR_TESTS).value
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
        # with self.assertRaises(SyntaxError):
        with self.assertRaises(TypeError):
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
        ["qustring", "foo", "1q", Qustring.fromValue(Qubit(0,1))],
        ["qustring", "foo", "|+>", Qustring.fromValue(Qubit(0.5, 0.5))],
    ])
    def test_quantum_type_declaration_succeed(self, var_type, var_name, declaration_value, expected_value_of_var):
        code =  f"""
                {var_type} {var_name} = {declaration_value};
                """
        result = self.run_qutes_code(code)

        actual_value_of_var = str(result.variables_handler.get_variable_symbol(var_name, self.TOKEN_AST_INDEX_FOR_TESTS).value)
        self.assertEquals(actual_value_of_var, str(expected_value_of_var), f"Expected value: {expected_value_of_var}, actual value: {actual_value_of_var}")

    @parameterized.expand([
        ["qubit", "foo", "10"],
        ["qubit", "foo", "10q"],
        ["qubit", "foo", "\"test\""],
        ["quint", "foo", "\"test\""],
        ["qustring", "foo", "10q"],
        ["qustring", "foo", "[[0,1]q, 1q]"],
        ["qustring", "foo", "false"],
    ])
    def test_quantum_type_declaration_fail(self, var_type, var_name, declaration_value):
        code =  f"""
                {var_type} {var_name} = {declaration_value};
                """
        with self.assertRaises(TypeError):
            result = self.run_qutes_code(code)

    def test_double_variable_declaration_fail(self):
        code =  f"""
                quint a = 5q;
                string a = "";
                """
        with self.assertRaises(SyntaxError):
            result = self.run_qutes_code(code)

    def test_variable_shadowing_succeed(self):
        var_name = "a"
        expected_value_of_var = "test"
        declaration_value_of_var = "\"test\""
        code =  f"""
                quint {var_name} = 5q;
                {{ string {var_name} = {declaration_value_of_var}; }}
                """
        result = self.run_qutes_code(code)
        result.scope_handler.push_scope()
        actual_value_of_var = str(result.variables_handler.get_variable_symbol(var_name, self.TOKEN_AST_INDEX_FOR_TESTS).value)
        self.assertEquals(actual_value_of_var, str(expected_value_of_var), f"Expected value: {expected_value_of_var}, actual value: {actual_value_of_var}")

    @parameterized.expand([
        ["\"00111111\"", "\"01\""],
        # ["\"001111\"", "\"01\""], #TODO: handle array not being power of size_char
        ["\"0011\"", "\"01\""],
        ["\"0011\"", "\"0\""],
        ["\"0011\"", "\"1\""],
        ["\"1\"", "\"1\""],
        ["\"0\"", "\"0\""],
        ["\"0111110\"", "\"01\", \"10\""],
        ["\"1110111\"", "\"0\""],
        ["\"0001000\"", "\"1\""],
    ])
    def test_grover_search_succeed(self, array, pattern_to_match):
        var_name = "found"
        expected_value_of_var = True
        code =  f"""
                bool {var_name} = false;
                qustring a = {array};
                if({pattern_to_match} in a){{
                    {var_name} = true;
                }}
                """
        result = self.run_qutes_code(code)
        actual_value_of_var = str(result.variables_handler.get_variable_symbol(var_name, self.TOKEN_AST_INDEX_FOR_TESTS).value)
        self.assertEquals(actual_value_of_var, str(expected_value_of_var), f"Expected value: {expected_value_of_var}, actual value: {actual_value_of_var}")

    @parameterized.expand([
        ["\"01111111\"", "\"00\""],
        ["\"001111\"", "\"000\""],
        ["\"0011\"", "\"111\""],
        ["\"0011\"", "\"11111\""],
    ])
    def test_grover_search_fail(self, array, pattern_to_match):
        var_name = "found"
        expected_value_of_var = False
        code =  f"""
                bool {var_name} = false;
                qustring a = {array};
                if({pattern_to_match} in a){{
                    {var_name} = true;
                }}
                """
        result = self.run_qutes_code(code)
        actual_value_of_var = str(result.variables_handler.get_variable_symbol(var_name, self.TOKEN_AST_INDEX_FOR_TESTS).value)
        self.assertEquals(actual_value_of_var, str(expected_value_of_var), f"Expected value: {expected_value_of_var}, actual value: {actual_value_of_var}")

if __name__ == '__main__':
    unittest.main()