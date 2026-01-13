using System.Runtime.CompilerServices;

using QutesLang.GrammarFrontend;

namespace QutesLang.Symbols.Types;

public class ClassValue(string qualifiedClassName) : IQutesValue
{
    public virtual TypeSymbol Type { get; } = TypeSymbol.Class;
    public virtual bool TryConvertTo(TypeSymbol targetType, out IQutesValue result)
    {
        throw new NotImplementedException();
    }
}

public class VoidValue() : IQutesValue
{
    public virtual TypeSymbol Type { get; } = TypeSymbol.Void;
    public static VoidValue GetDefaultValue() => new();
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

public class BoolValue(bool value) : IClassicalValue
{
    public virtual TypeSymbol Type { get; } = TypeSymbol.Bool;
    public bool Value { get; set; } = value;
    public object GetValueAsObject() => Value;
    public void SetValueFromObject(object value) => Value = (bool)value;
    public static BoolValue GetDefaultValue() => new(false);
    private static bool GetBoolValue(IClassicalValue term, [CallerMemberName] string operationName = "")
    {
        if (term is BoolValue boolType)
        {
            return boolType.Value;
        }
        throw new InvalidOperationException($"Operation {operationName} cannot be applied to {term.GetType().Name} type.");
    }
    public BoolValue Equals(IClassicalValue term) => new (this.Value == GetBoolValue(term));
    public BoolValue NotEquals(IClassicalValue term) => new (this.Value != GetBoolValue(term));

    public BoolValue And(IClassicalValue term) => new (this.Value && GetBoolValue(term));
    public BoolValue Or(IClassicalValue term) => new (this.Value || GetBoolValue(term));

    public BoolValue Not() => new (!this.Value);

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
        if (targetType.Value == QutesType.qucharacter)
        {
            result = new QucharValue(Convert.ToChar(this.Value));
            return true;
        }
        result = default!;
        return false;
    }
}

public class IntValue(int value) : IClassicalValue
{
    public virtual TypeSymbol Type { get; } = TypeSymbol.Int;
    public int Value { get; set; } = value;
    public object GetValueAsObject() => Value;
    public void SetValueFromObject(object value) => Value = (int)value;
    public static IntValue GetDefaultValue() => new(0);
    private static int GetIntValue(IClassicalValue term) => ((IntValue)term).Value;

    public IQutesValue LeftShift(IntValue positions) => new IntValue(this.Value << GetIntValue(positions));
    public IQutesValue RightShift(IntValue positions) => new IntValue(this.Value >> GetIntValue(positions));

    public IQutesValue Addition(IClassicalValue term) => new IntValue(this.Value + GetIntValue(term));
    public IQutesValue Subtraction(IClassicalValue term) => new IntValue(this.Value - GetIntValue(term));
    public IQutesValue Multiply(IClassicalValue term) => new IntValue(this.Value * GetIntValue(term));
    public IQutesValue Divide(IClassicalValue term) => new IntValue(this.Value / GetIntValue(term));
    public IQutesValue Module(IClassicalValue term) => new IntValue(this.Value % GetIntValue(term));

    public BoolValue LowerThan(IClassicalValue term) => new(this.Value < GetIntValue(term));
    public BoolValue LowerEqualThan(IClassicalValue term) => new(this.Value <= GetIntValue(term));
    public BoolValue GreaterThan(IClassicalValue term) => new(this.Value > GetIntValue(term));
    public BoolValue GreaterEqualThan(IClassicalValue term) => new(this.Value >= GetIntValue(term));
    public BoolValue Equals(IClassicalValue term) => new(this.Value == GetIntValue(term));
    public BoolValue NotEquals(IClassicalValue term) => new(this.Value != GetIntValue(term));

    public IQutesValue Minus() => new IntValue(-this.Value);
    public IQutesValue InplacePreIncrement() => new IntValue(++this.Value);
    public IQutesValue InplacePreDecrement() => new IntValue(--this.Value);
    public IQutesValue InplacePostIncrement() => new IntValue(this.Value++);
    public IQutesValue InplacePostDecrement() => new IntValue(this.Value--);

