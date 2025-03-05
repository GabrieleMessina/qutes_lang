"""An antlr visitor for the qutes grammar."""

from grammar_frontend.shared.qutes_parser import QutesParser as qutes_parser
from symbols.scope_tree_node import ScopeTreeNode
from symbols.scope_handler import ScopeHandlerForSymbolsUpdate
from symbols.variables_handler import VariablesHandler
from quantum_circuit.quantum_circuit_handler import QuantumCircuitHandler
from symbols.symbol import Symbol

from grammar_frontend.code_execution.expressions_visitor import ExpressionsVisitor
from grammar_frontend.code_execution.statements_visitor import StatementsVisitor
from grammar_frontend.code_execution.literals_visitor import LiteralsVisitor
from grammar_frontend.code_execution.operations_visitor import OperationsVisitor

class CodeExecutionVisitor(ExpressionsVisitor, StatementsVisitor, LiteralsVisitor, OperationsVisitor):
    """An antlr visitor for the qutes grammar."""

    def __init__(self, symbols_tree:ScopeTreeNode, quantum_circuit_handler : QuantumCircuitHandler, scope_handler:ScopeHandlerForSymbolsUpdate, variables_handler:VariablesHandler, verbose:bool = False):
        if not symbols_tree:
            raise ValueError("A symbols tree must be provided to the QutesGrammarVisitor.")
        super().__init__(symbols_tree, quantum_circuit_handler, scope_handler, variables_handler, verbose)

        # Debug flags
        self.log_code_structure = False
        self.log_trace_enabled = False
        self.log_step_by_step_results_enabled = False

        Symbol.verbose_print = verbose
        ScopeHandlerForSymbolsUpdate.print_trace = False
        self.allow_program_print = True
        self.log_grover_verbose = verbose
        self.log_grover_esm_rotation = True

        if(self.log_code_structure or self.log_trace_enabled or self.log_step_by_step_results_enabled):
            print()
            print("----Code Structure----")

    def visitProgram(self, ctx:qutes_parser.ProgramContext):
        if self.allow_program_print:
            print("\n----Program print----")
        self.scope_handler.push_scope()
        result = str()
        statement_count = 0
        for child in ctx.getChildren(lambda child : isinstance(child, qutes_parser.StatementContext)):
            statement_count += 1
            new_value = self.__visit("visitProgram", lambda i=child : self.visit(i))
            result = f'{result}\nStatement[{statement_count}]: {new_value}'
            if(self.log_code_structure): print(result, end=None)
        self.scope_handler.pop_scope()
        return None  
    
    # Utility method for logging and scaffolding operation
    def __visit(self, parent_caller_name, func, push_pop_scope:bool = False):
        if(self.log_trace_enabled): print("start " + parent_caller_name)
        if(push_pop_scope): self.scope_handler.push_scope()
        result = func()
        if(push_pop_scope): self.scope_handler.pop_scope()
        if(self.log_trace_enabled): print("end " + parent_caller_name)
        if(self.log_step_by_step_results_enabled): print(result)
        return result