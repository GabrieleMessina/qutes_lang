from grammar_frontend.qutes_parser import QutesParser as qutes_parser
from symbols.scope_tree_node import ScopeTreeNode
from symbols.symbol import Symbol
from symbols.scope_handler import ScopeHandlerForSymbolsUpdate
from symbols.variables_handler import VariablesHandler
from symbols.types import Qustring, QutesDataType
from quantum_circuit import QuantumCircuitHandler
from grammar_frontend.qutes_base_visitor import QutesBaseVisitor
from symbols.types import Qubit, Quint, QutesDataType
import math

class QutesGrammarOperationVisitor(QutesBaseVisitor):
    def __init__(self, symbols_tree:ScopeTreeNode, quantum_circuit_handler : QuantumCircuitHandler, scope_handler:ScopeHandlerForSymbolsUpdate, variables_handler:VariablesHandler, verbose:bool = False):
        super().__init__(symbols_tree, quantum_circuit_handler, scope_handler, variables_handler, verbose)
        
    def visitPostfixOperator(self, ctx:qutes_parser.PostfixOperatorContext):
        return self.__visit_unary_operator(ctx)
    
    def visitPrefixOperator(self, ctx:qutes_parser.PrefixOperatorContext):
        return self.__visit_unary_operator(ctx)
    
    def visitMultiplicativeOperator(self, ctx:qutes_parser.MultiplicativeOperatorContext):
        return self.__visit_binary_operator(ctx)

    def visitSumOperator(self, ctx:qutes_parser.SumOperatorContext):
         return self.__visit_binary_operator(ctx)
    
    def visitRelationalOperator(self, ctx:qutes_parser.RelationalOperatorContext):
        return self.__visit_boolean_operation(ctx)
    
    def visitEqualityOperator(self, ctx:qutes_parser.EqualityOperatorContext):
        return self.__visit_boolean_operation(ctx)
    
    def visitLogicAndOperator(self, ctx:qutes_parser.LogicAndOperatorContext):
        return self.__visit_boolean_operation(ctx)
    
    def visitLogicOrOperator(self, ctx:qutes_parser.LogicOrOperatorContext):
        return self.__visit_boolean_operation(ctx)

    def visitMultipleUnaryOperator(self, ctx:qutes_parser.MultipleUnaryOperatorContext):
        return self.__visitMultipleUnaryOperator(ctx)
    
    def visitUnaryOperator(self, ctx:qutes_parser.UnaryOperatorContext):
        return self.__visit_unary_operator(ctx)
    
    def visitMultipleUnaryPhaseOperator(self, ctx:qutes_parser.MultipleUnaryPhaseOperatorContext):
        return self.__visitMultipleUnaryPhaseOperator(ctx)
    
    def __visit_binary_operator(self, ctx:qutes_parser.SumOperatorContext | qutes_parser.MultiplicativeOperatorContext | qutes_parser.RelationalOperatorContext | qutes_parser.EqualityOperatorContext | qutes_parser.LogicAndOperatorContext | qutes_parser.LogicOrOperatorContext):
        result = None
        first_term_symbol = self.visit(ctx.expr(0))
        second_term_symbol = self.visit(ctx.expr(1))
        first_term = self.variables_handler.get_value(first_term_symbol)
        second_term = self.variables_handler.get_value(second_term_symbol)

        if(self.log_code_structure): print(f"{first_term_symbol} {ctx.op.text} {second_term_symbol}", end=None)
        
        if(isinstance(ctx, qutes_parser.SumOperatorContext)):
            if(ctx.ADD()):
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
            if(ctx.SUB()):
                if (first_term_symbol and QutesDataType.is_quantum_type(first_term_symbol.symbol_declaration_static_type)):
                    #TODO: handle sub operation of quantum variables
                    pass
                result = first_term - second_term
        if(isinstance(ctx, qutes_parser.MultiplicativeOperatorContext)):
            if(ctx.MULTIPLY()):
                if (first_term_symbol and QutesDataType.is_quantum_type(first_term_symbol.symbol_declaration_static_type)):
                    #TODO: handle multiply operation of quantum variables
                    pass
                result = first_term * second_term
            if(ctx.DIVIDE()):
                if (first_term_symbol and QutesDataType.is_quantum_type(first_term_symbol.symbol_declaration_static_type)):
                    #TODO: handle divide operation of quantum variables
                    pass
                result = first_term / second_term
        return result
    
    def __visit_boolean_operation(self, ctx:qutes_parser.RelationalOperatorContext | qutes_parser.EqualityOperatorContext | qutes_parser.LogicAndOperatorContext | qutes_parser.LogicOrOperatorContext):
        result = None
        first_term_symbol = self.visit(ctx.expr(0))
        second_term_symbol = self.visit(ctx.expr(1))
        first_term = self.variables_handler.get_value(first_term_symbol)
        second_term = self.variables_handler.get_value(second_term_symbol)

        if(self.log_code_structure): print(f"{first_term_symbol} {ctx.op.text} {second_term_symbol}", end=None)

        if(isinstance(ctx, qutes_parser.EqualityOperatorContext)):
            if(ctx.EQUAL()):
                if (first_term_symbol and QutesDataType.is_quantum_type(first_term_symbol.symbol_declaration_static_type)
                    and second_term_symbol and not QutesDataType.is_quantum_type(second_term_symbol.symbol_declaration_static_type)):
                    # At the moment this only works for comparing quantum variables to classical values.
                    result = self.quantum_circuit_handler.push_equals_operation(first_term_symbol.quantum_register, second_term_symbol.value)
                else:
                    result = first_term == second_term
            if(ctx.NOT_EQUAL()):
                result = first_term != second_term
        elif(isinstance(ctx, qutes_parser.RelationalOperatorContext)):
            if(ctx.GREATER()):
                result = first_term > second_term
            elif(ctx.LOWER()):
                result = first_term < second_term
            elif(ctx.GREATEREQUAL()):
                result = first_term >= second_term
            elif(ctx.LOWEREQUAL()):
                result = first_term <= second_term
        elif(isinstance(ctx, qutes_parser.LogicAndOperatorContext)):
            if(ctx.AND()):
                result = first_term and second_term
        elif(isinstance(ctx, qutes_parser.LogicOrOperatorContext)):
            if(ctx.OR()):
                result = first_term or second_term
        return result

    def __visitMultipleUnaryOperator(self, ctx:qutes_parser.MultipleUnaryOperatorContext):
        terms:list[Symbol] = self.visit(ctx.termList())
        registers = [register.quantum_register for register in terms]
        if(self.log_code_structure): print(f"{ctx.op.text} {registers}", end=None)
        if(ctx.MCZ()):
            self.quantum_circuit_handler.push_MCZ_operation(registers)
        if(ctx.MCX()):
            self.quantum_circuit_handler.push_MCX_operation(registers)
        if(ctx.MCY()):
            self.quantum_circuit_handler.push_MCY_operation(registers)
        if(ctx.SWAP()):
            self.quantum_circuit_handler.push_swap_operation(registers[0], registers[1])
        return None

    def __visitMultipleUnaryPhaseOperator(self, ctx:qutes_parser.MultipleUnaryPhaseOperatorContext):
        terms:list[Symbol] = self.visit(ctx.termList())
        registers = [register.quantum_register for register in terms]
        theta = self.visit(ctx.expr())
        if(self.log_code_structure): print(f"{ctx.op.text} {registers} by {theta}", end=None)
        if(ctx.MCP()):
            self.quantum_circuit_handler.push_MCP_operation(theta, registers)
        return None

    def __visit_unary_operator(self, ctx:qutes_parser.UnaryOperatorContext | qutes_parser.PrefixOperatorContext | qutes_parser.PostfixOperatorContext):
        result = None
        first_term_symbol = self.visit(ctx.expr())
        first_term = self.variables_handler.get_value(first_term_symbol)

        if(self.log_code_structure): print(f"{first_term_symbol} {ctx.op.text}", end=None)

        if(isinstance(ctx, qutes_parser.UnaryOperatorContext)):
            if(ctx.PRINT()):
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
            if(ctx.PAULIY()):
                if (first_term_symbol and QutesDataType.is_quantum_type(first_term_symbol.symbol_declaration_static_type)):
                    result = self.quantum_circuit_handler.push_pauliy_operation(first_term_symbol.quantum_register)
            if(ctx.PAULIZ()):
                if (first_term_symbol and QutesDataType.is_quantum_type(first_term_symbol.symbol_declaration_static_type)):
                    result = self.quantum_circuit_handler.push_pauliz_operation(first_term_symbol.quantum_register)
            if(ctx.HADAMARD()):
                if (first_term_symbol and QutesDataType.is_quantum_type(first_term_symbol.symbol_declaration_static_type)):
                    result = self.quantum_circuit_handler.push_hadamard_operation(first_term_symbol.quantum_register)
            if(ctx.MEASURE()):
                if (first_term_symbol and QutesDataType.is_quantum_type(first_term_symbol.symbol_declaration_static_type)):
                    result = self.quantum_circuit_handler.push_measure_operation([first_term_symbol.quantum_register])
        if(isinstance(ctx, qutes_parser.PrefixOperatorContext)):
            if(ctx.ADD()):
                pass
            if(ctx.SUB()):
                if (first_term_symbol and QutesDataType.is_quantum_type(first_term_symbol.symbol_declaration_static_type)):
                    result = self.quantum_circuit_handler.push_pauliz_operation(first_term_symbol.quantum_register)
                result = -first_term
            if(ctx.AUTO_INCREMENT()):
                #TODO: handle quantum
                result = first_term + 1
            if(ctx.AUTO_DECREMENT()):
                #TODO: handle quantum
                result = first_term - 1
            if(ctx.NOT()):
                if(self.log_trace_enabled): print("visitUnaryOperator -> NOT")
                if (first_term_symbol and QutesDataType.is_quantum_type(first_term_symbol.symbol_declaration_static_type)):
                    result = self.quantum_circuit_handler.push_not_operation(first_term_symbol.quantum_register)
                else:
                    result = not first_term
        if(isinstance(ctx, qutes_parser.PostfixOperatorContext)):
            #TODO: handle quantum
            #TODO: handle postfix expected behaviour
            if(ctx.AUTO_INCREMENT()):
                result = first_term + 1
            if(ctx.AUTO_DECREMENT()):
                result = first_term - 1
        return result

    grover_count = iter(range(1, 1000))
    def visitGroverOperator(self, ctx:qutes_parser.GroverOperatorContext):
        current_grover_count = next(self.grover_count)
        target_symbol:Symbol = self.visit(ctx.qualifiedName())
        if(not QutesDataType.is_quantum_type(target_symbol.casted_static_type)):
            #TODO: Handle promotion to quantum type?
            return None
        if(ctx.IN_STATEMENT()):
            array_register = target_symbol.quantum_register
            self.quantum_circuit_handler.start_quantum_function()
            termList:list[Symbol] = self.visit(ctx.termList())            
            array_size = len(target_symbol.quantum_register)

            grover_result = self.quantum_circuit_handler.declare_quantum_register("grover_phase_ancilla", Qubit())
            oracle_registers = [array_register]
            registers_to_measure = []
            if(self.log_grover_verbose):
                registers_to_measure.append(array_register)
            rotation_register = None
            phase_kickback_ancilla = None

            for term in termList:
                if(not QutesDataType.is_array_type(target_symbol.casted_static_type)):
                    self.quantum_circuit_handler.push_equals_operation(array_register, term.value)
                    if(len(array_register) == 1):
                        if(phase_kickback_ancilla == None):
                            phase_kickback_ancilla = self.quantum_circuit_handler.declare_quantum_register(f"phase_kickback_ancilla_{current_grover_count}", Qubit(0,1))
                            oracle_registers.append(phase_kickback_ancilla)
                        self.quantum_circuit_handler.push_MCZ_operation([*array_register, phase_kickback_ancilla])
                    else:
                        self.quantum_circuit_handler.push_MCZ_operation([*array_register])
                    self.quantum_circuit_handler.push_equals_operation(array_register, term.value)
                else:
                    term_to_quantum = QutesDataType.promote_classical_to_quantum_value(term.value)
                    block_size = target_symbol.value.default_block_size
                    array_size = int(len(target_symbol.quantum_register)/block_size)
                    logn = max(int(math.log2(array_size)),1)
                    if(term_to_quantum.size == 1):
                        if(phase_kickback_ancilla == None):
                            phase_kickback_ancilla = self.quantum_circuit_handler.declare_quantum_register(f"phase_kickback_ancilla_{current_grover_count}", Qubit(0,1))
                            oracle_registers.append(phase_kickback_ancilla)
                    if(rotation_register == None):
                        rotation_register = self.quantum_circuit_handler.declare_quantum_register(f"rotation(grover:{current_grover_count})", Quint.init_from_integer(0,logn,True))
                        oracle_registers.append(rotation_register)
                        if(self.log_grover_verbose):
                            registers_to_measure.append(rotation_register)
                    self.quantum_circuit_handler.push_ESM_operation(array_register, rotation_register, term_to_quantum, phase_kickback_ancilla)
                   
            oracle_registers.append(grover_result)
            quantum_function = self.quantum_circuit_handler.end_quantum_function(*oracle_registers, gate_name=f"grover_oracle_{current_grover_count}", create_gate=False)
            
            qubits_involved_in_grover = [*range(quantum_function.num_qubits)]
            if(rotation_register != None):
                qubits_involved_in_grover = [*range(quantum_function.num_qubits-len(rotation_register)-1, quantum_function.num_qubits-1), quantum_function.num_qubits-1]

            for n_results in range(1, array_size+1):
                oracle_result = self.quantum_circuit_handler.push_grover_operation(*oracle_registers, quantum_function=quantum_function, register_involved_indexes=qubits_involved_in_grover, dataset_size=array_size, n_results=n_results, verbose=self.log_grover_verbose)
                registers_to_measure.append(oracle_result)
                circuit_runs = 3
                self.quantum_circuit_handler.get_run_and_measure_results(registers_to_measure.copy(), repetition=circuit_runs)

                positive_results = [(index, result) for index, result in enumerate(oracle_result.measured_classical_register.measured_values) if "1" in result]
                any_positive_results = len(positive_results) > 0
                if (any_positive_results):
                    if(self.log_grover_verbose and rotation_register.measured_classical_register is not None):
                        print(f"Solution found with rotation {rotation_register.measured_classical_register.measured_values[positive_results[0][0]]} (for the first hit)")
                    return True
                registers_to_measure.remove(oracle_result)
            return False