    public virtual bool TryConvertTo(TypeSymbol targetType, out IQutesValue result)
    {
        if (targetType == Type)
        {
            result = this;
            return true;
        }
        if (targetType == TypeSymbol.Int)
        {
            result = new QuintValue(this.Value);
            return true;
        }
        result = default!;
        return false;
    }
}

public class FloatValue(float value) : IClassicalValue
{
    public virtual TypeSymbol Type { get; } = TypeSymbol.Float;
    public float Value { get; set; } = value;
    public object GetValueAsObject() => Value;
    public void SetValueFromObject(object value) => Value = (float)value;
    public static FloatValue GetDefaultValue() => new(0f);
    private static float GetFloatValue(IClassicalValue term, [CallerMemberName] string operationName = "")
    {
        if (term is FloatValue floatType)
        {
            return floatType.Value;
        }
        throw new InvalidOperationException($"Operation {operationName} cannot be applied to {term.GetType().Name} type.");
    }

    public IQutesValue Addition(IClassicalValue term) => new FloatValue(this.Value + GetFloatValue(term));
    public IQutesValue Subtraction(IClassicalValue term) => new FloatValue(this.Value - GetFloatValue(term));
    public IQutesValue Multiply(IClassicalValue term) => new FloatValue(this.Value * GetFloatValue(term));
    public IQutesValue Divide(IClassicalValue term) => new FloatValue(this.Value / GetFloatValue(term));
    public IQutesValue Module(IClassicalValue term) => new FloatValue(this.Value % GetFloatValue(term));

    public BoolValue LowerThan(IClassicalValue term) => new(this.Value < GetFloatValue(term));
    public BoolValue LowerEqualThan(IClassicalValue term) => new(this.Value <= GetFloatValue(term));
    public BoolValue GreaterThan(IClassicalValue term) => new(this.Value > GetFloatValue(term));
    public BoolValue GreaterEqualThan(IClassicalValue term) => new(this.Value >= GetFloatValue(term));
    public BoolValue Equals(IClassicalValue term) => new(this.Value == GetFloatValue(term));
    public BoolValue NotEquals(IClassicalValue term) => new(this.Value != GetFloatValue(term));

    public IQutesValue Minus() => new FloatValue(-this.Value);
    public IQutesValue InplacePreIncrement() => new FloatValue(++this.Value);
    public IQutesValue InplacePreDecrement() => new FloatValue(--this.Value);
    public IQutesValue InplacePostIncrement() => new FloatValue(this.Value++);
    public IQutesValue InplacePostDecrement() => new FloatValue(this.Value--);

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

public class StringValue(string value) : IClassicalValue
{
    public virtual TypeSymbol Type { get; } = TypeSymbol.String;
    public string Value { get; set; } = value;
    public object GetValueAsObject() => Value;
    public void SetValueFromObject(object value) => Value = (string)value;
    public static StringValue GetDefaultValue() => new("");
    private static string GetStringValue(IClassicalValue term, [CallerMemberName] string operationName = "")
    {
        if (term is StringValue stringType)
        {
            return stringType.Value;
        }
        throw new InvalidOperationException($"Operation {operationName} cannot be applied to {term.GetType().Name} type.");
    }

    public IQutesValue LeftShift(IntValue positions)
    {
        var n = positions.Value % this.Value.Length;
        var result = this.Value[n..] + this.Value[..n].Reverse();
        return new StringValue(result);
    }

    public IQutesValue RightShift(IntValue positions)
    {
        var n = positions.Value % this.Value.Length;
        var result = this.Value[^n..] + this.Value[..^n];
        return new StringValue(result);
    }

    public IQutesValue Addition(IClassicalValue term) => new StringValue(this.Value + GetStringValue(term));

    public IQutesValue Subtraction(IClassicalValue term) => new StringValue(this.Value.Replace(GetStringValue(term), string.Empty));

    public BoolValue LowerThan(IClassicalValue term) => new (string.Compare(this.Value, GetStringValue(term)) < 0);

    public BoolValue LowerEqualThan(IClassicalValue term) => new (string.Compare(this.Value, GetStringValue(term)) <= 0);

    public BoolValue GreaterThan(IClassicalValue term) => new (string.Compare(this.Value, GetStringValue(term)) > 0);

    public BoolValue GreaterEqualThan(IClassicalValue term) => new (string.Compare(this.Value, GetStringValue(term)) >= 0);

