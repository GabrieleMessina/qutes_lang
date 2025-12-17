using CommunityToolkit.Diagnostics;

using Qutes.Grammar;

using QutesLang.Exceptions;
using QutesLang.Symbols;
using QutesLang.Symbols.Types;
using QutesLang.Utils;

namespace QutesLang.GrammarFrontend;

public class QutesVisitor(IScopeHandler scopeHandler, IQuantumCircuitHandler circuitHandler) : qutes_parserBaseVisitor<Symbol>
{
    private Symbol FindSymbolByQualifiedName(Symbol qualifiedName)
    {
        throw new NotImplementedException();
    }

    private AnonymousValueSymbol GetDefaultValueSymbolForType(Symbol varTypeSymbol)
    {
        //todo: get default value, even if we decide null is ok for uninitialized variables, it's better to have a function retrieving that.
        throw new NotImplementedException();
    }

    public override Symbol VisitProgram(qutes_parser.ProgramContext context)
    {
        scopeHandler.PushScope(scopeHandler.CreateScope());
        return base.VisitProgram(context);
    }

    public override Symbol VisitIfStatement(qutes_parser.IfStatementContext context)
    {
        return base.VisitIfStatement(context);
    }

    public override Symbol VisitIfElseStatement(qutes_parser.IfElseStatementContext context)
    {
        return base.VisitIfElseStatement(context);
    }

    public override Symbol VisitWhileStatement(qutes_parser.WhileStatementContext context)
    {
        return base.VisitWhileStatement(context);
    }

    public override Symbol VisitForeachStatement(qutes_parser.ForeachStatementContext context)
    {
        return base.VisitForeachStatement(context);
    }

    public override Symbol VisitDoWhileStatement(qutes_parser.DoWhileStatementContext context)
    {
        return base.VisitDoWhileStatement(context);
    }

    public override Symbol VisitBlockStatement(qutes_parser.BlockStatementContext context)
    {
        return base.VisitBlockStatement(context);
    }

    public override Symbol VisitFunctionStatement(qutes_parser.FunctionStatementContext context)
    {
        return base.VisitFunctionStatement(context);
    }

    public override Symbol VisitDeclarationStatement(qutes_parser.DeclarationStatementContext context)
    {
        return base.VisitDeclarationStatement(context);
    }

    public override Symbol VisitAssignmentStatement(qutes_parser.AssignmentStatementContext context)
    {
        return base.VisitAssignmentStatement(context);
    }

    public override Symbol VisitReturnStatement(qutes_parser.ReturnStatementContext context)
    {
        return base.VisitReturnStatement(context);
    }

    public override Symbol VisitExpressionStatement(qutes_parser.ExpressionStatementContext context)
    {
        return base.VisitExpressionStatement(context);
    }

    public override Symbol VisitFactStatement(qutes_parser.FactStatementContext context)
    {
        return base.VisitFactStatement(context);
    }

    public override Symbol VisitEmptyStatement(qutes_parser.EmptyStatementContext context)
    {
        return base.VisitEmptyStatement(context);
    }

    public override Symbol VisitParentesizeExpression(qutes_parser.ParentesizeExpressionContext context)
    {
        return base.VisitParentesizeExpression(context);
    }

    public override Symbol VisitLiteralExpression(qutes_parser.LiteralExpressionContext context)
    {
        return base.VisitLiteralExpression(context);
    }

    public override Symbol VisitQualifiedNameExpression(qutes_parser.QualifiedNameExpressionContext context)
    {
        var qualifiedNameSymbol = Visit(context.qualifiedName());
        Guard.IsOfType<QualifiedNameSymbol>(qualifiedNameSymbol);
        var qualifiedName = ((QualifiedNameSymbol)qualifiedNameSymbol).QualifiedName;
        if (!scopeHandler.GetCurrentScope().SymbolTable.TryGetValue(qualifiedName, out var symbol))
        {
            throw new VariableNotDeclaredException($"Variable with name '{qualifiedName}' not declared.");
        }
        else
        {
            return symbol;
        }
    }

    public override Symbol VisitArrayExpression(qutes_parser.ArrayExpressionContext context)
    {
        return base.VisitArrayExpression(context);
    }

