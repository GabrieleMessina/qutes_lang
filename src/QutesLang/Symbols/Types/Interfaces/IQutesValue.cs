namespace QutesLang.Symbols.Types.Interfaces;

public interface IQutesValue
{
    public abstract TypeSymbol Type { get; }
    public virtual bool TryConvertTo(TypeSymbol targetType, out IQutesValue result)
    {
        throw new NotImplementedException();
    }
}
