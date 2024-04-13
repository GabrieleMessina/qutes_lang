from grammar_frontend.qutes_parser import QutesParser as qutes_parser
from symbols.scope_tree_node import ScopeTreeNode
from symbols.symbol import Symbol
from symbols.scope_handler import ScopeHandlerForSymbolsUpdate
from symbols.variables_handler import VariablesHandler
from symbols.types import Qustring, QutesDataType
from quantum_circuit import QuantumCircuitHandler
from grammar_frontend.qutes_base_visitor import QutesBaseVisitor

class QutesGrammarOperationVisitor(QutesBaseVisitor):
    def __init__(self, symbols_tree:ScopeTreeNode, quantum_circuit_handler : QuantumCircuitHandler, scope_handler:ScopeHandlerForSymbolsUpdate, variables_handler:VariablesHandler, verbose:bool = False):
        super().__init__(symbols_tree, quantum_circuit_handler, scope_handler, variables_handler, verbose)
    
    # Visit a parse tree produced by qutes_parser#test.
    def visitTest(self, ctx:qutes_parser.TestContext):
        return self.__visit("visitTest", lambda : self.__visit_test(ctx))

    def __visit_test(self, ctx:qutes_parser.TestContext):
        result = None
        first_term_symbol = self.visitChildren(ctx.term(0))
        second_term_symbol = self.visitChildren(ctx.term(1))
        first_term = self.variables_handler.get_value(first_term_symbol)
        second_term = self.variables_handler.get_value(second_term_symbol)

        if(ctx.GREATER()):
            if(self.log_code_structure): print(f"{first_term_symbol} > {second_term_symbol}", end=None)
            if(self.log_trace_enabled): print("visitTest -> greater")
            result = first_term > second_term
        elif(ctx.LOWER()):
            if(self.log_code_structure): print(f"{first_term_symbol} < {second_term_symbol}", end=None)
            if(self.log_trace_enabled): print("visitTest -> lower")
            result = first_term < second_term
        elif(ctx.EQUAL()):
            if(self.log_code_structure): print(f"{first_term_symbol} == {second_term_symbol}", end=None)
            if(self.log_trace_enabled): print("visitTest -> equal")
            if (first_term_symbol and QutesDataType.is_quantum_type(first_term_symbol.symbol_declaration_static_type)
                and second_term_symbol and not QutesDataType.is_quantum_type(second_term_symbol.symbol_declaration_static_type)):
                # At the moment this only works for comparing quantum variables to classical values.
                result = self.quantum_circuit_handler.push_equals_operation(first_term_symbol.quantum_register, second_term_symbol.value)
            else:
                result = first_term == second_term
        elif(ctx.GREATEREQUAL()):
            if(self.log_code_structure): print(f"{first_term_symbol} >= {second_term_symbol}", end=None)
            if(self.log_trace_enabled): print("visitTest -> greater equal")
            result = first_term >= second_term
        elif(ctx.LOWEREQUAL()):
            if(self.log_code_structure): print(f"{first_term_symbol} <= {second_term_symbol}", end=None)
            if(self.log_trace_enabled): print("visitTest -> lower equal")
            result = first_term <= second_term
        else:
            if(self.log_code_structure): print(f"{first_term_symbol}", end=None)
            if(self.log_trace_enabled): print("visitTest -> test no operator")
            result = first_term
        return result

    # Visit a parse tree produced by qutes_parser#MultipleUnaryPhaseOperator.
    def visitMultipleUnaryPhaseOperator(self, ctx:qutes_parser.MultipleUnaryPhaseOperatorContext):
        return self.__visit("visitMultipleUnaryPhaseOperator", lambda : self.__visitMultipleUnaryPhaseOperator(ctx))

    # Visit a parse tree produced by qutes_parser#MultipleUnaryOperator.
    def visitMultipleUnaryOperator(self, ctx:qutes_parser.MultipleUnaryOperatorContext):
        return self.__visit("visitMultipleUnaryOperator", lambda : self.__visitMultipleUnaryOperator(ctx))

    def __visitMultipleUnaryOperator(self, ctx:qutes_parser.MultipleUnaryOperatorContext):
        terms:list[Symbol] = self.visit(ctx.termList())
        registers = [register.quantum_register for register in terms]
        if(ctx.MCZ()):
            self.quantum_circuit_handler.push_MCZ_operation(registers)
        if(ctx.MCX()):
            self.quantum_circuit_handler.push_MCX_operation(registers)
        if(ctx.MCY()):
            self.quantum_circuit_handler.push_MCY_operation(registers)
        if(ctx.SWAP()):
            self.quantum_circuit_handler.push_swap_operation(registers[0], registers[1])

    def __visitMultipleUnaryPhaseOperator(self, ctx:qutes_parser.MultipleUnaryPhaseOperatorContext):
        terms:list[Symbol] = self.visit(ctx.termList())
        registers = [register.quantum_register for register in terms]
        if(ctx.MCP()):
            theta = self.visit(ctx.expr())
            self.quantum_circuit_handler.push_MCP_operation(theta, registers)

    # Visit a parse tree produced by qutes_parser#termList.
    def visitTermList(self, ctx:qutes_parser.TermListContext):
        term = self.visit(ctx.term())
        terms = []
        if(ctx.termList()):
            terms = self.__visit("visitTermList", lambda : self.visit(ctx.termList()))
            if(not isinstance(terms, list)):
                terms = [terms]
        terms.append(term)
        return terms[::-1]
                
    # Visit a parse tree produced by qutes_parser#IdentityOperator.
    def visitIdentityOperator(self, ctx:qutes_parser.IdentityOperatorContext):
        result = self.__visit_identity_operator(ctx)
        if(self.log_code_structure): print(result, end=None) 
        return self.__visit("visitIdentityOperator", lambda : result)
    
    def __visit_identity_operator(self, ctx:qutes_parser.IdentityOperatorContext):
        result = self.visitChildren(ctx)
        if(ctx.boolean()):
            if(self.log_trace_enabled): print("visitTerm -> boolean")
        if(ctx.integer()):
            if(self.log_trace_enabled): print("visitTerm -> integer")
        if(ctx.float_()):
            if(self.log_trace_enabled): print("visitTerm -> float")
        if(ctx.qubit()):
            if(self.log_trace_enabled): print("visitTerm -> qubit")
        if(ctx.quint()):
            if(self.log_trace_enabled): print("visitTerm -> quint")
        if(ctx.qustring()):
            if(self.log_trace_enabled): print("visitTerm -> qustring")
        if(ctx.qualifiedName()):
            if(self.log_trace_enabled): print("visitTerm -> qualifiedName")
        if(ctx.string()):
            if(self.log_trace_enabled): print("visitTerm -> string")
        if(ctx.MEASURE()):
            if(self.log_trace_enabled): print("visitTerm -> measure")
            self.quantum_circuit_handler.push_measure_operation()
        if(ctx.BARRIER()):
            if(self.log_trace_enabled): print("visitTerm -> barrier")
            self.quantum_circuit_handler.push_barrier_operation()
        return result


    # Visit a parse tree produced by qutes_parser#UnaryOperator.
    def visitUnaryOperator(self, ctx:qutes_parser.UnaryOperatorContext):
         return self.__visit("visitUnaryOperator", lambda : self.__visit_unary_operator(ctx))
    
    def __visit_unary_operator(self, ctx:qutes_parser.UnaryOperatorContext):
        result = None
        if(ctx.term()):
            if(self.log_trace_enabled): print("visitTerm -> unary operation")
            first_term = self.visitChildren(ctx.term())
            first_term_symbol : Symbol | None = None

            if(isinstance(first_term, Symbol)):
                first_term_symbol = first_term
                first_term = first_term.value

            first_term_print = f"{first_term if first_term_symbol == None else first_term_symbol}"

            if(ctx.PRINT()):
                if(self.log_code_structure): print(f"print {first_term_print}", end=None)
                if(self.log_trace_enabled): print("visitUnaryOperator -> PRINT")
                if(first_term_symbol):
                    if(QutesDataType.is_quantum_type(first_term_symbol.symbol_declaration_static_type)):
                        classical_register = self.quantum_circuit_handler.run_and_measure([first_term_symbol.quantum_register])
                        bytes_str = [reg.measured_values[0] for reg in classical_register if first_term_symbol.quantum_register.name in reg.name][0]
                        if(first_term_symbol.symbol_declaration_static_type == QutesDataType.qustring):
                            index = 0
                            string_value = ""
                            while index < first_term_symbol.value.number_of_chars * Qustring.default_char_size:
                                bin_char = bytes_str[index:Qustring.default_char_size + index]
                                string_value = string_value + Qustring.get_char_from_int(int(bin_char, 2))
                                index = index + Qustring.default_char_size
                            print(string_value)
                        else:
                            new_value = int(bytes_str, 2)
                            print(new_value)
                        #TODO: handle the conversion from a string of binadry digits to the current quantum variable type
                        #TODO: adding the next line cause a crash in the circuit 
                        # self.variables_handler.update_variable_state(first_term_symbol.name, new_value) 
                    print(first_term_symbol)
                else:
                    print(first_term)
            if(ctx.ADD()):
                if(self.log_code_structure): print(f"+{first_term_print}", end=None)
                if(self.log_trace_enabled): print("visitUnaryOperator -> ADD")
            if(ctx.SUB()):
                if(self.log_code_structure): print(f"-{first_term_print}", end=None)
                if(self.log_trace_enabled): print("visitUnaryOperator -> SUB")
                if (first_term_symbol and QutesDataType.is_quantum_type(first_term_symbol.symbol_declaration_static_type)):
                    result = self.quantum_circuit_handler.push_pauliz_operation(first_term_symbol.quantum_register)
                result = -first_term
            if(ctx.NOT()):
                if(self.log_code_structure): print(f"NOT{first_term_print}", end=None)
                if(self.log_trace_enabled): print("visitUnaryOperator -> NOT")
                if (first_term_symbol and QutesDataType.is_quantum_type(first_term_symbol.symbol_declaration_static_type)):
                    result = self.quantum_circuit_handler.push_not_operation(first_term_symbol.quantum_register)
                else:
                    result = not first_term
            if(ctx.PAULIY()):
                if(self.log_code_structure): print(f"NOT{first_term_print}", end=None)
                if(self.log_trace_enabled): print("visitUnaryOperator -> NOT")
                if (first_term_symbol and QutesDataType.is_quantum_type(first_term_symbol.symbol_declaration_static_type)):
                    result = self.quantum_circuit_handler.push_pauliy_operation(first_term_symbol.quantum_register)
            if(ctx.PAULIZ()):
                if(self.log_code_structure): print(f"PAULIZ{first_term_print}", end=None)
                if(self.log_trace_enabled): print("visitUnaryOperator -> PAULIZ")
                if (first_term_symbol and QutesDataType.is_quantum_type(first_term_symbol.symbol_declaration_static_type)):
                    result = self.quantum_circuit_handler.push_pauliz_operation(first_term_symbol.quantum_register)
            if(ctx.HADAMARD()):
                if(self.log_code_structure): print(f"HADAMARD{first_term_print}", end=None)
                if(self.log_trace_enabled): print("visitUnaryOperator -> HADAMARD")
                if (first_term_symbol and QutesDataType.is_quantum_type(first_term_symbol.symbol_declaration_static_type)):
                    result = self.quantum_circuit_handler.push_hadamard_operation(first_term_symbol.quantum_register)
            if(ctx.MEASURE()):
                if(self.log_code_structure): print(f"MEASURE{first_term_print}", end=None)
                if(self.log_trace_enabled): print("visitUnaryOperator -> MEASURE")
                if (first_term_symbol and QutesDataType.is_quantum_type(first_term_symbol.symbol_declaration_static_type)):
                    result = self.quantum_circuit_handler.push_measure_operation([first_term_symbol.quantum_register])
        return result


    # Visit a parse tree produced by qutes_parser#BinaryPriorityOperator.
    def visitBinaryPriorityOperator(self, ctx:qutes_parser.BinaryPriorityOperatorContext):
         return self.__visit("visitBinaryPriorityOperator", lambda : self.__visit_binary_operator(ctx))

    # Visit a parse tree produced by qutes_parser#BinaryOperator.
    def visitBinaryOperator(self, ctx:qutes_parser.BinaryOperatorContext):
         return self.__visit("visitBinaryOperator", lambda : self.__visit_binary_operator(ctx))

    def __visit_binary_operator(self, ctx:qutes_parser.BinaryOperatorContext|qutes_parser.BinaryPriorityOperatorContext):
        result = None
        if(ctx.term(0) and ctx.term(1)):
            if(self.log_trace_enabled): print("visitTerm -> binary operation")
            first_term = self.visitChildren(ctx.term(0))
            second_term = self.visitChildren(ctx.term(1))
            first_term_symbol : Symbol | None = None
            second_term_symbol : Symbol | None = None

            if(isinstance(first_term, Symbol)):
                first_term_symbol = first_term
                first_term = first_term.value
            if(isinstance(second_term, Symbol)):
                second_term_symbol = second_term
                second_term = second_term.value
            
            first_term_print = f"{first_term if first_term_symbol == None else first_term_symbol}"
            second_term_print = f"{second_term if second_term_symbol == None else second_term_symbol}"

            if(isinstance(ctx, qutes_parser.BinaryOperatorContext) and ctx.ADD()):
                if(self.log_code_structure): print(f"{first_term_print} + {second_term_print}", end=None)
                if(self.log_trace_enabled): print("visitBinaryOperator -> ADD")
                if (first_term_symbol and QutesDataType.is_quantum_type(first_term_symbol.symbol_declaration_static_type)
                    and second_term_symbol and QutesDataType.is_quantum_type(second_term_symbol.symbol_declaration_static_type)):
                    #TODO: we should measure the circuit and assign the value to the result variable.
                    #But we don't want to measure the circuit at every operation, so we need to return a kind of promise
                    #Promise that will be measured only when needed
                    #At first i was thinking about measure on assignment, but that is not actually needed,
                    #We can measure only when classical computation is required
                    #Or when explicitly required by the user.
                    result = self.qutes_gates.sum(first_term_symbol, second_term_symbol)
                else:
                    result = first_term + second_term
            if(isinstance(ctx, qutes_parser.BinaryOperatorContext) and ctx.SUB()):
                if(self.log_code_structure): print(f"{first_term_print} - {second_term_print}", end=None)
                if(self.log_trace_enabled): print("visitBinaryOperator -> SUB")
                if (first_term_symbol and QutesDataType.is_quantum_type(first_term_symbol.symbol_declaration_static_type)):
                    #TODO: handle sub operation of quantum variables
                    pass
                result = first_term - second_term
            if(isinstance(ctx, qutes_parser.BinaryPriorityOperatorContext) and ctx.MULTIPLY()):
                if(self.log_code_structure): print(f"{first_term_print} - {second_term_print}", end=None)
                if(self.log_trace_enabled): print("visitBinaryOperator -> SUB")
                if (first_term_symbol and QutesDataType.is_quantum_type(first_term_symbol.symbol_declaration_static_type)):
                    #TODO: handle multiply operation of quantum variables
                    pass
                result = first_term * second_term
            if(isinstance(ctx, qutes_parser.BinaryPriorityOperatorContext) and ctx.DIVIDE()):
                if(self.log_code_structure): print(f"{first_term_print} - {second_term_print}", end=None)
                if(self.log_trace_enabled): print("visitBinaryOperator -> SUB")
                if (first_term_symbol and QutesDataType.is_quantum_type(first_term_symbol.symbol_declaration_static_type)):
                    #TODO: handle divide operation of quantum variables
                    pass
                result = first_term / second_term
        return result

    # Utility method for logging and scaffolding operation
    def __visit(self, parent_caller_name, func, push_pop_scope:bool = False):
        if(self.log_trace_enabled): print("start " + parent_caller_name)
        if(push_pop_scope): self.scope_handler.push_scope()
        result = func()
        if(push_pop_scope): self.scope_handler.pop_scope()
        if(self.log_trace_enabled): print("end " + parent_caller_name)
        if(self.log_step_by_step_results_enabled): print(result)
        return result