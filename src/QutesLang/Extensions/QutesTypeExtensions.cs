using Qutes.Grammar;
using QutesLang.Symbols;
using QutesLang.Symbols.Types;
using QutesLang.Symbols.Types.Interfaces;

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

    public static QutesType GetQutesType(this qutes_parser.TypeContext context)
    {
        return context.BOOL_TYPE() != null ? QutesType.boolean
            : context.INT_TYPE() != null ? QutesType.integer
            : context.CHAR_TYPE() != null ? QutesType.character
            : context.FLOAT_TYPE() != null ? QutesType.floating
            : context.STRING_TYPE() != null ? QutesType.@string
            : context.QUBIT_TYPE() != null ? QutesType.qubit
            : context.QUINT_TYPE() != null ? QutesType.quinteger
            : context.QUCHAR_TYPE() != null ? QutesType.qucharacter
            : context.QUSTRING_TYPE() != null ? QutesType.qustring
            : context.VOID_TYPE() != null ? QutesType.@void
            : context.RANGE_TYPE() != null ? QutesType.range
            : context.FUNCTION_TYPE() != null ? QutesType.function
            : throw new InvalidOperationException($"Unknown type '{context.GetText()}'.");
    }

    public static IQutesValue GetDefaultValueFromType(this TypeSymbol type)
    {
        return type.Value switch
        {
            QutesType.boolean => BoolValue.GetDefaultValue(),
            QutesType.integer => IntValue.GetDefaultValue(),
            QutesType.character => CharValue.GetDefaultValue(),
            QutesType.floating => FloatValue.GetDefaultValue(),
            QutesType.@string => StringValue.GetDefaultValue(),
            QutesType.qubit => QubitValue.GetDefaultValue(),
            QutesType.quinteger => QuintValue.GetDefaultValue(),
            QutesType.qucharacter => QucharValue.GetDefaultValue(),
            QutesType.qustring => QustringValue.GetDefaultValue(),
            QutesType.classicalArray => ClassicalArrayValue.GetDefaultValue(type.NestedValue!),
            QutesType.quantumArray => QuantumArrayValue.GetDefaultValue(type.NestedValue!),
            QutesType.@void => VoidValue.GetDefaultValue(),
            QutesType.range => RangeValue.GetDefaultValue(),
            _ => throw new InvalidOperationException($"Cannot get default value for type '{type}'."),
        };
    }

    public static IQutesValue GetValueFromType(this TypeSymbol type, object? value)
    {
        if (value == null)
        {
            return type.GetDefaultValueFromType();
        }
        return type.Value switch
        {
            QutesType.boolean => QutesConvert.ToBoolValue(value),
            QutesType.integer => QutesConvert.ToIntValue(value),
            QutesType.character => QutesConvert.ToCharValue(value),
            QutesType.floating => QutesConvert.ToFloatValue(value),
            QutesType.@string => QutesConvert.ToStringValue(value),
            QutesType.qubit => QutesConvert.ToQubitValue(value),
            QutesType.quinteger => QutesConvert.ToQuintValue(value),
            QutesType.qucharacter => QutesConvert.ToQucharValue(value),
            QutesType.qustring => QutesConvert.ToQustringValue(value),
            QutesType.classicalArray => new ClassicalArrayValue((IEnumerable<ValueSymbol>)value, type.NestedValue!),
            QutesType.quantumArray => new QuantumArrayValue((IEnumerable<ValueSymbol>)value, type.NestedValue!),
            _ => throw new InvalidOperationException($"Cannot get default value for type '{type}'."),
        };
    }
}
