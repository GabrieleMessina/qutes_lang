using QutesLang.GrammarFrontend;

namespace QutesLang.Symbols.Types;

public enum QutesType
{
    boolean,
    integer,
    character,
    floating,
    @string,
    qubit,
    quinteger,
    qucharacter,
    qustring,
    classicalArray,
    quantumArray,
    tuple,
    @class,
    @void,
}
public interface IQutesValue
{
    public abstract TypeSymbol Type { get; }
    public virtual bool TryConvertTo(TypeSymbol targetType, out IQutesValue result)
    {
        throw new NotImplementedException();
    }
}

public abstract class ClassicalScalarValue : IClassicalValue
{
    public abstract TypeSymbol Type { get; }

    public abstract object GetValueAsObject();
    public abstract void SetValueFromObject(object value);

    public override string ToString()
    {
        return $"{GetValueAsObject()}";
    }
}
public abstract class QuantumScalarValue : IQuantumValue
{
    public abstract int Size { get; }
    public abstract QuantumRegister Register { get; protected set; }
    public abstract TypeSymbol Type { get; }
    public virtual CircuitOperation Minus() => throw new InvalidOperationException($"Operator {nameof(Minus)} cannot be applied to {this.Type}.");

    //TODO: implement all operations as virtual.
    public override string ToString()
    {
        return $"({Type}) {Register}";
    }
}

public abstract class ArrayValue : IQutesValue
{
    public abstract IEnumerable<ValueSymbol> Values { get; protected set; }
    public abstract TypeSymbol Type { get; }

    public virtual bool TryConvertTo(TypeSymbol targetType, out IQutesValue result)
    {
        if (Type == targetType)
        {
            result = this;
            return true;
        }
        else
        {
            var newArray = CastAllElementsToType(targetType.NestedValue!);
            result = newArray;
            return true;
        }
    }

    private ArrayValue CastAllElementsToType(TypeSymbol targetType)
    {
        var castedValues = new List<ValueSymbol>();
        foreach (var symbol in Values)
        {
            if (symbol.Value.TryConvertTo(targetType, out var castedValue))
            {
                castedValues.Add(new AnonymousValueSymbol(castedValue, null!, default)); //TODO: check scope and astTokenIndex how to handle here. And if really necessay in general.
            }
            else
            {
                throw new InvalidCastException($"Cannot cast value of type {symbol.Type} to {targetType}");
            }
        }

        if (targetType.IsQuantum())
        {
            return new QuantumArrayValue(castedValues);

        }
        else
        {
            return new ClassicalArrayValue(castedValues);
        }
    }
}