    public override Symbol VisitFunctionCallExpression(qutes_parser.FunctionCallExpressionContext context)
    {
        return base.VisitFunctionCallExpression(context);
    }

    public override Symbol VisitArrayAccessExpression(qutes_parser.ArrayAccessExpressionContext context)
    {
        return base.VisitArrayAccessExpression(context);
    }

    public override Symbol VisitPostfixOperator(qutes_parser.PostfixOperatorContext context)
    {
        return base.VisitPostfixOperator(context);
    }

    public override Symbol VisitExpOperator(qutes_parser.ExpOperatorContext context)
    {
        return base.VisitExpOperator(context);
    }

    public override Symbol VisitPrefixOperator(qutes_parser.PrefixOperatorContext context)
    {
        return base.VisitPrefixOperator(context);
    }

    public override Symbol VisitMultiplicativeOperator(qutes_parser.MultiplicativeOperatorContext context)
    {
        return base.VisitMultiplicativeOperator(context);
    }

    public override Symbol VisitSumOperator(qutes_parser.SumOperatorContext context)
    {
        Guard.IsOfType<ValueSymbol>(context.expr(0));
        var leftSymbol = (ValueSymbol)Visit(context.expr(0));
        Guard.IsOfType<ValueSymbol>(context.expr(1));
        var RightSymbol = (ValueSymbol)Visit(context.expr(1));

        if (leftSymbol.Value.GetType() != RightSymbol.Value.GetType())
        {
            throw new InvalidOperationException($"Cannot apply logical operator '{context.GetChild(1).GetText()}' between different types '{leftSymbol.Value.GetType().Name}' and '{RightSymbol.Value.GetType().Name}'.");
        }

        switch (leftSymbol.Value)
        {
            case IQuantumType leftValue when RightSymbol.Value is IQuantumType rightValue:
                {
                    var operation
                       = context.ADD() != null ? leftValue.Addition(rightValue)
                       : context.SUB() != null ? leftValue.Subtraction(rightValue)
                       : throw new InvalidOperationException($"Unknown operator '{context.GetChild(1).GetText()}'.");
                    var destinationSymbol = new AnonymousValueSymbol(operation.Destination, scopeHandler.GetCurrentScope(), context.Start.TokenIndex);
                    circuitHandler.PushOperation(operation);
                    return destinationSymbol;
                }

            case IClassicalType leftValue when RightSymbol.Value is IClassicalType rightValue:
                {
                    var result
                        = context.ADD() != null ? leftValue.Addition(rightValue)
                        : context.SUB() != null ? leftValue.Subtraction(rightValue)
                        : throw new InvalidOperationException($"Unknown operator '{context.GetChild(1).GetText()}'.");
                    return new AnonymousValueSymbol(result, scopeHandler.GetCurrentScope(), context.Start.TokenIndex);
                }

            default:
                throw new InvalidOperationException($"Cannot apply operator '{context.GetChild(1).GetText()}' to type '{leftSymbol.Value.GetType().Name}'.");
        }
    }

    public override Symbol VisitShiftOperator(qutes_parser.ShiftOperatorContext context)
    {
        Guard.IsOfType<ValueSymbol>(context.expr(0));
        var leftSymbol = (ValueSymbol)Visit(context.expr(0));
        Guard.IsOfType<ValueSymbol>(context.expr(1));
        var RightSymbol = (ValueSymbol)Visit(context.expr(1));

        switch (leftSymbol.Value)
        {
            case IQuantumType leftValue when RightSymbol.Value is QuintType rightValue:
                {
                    var operation
                        = context.LSHIFT() != null ? leftValue.LShift(rightValue)
                        : context.RSHIFT() != null ? leftValue.RShift(rightValue)
                        : throw new InvalidOperationException($"Unknown operator '{context.GetChild(1).GetText()}'.");
                    //TODO: we are assuming that the destination is a new anonymous variable, but in this case the operation happens inplace,
                    // we should assume to know this detail? or is it ok to create this new anon var?
                    var destinationSymbol = new AnonymousValueSymbol(operation.Destination, scopeHandler.GetCurrentScope(), context.Start.TokenIndex);
                    circuitHandler.PushOperation(operation);
                    return destinationSymbol;
                }

            case IClassicalType leftValue when RightSymbol.Value is IntType rightValue:
                {
                    var result
                        = context.LSHIFT() != null ? leftValue.LShift(rightValue)
                        : context.RSHIFT() != null ? leftValue.RShift(rightValue)
                        : throw new InvalidOperationException($"Unknown operator '{context.GetChild(1).GetText()}'.");
                    return new AnonymousValueSymbol(result, scopeHandler.GetCurrentScope(), context.Start.TokenIndex);
                }

            default:
                throw new InvalidOperationException($"Cannot apply operator '{context.GetChild(1).GetText()}' to type '{leftSymbol.Value.GetType().Name}'.");
        }
    }