    public BoolValue Equals(IClassicalValue term) => new (this.Value == GetStringValue(term));

    public BoolValue NotEquals(IClassicalValue term) => new (this.Value != GetStringValue(term));

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

public class ClassicalArrayValue(IEnumerable<ValueSymbol> values) : ArrayValue, IClassicalValue
{
    public override IEnumerable<ValueSymbol> Values { get; protected set; } = values;

    public override TypeSymbol Type => new (QutesType.classicalArray, Values.FirstOrDefault()?.Type);

    public object GetValueAsObject() => Values;
    public void SetValueFromObject(object value) => Values = (IEnumerable<ValueSymbol>)value;
    public static ClassicalArrayValue GetDefaultValue() => new([]);

    public IQutesValue LeftShift(IntValue positions)
    {
        var n = positions.Value % Values.Count();
        var result = Values.Skip(n).Concat(Values.Take(n).Reverse());
        return new ClassicalArrayValue(result);
    }

    public IQutesValue RightShift(IntValue positions)
    {
        var n = positions.Value % Values.Count();
        var result = Values.Skip(Values.Count() - n).Concat(Values.Take(Values.Count() - n));
        return new ClassicalArrayValue(result);
    }

    public IQutesValue Addition(IClassicalValue term) => new ClassicalArrayValue(Values.Concat(Values));

    public IQutesValue Subtraction(IClassicalValue term) => new ClassicalArrayValue(Values.Except(Values));

    public BoolValue Equals(IClassicalValue term) => new(!Values.Any() && !Values.Except(Values).Any());

    public BoolValue NotEquals(IClassicalValue term) => new(Values.Any() || Values.Except(Values).Any());
}

public class QubitValue() : IQuantumValue
{
    public const int DefaultSize = 1;

    public QubitValue(StateVector initialStateVector) : this()
    {
        InitialStateVector = initialStateVector;
    }

    public QubitValue(bool value) : this()
    {
        InitialStateVector = QubitParser.Parse(value ? "1q" : "0q");
    }

    public virtual TypeSymbol Type { get; } = TypeSymbol.Qubit;
    public int Size { get; } = DefaultSize;
    public QuantumRegister Register { get; } = new(DefaultSize);
    public StateVector? InitialStateVector { get; private set { field = value; Register.InitialStateVector = value; } }

    public static QubitValue GetDefaultValue() => new();

    public CircuitOperation And(IQuantumValue term) => new And(this, term, QubitValue.GetDefaultValue());
    public CircuitOperation Or(IQuantumValue term) => new Or(this, term, QubitValue.GetDefaultValue());
    public CircuitOperation Not() => new Not(this);

    public virtual bool TryConvertTo(TypeSymbol targetType, out IQutesValue result)
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

    public static explicit operator QuintValue(QubitValue qubit) => new(qubit);
}

public class QucharValue : QuintValue
{
    public static readonly char[] Alphabet = ['2', '3']; //TODO: this can't be larger than 2^QuintValue.DefaultSize

    public QucharValue() : base()
    {
    }

    public QucharValue(StateVector initialStateVector) : base(initialStateVector)
    {
    }

    public QucharValue(char value) : this(QucharParser.Parse($"'{value}'q"))
    {
    }

    public QucharValue(QuintValue value)
    {
        //InitialStateVector already handled in QuintValue
        this.Register = value.Register;
    }

    public override TypeSymbol Type => TypeSymbol.Char;

    public new static QucharValue GetDefaultValue() => new(QustringParser.Parse("0"));

    public override bool TryConvertTo(TypeSymbol targetType, out IQutesValue result)
    {
        if (targetType == Type)
        {
            result = this;
            return true;
        }
        if (targetType == TypeSymbol.Quint)
        {
            result = this;
            return true;
        }
        result = default!;
        return false;
    }
}

public class QuintValue() : IQuantumValue
{
    public const int DefaultSize = 3;

    public QuintValue(StateVector initialStateVector) : this()
    {
        InitialStateVector = initialStateVector;
    }

