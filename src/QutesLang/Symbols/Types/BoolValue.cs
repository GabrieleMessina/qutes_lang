using System.Runtime.CompilerServices;

using QutesLang.GrammarFrontend;

namespace QutesLang.Symbols.Types;

public class ClassValue(string qualifiedClassName) : IQutesValue
{
    public virtual TypeSymbol Type { get; } = TypeSymbol.Class();
    public virtual bool TryConvertTo(TypeSymbol targetType, out IQutesValue result)
    {
        throw new NotImplementedException();
    }
}

public class VoidValue() : IQutesValue
{
    public virtual TypeSymbol Type { get; } = TypeSymbol.Void();
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

public class BoolValue(bool value) : IClassicalType
{
    public virtual TypeSymbol Type { get; } = TypeSymbol.Bool();
    public bool Value { get; set; } = value;
    public object GetValueAsObject() => Value;
    public void SetValueFromObject(object value) => Value = (bool)value;
    public static BoolValue GetDefaultValue() => new(false);
    private static bool GetBoolValue(IClassicalType term, [CallerMemberName] string operationName = "")
    {
        if (term is BoolValue boolType)
        {
            return boolType.Value;
        }
        throw new InvalidOperationException($"Operation {operationName} cannot be applied to {term.GetType().Name} type.");
    }
    public BoolValue Equals(IClassicalType term) => new (this.Value == GetBoolValue(term));
    public BoolValue NotEquals(IClassicalType term) => new (this.Value != GetBoolValue(term));

    public BoolValue And(IClassicalType term) => new (this.Value && GetBoolValue(term));
    public BoolValue Or(IClassicalType term) => new (this.Value || GetBoolValue(term));

    public BoolValue Not() => new (!this.Value);

