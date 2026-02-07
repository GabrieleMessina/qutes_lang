using System.Runtime.CompilerServices;

using QutesLang.Symbols.Types.Interfaces;

namespace QutesLang.Symbols.Types;

public class BoolValue(bool value) : ClassicalValue
{
    public override TypeSymbol Type { get; } = TypeSymbol.Bool;
    public bool Value { get; set; } = value;
    public override object GetValueAsObject() => Value;
    public override void SetValueFromObject(object value) => Value = (bool)value;
    public static BoolValue GetDefaultValue() => new(false);
    private static bool GetBoolValue(IQutesValue term, [CallerMemberName] string operationName = "")
    {
        if (term is not BoolValue boolValue)
            throw new InvalidOperationException($"Operation {operationName} cannot be applied to {term.Type} type.");
        
        return boolValue.Value;
    }
    public override QutesResult Equals(IQutesValue term) => new BoolValue(this.Value == GetBoolValue(term));
    public override QutesResult NotEquals(IQutesValue term) => new BoolValue(this.Value != GetBoolValue(term));
    public override QutesResult And(IQutesValue term) => new BoolValue(this.Value && GetBoolValue(term));
    public override QutesResult Or(IQutesValue term) => new BoolValue(this.Value || GetBoolValue(term));
    public override QutesResult Not() => new BoolValue(!this.Value);

    public override bool TryConvertTo(TypeSymbol targetType, out IQutesValue result)
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

public class IntValue(int value) : ClassicalValue
{
    public override TypeSymbol Type { get; } = TypeSymbol.Int;
    public int Value { get; set; } = value;
    public override object GetValueAsObject() => Value;
    public override void SetValueFromObject(object value) => Value = (int)value;
    public static IntValue GetDefaultValue() => new(0);
    private static int GetIntValue(IQutesValue term, [CallerMemberName] string operationName = "")
    {
        if (term is not IntValue intValue)
            throw new InvalidOperationException($"Operation {operationName} cannot be applied to {term.Type} type.");

        return intValue.Value;
    }

    public override QutesResult LeftShift(IQutesValue positions) => new IntValue(this.Value << GetIntValue(positions));
    public override QutesResult RightShift(IQutesValue positions) => new IntValue(this.Value >> GetIntValue(positions));

    public override QutesResult Addition(IQutesValue term) => new IntValue(this.Value + GetIntValue(term));
    public override QutesResult Subtraction(IQutesValue term) => new IntValue(this.Value - GetIntValue(term));
    public override QutesResult Multiply(IQutesValue term) => new IntValue(this.Value * GetIntValue(term));
    public override QutesResult Divide(IQutesValue term) => new IntValue(this.Value / GetIntValue(term));
    public override QutesResult Module(IQutesValue term) => new IntValue(this.Value % GetIntValue(term));

    public override QutesResult LowerThan(IQutesValue term) => new BoolValue(this.Value < GetIntValue(term));
    public override QutesResult LowerEqualThan(IQutesValue term) => new BoolValue(this.Value <= GetIntValue(term));
    public override QutesResult GreaterThan(IQutesValue term) => new BoolValue(this.Value > GetIntValue(term));
    public override QutesResult GreaterEqualThan(IQutesValue term) => new BoolValue(this.Value >= GetIntValue(term));
    public override QutesResult Equals(IQutesValue term) => new BoolValue(this.Value == GetIntValue(term));
    public override QutesResult NotEquals(IQutesValue term) => new BoolValue(this.Value != GetIntValue(term));

    public override QutesResult Minus() => new IntValue(-this.Value);
    public override QutesResult InplacePreIncrement() => new IntValue(++this.Value);
    public override QutesResult InplacePreDecrement() => new IntValue(--this.Value);
    public override QutesResult InplacePostIncrement() => new IntValue(this.Value++);
    public override QutesResult InplacePostDecrement() => new IntValue(this.Value--);

    public override bool TryConvertTo(TypeSymbol targetType, out IQutesValue result)
    {
        if (targetType == Type)
        {
            result = this;
            return true;
        }
        if (targetType == TypeSymbol.Quint)
        {
            result = new QuintValue(this);
            return true;
        }
        result = default!;
        return false;
    }

    public static IntValue Parse(string v)
    {
        return new IntValue(int.Parse(v));
    }
}

public class FloatValue(float value) : ClassicalValue
{
    public override TypeSymbol Type { get; } = TypeSymbol.Float;
    public float Value { get; set; } = value;
    public override object GetValueAsObject() => Value;
    public override void SetValueFromObject(object value) => Value = (float)value;
    public static FloatValue GetDefaultValue() => new(0f);
    private static float GetFloatValue(IQutesValue term, [CallerMemberName] string operationName = "")
    {
        if (term is not FloatValue floatValue)
            throw new InvalidOperationException($"Operation {operationName} cannot be applied to {term.Type} type.");
        
        return floatValue.Value;
    }

