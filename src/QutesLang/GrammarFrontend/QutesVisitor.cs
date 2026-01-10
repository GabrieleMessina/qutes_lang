using Antlr4.Runtime.Misc;
using Antlr4.Runtime.Tree;

using CommunityToolkit.Diagnostics;

using Qutes.Grammar;

using QutesLang.Symbols;
using QutesLang.Symbols.Types;
namespace QutesLang.GrammarFrontend;

public class QutesVisitor(IScopeHandler scopeHandler, ICircuitHandler circuitHandler) : qutes_parserBaseVisitor<Symbol>
{
    protected override bool ShouldVisitNextChild([NotNull] IRuleNode node, Symbol currentResult)
    {
        return !handlingReturnStatement;
    }

    private AnonymousValueSymbol GetDefaultValueSymbolForType(TypeSymbol varTypeSymbol)
    {
        //todo: get default value, even if we decide null is ok for uninitialized variables, it's better to have a function retrieving that.
        throw new NotImplementedException();
    }

    private void DeclareNewVariable(ValueSymbol symbol)
    {
        scopeHandler.GetCurrentScope().DefineVariable(symbol);
    }

    private void DeclareNewFunction(FunctionSymbol symbol)
    {
        scopeHandler.GetCurrentScope().DefineFunction(symbol);
    }

    public override Symbol VisitProgram(qutes_parser.ProgramContext context)
    {
        circuitHandler.PushCircuit(circuitHandler.CreateNewCircuit());
        scopeHandler.PushScope(scopeHandler.CreateScope());
        CheckForFunctionHoisting(context);
        return base.VisitProgram(context); //return value doesn't matter no one will use it.
    }

    public override Symbol VisitBlockStatement(qutes_parser.BlockStatementContext context)
    {
        scopeHandler.PushScope(scopeHandler.CreateScope());
        CheckForFunctionHoisting(context);
        return base.VisitBlockStatement(context); //return value doesn't matter no one will use it.
    }

    public override Symbol VisitIfStatement(qutes_parser.IfStatementContext context)
    {
        var condition = QutesLanguageGuard.IsAssignableToType<ValueSymbol>(Visit(context.expr()));
        var ifBody = context.statement();

        switch (condition.Value)
        {
            case IQuantumType quantumCondition:
                var mainCircuit = circuitHandler.Current;
                HandleBranchingVisiting(ifBody, quantumCondition, mainCircuit);
                break;
            case BoolType boolCondition:
                if (boolCondition.Value == true) Visit(ifBody);
                break;
            default:
                throw new InvalidOperationException("If condition must be of type 'bool' or a quantum type.");
        }

        return null!;
    }

    public override Symbol VisitIfElseStatement(qutes_parser.IfElseStatementContext context)
    {
        var condition = QutesLanguageGuard.IsAssignableToType<ValueSymbol>(Visit(context.expr()));
        var ifBody = context.statement(0);
        var elseBody = context.statement(1);

        switch (condition.Value)
        {
            case IQuantumType quantumCondition:
                var mainCircuit = circuitHandler.Current;
                HandleBranchingVisiting(ifBody, quantumCondition, mainCircuit);
                HandleBranchingVisiting(elseBody, quantumCondition, mainCircuit, false);
                break;
            case BoolType boolCondition:
                if (boolCondition.Value == true) Visit(ifBody);
                else Visit(elseBody);
                break;
            default:
                throw new InvalidOperationException("If-Else condition must be of type 'bool' or a quantum type.");
        }

        return null!;
    }

    private void HandleBranchingVisiting(qutes_parser.StatementContext branchBody, IQuantumType quantumCondition, IQuantumCircuit mainCircuit, bool onCondition = true)
    {
        var quantumBodyCircuit = circuitHandler.CreateNewCircuit();
        var controlledCircuit = quantumBodyCircuit.MakeControlledBy(quantumCondition.Register, onCondition);
        circuitHandler.PushCircuit(controlledCircuit);
        circuitHandler.PushCircuit(quantumBodyCircuit);
        Visit(branchBody); //TODO: how to handle classical ops inside quantum if body.
        circuitHandler.PopCircuit();
        circuitHandler.PopCircuit();
        mainCircuit.PushOperation(new ComposeCircuit(controlledCircuit));
    }

    public override Symbol VisitWhileStatement(qutes_parser.WhileStatementContext context)
    {
        var temp = Visit(context.expr());
        var condition = QutesLanguageGuard.IsAssignableToType<ValueSymbol>(temp);
        var whileBody = context.statement();

        switch (condition.Value)
        {
            case IQuantumType:
                //TODO: quantum while loops could be implemented with repeated appended controlled circuits based on all possible combination of the qubits in the condition register.
                throw new NotImplementedException("Quantum while loops are not yet implemented.");
            case BoolType classicalCondition:
                while (classicalCondition.Value && !handlingBreakStatement)
                {
                    Visit(whileBody);
                    classicalCondition = QutesLanguageGuard.IsAssignableToType<BoolType>(QutesLanguageGuard.IsAssignableToType<ValueSymbol>(Visit(context.expr())).Value);
                }
                handlingBreakStatement = false;
                break;
            default:
                throw new InvalidOperationException("While loop condition must be of type 'bool' or a quantum type.");
        }

        return null!;
    }

