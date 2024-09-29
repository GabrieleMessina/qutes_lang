import numpy as np
from grammar_frontend.qutes_parser import QutesParser as qutes_parser
from symbols.scope_tree_node import ScopeTreeNode
from symbols.symbol import Symbol, SymbolClass
from symbols.scope_handler import ScopeHandlerForSymbolsUpdate
from symbols.variables_handler import VariablesHandler
from symbols.types import Qustring, QutesDataType
from quantum_circuit import QuantumCircuitHandler
from grammar_frontend.qutes_base_visitor import QutesBaseVisitor
from symbols.types import Qubit, Quint, QutesDataType
import math
import utils

class QutesGrammarOperationVisitor(QutesBaseVisitor):
    def __init__(self, symbols_tree:ScopeTreeNode, quantum_circuit_handler : QuantumCircuitHandler, scope_handler:ScopeHandlerForSymbolsUpdate, variables_handler:VariablesHandler, verbose:bool = False):
        super().__init__(symbols_tree, quantum_circuit_handler, scope_handler, variables_handler, verbose)
        
    def visitPostfixOperator(self, ctx:qutes_parser.PostfixOperatorContext):
        return self.__visit_unary_operator(ctx)
    
    def visitPrefixOperator(self, ctx:qutes_parser.PrefixOperatorContext):
        return self.__visit_unary_operator(ctx)
    
    def visitMultiplicativeOperator(self, ctx:qutes_parser.MultiplicativeOperatorContext):
        return self.__visit_binary_operator(ctx)

    def visitExpOperator(self, ctx:qutes_parser.ExpOperatorContext):
        return self.__visit_binary_operator(ctx)

    def visitSumOperator(self, ctx:qutes_parser.SumOperatorContext):
        return self.__visit_binary_operator(ctx)

    def visitShiftOperator(self, ctx:qutes_parser.ShiftOperatorContext):
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
        first_term_symbol:Symbol = self.visit(ctx.expr(0))
        second_term_symbol:Symbol = self.visit(ctx.expr(1))
        first_term_value = self.variables_handler.get_value(first_term_symbol)
        second_term_value = self.variables_handler.get_value(second_term_symbol)

        if(self.log_code_structure): print(f"{first_term_symbol} {ctx.op.text} {second_term_symbol}", end=None)
        
        #TODO: handle binary operation of quantum variables
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
                    result = first_term_value + second_term_value
            if(ctx.SUB()):
                if (first_term_symbol and QutesDataType.is_quantum_type(first_term_symbol.symbol_declaration_static_type)):
                    pass
                result = first_term_value - second_term_value
        if(isinstance(ctx, qutes_parser.ShiftOperatorContext)):
            if(ctx.LSHIFT()):
                if (first_term_symbol and QutesDataType.is_quantum_type(first_term_symbol.symbol_declaration_static_type)):
                    if(second_term_symbol and not QutesDataType.is_quantum_type(second_term_symbol.symbol_declaration_static_type)):
                        from quantum_circuit.qutes_gates import QutesGates
                        self.quantum_circuit_handler.push_compose_circuit_operation(QutesGates.left_rot(len(first_term_symbol.quantum_register), second_term_value, first_term_symbol.casted_static_type.get_unit_size_in_qubit()), [first_term_symbol.quantum_register])
                        result = first_term_symbol
                    else:
                        raise NotImplementedError("Left shift operator doesn't support second term to be a quantum variable.")
                else:
                    result = first_term_value << second_term_value
            if(ctx.RSHIFT()):
                if (first_term_symbol and QutesDataType.is_quantum_type(first_term_symbol.symbol_declaration_static_type)):
                    if(second_term_symbol and not QutesDataType.is_quantum_type(second_term_symbol.symbol_declaration_static_type)):
                        from quantum_circuit.qutes_gates import QutesGates
                        self.quantum_circuit_handler.push_compose_circuit_operation(QutesGates.right_rot(len(first_term_symbol.quantum_register), second_term_value, first_term_symbol.casted_static_type.get_unit_size_in_qubit()), [first_term_symbol.quantum_register])
                        result = first_term_symbol
                    else:
                        raise NotImplementedError("Right shift operator doesn't support second term to be a quantum variable.")
                else:
                    result = first_term_value >> second_term_value
        if(isinstance(ctx, qutes_parser.MultiplicativeOperatorContext)):
            if(ctx.MULTIPLY()):
                if (first_term_symbol and QutesDataType.is_quantum_type(first_term_symbol.symbol_declaration_static_type)):
                    pass
                result = first_term_value * second_term_value
            if(ctx.DIVIDE()):
                if (first_term_symbol and QutesDataType.is_quantum_type(first_term_symbol.symbol_declaration_static_type)):
                    pass
                result = first_term_value / second_term_value
            if(ctx.MODULE()):
                if (first_term_symbol and QutesDataType.is_quantum_type(first_term_symbol.symbol_declaration_static_type)):
                    pass
                result = first_term_value % second_term_value
        if(isinstance(ctx, qutes_parser.ExpOperatorContext)):
            if(ctx.EXP()):
                if (first_term_symbol and QutesDataType.is_quantum_type(first_term_symbol.symbol_declaration_static_type)):
                    pass
                result = first_term_value ** second_term_value
        
        return self.variables_handler.declare_anonymous_variable(QutesDataType.type_of(result), result, ctx.start.tokenIndex)
    
    def __visit_boolean_operation(self, ctx:qutes_parser.RelationalOperatorContext | qutes_parser.EqualityOperatorContext | qutes_parser.LogicAndOperatorContext | qutes_parser.LogicOrOperatorContext):
        result = None
        first_term_symbol:Symbol = self.visit(ctx.expr(0))
        second_term_symbol:Symbol = self.visit(ctx.expr(1))
        first_term_value = self.variables_handler.get_value(first_term_symbol)
        second_term_value = self.variables_handler.get_value(second_term_symbol)

        if(self.log_code_structure): print(f"{first_term_symbol} {ctx.op.text} {second_term_symbol}", end=None)

        if(isinstance(ctx, qutes_parser.EqualityOperatorContext)):
            if(ctx.EQUAL()):
                if (first_term_symbol and QutesDataType.is_quantum_type(first_term_symbol.symbol_declaration_static_type)
                    and second_term_symbol and not QutesDataType.is_quantum_type(second_term_symbol.symbol_declaration_static_type)):
                    # At the moment this only works for comparing quantum variables to classical values.
                    result = self.quantum_circuit_handler.push_equals_operation(first_term_symbol.quantum_register, second_term_symbol.value)
                else:
                    result = first_term_value == second_term_value
            if(ctx.NOT_EQUAL()):
                result = first_term_value != second_term_value
        elif(isinstance(ctx, qutes_parser.RelationalOperatorContext)):
            if(ctx.GREATER()):
                result = first_term_value > second_term_value
            elif(ctx.LOWER()):
                result = first_term_value < second_term_value
            elif(ctx.GREATEREQUAL()):
                result = first_term_value >= second_term_value
            elif(ctx.LOWEREQUAL()):
                result = first_term_value <= second_term_value
        elif(isinstance(ctx, qutes_parser.LogicAndOperatorContext)):
            if(ctx.AND()):
                result = first_term_value and second_term_value
        elif(isinstance(ctx, qutes_parser.LogicOrOperatorContext)):
            if(ctx.OR()):
                result = first_term_value or second_term_value
        return self.variables_handler.declare_anonymous_variable(QutesDataType.bool, result, ctx.start.tokenIndex)

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
        theta:Symbol = self.visit(ctx.expr())
        if(self.log_code_structure): print(f"{ctx.op.text} {registers} by {theta}", end=None)
        if(ctx.MCP()):
            self.quantum_circuit_handler.push_MCP_operation(theta.value, registers)
        return None

    def __visit_unary_operator(self, ctx:qutes_parser.UnaryOperatorContext | qutes_parser.PrefixOperatorContext | qutes_parser.PostfixOperatorContext):
        result = None
        first_term_symbol:Symbol = self.visit(ctx.expr())
        first_term_value = self.variables_handler.get_value(first_term_symbol)

        if(self.log_code_structure): print(f"{first_term_symbol} {ctx.op.text}", end=None)

        if(isinstance(ctx, qutes_parser.UnaryOperatorContext)):
            if(ctx.PRINT() or ctx.PRINT_LN()):
                if(first_term_symbol):
                    if(QutesDataType.is_quantum_type(first_term_symbol.symbol_declaration_static_type)):
                        classical_register = self.quantum_circuit_handler.run_and_measure([first_term_symbol.quantum_register])
                        #TODO: adding the next line cause a crash in the circuit 
                        # self.variables_handler.update_variable_state(first_term_symbol.name, new_value) 
                    print(first_term_symbol, end=("" if ctx.PRINT() else "\n"))
                else:
                    print(first_term_value, end=("" if ctx.PRINT() else "\n"))
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
                    #TODO:  at the moment we return just the first measure value as result, but when array type got implemented, then we should return a list.
                    #       but also, the result will have the right value only after the circuit is run.
                    #       we should measure immediately? or avoid to return anything?
                    #       we already measure immediately on assignment.
                    result = self.quantum_circuit_handler.push_measure_operation([first_term_symbol.quantum_register])[0].measured_values
        if(isinstance(ctx, qutes_parser.PrefixOperatorContext)):
            if(ctx.ADD()):
                result = first_term_symbol
                return result
            if(ctx.SUB()):
                if (first_term_symbol and QutesDataType.is_quantum_type(first_term_symbol.symbol_declaration_static_type)):
                    result = self.quantum_circuit_handler.push_pauliz_operation(first_term_symbol.quantum_register)
                first_term_symbol.value = -first_term_symbol.value 
                result = first_term_symbol
                return result
            if(ctx.AUTO_INCREMENT()):
                #TODO: handle quantum
                first_term_symbol.value = first_term_symbol.value + 1 
                result = first_term_symbol
                return result
            if(ctx.AUTO_DECREMENT()):
                #TODO: handle quantum
                first_term_symbol.value = first_term_symbol.value - 1 
                result = first_term_symbol
                return result
            if(ctx.NOT()):
                if(self.log_trace_enabled): print("visitUnaryOperator -> NOT")
                if (first_term_symbol and QutesDataType.is_quantum_type(first_term_symbol.symbol_declaration_static_type)):
                    result = self.quantum_circuit_handler.push_not_operation(first_term_symbol.quantum_register)
                else:
                    result = not first_term_value
        if(isinstance(ctx, qutes_parser.PostfixOperatorContext)):
            #TODO: handle quantum
            if(ctx.AUTO_INCREMENT()):
                result = self.variables_handler.declare_anonymous_variable(QutesDataType.type_of(first_term_symbol), first_term_value, ctx.start.tokenIndex)
                first_term_symbol.value = first_term_symbol.value + 1 
                return result
            if(ctx.AUTO_DECREMENT()):
                result = self.variables_handler.declare_anonymous_variable(QutesDataType.type_of(first_term_symbol), first_term_value, ctx.start.tokenIndex)
                first_term_symbol.value = first_term_symbol.value - 1 
                return result

        return self.variables_handler.declare_anonymous_variable(QutesDataType.type_of(result), result, ctx.start.tokenIndex)

    def __visitFunctionCall(self, function_name, function_params:list[Symbol], tokenIndex):
        function_symbol = self.variables_handler.get_function_symbol(function_name, function_params, tokenIndex)  

        self.scope_handler.push_function_inner_scope(function_symbol.inner_scope)        
        default_params_to_restore_on_exit = function_symbol.function_input_params_definition.copy()

        symbol_params_to_push = []
        # regs = []
        for index in range(len(function_params)):
            symbol_to_push = default_params_to_restore_on_exit[index]
            symbol_to_push.value = function_params[index].value
            symbol_to_push.quantum_register = function_params[index].quantum_register
            symbol_params_to_push.append(symbol_to_push)
            # regs.append(symbol_to_push.quantum_register)
        [symbol for symbol in function_symbol.inner_scope.__hash__.symbols if symbol.symbol_class == SymbolClass.FunctionSymbol][:len(function_params)] = symbol_params_to_push

        #TODO: staff commented for make return value work for quantum variable, do some tests to assure the behaviour is correct
        # self.quantum_circuit_handler.start_quantum_function()
        function_return_result = self.visitChildren(function_symbol.value)
        # gate = self.quantum_circuit_handler.end_quantum_function(*regs, gate_name=function_symbol.name, create_gate=True)
        # function_symbol.quantum_function = gate

        self.scope_handler.pop_function_inner_scope(function_symbol.inner_scope)
        [symbol for symbol in function_symbol.inner_scope.scope_node.symbols if symbol.symbol_class == SymbolClass.FunctionSymbol][:len(function_params)] = default_params_to_restore_on_exit

        return function_symbol

    free_grover_count = iter(range(1, 1000))

    grover_count = iter(range(1, 1000))
    def visitFreeGroverOperator(self, ctx:qutes_parser.FreeGroverOperatorContext):
        current_grover_count = next(self.free_grover_count)
        function_name = self.visit(ctx.functionName())
        function_params:list[Symbol] = []
        if(ctx.termList()):
            function_params = self.visit(ctx.termList())
        if(ctx.GROVER()):
            array_register = []
            for symbol in function_params:
                    array_register.append(symbol.quantum_register)
            block_size = 1
            try:
                block_size = [symbol.quantum_register.symbol_declaration_static_type.get_unit_size_in_qubit() for symbol in function_params][0] #TODO: this is based on the function first argument type but there is no check on type coherency in following params.
            except:
                pass
            array_size = int(len(array_register)/block_size)
            n_element_to_rotate = array_size/block_size

            self.quantum_circuit_handler.start_quantum_function()
            termList:list[Symbol] = self.visit(ctx.termList())    

            grover_result = self.quantum_circuit_handler.declare_quantum_register("grover_phase_ancilla", Qubit())
            oracle_registers = array_register
            registers_to_measure = []
            if(self.log_grover_verbose):
                registers_to_measure.extend(array_register)

            oracle_function_symbol:Symbol = self.__visitFunctionCall(function_name, function_params, ctx.start.tokenIndex)
            # self.quantum_circuit_handler.push_compose_circuit_operation(oracle_function_symbol.quantum_function, array_register)
                   
            oracle_registers.append(grover_result)
            quantum_function = self.quantum_circuit_handler.end_quantum_function(*oracle_registers, gate_name=f"grover_oracle_{current_grover_count}", create_gate=False)
            
            qubits_involved_in_grover = [*range(quantum_function.num_qubits)]

            for n_results in np.arange(1.1, 1.1**math.log(n_element_to_rotate/2 + 1, 1.1)):
                oracle_result = self.quantum_circuit_handler.push_grover_operation(*oracle_registers, quantum_function=quantum_function, register_involved_indexes=qubits_involved_in_grover, dataset_size=array_size, n_results=int(n_results), verbose=self.log_grover_verbose)
                registers_to_measure.append(oracle_result)
                circuit_runs = 3
                self.quantum_circuit_handler.get_run_and_measure_results(registers_to_measure.copy(), repetition=circuit_runs)

                positive_results = [(index, result) for index, result in enumerate(oracle_result.measured_classical_register.measured_values) if "1" in result] if oracle_result.measured_classical_register != None else []
                any_positive_results = len(positive_results) > 0
                if (any_positive_results):
                    return self.variables_handler.declare_anonymous_variable(QutesDataType.bool, True, ctx.start.tokenIndex)
                registers_to_measure.remove(oracle_result)
            return self.variables_handler.declare_anonymous_variable(QutesDataType.bool, False, ctx.start.tokenIndex)

    def visitFreeGroverOperator1(self, ctx:qutes_parser.FreeGroverOperatorContext):
        current_grover_count = next(self.free_grover_count)
        function_name = self.visit(ctx.functionName())
        function_params:list[Symbol] = []
        phase_kickback_ancilla = None
        if(ctx.termList()):
            function_params = self.visit(ctx.termList())
        oracle_function_symbol:Symbol = self.__visitFunctionCall(function_name, function_params, ctx.start.tokenIndex)
        registers_to_measure = []
        oracle_registers = [oracle_function_symbol.quantum_register]
        if ctx.GROVER(): 
            array_size = oracle_function_symbol.quantum_function.num_qubits

            if(phase_kickback_ancilla == None):
                phase_kickback_ancilla = self.quantum_circuit_handler.declare_quantum_register(f"phase_kickback_ancilla_{current_grover_count}", Qubit(0,1))
                oracle_registers.append(phase_kickback_ancilla)
            self.quantum_circuit_handler.push_MCZ_operation([*oracle_registers, phase_kickback_ancilla])

            for n_results in np.arange(1.1, 1.1**math.log(array_size/2 + 1, 1.1)):
                oracle_result = self.quantum_circuit_handler.push_grover_operation(*oracle_registers, quantum_function=oracle_function_symbol.quantum_function, register_involved_indexes=[*range(array_size)], dataset_size=array_size, n_results=int(n_results), verbose=self.log_grover_verbose) 
                registers_to_measure.append(oracle_result)
                circuit_runs = 3
                self.quantum_circuit_handler.get_run_and_measure_results(registers_to_measure.copy(), repetition=circuit_runs)

                positive_results = [(index, result) for index, result in enumerate(oracle_result.measured_classical_register.measured_values) if "1" in result] if oracle_result.measured_classical_register != None else []
                any_positive_results = len(positive_results) > 0
                if (any_positive_results):
                    return self.variables_handler.declare_anonymous_variable(QutesDataType.bool, True, ctx.start.tokenIndex)
                registers_to_measure.remove(oracle_result)
        return self.variables_handler.declare_anonymous_variable(QutesDataType.bool, False, ctx.start.tokenIndex)


    grover_count = iter(range(1, 1000))
    def visitGroverOperator(self, ctx:qutes_parser.GroverOperatorContext):
        current_grover_count = next(self.grover_count)
        target_symbol:Symbol = self.visit(ctx.qualifiedName())
        if(not QutesDataType.is_quantum_type(target_symbol.casted_static_type)):
            #TODO: Handle promotion to quantum type?
            return None
        if(ctx.IN_STATEMENT()):
            array_register = target_symbol.quantum_register
            block_size = 1
            try:
                block_size = target_symbol.symbol_declaration_static_type.get_unit_size_in_qubit()
            except:
                pass
            array_size = int(len(target_symbol.quantum_register)/block_size)
            n_element_to_rotate = array_size/block_size

            self.quantum_circuit_handler.start_quantum_function()
            termList:list[Symbol] = self.visit(ctx.termList())    

            grover_result = self.quantum_circuit_handler.declare_quantum_register("grover_phase_ancilla", Qubit())
            oracle_registers = [array_register]
            registers_to_measure = []
            if(self.log_grover_verbose):
                registers_to_measure.append(array_register)
            rotation_register = None
            phase_kickback_ancilla = None

            for term in termList:
                if(not QutesDataType.is_array_type(target_symbol.casted_static_type)):
                    #TODO: Write tests for this case.
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
                    logn = max(int(math.log2(array_size)),1)

                    if(n_element_to_rotate.is_integer() and utils.is_power_of_two(int(n_element_to_rotate))):
                        logn = max(int(math.log2(n_element_to_rotate)),1)
                    else:
                        logn = max(int(math.log2(n_element_to_rotate))+1,1)

                    if(term_to_quantum.size == 1):
                        if(phase_kickback_ancilla == None):
                            phase_kickback_ancilla = self.quantum_circuit_handler.declare_quantum_register(f"phase_kickback_ancilla_{current_grover_count}", Qubit(0,1))
                            oracle_registers.append(phase_kickback_ancilla)
                    if(rotation_register == None):
                        rotation_register = self.quantum_circuit_handler.declare_quantum_register(f"rotation(grover:{current_grover_count})", Quint.init_from_size(logn,True))
                        oracle_registers.append(rotation_register)
                        if(self.log_grover_esm_rotation):
                            registers_to_measure.append(rotation_register)
                    self.quantum_circuit_handler.push_ESM_operation(array_register, rotation_register, term_to_quantum, block_size, phase_kickback_ancilla)
                   
            oracle_registers.append(grover_result)
            quantum_function = self.quantum_circuit_handler.end_quantum_function(*oracle_registers, gate_name=f"grover_oracle_{current_grover_count}", create_gate=False)
            
            qubits_involved_in_grover = [*range(quantum_function.num_qubits)]
            if(rotation_register != None):
                qubits_involved_in_grover = [*range(quantum_function.num_qubits-len(rotation_register)-1, quantum_function.num_qubits-1), quantum_function.num_qubits-1]

            for n_results in np.arange(1.1, 1.1**math.log(n_element_to_rotate/2 + 1, 1.1)):
                oracle_result = self.quantum_circuit_handler.push_grover_operation(*oracle_registers, quantum_function=quantum_function, register_involved_indexes=qubits_involved_in_grover, dataset_size=array_size, n_results=int(n_results), verbose=self.log_grover_verbose)
                registers_to_measure.append(oracle_result)
                circuit_runs = 3
                self.quantum_circuit_handler.get_run_and_measure_results(registers_to_measure.copy(), repetition=circuit_runs)

                positive_results = [(index, result) for index, result in enumerate(oracle_result.measured_classical_register.measured_values) if "1" in result] if oracle_result.measured_classical_register != None else []
                any_positive_results = len(positive_results) > 0
                if (any_positive_results):
                    if(self.log_grover_esm_rotation and rotation_register.measured_classical_register is not None):
                        for result in positive_results:
                            print(f"Solution found with {int(rotation_register.measured_classical_register.measured_values[result[0]], 2)} left rotations")
                            # print(f"Solution found with rotation {int(rotation_register.measured_classical_register.measured_values[result[0]], 2) % (n_element_to_rotate)}")
                    return self.variables_handler.declare_anonymous_variable(QutesDataType.bool, True, ctx.start.tokenIndex)
                registers_to_measure.remove(oracle_result)
            return self.variables_handler.declare_anonymous_variable(QutesDataType.bool, False, ctx.start.tokenIndex)
