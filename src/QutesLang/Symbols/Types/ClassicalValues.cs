using System.Runtime.CompilerServices;

using QutesLang.Symbols.Types.Interfaces;

namespace QutesLang.Symbols.Types;

public class BoolValue(bool value) : ClassicalScalarValue
{
    public override TypeSymbol Type { get; } = TypeSymbol.Bool;
    public bool Value { get; set; } = value;
    public override object GetValueAsObject() => Value;
    public override void SetValueFromObject(object value) => Value = (bool)value;
    public static BoolValue GetDefaultValue() => new(false);
    private static bool GetBoolValue(IClassicalValue term, [CallerMemberName] string operationName = "")
    {
        if (term is BoolValue boolType)
        {
            return boolType.Value;
        }
        throw new InvalidOperationException($"Operation {operationName} cannot be applied to {term.Type} type.");
    }
    public override BoolValue Equals(IClassicalValue term) => new(this.Value == GetBoolValue(term));
    public override BoolValue NotEquals(IClassicalValue term) => new(this.Value != GetBoolValue(term));

    public override BoolValue And(IClassicalValue term) => new(this.Value && GetBoolValue(term));
    public override BoolValue Or(IClassicalValue term) => new(this.Value || GetBoolValue(term));

    public override BoolValue Not() => new(!this.Value);

    public virtual bool TryConvertTo(TypeSymbol targetType, out IQutesValue result)
    {
        if (targetType == Type)
        {
            result = this;
            return true;
        }
        if (targetType == TypeSymbol.Int)
        {
            result = new IntValue(this.Value ? 1 : 0);
            return true;
        }
        if (targetType == TypeSymbol.Qubit)
        {
            result = new QubitValue(this.Value);
            return true;
        }
        result = default!;
        return false;
    }

    public static explicit operator IntValue(BoolValue v) => new(v.Value ? 1 : 0);
}

public class CharValue(char value) : IntValue(value)
{
    public override TypeSymbol Type => TypeSymbol.Char;

    public override bool TryConvertTo(TypeSymbol targetType, out IQutesValue result)
    {
        if (targetType == Type)
        {
            result = this;
            return true;
        }
        if (targetType == TypeSymbol.Quchar)
        {
            result = new QucharValue(Convert.ToChar(this.Value));
            return true;
        }
        result = default!;
        return false;
    }
}

public class IntValue(int value) : ClassicalScalarValue
{
    public override TypeSymbol Type { get; } = TypeSymbol.Int;
    public int Value { get; set; } = value;
    public override object GetValueAsObject() => Value;
    public override void SetValueFromObject(object value) => Value = (int)value;
    public static IntValue GetDefaultValue() => new(0);
    private static int GetIntValue(IClassicalValue term) => ((IntValue)term).Value;

    public override IQutesValue LeftShift(IntValue positions) => new IntValue(this.Value << GetIntValue(positions));
    public override IQutesValue RightShift(IntValue positions) => new IntValue(this.Value >> GetIntValue(positions));

    public override IQutesValue Addition(IClassicalValue term) => new IntValue(this.Value + GetIntValue(term));
    public override IQutesValue Subtraction(IClassicalValue term) => new IntValue(this.Value - GetIntValue(term));
    public override IQutesValue Multiply(IClassicalValue term) => new IntValue(this.Value * GetIntValue(term));
    public override IQutesValue Divide(IClassicalValue term) => new IntValue(this.Value / GetIntValue(term));
    public override IQutesValue Module(IClassicalValue term) => new IntValue(this.Value % GetIntValue(term));

    public override BoolValue LowerThan(IClassicalValue term) => new(this.Value < GetIntValue(term));
    public override BoolValue LowerEqualThan(IClassicalValue term) => new(this.Value <= GetIntValue(term));
    public override BoolValue GreaterThan(IClassicalValue term) => new(this.Value > GetIntValue(term));
    public override BoolValue GreaterEqualThan(IClassicalValue term) => new(this.Value >= GetIntValue(term));
    public override BoolValue Equals(IClassicalValue term) => new(this.Value == GetIntValue(term));
    public override BoolValue NotEquals(IClassicalValue term) => new(this.Value != GetIntValue(term));

    public override IQutesValue Minus() => new IntValue(-this.Value);
    public override IQutesValue InplacePreIncrement() => new IntValue(++this.Value);
    public override IQutesValue InplacePreDecrement() => new IntValue(--this.Value);
    public override IQutesValue InplacePostIncrement() => new IntValue(this.Value++);
    public override IQutesValue InplacePostDecrement() => new IntValue(this.Value--);

    public virtual bool TryConvertTo(TypeSymbol targetType, out IQutesValue result)
    {
        if (targetType == Type)
        {
            result = this;
            return true;
        }
        if (targetType == TypeSymbol.Quint)
        {
            result = new QuintValue(this.Value);
            return true;
        }
        result = default!;
        return false;
    }
}

