"""An antlr visitor for the qutes grammar."""

from grammar_frontend.shared.qutes_parser import QutesParser as qutes_parser
from symbols.scope_tree_node import ScopeClass
from symbols.variables_handler import VariablesHandler
from quantum_circuit.quantum_circuit_handler import QuantumCircuitHandler
from symbols.scope_handler import ScopeHandlerForSymbolsDiscovery

from grammar_frontend.shared.literals_visitor import LiteralsVisitor
from grammar_frontend.symbols_discovery.statements_visitor import StatementsVisitor

class SymbolsDiscoveryVisitor(LiteralsVisitor, StatementsVisitor):
    """An antlr visitor for the qutes grammar that discovers symbols like variable, function names etc."""

    def __init__(self, quantum_circuit_handler : QuantumCircuitHandler, verbose:bool = False):
        self.quantum_circuit_handler = quantum_circuit_handler
        self.verbose = verbose
        self.scope_handler = ScopeHandlerForSymbolsDiscovery()
        self.scope_count = 0
        self.if_else_scope_count = 0
        self.loop_scope_count = 0
        self.function_scope_count = 0
        self.variables_handler = VariablesHandler(self.scope_handler, self.quantum_circuit_handler)
        super().__init__(None, quantum_circuit_handler, self.scope_handler, self.variables_handler, verbose)
        
        # Debug flags
        self.log_code_structure = False
        self.log_trace_enabled = False
        self.log_step_by_step_results_enabled = False

        ScopeHandlerForSymbolsDiscovery.print_trace = False

    def visitProgram(self, ctx:qutes_parser.ProgramContext):
        self.scope_handler.push_scope(ScopeClass.GlobalScope, "GlobalScope")
        self.visitChildren(ctx)
        self.scope_handler.pop_scope()

    # Utility method for logging and scaffolding operation
    def __visit(self, parent_caller_name, func, push_pop_scope:bool = False):
        result = func()
        return result