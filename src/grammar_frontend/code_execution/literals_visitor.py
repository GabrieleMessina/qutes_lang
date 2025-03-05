from grammar_frontend.shared.qutes_parser import QutesParser as qutes_parser
from symbols.scope_tree_node import ScopeTreeNode
from symbols.symbol import Symbol
from symbols.scope_handler import ScopeHandlerForSymbolsUpdate, ScopeHandlerForSymbolsDiscovery
from symbols.variables_handler import VariablesHandler
from symbols.types import Qubit, Quint, Qustring, QutesDataType, QuantumArrayType, TypeCastingHandler
from quantum_circuit.quantum_circuit_handler import QuantumCircuitHandler
from grammar_frontend.shared.qutes_base_visitor import QutesBaseVisitor

class LiteralsVisitor(QutesBaseVisitor):
    def __init__(self, symbols_tree:ScopeTreeNode, quantum_circuit_handler : QuantumCircuitHandler, scope_handler:ScopeHandlerForSymbolsUpdate|ScopeHandlerForSymbolsDiscovery, variables_handler:VariablesHandler, verbose:bool = False):
        super().__init__(symbols_tree, quantum_circuit_handler, scope_handler, variables_handler, verbose)
    
    def visitType(self, ctx:qutes_parser.TypeContext):
        return ctx.getText()
    
    def visitFunctionDeclarationParams(self, ctx:qutes_parser.FunctionDeclarationParamsContext):
        head = [self.visit(ctx.variableDeclaration())]
        tail = []
        if(ctx.functionDeclarationParams()):
            tail = self.visit(ctx.functionDeclarationParams()) #recursion
            if(not isinstance(tail, list)):
                tail = [tail]
            head.extend(tail)
        return head

    def visitTermList(self, ctx:qutes_parser.TermListContext) -> list[Symbol]:
        head = [self.visit(ctx.expr())]
        tail = []
        if(ctx.termList()):
            tail = self.visit(ctx.termList()) #recursion
            if(not isinstance(tail, list)):
                tail = [tail]
            head.extend(tail)
        return head
    
    def visitArrayLiteral(self, ctx:qutes_parser.ArrayLiteralContext) -> list[Symbol]:
        terms:list[Symbol] = self.visit(ctx.termList())
        
        unit_type = max(TypeCastingHandler.try_get_array_type(terms))
        array_type = QutesDataType.promote_unit_to_array_type(unit_type)
        unit_class_type = QutesDataType.get_unit_class_from_array_type(array_type)
        if(QutesDataType.is_quantum_type(array_type)):
            array_symbol = self.variables_handler.declare_anonymous_variable(array_type, QuantumArrayType(unit_class_type, terms), ctx.start.tokenIndex)
        else:
            array_symbol = self.variables_handler.declare_anonymous_variable(array_type, terms, ctx.start.tokenIndex)
        return array_symbol

    def visitVariableType(self, ctx:qutes_parser.VariableTypeContext):
        value = str(ctx.getText())
        if(self.log_code_structure): print(value, end=None)
        return value

    def visitQualifiedName(self, ctx:qutes_parser.QualifiedNameContext):
        var_name = str(ctx.getText())
        if(ctx.variableName()):
            var_name = self.visit(ctx.variableName())
        if(ctx.functionName()):
            var_name = self.visit(ctx.functionName())
        token_index = ctx.start.tokenIndex
        symbol_to_resolve = self.variables_handler.get_variable_symbol(var_name, token_index)
        if(self.log_code_structure): print(symbol_to_resolve, end=None)
        return self.variables_handler.get_variable_symbol(var_name, token_index)

    def visitVariableName(self, ctx:qutes_parser.VariableNameContext):
        value = str(ctx.getText())
        if(self.log_code_structure): print(value, end=None)
        return value

    def visitFunctionName(self, ctx:qutes_parser.FunctionNameContext):
        value = str(ctx.getText())
        if(self.log_code_structure): print(value, end=None)
        return value

    def visitLiteral(self, ctx:qutes_parser.LiteralContext):
        return self.visitChildren(ctx)

    def visitString(self, ctx:qutes_parser.StringContext):
        string_literal_enclosure = qutes_parser.literal_to_string(qutes_parser.STRING_ENCLOSURE)
        value = ctx.getText().removeprefix(string_literal_enclosure).removesuffix(string_literal_enclosure)
        symbol = self.variables_handler.declare_anonymous_variable(QutesDataType.string, value, ctx.start.tokenIndex)
        if(self.log_code_structure): print(value, end=None)
        return symbol

    def visitQubit(self, ctx:qutes_parser.QubitContext):
        value = Qubit.from_string(ctx.getText())
        symbol = self.variables_handler.declare_anonymous_variable(QutesDataType.qubit, value, ctx.start.tokenIndex)
        if(self.log_code_structure): print(value, end=None)
        return symbol
    
    def visitQuint(self, ctx:qutes_parser.QuintContext):
        value = Quint.init_from_string(ctx.getText())
        symbol = self.variables_handler.declare_anonymous_variable(QutesDataType.quint, value, ctx.start.tokenIndex)
        if(self.log_code_structure): print(value, end=None)
        return symbol

    def visitQustring(self, ctx:qutes_parser.QustringContext):
        value = Qustring.init_from_string(ctx.getText())
        symbol = self.variables_handler.declare_anonymous_variable(QutesDataType.qustring, value, ctx.start.tokenIndex)
        if(self.log_code_structure): print(value, end=None)
        return symbol

    def visitFloat(self, ctx:qutes_parser.FloatContext):
        value = float(ctx.getText())
        symbol = self.variables_handler.declare_anonymous_variable(QutesDataType.float, value, ctx.start.tokenIndex)
        if(self.log_code_structure): print(value, end=None)
        return symbol

    def visitInteger(self, ctx:qutes_parser.IntegerContext):
        value = int(ctx.getText())
        symbol = self.variables_handler.declare_anonymous_variable(QutesDataType.int, value, ctx.start.tokenIndex)
        if(self.log_code_structure): print(value, end=None)
        return symbol

    def visitBoolean(self, ctx:qutes_parser.BooleanContext):
        value = ctx.getText().lower() == "true" or ctx.getText() == "1"
        symbol = self.variables_handler.declare_anonymous_variable(QutesDataType.bool, value, ctx.start.tokenIndex)
        if(self.log_code_structure): print(value, end=None)
        return symbol