    public override Symbol VisitForeachStatement(qutes_parser.ForeachStatementContext context)
    {
        var valueSymbol = QutesLanguageGuard.IsAssignableToType<ValueSymbol>(Visit(context.expr()));
        var itemNameSymbol = QutesLanguageGuard.IsAssignableToType<QualifiedNameSymbol>(Visit(context.qualifiedName(0)));
        QualifiedNameSymbol? indexNameSymbol = null;

        if (context.qualifiedName(1) != null)
        {
            indexNameSymbol = QutesLanguageGuard.IsAssignableToType<QualifiedNameSymbol>(Visit(context.qualifiedName(1)));
        }

        if(valueSymbol.Value is IArrayType collection)
        {
            for (int i = 0; i < collection.Values.Count() && !handlingBreakStatement; i++)
            {
                var itemElementSymbol = QutesLanguageGuard.IsAssignableToType<ValueSymbol>(collection.Values.ElementAt(i));
                var itemSymbol = new ValueSymbol(itemNameSymbol.QualifiedName, itemElementSymbol.Value, scopeHandler.GetCurrentScope(), context.Start.TokenIndex);
                DeclareNewVariable(itemSymbol);
                if (indexNameSymbol != null)
                {
                    var indexSymbol = new ValueSymbol(indexNameSymbol.QualifiedName, new IntType(i), scopeHandler.GetCurrentScope(), context.Start.TokenIndex);
                    DeclareNewVariable(indexSymbol);
                }
                Visit(context.statement());
            }
            handlingBreakStatement = false;
            return null!;
        }

        throw new InvalidOperationException("Foreach loop can only iterate over array types.");
    }

    public override Symbol VisitDoWhileStatement(qutes_parser.DoWhileStatementContext context)
    {
        var condition = QutesLanguageGuard.IsAssignableToType<ValueSymbol>(Visit(context.expr()));
        var whileBody = context.statement();

        switch (condition.Value)
        {
            case IQuantumType:
                throw new NotImplementedException("Quantum while loops are not yet implemented.");
            case BoolType classicalCondition:
                do
                {
                    Visit(whileBody);
                    classicalCondition = QutesLanguageGuard.IsAssignableToType<BoolType>(QutesLanguageGuard.IsAssignableToType<ValueSymbol>(Visit(context.expr())).Value);
                }
                while (classicalCondition.Value && !handlingBreakStatement);
                handlingBreakStatement = false;
                break;
            default:
                throw new InvalidOperationException("While loop condition must be of type 'bool' or a quantum type.");
        }

        return null!;
    }

    public override Symbol VisitFunctionDeclarationStatement([NotNull] qutes_parser.FunctionDeclarationStatementContext context)
    {
        return null!; //this is handled by HandleFunctionsHoisting
    }

    private void CheckForFunctionHoisting(Antlr4.Runtime.ParserRuleContext context)
    {
        foreach (var node in context.children)
        {
            if (node is qutes_parser.BlockStatementContext or qutes_parser.ProgramContext)
            {
                break;
            }
            if (node is qutes_parser.FunctionDeclarationStatementContext functionDeclarationStatementContext)
            {
                HandleFunctionsHoisting(functionDeclarationStatementContext);
            }
        }
    }

    private FunctionSymbol HandleFunctionsHoisting(qutes_parser.FunctionDeclarationStatementContext context)
    {
        var outputTypeSymbol = QutesLanguageGuard.IsAssignableToType<TypeSymbol>(Visit(context.variableType()));
        var qualifiedNameSymbol = QutesLanguageGuard.IsAssignableToType<QualifiedNameSymbol>(Visit(context.qualifiedName()));

        scopeHandler.PushScope(scopeHandler.CreateScope()); //create function scope for params declaration

        var functionParamsSymbol = 
            context.functionDeclarationParams() == null 
            ? new([], scopeHandler.GetCurrentScope(), context.Start.TokenIndex)
            : QutesLanguageGuard.IsAssignableToType<TupleSymbol>(Visit(context.functionDeclarationParams()));
        var functionParamsValues = QutesLanguageGuard.AreAllAssignableToType<ValueSymbol>(functionParamsSymbol.Elements);
        var functionBody = context.statement();

        var functionScope = scopeHandler.PopScope();

        var qualifiedName = qualifiedNameSymbol.QualifiedName;
        var functionToCreateSymbol = new FunctionSymbol(qualifiedName, functionParamsValues, outputTypeSymbol, functionBody, functionScope, context.Start.TokenIndex);
        DeclareNewFunction(functionToCreateSymbol);

        return functionToCreateSymbol;
    }