    public override Symbol VisitRelationalOperator(qutes_parser.RelationalOperatorContext context)
    {
        var leftSymbol = QutesLanguageGuard.IsAssignableToType<ValueSymbol>(Visit(context.expr(0)));
        var rightSymbol = QutesLanguageGuard.IsAssignableToType<ValueSymbol>(Visit(context.expr(1)));

        if (leftSymbol.Value.GetType() != rightSymbol.Value.GetType())
        {
            throw new InvalidOperationException($"Cannot apply operator '{context.GetChild(1).GetText()}' between different types '{leftSymbol.Value.GetType().Name}' and '{rightSymbol.Value.GetType().Name}'.");
        }

        switch (leftSymbol.Value)
        {
            case IQuantumType leftValue when rightSymbol.Value is IQuantumType rightValue:
                {
                    var operation
                        = context.LOWER() != null ? leftValue.LowerThan(rightValue)
                        : context.LOWEREQUAL() != null ? leftValue.LowerEqualThan(rightValue)
                        : context.GREATER() != null ? leftValue.GreaterThan(rightValue)
                        : context.GREATEREQUAL() != null ? leftValue.GreaterEqualThan(rightValue)
                        : throw new InvalidOperationException($"Unknown operator '{context.GetChild(1).GetText()}'.");
                    var destinationSymbol = new AnonymousValueSymbol(operation.Destination, scopeHandler.GetCurrentScope(), context.Start.TokenIndex);
                    circuitHandler.PushOperation(operation);
                    return destinationSymbol;
                }

            case IClassicalType leftValue when rightSymbol.Value is IClassicalType rightValue:
                {
                    var result
                        = context.LOWER() != null ? leftValue.LowerThan(rightValue)
                        : context.LOWEREQUAL() != null ? leftValue.LowerEqualThan(rightValue)
                        : context.GREATER() != null ? leftValue.GreaterThan(rightValue)
                        : context.GREATEREQUAL() != null ? leftValue.GreaterEqualThan(rightValue)
                        : throw new InvalidOperationException($"Unknown operator '{context.GetChild(1).GetText()}'.");
                    return new AnonymousValueSymbol(result, scopeHandler.GetCurrentScope(), context.Start.TokenIndex);
                }

            default:
                throw new InvalidOperationException($"Cannot apply operator '{context.GetChild(1).GetText()}' to type '{leftSymbol.Value.GetType().Name}'.");
        }
    }

    public override Symbol VisitEqualityOperator(qutes_parser.EqualityOperatorContext context)
    {
        var leftSymbol = QutesLanguageGuard.IsAssignableToType<ValueSymbol>(Visit(context.expr(0)));
        var rightSymbol = QutesLanguageGuard.IsAssignableToType<ValueSymbol>(Visit(context.expr(1)));

        if (leftSymbol.Value.GetType() != rightSymbol.Value.GetType())
        {
            throw new InvalidOperationException($"Cannot apply operator '{context.GetChild(1).GetText()}' between different types '{leftSymbol.Value.GetType().Name}' and '{rightSymbol.Value.GetType().Name}'.");
        }

        switch (leftSymbol.Value)
        {
            case IQuantumType leftValue when rightSymbol.Value is IQuantumType rightValue:
                {
                    var operation
                        = context.EQUAL() != null ? leftValue.Equals(rightValue)
                        : context.NOT_EQUAL() != null ? leftValue.NotEquals(rightValue)
                        : throw new InvalidOperationException($"Unknown operator '{context.GetChild(1).GetText()}'.");
                    var destinationSymbol = new AnonymousValueSymbol(operation.Destination, scopeHandler.GetCurrentScope(), context.Start.TokenIndex);
                    circuitHandler.PushOperation(operation);
                    return destinationSymbol;
                }

            case IClassicalType leftValue when rightSymbol.Value is IClassicalType rightValue:
                {
                    var result
                        = context.EQUAL() != null ? leftValue.Equals(rightValue)
                        : context.NOT_EQUAL() != null ? leftValue.NotEquals(rightValue)
                        : throw new InvalidOperationException($"Unknown operator '{context.GetChild(1).GetText()}'.");
                    return new AnonymousValueSymbol(result, scopeHandler.GetCurrentScope(), context.Start.TokenIndex);
                }

            default:
                throw new InvalidOperationException($"Cannot apply operator '{context.GetChild(1).GetText()}' to type '{leftSymbol.Value.GetType().Name}'.");
        }
    }

