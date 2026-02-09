namespace QutesLang.Symbols.Types.Interfaces;

public interface IQutesValue
{
    public abstract TypeSymbol Type { get; }
    public bool TryConvertTo(TypeSymbol targetType, out IQutesValue result);
    public bool TryConvertTo<TargetType>(out TargetType result) where TargetType : IQutesValue
    {
        var success = TryConvertTo(TypeSymbol.FromType(typeof(TargetType)), out var value);
        result = (TargetType)value;
        return success;
    }
}
