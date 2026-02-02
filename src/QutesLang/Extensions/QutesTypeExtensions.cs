using QutesLang.Symbols;
using QutesLang.Symbols.Types;

namespace QutesLang.Extensions;

public static class QutesTypeExtensions
{
    public static bool IsQuantum(this QutesType type)
    {
        return type == QutesType.qubit
            || type == QutesType.quinteger
            || type == QutesType.qustring
            || type == QutesType.quantumArray;
    }

    public static bool IsClassical(this QutesType type)
    {
        return !type.IsQuantum();
    }

    public static bool IsQuantum(this TypeSymbol type)
    {
        //This also handle the Array case,
        //in that case we still get Classical or Quantum Array Type as Value,
        //so we don't need to check NestedValue here.
        return type.Value.IsQuantum();
    }

    public static bool IsClassical(this TypeSymbol type)
    {
        return !type.IsQuantum();
    }
}
