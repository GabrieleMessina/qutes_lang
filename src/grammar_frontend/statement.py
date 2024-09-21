from grammar_frontend.qutes_parser import QutesParser as qutes_parser
from symbols.scope_tree_node import ScopeTreeNode
from symbols.symbol import Symbol
from symbols.scope_handler import ScopeHandlerForSymbolsUpdate
from symbols.variables_handler import VariablesHandler
from symbols.types import QutesDataType, QuantumArrayType
from quantum_circuit import QuantumCircuitHandler
from grammar_frontend.qutes_base_visitor import QutesBaseVisitor

class QutesGrammarStatementVisitor(QutesBaseVisitor):
    def __init__(self, symbols_tree:ScopeTreeNode, quantum_circuit_handler : QuantumCircuitHandler, scope_handler:ScopeHandlerForSymbolsUpdate, variables_handler:VariablesHandler, verbose:bool = False):
        super().__init__(symbols_tree, quantum_circuit_handler, scope_handler, variables_handler, verbose)
    
    def visitIfStatement(self, ctx:qutes_parser.IfStatementContext):
        self.scope_handler.push_scope()
        condition = self.visit(ctx.expr())
        if(condition != None):
            if(self.variables_handler.get_value(condition) == True):
                self.visit(ctx.statement())
            elif(isinstance(ctx.statement(), qutes_parser.BlockStatementContext)):
                #remove the unused block statement scope
                self.scope_handler.push_scope()
                self.scope_handler.pop_scope()
        self.scope_handler.pop_scope()
        return None
    
    def visitIfElseStatement(self, ctx:qutes_parser.IfElseStatementContext):
        self.scope_handler.push_scope()
        condition = self.visit(ctx.expr())
        if(condition != None):
            if(self.variables_handler.get_value(condition) == True):
                self.visit(ctx.statement(0))
                if(isinstance(ctx.statement(1), qutes_parser.BlockStatementContext)):
                    #get rid of the ELSE branch scope 
                    self.scope_handler.push_scope()
                    self.scope_handler.pop_scope()
            else:
                if(isinstance(ctx.statement(0), qutes_parser.BlockStatementContext)):
                    #get rid of the IF branch scope 
                    self.scope_handler.push_scope()
                    self.scope_handler.pop_scope()
                self.visit(ctx.statement(1))
        self.scope_handler.pop_scope()
        return None   

    def visitForeachStatement(self, ctx:qutes_parser.ForeachStatementContext):
        self.scope_handler.push_scope()
        auxiliary:Symbol = self.visit(ctx.variableDeclaration(0))
        index:Symbol|None = None
        if(ctx.variableDeclaration(1)):
            index = self.visit(ctx.variableDeclaration(1))
            if(index.symbol_declaration_static_type != QutesDataType.int):
                raise TypeError(f"Index variable '{index.name}' must be of type 'int'.")
        array = self.visit(ctx.qualifiedName()).value
        if(array != None):
            self.scope_handler.start_loop() #avoid block statement to change the scope
            
            for i, next_value in enumerate(array):
                self.scope_handler.handle_loop_cycle()
                self.variables_handler.update_variable_state(auxiliary.name, next_value)
                if(index != None):
                    self.variables_handler.update_variable_state(index.name, i)
                self.visit(ctx.statement())

            self.scope_handler.end_loop() #reset scope handling

        self.scope_handler.pop_scope()
        return None

    def visitWhileStatement(self, ctx:qutes_parser.WhileStatementContext):
        return self.__visit_while_statement(ctx)
    
    def __visit_while_statement(self, ctx:qutes_parser.IfStatementContext):
        self.scope_handler.push_scope()
        condition = self.visit(ctx.expr())
        if(condition != None):
            self.scope_handler.start_loop() #avoid block statement to change the scope
            
            while(self.variables_handler.get_value(condition)):
                self.scope_handler.handle_loop_cycle()
                self.visit(ctx.statement())
                condition = self.visit(ctx.expr())

            self.scope_handler.end_loop() #reset scope handling

        self.scope_handler.pop_scope()
        return None


    def visitDoWhileStatement(self, ctx:qutes_parser.DoWhileStatementContext):
        #TODO: implement
        return self.visitChildren(ctx)

    def visitBlockStatement(self, ctx:qutes_parser.BlockStatementContext):
        self.scope_handler.push_scope()
        log_string = str()
        statement_count = 0
        for child in ctx.getChildren(lambda child : isinstance(child, qutes_parser.StatementContext)):
            statement_count += 1
            new_value = self.visit(child)
            log_string = f'{log_string}\n\tStatement[{statement_count}]: {new_value}'
            if(self.log_code_structure): print(log_string, end=None)
            if(isinstance(new_value, Symbol) and new_value.is_return_value_of_function):
                return new_value
        self.scope_handler.pop_scope()
        return None
    
    def visitFunctionStatement(self, ctx:qutes_parser.FunctionStatementContext):
        self.scope_handler.push_scope()
        function_name = self.visit(ctx.functionName())
        function_params = []
        if(ctx.functionDeclarationParams()):
            function_params = self.visit(ctx.functionDeclarationParams())
        function_params.reverse()
        #do not call a visit on the statement here, or on all the context, the statement is being saved by the discovery and should be traversed only on function execution
        self.scope_handler.pop_scope()
        return None
    
    def visitDeclarationStatement(self, ctx:qutes_parser.DeclarationStatementContext):
        return self.visit(ctx.variableDeclaration())
        
    def visitVariableDeclaration(self, ctx:qutes_parser.VariableDeclarationContext):
        var_type =  self.visit(ctx.variableType()) # we already know the variable type thanks to the discovery listener.
        var_name = self.visit(ctx.variableName())
        var_value = None
        return self.__visit_assignment_statement(var_name, var_value, ctx)

    def visitAssignmentStatement(self, ctx:qutes_parser.AssignmentStatementContext):
        var_name = self.visit(ctx.qualifiedName())
        var_value = None
        return self.__visit_assignment_statement(var_name, var_value, ctx)

    def __visit_assignment_statement(self, var_name : str | Symbol, var_value, ctx:(qutes_parser.AssignmentStatementContext | qutes_parser.VariableDeclarationContext)):
        if(ctx.expr()):
            var_value = self.visit(ctx.expr())

        if(isinstance(var_name, Symbol)):
            var_symbol = var_name
            var_name = var_symbol.name
        else: 
            var_symbol = self.variables_handler.get_variable_symbol(var_name, ctx.start.tokenIndex)

        if(isinstance(var_value, list)):
            var_value = QuantumArrayType(QutesDataType.get_unit_class_from_array_type(QutesDataType.type_of(var_value)), [symbol for symbol in var_value])

        if(var_value == None):
            var_value =  QutesDataType.get_default_value(var_symbol.symbol_declaration_static_type)
        
        if(isinstance(ctx, qutes_parser.AssignmentStatementContext)):
            if(self.log_code_structure): print(f"{str(var_name)} = {str(var_value)}", end=None)
            var_symbol = self.variables_handler.update_variable_state(var_name, var_value)
        else:
            if(var_value != None):
                var_symbol = self.variables_handler.update_variable_state(var_name, var_value)
                if(self.log_code_structure): print(f"{var_symbol.symbol_declaration_static_type.name} {str(var_name)} = {str(var_value)}", end=None)
            else:
                if(self.log_code_structure): print(f"{var_symbol.symbol_declaration_static_type.name} {str(var_name)}", end=None)        
        return var_symbol

    def visitReturnStatement(self, ctx:qutes_parser.ReturnStatementContext):
        result = self.visit(ctx.expr())
        if(isinstance(result, Symbol)):
            result.is_return_value_of_function = True
        return result    
    
    def visitExpressionStatement(self, ctx:qutes_parser.ExpressionStatementContext):
        return self.visit(ctx.expr())
    
    def visitFactStatement(self, ctx:qutes_parser.FactStatementContext):
        if(self.log_code_structure): print(f"{ctx.op.text}", end=None)
        if(ctx.MEASURE()):
            self.quantum_circuit_handler.push_measure_operation()
        if(ctx.BARRIER()):
            self.quantum_circuit_handler.push_barrier_operation()
        if(ctx.PRINT_LN()):
            print()
        return None

    def visitEmptyStatement(self, ctx:qutes_parser.EmptyStatementContext):
        return None