    public override Symbol VisitLogicAndOperator(qutes_parser.LogicAndOperatorContext context)
    {
        var leftSymbol = QutesLanguageGuard.IsAssignableToType<ValueSymbol>(Visit(context.expr(0)));
        var rightSymbol = QutesLanguageGuard.IsAssignableToType<ValueSymbol>(Visit(context.expr(1)));

        switch (leftSymbol.Value)
        {
            case IQuantumType leftValue when rightSymbol.Value is IQuantumType rightValue:
                {
                    var operation
                        = context.AND() != null ? leftValue.And(rightValue)
                        : throw new InvalidOperationException($"Unknown operator '{context.GetChild(1).GetText()}'.");
                    var destinationSymbol = new AnonymousValueSymbol(operation.Destination, scopeHandler.GetCurrentScope(), context.Start.TokenIndex);
                    circuitHandler.PushOperation(operation);
                    return destinationSymbol;
                }

            case IClassicalType leftValue when rightSymbol.Value is IClassicalType rightValue:
                {
                    var result
                        = context.AND() != null ? leftValue.And(rightValue)
                        : throw new InvalidOperationException($"Unknown operator '{context.GetChild(1).GetText()}'.");
                    return new AnonymousValueSymbol(result, scopeHandler.GetCurrentScope(), context.Start.TokenIndex);
                }

            default:
                throw new InvalidOperationException($"Cannot apply operator '{context.GetChild(1).GetText()}' to type '{leftSymbol.Value.GetType().Name}'.");
        }
    }

    public override Symbol VisitLogicOrOperator(qutes_parser.LogicOrOperatorContext context)
    {
        var leftSymbol = QutesLanguageGuard.IsAssignableToType<ValueSymbol>(Visit(context.expr(0)));
        var rightSymbol = QutesLanguageGuard.IsAssignableToType<ValueSymbol>(Visit(context.expr(1)));

        switch (leftSymbol.Value)
        {
            case IQuantumType leftValue when rightSymbol.Value is IQuantumType rightValue:
                {
                    var operation
                        = context.OR() != null ? leftValue.Or(rightValue)
                        : throw new InvalidOperationException($"Unknown operator '{context.GetChild(1).GetText()}'.");
                    var destinationSymbol = new AnonymousValueSymbol(operation.Destination, scopeHandler.GetCurrentScope(), context.Start.TokenIndex);
                    circuitHandler.PushOperation(operation);
                    return destinationSymbol;
                }

            case IClassicalType leftValue when rightSymbol.Value is IClassicalType rightValue:
                {
                    var result
                        = context.OR() != null ? leftValue.Or(rightValue)
                        : throw new InvalidOperationException($"Unknown operator '{context.GetChild(1).GetText()}'.");
                    return new AnonymousValueSymbol(result, scopeHandler.GetCurrentScope(), context.Start.TokenIndex);
                }

            default:
                throw new InvalidOperationException($"Cannot apply operator '{context.GetChild(1).GetText()}' to type '{leftSymbol.Value.GetType().Name}'.");
        }
    }