    public virtual bool TryConvertTo(TypeSymbol targetType, out IQutesValue result)
    {
        if (targetType.Value == QutesType.boolean)
        {
            result = this;
            return true;
        }
        if (targetType.Value == QutesType.integer)
        {
            result = new IntValue(this.Value ? 1 : 0);
            return true;
        }
        if (targetType.Value == QutesType.qubit)
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
    public override TypeSymbol Type => TypeSymbol.Char();

    public override bool TryConvertTo(TypeSymbol targetType, out IQutesValue result)
    {
        if (targetType.Value == QutesType.character)
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

public class IntValue(int value) : IClassicalType
{
    public virtual TypeSymbol Type { get; } = TypeSymbol.Int();
    public int Value { get; set; } = value;
    public object GetValueAsObject() => Value;
    public void SetValueFromObject(object value) => Value = (int)value;
    public static IntValue GetDefaultValue() => new(0);
    private static int GetIntValue(IClassicalType term) => ((IntValue)term).Value;

    public IQutesValue LeftShift(IntValue positions) => new IntValue(this.Value << GetIntValue(positions));
    public IQutesValue RightShift(IntValue positions) => new IntValue(this.Value >> GetIntValue(positions));

    public IQutesValue Addition(IClassicalType term) => new IntValue(this.Value + GetIntValue(term));
    public IQutesValue Subtraction(IClassicalType term) => new IntValue(this.Value - GetIntValue(term));
    public IQutesValue Multiply(IClassicalType term) => new IntValue(this.Value * GetIntValue(term));
    public IQutesValue Divide(IClassicalType term) => new IntValue(this.Value / GetIntValue(term));
    public IQutesValue Module(IClassicalType term) => new IntValue(this.Value % GetIntValue(term));

    public BoolValue LowerThan(IClassicalType term) => new(this.Value < GetIntValue(term));
    public BoolValue LowerEqualThan(IClassicalType term) => new(this.Value <= GetIntValue(term));
    public BoolValue GreaterThan(IClassicalType term) => new(this.Value > GetIntValue(term));
    public BoolValue GreaterEqualThan(IClassicalType term) => new(this.Value >= GetIntValue(term));
    public BoolValue Equals(IClassicalType term) => new(this.Value == GetIntValue(term));
    public BoolValue NotEquals(IClassicalType term) => new(this.Value != GetIntValue(term));

    public IQutesValue Minus() => new IntValue(-this.Value);
    public IQutesValue InplacePreIncrement() => new IntValue(++this.Value);
    public IQutesValue InplacePreDecrement() => new IntValue(--this.Value);
    public IQutesValue InplacePostIncrement() => new IntValue(this.Value++);
    public IQutesValue InplacePostDecrement() => new IntValue(this.Value--);

    public virtual bool TryConvertTo(TypeSymbol targetType, out IQutesValue result)
    {
        if (targetType.Value == QutesType.integer)
        {
            result = this;
            return true;
        }
        if (targetType.Value == QutesType.quinteger)
        {
            result = new QuintValue(this.Value);
            return true;
        }
        result = default!;
        return false;
    }
}

public class FloatValue(float value) : IClassicalType
{
    public virtual TypeSymbol Type { get; } = TypeSymbol.Float();
    public float Value { get; set; } = value;
    public object GetValueAsObject() => Value;
    public void SetValueFromObject(object value) => Value = (float)value;
    public static FloatValue GetDefaultValue() => new(0f);
    private static float GetFloatValue(IClassicalType term, [CallerMemberName] string operationName = "")
    {
        if (term is FloatValue floatType)
        {
            return floatType.Value;
        }
        throw new InvalidOperationException($"Operation {operationName} cannot be applied to {term.GetType().Name} type.");
    }

    public IQutesValue Addition(IClassicalType term) => new FloatValue(this.Value + GetFloatValue(term));
    public IQutesValue Subtraction(IClassicalType term) => new FloatValue(this.Value - GetFloatValue(term));
    public IQutesValue Multiply(IClassicalType term) => new FloatValue(this.Value * GetFloatValue(term));
    public IQutesValue Divide(IClassicalType term) => new FloatValue(this.Value / GetFloatValue(term));
    public IQutesValue Module(IClassicalType term) => new FloatValue(this.Value % GetFloatValue(term));

    public BoolValue LowerThan(IClassicalType term) => new(this.Value < GetFloatValue(term));
    public BoolValue LowerEqualThan(IClassicalType term) => new(this.Value <= GetFloatValue(term));
    public BoolValue GreaterThan(IClassicalType term) => new(this.Value > GetFloatValue(term));
    public BoolValue GreaterEqualThan(IClassicalType term) => new(this.Value >= GetFloatValue(term));
    public BoolValue Equals(IClassicalType term) => new(this.Value == GetFloatValue(term));
    public BoolValue NotEquals(IClassicalType term) => new(this.Value != GetFloatValue(term));

    public IQutesValue Minus() => new FloatValue(-this.Value);
    public IQutesValue InplacePreIncrement() => new FloatValue(++this.Value);
    public IQutesValue InplacePreDecrement() => new FloatValue(--this.Value);
    public IQutesValue InplacePostIncrement() => new FloatValue(this.Value++);
    public IQutesValue InplacePostDecrement() => new FloatValue(this.Value--);

    public virtual bool TryConvertTo(TypeSymbol targetType, out IQutesValue result)
    {
        if (targetType.Value == QutesType.floating)
        {
            result = this;
            return true;
        }
        result = default!;
        return false;
    }
}

public class StringValue(string value) : IClassicalType
{
    public virtual TypeSymbol Type { get; } = TypeSymbol.String();
    public string Value { get; set; } = value;
    public object GetValueAsObject() => Value;
    public void SetValueFromObject(object value) => Value = (string)value;
    public static StringValue GetDefaultValue() => new("");
    private static string GetStringValue(IClassicalType term, [CallerMemberName] string operationName = "")
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

    public IQutesValue Addition(IClassicalType term) => new StringValue(this.Value + GetStringValue(term));

    public IQutesValue Subtraction(IClassicalType term) => new StringValue(this.Value.Replace(GetStringValue(term), string.Empty));

    public BoolValue LowerThan(IClassicalType term) => new (string.Compare(this.Value, GetStringValue(term)) < 0);

    public BoolValue LowerEqualThan(IClassicalType term) => new (string.Compare(this.Value, GetStringValue(term)) <= 0);

    public BoolValue GreaterThan(IClassicalType term) => new (string.Compare(this.Value, GetStringValue(term)) > 0);

    public BoolValue GreaterEqualThan(IClassicalType term) => new (string.Compare(this.Value, GetStringValue(term)) >= 0);

    public BoolValue Equals(IClassicalType term) => new (this.Value == GetStringValue(term));

    public BoolValue NotEquals(IClassicalType term) => new (this.Value != GetStringValue(term));

    public virtual bool TryConvertTo(TypeSymbol targetType, out IQutesValue result)
    {
        if (targetType.Value == QutesType.@string)
        {
            result = this;
            return true;
        }
        result = default!;
        return false;
    }
}

public class ClassicalArrayValue(IEnumerable<ValueSymbol> values) : ArrayValue, IClassicalType
{
    public override IEnumerable<ValueSymbol> Values { get; protected set; } = values;

    public override TypeSymbol Type => new (QutesType.classicalArray, Values.First().Type);

    public object GetValueAsObject() => Values;
    public void SetValueFromObject(object value) => Values = (IEnumerable<ValueSymbol>)value;

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

    public IQutesValue Addition(IClassicalType term) => new ClassicalArrayValue(Values.Concat(Values));

    public IQutesValue Subtraction(IClassicalType term) => new ClassicalArrayValue(Values.Except(Values));

    public BoolValue Equals(IClassicalType term) => new(!Values.Any() && !Values.Except(Values).Any());

    public BoolValue NotEquals(IClassicalType term) => new(Values.Any() || Values.Except(Values).Any());
}

public class QubitValue() : IQuantumType
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

    public virtual TypeSymbol Type { get; } = TypeSymbol.Qubit();
    public int Size { get; } = DefaultSize;
    public QuantumRegister Register { get; } = new(DefaultSize);
    public StateVector? InitialStateVector { get; private set { field = value; Register.InitialStateVector = value; } }

    public static QubitValue GetDefaultValue() => new();

    public CircuitOperation And(IQuantumType term) => new And(this, term, QubitValue.GetDefaultValue());
    public CircuitOperation Or(IQuantumType term) => new Or(this, term, QubitValue.GetDefaultValue());
    public CircuitOperation Not() => new Not(this);

    public virtual bool TryConvertTo(TypeSymbol targetType, out IQutesValue result)
    {
        if (targetType.Value == QutesType.qubit)
        {
            result = this;
            return true;
        }
        if (targetType.Value == QutesType.quinteger)
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
    public new const int DefaultSize = 2; //TODO: size could be derived from the alphabet length.

    public static readonly char[] Alphabet = ['2', '3'];

    public QucharValue() : base()
    {
    }

    public QucharValue(StateVector initialStateVector) : base(initialStateVector)
    {
    }

    public QucharValue(char value) : this(QucharParser.Parse($"'{value}'q"))
    {
    }

    public override TypeSymbol Type => TypeSymbol.Char();

    public new static QucharValue GetDefaultValue() => new (QustringParser.Parse("0"));

    public override bool TryConvertTo(TypeSymbol targetType, out IQutesValue result)
    {
        if (targetType.Value == QutesType.quinteger)
        {
            result = this;
            return true;
        }
        result = default!;
        return false;
    }
}

public class QuintValue() : IQuantumType
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
        this.InitialStateVector.Amplitudes[0] = qubit.InitialStateVector?.Amplitudes[0] ?? StateVector.Default(QubitValue.DefaultSize).Amplitudes[0];
    }

    public QuintValue(int value) : this()
    {
        InitialStateVector = QuintParser.Parse(value.ToString() + "q");
    }

    public virtual TypeSymbol Type { get; } = TypeSymbol.Quint();
    public int Size { get; } = DefaultSize;
    public QuantumRegister Register { get; } = new(DefaultSize);
    public StateVector? InitialStateVector { get; private set { field = value; Register.InitialStateVector = value; }  }

    //TODO: is getDefaultValue really necessary? can we use an empty constructor instead?

    public static QuintValue GetDefaultValue() => new();

    public CircuitOperation Addition(IQuantumType term) => new Addition(this, term, QuintValue.GetDefaultValue()); //TODO: right now sum of char gives an error because return type of sum is quint and cannot cast quint to quchar.
    public CircuitOperation Subtraction(IQuantumType term) => new Subtraction(this, term, QuintValue.GetDefaultValue());
    public CircuitOperation Multiply(IQuantumType term) => new Multiply(this, term, QuintValue.GetDefaultValue());
    public CircuitOperation Divide(IQuantumType term) => new Divide(this, term, QuintValue.GetDefaultValue());
    public CircuitOperation Module(IQuantumType term) => new Module(this, term, QuintValue.GetDefaultValue());

    public CircuitOperation LowerThan(IQuantumType term) => new LowerThan(this, term, QubitValue.GetDefaultValue());
    public CircuitOperation LowerEqualThan(IQuantumType term) => new LowerEqualThan(this, term, QubitValue.GetDefaultValue());
    public CircuitOperation GreaterThan(IQuantumType term) => new GreaterThan(this, term, QubitValue.GetDefaultValue());
    public CircuitOperation GreaterEqualThan(IQuantumType term) => new GreaterEqualThan(this, term, QubitValue.GetDefaultValue());

    public CircuitOperation Minus() => new Opposite(this, QuintValue.GetDefaultValue());
    public CircuitOperation InplacePreIncrement() => new Increment(this, this);
    public CircuitOperation InplacePostIncrement() => new Increment(this, this);
    public CircuitOperation InplacePreDecrement() => new Decrement(this, this);
    public CircuitOperation InplacePostDecrement() => new Decrement(this, this);

    public virtual bool TryConvertTo(TypeSymbol targetType, out IQutesValue result)
    {
        if (targetType.Value == QutesType.quinteger)
        {
            result = this;
            return true;
        }
        result = default!;
        return false;
    }
}

public class QustringValue : IQuantumType //TODO: this is an array type, should inherit from QuantumArrayType?
{
    public const int CharSize = 3;

