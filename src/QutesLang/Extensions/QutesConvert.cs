using QutesLang.Symbols.Types;

namespace QutesLang.Extensions;

public static class QutesConvert
{
    public static BoolValue ToBoolValue(object value)
    {
        return value switch
        {
            bool v => new BoolValue(v),
            BoolValue v => v,
            _ => throw new InvalidCastException($"Cannot convert value of type '{value.GetType()}' to {nameof(BoolValue)}.")
        };
    }

    public static IntValue ToIntValue(object value)
    {
        return value switch
        {
            int v => new IntValue(v),
            IntValue v => v,
            _ => throw new InvalidCastException($"Cannot convert value of type '{value.GetType()}' to {nameof(IntValue)}.")
        };
    }

    public static CharValue ToCharValue(object value)
    {
        return value switch
        {
            char v => new CharValue(v),
            CharValue v => v,
            _ => throw new InvalidCastException($"Cannot convert value of type '{value.GetType()}' to {nameof(CharValue)}.")
        };
    }

    public static FloatValue ToFloatValue(object value)
    {
        return value switch
        {
            float v => new FloatValue(v),
            FloatValue v => v,
            _ => throw new InvalidCastException($"Cannot convert value of type '{value.GetType()}' to {nameof(FloatValue)}.")
        };
    }

    public static StringValue ToStringValue(object value)
    {
        return value switch
        {
            string v => new StringValue(v),
            StringValue v => v,
            _ => throw new InvalidCastException($"Cannot convert value of type '{value.GetType()}' to {nameof(StringValue)}.")
        };
    }

    public static QubitValue ToQubitValue(object value)
    {
        return value switch
        {
            bool v => new QubitValue(v),
            QuintValue v => new QubitValue(v),
            QubitValue v => v,
            _ => throw new InvalidCastException($"Cannot convert value of type '{value.GetType()}' to {nameof(QubitValue)}.")
        };
    }

    public static QuintValue ToQuintValue(object value)
    {
        return value switch
        {
            int v => new QuintValue(v),
            IntValue v => new QuintValue(v),
            QubitValue v => new QuintValue(v),
            QuintValue v => v,
            _ => throw new InvalidCastException($"Cannot convert value of type '{value.GetType()}' to {nameof(QuintValue)}.")
        };
    }

    public static QucharValue ToQucharValue(object value)
    {
        return value switch
        {
            char v => new QucharValue(v),
            QuintValue v => new QucharValue(v),
            CharValue v => new QucharValue(new QuintValue(v.Value)),
            //QucharValue v => v, //quchar is quint, so this case is covered above
            _ => throw new InvalidCastException($"Cannot convert value of type '{value.GetType()}' to {nameof(QucharValue)}.")
        };
    }

    public static QustringValue ToQustringValue(object value)
    {
        return value switch
        {
            string v => new QustringValue(v),
            StringValue v => new QustringValue(v.Value),
            QustringValue v => v,
            _ => throw new InvalidCastException($"Cannot convert value of type '{value.GetType()}' to {nameof(QustringValue)}.")
        };
    }
}
