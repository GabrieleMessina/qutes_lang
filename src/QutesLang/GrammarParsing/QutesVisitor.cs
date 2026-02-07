using Antlr4.Runtime;
using Antlr4.Runtime.Misc;
using Antlr4.Runtime.Tree;

using Qutes.Grammar;

using QutesLang.QuantumCircuits.Operations;
using QutesLang.QuantumCircuits.Interfaces;
using QutesLang.Symbols;
using QutesLang.Symbols.Types;
using QutesLang.Symbols.Types.Interfaces;
namespace QutesLang.GrammarParsing;

public class QutesVisitor(IScopeHandler scopeHandler, ICircuitHandler circuitHandler) : qutes_parserBaseVisitor<Symbol>
{
    private readonly string QuantumSuffix = qutes_parser.DefaultVocabulary.GetLiteralName(qutes_parser.QUANTUM_SUFFIX);

    protected override bool ShouldVisitNextChild([NotNull] IRuleNode node, Symbol currentResult)
    {
        return !IsReturning();
    }
    private bool IsReturning() => handlingReturnStatement > 0 || handlingYieldStatement > 0;

    public override Symbol Visit(IParseTree tree)
    {
        try
        {
            return base.Visit(tree);
        }
        catch (Exception ex)
        {
            if (tree is ParserRuleContext context)
            {
                if (ex.Data.Contains("LocationInfoAdded"))
                {
                    throw;
                }

                var newEx = new Exception($"At {context.Start.Line}:{context.Start.Column} {ex.Message}", ex);
                newEx.Data["LocationInfoAdded"] = true;
                throw newEx;
            }

            throw;
        }
    }

    private Symbol VisitAllChildren(ParserRuleContext context)
    {
        Symbol result = default!;
        if (context.children != null)
        {
            foreach (var child in context.children.Where(c => c is not TerminalNodeImpl))
            {
                if (!ShouldVisitNextChild(context, null!)) break;
                Symbol childResult = Visit(child);
                result = AggregateResult(result, childResult); //this just return last visited node's result. Override if needed.
            }
        }
        return result;
    }

    private AnonymousValueSymbol GetDefaultValueSymbolForType(TypeSymbol varTypeSymbol, int astTokenIndex)
    {
        var defaultValue = varTypeSymbol.GetDefaultValueFromType();
        return new AnonymousValueSymbol(defaultValue, scopeHandler.GetCurrentScope(), astTokenIndex);
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
        scopeHandler.PushScope(scopeHandler.CreateScope("MainScope"));
        CheckForFunctionHoisting(context);
        var res = VisitAllChildren(context); //return value doesn't matter no one will use it.
        res = IsReturning() ? res : null!;
        //scope intentionally not popped to keep the main scope available after visiting.
        return res;
    }

    public override Symbol VisitBlockStatement(qutes_parser.BlockStatementContext context)
    {
        scopeHandler.PushScope(scopeHandler.CreateScope("BlockScope"));
        CheckForFunctionHoisting(context);
        var res = VisitAllChildren(context);
        res = IsReturning() ? res : null!;
        scopeHandler.PopScope();
        return res;
    }

    public override Symbol VisitIfStatement(qutes_parser.IfStatementContext context)
    {
        var condition = Visit(context.expr()).As<ValueSymbol>();
        var ifBody = context.statement();

        switch (condition.Value)
        {
            case IQuantumValue quantumCondition:
                HandleBranchingVisiting(ifBody, quantumCondition);
                break;
            case BoolValue boolCondition:
                if (boolCondition.Value == true) Visit(ifBody);
                break;
            default:
                throw new InvalidOperationException("If condition must be of type 'bool' or a quantum type.");
        }

        return null!;
    }

    public override Symbol VisitIfElseStatement(qutes_parser.IfElseStatementContext context)
    {
        var condition = Visit(context.expr()).As<ValueSymbol>();
        var ifBody = context.statement(0);
        var elseBody = context.statement(1);

        switch (condition.Value)
        {
            case IQuantumValue quantumCondition:
                HandleBranchingVisiting(ifBody, quantumCondition);
                HandleBranchingVisiting(elseBody, quantumCondition, false);
                break;
            case BoolValue boolCondition:
                if (boolCondition.Value == true) Visit(ifBody);
                else Visit(elseBody);
                break;
            default:
                throw new InvalidOperationException("If-Else condition must be of type 'bool' or a quantum type.");
        }

        return null!;
    }

