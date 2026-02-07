using QutesLang.GrammarFrontend.Operations;
using QutesLang.QuantumCircuits.Interfaces;
using QutesLang.Symbols.Types.Interfaces;

namespace QutesLang.Symbols.Types;

public class QutesResult
{
    public IQutesValue? StaticValue { get; } = null;
    public CircuitOperation? CircuitOperation { get; } = null;

    public QutesResult(IQutesValue staticValue)
    {
        StaticValue = staticValue;
    }

    public QutesResult(CircuitOperation circuitOperation)
    {
        CircuitOperation = circuitOperation;
    }

    public AnonymousValueSymbol Submit(ICircuitHandler circuitHandler)
    {
        PushOperation(circuitHandler);
        return GetSymbol();
    }

    private QutesResult PushOperation(ICircuitHandler circuitHandler)
    {
        if (CircuitOperation is not null)
        {
            circuitHandler.PushOperation(CircuitOperation);
        }
        return this;
    }

    private AnonymousValueSymbol GetSymbol()
    {
        if (StaticValue is not null)
            return AnonymousValueSymbol.Default(StaticValue);
        if (CircuitOperation is not null)
            return AnonymousValueSymbol.Default(CircuitOperation.Destination);
        throw new InvalidOperationException("QutesResult must have either a static value or a circuit operation.");
    }

    public static implicit operator QutesResult(OperableValue value)
    {
        return new QutesResult(value);
    }

    public static implicit operator QutesResult(ArrayValue value)
    {
        return new QutesResult(value);
    }

    public static implicit operator QutesResult(CircuitOperation operation)
    {
        return new QutesResult(operation);
    }
}
