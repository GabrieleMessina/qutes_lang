"""An antlr visitor for the qutes grammar."""

from grammar_frontend.shared.qutes_parser import QutesParser as qutes_parser
from symbols.scope_tree_node import ScopeClass
from symbols.variables_handler import VariablesHandler
from quantum_circuit import QuantumCircuitHandler
from symbols.scope_handler import ScopeHandlerForSymbolsDiscovery

from grammar_frontend.shared.literals_visitor import LiteralVisitor
from grammar_frontend.symbols_discovery.statements_visitor import StatementVisitor

class SymbolsDiscoveryVisitor(LiteralVisitor, StatementVisitor):
    """An antlr visitor for the qutes grammar that discovers symbols like variable, function names etc."""

    def __init__(self, quantum_circuit_handler : QuantumCircuitHandler, verbose:bool = False):
        super().__init__(None, quantum_circuit_handler, None, None, verbose)
        self.quantum_circuit_handler = quantum_circuit_handler
        self.verbose = verbose
        self.scope_handler = ScopeHandlerForSymbolsDiscovery()
        self.scope_count = 0
        self.if_else_scope_count = 0
        self.loop_scope_count = 0
        self.function_scope_count = 0
        self.variables_handler = VariablesHandler(self.scope_handler, self.quantum_circuit_handler)
        
        ScopeHandlerForSymbolsDiscovery.print_trace = False

    def visitProgram(self, ctx:qutes_parser.ProgramContext):
        self.scope_handler.push_scope(ScopeClass.GlobalScope, "GlobalScope")
        self.visitChildren(ctx)
        self.scope_handler.pop_scope()

    # Utility method for logging and scaffolding operation
    def __visit(self, parent_caller_name, func, push_pop_scope:bool = False):
        result = func()
        return result