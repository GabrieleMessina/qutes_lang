from grammar_frontend.qutes_parser import QutesParser as qutes_parser
from symbols.scope_tree_node import ScopeTreeNode
from symbols.symbol import Symbol, SymbolClass
from symbols.scope_handler import ScopeHandlerForSymbolsUpdate
from symbols.variables_handler import VariablesHandler
from symbols.types import Qubit, Quint, QutesDataType
from quantum_circuit import QuantumCircuitHandler
from grammar_frontend.qutes_base_visitor import QutesBaseVisitor
import math

class QutesGrammarExpressionVisitor(QutesBaseVisitor):
    def __init__(self, symbols_tree:ScopeTreeNode, quantum_circuit_handler : QuantumCircuitHandler, scope_handler:ScopeHandlerForSymbolsUpdate, variables_handler:VariablesHandler, verbose:bool = False):
        super().__init__(symbols_tree, quantum_circuit_handler, scope_handler, variables_handler, verbose)

    # Visit a parse tree produced by qutesParser#expr.
    def visitExpr(self, ctx:qutes_parser.ExprContext):
        return self.__visit("visitExpr", lambda : self.visitChildren(ctx))

    # Visit a parse tree produced by qutes_parser#functionCall.
    def visitFunctionCall(self, ctx:qutes_parser.FunctionCallContext):
        function_name = self.visit(ctx.functionName())
        function_params:list[Symbol] = []
        if(ctx.functionCallParams()):
            function_params = self.visit(ctx.functionCallParams())
        result:Symbol = self.__visitFunctionCall(function_name, function_params, ctx.start.tokenIndex)
        #TODO: staff commented for make return value work for quantum variable, do some tests to assure the behaviour is correct
        # function_symbol = self.variables_handler.get_function_symbol(function_name, ctx.start.tokenIndex, function_params)
        # self.quantum_cirtcuit_handler.push_compose_circuit_operation(function_symbol.quantum_function)
        return result

    def __visitFunctionCall(self, function_name, function_params, tokenIndex):
        self.scope_handler.start_function() #To avoid block statement to push its scope

        function_symbol = self.variables_handler.get_function_symbol(function_name, tokenIndex, function_params)  

        scope_to_restore_on_exit = self.scope_handler.current_symbols_scope
        self.scope_handler.current_symbols_scope = function_symbol.inner_scope
        
        default_params_to_restore_on_exit = function_symbol.function_input_params_definition.copy()

        symbol_params_to_push = []
        for index in range(len(function_params)):
            symbol_to_push = default_params_to_restore_on_exit[index]
            symbol_to_push.value = function_params[index].value
            symbol_to_push.quantum_register = function_params[index].quantum_register
            symbol_params_to_push.append(symbol_to_push)
        [symbol for symbol in function_symbol.inner_scope.symbols if symbol.symbol_class == SymbolClass.FunctionSymbol][:len(function_params)] = symbol_params_to_push

        #TODO: staff commented for make return value work for quantum variable, do some tests to assure the behaviour is correct
        # self.quantum_cirtcuit_handler.start_quantum_function()
        result = self.visitChildren(function_symbol.value)
        # gate = self.quantum_cirtcuit_handler.end_quantum_function(function_symbol.name)
        # function_symbol.quantum_function = gate

        self.scope_handler.current_symbols_scope = scope_to_restore_on_exit
        [symbol for symbol in function_symbol.inner_scope.symbols if symbol.symbol_class == SymbolClass.FunctionSymbol][:len(function_params)] = default_params_to_restore_on_exit

        self.scope_handler.end_function()
        return result
    
    # Visit a parse tree produced by qutes_parser#functionCallParams.
    def visitFunctionCallParams(self, ctx:qutes_parser.FunctionCallParamsContext):
        param = self.visit(ctx.qualifiedName())
        params = []
        if(ctx.functionCallParams()):
            params = self.__visit("functionCallParams", lambda : self.visit(ctx.functionCallParams()))
            if(not isinstance(params, list)):
                params = [params]
        params.append(param)
        return params[::-1]

     # Visit a parse tree produced by qutesParser#parenExpr.
    def visitParenExpr(self, ctx:qutes_parser.ParenExprContext):
        return self.__visit("visitparenExpr", lambda : self.__visit_paren_expr(ctx))
    
    def __visit_paren_expr(self, ctx:qutes_parser.ParenExprContext):
        result = None
        if(ctx.expr()):
            if(self.log_trace_enabled): print("visitParenExpr -> expr")
            result = self.visitChildren(ctx.expr())
        return result
    
    # Visit a parse tree produced by qutes_parser#GroverOperator.
    def visitGroverExpr(self, ctx:qutes_parser.GroverExprContext):
        return self.__visitGroverOperator(ctx)

    grover_count = iter(range(1, 1000))
    def __visitGroverOperator(self, ctx:qutes_parser.GroverExprContext):
        current_grover_count = next(self.grover_count)
        target_symbol:Symbol = self.visit(ctx.qualifiedName())
        if(not QutesDataType.is_quantum_type(target_symbol.casted_static_type)):
            #TODO: Handle promotion to quantum type?
            return
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

    # Utility method for logging and scaffolding operation
    def __visit(self, parent_caller_name, func, push_pop_scope:bool = False):
        if(self.log_trace_enabled): print("start " + parent_caller_name)
        if(push_pop_scope): self.scope_handler.push_scope()
        result = func()
        if(push_pop_scope): self.scope_handler.pop_scope()
        if(self.log_trace_enabled): print("end " + parent_caller_name)
        if(self.log_step_by_step_results_enabled): print(result)
        return result