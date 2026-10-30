"""Recursive-descent statements and precedence-climbing expressions; no semantics."""

from contextlib import contextmanager
from dataclasses import fields, replace

from qutes import syntax as ast
from qutes.diagnostics import DiagnosticError
from qutes.lexer import Token, lex
from qutes.vocabulary import TYPES


class Parser:
    PRECEDENCE = {
        "||": 1, "&&": 2, "==": 3, "!=": 3,
        "<": 4, "<=": 4, ">": 4, ">=": 4,
        "+": 5, "-": 5, "*": 6, "/": 6, "%": 6,
    }

    def __init__(self, tokens: tuple[Token, ...], max_depth: int = 64):
        self.tokens = tokens
        self.index = 0
        self.depth = 0
        self.max_depth = max_depth

    @property
    def current(self) -> Token:
        return self.tokens[self.index]

    def error(self, message: str) -> DiagnosticError:
        return DiagnosticError("Q1002", message, self.current.span)

    def take(self) -> Token:
        token = self.current
        if token.kind != "EOF":
            self.index += 1
        return token

    def match(self, kind: str) -> Token | None:
        return self.take() if self.current.kind == kind else None

    def expect(self, kind: str) -> Token:
        if self.current.kind != kind:
            found = "end of file" if self.current.kind == "EOF" else repr(self.current.text)
            raise self.error(f"expected {kind!r}, found {found}")
        return self.take()

    @contextmanager
    def nested(self):
        if self.depth >= self.max_depth:
            raise self.error("maximum syntax nesting exceeded")
        self.depth += 1
        try:
            yield
        finally:
            self.depth -= 1

    def type_ref(self, allow_array: bool = True) -> ast.TypeRef:
        if self.current.kind not in TYPES:
            raise self.error("expected a type name")
        start = self.take()
        span = start.span
        array = False
        if allow_array and self.match("["):
            span = span.through(self.expect("]").span)
            array = True
        return ast.TypeRef(span, start.kind, array)

    def program(self) -> ast.Program:
        start = self.current.span
        functions = []
        while self.current.kind != "EOF":
            functions.append(self.function())
        return ast.Program(start.through(self.current.span), tuple(functions))

    def function(self) -> ast.Function:
        return_type = self.type_ref()
        name = self.expect("IDENT")
        self.expect("(")
        parameters = []
        if self.current.kind != ")":
            while True:
                type_ref = self.type_ref()
                parameter_name = self.expect("IDENT")
                parameters.append(ast.Parameter(type_ref.span.through(parameter_name.span), type_ref, parameter_name.text))
                if not self.match(","):
                    break
        self.expect(")")
        body = self.block()
        return ast.Function(return_type.span.through(body.span), return_type, name.text, tuple(parameters), body)

    def block(self) -> ast.Block:
        with self.nested():
            start = self.expect("{")
            statements = []
            while self.current.kind not in {"}", "EOF"}:
                statements.append(self.statement())
            end = self.expect("}")
            return ast.Block(start.span.through(end.span), tuple(statements))

    def declaration(self) -> ast.Declaration:
        type_ref = self.type_ref()
        name = self.expect("IDENT")
        self.expect("=")
        initializer = self.expression()
        return ast.Declaration(type_ref.span.through(initializer.span), type_ref, name.text, initializer)

    def simple(self) -> ast.Stmt:
        expression = self.expression()
        if self.current.kind in {"=", "+=", "-="}:
            operator = self.take()
            value = self.expression()
            return ast.Assignment(expression.span.through(value.span), expression, operator.kind, value)
        if self.current.kind in {"++", "--"}:
            operator = self.take()
            return ast.Update(expression.span.through(operator.span), expression, operator.kind)
        return ast.ExpressionStatement(expression.span, expression)

    def statement(self) -> ast.Stmt:
        kind = self.current.kind
        if kind == "{":
            return self.block()
        if kind == "if":
            return self.if_statement()
        if kind == "while":
            start = self.take()
            self.expect("(")
            condition = self.expression()
            self.expect(")")
            body = self.block()
            return ast.While(start.span.through(body.span), condition, body)
        if kind == "for":
            return self.for_statement()
        if kind == "foreach":
            start = self.take()
            self.expect("(")
            type_ref = self.type_ref()
            name = self.expect("IDENT")
            self.expect("in")
            collection = self.expression()
            self.expect(")")
            body = self.block()
            return ast.Foreach(start.span.through(body.span), type_ref, name.text, collection, body)
        if kind == "return":
            start = self.take()
            value = None if self.current.kind == ";" else self.expression()
            end = self.expect(";")
            return ast.Return(start.span.through(end.span), value)
        result = self.declaration() if kind in TYPES else self.simple()
        return replace(result, span=result.span.through(self.expect(";").span))

    def if_statement(self) -> ast.If:
        with self.nested():
            start = self.expect("if")
            self.expect("(")
            condition = self.expression()
            self.expect(")")
            then_block = self.block()
            otherwise = None
            if self.match("else"):
                otherwise = self.if_statement() if self.current.kind == "if" else self.block()
            end = otherwise.span if otherwise else then_block.span
            return ast.If(start.span.through(end), condition, then_block, otherwise)

    def for_statement(self) -> ast.For:
        start = self.expect("for")
        self.expect("(")
        initializer = None
        if self.current.kind != ";":
            initializer = self.declaration() if self.current.kind in TYPES else self.simple()
        self.expect(";")
        condition = None if self.current.kind == ";" else self.expression()
        self.expect(";")
        update = None if self.current.kind == ")" else self.simple()
        self.expect(")")
        body = self.block()
        return ast.For(start.span.through(body.span), initializer, condition, update, body)

    def expression(self, minimum: int = 1) -> ast.Expr:
        with self.nested():
            left = self.unary()
            while self.PRECEDENCE.get(self.current.kind, 0) >= minimum:
                operator = self.take()
                right = self.expression(self.PRECEDENCE[operator.kind] + 1)
                left = ast.Binary(left.span.through(right.span), operator.kind, left, right)
            return left

    def unary(self) -> ast.Expr:
        operators = []
        while self.current.kind in {"!", "-", "+"}:
            if len(operators) >= self.max_depth:
                raise self.error("maximum unary nesting exceeded")
            operators.append(self.take())
        expression = self.postfix()
        for operator in reversed(operators):
            expression = ast.Unary(operator.span.through(expression.span), operator.kind, expression)
        return expression

    def expression_list(self, end: str) -> tuple[ast.Expr, ...]:
        arguments = []
        if self.current.kind != end:
            while True:
                arguments.append(self.expression())
                if not self.match(","):
                    break
        return tuple(arguments)

    def postfix(self) -> ast.Expr:
        expression = self.primary()
        while True:
            if self.match("("):
                arguments = self.expression_list(")")
                end = self.expect(")")
                expression = ast.Call(expression.span.through(end.span), expression, arguments)
            elif self.match("["):
                index = self.expression()
                end = self.expect("]")
                expression = ast.Index(expression.span.through(end.span), expression, index)
            elif self.match("."):
                member = self.expect("IDENT")
                expression = ast.Member(expression.span.through(member.span), expression, member.text)
            else:
                return expression

    def primary(self) -> ast.Expr:
        token = self.current
        if token.kind in {"INT", "STRING", "CHAR"}:
            self.take()
            return ast.Literal(token.span, {"INT": "int", "STRING": "string", "CHAR": "char"}[token.kind], token.value)
        if token.kind in {"true", "false"}:
            self.take()
            return ast.Literal(token.span, "bool", token.kind == "true")
        if token.kind == "IDENT":
            self.take()
            return ast.Name(token.span, token.text)
        if self.match("("):
            expression = self.expression()
            end = self.expect(")")
            return ast.Group(token.span.through(end.span), expression)
        if self.match("["):
            elements = self.expression_list("]")
            end = self.expect("]")
            return ast.ArrayLiteral(token.span.through(end.span), elements)
        if self.match("new"):
            element_type = self.type_ref(allow_array=False)
            self.expect("[")
            length = self.expression()
            end = self.expect("]")
            return ast.NewArray(token.span.through(end.span), element_type, length)
        raise self.error("expected an expression")


def parse(source: str, path: str = "<source>") -> ast.Program:
    program = Parser(lex(source, path)).program()
    # Flat operator/postfix chains parse iteratively but can create deep trees.
    # Bound the result too, so subsequent serialization/visitors remain safe.
    pending = [(program, 0)]
    while pending:
        node, depth = pending.pop()
        if depth > 128:
            raise DiagnosticError("Q1002", "maximum syntax tree nesting exceeded", node.span)
        for field in fields(node):
            value = getattr(node, field.name)
            if isinstance(value, ast.Node):
                pending.append((value, depth + 1))
            elif isinstance(value, tuple):
                pending.extend((child, depth + 1) for child in value if isinstance(child, ast.Node))
    return program
