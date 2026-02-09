using QutesLang.Symbols.Types.Interfaces;

namespace QutesLang.Symbols.Types;

/// <summary>
/// Represents a class value.
/// </summary>
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
    public bool TryConvertTo(TypeSymbol targetType, out IQutesValue result)
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

/// <summary>
/// Represents a void value.
/// </summary>
public class VoidValue() : IQutesValue
{
    public TypeSymbol Type { get; } = TypeSymbol.Void;
    public static VoidValue GetDefaultValue() => new();
    public bool TryConvertTo(TypeSymbol targetType, out IQutesValue result)
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

/// <summary>
/// Represents a range value with optional start and end bounds.
/// Used for slicing arrays and iterating in foreach loops.
/// </summary>
/// <param name="start">The start index (inclusive), or null for "from beginning".</param>
/// <param name="end">The end index (exclusive), or null for "to end".</param>\
/// <param name="step">The step size for enumeration, default is 1.</param>
public class RangeValue(IntValue? start, IntValue? end, IntValue? step = null) : IQutesValue
{
    public IntValue? Start { get; } = start;
    public IntValue? End { get; } = end;
    public IntValue Step { get; } = step ?? new(1);
    public TypeSymbol Type { get; } = TypeSymbol.Range;

    public static RangeValue GetDefaultValue() => new(null, null);

    public static RangeValue Parse(string input)
    {
        var parts = input.Split("..");
        var startString = string.IsNullOrEmpty(parts[0]) ? null : parts[0];
        var endString = string.IsNullOrEmpty(parts[1]) ? null : parts[1];
        string? stepString = null;

        if(parts.Length > 3) throw new FormatException($"Invalid range format: '{input}'");

        if (endString?.Contains(':') ?? false)
        {
            var stepParts = endString.Split(':');
            endString = stepParts[0];
            stepString = stepParts.Length == 1 ? null : stepParts[1];
        }

        IntValue? start = string.IsNullOrWhiteSpace(startString) ? null : IntValue.Parse(startString);
        IntValue? end = string.IsNullOrWhiteSpace(endString) ? null : IntValue.Parse(endString);
        IntValue? step = string.IsNullOrWhiteSpace(stepString) ? null : IntValue.Parse(stepString);
        return new RangeValue(start, end, step);
    }

    /// <summary>
    /// Enumerates the indices represented by this range, given the length of a collection.
    /// </summary>
    /// <param name="length">The length of the collection being accessed.</param>
    /// <returns>An enumerable of indices.</returns>
    public IEnumerable<IntValue> Enumerate(int length)
    {
        var actualStart = Start?.Value ?? 0;
        var actualEnd = End?.Value ?? length;
        for (var i = actualStart; i < actualEnd; i+=Step.Value)
            yield return new IntValue(i);
    }

    public bool TryConvertTo(TypeSymbol targetType, out IQutesValue result)
    {
        if (Type == targetType)
        {
            result = this;
            return true;
        }
        if (targetType == TypeSymbol.Quint)
        {
            result = new QuintValue(new FullyQualifiedRangeValue(this));
            return true;
        }
        if (targetType == TypeSymbol.Array(TypeSymbol.Quint))
        {
            result = new QuantumArrayValue(Enumerate(End?.Value ?? 0).Select(intValue => AnonymousValueSymbol.Default(new QuintValue(intValue))).ToList(), TypeSymbol.Quint);
            return true;
        }
        if (targetType == TypeSymbol.Array(TypeSymbol.Int))
        {
            result = new ClassicalArrayValue(Enumerate(End?.Value ?? 0).Select(intValue => AnonymousValueSymbol.Default(intValue)).ToList(), TypeSymbol.Int);
            return true;
        }
        result = default!;
        return false;
    }

    public override string ToString() => $"{Start?.ToString() ?? ""}..{End?.ToString() ?? ""}:{Step}";
}

/// <summary>
/// Represents a range value with fully specified start and end bounds.
/// </summary>
public class FullyQualifiedRangeValue : RangeValue
{
    public new IntValue Start => base.Start!;
    public new IntValue End => base.End!;

    public new static FullyQualifiedRangeValue GetDefaultValue() => new(IntValue.GetDefaultValue(), IntValue.GetDefaultValue());
    public new static FullyQualifiedRangeValue Parse(string input)
    {
        RangeValue range = RangeValue.Parse(input);
        if(range.Start == null || range.End == null)
        {
            throw new FormatException($"Invalid full qualified range format: '{input}'");
        }
        return new FullyQualifiedRangeValue(range);
    }

    /// <summary>
    /// Constructs a FullyQualifiedRange from a RangeValue, ensuring both bounds are defined.
    /// </summary>
    /// <param name="range">The RangeValue to convert.</param>
    public FullyQualifiedRangeValue(RangeValue range) : base(range.Start, range.End, range.Step)
    {
        if(range.Start == null || range.End == null)
        {
            throw new ArgumentException("RangeValue must have both start and end defined to convert to FullyQualifiedRange.");
        }
    }

    /// <summary>
    /// Represents a range value with fully specified start and end bounds.
    /// </summary>
    /// <param name="start">The start index (inclusive).</param>
    /// <param name="end">The end index (exclusive).</param>
    public FullyQualifiedRangeValue(IntValue start, IntValue end, IntValue? step = null) : base(start, end, step)
    {
    }
    
    /// <summary>
    /// Enumerates the indices represented by this range.
    /// </summary>
    /// <returns>An enumerable of indices.</returns>
    public IEnumerable<IntValue> Enumerate()
    {
        return base.Enumerate(End.Value);
    }
}