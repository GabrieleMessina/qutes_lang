from .qutes_base_test import QutesBaseTest

class TestArrayAccess(QutesBaseTest):
    def assert_operation_test(self, code, var_name, expected_value_of_var):
        result = self.parse_qutes_code(code)
        actual_value_of_var = str(result.variables_handler.get_variable_symbol(var_name, self.TOKEN_AST_INDEX_FOR_TESTS).value)
        self.assertEqual(actual_value_of_var, str(expected_value_of_var), f"Expected value: {expected_value_of_var}, actual value: {actual_value_of_var}")

    def test_left_shift_return_expected_value(self):
        params = [
            ("\"01111111\"", "0", "01111111"),
        ]
        var_name = "a"
        var_result_name = "result"
        for init_string, n_shift, expected_value_of_var in params:
            with self.subTest(init_string=init_string, n_shift=n_shift, expected_value_of_var=expected_value_of_var):
                code =  f"""
                        qustring {var_name} = {init_string};
                        {var_name} << {n_shift};
                        string {var_result_name} = {var_name};
                        """
                self.assert_operation_test(code, var_result_name, expected_value_of_var)