    private bool handlingReturnStatement = false;
    private bool handlingBreakStatement = false;
    public override Symbol VisitFunctionCallExpression(qutes_parser.FunctionCallExpressionContext context)
    {
        var qualifiedNameSymbol = QutesLanguageGuard.IsAssignableToType<QualifiedNameSymbol>(Visit(context.qualifiedName()));
        var providedParamsSymbol =
            context.termList() == null
            ? new([], scopeHandler.GetCurrentScope(), context.Start.TokenIndex)
            : QutesLanguageGuard.IsAssignableToType<TupleSymbol>(Visit(context.termList()));
        var providedParamsValues = QutesLanguageGuard.AreAllAssignableToType<ValueSymbol>(providedParamsSymbol.Elements).ToList();

        var qualifiedName = qualifiedNameSymbol.QualifiedName;
        var functionSymbol = scopeHandler.GetCurrentScope().ResolveFunction(qualifiedName);

        //check that the number of parameters match
        if (functionSymbol.InputParamTypes.Count() != providedParamsSymbol.Elements.Count())
        {
            throw new InvalidOperationException($"Function '{qualifiedName}' expects {functionSymbol.InputParamTypes.Count()} parameters, but {providedParamsSymbol.Elements.Count()} were provided.");
        }

        //check that the types of the parameters match
        var functionParamTypes = functionSymbol.InputParamTypes.ToList();

        foreach (var (paramType, index) in functionParamTypes.Select((value, i) => (value.GetType(), i)))
        {
            var providedParamType = providedParamsValues[index].Value.GetType();
            if (paramType != providedParamType)
            {
                throw new InvalidOperationException($"Function '{qualifiedName}' expects parameter of type '{paramType.Name}', but '{providedParamType.Name}' was provided.");
            }
        }

        scopeHandler.PushScope(functionSymbol.Scope);
        var bodyStatementReturnValue = Visit(functionSymbol.Body);
        handlingReturnStatement = false;
        scopeHandler.PopScope();
        if(bodyStatementReturnValue != null)
        {
            var outputSymbol = QutesLanguageGuard.IsAssignableToType<ValueSymbol>(bodyStatementReturnValue);

            if(outputSymbol.Value != functionSymbol.OutputType)
            {
                throw new InvalidOperationException($"Function '{qualifiedName}' should return type '{functionSymbol.OutputType}', but returned type '{outputSymbol.Type}'.");
            }

            return outputSymbol;
        }
        if(functionSymbol.OutputType.Value != QutesType.@void)
        {
            throw new InvalidOperationException($"Function '{qualifiedName}' should return type '{functionSymbol.OutputType}', but no value was returned.");
        }
        return null!;
    }

    public override Symbol VisitReturnStatement(qutes_parser.ReturnStatementContext context)
    {
        ValueSymbol output;
        handlingReturnStatement = true;
        if (context.expr() != null)
        {
            output = QutesLanguageGuard.IsAssignableToType<ValueSymbol>(Visit(context.expr()));
        }
        else
        {
            output = new AnonymousValueSymbol(new VoidType(), scopeHandler.GetCurrentScope(), context.Start.TokenIndex);
        }
        return output;
    }

    public override Symbol VisitBreakStatement([NotNull] qutes_parser.BreakStatementContext context)
    {
        handlingBreakStatement = true;
        return null!; //TODO: is it better to return an errorSymbol?
    }

    public override Symbol VisitDeclarationStatement(qutes_parser.DeclarationStatementContext context)
    {
        return Visit(context.variableDeclaration());
    }

    public override Symbol VisitAssignmentStatement(qutes_parser.AssignmentStatementContext context)
    {
        var qualifiedName = QutesLanguageGuard.IsAssignableToType<ValueSymbol>(Visit(context.expr(0))).QualifiedName;
        var valueToAssignSymbol = QutesLanguageGuard.IsAssignableToType<ValueSymbol>(Visit(context.expr(1)));

        var variableToUpdateSymbol = scopeHandler.GetCurrentScope().ResolveVariable(qualifiedName);

        variableToUpdateSymbol.Value = CastValueToType(valueToAssignSymbol, variableToUpdateSymbol.Type).Value;

        //TODO: check how to handle in case of casting.
        if (variableToUpdateSymbol.Value is IQuantumType quantumValue)
        {
            circuitHandler.UpdateQuantumVariable(variableToUpdateSymbol.QualifiedName, quantumValue.Register);
        }

        return variableToUpdateSymbol;
    }

    public override Symbol VisitExpressionStatement(qutes_parser.ExpressionStatementContext context)
    {
        return Visit(context.expr());
    }

    public override Symbol VisitFactStatement(qutes_parser.FactStatementContext context)
    {
        if (context.MEASURE() != null)
        {
            circuitHandler.PushOperation(new MeasureAll());
        }
        else if (context.BARRIER() != null)
        {
            circuitHandler.PushOperation(new BarrierAll());
        }
        else if (context.PRINT() != null)
        {
            //print all variable, both quantum and classics from symbol table
            foreach (var symbol in scopeHandler.GetCurrentScope().SymbolTable.Values)
            {
                if (symbol is ValueSymbol valueSymbol)
                {
                    switch (valueSymbol.Value)
                    {
                        case IQuantumType quantumType:
                            Console.WriteLine($"{quantumType.Type} '{valueSymbol.QualifiedName}': {quantumType.QubitStringList}");
                            break;
                        case IClassicalType classicalType:
                            Console.WriteLine($"{classicalType.Type} '{valueSymbol.QualifiedName}': {classicalType.GetValueAsObject()}");
                            break;
                    }
                }
            }
        }
        else
        {
            throw new InvalidOperationException($"Unknown operator '{context.GetChild(0).GetText()}'.");
        }

        return null!;
    }

    public override Symbol VisitEmptyStatement(qutes_parser.EmptyStatementContext context)
    {
        return null!;
    }