    private void HandleBranchingVisiting(qutes_parser.StatementContext branchBody, IQuantumValue quantumCondition, bool onCondition = true)
    {
        var quantumBodyCircuit = circuitHandler.DeclareNewQuantumGate();
        using (var context = circuitHandler.SetCurrentContext(quantumBodyCircuit)) //We want operations to be pushed on the body.
        {
            Visit(branchBody); //TODO: how to handle classical ops inside quantum if body.
        }
        var controlledCircuit = quantumBodyCircuit.MakeControlledBy(quantumCondition.Register, onCondition);
        circuitHandler.DeclareNewQuantumGate(circuit: controlledCircuit);
        circuitHandler.AddDependentCircuit(quantumBodyCircuit);
        circuitHandler.AddDependentCircuit(controlledCircuit);//control then target
        circuitHandler.PushOperation(new ComposeCircuit(controlledCircuit, controlledCircuit.LocalRegisters));
    }

    public override Symbol VisitWhileStatement(qutes_parser.WhileStatementContext context)
    {
        var condition = Visit(context.expr()).As<ValueSymbol>();
        var whileBody = context.statement();

        switch (condition.Value)
        {
            case IQuantumValue:
                //TODO: quantum while loops could be implemented with repeated appended controlled circuits based on all possible combination of the qubits in the condition register.
                throw new NotImplementedException("Quantum while loops are not yet implemented.");
            case BoolValue classicalCondition:
                while (classicalCondition.Value && handlingBreakStatement == 0)
                {
                    Visit(whileBody);
                    classicalCondition = Visit(context.expr()).Contains<BoolValue>();
                }
                handlingBreakStatement--;
                break;
            default:
                throw new InvalidOperationException("While loop condition must be of type 'bool' or a quantum type.");
        }

        return null!;
    }

    public override Symbol VisitForeachStatement(qutes_parser.ForeachStatementContext context)
    {
        var array = Visit(context.expr()).Contains<ArrayValue>();
        var itemNameSymbol = Visit(context.qualifiedName(0)).As<QualifiedNameSymbol>();
        QualifiedNameSymbol? indexNameSymbol = null;
        ValueSymbol? indexSymbol = null;
        
        if (context.qualifiedName(1) != null)
        {
            indexNameSymbol = Visit(context.qualifiedName(1)).As<QualifiedNameSymbol>();
        }

        if (!array.Values.Any())
        {
            return null!;
        }

        int i = 0;
        var itemSymbol = new ValueSymbol(itemNameSymbol.QualifiedName, array.Values.ElementAt(i).Value, scopeHandler.GetCurrentScope(), context.Start.TokenIndex);
        DeclareNewVariable(itemSymbol);
        if (indexNameSymbol != null)
        {
            indexSymbol = new ValueSymbol(indexNameSymbol.QualifiedName, new IntValue(i), scopeHandler.GetCurrentScope(), context.Start.TokenIndex);
            DeclareNewVariable(indexSymbol);
        }
        for (; i < array.Values.Count() && handlingBreakStatement == 0; i++)
        {
            itemSymbol.Value = array.Values.ElementAt(i).Value; //It is ok even for quantum, this variable will just point to the qubit in the array, it's an alias.
            indexSymbol?.Value = new IntValue(i);
            Visit(context.statement());
        }
        handlingBreakStatement--;
        return null!;

        //throw new InvalidOperationException("Foreach loop can only iterate over array types."); //TODO: pass this message to contains extension methods in first line of this method.
    }

