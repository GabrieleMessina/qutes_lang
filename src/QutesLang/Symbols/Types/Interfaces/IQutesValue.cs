namespace QutesLang.Symbols.Types.Interfaces;

public interface IQutesValue
{
    public abstract TypeSymbol Type { get; }
    public bool TryConvertTo(TypeSymbol targetType, out IQutesValue result);
}