    public override Symbol VisitExpOperator(qutes_parser.ExpOperatorContext context)
    {
        var leftSymbol = QutesLanguageGuard.IsAssignableToType<ValueSymbol>(Visit(context.expr(0)));
        var rightSymbol = QutesLanguageGuard.IsAssignableToType<ValueSymbol>(Visit(context.expr(1)));

        if (leftSymbol.Value.GetType() != rightSymbol.Value.GetType())
        {
            throw new InvalidOperationException($"Cannot apply logical operator '{context.op.Text}' between different types '{leftSymbol.Type}' and '{rightSymbol.Type}'.");
        }

        switch (leftSymbol.Value)
        {
            case IQuantumType leftValue when rightSymbol.Value is IQuantumType rightValue:
                {
                    var operation
                       = context.EXP() != null ? leftValue.Exp(rightValue)
                       : throw new InvalidOperationException($"Unknown operator '{context.op.Text}'.");
                    var destinationSymbol = new AnonymousValueSymbol(operation.Destination, scopeHandler.GetCurrentScope(), context.Start.TokenIndex);
                    circuitHandler.PushOperation(operation);
                    return destinationSymbol;
                }

            case IClassicalType leftValue when rightSymbol.Value is IClassicalType rightValue:
                {
                    var result
                        = context.EXP() != null ? leftValue.Exp(rightValue)
                        : throw new InvalidOperationException($"Unknown operator '{context.op.Text}'.");
                    return new AnonymousValueSymbol(result, scopeHandler.GetCurrentScope(), context.Start.TokenIndex);
                }

            default:
                throw new InvalidOperationException($"Cannot apply operator '{context.op.Text}' to type '{leftSymbol.Type}'.");
        }
    }

    public override Symbol VisitParentesizeExpression(qutes_parser.ParentesizeExpressionContext context)
    {
        return Visit(context.expr());
    }

    public override Symbol VisitLiteralExpression(qutes_parser.LiteralExpressionContext context)
    {
        return Visit(context.literal());
    }

    public override Symbol VisitQualifiedNameExpression(qutes_parser.QualifiedNameExpressionContext context)
    {
        var qualifiedNameSymbol = QutesLanguageGuard.IsAssignableToType<QualifiedNameSymbol>(Visit(context.qualifiedName()));
        var qualifiedName = qualifiedNameSymbol.QualifiedName;
        var symbol = scopeHandler.GetCurrentScope().ResolveVariable(qualifiedName);
        return symbol;
    }

    public override Symbol VisitArrayExpression(qutes_parser.ArrayExpressionContext context)
    {
        var tupleSymbol = QutesLanguageGuard.IsAssignableToType<TupleSymbol>(Visit(context.termList()));
        var elements = QutesLanguageGuard.AreAllAssignableToType<ValueSymbol>(tupleSymbol.Elements);
        var arrayType = elements.First().Type;

        //TODO: Chefk that all elements are of the same type or can be casted to the same type.
        //Guard.IsTrue(elements.All(e => e.Type == arrayType)); //how should we handle [1q,0,3,1]?

        if (arrayType.IsQuantum())
        {
            return new AnonymousValueSymbol(new QuantumArrayType(elements), scopeHandler.GetCurrentScope(), context.Start.TokenIndex);
        }
        else
        {
            return new AnonymousValueSymbol(new ClassicalArrayType(elements), scopeHandler.GetCurrentScope(), context.Start.TokenIndex);
        }

        throw new InvalidOperationException("Array elements must be of quantum or classical types.");
    }

    public override Symbol VisitArrayAccessExpression(qutes_parser.ArrayAccessExpressionContext context)
    {
        var arraySymbol = QutesLanguageGuard.IsAssignableToType<ValueSymbol>(Visit(context.expr(0)));
        if (arraySymbol.Value is IArrayType array)
        {
            var indexSymbol = QutesLanguageGuard.IsAssignableToType<ValueSymbol>(Visit(context.expr(1)));
            var indexValue = QutesLanguageGuard.IsAssignableToType<IntType>(indexSymbol.Value).Value;
            return array.Values.ElementAt(indexValue);
        }
        else
        {
            throw new InvalidOperationException($"Cannot access index of non-array type '{arraySymbol.Type}'.");
        }
    }

    public override Symbol VisitPostfixOperator(qutes_parser.PostfixOperatorContext context)
    {
        var targetSymbol = QutesLanguageGuard.IsAssignableToType<ValueSymbol>(Visit(context.expr()));

        switch (targetSymbol.Value)
        {
            case IQuantumType leftValue:
                {
                    var operation
                       = context.AUTO_INCREMENT() != null ? leftValue.InplacePostIncrement()
                       : context.AUTO_DECREMENT() != null ? leftValue.InplacePostDecrement()
                       : throw new InvalidOperationException($"Unknown operator '{context.op.Text}'.");
                    var destinationSymbol = new AnonymousValueSymbol(operation.Destination, scopeHandler.GetCurrentScope(), context.Start.TokenIndex);
                    circuitHandler.PushOperation(operation);
                    return destinationSymbol;
                }

            case IClassicalType leftValue:
                {
                    var result
                        = context.AUTO_INCREMENT() != null ? leftValue.InplacePostIncrement()
                        : context.AUTO_DECREMENT() != null ? leftValue.InplacePostDecrement()
                        : throw new InvalidOperationException($"Unknown operator '{context.op.Text}'.");
                    return new AnonymousValueSymbol(result, scopeHandler.GetCurrentScope(), context.Start.TokenIndex);
                }

            default:
                throw new InvalidOperationException($"Cannot apply operator '{context.op.Text}' to type '{targetSymbol.Type}'.");
        }
    }

