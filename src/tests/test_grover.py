from .qutes_base_test import QutesBaseTest

class TestGrover(QutesBaseTest):
    TOKEN_AST_INDEX_FOR_TESTS = 100000

    def test_grover_search_succeed(self):
        params = [
            ("\"00111111\"", "\"01\""),
            # ["\"001111\"", "\"01\""), #TODO: handle array not being power of size_char
            ("\"0011\"", "\"01\""),
            ("\"0011\"", "\"0\""),
            ("\"0011\"", "\"1\""),
            ("\"1\"", "\"1\""),
            ("\"0\"", "\"0\""),
            ("\"0111110\"", "\"01\", \"10\""),
            ("\"1110111\"", "\"0\""),
            ("\"0001000\"", "\"1\""),
        ]
        var_name = "found"
        expected_value_of_var = True
        for array, pattern_to_match in params:
            with self.subTest(array=array, pattern_to_match=pattern_to_match):
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

    def test_grover_search_throws(self):
        params = [
            ("\"01111111\"", "\"00\""),
            ("\"001111\"", "\"000\""),
            ("\"0011\"", "\"111\""),
            ("\"0011\"", "\"11111\""),
        ]
        var_name = "found"
        expected_value_of_var = False

        for array, pattern_to_match in params:
            with self.subTest(array=array, pattern_to_match=pattern_to_match):
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