# Generated from Qutes.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .QutesParser import QutesParser
else:
    from QutesParser import QutesParser

# This class defines a complete generic visitor for a parse tree produced by QutesParser.

class QutesVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by QutesParser#program.
    def visitProgram(self, ctx:QutesParser.ProgramContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QutesParser#inputDeclaration.
    def visitInputDeclaration(self, ctx:QutesParser.InputDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QutesParser#function.
    def visitFunction(self, ctx:QutesParser.FunctionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QutesParser#parameters.
    def visitParameters(self, ctx:QutesParser.ParametersContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QutesParser#parameter.
    def visitParameter(self, ctx:QutesParser.ParameterContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QutesParser#type.
    def visitType(self, ctx:QutesParser.TypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QutesParser#typeName.
    def visitTypeName(self, ctx:QutesParser.TypeNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QutesParser#block.
    def visitBlock(self, ctx:QutesParser.BlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QutesParser#statement.
    def visitStatement(self, ctx:QutesParser.StatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QutesParser#initializer.
    def visitInitializer(self, ctx:QutesParser.InitializerContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QutesParser#declaration.
    def visitDeclaration(self, ctx:QutesParser.DeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QutesParser#simple.
    def visitSimple(self, ctx:QutesParser.SimpleContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QutesParser#ifStatement.
    def visitIfStatement(self, ctx:QutesParser.IfStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QutesParser#expression.
    def visitExpression(self, ctx:QutesParser.ExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QutesParser#logicalOr.
    def visitLogicalOr(self, ctx:QutesParser.LogicalOrContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QutesParser#logicalAnd.
    def visitLogicalAnd(self, ctx:QutesParser.LogicalAndContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QutesParser#equality.
    def visitEquality(self, ctx:QutesParser.EqualityContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QutesParser#comparison.
    def visitComparison(self, ctx:QutesParser.ComparisonContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QutesParser#addition.
    def visitAddition(self, ctx:QutesParser.AdditionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QutesParser#multiplication.
    def visitMultiplication(self, ctx:QutesParser.MultiplicationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QutesParser#unary.
    def visitUnary(self, ctx:QutesParser.UnaryContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QutesParser#postfix.
    def visitPostfix(self, ctx:QutesParser.PostfixContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QutesParser#suffix.
    def visitSuffix(self, ctx:QutesParser.SuffixContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QutesParser#arguments.
    def visitArguments(self, ctx:QutesParser.ArgumentsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by QutesParser#primary.
    def visitPrimary(self, ctx:QutesParser.PrimaryContext):
        return self.visitChildren(ctx)



del QutesParser