    public override Symbol VisitPrefixOperator(qutes_parser.PrefixOperatorContext context)
    {
        var targetSymbol = QutesLanguageGuard.IsAssignableToType<ValueSymbol>(Visit(context.expr()));

        switch (targetSymbol.Value)
        {
            case IQuantumType leftValue:
                {
                    var operation
                       = context.NOT() != null ? leftValue.Not()
                       : context.ADD() != null ? leftValue.Plus()
                       : context.SUB() != null ? leftValue.Minus()
                       : context.AUTO_INCREMENT() != null ? leftValue.InplacePreIncrement()
                       : context.AUTO_DECREMENT() != null ? leftValue.InplacePreDecrement()
                       : throw new InvalidOperationException($"Unknown operator '{context.op.Text}'.");
                    var destinationSymbol = new AnonymousValueSymbol(operation.Destination, scopeHandler.GetCurrentScope(), context.Start.TokenIndex);
                    circuitHandler.PushOperation(operation);
                    return destinationSymbol;
                }

            case IClassicalType leftValue:
                {
                    var result
                        = context.NOT() != null ? leftValue.Not()
                        : context.ADD() != null ? leftValue.Plus()
                        : context.SUB() != null ? leftValue.Minus()
                        : context.AUTO_INCREMENT() != null ? leftValue.InplacePreIncrement()
                        : context.AUTO_DECREMENT() != null ? leftValue.InplacePreDecrement()
                        : throw new InvalidOperationException($"Unknown operator '{context.op.Text}'.");
                    return new AnonymousValueSymbol(result, scopeHandler.GetCurrentScope(), context.Start.TokenIndex);
                }

            default:
                throw new InvalidOperationException($"Cannot apply operator '{context.op.Text}' to type '{targetSymbol.Type}'.");
        }
    }

    public override Symbol VisitMultiplicativeOperator(qutes_parser.MultiplicativeOperatorContext context)
    {
        var leftSymbol = QutesLanguageGuard.IsAssignableToType<ValueSymbol>(Visit(context.expr(0)));
        var rightSymbol = QutesLanguageGuard.IsAssignableToType<ValueSymbol>(Visit(context.expr(1)));

        if (leftSymbol.Value.GetType() != rightSymbol.Value.GetType())
        {
            throw new InvalidOperationException($"Cannot apply logical operator '{context.op.Text}' between different types '{leftSymbol.Type}' and '{rightSymbol.Type}'.");
        }

        switch (leftSymbol.Value)
        {
            case IQuantumType leftValue when rightSymbol.Value is IQuantumType rightValue:
                {
                    var operation
                       = context.MULTIPLY() != null ? leftValue.Addition(rightValue)
                       : context.DIVIDE() != null ? leftValue.Subtraction(rightValue)
                       : context.MODULE() != null ? leftValue.Subtraction(rightValue)
                       : throw new InvalidOperationException($"Unknown operator '{context.op.Text}'.");
                    var destinationSymbol = new AnonymousValueSymbol(operation.Destination, scopeHandler.GetCurrentScope(), context.Start.TokenIndex);
                    circuitHandler.PushOperation(operation);
                    return destinationSymbol;
                }

            case IClassicalType leftValue when rightSymbol.Value is IClassicalType rightValue:
                {
                    var result
                        = context.MULTIPLY() != null ? leftValue.Addition(rightValue)
                        : context.DIVIDE() != null ? leftValue.Subtraction(rightValue)
                        : context.MODULE() != null ? leftValue.Subtraction(rightValue)
                        : throw new InvalidOperationException($"Unknown operator '{context.op.Text}'.");
                    return new AnonymousValueSymbol(result, scopeHandler.GetCurrentScope(), context.Start.TokenIndex);
                }

            default:
                throw new InvalidOperationException($"Cannot apply operator '{context.op.Text}' to type '{leftSymbol.Type}'.");
        }
    }

    public override Symbol VisitSumOperator(qutes_parser.SumOperatorContext context)
    {
        var leftSymbol = QutesLanguageGuard.IsAssignableToType<ValueSymbol>(Visit(context.expr(0)));
        var rightSymbol = QutesLanguageGuard.IsAssignableToType<ValueSymbol>(Visit(context.expr(1)));

        if (leftSymbol.Value.GetType() != rightSymbol.Value.GetType())
        {
            throw new InvalidOperationException($"Cannot apply logical operator '{context.op.Text}' between different types '{leftSymbol.Type}' and '{rightSymbol.Type}'.");
        }

        switch (leftSymbol.Value)
        {
            case IQuantumType leftValue when rightSymbol.Value is IQuantumType rightValue:
                {
                    var operation
                       = context.ADD() != null ? leftValue.Addition(rightValue)
                       : context.SUB() != null ? leftValue.Subtraction(rightValue)
                       : throw new InvalidOperationException($"Unknown operator '{context.op.Text}'.");
                    var destinationSymbol = new AnonymousValueSymbol(operation.Destination, scopeHandler.GetCurrentScope(), context.Start.TokenIndex);
                    circuitHandler.PushOperation(operation);
                    return destinationSymbol;
                }

            case IClassicalType leftValue when rightSymbol.Value is IClassicalType rightValue:
                {
                    var result
                        = context.ADD() != null ? leftValue.Addition(rightValue)
                        : context.SUB() != null ? leftValue.Subtraction(rightValue)
                        : throw new InvalidOperationException($"Unknown operator '{context.op.Text}'.");
                    return new AnonymousValueSymbol(result, scopeHandler.GetCurrentScope(), context.Start.TokenIndex);
                }

            default:
                throw new InvalidOperationException($"Cannot apply operator '{context.op.Text}' to type '{leftSymbol.Type}'.");
        }
    }