    public QuintValue(QubitValue qubit) : this()
    {
        this.Register.Qubits.ToList()[0] = qubit.Register.Qubits.First();
        this.InitialStateVector = StateVector.Default(DefaultSize);
        this.InitialStateVector.Amplitudes[0] = qubit.InitialStateVector?.Amplitudes[0] ?? StateVector.Default(QubitValue.DefaultSize).Amplitudes[0]; //TODO: this could lead to double initialization of the same qubit?
    }

    public QuintValue(int value) : this()
    {
        InitialStateVector = QuintParser.Parse(value.ToString() + "q");
    }

    public virtual TypeSymbol Type { get; } = TypeSymbol.Quint;
    public int Size { get; } = DefaultSize;
    public QuantumRegister Register { get; protected set; } = new(DefaultSize);
    public StateVector? InitialStateVector { get; private set { field = value; Register.InitialStateVector = value; }  }

    //TODO: is getDefaultValue really necessary? can we use an empty constructor instead?

    public static QuintValue GetDefaultValue() => new();

    public CircuitOperation Addition(IQuantumValue term) => new Addition(this, term, GetDefaultValue());
    public CircuitOperation Subtraction(IQuantumValue term) => new Subtraction(this, term, GetDefaultValue());
    public CircuitOperation Multiply(IQuantumValue term) => new Multiply(this, term, GetDefaultValue());
    public CircuitOperation Divide(IQuantumValue term) => new Divide(this, term, GetDefaultValue());
    public CircuitOperation Module(IQuantumValue term) => new Module(this, term, GetDefaultValue());

    public CircuitOperation LowerThan(IQuantumValue term) => new LowerThan(this, term, QubitValue.GetDefaultValue());
    public CircuitOperation LowerEqualThan(IQuantumValue term) => new LowerEqualThan(this, term, QubitValue.GetDefaultValue());
    public CircuitOperation GreaterThan(IQuantumValue term) => new GreaterThan(this, term, QubitValue.GetDefaultValue());
    public CircuitOperation GreaterEqualThan(IQuantumValue term) => new GreaterEqualThan(this, term, QubitValue.GetDefaultValue());

    public CircuitOperation Minus() => new Opposite(this, GetDefaultValue());
    public CircuitOperation InplacePreIncrement() => new Increment(this, this);
    public CircuitOperation InplacePostIncrement() => new Increment(this, this);
    public CircuitOperation InplacePreDecrement() => new Decrement(this, this);
    public CircuitOperation InplacePostDecrement() => new Decrement(this, this);

    public virtual bool TryConvertTo(TypeSymbol targetType, out IQutesValue result)
    {
        if (targetType == Type)
        {
            result = this;
            return true;
        }
        if (targetType == TypeSymbol.Quchar)
        {
            result = new QucharValue(this);
            return true;
        }
        result = default!;
        return false;
    }
}

public class QustringValue(string initialValue) : QuantumArrayValue(initialValue.Select(c => AnonymousValueSymbol.Default(new QucharValue(c))))
{
    public const int CharSize = 3;

    public CircuitOperation LowerThan(IQuantumValue term) => new LowerThan(this, term, QubitValue.GetDefaultValue());
    public CircuitOperation LowerEqualThan(IQuantumValue term) => new LowerEqualThan(this, term, QubitValue.GetDefaultValue());
    public CircuitOperation GreaterThan(IQuantumValue term) => new GreaterThan(this, term, QubitValue.GetDefaultValue());
    public CircuitOperation GreaterEqualThan(IQuantumValue term) => new GreaterEqualThan(this, term, QubitValue.GetDefaultValue());
}

public class QuantumArrayValue : ArrayValue, IQuantumValue
{
    public QuantumArrayValue(IEnumerable<ValueSymbol> values)
    {
        Values = values;
        Size = Register.Qubits.Count;
    }

    public override TypeSymbol Type => new (QutesType.quantumArray, Values.FirstOrDefault()?.Type);
    public int Size { get; }
    public QuantumRegister Register => new(Values.Select(v => v.Value).Cast<IQuantumValue>().Select(v => v.Register));
    public override IEnumerable<ValueSymbol> Values { get; protected set; }

    public static QuantumArrayValue GetDefaultValue() => new([]);

    public CircuitOperation LeftShift(QuintValue positions) => new LeftShift(this, positions);
    public CircuitOperation RightShift(QuintValue positions) => new RightShift(this, positions);

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