    public QustringValue(string initialValue)
    {
        InitialStateVector = QustringParser.Parse(initialValue);
        Size = initialValue.Length * CharSize;
        Register = new(Size, InitialStateVector);
    }

    public virtual TypeSymbol Type { get; } = TypeSymbol.Qustring();
    public int Size { get; }
    public QuantumRegister Register { get; }
    public StateVector? InitialStateVector { get; set { field = value; Register.InitialStateVector = value; } }

    public static QustringValue GetDefaultValue() => new ("0");

    public CircuitOperation LeftShift(QuintValue positions) => new LeftShift(this, positions);
    public CircuitOperation RightShift(QuintValue positions) => new RightShift(this, positions);

    public CircuitOperation LowerThan(IQuantumType term) => new LowerThan(this, term, QubitValue.GetDefaultValue());
    public CircuitOperation LowerEqualThan(IQuantumType term) => new LowerEqualThan(this, term, QubitValue.GetDefaultValue());
    public CircuitOperation GreaterThan(IQuantumType term) => new GreaterThan(this, term, QubitValue.GetDefaultValue());
    public CircuitOperation GreaterEqualThan(IQuantumType term) => new GreaterEqualThan(this, term, QubitValue.GetDefaultValue());

    public virtual bool TryConvertTo(TypeSymbol targetType, out IQutesValue result)
    {
        if (targetType.Value == QutesType.qustring)
        {
            result = this;
            return true;
        }
        result = default!;
        return false;
    }
}

public class QuantumArrayValue : ArrayValue, IQuantumType
{
    public QuantumArrayValue(IEnumerable<ValueSymbol> values)
    {
        Values = values;
        Size = Register.Qubits.Count;
    }

    public override TypeSymbol Type => new (QutesType.quantumArray, Values.First().Type);
    public int Size { get; }
    public QuantumRegister Register => new(Values.Select(v => v.Value).Cast<IQuantumType>().Select(v => v.Register));
    public override IEnumerable<ValueSymbol> Values { get; protected set; }

    public static QuantumArrayValue GetDefaultValue() => new([]);

    public CircuitOperation LeftShift(QuintValue positions) => new LeftShift(this, positions);
    public CircuitOperation RightShift(QuintValue positions) => new RightShift(this, positions);

    public CircuitOperation Addition(IQuantumType term){
        if (term is not QuantumArrayValue arratToConcat)
        {
            throw new InvalidOperationException($"Operation Addition cannot be applied to {term.GetType().Name} type.");
        }

        var concatArray = new QuantumArrayValue(Values.Concat(arratToConcat.Values));
        return new Empty(concatArray);
    }
}