    public override Symbol VisitShiftOperator(qutes_parser.ShiftOperatorContext context)
    {
        var leftSymbol = QutesLanguageGuard.IsAssignableToType<ValueSymbol>(Visit(context.expr(0)));
        var rightSymbol = QutesLanguageGuard.IsAssignableToType<ValueSymbol>(Visit(context.expr(1)));

        switch (leftSymbol.Value)
        {
            case IQuantumType leftValue when rightSymbol.Value is QuintType rightValue:
                {
                    var operation
                        = context.LSHIFT() != null ? leftValue.LeftShift(rightValue)
                        : context.RSHIFT() != null ? leftValue.RightShift(rightValue)
                        : throw new InvalidOperationException($"Unknown operator '{context.op.Text}'.");
                    //TODO: we are assuming that the destination is a new anonymous variable, but in this case the operation happens inplace,
                    // we should assume to know this detail? or is it ok to create this new anon var?
                    var destinationSymbol = new AnonymousValueSymbol(operation.Destination, scopeHandler.GetCurrentScope(), context.Start.TokenIndex);
                    circuitHandler.PushOperation(operation);
                    return destinationSymbol;
                }

            case IClassicalType leftValue when rightSymbol.Value is IntType rightValue:
                {
                    var result
                        = context.LSHIFT() != null ? leftValue.LeftShift(rightValue)
                        : context.RSHIFT() != null ? leftValue.RightShift(rightValue)
                        : throw new InvalidOperationException($"Unknown operator '{context.op.Text}'.");
                    return new AnonymousValueSymbol(result, scopeHandler.GetCurrentScope(), context.Start.TokenIndex);
                }

            default:
                throw new InvalidOperationException($"Cannot apply operator '{context.op.Text}' to type '{leftSymbol.Type}'.");
        }
    }