public class FloatValue(float value) : ClassicalScalarValue
{
    public override TypeSymbol Type { get; } = TypeSymbol.Float;
    public float Value { get; set; } = value;
    public override object GetValueAsObject() => Value;
    public override void SetValueFromObject(object value) => Value = (float)value;
    public static FloatValue GetDefaultValue() => new(0f);
    private static float GetFloatValue(IClassicalValue term, [CallerMemberName] string operationName = "")
    {
        if (term is FloatValue floatType)
        {
            return floatType.Value;
        }
        throw new InvalidOperationException($"Operation {operationName} cannot be applied to {term.Type} type.");
    }

    public override IQutesValue Addition(IClassicalValue term) => new FloatValue(this.Value + GetFloatValue(term));
    public override IQutesValue Subtraction(IClassicalValue term) => new FloatValue(this.Value - GetFloatValue(term));
    public override IQutesValue Multiply(IClassicalValue term) => new FloatValue(this.Value * GetFloatValue(term));
    public override IQutesValue Divide(IClassicalValue term) => new FloatValue(this.Value / GetFloatValue(term));
    public override IQutesValue Module(IClassicalValue term) => new FloatValue(this.Value % GetFloatValue(term));

    public override BoolValue LowerThan(IClassicalValue term) => new(this.Value < GetFloatValue(term));
    public override BoolValue LowerEqualThan(IClassicalValue term) => new(this.Value <= GetFloatValue(term));
    public override BoolValue GreaterThan(IClassicalValue term) => new(this.Value > GetFloatValue(term));
    public override BoolValue GreaterEqualThan(IClassicalValue term) => new(this.Value >= GetFloatValue(term));
    public override BoolValue Equals(IClassicalValue term) => new(this.Value == GetFloatValue(term));
    public override BoolValue NotEquals(IClassicalValue term) => new(this.Value != GetFloatValue(term));

    public override IQutesValue Minus() => new FloatValue(-this.Value);
    public override IQutesValue InplacePreIncrement() => new FloatValue(++this.Value);
    public override IQutesValue InplacePreDecrement() => new FloatValue(--this.Value);
    public override IQutesValue InplacePostIncrement() => new FloatValue(this.Value++);
    public override IQutesValue InplacePostDecrement() => new FloatValue(this.Value--);

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

//TODO: Qustring is an array type but string is not, so we can't access string with array access notation.
public class StringValue(string value) : ClassicalScalarValue
{
    public override TypeSymbol Type { get; } = TypeSymbol.String;
    public string Value { get; set; } = value;
    public override object GetValueAsObject() => Value;
    public override void SetValueFromObject(object value) => Value = (string)value;
    public static StringValue GetDefaultValue() => new("");
    private static string GetStringValue(IClassicalValue term, [CallerMemberName] string operationName = "")
    {
        if (term is StringValue stringType)
        {
            return stringType.Value;
        }
        throw new InvalidOperationException($"Operation {operationName} cannot be applied to {term.Type} type.");
    }

    public override IQutesValue LeftShift(IntValue positions)
    {
        var n = positions.Value % this.Value.Length;
        var result = this.Value[n..] + this.Value[..n].Reverse();
        return new StringValue(result);
    }

    public override IQutesValue RightShift(IntValue positions)
    {
        var n = positions.Value % this.Value.Length;
        var result = this.Value[^n..] + this.Value[..^n];
        return new StringValue(result);
    }

    public override IQutesValue Addition(IClassicalValue term) => new StringValue(this.Value + GetStringValue(term));
    public override IQutesValue Subtraction(IClassicalValue term) => new StringValue(this.Value.Replace(GetStringValue(term), string.Empty));
    public override BoolValue LowerThan(IClassicalValue term) => new(string.Compare(this.Value, GetStringValue(term)) < 0);
    public override BoolValue LowerEqualThan(IClassicalValue term) => new(string.Compare(this.Value, GetStringValue(term)) <= 0);
    public override BoolValue GreaterThan(IClassicalValue term) => new(string.Compare(this.Value, GetStringValue(term)) > 0);
    public override BoolValue GreaterEqualThan(IClassicalValue term) => new(string.Compare(this.Value, GetStringValue(term)) >= 0);
    public override BoolValue Equals(IClassicalValue term) => new(this.Value == GetStringValue(term));
    public override BoolValue NotEquals(IClassicalValue term) => new(this.Value != GetStringValue(term));

    public virtual bool TryConvertTo(TypeSymbol targetType, out IQutesValue result)
    {
        if (targetType == Type)
        {
            result = this;
            return true;
        }
        if (targetType == TypeSymbol.Qustring)
        {
            result = new QustringValue(this.Value);
            return true;
        }
        result = default!;
        return false;
    }
}
