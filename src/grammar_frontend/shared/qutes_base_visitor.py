
from symbols.scope_tree_node import ScopeTreeNode
from symbols.scope_handler import ScopeHandlerForSymbolsUpdate
from symbols.variables_handler import VariablesHandler
from quantum_circuit import QuantumCircuitHandler
from quantum_circuit.qutes_gates import QutesGates
from qutes_antlr.qutes_parserVisitor import qutes_parserVisitor as qutesVisitor
import inspect

class QutesBaseVisitor(qutesVisitor):
    def __init__(self, symbols_tree:ScopeTreeNode, quantum_circuit_handler : QuantumCircuitHandler, scope_handler:ScopeHandlerForSymbolsUpdate, variables_handler:VariablesHandler, verbose:bool = False):
        self.symbols_tree = symbols_tree
        self.quantum_circuit_handler = quantum_circuit_handler
        self.scope_handler = scope_handler
        self.variables_handler = variables_handler
        self.qutes_gates = QutesGates(self.quantum_circuit_handler, self.variables_handler)

    def visit(self, tree):
        """ Visit the node """
        caller_name = inspect.stack()[1].function
        if(self.log_trace_enabled): print("start " + caller_name)
        result = super(qutesVisitor, self).visit(tree)
        if(self.log_trace_enabled): print("end " + caller_name)
        if(self.log_step_by_step_results_enabled): print(result)
        return result

    def visitChildren(self, node):        
        """ Visit the node childre, but not the node itself """
        caller_name = inspect.stack()[1].function
        if(self.log_trace_enabled): print("start " + caller_name)
        result = super(qutesVisitor, self).visitChildren(node)
        if(self.log_trace_enabled): print("end " + caller_name)
        if(self.log_step_by_step_results_enabled): print(result)
        return result