    public override Symbol VisitDoubleUnaryOperator(qutes_parser.DoubleUnaryOperatorContext context)
    {
        var firstSymbol = QutesLanguageGuard.IsAssignableToType<ValueSymbol>(Visit(context.expr(0)));
        var secondSymbol = QutesLanguageGuard.IsAssignableToType<ValueSymbol>(Visit(context.expr(1)));

        switch (firstSymbol.Value)
        {
            case IQuantumType firstValue when secondSymbol.Value is IQuantumType secondValue:
                {
                    var operation
                        = context.SWAP() != null ? firstValue.Swap(secondValue)
                        : throw new InvalidOperationException($"Unknown operator '{context.GetChild(1).GetText()}'.");
                    var destinationSymbol = new AnonymousValueSymbol(operation.Destination, scopeHandler.GetCurrentScope(), context.Start.TokenIndex);
                    circuitHandler.PushOperation(operation);
                    return destinationSymbol;
                }

            case IClassicalType leftValue when secondSymbol.Value is IClassicalType rightValue:
                {
                    var result
                        = context.SWAP() != null ? leftValue.Swap(rightValue)
                        : throw new InvalidOperationException($"Unknown operator '{context.GetChild(1).GetText()}'.");
                    return new AnonymousValueSymbol(result, scopeHandler.GetCurrentScope(), context.Start.TokenIndex);
                }

            default:
                throw new InvalidOperationException($"Cannot apply operator '{context.GetChild(1).GetText()}' to type '{firstSymbol.Value.GetType().Name}'.");
        }
    }

    public override Symbol VisitMultipleUnaryOperator(qutes_parser.MultipleUnaryOperatorContext context)
    {
        var termListSymbol = QutesLanguageGuard.IsAssignableToType<TupleSymbol>(Visit(context.termList()));
        var termListSymbolValue = QutesLanguageGuard.AreAllAssignableToType<IQuantumType>(termListSymbol.Elements.Cast<ValueSymbol>().Select(e => e.Value));
        var target = termListSymbolValue.Last();
        var controls = termListSymbolValue.Take(termListSymbol.Elements.Count() - 1);

        CircuitOperation operation 
            = context.MCX() != null ? new MCX(controls, target)
            : context.MCZ() != null ? new MCZ(controls, target)
            : context.MCY() != null ? new MCY(controls, target)
            : throw new InvalidOperationException($"Unknown operator '{context.GetChild(1).GetText()}'.");
        var destinationSymbol = new AnonymousValueSymbol(operation.Destination, scopeHandler.GetCurrentScope(), context.Start.TokenIndex);
        circuitHandler.PushOperation(operation);
        return destinationSymbol;
    }

    public override Symbol VisitUnaryOperator(qutes_parser.UnaryOperatorContext context)
    {
        var targetSymbol = QutesLanguageGuard.IsAssignableToType<ValueSymbol>(Visit(context.expr()));

        switch (targetSymbol.Value)
        {
            case IQuantumType targetValue:
                {
                    if (context.PRINT() != null)
                    {
                        Console.WriteLine($"Quantum State: {targetValue.QubitStringList}");
                        return targetSymbol;
                    }

                    CircuitOperation operation
                        = context.HADAMARD() != null ? new Hadamard(targetValue)
                        : context.PAULIY() != null ? new PauliY(targetValue)
                        : context.PAULIZ() != null ? new PauliZ(targetValue)
                        : context.MEASURE() != null ? new Measure(targetValue)
                        : throw new InvalidOperationException($"Unknown operator '{context.GetChild(1).GetText()}'.");
                    var destinationSymbol = new AnonymousValueSymbol(operation.Destination, scopeHandler.GetCurrentScope(), context.Start.TokenIndex);
                    circuitHandler.PushOperation(operation);
                    return destinationSymbol;
                }

            case IClassicalType targetValue:
                {
                    if (context.PRINT() != null)
                    {
                        Console.WriteLine($"State: {targetValue.GetValueAsObject()}");
                        return targetSymbol;
                    }

                    throw new InvalidOperationException($"Cannot apply operator '{context.GetChild(1).GetText()}' to type '{targetSymbol.Value.GetType().Name}'.");
                }
            default:
                throw new InvalidOperationException($"Cannot apply operator '{context.GetChild(1).GetText()}' to type '{targetSymbol.Value.GetType().Name}'.");
        }
    }

