using System.Runtime.CompilerServices;

using QutesLang.GrammarFrontend;

namespace QutesLang.Symbols.Types;

//todo: rename al type suffix to value?

public class ClassType(string qualifiedClassName) : IQutesType
{
}


public class BoolType(bool value) : IClassicalType
{
    public bool Value { get; set; } = value;
    public object GetValueAsObject() => Value;
    public void SetValueFromObject(object value) => Value = (bool)value;
    public static BoolType GetDefaultValue() => new(false);
    private static bool GetBoolValue(IClassicalType term, [CallerMemberName] string operationName = "")
    {
        if (term is BoolType boolType)
        {
            return boolType.Value;
        }
        throw new InvalidOperationException($"Operation {operationName} cannot be applied to {term.GetType().Name} type.");
    }
    public BoolType Equals(IClassicalType term) => new (this.Value == GetBoolValue(term));
    public BoolType NotEquals(IClassicalType term) => new (this.Value != GetBoolValue(term));

    public BoolType And(IClassicalType term) => new (this.Value && GetBoolValue(term));
    public BoolType Or(IClassicalType term) => new (this.Value || GetBoolValue(term));

    public BoolType Not() => new (!this.Value);
}

public class IntType(int value) : IClassicalType
{
    public int Value { get; set; } = value;
    public object GetValueAsObject() => Value;
    public void SetValueFromObject(object value) => Value = (int)value;
    public static IntType GetDefaultValue() => new(0);
    private static int GetIntValue(IClassicalType term) => ((IntType)term).Value;

    public IQutesType LeftShift(IntType positions) => new IntType(this.Value << GetIntValue(positions));
    public IQutesType RightShift(IntType positions) => new IntType(this.Value >> GetIntValue(positions));

    public IQutesType Addition(IClassicalType term) => new IntType(this.Value + GetIntValue(term));
    public IQutesType Subtraction(IClassicalType term) => new IntType(this.Value - GetIntValue(term));
    public IQutesType Multiply(IClassicalType term) => new IntType(this.Value * GetIntValue(term));
    public IQutesType Divide(IClassicalType term) => new IntType(this.Value / GetIntValue(term));
    public IQutesType Module(IClassicalType term) => new IntType(this.Value % GetIntValue(term));

    public BoolType LowerThan(IClassicalType term) => new(this.Value < GetIntValue(term));
    public BoolType LowerEqualThan(IClassicalType term) => new(this.Value <= GetIntValue(term));
    public BoolType GreaterThan(IClassicalType term) => new(this.Value > GetIntValue(term));
    public BoolType GreaterEqualThan(IClassicalType term) => new(this.Value >= GetIntValue(term));
    public BoolType Equals(IClassicalType term) => new(this.Value == GetIntValue(term));
    public BoolType NotEquals(IClassicalType term) => new(this.Value != GetIntValue(term));

    public IQutesType Minus() => new IntType(-this.Value);
    public IQutesType InplacePreIncrement() => new IntType(++this.Value);
    public IQutesType InplacePreDecrement() => new IntType(--this.Value);
    public IQutesType InplacePostIncrement() => new IntType(this.Value++);
    public IQutesType InplacePostDecrement() => new IntType(this.Value--);
}

public class FloatType(float value) : IClassicalType
{
    public float Value { get; set; } = value;
    public object GetValueAsObject() => Value;
    public void SetValueFromObject(object value) => Value = (float)value;
    public static FloatType GetDefaultValue() => new(0f);
    private static float GetFloatValue(IClassicalType term, [CallerMemberName] string operationName = "")
    {
        if (term is FloatType floatType)
        {
            return floatType.Value;
        }
        throw new InvalidOperationException($"Operation {operationName} cannot be applied to {term.GetType().Name} type.");
    }

    public IQutesType Addition(IClassicalType term) => new FloatType(this.Value + GetFloatValue(term));
    public IQutesType Subtraction(IClassicalType term) => new FloatType(this.Value - GetFloatValue(term));
    public IQutesType Multiply(IClassicalType term) => new FloatType(this.Value * GetFloatValue(term));
    public IQutesType Divide(IClassicalType term) => new FloatType(this.Value / GetFloatValue(term));
    public IQutesType Module(IClassicalType term) => new FloatType(this.Value % GetFloatValue(term));

