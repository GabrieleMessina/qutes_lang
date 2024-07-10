from grammar_frontend.qutes_parser import QutesParser as qutes_parser
from symbols.scope_tree_node import ScopeTreeNode
from symbols.symbol import Symbol
from symbols.scope_handler import ScopeHandlerForSymbolsUpdate
from symbols.variables_handler import VariablesHandler
from symbols.types import Qubit, Quint, Qustring, QutesDataType
from quantum_circuit import QuantumCircuitHandler
from grammar_frontend.qutes_base_visitor import QutesBaseVisitor

class QutesGrammarLiteralVisitor(QutesBaseVisitor):
    def __init__(self, symbols_tree:ScopeTreeNode, quantum_circuit_handler : QuantumCircuitHandler, scope_handler:ScopeHandlerForSymbolsUpdate, variables_handler:VariablesHandler, verbose:bool = False):
        super().__init__(symbols_tree, quantum_circuit_handler, scope_handler, variables_handler, verbose)
    
    def visitType(self, ctx:qutes_parser.TypeContext):
        return ctx.getText()
    
    def visitFunctionDeclarationParams(self, ctx:qutes_parser.FunctionDeclarationParamsContext):
        param = self.visit(ctx.variableDeclaration())
        params = []
        if(ctx.functionDeclarationParams()):
            params = self.visit(ctx.functionDeclarationParams())
            if(not isinstance(params, list)):
                params = [params]
        params.append(param)
        return params[::-1]

    def visitTermList(self, ctx:qutes_parser.TermListContext) -> list[Symbol]:
        term = self.visit(ctx.literal()) if ctx.literal() else self.visit(ctx.qualifiedName())
        terms = []
        if(ctx.termList()):
            terms = self.visit(ctx.termList())
            if(not isinstance(terms, list)):
                terms = [terms]
        terms.append(term)
        return terms[::-1]
    
    def visitArray(self, ctx:qutes_parser.ArrayContext) -> list[Symbol]:
        return self.visit(ctx.termList())    

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
        symbol = self.variables_handler.create_anonymous_symbol(QutesDataType.string, value, ctx.start.tokenIndex)
        if(self.log_code_structure): print(value, end=None)
        return symbol

    def visitQubit(self, ctx:qutes_parser.QubitContext):
        value = Qubit.from_string(ctx.getText())
        symbol = self.variables_handler.create_anonymous_symbol(QutesDataType.qubit, value, ctx.start.tokenIndex)
        if(self.log_code_structure): print(value, end=None)
        return symbol
    
    def visitQuint(self, ctx:qutes_parser.QuintContext):
        value = Quint.init_from_string(ctx.getText())
        symbol = self.variables_handler.create_anonymous_symbol(QutesDataType.quint, value, ctx.start.tokenIndex)
        if(self.log_code_structure): print(value, end=None)
        return symbol

    def visitQustring(self, ctx:qutes_parser.QustringContext):
        value = Qustring.init_from_string(ctx.getText())
        symbol = self.variables_handler.create_anonymous_symbol(QutesDataType.qustring, value, ctx.start.tokenIndex)
        if(self.log_code_structure): print(value, end=None)
        return symbol

    def visitFloat(self, ctx:qutes_parser.FloatContext):
        value = float(ctx.getText())
        symbol = self.variables_handler.create_anonymous_symbol(QutesDataType.float, value, ctx.start.tokenIndex)
        if(self.log_code_structure): print(value, end=None)
        return symbol

    def visitInteger(self, ctx:qutes_parser.IntegerContext):
        value = int(ctx.getText())
        symbol = self.variables_handler.create_anonymous_symbol(QutesDataType.int, value, ctx.start.tokenIndex)
        if(self.log_code_structure): print(value, end=None)
        return symbol

    def visitBoolean(self, ctx:qutes_parser.BooleanContext):
        value = ctx.getText().lower() == "true" or ctx.getText() == "1"
        symbol = self.variables_handler.create_anonymous_symbol(QutesDataType.bool, value, ctx.start.tokenIndex)
        if(self.log_code_structure): print(value, end=None)
        return symbol