    public override Symbol VisitDoWhileStatement(qutes_parser.DoWhileStatementContext context)
    {
        var condition = Visit(context.expr()).As<ValueSymbol>();
        var whileBody = context.statement();

        switch (condition.Value)
        {
            case IQuantumValue:
                throw new NotImplementedException("Quantum while loops are not yet implemented.");
            case BoolValue:
                BoolValue classicalCondition;
                do
                {
                    Visit(whileBody);
                    classicalCondition = Visit(context.expr()).Contains<BoolValue>();
                }
                while (classicalCondition.Value && handlingBreakStatement == 0);
                handlingBreakStatement--;
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

    private void CheckForFunctionHoisting(ParserRuleContext context)
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
        var outputTypeSymbol = Visit(context.variableType()).As<TypeSymbol>();
        var qualifiedNameSymbol = Visit(context.qualifiedName()).As<QualifiedNameSymbol>();

        scopeHandler.PushScope(scopeHandler.CreateScope(qualifiedNameSymbol.QualifiedName + "Scope")); //create function scope for params declaration

        var functionBody = context.statement();
        var functionParams = context.functionDeclarationParams();
        ValueSymbol? bodyStatementReturnValue = null;
        var quantumBodyCircuit = circuitHandler.DeclareNewQuantumGate(qualifiedNameSymbol.QualifiedName);
        ICollection<ValueSymbol> functionParamsValues = [];

        if (!CompilerFlags.Current.VisitFunctionBodyAtEachCall)
        {
            using (var circuitContext = circuitHandler.SetCurrentContext(quantumBodyCircuit)) //We want operations to be pushed on the body.
            {
                functionParamsValues =
                    functionParams == null
                        ? []
                        : Visit(context.functionDeclarationParams()).Contains<TupleValue>().Values.As<ValueSymbol>().ToList();
                bodyStatementReturnValue = (ValueSymbol?)Visit(functionBody); //TODO: how to handle classical ops inside quantum body.
            }
            circuitHandler.AddDependentCircuit(quantumBodyCircuit);
            handlingReturnStatement--;
        }

        var functionScope = scopeHandler.PopScope();
        var qualifiedName = qualifiedNameSymbol.QualifiedName;
        var functionToCreateSymbol = new FunctionSymbol(qualifiedName, bodyStatementReturnValue, functionParamsValues, outputTypeSymbol, quantumBodyCircuit, functionBody, functionParams, functionScope, context.Start.TokenIndex);
        DeclareNewFunction(functionToCreateSymbol);

        return functionToCreateSymbol;
    }

    //TODO: the statement related to this could be used outside of their original context (e.g. return statement in a function could be used in a lambda inside the same function), we should find a better way to handle this instead of using these counters, maybe with a stack of contexts or something like that.
    private int handlingReturnStatement = 0;
    private int handlingYieldStatement = 0;
    private int handlingBreakStatement = 0;

    public override Symbol VisitFunctionCallExpression(qutes_parser.FunctionCallExpressionContext context)
    {
        var qualifiedName = Visit(context.qualifiedName()).As<QualifiedNameSymbol>().QualifiedName;
        var providedParamsValues =
            context.termList() == null
            ? []
            : Visit(context.termList()).Contains<TupleValue>().Values.As<ValueSymbol>().ToList();

        var functionSymbol = scopeHandler.GetCurrentScope().ResolveFunction(qualifiedName);

        IQuantumCircuit functionCircuit = functionSymbol.Gate; //we cannot re-use the same circuit (e.g. different array as input params want different gate implementation if have different count of elements.)
        if (CompilerFlags.Current.VisitFunctionBodyAtEachCall)
        {
            scopeHandler.PushScope(functionSymbol.InnerScope);
            functionCircuit = circuitHandler.DeclareNewQuantumGate(qualifiedName);
            using (var circuitContext = circuitHandler.SetCurrentContext(functionCircuit)) //We want operations to be pushed on the body.
            {
                if (!functionSymbol.InputParamTypes.Any()) //declare quantum registers only once.
                {
                    functionSymbol.InputParamTypes =
                        functionSymbol.VariableDeclaration == null
                            ? []
                            : Visit(functionSymbol.VariableDeclaration).Contains<TupleValue>().Values.As<ValueSymbol>().ToList();
                }

                //TODO: the check on input params number and type should be done here not after.
                foreach (var (param, index) in functionSymbol.InputParamTypes.Select((param, index) => (param, index)))
                {
                    param.Value = providedParamsValues[index].Value;
                }

                functionSymbol.OutputSymbol = (ValueSymbol?)Visit(functionSymbol.Body); //TODO: how to handle classical ops inside quantum body.
            }
            circuitHandler.AddDependentCircuit(functionCircuit);
            handlingReturnStatement--;
            scopeHandler.PopScope();
        }

        //check that the number of parameters match
        if (functionSymbol.InputParamTypes.Count() != providedParamsValues.Count)
        {
            throw new InvalidOperationException($"Function '{qualifiedName}' expects {functionSymbol.InputParamTypes.Count()} parameters, but {providedParamsValues.Count} were provided.");
        }

        //check that the types of the parameters match
        var functionParamTypes = functionSymbol.InputParamTypes.ToList();

        foreach (var (paramType, index) in functionParamTypes.Select((value, i) => (value.Type, i)))
        {
            var providedParamType = providedParamsValues[index].Value.Type;
            if (paramType != providedParamType)
            {
                throw new InvalidOperationException($"Function '{qualifiedName}' expects parameter of type '{paramType}', but '{providedParamType}' was provided.");
            }
        }

        circuitHandler.PushOperation(new ComposeCircuit(functionCircuit, providedParamsValues.Where(p => p.Value.Type.IsQuantum()).Select(v => ((IQuantumValue)v.Value).Register).ToList()));

        if (functionSymbol.OutputSymbol != null)
        {
            var outputSymbol = functionSymbol.OutputSymbol.As<ValueSymbol>();

            if (outputSymbol.Type != functionSymbol.OutputType)
            {
                throw new InvalidOperationException($"Function '{qualifiedName}' should return type '{functionSymbol.OutputType}', but returned type '{outputSymbol.Type}'.");
            }

            return outputSymbol;
        }
        if (functionSymbol.OutputType.Value != QutesType.@void)
        {
            throw new InvalidOperationException($"Function '{qualifiedName}' should return type '{functionSymbol.OutputType}', but no value was returned.");
        }
        return null!;
    }

    public override Symbol VisitReturnStatement(qutes_parser.ReturnStatementContext context)
    {
        ValueSymbol output;
        if (context.expr() != null)
        {
            var temp = Visit(context.expr());
            output = temp.As<ValueSymbol>();
        }
        else
        {
            output = new AnonymousValueSymbol(new VoidValue(), scopeHandler.GetCurrentScope(), context.Start.TokenIndex);
        }
        handlingReturnStatement++; //this must be done after visiting ReturnStatementContext children.
        return output;
    }

    public override Symbol VisitYieldStatement([NotNull] qutes_parser.YieldStatementContext context)
    {
        var res = Visit(context.expr()).As<ValueSymbol>();
        handlingYieldStatement++; //this must be done after visiting YieldStatementContext children.
        return res;
    }

    public override Symbol VisitBreakStatement([NotNull] qutes_parser.BreakStatementContext context)
    {
        handlingBreakStatement++;
        return null!; //TODO: is it better to return an errorSymbol?
    }

    public override Symbol VisitDeclarationStatement(qutes_parser.DeclarationStatementContext context)
    {
        return Visit(context.variableDeclaration());
    }

    public override Symbol VisitAssignmentStatement(qutes_parser.AssignmentStatementContext context)
    {
        var qualifiedName = Visit(context.expr(0)).As<ValueSymbol>().QualifiedName;
        var valueToAssignSymbol = Visit(context.expr(1)).As<ValueSymbol>();

        var variableToUpdateSymbol = scopeHandler.GetCurrentScope().ResolveVariable(qualifiedName);

        variableToUpdateSymbol.Value = CastValueToType(valueToAssignSymbol, variableToUpdateSymbol.Type).Value;

        if (variableToUpdateSymbol.Value is IQuantumValue quantumValue)
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
                Console.WriteLine(symbol);
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
        var leftValue = Visit(context.expr(0)).Contains<OperableValue>();
        var rightValue = Visit(context.expr(1)).Contains<IQutesValue>();

        return leftValue.Exp(rightValue).Submit(circuitHandler);
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
        var qualifiedName = Visit(context.qualifiedName()).As<QualifiedNameSymbol>().QualifiedName;
        var symbol = scopeHandler.GetCurrentScope().ResolveVariable(qualifiedName);
        return symbol;
    }

    public override Symbol VisitArrayExpression(qutes_parser.ArrayExpressionContext context)
    {
        var rawSymbolList = Visit(context.termList()).Contains<TupleValue>().Values.As<ValueSymbol>().ToList();
        var arrayElements = new List<ValueSymbol>();

        //expand range values into individual elements
        foreach (var element in rawSymbolList)
        {
            if (element.Value is RangeValue)
            {
                var innerArray = (ArrayValue)CastValueToType(element, TypeSymbol.Array(TypeSymbol.Int)).Value;
                arrayElements.AddRange(innerArray.Values);
            }
            else
            {
                arrayElements.AddRange(element);
            }
        }

        //ensure all elements are of the same type or can be cast to the same type
        var elementsType = arrayElements.First().Type; //TODO: we should check for the least restrictive common type.
        var castedElements = arrayElements.Select(element => CastValueToType(element, elementsType)).ToList();

        ArrayValue array = elementsType.IsQuantum()
            ? new QuantumArrayValue(castedElements, elementsType)
            : new ClassicalArrayValue(castedElements, elementsType);
        return new AnonymousValueSymbol(array, scopeHandler.GetCurrentScope(), context.Start.TokenIndex);
    }

    public override Symbol VisitArrayAccessExpression(qutes_parser.ArrayAccessExpressionContext context)
    {
        var arraySymbol = Visit(context.expr(0)).As<ValueSymbol>();
        if (arraySymbol.Value is ArrayValue array)
        {
            var indexSymbol = Visit(context.expr(1)).As<ValueSymbol>();
            switch (indexSymbol.Value)
            {
                case IntValue intValue:
                    return array.Values.ElementAt(intValue.Value);
                case QuintValue quintValue when arraySymbol.Value is QuantumArrayValue quantumArray:
                {
                    var destinationSymbol = GetDefaultValueSymbolForType(quantumArray.Type.NestedValue!, context.Start.TokenIndex);
                    circuitHandler.PushOperation(new QramAccess(quantumArray, quintValue, (IQuantumValue)destinationSymbol.Value));
                    return destinationSymbol;
                }
                case RangeValue rangeValue:
                {
                    // Slice the array using the range
                    var indices = rangeValue.Enumerate(array.Values.Count()).ToList();
                    var slicedElements = indices.Select(i => array.Values.ElementAt(i.Value)).ToList();
                    var elementsType = array.Type.NestedValue!;
                    ArrayValue slicedArray = elementsType.IsQuantum()
                        ? new QuantumArrayValue(slicedElements, elementsType)
                        : new ClassicalArrayValue(slicedElements, elementsType);
                    return new AnonymousValueSymbol(slicedArray, scopeHandler.GetCurrentScope(), context.Start.TokenIndex);
                }
                default:
                    throw new InvalidOperationException($"Array index must be of type '{TypeSymbol.Int}', '{TypeSymbol.Quint}', or '{TypeSymbol.Range}', but '{indexSymbol.Type}' was provided.");
            }
        }
        else
        {
            throw new InvalidOperationException($"Cannot access index of non-array type '{arraySymbol.Type}'.");
        }
    }

    public override Symbol VisitRangeExpression(qutes_parser.RangeExpressionContext context)
    {
        var start = Visit(context.expr(0)).Contains<IntValue>();
        var end = Visit(context.expr(1)).Contains<IntValue>();
        return new AnonymousValueSymbol(new FullyQualifiedRange(start, end), scopeHandler.GetCurrentScope(), context.Start.TokenIndex);
    }

    public override Symbol VisitRangeFromExpression(qutes_parser.RangeFromExpressionContext context)
    {
        var start = Visit(context.expr()).Contains<IntValue>();
        return new AnonymousValueSymbol(new RangeValue(start, end:null), scopeHandler.GetCurrentScope(), context.Start.TokenIndex);
    }

    public override Symbol VisitRangeToExpression(qutes_parser.RangeToExpressionContext context)
    {
        var end = Visit(context.expr()).Contains<IntValue>();
        return new AnonymousValueSymbol(new RangeValue(start: null, end), scopeHandler.GetCurrentScope(), context.Start.TokenIndex);
    }

    public override Symbol VisitRangeFullExpression(qutes_parser.RangeFullExpressionContext context)
    {
        return new AnonymousValueSymbol(new RangeValue(start: null, end: null), scopeHandler.GetCurrentScope(), context.Start.TokenIndex);
    }

    public override Symbol VisitPostfixOperator(qutes_parser.PostfixOperatorContext context)
    {
        var targetValue = Visit(context.expr()).Contains<OperableValue>();

        return context.AUTO_INCREMENT() != null ? targetValue.InplacePostIncrement().Submit(circuitHandler)
                : context.AUTO_DECREMENT() != null ? targetValue.InplacePostDecrement().Submit(circuitHandler)
                : throw new InvalidOperationException($"Unknown operator '{context.op.Text}'.");
    }

    public override Symbol VisitPrefixOperator(qutes_parser.PrefixOperatorContext context)
    {
        var targetValue = Visit(context.expr()).Contains<OperableValue>();

        return context.NOT() != null ? targetValue.Not().Submit(circuitHandler)
                : context.ADD() != null ? targetValue.Plus().Submit(circuitHandler)
                : context.SUB() != null ? targetValue.Minus().Submit(circuitHandler)
                : context.AUTO_INCREMENT() != null ? targetValue.InplacePreIncrement().Submit(circuitHandler)
                : context.AUTO_DECREMENT() != null ? targetValue.InplacePreDecrement().Submit(circuitHandler)
                : throw new InvalidOperationException($"Unknown operator '{context.op.Text}'.");
    }

    public override Symbol VisitMultiplicativeOperator(qutes_parser.MultiplicativeOperatorContext context)
    {
        var leftValue = Visit(context.expr(0)).Contains<OperableValue>();
        var rightValue = Visit(context.expr(1)).Contains<IQutesValue>();

        return context.MULTIPLY() != null ? leftValue.Multiply(rightValue).Submit(circuitHandler)
                : context.DIVIDE() != null ? leftValue.Divide(rightValue).Submit(circuitHandler)
                : context.MODULE() != null ? leftValue.Module(rightValue).Submit(circuitHandler)
                : throw new InvalidOperationException($"Unknown operator '{context.op.Text}'.");
    }

    public override Symbol VisitSumOperator(qutes_parser.SumOperatorContext context)
    {
        var leftValue = Visit(context.expr(0)).Contains<OperableValue>();
        var rightValue = Visit(context.expr(1)).Contains<IQutesValue>();

        return context.ADD() != null ? leftValue.Addition(rightValue).Submit(circuitHandler)
                : context.SUB() != null ? leftValue.Subtraction(rightValue).Submit(circuitHandler)
                : throw new InvalidOperationException($"Unknown operator '{context.op.Text}'.");
    }

    public override Symbol VisitShiftOperator(qutes_parser.ShiftOperatorContext context)
    {
        var leftValue = Visit(context.expr(0)).Contains<OperableValue>();
        var rightValue = Visit(context.expr(1)).Contains<IQutesValue>();

        return context.LSHIFT() != null ? leftValue.LeftShift(rightValue).Submit(circuitHandler)
                : context.RSHIFT() != null ? leftValue.RightShift(rightValue).Submit(circuitHandler)
                : throw new InvalidOperationException($"Unknown operator '{context.op.Text}'.");
    }

    public override Symbol VisitRelationalOperator(qutes_parser.RelationalOperatorContext context)
    {
        var leftValue = Visit(context.expr(0)).Contains<OperableValue>();
        var rightValue = Visit(context.expr(1)).Contains<IQutesValue>();

        return context.LOWER() != null ? leftValue.LowerThan(rightValue).Submit(circuitHandler)
                : context.LOWEREQUAL() != null ? leftValue.LowerEqualThan(rightValue).Submit(circuitHandler)
                : context.GREATER() != null ? leftValue.GreaterThan(rightValue).Submit(circuitHandler)
                : context.GREATEREQUAL() != null ? leftValue.GreaterEqualThan(rightValue).Submit(circuitHandler)
                : throw new InvalidOperationException($"Unknown operator '{context.op.Text}'.");
    }

    public override Symbol VisitEqualityOperator(qutes_parser.EqualityOperatorContext context)
    {
        var leftValue = Visit(context.expr(0)).Contains<OperableValue>();
        var rightValue = Visit(context.expr(1)).Contains<IQutesValue>();

        return context.EQUAL() != null ? leftValue.Equals(rightValue).Submit(circuitHandler)
                : context.NOT_EQUAL() != null ? leftValue.NotEquals(rightValue).Submit(circuitHandler)
                : throw new InvalidOperationException($"Unknown operator '{context.op.Text}'.");
    }

    public override Symbol VisitLogicAndOperator(qutes_parser.LogicAndOperatorContext context)
    {
        var leftValue = Visit(context.expr(0)).Contains<OperableValue>();
        var rightValue = Visit(context.expr(1)).Contains<IQutesValue>();

        return leftValue.And(rightValue).Submit(circuitHandler);
    }

    public override Symbol VisitLogicOrOperator(qutes_parser.LogicOrOperatorContext context)
    {
        var leftValue = Visit(context.expr(0)).Contains<OperableValue>();
        var rightValue = Visit(context.expr(1)).Contains<IQutesValue>();

        return leftValue.Or(rightValue).Submit(circuitHandler);
    }

    public override Symbol VisitMultipleUnaryOperator(qutes_parser.MultipleUnaryOperatorContext context)
    {
        var termListValues = Visit(context.termList()).Contains<TupleValue>().Of<IQuantumValue>();
        var target = termListValues.Last();
        var controls = termListValues.Take(termListValues.Count - 1);

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
        var firstValue = Visit(context.expr(0)).Contains<OperableValue>();
        var secondValue = Visit(context.expr(1)).Contains<IQutesValue>();

        return context.SWAP() != null ? firstValue.Swap(secondValue).Submit(circuitHandler)
                : context.CNOT() != null ? firstValue.CNot(secondValue).Submit(circuitHandler)
                : throw new InvalidOperationException($"Unknown operator '{context.op.Text}'.");
    }

    public override Symbol VisitUnaryOperator(qutes_parser.UnaryOperatorContext context)
    {
        var targetSymbol = Visit(context.expr()).As<ValueSymbol>();

        if (context.PRINT() != null)
        {
            Console.WriteLine(targetSymbol.ToString());
            return targetSymbol;
        }

        switch (targetSymbol.Value)
        {
            case IQuantumValue targetValue:
                {
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

            case IClassicalValue:
                {
                    throw new InvalidOperationException($"Cannot apply operator '{context.op.Text}' to type '{targetSymbol.Type}'.");
                }
            default:
                throw new InvalidOperationException($"Cannot apply operator '{context.op.Text}' to type '{targetSymbol.Type}'.");
        }
    }

    public override Symbol VisitMultipleUnaryPhaseOperator(qutes_parser.MultipleUnaryPhaseOperatorContext context)
    {
        var rotationValue = Visit(context.expr()).Contains<FloatValue>();
        var termListValues = Visit(context.termList()).Contains<TupleValue>().Of<IQuantumValue>();
        var controls = termListValues.Take(termListValues.Count - 1);
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
        var pattern = Visit(context.expr(0)).Contains<IQuantumValue>(); //TODO: handle casting from classical to quantum if needed both for pattern and array.
        var array = Visit(context.expr(1)).Contains<QuantumArrayValue>();

        var rotation = QuintValue.Superposition();
        rotation.Register.Name = VariableNameGuid.New("rotation");
        var predicateResult = QubitValue.MinusState();
        predicateResult.Register.Name = VariableNameGuid.New("grover_result");

        // Create oracle
        var predicate = circuitHandler.DeclareNewQuantumGate();
        using (var circuitContext = circuitHandler.SetCurrentContext(predicate))
        {
            circuitHandler.PushOperation(new ESM(pattern, array, rotation, predicateResult));
        }

        // Run Grover on predicate
        circuitHandler.AddDependentCircuit(predicate);
        circuitHandler.PushOperation(new Grover(pattern, array, predicate, rotation));

        // Run oracle again to check that grover found right rotation
        var finalResult = new QubitValue();
        finalResult.Register.Name = VariableNameGuid.New("esm_result");
        circuitHandler.PushOperation(new ESM(pattern, array, rotation, finalResult));

        // Measure rotation and final results
        circuitHandler.PushOperation(new Measure(rotation));
        return new AnonymousValueSymbol(finalResult, scopeHandler.GetCurrentScope(), context.Start.TokenIndex);
    }

    public override Symbol VisitFreeGroverOperator(qutes_parser.FreeGroverOperatorContext context)
    {
        //TODO: implement free grover operator
        return base.VisitFreeGroverOperator(context);
    }

    public override Symbol VisitExpr(qutes_parser.ExprContext context)
    {
        return VisitAllChildren(context); //return the specific expr child type symbol
    }

    public override Symbol VisitStatement(qutes_parser.StatementContext context)
    {
        return VisitAllChildren(context); //return the specific statement child type symbol
    }

    public override Symbol VisitFunctionDeclarationParams(qutes_parser.FunctionDeclarationParamsContext context)
    {
        var symbols = context.variableDeclaration().Select(e => Visit(e)).ToList() ?? [];
        return new AnonymousValueSymbol(new TupleValue(symbols), scopeHandler.GetCurrentScope(), context.Start.TokenIndex);
    }

    public override Symbol VisitVariableDeclaration(qutes_parser.VariableDeclarationContext context)
    {
        var varTypeSymbol = Visit(context.variableType()).As<TypeSymbol>();
        var qualifiedName = Visit(context.qualifiedName()).As<QualifiedNameSymbol>().QualifiedName;
        var valueToAssignSymbol = context.expr() == null ? GetDefaultValueSymbolForType(varTypeSymbol, context.Start.TokenIndex) : (ValueSymbol)Visit(context.expr());

        var variableToCreateSymbol = CastValueToType(valueToAssignSymbol, varTypeSymbol);
        variableToCreateSymbol = new ValueSymbol(qualifiedName, variableToCreateSymbol.Value, scopeHandler.GetCurrentScope(), context.Start.TokenIndex);

        DeclareNewVariable(variableToCreateSymbol);

        if (variableToCreateSymbol.Value is IQuantumValue quantumValue)
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
        var symbols = context.expr().Select(e => Visit(e)).ToList() ?? [];
        return new AnonymousValueSymbol(new TupleValue(symbols), scopeHandler.GetCurrentScope(), context.Start.TokenIndex);
    }

    public override Symbol VisitVariableType(qutes_parser.VariableTypeContext context)
    {
        var type = Visit(context.type()).As<TypeSymbol>();

        if (context.GetText().Contains("[]"))
        {
            type = new TypeSymbol(type.Value.IsQuantum() ? QutesType.quantumArray : QutesType.classicalArray, type);
        }

        return type;
    }

    public override Symbol VisitType(qutes_parser.TypeContext context)
    {
        return new TypeSymbol(context.GetQutesType());
    }

    public override Symbol VisitQualifiedName(qutes_parser.QualifiedNameContext context)
    {
        //this is used in variable/function usage and declaration,
        //so cannot return a Symbol taken from the symbol table by name.
        var value = string.Join('.', context.SYMBOL_LITERAL().Select(e => e.GetText()));
        return new QualifiedNameSymbol(value, scopeHandler.GetCurrentScope(), context.Start.TokenIndex);
    }

    public override Symbol VisitLiteral(qutes_parser.LiteralContext context)
    {
        return VisitAllChildren(context); //return the symbol of the specific literal children type 
    }

    public override Symbol VisitString(qutes_parser.StringContext context)
    {
        var value = Convert.ToString(context.STRING_LITERAL().GetText()[1..^1]);
        return new AnonymousValueSymbol(new StringValue(value), scopeHandler.GetCurrentScope(), context.Start.TokenIndex);
    }

    public override Symbol VisitQubit(qutes_parser.QubitContext context)
    {
        var value = context.GetText().TrimEnd(QuantumSuffix).ToString();
        var stateVector = QubitParser.Parse(value);
        return new AnonymousValueSymbol(new QubitValue(stateVector), scopeHandler.GetCurrentScope(), context.Start.TokenIndex);
    }

    public override Symbol VisitQuint(qutes_parser.QuintContext context)
    {
        var value = context.GetText().TrimEnd(QuantumSuffix).ToString();
        var stateVector = QuintParser.Parse(value);
        return new AnonymousValueSymbol(new QuintValue(stateVector), scopeHandler.GetCurrentScope(), context.Start.TokenIndex);
    }

    public override Symbol VisitQuchar(qutes_parser.QucharContext context)
    {
        var value = context.GetText().TrimEnd(QuantumSuffix).ToString();
        var stateVector = QucharParser.Parse(value);
        return new AnonymousValueSymbol(new QucharValue(stateVector), scopeHandler.GetCurrentScope(), context.Start.TokenIndex);
    }

    public override Symbol VisitQustring(qutes_parser.QustringContext context)
    {
        var value = context.GetText().TrimEnd(QuantumSuffix).ToString();
        return new AnonymousValueSymbol(new QustringValue(value), scopeHandler.GetCurrentScope(), context.Start.TokenIndex);
    }

    public override Symbol VisitFloat(qutes_parser.FloatContext context)
    {
        var value = Convert.ToSingle(context.FLOAT_LITERAL().GetText());
        return new AnonymousValueSymbol(new FloatValue(value), scopeHandler.GetCurrentScope(), context.Start.TokenIndex);
    }

    public override Symbol VisitChar(qutes_parser.CharContext context)
    {
        var value = Convert.ToChar(context.CHAR_LITERAL().GetText()[1..^1]);
        return new AnonymousValueSymbol(new CharValue(value), scopeHandler.GetCurrentScope(), context.Start.TokenIndex);
    }

    public override Symbol VisitInteger(qutes_parser.IntegerContext context)
    {
        var value = Convert.ToInt32(context.INT_LITERAL().GetText());
        return new AnonymousValueSymbol(new IntValue(value), scopeHandler.GetCurrentScope(), context.Start.TokenIndex);
    }

    public override Symbol VisitBoolean(qutes_parser.BooleanContext context)
    {
        var value = BoolParser.Parse(context.BOOL_LITERAL().GetText());
        return new AnonymousValueSymbol(new BoolValue(value), scopeHandler.GetCurrentScope(), context.Start.TokenIndex);
    }
}