"""An antlr visitor for the qutes grammar."""

from grammar_frontend.shared.qutes_parser import QutesParser as qutes_parser
from symbols.scope_tree_node import ScopeTreeNode
from symbols.scope_handler import ScopeHandlerForSymbolsUpdate
from symbols.variables_handler import VariablesHandler
from quantum_circuit import QuantumCircuitHandler

from grammar_frontend.code_execution.expressions_visitor import QutesGrammarExpressionVisitor
from grammar_frontend.code_execution.statements_visitor import QutesGrammarStatementVisitor
from grammar_frontend.shared.literals_visitor import LiteralVisitor
from grammar_frontend.code_execution.operations_visitor import QutesGrammarOperationVisitor

class QutesGrammarVisitor(QutesGrammarExpressionVisitor, QutesGrammarStatementVisitor, LiteralVisitor, QutesGrammarOperationVisitor):
    """An antlr visitor for the qutes grammar."""

    def __init__(self, symbols_tree:ScopeTreeNode, quantum_circuit_handler : QuantumCircuitHandler, scope_handler:ScopeHandlerForSymbolsUpdate, variables_handler:VariablesHandler, verbose:bool = False):
        if not symbols_tree:
            raise ValueError("A symbols tree must be provided to the QutesGrammarVisitor.")
        super().__init__(symbols_tree, quantum_circuit_handler, scope_handler, variables_handler, verbose)

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