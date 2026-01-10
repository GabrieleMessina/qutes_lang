using System.Runtime.CompilerServices;

using QutesLang.GrammarFrontend;

namespace QutesLang.Symbols.Types;

//todo: rename al type suffix to value?

public class ClassType(string qualifiedClassName) : IQutesType
{
    public TypeSymbol Type { get; } = TypeSymbol.Class();
    public bool TryConvertTo(TypeSymbol targetType, out IQutesType result)
    {
        throw new NotImplementedException();
    }
}

public class VoidType() : IQutesType
{
    public TypeSymbol Type { get; } = TypeSymbol.Void();
    public bool TryConvertTo(TypeSymbol targetType, out IQutesType result)
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

public class BoolType(bool value) : IClassicalType
{
    public TypeSymbol Type { get; } = TypeSymbol.Bool();
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

    public bool TryConvertTo(TypeSymbol targetType, out IQutesType result)
    {
        if (targetType.Value == QutesType.boolean)
        {
            result = this;
            return true;
        }
        if (targetType.Value == QutesType.integer)
        {
            result = new IntType(this.Value ? 1 : 0);
            return true;
        }
        if (targetType.Value == QutesType.qubit)
        {
            result = new QubitType(this.Value);
            return true;
        }
        result = default!;
        return false;
    }

    public static explicit operator IntType(BoolType v) => new(v.Value ? 1 : 0);
}

public class IntType(int value) : IClassicalType
{
    public TypeSymbol Type { get; } = TypeSymbol.Int();
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

    public bool TryConvertTo(TypeSymbol targetType, out IQutesType result)
    {
        if (targetType.Value == QutesType.integer)
        {
            result = this;
            return true;
        }
        if (targetType.Value == QutesType.quinteger)
        {
            result = new QuintType(this.Value);
            return true;
        }
        result = default!;
        return false;
    }
}

public class FloatType(float value) : IClassicalType
{
    public TypeSymbol Type { get; } = TypeSymbol.Float();
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

    public bool TryConvertTo(TypeSymbol targetType, out IQutesType result)
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

public class StringType(string value) : IClassicalType
{
    public TypeSymbol Type { get; } = TypeSymbol.String();
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

    public bool TryConvertTo(TypeSymbol targetType, out IQutesType result)
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

public class ClassicalArrayType(IEnumerable<ValueSymbol> values) : IArrayType, IClassicalType
{
    public override IEnumerable<ValueSymbol> Values { get; protected set; } = values;

    public override TypeSymbol Type => new (QutesType.classicalArray, Values.First().Type);

    public object GetValueAsObject() => Values;
    public void SetValueFromObject(object value) => Values = (IEnumerable<ValueSymbol>)value;

    public IQutesType LeftShift(IntType positions)
    {
        var n = positions.Value % Values.Count();
        var result = Values.Skip(n).Concat(Values.Take(n).Reverse());
        return new ClassicalArrayType(result);
    }

    public IQutesType RightShift(IntType positions)
    {
        var n = positions.Value % Values.Count();
        var result = Values.Skip(Values.Count() - n).Concat(Values.Take(Values.Count() - n));
        return new ClassicalArrayType(result);
    }

    public IQutesType Addition(IClassicalType term) => new ClassicalArrayType(Values.Concat(Values));

    public IQutesType Subtraction(IClassicalType term) => new ClassicalArrayType(Values.Except(Values));

    public BoolType Equals(IClassicalType term) => new(!Values.Any() && !Values.Except(Values).Any());

    public BoolType NotEquals(IClassicalType term) => new(Values.Any() || Values.Except(Values).Any());
}

public class QubitType() : IQuantumType
{
    public const int DefaultSize = 1;

    public QubitType(StateVector initialStateVector) : this()
    {
        InitialStateVector = initialStateVector;
    }

    public QubitType(bool value) : this()
    {
        InitialStateVector = QubitParser.Parse(value ? "1q" : "0q");
    }

    public TypeSymbol Type { get; } = TypeSymbol.Qubit();
    public int Size { get; } = DefaultSize;
    public QuantumRegister Register { get; } = new(DefaultSize);
    public StateVector? InitialStateVector { get; private set { field = value; Register.InitialStateVector = value; } }

    public static QubitType GetDefaultValue() => new();