    public BoolType LowerThan(IClassicalType term) => new(this.Value < GetFloatValue(term));
    public BoolType LowerEqualThan(IClassicalType term) => new(this.Value <= GetFloatValue(term));
    public BoolType GreaterThan(IClassicalType term) => new(this.Value > GetFloatValue(term));
    public BoolType GreaterEqualThan(IClassicalType term) => new(this.Value >= GetFloatValue(term));
    public BoolType Equals(IClassicalType term) => new(this.Value == GetFloatValue(term));
    public BoolType NotEquals(IClassicalType term) => new(this.Value != GetFloatValue(term));

    public IQutesType Minus() => new FloatType(-this.Value);
    public IQutesType InplacePreIncrement() => new FloatType(++this.Value);
    public IQutesType InplacePreDecrement() => new FloatType(--this.Value);
    public IQutesType InplacePostIncrement() => new FloatType(this.Value++);
    public IQutesType InplacePostDecrement() => new FloatType(this.Value--);
}

public class StringType(string value) : IClassicalType
{
    public string Value { get; set; } = value;
    public object GetValueAsObject() => Value;
    public void SetValueFromObject(object value) => Value = (string)value;
    public static StringType GetDefaultValue() => new("");
    private static string GetStringValue(IClassicalType term, [CallerMemberName] string operationName = "")
    {
        if (term is StringType stringType)
        {
            return stringType.Value;
        }
        throw new InvalidOperationException($"Operation {operationName} cannot be applied to {term.GetType().Name} type.");
    }

    public IQutesType LeftShift(IntType positions)
    {
        var n = positions.Value % this.Value.Length;
        var result = this.Value[n..] + this.Value[..n].Reverse();
        return new StringType(result);
    }

    public IQutesType RightShift(IntType positions)
    {
        var n = positions.Value % this.Value.Length;
        var result = this.Value[^n..] + this.Value[..^n];
        return new StringType(result);
    }

    public IQutesType Addition(IClassicalType term) => new StringType(this.Value + GetStringValue(term));

    public IQutesType Subtraction(IClassicalType term) => new StringType(this.Value.Replace(GetStringValue(term), string.Empty));

    public BoolType LowerThan(IClassicalType term) => new (string.Compare(this.Value, GetStringValue(term)) < 0);

    public BoolType LowerEqualThan(IClassicalType term) => new (string.Compare(this.Value, GetStringValue(term)) <= 0);

    public BoolType GreaterThan(IClassicalType term) => new (string.Compare(this.Value, GetStringValue(term)) > 0);

    public BoolType GreaterEqualThan(IClassicalType term) => new (string.Compare(this.Value, GetStringValue(term)) >= 0);

    public BoolType Equals(IClassicalType term) => new (this.Value == GetStringValue(term));

    public BoolType NotEquals(IClassicalType term) => new (this.Value != GetStringValue(term));
}

public class ClassicalArrayType(IEnumerable<Symbol> values) : IClassicalType
{
    public IEnumerable<Symbol> Values { get; private set; } = values;
    public object GetValueAsObject() => Values;
    public void SetValueFromObject(object value) => Values = (IEnumerable<Symbol>)value;
    public static ClassicalArrayType GetDefaultValue() => new([]);
    private static IEnumerable<Symbol> GetArrayValues(IClassicalType term, [CallerMemberName] string operationName = "") 
    {
        if (term is ClassicalArrayType arrayType)
        {
            return arrayType.Values;
        }
        throw new InvalidOperationException($"Operation {operationName} cannot be applied to {term.GetType().Name} type.");
    }

    public IQutesType LeftShift(IntType positions)
    {
        var n = positions.Value % Values.Count();
        var result = GetArrayValues(this).Skip(n).Concat(GetArrayValues(this).Take(n).Reverse());
        return new ClassicalArrayType(result);
    }

    public IQutesType RightShift(IntType positions)
    {
        var n = positions.Value % Values.Count();
        var result = GetArrayValues(this).Skip(Values.Count() - n).Concat(GetArrayValues(this).Take(Values.Count() - n));
        return new ClassicalArrayType(result);
    }

    public IQutesType Addition(IClassicalType term) => new ClassicalArrayType(GetArrayValues(this).Concat(GetArrayValues(term)));

    public IQutesType Subtraction(IClassicalType term) => new ClassicalArrayType(GetArrayValues(this).Except(GetArrayValues(term)));

    public BoolType Equals(IClassicalType term) => new(!GetArrayValues(term).Any() && !GetArrayValues(term).Except(Values).Any());

    public BoolType NotEquals(IClassicalType term) => new(GetArrayValues(term).Any() || GetArrayValues(term).Except(Values).Any());
}

public class QubitType(string initialValue) : IQuantumType
{
    public int Size { get; } = 1;
    public IEnumerable<CircuitQubit?> Qubits { get; } = [new()];