    public override Symbol VisitMultipleUnaryPhaseOperator(qutes_parser.MultipleUnaryPhaseOperatorContext context)
    {
        var rotationSymbol = QutesLanguageGuard.IsAssignableToType<ValueSymbol>(Visit(context.expr()));
        var rotationValue = QutesLanguageGuard.IsAssignableToType<FloatType>(rotationSymbol.Value);
        var termListSymbol = QutesLanguageGuard.IsAssignableToType<TupleSymbol>(Visit(context.termList()));
        var termListElements = QutesLanguageGuard.AreAllAssignableToType<IQuantumType>(termListSymbol.Elements.Cast<ValueSymbol>().Select(e => e.Value));
        var controls = termListElements.Take(termListSymbol.Elements.Count() - 1);
        var target = termListElements.Last();

        CircuitOperation operation
            = context.MCP() != null ? new MCP(controls, target, rotationValue)
            : throw new InvalidOperationException($"Unknown operator '{context.GetChild(1).GetText()}'.");
        var destinationSymbol = new AnonymousValueSymbol(operation.Destination, scopeHandler.GetCurrentScope(), context.Start.TokenIndex);
        circuitHandler.PushOperation(operation);
        return destinationSymbol;
    }

    public override Symbol VisitGroverOperator(qutes_parser.GroverOperatorContext context)
    {
        return base.VisitGroverOperator(context);
    }

    public override Symbol VisitFreeGroverOperator(qutes_parser.FreeGroverOperatorContext context)
    {
        return base.VisitFreeGroverOperator(context);
    }

    // ReSharper disable once RedundantOverriddenMember
    public override Symbol VisitExpr(qutes_parser.ExprContext context)
    {
        return base.VisitExpr(context); //return the specific expr child type symbol
    }

    // ReSharper disable once RedundantOverriddenMember
    public override Symbol VisitStatement(qutes_parser.StatementContext context)
    {
        return base.VisitStatement(context); //return the specific statement child type symbol
    }

    public override Symbol VisitFunctionDeclarationParams(qutes_parser.FunctionDeclarationParamsContext context)
    {
        var symbols = context.variableDeclaration().Select(e => Visit(e)) ?? [];
        return new TupleSymbol(symbols, scopeHandler.GetCurrentScope(), context.Start.TokenIndex);
    }

    public override Symbol VisitVariableDeclaration(qutes_parser.VariableDeclarationContext context)
    {
        var varTypeSymbol = Visit(context.variableType());
        var qualifiedNameSymbol = Visit(context.qualifiedName());
        Guard.IsOfType<TypeSymbol>(varTypeSymbol);
        Guard.IsOfType<QualifiedNameSymbol>(qualifiedNameSymbol);
        
        AnonymousValueSymbol valueSymbol;
        if (context.expr() is not null)
        {
            valueSymbol = (AnonymousValueSymbol)Visit(context.expr());
        }
        else
        {
            valueSymbol = GetDefaultValueSymbolForType(varTypeSymbol);
        }

        var qualifiedName = ((QualifiedNameSymbol)qualifiedNameSymbol).QualifiedName;
        var namedSymbol = new ValueSymbol(qualifiedName, valueSymbol.Value, scopeHandler.GetCurrentScope(), context.Start.TokenIndex);
        DeclareNewVariable(namedSymbol);
        
        if(valueSymbol.Value is IQuantumType quantumValue)
        {
            circuitHandler.DeclareQuantumRegister(valueSymbol.QualifiedName, quantumValue.Qubits);
        }

        return namedSymbol;
    }

    private void DeclareNewVariable(ValueSymbol symbol)
    {
        if (scopeHandler.GetCurrentScope().SymbolTable.ContainsKey(symbol.QualifiedName))
        {
            throw new VariableAlreadyDeclaredException($"Variable with name '{symbol.QualifiedName}' already declared.");
        }
        scopeHandler.GetCurrentScope().SymbolTable[symbol.QualifiedName] = symbol;
    }

    public override Symbol VisitArrayAccess(qutes_parser.ArrayAccessContext context)
    {
        var indexSymbol = (AnonymousValueSymbol)Visit(context.expr());
        var qualifiedName = Visit(context.qualifiedName());
        Guard.IsOfType<IntType>(indexSymbol.Value);
        var index = ((IntType)indexSymbol.Value).Value;
        var symbol = FindSymbolByQualifiedName(qualifiedName);
        Guard.IsOfType<ArraySymbol>(symbol);
        return ((ArraySymbol)symbol).Elements.ElementAt(index);

    }

