from symbols.types import Qubit, Quint, Qustring
from .qutes_base_test import QutesBaseTest
from grammar_frontend.qutes_grammar_visitor import QutesGrammarVisitor
from qutes_antlr.qutes_parserVisitor import __name__ as qutes_parserVisitor_class_name
import inspect

def sanitizeForVariableDeclarationUsage(value:any) -> str:
    value = str(value)
    return value.replace("\"", "").replace(" ", "")

class TestGrammar(QutesBaseTest):
    def test_all_visitor_method_implemented(self):
        visitor_methods = [method for method in inspect.getmembers(QutesGrammarVisitor, predicate=inspect.isfunction) if not method[0].startswith("_")]
        for method in visitor_methods:
            with self.subTest(method=method):
                method_module = method[1].__module__
                method_name = method[1].__name__
                self.assertNotEqual(qutes_parserVisitor_class_name, method_module, f"Method {method_name} was never explicitly implemented.")

    def test_var_declaration_with_allowed_char_succeed(self):
        params = [
            ("a"),
            ("A"),
            ("z"),
            ("Z"),
            ("_"),
            ("_1234"),
            ("_1234asd"),
            ("_1234asASASd"),
            ("_sdas1234"),
            ("_sdaASDASs1234"),
            ("__sdas1234"),
            ("__sdASaSas1234"),
            ("asdf__23w"),
            ("aASASdf__23wASSA"),
            ("asdf1234r_"),
            ("asdfASAS1234r_"),
            ("asdf1234r__"),
            ("asASSASdf1234r__"),
        ]
        for var_name in params:
            with self.subTest(var_name=var_name):
                code =  f"""
                        bool {var_name};
                        """
                self.parse_qutes_code(code)

    def test_var_declaration_with_unexpected_char_throws(self):
        params = [
            ("1"),
            ("121212"),
            ("1221___"),
            ("1221___1212"),
            ("1221___asasa"),
            ("1221asasa___"),
            ("1221as___asa___"),
            ("1221asassa_Asas"),
            ("ass-asas"),
            ("ass(asas"),
            ("ass*asas"),
            ("ass&asas"),
            ("&assasas"),
            ("___&assasas"),
            ("___assasas&"),
        ]
        for var_name in params:
            with self.subTest(var_name=var_name):
                code =  f"""
                        bool {var_name};
                        """
                with self.assertRaises(SyntaxError):
                    self.parse_qutes_code(code)

    def test_classic_type_declaration_succeed(self):
        params = [
            ("bool", "false", False),
            ("bool", "0", False),
            ("bool", "TRUE", True),
            ("bool", "1", True),
            ("bool", "1q", True), #TODO: handle, the quantum var should be declared even when anonymous, so we can measure and assign the value to bool.
            ("bool", "0q", False),
            ("int", "10", 10),
            ("int", "false+false", 0),
            ("int", "true+true", 2),
            ("int", "10q", 10),
            ("string", "\"test\"", "test"),
            ("string", "\"test\" + \"sum\"", "testsum"),
            ("string", "1", "True"), #TODO: We should expect "1" not "True"
            ("string", "2", "2"),
        ]
        var_name:str = "foo"
        for var_type, declaration_value, expected_value_of_var in params:
            with self.subTest(var_type=var_type, declaration_value=declaration_value, expected_value_of_var=expected_value_of_var):
                code =  f"""
                        {var_type} {var_name} = {declaration_value};
                        """
                result = self.parse_qutes_code(code)
                actual_value_of_var = result.variables_handler.get_variable_symbol(var_name, self.TOKEN_AST_INDEX_FOR_TESTS).value
                self.assertEqual(actual_value_of_var, expected_value_of_var, f"Expected value: {expected_value_of_var}, actual value: {actual_value_of_var}")

    def test_classic_type_declaration_throws(self):
        params = [
            ("bool", "10"),
            ("bool", "\"test\""),
            ("bool", "10q"),
            ("int", "\"test\""),
            ("string", "0q"),
            ("string", "2q"),
        ]
        var_name:str = "foo"
        for var_type, declaration_value in params:
            with self.subTest(var_type=var_type, declaration_value=declaration_value):
                code =  f"""
                        {var_type} {var_name} = {declaration_value};
                        """
                with self.assertRaises(TypeError):
                    self.parse_qutes_code(code)


    def test_quantum_type_declaration_succeed(self):
        params = [
            ("qubit", "0q", Qubit()),
            ("qubit", "0", Qubit()),
            ("qubit", "true", Qubit(0,1)),
            ("qubit", "|+>", Qubit(0.5, 0.5)),
            ("qubit", "|->", Qubit(0.5, -0.5)),
            ("quint", "10q", Quint.fromValue(10)),
            ("quint", "false", Quint.fromValue(0)),
            ("quint", "[[0,1]q, 1q]", Quint([Qubit(0.5, 0.5), Qubit(0, 1)])),
            ("qustring", "\"test\"", Qustring.fromValue("test")),
            ("qustring", "\"t*st\"", Qustring.fromValue("t*st")),
            ("qustring", "1q", Qustring.fromValue(Qubit(0,1))),
            ("qustring", "|+>", Qustring.fromValue(Qubit(0.5, 0.5))),
        ]
        var_name:str = "foo"
        for var_type, declaration_value, expected_value_of_var in params:
            with self.subTest(var_type=var_type, declaration_value=declaration_value, expected_value_of_var=expected_value_of_var):
                code =  f"""
                        {var_type} {var_name} = {declaration_value};
                        """
                result = self.parse_qutes_code(code)

                actual_value_of_var = str(result.variables_handler.get_variable_symbol(var_name, self.TOKEN_AST_INDEX_FOR_TESTS).value)
                self.assertEqual(actual_value_of_var, str(expected_value_of_var), f"Expected value: {expected_value_of_var}, actual value: {actual_value_of_var}")

    def test_quantum_type_declaration_throws(self):
        params = [
            ("qubit", "10"),
            ("qubit", "10q"),
            ("qubit", "\"test\""),
            ("quint", "\"test\""),
            ("qustring", "10q"),
            ("qustring", "[[0,1]q, 1q]"),
            ("qustring", "false"),
        ]
        for var_type, declaration_value in params:
            with self.subTest("var_type, declaration_value", var_type=var_type, declaration_value=declaration_value):
                var_name:str = "foo"
                code =  f"""
                        {var_type} {var_name} = {declaration_value};
                        """
                with self.assertRaises(TypeError):
                    self.parse_qutes_code(code)

    def test_double_variable_declaration_throws(self):
        code =  """
                quint a = 5q;
                string a = "";
                """
        with self.assertRaises(SyntaxError):
            self.parse_qutes_code(code)

    def test_variable_shadowing_succeed(self):
        var_name = "a"
        expected_value_of_var = "test"
        declaration_value_of_var = "\"test\""
        code =  f"""
                quint {var_name} = 5q;
                {{ string {var_name} = {declaration_value_of_var}; }}
                """
        result = self.parse_qutes_code(code)
        result.scope_handler.push_scope()
        actual_value_of_var = str(result.variables_handler.get_variable_symbol(var_name, self.TOKEN_AST_INDEX_FOR_TESTS).value)
        self.assertEqual(actual_value_of_var, str(expected_value_of_var), f"Expected value: {expected_value_of_var}, actual value: {actual_value_of_var}")