    public override QutesResult Addition(IQutesValue term) => new FloatValue(this.Value + GetFloatValue(term));
    public override QutesResult Subtraction(IQutesValue term) => new FloatValue(this.Value - GetFloatValue(term));
    public override QutesResult Multiply(IQutesValue term) => new FloatValue(this.Value * GetFloatValue(term));
    public override QutesResult Divide(IQutesValue term) => new FloatValue(this.Value / GetFloatValue(term));
    public override QutesResult Module(IQutesValue term) => new FloatValue(this.Value % GetFloatValue(term));

    public override QutesResult LowerThan(IQutesValue term) => new BoolValue(this.Value < GetFloatValue(term));
    public override QutesResult LowerEqualThan(IQutesValue term) => new BoolValue(this.Value <= GetFloatValue(term));
    public override QutesResult GreaterThan(IQutesValue term) => new BoolValue(this.Value > GetFloatValue(term));
    public override QutesResult GreaterEqualThan(IQutesValue term) => new BoolValue(this.Value >= GetFloatValue(term));
    public override QutesResult Equals(IQutesValue term) => new BoolValue(this.Value == GetFloatValue(term));
    public override QutesResult NotEquals(IQutesValue term) => new BoolValue(this.Value != GetFloatValue(term));

    public override QutesResult Minus() => new FloatValue(-this.Value);
    public override QutesResult InplacePreIncrement() => new FloatValue(++this.Value);
    public override QutesResult InplacePreDecrement() => new FloatValue(--this.Value);
    public override QutesResult InplacePostIncrement() => new FloatValue(this.Value++);
    public override QutesResult InplacePostDecrement() => new FloatValue(this.Value--);

    public override bool TryConvertTo(TypeSymbol targetType, out IQutesValue result)
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
public class StringValue(string value) : ClassicalValue
{
    public override TypeSymbol Type { get; } = TypeSymbol.String;
    public string Value { get; set; } = value;
    public override object GetValueAsObject() => Value;
    public override void SetValueFromObject(object value) => Value = (string)value;
    public static StringValue GetDefaultValue() => new("");
    private static string GetStringValue(IQutesValue term, [CallerMemberName] string operationName = "")
    {
        if (term is not StringValue stringValue)
            throw new InvalidOperationException($"Operation {operationName} cannot be applied to {term.Type} type.");
        
        return stringValue.Value;
    }

    public override QutesResult LeftShift(IQutesValue positions)
    {
        if(positions is not IntValue intValue)
            throw new InvalidOperationException($"Operation LeftShift cannot be applied to {positions.Type} type.");

        var n = intValue.Value % this.Value.Length;
        var result = this.Value[n..] + this.Value[..n].Reverse();
        return new StringValue(result);
    }

    public override QutesResult RightShift(IQutesValue positions)
    {
        if(positions is not IntValue intValue)
            throw new InvalidOperationException($"Operation RightShift cannot be applied to {positions.Type} type.");

        var n = intValue.Value % this.Value.Length;
        var result = this.Value[^n..] + this.Value[..^n];
        return new StringValue(result);
    }

    public override QutesResult Addition(IQutesValue term) => new StringValue(this.Value + GetStringValue(term));
    public override QutesResult Subtraction(IQutesValue term) => new StringValue(this.Value.Replace(GetStringValue(term), string.Empty));
    public override QutesResult LowerThan(IQutesValue term) => new BoolValue(string.Compare(this.Value, GetStringValue(term)) < 0);
    public override QutesResult LowerEqualThan(IQutesValue term) => new BoolValue(string.Compare(this.Value, GetStringValue(term)) <= 0);
    public override QutesResult GreaterThan(IQutesValue term) => new BoolValue(string.Compare(this.Value, GetStringValue(term)) > 0);
    public override QutesResult GreaterEqualThan(IQutesValue term) => new BoolValue(string.Compare(this.Value, GetStringValue(term)) >= 0);
    public override QutesResult Equals(IQutesValue term) => new BoolValue(this.Value == GetStringValue(term));
    public override QutesResult NotEquals(IQutesValue term) => new BoolValue(this.Value != GetStringValue(term));

    public override bool TryConvertTo(TypeSymbol targetType, out IQutesValue result)
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
