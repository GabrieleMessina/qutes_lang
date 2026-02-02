namespace QutesLang.Symbols.Types;

public class ClassValue : IQutesValue
{
    public virtual TypeSymbol Type { get; } = TypeSymbol.Class;
    public virtual bool TryConvertTo(TypeSymbol targetType, out IQutesValue result)
    {
        throw new NotImplementedException();
    }
}


/// <summary>
/// Represents a tuple value containing a sequence of symbols with no check on symbol types.
/// </summary>
/// <param name="values">The collection of symbols that make up the elements of the tuple.</param>
public class TupleValue(IEnumerable<Symbol> values) : IQutesValue
{
    public IEnumerable<Symbol> Values { get; } = values;
    public TypeSymbol Type { get; } = new(QutesType.tuple);
    public virtual bool TryConvertTo(TypeSymbol targetType, out IQutesValue result)
    {
        if (Type == targetType)
        {
            result = this;
            return true;
        }
        result = default!;
        return false;
    }
}

public class VoidValue() : IQutesValue
{
    public virtual TypeSymbol Type { get; } = TypeSymbol.Void;
    public static VoidValue GetDefaultValue() => new();
    public virtual bool TryConvertTo(TypeSymbol targetType, out IQutesValue result)
    {
        if (targetType == Type)
        {
            result = this;
            return true;
        }
        result = default!;
        return false;
    }
}