    public override Symbol VisitRelationalOperator(qutes_parser.RelationalOperatorContext context)
    {
        var leftSymbol = QutesLanguageGuard.IsAssignableToType<ValueSymbol>(Visit(context.expr(0)));
        var rightSymbol = QutesLanguageGuard.IsAssignableToType<ValueSymbol>(Visit(context.expr(1)));

        if (leftSymbol.Value.GetType() != rightSymbol.Value.GetType())
        {
            throw new InvalidOperationException($"Cannot apply operator '{context.op.Text}' between different types '{leftSymbol.Type}' and '{rightSymbol.Type}'.");
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
                        : throw new InvalidOperationException($"Unknown operator '{context.op.Text}'.");
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
                        : throw new InvalidOperationException($"Unknown operator '{context.op.Text}'.");
                    return new AnonymousValueSymbol(result, scopeHandler.GetCurrentScope(), context.Start.TokenIndex);
                }

            default:
                throw new InvalidOperationException($"Cannot apply operator '{context.op.Text}' to type '{leftSymbol.Type}'.");
        }
    }

    public override Symbol VisitEqualityOperator(qutes_parser.EqualityOperatorContext context)
    {
        var leftSymbol = QutesLanguageGuard.IsAssignableToType<ValueSymbol>(Visit(context.expr(0)));
        var rightSymbol = QutesLanguageGuard.IsAssignableToType<ValueSymbol>(Visit(context.expr(1)));

        if (leftSymbol.Value.GetType() != rightSymbol.Value.GetType())
        {
            throw new InvalidOperationException($"Cannot apply operator '{context.op.Text}' between different types '{leftSymbol.Type}' and '{rightSymbol.Type}'.");
        }

        switch (leftSymbol.Value)
        {
            case IQuantumType leftValue when rightSymbol.Value is IQuantumType rightValue:
                {
                    var operation
                        = context.EQUAL() != null ? leftValue.Equals(rightValue)
                        : context.NOT_EQUAL() != null ? leftValue.NotEquals(rightValue)
                        : throw new InvalidOperationException($"Unknown operator '{context.op.Text}'.");
                    var destinationSymbol = new AnonymousValueSymbol(operation.Destination, scopeHandler.GetCurrentScope(), context.Start.TokenIndex);
                    circuitHandler.PushOperation(operation);
                    return destinationSymbol;
                }

            case IClassicalType leftValue when rightSymbol.Value is IClassicalType rightValue:
                {
                    var result
                        = context.EQUAL() != null ? leftValue.Equals(rightValue)
                        : context.NOT_EQUAL() != null ? leftValue.NotEquals(rightValue)
                        : throw new InvalidOperationException($"Unknown operator '{context.op.Text}'.");
                    return new AnonymousValueSymbol(result, scopeHandler.GetCurrentScope(), context.Start.TokenIndex);
                }

            default:
                throw new InvalidOperationException($"Cannot apply operator '{context.op.Text}' to type '{leftSymbol.Type}'.");
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
                        : throw new InvalidOperationException($"Unknown operator '{context.op.Text}'.");
                    var destinationSymbol = new AnonymousValueSymbol(operation.Destination, scopeHandler.GetCurrentScope(), context.Start.TokenIndex);
                    circuitHandler.PushOperation(operation);
                    return destinationSymbol;
                }

            case IClassicalType leftValue when rightSymbol.Value is IClassicalType rightValue:
                {
                    var result
                        = context.AND() != null ? leftValue.And(rightValue)
                        : throw new InvalidOperationException($"Unknown operator '{context.op.Text}'.");
                    return new AnonymousValueSymbol(result, scopeHandler.GetCurrentScope(), context.Start.TokenIndex);
                }

            default:
                throw new InvalidOperationException($"Cannot apply operator '{context.op.Text}' to type '{leftSymbol.Type}'.");
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
                        : throw new InvalidOperationException($"Unknown operator '{context.op.Text}'.");
                    var destinationSymbol = new AnonymousValueSymbol(operation.Destination, scopeHandler.GetCurrentScope(), context.Start.TokenIndex);
                    circuitHandler.PushOperation(operation);
                    return destinationSymbol;
                }

            case IClassicalType leftValue when rightSymbol.Value is IClassicalType rightValue:
                {
                    var result
                        = context.OR() != null ? leftValue.Or(rightValue)
                        : throw new InvalidOperationException($"Unknown operator '{context.op.Text}'.");
                    return new AnonymousValueSymbol(result, scopeHandler.GetCurrentScope(), context.Start.TokenIndex);
                }

            default:
                throw new InvalidOperationException($"Cannot apply operator '{context.op.Text}' to type '{leftSymbol.Type}'.");
        }
    }

    public override Symbol VisitMultipleUnaryOperator(qutes_parser.MultipleUnaryOperatorContext context)
    {
        var termListSymbol = QutesLanguageGuard.IsAssignableToType<TupleSymbol>(Visit(context.termList()));
        var termListValues = QutesLanguageGuard.AreAllAssignableToType<IQuantumType>(termListSymbol.Elements.Cast<ValueSymbol>().Select(e => e.Value));
        var target = termListValues.Last();
        var controls = termListValues.Take(termListSymbol.Elements.Count() - 1);

        CircuitOperation operation
            = context.MCX() != null ? new MCX(controls, target)
            : context.MCZ() != null ? new MCZ(controls, target)
            : context.SWAP() != null ? new MultiSwap(controls, target)
            : context.HADAMARD() != null ? new MultiHadamard(termListValues)
            : context.MEASURE() != null ? new MultiMeasure(termListValues)
            : context.BARRIER() != null ? new MultiBarrier(termListValues)
            : throw new InvalidOperationException($"Unknown operator '{context.op.Text}'.");
        var destinationSymbol = new AnonymousValueSymbol(operation.Destination, scopeHandler.GetCurrentScope(), context.Start.TokenIndex);
        circuitHandler.PushOperation(operation);
        return destinationSymbol;
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
                        : context.CNOT() != null ? new CNOT(firstValue, secondValue)
                        : throw new InvalidOperationException($"Unknown operator '{context.op.Text}'.");
                    var destinationSymbol = new AnonymousValueSymbol(operation.Destination, scopeHandler.GetCurrentScope(), context.Start.TokenIndex);
                    circuitHandler.PushOperation(operation);
                    return destinationSymbol;
                }

            case IClassicalType firstValue when secondSymbol.Value is IClassicalType secondValue:
                {
                    var result
                        = context.SWAP() != null ? firstValue.Swap(secondValue)
                        : context.CNOT() != null ? ((bool)firstValue.GetValueAsObject()) == true ? firstValue.Not() : secondValue
                        : throw new InvalidOperationException($"Unknown operator '{context.op.Text}'.");
                    return new AnonymousValueSymbol(result, scopeHandler.GetCurrentScope(), context.Start.TokenIndex);
                }

            default:
                throw new InvalidOperationException($"Cannot apply operator '{context.op.Text}' to type '{firstSymbol.Type}'.");
        }
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
                        Console.WriteLine($"{targetValue.Type} '{targetSymbol.QualifiedName}': {targetValue.QubitStringList}");
                        return targetSymbol;
                    }

                    CircuitOperation operation
                        = context.HADAMARD() != null ? new Hadamard(targetValue)
                        : context.PAULIY() != null ? new PauliY(targetValue)
                        : context.PAULIZ() != null ? new PauliZ(targetValue)
                        : context.MEASURE() != null ? new Measure(targetValue)
                        : throw new InvalidOperationException($"Unknown operator '{context.op.Text}'.");
                    var destinationSymbol = new AnonymousValueSymbol(operation.Destination, scopeHandler.GetCurrentScope(), context.Start.TokenIndex);
                    circuitHandler.PushOperation(operation);
                    return destinationSymbol;
                }

            case IClassicalType targetValue:
                {
                    if (context.PRINT() != null)
                    {
                        Console.WriteLine($"{targetValue.Type} '{targetSymbol.QualifiedName}': {targetValue.GetValueAsObject()}");
                        return targetSymbol;
                    }

                    throw new InvalidOperationException($"Cannot apply operator '{context.op.Text}' to type '{targetSymbol.Type}'.");
                }
            default:
                throw new InvalidOperationException($"Cannot apply operator '{context.op.Text}' to type '{targetSymbol.Type}'.");
        }
    }

    public override Symbol VisitMultipleUnaryPhaseOperator(qutes_parser.MultipleUnaryPhaseOperatorContext context)
    {
        var rotationSymbol = QutesLanguageGuard.IsAssignableToType<ValueSymbol>(Visit(context.expr()));
        var rotationValue = QutesLanguageGuard.IsAssignableToType<FloatType>(rotationSymbol.Value);
        var termListSymbol = QutesLanguageGuard.IsAssignableToType<TupleSymbol>(Visit(context.termList()));
        var termListValues = QutesLanguageGuard.AreAllAssignableToType<IQuantumType>(termListSymbol.Elements.Cast<ValueSymbol>().Select(e => e.Value));
        var controls = termListValues.Take(termListSymbol.Elements.Count() - 1);
        var target = termListValues.Last();

        CircuitOperation operation
            = context.MCP() != null ? new MCP(controls, target, rotationValue)
            : throw new InvalidOperationException($"Unknown operator '{context.op.Text}'.");
        var destinationSymbol = new AnonymousValueSymbol(operation.Destination, scopeHandler.GetCurrentScope(), context.Start.TokenIndex);
        circuitHandler.PushOperation(operation);
        return destinationSymbol;
    }

    public override Symbol VisitGroverOperator(qutes_parser.GroverOperatorContext context)
    {
        //TODO: implement grover operator
        return base.VisitGroverOperator(context);
    }

    public override Symbol VisitFreeGroverOperator(qutes_parser.FreeGroverOperatorContext context)
    {
        //TODO: implement free grover operator
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
        var varTypeSymbol = QutesLanguageGuard.IsAssignableToType<TypeSymbol>(Visit(context.variableType()));
        var qualifiedName = QutesLanguageGuard.IsAssignableToType<QualifiedNameSymbol>(Visit(context.qualifiedName())).QualifiedName;
        var valueToAssignSymbol = context.expr() == null ? GetDefaultValueSymbolForType(varTypeSymbol) : (ValueSymbol)Visit(context.expr());

        var variableToCreateSymbol = CastValueToType(valueToAssignSymbol, varTypeSymbol);
        //TODO: could be a problem directly using the value in the valueSymbol constructor, stuff could share references and mutate each other.
        variableToCreateSymbol = new ValueSymbol(qualifiedName, variableToCreateSymbol.Value, scopeHandler.GetCurrentScope(), context.Start.TokenIndex);
        
        DeclareNewVariable(variableToCreateSymbol);

        if(variableToCreateSymbol.Value is IQuantumType quantumValue)
        {
            circuitHandler.DeclareQuantumVariable(variableToCreateSymbol.QualifiedName, quantumValue.Register);
        }

        return variableToCreateSymbol;
    }

    private static ValueSymbol CastValueToType(ValueSymbol symbolToCast, TypeSymbol targetType)
    {
        if (symbolToCast.Type == targetType)
        {
            return symbolToCast;
        }
        else if (symbolToCast.Value.TryConvertTo(targetType, out var casted))
        {
            return new AnonymousValueSymbol(casted, null!, default); //TODO: check scope and asttokenindex
        }
        throw new InvalidOperationException($"Cannot cast value of type '{symbolToCast.Type}' to '{targetType}'.");
    }

    public override Symbol VisitTermList(qutes_parser.TermListContext context)
    {
        var symbols = context.expr().Select(e => Visit(e)) ?? [];

        return new TupleSymbol(symbols, scopeHandler.GetCurrentScope(), context.Start.TokenIndex);
    }

    public override Symbol VisitVariableType(qutes_parser.VariableTypeContext context)
    {
        var type = QutesLanguageGuard.IsAssignableToType<TypeSymbol>(Visit(context.type()));

        if(context.GetText().Contains("[]"))
        {
            type = new TypeSymbol(type.Value.IsQuantum() ? QutesType.quantumArray : QutesType.classicalArray, type);
        }

        return type;
    }

    public override Symbol VisitType(qutes_parser.TypeContext context)
    {
        var type
            = context.BOOL_TYPE() != null ? QutesType.boolean
            : context.INT_TYPE() != null ? QutesType.integer
            : context.FLOAT_TYPE() != null ? QutesType.floating
            : context.STRING_TYPE() != null ? QutesType.@string
            : context.QUBIT_TYPE() != null ? QutesType.qubit
            : context.QUINT_TYPE() != null ? QutesType.quinteger
            : context.QUSTRING_TYPE() != null ? QutesType.qustring
            : context.VOID_TYPE() != null ? QutesType.@void
            : throw new InvalidOperationException($"Unknown type '{context.GetText()}'.");

        return new TypeSymbol(type);
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
        var stateVector = QubitParser.Parse(value);
        return new AnonymousValueSymbol(new QubitType(stateVector), scopeHandler.GetCurrentScope(), context.Start.TokenIndex);
    }

    public override Symbol VisitQuint(qutes_parser.QuintContext context)
    {
        var value = context.QUINT_LITERAL().GetText();
        var stateVector = QuintParser.Parse(value);
        return new AnonymousValueSymbol(new QuintType(stateVector), scopeHandler.GetCurrentScope(), context.Start.TokenIndex);
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
        var value = BoolParser.Parse(context.BOOL_LITERAL().GetText());
        return new AnonymousValueSymbol(new BoolType(value), scopeHandler.GetCurrentScope(), context.Start.TokenIndex);
    }
}