"""ANTLR frontend adapter; syntax recovery never reaches semantic compilation."""
from dataclasses import fields, replace

from antlr4.error.ErrorListener import ErrorListener
from qutes import syntax as ast
from qutes.diagnostics import DiagnosticError, DiagnosticErrors
from qutes.generated.QutesParser import QutesParser
from qutes.generated.QutesVisitor import QutesVisitor
from qutes.lexer import token_stream, token_value


class SyntaxErrors(ErrorListener):
    def __init__(self, locations, tokens):
        self.locations, self.tokens = locations, tokens
        self.errors = []

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        token = offendingSymbol
        found = "end of file" if token.type == -1 else repr(token.text)
        help = "Check the statement and its surrounding delimiters."
        related = []
        expected = recognizer.getExpectedTokens().toString(recognizer.literalNames, recognizer.symbolicNames)
        expected = expected.replace("IDENT", "a name").replace("INT", "an integer").replace("STRING", "a string").replace("CHAR", "a character")
        message = f"Unexpected {found}; expected {expected}."
        if msg.startswith("missing "):
            missing = msg[8:].split(" at ")[0]
            message = f"Missing {missing} before {found}."
            help = "End the declaration or statement with ';'." if missing == "';'" else f"Insert {missing} before {found}."
        elif token.text in {";", "="}:
            message = f"Missing or invalid expression before {found}."
            help = "Provide a value or expression after '=' and before ';'."
        elif token.text == "else":
            help = "An 'else' must immediately follow an 'if' block."
        stack = []
        pairs = {")": "(", "]": "[", "}": "{"}
        for prior in self.tokens[:token.tokenIndex]:
            if prior.text in pairs.values():
                stack.append(prior)
            elif prior.text in pairs and stack and stack[-1].text == pairs[prior.text]:
                stack.pop()
        if stack and (token.type == -1 or msg.startswith("missing ")):
            opener = stack[-1]
            related.append((f"Opening {opener.text!r} is here.", self.locations.token_span(opener)))
            if token.type == -1:
                closer = {"(": ")", "[": "]", "{": "}"}[opener.text]
                message = f"Missing {closer!r} at end of file."
                help = f"Close the {opener.text!r} opened at line {self.locations.token_span(opener).start.line}."
        error = DiagnosticError("Q1002", message, self.locations.token_span(token),
                                help=help, related=related, source=self.locations.source)
        if not self.errors or self.errors[-1].span.start.offset != error.span.start.offset:
            self.errors.append(error)
        if len(self.errors) >= 10:
            raise DiagnosticErrors(self.errors)


