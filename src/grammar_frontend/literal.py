from grammar_frontend.qutes_parser import QutesParser as qutes_parser
from symbols.scope_tree_node import ScopeTreeNode
from symbols.scope_handler import ScopeHandlerForSymbolsUpdate
from symbols.variables_handler import VariablesHandler
from symbols.types import Qubit, Quint, Qustring, QutesDataType
from quantum_circuit import QuantumCircuitHandler
from grammar_frontend.qutes_base_visitor import QutesBaseVisitor

class QutesGrammarLiteralVisitor(QutesBaseVisitor):
    def __init__(self, symbols_tree:ScopeTreeNode, quantum_circuit_handler : QuantumCircuitHandler, scope_handler:ScopeHandlerForSymbolsUpdate, variables_handler:VariablesHandler, verbose:bool = False):
        super().__init__(symbols_tree, quantum_circuit_handler, scope_handler, variables_handler, verbose)
    
    # Visit a parse tree produced by qutes_parser#variableType.
    def visitVariableType(self, ctx:qutes_parser.VariableTypeContext):
        value = str(ctx.getText())
        if(self.log_code_structure): print(value, end=None)
        return self.__visit("visitVariableType", lambda : value)


    # Visit a parse tree produced by qutes_parser#qualifiedName.
    def visitQualifiedName(self, ctx:qutes_parser.QualifiedNameContext):
        var_name = str(ctx.getText())
        token_index = ctx.start.tokenIndex
        symbol_to_resolve = self.variables_handler.get_variable_symbol(var_name, token_index)
        if(self.log_code_structure): print(symbol_to_resolve, end=None)
        return self.__visit("visitQualifiedName", lambda : self.variables_handler.get_variable_symbol(var_name, token_index))


    # Visit a parse tree produced by qutes_parser#functionName.
    def visitFunctionName(self, ctx:qutes_parser.FunctionNameContext):
        #TODO: this should be aligned to visitQualifiedName which returns a symbol
        value = str(ctx.getText())
        if(self.log_code_structure): print(value, end=None)
        return self.__visit("visitFunctionName", lambda : value)


    # Visit a parse tree produced by qutes_parser#id.
    def visitString(self, ctx:qutes_parser.StringContext):
        string_literal_enclosure = qutes_parser.literal_to_string(qutes_parser.STRING_ENCLOSURE)
        value = ctx.getText().removeprefix(string_literal_enclosure).removesuffix(string_literal_enclosure)
        symbol = self.variables_handler.create_anonymous_symbol(QutesDataType.string, value, ctx.start.tokenIndex)
        if(self.log_code_structure): print(value, end=None)
        return self.__visit("visitString", lambda : symbol)

    
    # Visit a parse tree produced by qutes_parser#qubit.
    def visitQubit(self, ctx:qutes_parser.QubitContext):
        value = Qubit.from_string(ctx.getText())
        symbol = self.variables_handler.create_anonymous_symbol(QutesDataType.qubit, value, ctx.start.tokenIndex)
        if(self.log_code_structure): print(value, end=None)
        return self.__visit("visitQubit", lambda : symbol)
    
    
    # Visit a parse tree produced by qutes_parser#quint.
    def visitQuint(self, ctx:qutes_parser.QuintContext):
        value = Quint.init_from_string(ctx.getText())
        symbol = self.variables_handler.create_anonymous_symbol(QutesDataType.quint, value, ctx.start.tokenIndex)
        if(self.log_code_structure): print(value, end=None)
        return self.__visit("visitQuint", lambda : symbol)

    
    # Visit a parse tree produced by qutes_parser#qustring.
    def visitQustring(self, ctx:qutes_parser.QustringContext):
        value = Qustring.init_from_string(ctx.getText())
        symbol = self.variables_handler.create_anonymous_symbol(QutesDataType.qustring, value, ctx.start.tokenIndex)
        if(self.log_code_structure): print(value, end=None)
        return self.__visit("visitQustring", lambda : symbol)

    
    # Visit a parse tree produced by qutes_parser#float.
    def visitFloat(self, ctx:qutes_parser.FloatContext):
        value = float(ctx.getText())
        symbol = self.variables_handler.create_anonymous_symbol(QutesDataType.float, value, ctx.start.tokenIndex)
        if(self.log_code_structure): print(value, end=None)
        return self.__visit("visitFloat", lambda : symbol)


    # Visit a parse tree produced by qutes_parser#integer.
    def visitInteger(self, ctx:qutes_parser.IntegerContext):
        value = int(ctx.getText())
        symbol = self.variables_handler.create_anonymous_symbol(QutesDataType.int, value, ctx.start.tokenIndex)
        if(self.log_code_structure): print(value, end=None)
        return self.__visit("visitInteger", lambda : symbol)


    # Visit a parse tree produced by qutes_parser#boolean.
    def visitBoolean(self, ctx:qutes_parser.BooleanContext):
        value = ctx.getText().lower() == "true" or ctx.getText() == "1"
        symbol = self.variables_handler.create_anonymous_symbol(QutesDataType.bool, value, ctx.start.tokenIndex)
        if(self.log_code_structure): print(value, end=None)
        return self.__visit("visitBoolean", lambda : symbol)
    
    # Visit a parse tree produced by qutesParser#integer.
    def visitVariableName(self, ctx:qutes_parser.VariableNameContext):
        value = str(ctx.getText())
        if(self.log_code_structure): print(value, end=None)
        return self.__visit("visitVariableName", lambda : value)
    
    def visitType(self, ctx:qutes_parser.TypeContext):
        return self.visitChildren(ctx)
    
    # Utility method for logging and scaffolding operation
    def __visit(self, parent_caller_name, func, push_pop_scope:bool = False):
        if(self.log_trace_enabled): print("start " + parent_caller_name)
        if(push_pop_scope): self.scope_handler.push_scope()
        result = func()
        if(push_pop_scope): self.scope_handler.pop_scope()
        if(self.log_trace_enabled): print("end " + parent_caller_name)
        if(self.log_step_by_step_results_enabled): print(result)
        return result