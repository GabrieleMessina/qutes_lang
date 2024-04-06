"""An antlr visitor for the qutes grammar."""

from grammar_frontend.qutes_parser import QutesParser as qutesParser
from qutes_antlr.qutes_parserVisitor import qutes_parserVisitor as qutesVisitor
from symbols.scope_tree_node import ScopeTreeNode
from symbols.symbol import Symbol, SymbolClass
from symbols.scope_handler import ScopeHandlerForSymbolsUpdate
from symbols.variables_handler import VariablesHandler
from symbols.types import Qubit, Quint, Qustring, QutesDataType
from quantum_circuit import QuantumCircuitHandler
from quantum_circuit.quantum_register import QuantumRegister
from quantum_circuit.qutes_gates import QutesGates
import math

class QutesGrammarVisitor(qutesVisitor):
    """An antlr visitor for the qutes grammar."""

    def __init__(self, symbols_tree:ScopeTreeNode, quantum_circuit_handler : QuantumCircuitHandler, scope_handler:ScopeHandlerForSymbolsUpdate, variables_handler:VariablesHandler, verbose:bool = False):
        if not symbols_tree:
            raise ValueError("A symbols tree must be provided to the QutesGrammarVisitor.")
        self.symbols_tree = symbols_tree
        self.quantum_circuit_handler = quantum_circuit_handler
        #We need to travers the symbols_tree going orderly like in a breadth first search
        #Every time we need to create a new scope, we visit instead the next node in the tree
        #And every time we need to close a scope, we return to the parent of the current node
        #This way we know, at each moment, what symbols are defined.
        self.scope_handler = scope_handler
        self.variables_handler = variables_handler

        self.qutes_gates = QutesGates(self.quantum_circuit_handler, self.variables_handler)

        # Debug flags
        self.allow_program_print = True
        self.log_code_structure = verbose
        self.log_trace_enabled = verbose
        self.log_step_by_step_results_enabled = verbose
        self.log_grover_verbose = verbose

        if(self.log_code_structure or self.log_trace_enabled or self.log_step_by_step_results_enabled):
            print()
            print("----Code Structure----")

    # Visit a parse tree produced by qutesParser#program.
    def visitProgram(self, ctx:qutesParser.ProgramContext):
        if self.allow_program_print:
            print("\n----Program print----")
        self.scope_handler.push_scope()
        result = str()
        statement_count = 0
        for child in ctx.getChildren(lambda child : isinstance(child, qutesParser.StatementContext)):
            statement_count += 1
            new_value = self.__visit("visitProgram", lambda i=child : self.visit(i))
            result = f'{result}\nStatement[{statement_count}]: {new_value}'
            if(self.log_code_structure): print(result, end=None)
        self.scope_handler.pop_scope()
        return None

    # Visit a parse tree produced by qutesParser#IfStatement.
    def visitIfStatement(self, ctx:qutesParser.IfStatementContext):
        return self.__visit("visitIfStatement", lambda : self.__visit_if_statement(ctx))
    
    def __visit_if_statement(self, ctx:qutesParser.IfStatementContext):
        self.scope_handler.push_scope()
        condition = self.visitChildren(ctx.expr())
        if(condition != None):
            if(self.variables_handler.get_value(condition) == True):
                self.visit(ctx.statement())
            elif(isinstance(ctx.statement(), qutesParser.BlockStatementContext)):
                #remove the unused block statement scope
                self.scope_handler.push_scope()
                self.scope_handler.pop_scope()
        self.scope_handler.pop_scope()
        return None


    # Visit a parse tree produced by qutesParser#IfElseStatement.
    def visitIfElseStatement(self, ctx:qutesParser.IfElseStatementContext):
        return self.__visit("visitIfElseStatement", lambda : self.__visit_if_else_statement(ctx))
    
    def __visit_if_else_statement(self, ctx:qutesParser.IfStatementContext):
        self.scope_handler.push_scope()
        condition = self.visitChildren(ctx.expr())
        if(condition != None):
            if(self.variables_handler.get_value(condition) == True):
                self.visit(ctx.statement(0))
                if(isinstance(ctx.statement(1), qutesParser.BlockStatementContext)):
                    #get rid of the ELSE branch scope 
                    self.scope_handler.push_scope()
                    self.scope_handler.pop_scope()
            else:
                if(isinstance(ctx.statement(0), qutesParser.BlockStatementContext)):
                    #get rid of the IF branch scope 
                    self.scope_handler.push_scope()
                    self.scope_handler.pop_scope()
                self.visit(ctx.statement(1))
        self.scope_handler.pop_scope()
        return None


    # Visit a parse tree produced by qutesParser#WhileStatement.
    def visitWhileStatement(self, ctx:qutesParser.WhileStatementContext):
        return self.__visit("visitWhileStatement", lambda : self.__visit_while_statement(ctx))
    
    def __visit_while_statement(self, ctx:qutesParser.IfStatementContext):
        self.scope_handler.push_scope()
        condition = self.visitChildren(ctx.expr())
        if(condition != None):
            if(isinstance(ctx.statement(), qutesParser.BlockStatementContext)):
                #the while statement needs to handle the scope so that the the block statement can work always on the same scope(its own scope)
                self.scope_handler.push_scope()

            self.scope_handler.start_loop() #avoid block statement to change the scope
            
            while(condition):
                self.visit(ctx.statement())
                condition = self.visitChildren(ctx.expr())

            self.scope_handler.end_loop() #reset scope handling

            if(isinstance(ctx.statement(), qutesParser.BlockStatementContext)):
                #the while statement needs to handle the scope so that the the block statement can work always on the same scope(its own scope)
                self.scope_handler.pop_scope()
        self.scope_handler.pop_scope()
        return None


    # Visit a parse tree produced by qutesParser#DoWhileStatement.
    def visitDoWhileStatement(self, ctx:qutesParser.DoWhileStatementContext):
        return self.__visit("visitDoWhileStatement", lambda : self.visitChildren(ctx))


    # Visit a parse tree produced by qutesParser#ExpressionStatement.
    def visitExpressionStatement(self, ctx:qutesParser.ExpressionStatementContext):
        return self.__visit("visitExpressionStatement", lambda : self.visitChildren(ctx.expr()))


    # Visit a parse tree produced by qutesParser#EmptyStatement.
    def visitEmptyStatement(self, ctx:qutesParser.EmptyStatementContext):
        return self.__visit("visitEmptyStatement", lambda : self.visitChildren(ctx))


    # Visit a parse tree produced by qutesParser#BlockStatement.
    def visitBlockStatement(self, ctx:qutesParser.BlockStatementContext):
        self.scope_handler.push_scope()
        result = self.__visit("visitBlockStatement", lambda : self.visitChildren(ctx))
        self.scope_handler.pop_scope()
        return result
    
    
    # Visit a parse tree produced by qutes_parser#FunctionStatement.
    def visitFunctionStatement(self, ctx:qutesParser.FunctionStatementContext):
        self.scope_handler.push_scope()
        function_name = self.visit(ctx.functionName())
        if(ctx.functionDeclarationParams()):
            function_params = self.visit(ctx.functionDeclarationParams())
        #do not call a visit on the statement here, or on all the context, the statement is being saved by the discovery and should be traversed only on function execution
        self.scope_handler.pop_scope()
        return None


    # Visit a parse tree produced by qutesParser#DeclarationStatement.
    def visitDeclarationStatement(self, ctx:qutesParser.DeclarationStatementContext):
        return self.__visit("visitDeclarationStatement", lambda :  self.visitChildren(ctx))
        
    # Visit a parse tree produced by qutes_parser#variableDeclaration.
    def visitVariableDeclaration(self, ctx:qutesParser.VariableDeclarationContext):
        var_type =  self.visit(ctx.variableType()) # we already know the variable type thanks to the discovery listener.
        var_name = self.visit(ctx.variableName())
        var_value = None

        return self.__visit("visitVariableDeclaration", lambda : self.__visit_assignment_statement(var_name, var_value, ctx))


    # Visit a parse tree produced by qutesParser#AssignmentStatement.
    def visitAssignmentStatement(self, ctx:qutesParser.AssignmentStatementContext):
        var_name = self.visit(ctx.qualifiedName())
        var_value = None
        return self.__visit("visitAssignmentStatement", lambda : self.__visit_assignment_statement(var_name, var_value, ctx))


    def __visit_assignment_statement(self, var_name : str | Symbol, var_value, ctx:(qutesParser.AssignmentStatementContext | qutesParser.VariableDeclarationContext)):
        if(ctx.expr()):
            var_value = self.visit(ctx.expr())

        if(isinstance(var_name, Symbol)):
            var_symbol = var_name
            var_name = var_symbol.name
        else: 
            var_symbol = self.variables_handler.get_variable_symbol(var_name, ctx.start.tokenIndex)

        if(var_value == None):
            var_value =  QutesDataType.get_default_value(var_symbol.symbol_declaration_static_type)
        
        if(isinstance(ctx, qutesParser.AssignmentStatementContext)):
            if(self.log_code_structure): print(f"{str(var_name)} = {str(var_value)}", end=None)
            var_symbol = self.variables_handler.update_variable_state(var_name, var_value)
        else:
            if(var_value != None):
                var_symbol = self.variables_handler.update_variable_state(var_name, var_value)
                if(self.log_code_structure): print(f"{var_symbol.symbol_declaration_static_type.name} {str(var_name)} = {str(var_value)}", end=None)
            else:
                if(self.log_code_structure): print(f"{var_symbol.symbol_declaration_static_type.name} {str(var_name)}", end=None)        
        return var_symbol


    # Visit a parse tree produced by qutes_parser#ReturnStatement.
    def visitReturnStatement(self, ctx:qutesParser.ReturnStatementContext):
        result = self.__visit("visitReturnStatement", lambda : self.visitChildren(ctx.expr()))
        if(isinstance(result, Symbol)):
            result.is_return_value_of_function = True
        return result
    
    
    # Visit a parse tree produced by qutes_parser#block.
    def visitBlock(self, ctx:qutesParser.BlockContext):
        log_string = str()
        statement_count = 0
        for child in ctx.getChildren(lambda child : isinstance(child, qutesParser.StatementContext)):
            statement_count += 1
            new_value = self.__visit("visitBlockStatement", lambda i=child : self.visit(i))
            log_string = f'{log_string}\n\tStatement[{statement_count}]: {new_value}'
            if(self.log_code_structure): print(log_string, end=None)
            if(isinstance(new_value, Symbol) and new_value.is_return_value_of_function):
                return new_value
        return None


    # Visit a parse tree produced by qutes_parser#functionParams.
    def visitFunctionDeclarationParams(self, ctx:qutesParser.FunctionDeclarationParamsContext):
        param = self.visit(ctx.variableDeclaration())
        params = []
        if(ctx.functionDeclarationParams()):
            params = self.__visit("functionDeclarationParams", lambda : self.visit(ctx.functionDeclarationParams()))
            if(not isinstance(params, list)):
                params = [params]
        params.append(param)
        return params[::-1]
    
    
     # Visit a parse tree produced by qutes_parser#functionCallParams.
    def visitFunctionCallParams(self, ctx:qutesParser.FunctionCallParamsContext):
        param = self.visit(ctx.qualifiedName())
        params = []
        if(ctx.functionCallParams()):
            params = self.__visit("functionCallParams", lambda : self.visit(ctx.functionCallParams()))
            if(not isinstance(params, list)):
                params = [params]
        params.append(param)
        return params[::-1]


    # Visit a parse tree produced by qutesParser#expr.
    def visitExpr(self, ctx:qutesParser.ExprContext):
        return self.__visit("visitExpr", lambda : self.__visit_expr(ctx))
    def __visit_expr(self, ctx:qutesParser.ExprContext):
        result = self.visitChildren(ctx)
        if(ctx.term()):
            if(self.log_trace_enabled): print("visitExpr -> term")
        if(ctx.functionCall()):
            if(self.log_trace_enabled): print("functionCall -> term")
        if(ctx.test()):
            if(self.log_trace_enabled): print("visitExpr -> test")
        if(ctx.parenExpr()):
            if(self.log_trace_enabled): print("visitExpr -> parenExpr")
        return result

    # Visit a parse tree produced by qutes_parser#functionCall.
    def visitFunctionCall(self, ctx:qutesParser.FunctionCallContext):
        function_name = self.visit(ctx.functionName())
        function_params:list[Symbol] = []
        if(ctx.functionCallParams()):
            function_params = self.visit(ctx.functionCallParams())
        result:Symbol = self.__visit("visitFunctionCall", lambda : self.__visitFunctionCall(function_name, function_params, ctx.start.tokenIndex))
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
        result = self.__visit("visitFunctionCall", lambda : self.visitChildren(function_symbol.value))
        # gate = self.quantum_cirtcuit_handler.end_quantum_function(function_symbol.name)
        # function_symbol.quantum_function = gate

        self.scope_handler.current_symbols_scope = scope_to_restore_on_exit
        [symbol for symbol in function_symbol.inner_scope.symbols if symbol.symbol_class == SymbolClass.FunctionSymbol][:len(function_params)] = default_params_to_restore_on_exit

        self.scope_handler.end_function()
        return result
    
    
    # Visit a parse tree produced by qutesParser#parenExpr.
    def visitParenExpr(self, ctx:qutesParser.ParenExprContext):
        return self.__visit("visitparenExpr", lambda : self.__visit_paren_expr(ctx))
    
    def __visit_paren_expr(self, ctx:qutesParser.ParenExprContext):
        result = None
        if(ctx.expr()):
            if(self.log_trace_enabled): print("visitParenExpr -> expr")
            result = self.visitChildren(ctx.expr())
        return result


    # Visit a parse tree produced by qutesParser#test.
    def visitTest(self, ctx:qutesParser.TestContext):
        return self.__visit("visitTest", lambda : self.__visit_test(ctx))

    def __visit_test(self, ctx:qutesParser.TestContext):
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


    # Visit a parse tree produced by qutes_parser#MultipleUnaryOperator.
    def visitMultipleUnaryOperator(self, ctx:qutesParser.MultipleUnaryOperatorContext):
        return self.__visit("visitMultipleUnaryOperator", lambda : self.__visitMultipleUnaryOperator(ctx))

    def __visitMultipleUnaryOperator(self, ctx:qutesParser.MultipleUnaryOperatorContext):
        terms:list[Symbol] = self.visit(ctx.termList())
        registers = [register.quantum_register for register in terms]
        if(ctx.MCZ()):
            self.quantum_circuit_handler.push_MCZ_operation(registers)
        if(ctx.MCX()):
            self.quantum_circuit_handler.push_MCX_operation(registers)

    # Visit a parse tree produced by qutes_parser#termList.
    def visitTermList(self, ctx:qutesParser.TermListContext):
        term = self.visit(ctx.term())
        terms = []
        if(ctx.termList()):
            terms = self.__visit("visitTermList", lambda : self.visit(ctx.termList()))
            if(not isinstance(terms, list)):
                terms = [terms]
        terms.append(term)
        return terms[::-1]


    # Visit a parse tree produced by qutes_parser#GroverOperator.
    def visitGroverExpr(self, ctx:qutesParser.GroverExprContext):
        return self.__visit("visitGroverOperator", lambda : self.__visitGroverOperator(ctx))

    grover_count = iter(range(1, 1000))
    def __visitGroverOperator(self, ctx:qutesParser.GroverExprContext):
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
                results, _ = self.quantum_circuit_handler.get_run_and_measure_results(registers_to_measure, repetition=circuit_runs)

                positive_results = [result for result in results if result[0].split(" ")[0] == "1"]
                if (len(positive_results) > 0):
                    results_counts = sum([result[1] for result in positive_results])
                    if(self.log_grover_verbose):
                        print(f"Solution found with probability {results_counts}/{circuit_runs}")
                        if(len(positive_results[0][0].split(" ")) > 1):
                            print(f"and rotation: {positive_results[0][0].split(' ')[1]} (for the first hit)")
                    return True
                registers_to_measure.remove(oracle_result)
            return False
                
                
    # Visit a parse tree produced by qutes_parser#IdentityOperator.
    def visitIdentityOperator(self, ctx:qutesParser.IdentityOperatorContext):
        result = self.__visit_identity_operator(ctx)
        if(self.log_code_structure): print(result, end=None) 
        return self.__visit("visitIdentityOperator", lambda : result)
    
    def __visit_identity_operator(self, ctx:qutesParser.IdentityOperatorContext):
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
    def visitUnaryOperator(self, ctx:qutesParser.UnaryOperatorContext):
         return self.__visit("visitUnaryOperator", lambda : self.__visit_unary_operator(ctx))
    
    def __visit_unary_operator(self, ctx:qutesParser.UnaryOperatorContext):
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


    # Visit a parse tree produced by qutes_parser#BinaryOperator.
    def visitBinaryOperator(self, ctx:qutesParser.BinaryOperatorContext):
         return self.__visit("visitBinaryOperator", lambda : self.__visit_binary_operator(ctx))

    def __visit_binary_operator(self, ctx:qutesParser.BinaryOperatorContext):
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

            if(ctx.ADD()):
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
            if(ctx.SUB()):
                if(self.log_code_structure): print(f"{first_term_print} - {second_term_print}", end=None)
                if(self.log_trace_enabled): print("visitBinaryOperator -> SUB")
                if (first_term_symbol and QutesDataType.is_quantum_type(first_term_symbol.symbol_declaration_static_type)):
                    #TODO: handle sub operation of quantum variables
                    pass
                result = first_term - second_term
        return result
    

    # Visit a parse tree produced by qutesParser#variableType.
    def visitVariableType(self, ctx:qutesParser.VariableTypeContext):
        value = str(ctx.getText())
        if(self.log_code_structure): print(value, end=None)
        return self.__visit("visitVariableType", lambda : value)


    # Visit a parse tree produced by qutesParser#qualifiedName.
    def visitQualifiedName(self, ctx:qutesParser.QualifiedNameContext):
        var_name = str(ctx.getText())
        token_index = ctx.start.tokenIndex
        symbol_to_resolve = self.variables_handler.get_variable_symbol(var_name, token_index)
        if(self.log_code_structure): print(symbol_to_resolve, end=None)
        return self.__visit("visitQualifiedName", lambda : self.variables_handler.get_variable_symbol(var_name, token_index))


    # Visit a parse tree produced by qutes_parser#functionName.
    def visitFunctionName(self, ctx:qutesParser.FunctionNameContext):
        #TODO: this should be aligned to visitQualifiedName which returns a symbol
        value = str(ctx.getText())
        if(self.log_code_structure): print(value, end=None)
        return self.__visit("visitFunctionName", lambda : value)


    # Visit a parse tree produced by qutesParser#id.
    def visitString(self, ctx:qutesParser.StringContext):
        string_literal_enclosure = qutesParser.literal_to_string(qutesParser.STRING_ENCLOSURE)
        value = ctx.getText().removeprefix(string_literal_enclosure).removesuffix(string_literal_enclosure)
        symbol = self.variables_handler.create_anonymous_symbol(QutesDataType.string, value, ctx.start.tokenIndex)
        if(self.log_code_structure): print(value, end=None)
        return self.__visit("visitString", lambda : symbol)

    
    # Visit a parse tree produced by qutesParser#qubit.
    def visitQubit(self, ctx:qutesParser.QubitContext):
        value = Qubit.from_string(ctx.getText())
        symbol = self.variables_handler.create_anonymous_symbol(QutesDataType.qubit, value, ctx.start.tokenIndex)
        if(self.log_code_structure): print(value, end=None)
        return self.__visit("visitQubit", lambda : symbol)
    
    
    # Visit a parse tree produced by qutesParser#quint.
    def visitQuint(self, ctx:qutesParser.QuintContext):
        value = Quint.init_from_string(ctx.getText())
        symbol = self.variables_handler.create_anonymous_symbol(QutesDataType.quint, value, ctx.start.tokenIndex)
        if(self.log_code_structure): print(value, end=None)
        return self.__visit("visitQuint", lambda : symbol)

    
    # Visit a parse tree produced by qutes_parser#qustring.
    def visitQustring(self, ctx:qutesParser.QustringContext):
        value = Qustring.init_from_string(ctx.getText())
        symbol = self.variables_handler.create_anonymous_symbol(QutesDataType.qustring, value, ctx.start.tokenIndex)
        if(self.log_code_structure): print(value, end=None)
        return self.__visit("visitQustring", lambda : symbol)

    
    # Visit a parse tree produced by qutesParser#float.
    def visitFloat(self, ctx:qutesParser.FloatContext):
        value = float(ctx.getText())
        symbol = self.variables_handler.create_anonymous_symbol(QutesDataType.float, value, ctx.start.tokenIndex)
        if(self.log_code_structure): print(value, end=None)
        return self.__visit("visitFloat", lambda : symbol)


    # Visit a parse tree produced by qutesParser#integer.
    def visitInteger(self, ctx:qutesParser.IntegerContext):
        value = int(ctx.getText())
        symbol = self.variables_handler.create_anonymous_symbol(QutesDataType.int, value, ctx.start.tokenIndex)
        if(self.log_code_structure): print(value, end=None)
        return self.__visit("visitInteger", lambda : symbol)


    # Visit a parse tree produced by qutes_parser#boolean.
    def visitBoolean(self, ctx:qutesParser.BooleanContext):
        value = ctx.getText().lower() == "true" or ctx.getText() == "1"
        symbol = self.variables_handler.create_anonymous_symbol(QutesDataType.bool, value, ctx.start.tokenIndex)
        if(self.log_code_structure): print(value, end=None)
        return self.__visit("visitBoolean", lambda : symbol)

    
    # Visit a parse tree produced by qutesParser#integer.
    def visitVariableName(self, ctx:qutesParser.VariableNameContext):
        value = str(ctx.getText())
        if(self.log_code_structure): print(value, end=None)
        return self.__visit("visitVariableName", lambda : value)

    # Utility method for logging and scaffolding operation
    def __visit(self, parent_caller_name, func, push_pop_scope:bool = False):
        if(self.log_trace_enabled): print("start " + parent_caller_name)
        if(push_pop_scope): self.scope_handler.push_scope()
        result = func()
        if(push_pop_scope): self.scope_handler.pop_scope()
        if(self.log_trace_enabled): print("end " + parent_caller_name)
        if(self.log_step_by_step_results_enabled): print(result)
        return result