class Builder(QutesVisitor):
    def __init__(self, locations):
        self.locations = locations

    def span(self, context):
        return self.locations.token_span(context.start).through(self.locations.token_span(context.stop or context.start))

    def visitProgram(self, ctx):
        items = [self.visit(child) for child in ctx.children[:-1]]
        return ast.Program(self.span(ctx), tuple(item for item in items if isinstance(item, ast.Function)),
                           tuple(item for item in items if not isinstance(item, ast.Function)))

    def visitInputDeclaration(self, ctx):
        return ast.Input(self.span(ctx), self.visit(ctx.type_()), ctx.IDENT().getText())

    def visitFunction(self, ctx):
        parameters = tuple(self.visit(p) for p in ctx.parameters().parameter()) if ctx.parameters() else ()
        return ast.Function(self.span(ctx), self.visit(ctx.type_()), ctx.IDENT().getText(), parameters, self.visit(ctx.block()))

    def visitParameter(self, ctx):
        return ast.Parameter(self.span(ctx), self.visit(ctx.type_()), ctx.IDENT().getText())

    def visitType(self, ctx):
        return ast.TypeRef(self.span(ctx), ctx.typeName().getText(), ctx.getChildCount() > 1)

    def visitBlock(self, ctx):
        return ast.Block(self.span(ctx), tuple(self.visit(s) for s in ctx.statement()))

    def visitDeclaration(self, ctx):
        return ast.Declaration(self.span(ctx), self.visit(ctx.type_()), ctx.IDENT().getText(), self.visit(ctx.expression()))

    def visitSimple(self, ctx):
        expressions = ctx.expression()
        first = self.visit(expressions[0])
        if len(expressions) == 2:
            return ast.Assignment(self.span(ctx), first, ctx.getChild(1).getText(), self.visit(expressions[1]))
        if ctx.getChildCount() > 1:
            return ast.Update(self.span(ctx), first, ctx.getChild(1).getText())
        return ast.ExpressionStatement(self.span(ctx), first)

    def visitStatement(self, ctx):
        start = ctx.start.text
        span = self.span(ctx)
        if start == 'return':
            return ast.Return(span, self.visit(ctx.expression()) if ctx.expression() else None)
        if start == 'while':
            return ast.While(span, self.visit(ctx.expression()), self.visit(ctx.block()))
        if start == 'for':
            return ast.For(span, self.visit(ctx.initializer()) if ctx.initializer() else None,
                           self.visit(ctx.condition) if ctx.condition else None,
                           self.visit(ctx.update) if ctx.update else None, self.visit(ctx.block()))
        if start == 'foreach':
            return ast.Foreach(span, self.visit(ctx.type_()), ctx.IDENT().getText(),
                               self.visit(ctx.expression()), self.visit(ctx.block()))
        return replace(self.visit(ctx.getChild(0)), span=span)

    def visitIfStatement(self, ctx):
        blocks = ctx.block()
        otherwise = self.visit(ctx.ifStatement()) if ctx.ifStatement() else self.visit(blocks[1]) if len(blocks) > 1 else None
        return ast.If(self.span(ctx), self.visit(ctx.expression()), self.visit(blocks[0]), otherwise)

    def visitExpression(self, ctx):
        return self.visit(ctx.getChild(0))

    visitInitializer = visitExpression

    def binary(self, ctx):
        result = self.visit(ctx.getChild(0))
        for i in range(1, ctx.getChildCount(), 2):
            right = self.visit(ctx.getChild(i + 1))
            result = ast.Binary(result.span.through(right.span), ctx.getChild(i).getText(), result, right)
        return result

    visitLogicalOr = visitLogicalAnd = visitEquality = visitComparison = visitAddition = visitMultiplication = binary

    def visitUnary(self, ctx):
        result = self.visit(ctx.postfix())
        for child in reversed(ctx.children[:-1]):
            result = ast.Unary(self.locations.token_span(child.symbol).through(result.span), child.getText(), result)
        return result

    def arguments(self, ctx):
        return tuple(self.visit(e) for e in ctx.expression()) if ctx else ()

    def visitPostfix(self, ctx):
        result = self.visit(ctx.primary())
        for suffix in ctx.suffix():
            span = result.span.through(self.span(suffix))
            if suffix.start.text == '(':
                result = ast.Call(span, result, self.arguments(suffix.arguments()))
            elif suffix.start.text == '[':
                result = ast.Index(span, result, self.visit(suffix.expression()))
            else:
                result = ast.Member(span, result, suffix.IDENT().getText())
        return result

    def visitPrimary(self, ctx):
        span = self.span(ctx)
        for name, kind in [('INT', 'int'), ('STRING', 'string'), ('CHAR', 'char')]:
            token = getattr(ctx, name)()
            if token:
                return ast.Literal(span, kind, token_value(token.symbol, self.locations))
        if ctx.IDENT():
            return ast.Name(span, ctx.IDENT().getText())
        first = ctx.start.text
        if first in {'true', 'false'}:
            return ast.Literal(span, 'bool', first == 'true')
        if first == '(':
            return ast.Group(span, self.visit(ctx.expression()))
        if first == '[':
            return ast.ArrayLiteral(span, self.arguments(ctx.arguments()))
        return ast.NewArray(span, ast.TypeRef(self.span(ctx.typeName()), ctx.typeName().getText()), self.visit(ctx.expression()))


def parse(source: str, path: str = "<source>") -> ast.Program:
    stream, locations = token_stream(source, path)
    # Guard generated recursive rules before entering Python's call stack.
    depth = unary = 0
    for token in stream.tokens:
        if token.text in {'(', '[', '{'}:
            depth += 1
        elif token.text in {')', ']', '}'}:
            depth -= 1
        unary = unary + 1 if token.text in {'!', '-', '+'} else 0
        if depth > 64 or unary > 64:
            raise DiagnosticError('Q1002', 'maximum syntax nesting exceeded', locations.token_span(token), source=source)
    parser = QutesParser(stream)
    listener = SyntaxErrors(locations, stream.tokens)
    parser.removeErrorListeners()
    parser.addErrorListener(listener)
    try:
        tree = parser.program()
        if listener.errors:
            raise DiagnosticErrors(listener.errors)
        program = Builder(locations).visit(tree)
    except RecursionError:
        raise DiagnosticError('Q1002', 'maximum syntax nesting exceeded', locations.token_span(stream.LT(1)), source=source) from None
    pending = [(program, 0)]
    while pending:
        node, depth = pending.pop()
        if depth > 128:
            raise DiagnosticError('Q1002', 'maximum syntax tree nesting exceeded', node.span, source=source)
        for field in fields(node):
            value = getattr(node, field.name)
            if isinstance(value, ast.Node):
                pending.append((value, depth + 1))
            elif isinstance(value, tuple):
                pending.extend((child, depth + 1) for child in value if isinstance(child, ast.Node))
    return program