    public static QubitType GetDefaultValue() => new ("0q");

    public CircuitOperation And(IQuantumType term) => new And(this, term, QubitType.GetDefaultValue());
    public CircuitOperation Or(IQuantumType term) => new Or(this, term, QubitType.GetDefaultValue());

    public CircuitOperation Negate(IQuantumType term) => new Not(this, term, QubitType.GetDefaultValue());
}

public class QuintType(string initialValue) : IQuantumType
{
    public const int _size = 3;
    public int Size { get; } = _size;
    public IEnumerable<CircuitQubit?> Qubits { get; } = Enumerable.Repeat<CircuitQubit>(null!, _size).Select(_ => new CircuitQubit()).ToList(); //ToList is important

    public static QuintType GetDefaultValue() => new ("0q");

    public CircuitOperation Addition(IQuantumType term) => new Addition(this, term, QuintType.GetDefaultValue());
    public CircuitOperation Subtraction(IQuantumType term) => new Subtraction(this, term, QuintType.GetDefaultValue());
    public CircuitOperation Multiply(IQuantumType term) => new Multiply(this, term, QuintType.GetDefaultValue());
    public CircuitOperation Divide(IQuantumType term) => new Divide(this, term, QuintType.GetDefaultValue());
    public CircuitOperation Module(IQuantumType term) => new Module(this, term, QuintType.GetDefaultValue());

    public CircuitOperation LowerThan(IQuantumType term) => new LowerThan(this, term, QubitType.GetDefaultValue());
    public CircuitOperation LowerEqualThan(IQuantumType term) => new LowerEqualThan(this, term, QubitType.GetDefaultValue());
    public CircuitOperation GreaterThan(IQuantumType term) => new GreaterThan(this, term, QubitType.GetDefaultValue());
    public CircuitOperation GreaterEqualThan(IQuantumType term) => new GreaterEqualThan(this, term, QubitType.GetDefaultValue());

    public CircuitOperation Minus() => new Opposite(this, QuintType.GetDefaultValue());
    public CircuitOperation InplacePreIncrement() => new Increment(this, this);
    public CircuitOperation InplacePostIncrement() => new Increment(this, this);
    public CircuitOperation InplacePreDecrement() => new Decrement(this, this);
    public CircuitOperation InplacePostDecrement() => new Decrement(this, this);
}

public class QustringType(string initialValue) : IQuantumType //TODO: this is an array type, should inherit from QuantumArrayType?
{
    public const int _size = 3;
    public int Size { get; private set; } = _size;
    public IEnumerable<CircuitQubit?> Qubits { get; private set; } = Enumerable.Repeat<CircuitQubit>(null!, _size).Select(_ => new CircuitQubit()).ToList(); //ToList is important

    public static QustringType GetDefaultValue() => new ("0");

    public CircuitOperation LeftShift(QuintType positions) => new LeftShift(this, positions);
    public CircuitOperation RightShift(QuintType positions) => new RightShift(this, positions);

    public CircuitOperation Addition(IQuantumType term)
    {
        var concatQustring = new QustringType(string.Empty) { Qubits = this.Qubits.Concat(term.Qubits) };
        Size = concatQustring.Qubits.Count();
        return new Empty(concatQustring);
    }

    public CircuitOperation LowerThan(IQuantumType term) => new LowerThan(this, term, QubitType.GetDefaultValue());
    public CircuitOperation LowerEqualThan(IQuantumType term) => new LowerEqualThan(this, term, QubitType.GetDefaultValue());
    public CircuitOperation GreaterThan(IQuantumType term) => new GreaterThan(this, term, QubitType.GetDefaultValue());
    public CircuitOperation GreaterEqualThan(IQuantumType term) => new GreaterEqualThan(this, term, QubitType.GetDefaultValue());
}

public class QuantumArrayType(IEnumerable<Symbol> values) : IQuantumType
{
    public const int _size = 3; //TODO: depends on values type size.
    public int Size { get; private set; } = _size;
    public IEnumerable<CircuitQubit?> Qubits { get; private set; } = Enumerable.Repeat<CircuitQubit>(new(), _size);

    public static QuantumArrayType GetDefaultValue() => new([]);

    public CircuitOperation LeftShift(QuintType positions) => new LeftShift(this, positions);
    public CircuitOperation RightShift(QuintType positions) => new RightShift(this, positions);

    public CircuitOperation Addition(IQuantumType term){
        var concatArray = new QuantumArrayType([]) { Qubits = this.Qubits.Concat(term.Qubits) };
        Size = concatArray.Qubits.Count();
        return new Empty(concatArray);
    }
}