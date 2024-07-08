from .qutes_base_test import QutesBaseTest

class TestOperation(QutesBaseTest):
    TOKEN_AST_INDEX_FOR_TESTS = 100000

    def assert_operation_test(self, code, var_name, expected_value_of_var):
        result = self.parse_qutes_code(code)
        actual_value_of_var = str(result.variables_handler.get_variable_symbol(var_name, self.TOKEN_AST_INDEX_FOR_TESTS).value)
        self.assertEqual(actual_value_of_var, str(expected_value_of_var), f"Expected value: {expected_value_of_var}, actual value: {actual_value_of_var}")

    def test_left_shift_return_expected_value(self):
        params = [
            ("\"01111111\"", "0", "01111111"),
            ("\"0111111\"", "0", "0111111"),
            ("\"01111111\"", "1", "11111110"),
            ("\"0111111\"", "1", "1111110"),
            ("\"01111111\"", "2", "11111101"),
            ("\"0111111\"", "2", "1111101"),
            ("\"01111111\"", "3", "11111011"),
            ("\"0111111\"", "3", "1111011"),
            ("\"01111111\"", "4", "11110111"),
            ("\"0111111\"", "4", "1110111"),
            ("\"01111111\"", "5", "11101111"),
            ("\"0111111\"", "5", "1101111"),
            ("\"01111111\"", "6", "11011111"),
            ("\"0111111\"", "6", "1011111"),
            ("\"01111111\"", "7", "10111111"),
            ("\"0111111\"", "7", "0111111"),
            ("\"01111111\"", "8", "01111111"),
            ("\"0111111\"", "8", "1111110"),
            ("\"01111111\"", "9", "11111110"),
            ("\"0111111\"", "9", "1111101"),
        ]
        var_name = "a"
        var_result_name = "result"
        for init_string, n_shift, expected_value_of_var in params:
            with self.subTest(init_string=init_string, n_shift=n_shift, expected_value_of_var=expected_value_of_var):
                code =  f"""
                        qustring {var_name} = {init_string};
                        {var_name} >> {n_shift};
                        string {var_result_name} = {var_name};
                        """
                self.assert_operation_test(code, var_result_name, expected_value_of_var)

    def test_right_shift_return_expected_value(self):
        params = [
            ("\"01111111\"", "0", "01111111"),
            ("\"0111111\"", "0", "0111111"),
            ("\"01111111\"", "1", "10111111"),
            ("\"0111111\"", "1", "1011111"),
            ("\"01111111\"", "2", "11011111"),
            ("\"0111111\"", "2", "1101111"),
            ("\"01111111\"", "3", "11101111"),
            ("\"0111111\"", "3", "1110111"),
            ("\"01111111\"", "4", "11110111"),
            ("\"0111111\"", "4", "1111011"),
            ("\"01111111\"", "5", "11111011"),
            ("\"0111111\"", "5", "1111101"),
            ("\"01111111\"", "6", "11111101"),
            ("\"0111111\"", "6", "1111110"),
            ("\"01111111\"", "7", "11111110"),
            ("\"0111111\"", "7", "0111111"),
            ("\"01111111\"", "8", "01111111"),
            ("\"0111111\"", "8", "1011111"),
            ("\"01111111\"", "9", "10111111"),
            ("\"0111111\"", "9", "1101111"),
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