    public CircuitOperation And(IQuantumType term) => new And(this, term, QubitType.GetDefaultValue());
    public CircuitOperation Or(IQuantumType term) => new Or(this, term, QubitType.GetDefaultValue());
    public CircuitOperation Not() => new Not(this);

    public bool TryConvertTo(TypeSymbol targetType, out IQutesType result)
    {
        if (targetType.Value == QutesType.qubit)
        {
            result = this;
            return true;
        }
        if (targetType.Value == QutesType.quinteger)
        {
            result = new QuintType(this);
            return true;
        }

        result = default!;
        return false;
    }

    public static explicit operator QuintType(QubitType qubit) => new(qubit);
}

public class QuintType() : IQuantumType
{
    public const int DefaultSize = 3;

    public QuintType(StateVector initialStateVector) : this()
    {
        InitialStateVector = initialStateVector;
    }

    public QuintType(QubitType qubit) : this()
    {
        this.Register.Qubits.ToList()[0] = qubit.Register.Qubits.First();
        this.InitialStateVector = StateVector.Default(DefaultSize);
        this.InitialStateVector.Amplitudes[0] = qubit.InitialStateVector.Amplitudes[0];
    }

    public QuintType(int value) : this()
    {
        InitialStateVector = QuintParser.Parse(value.ToString() + "q");
    }

    public TypeSymbol Type { get; } = TypeSymbol.Quint();
    public int Size { get; } = DefaultSize;
    public QuantumRegister Register { get; } = new(DefaultSize);
    public StateVector? InitialStateVector { get; private set { field = value; Register.InitialStateVector = value; }  }

    //TODO: is getDefaultValue really necessary? can we use an empty constructor instead?

    public static QuintType GetDefaultValue() => new();

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

    public bool TryConvertTo(TypeSymbol targetType, out IQutesType result)
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

public class QustringType : IQuantumType //TODO: this is an array type, should inherit from QuantumArrayType?
{
    public const int CharSize = 3;

    public QustringType(string initialValue)
    {
        InitialStateVector = QustringParser.Parse(initialValue);
        Size = initialValue.Length * CharSize;
        Register = new(Size, InitialStateVector);
    }

    public TypeSymbol Type { get; } = TypeSymbol.Qustring();
    public int Size { get; }
    public QuantumRegister Register { get; }
    public StateVector? InitialStateVector { get; set { field = value; Register.InitialStateVector = value; } }

    public static QustringType GetDefaultValue() => new ("0");

    public CircuitOperation LeftShift(QuintType positions) => new LeftShift(this, positions);
    public CircuitOperation RightShift(QuintType positions) => new RightShift(this, positions);

    public CircuitOperation LowerThan(IQuantumType term) => new LowerThan(this, term, QubitType.GetDefaultValue());
    public CircuitOperation LowerEqualThan(IQuantumType term) => new LowerEqualThan(this, term, QubitType.GetDefaultValue());
    public CircuitOperation GreaterThan(IQuantumType term) => new GreaterThan(this, term, QubitType.GetDefaultValue());
    public CircuitOperation GreaterEqualThan(IQuantumType term) => new GreaterEqualThan(this, term, QubitType.GetDefaultValue());

    public bool TryConvertTo(TypeSymbol targetType, out IQutesType result)
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

public class QuantumArrayType : IArrayType, IQuantumType
{
    public QuantumArrayType(IEnumerable<ValueSymbol> values)
    {
        Values = values;
        Size = Register.Qubits.Count;
    }

    public override TypeSymbol Type => new (QutesType.quantumArray, Values.First().Type);
    public int Size { get; }
    public QuantumRegister Register => new(Values.Select(v => v.Value).Cast<IQuantumType>().Select(v => v.Register));
    public override IEnumerable<ValueSymbol> Values { get; protected set; }

    public static QuantumArrayType GetDefaultValue() => new([]);

    public CircuitOperation LeftShift(QuintType positions) => new LeftShift(this, positions);
    public CircuitOperation RightShift(QuintType positions) => new RightShift(this, positions);

    public CircuitOperation Addition(IQuantumType term){
        if (term is not QuantumArrayType arratToConcat)
        {
            throw new InvalidOperationException($"Operation Addition cannot be applied to {term.GetType().Name} type.");
        }

        var concatArray = new QuantumArrayType(Values.Concat(arratToConcat.Values));
        return new Empty(concatArray);
    }
}