    public override Symbol VisitArrayLiteral(qutes_parser.ArrayLiteralContext context)
    {
        var tupleSymbol = (TupleSymbol)Visit(context.termList());
        var elements = tupleSymbol.Elements;
        var arrayType = elements.First().GetType();
        Guard.IsTrue(elements.All(e => e.GetType() == arrayType));//TODO: is the case to use QutesLanguageAssert everywhere?
        //TODO: should we memorize the arraySymbol type based on the type of its elements?
        return new ArraySymbol(tupleSymbol.Elements, scopeHandler.GetCurrentScope(), context.Start.TokenIndex); 
    }
    
    public override Symbol VisitTermList(qutes_parser.TermListContext context)
    {
        //TODO: in grammar, use arrayLiteral instead of termList everywhere?
        var symbols = context.expr().Select(e => Visit(e)) ?? [];

        return new TupleSymbol(symbols, scopeHandler.GetCurrentScope(), context.Start.TokenIndex);
    }

    public override Symbol VisitVariableType(qutes_parser.VariableTypeContext context)
    {
        return context.type() is not null ? Visit(context.type()) : Visit(context.qualifiedName());
    }

    public override Symbol VisitType(qutes_parser.TypeContext context)
    {
        var value = Convert.ToString(context.GetChild(0).GetText());
        return new TypeSymbol(value, scopeHandler.GetCurrentScope(), context.Start.TokenIndex);
    }

    public override Symbol VisitQualifiedName(qutes_parser.QualifiedNameContext context)
    {
        //this is used in variable/function usage and declaration,
        //so cannot return a Symbol taken from the symbol table by name.
        var value = string.Join('.', context.SYMBOL_LITERAL().Select(e => e.GetText()));
        return new QualifiedNameSymbol(value, scopeHandler.GetCurrentScope(), context.Start.TokenIndex);
    }

    // ReSharper disable once RedundantOverriddenMember
    public override Symbol VisitLiteral(qutes_parser.LiteralContext context)
    {
        return base.VisitLiteral(context); //return the symbol of the specific literal children type 
    }

    public override Symbol VisitString(qutes_parser.StringContext context)
    {
        var value = Convert.ToString(context.STRING_LITERAL().GetText());
        return new AnonymousValueSymbol(new StringType(value), scopeHandler.GetCurrentScope(), context.Start.TokenIndex);
    }

    public override Symbol VisitQubit(qutes_parser.QubitContext context)
    {
        var value = context.QUBIT_LITERAL().GetText();
        return new AnonymousValueSymbol(new QubitType(value), scopeHandler.GetCurrentScope(), context.Start.TokenIndex);
    }

    public override Symbol VisitQuint(qutes_parser.QuintContext context)
    {
        var value = context.QUINT_LITERAL().GetText();
        return new AnonymousValueSymbol(new QuintType(value), scopeHandler.GetCurrentScope(), context.Start.TokenIndex);
    }

    public override Symbol VisitQustring(qutes_parser.QustringContext context)
    {
        var value = context.QUSTRING_LITERAL().GetText();
        return new AnonymousValueSymbol(new QustringType(value), scopeHandler.GetCurrentScope(), context.Start.TokenIndex);
    }

    public override Symbol VisitFloat(qutes_parser.FloatContext context)
    {
        var value = Convert.ToSingle(context.FLOAT_LITERAL().GetText());
        return new AnonymousValueSymbol(new FloatType(value), scopeHandler.GetCurrentScope(), context.Start.TokenIndex);
    }

    public override Symbol VisitInteger(qutes_parser.IntegerContext context)
    {
        var value = Convert.ToInt32(context.INT_LITERAL().GetText());
        return new AnonymousValueSymbol(new IntType(value), scopeHandler.GetCurrentScope(), context.Start.TokenIndex);
    }

    public override Symbol VisitBoolean(qutes_parser.BooleanContext context)
    {
        var value = Convert.ToBoolean(context.BOOL_LITERAL().GetText());
        return new AnonymousValueSymbol(new BoolType(value), scopeHandler.GetCurrentScope(), context.Start.TokenIndex);
    }
}