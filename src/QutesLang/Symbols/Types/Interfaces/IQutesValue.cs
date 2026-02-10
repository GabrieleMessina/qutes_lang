using System.Diagnostics.CodeAnalysis;

namespace QutesLang.Symbols.Types.Interfaces;

public interface IQutesValue
{
    public abstract TypeSymbol Type { get; }
    public bool TryConvertTo(TypeSymbol targetType, [MaybeNullWhen(false)] out IQutesValue result);
    public bool TryConvertTo<TargetType>([MaybeNullWhen(false)] out TargetType result) where TargetType : class, IQutesValue
    {
        var success = TryConvertTo(TypeSymbol.FromType(typeof(TargetType)), out var value);
        result = value as TargetType;
        return success;
    }
    public Dictionary<string, FunctionValue> Functions { get; }
}