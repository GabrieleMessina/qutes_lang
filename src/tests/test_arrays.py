from .qutes_base_test import QutesBaseTest
from symbols.types import Qubit, Quint, Qustring, QuantumArrayType
from quantum_circuit.state_preparation import StatePreparation

class TestArrays(QutesBaseTest):
    def assert_arrays_test(self, code, var_name, expected_value_of_var):
        result = self.parse_qutes_code(code)
        actual_value_of_var = result.variables_handler.get_variable_symbol(var_name, self.TOKEN_AST_INDEX_FOR_TESTS).value
        if isinstance(actual_value_of_var, list):
            actual_value_of_var = [symbol.value for symbol in actual_value_of_var]
        self.assertListEqual(actual_value_of_var, expected_value_of_var, f"Expected value: {expected_value_of_var}, actual value: {actual_value_of_var}")

    def test_quantum_type_declaration_succeed(self):
        params = [
            ("qubit[]", "[|+>, |->]", [Qubit(0.5, 0.5), Qubit(0.5, -0.5)]),
            ("qubit[]", "[1q, |->]", [Qubit(0, 1), Qubit(0.5, -0.5)]),
            ("quint[]", "[2q, 3q]", [Quint.fromValue(2), Quint.fromValue(3)]),
            ("quint[]", "[[[0,1]q, 1q]q, 3q]", [Quint(StatePreparation([complex(0), complex(1), complex(0), complex(1)])), Quint.fromValue(3)]),
            ("qustring[]", "[\"101\"q, \"001\"q]", [Qustring.fromValue("101"), Qustring.fromValue("001")]),
        ]
        var_name:str = "foo"
        for var_type, declaration_value, expected_values_of_array in params:
            with self.subTest(var_type=var_type, declaration_value=declaration_value, expected_values_of_array=expected_values_of_array):
                code =  f"""
                        {var_type} {var_name} = {declaration_value};
                        """
                self.assert_arrays_test(code, var_name, expected_values_of_array)

    def test_quantum_type_declaration_throws(self):
        params = [
            ("qubit[]", "[2q]"),
            ("qubit[]", "[2q, |->]"),
            ("qubit[]", "[|->, 2q]"),
            ("quint[]", "[\"11\"q]"),
            ("quint[]", "[\"11\"q, 3q]"),
            ("quint[]", "[3q, \"11\"q]"),
            ("qustring[]", "[1q]"),
            ("qustring[]", "[1q, \"11\"q]"),
            ("qustring[]", "[\"11\"q, 1q]"),
            ("qustring[]", "[3q]"),
            ("qustring[]", "[3q, \"11\"q]"),
            ("qustring[]", "[\"11\"q, 3q]"),
            ("qustring[]", "[|->]"),
            ("qustring[]", "[|->, \"11\"q]"),
            ("qustring[]", "[\"11\"q, |->]"),
        ]
        var_name:str = "foo"
        for var_type, declaration_value in params:
            with self.subTest(var_type=var_type, declaration_value=declaration_value):
                code =  f"""
                        {var_type} {var_name} = {declaration_value};
                        """
                with self.assertRaises((SyntaxError, TypeError)):
                    self.parse_qutes_code(code)
