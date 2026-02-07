using QutesLang.GrammarFrontend;
using QutesLang.GrammarFrontend.Operations;
using QutesLang.Symbols.Types.Interfaces;

namespace QutesLang.Symbols.Types;

public class QubitValue() : QuantumValue
{
    public const int DefaultSize = 1;

    public QubitValue(QuintValue quint) : this()
    {
        this.Register.Qubits[0] = quint.Register.Qubits.First();
        this.InitialStateVector = StateVector.Default(DefaultSize);

        //The following could cause double initialization of the first qubit, but each StatePreparation (in Qiskit) overwrites previous ones, so we are good.
        var qubitStateVector = quint.InitialStateVector?.Amplitudes[0..2] ?? StateVector.Default(QubitValue.DefaultSize).Amplitudes[0..2];
        this.InitialStateVector.Amplitudes[0] = qubitStateVector[0];
        this.InitialStateVector.Amplitudes[1] = qubitStateVector[1];
    }

    public QubitValue(StateVector initialStateVector) : this()
    {
        InitialStateVector = initialStateVector;
    }

    public QubitValue(bool value) : this()
    {
        InitialStateVector = QubitParser.Parse(value ? "1" : "0");
    }

    public override TypeSymbol Type { get; } = TypeSymbol.Qubit;
    public override QuantumRegister Register { get; protected set; } = new(DefaultSize);
    public StateVector? InitialStateVector { get; private set { field = value; Register.InitialStateVector = value; } }

    public static QubitValue GetDefaultValue() => new();
    public static QubitValue Superposition() => PlusState();
    public static QubitValue PlusState() => new(QubitParser.Parse("|+>"));
    public static QubitValue MinusState() => new(QubitParser.Parse("|->"));

    public override QutesResult And(IQutesValue term) => new And(this, GetQuantumValue(term), QubitValue.GetDefaultValue());
    public override QutesResult Or(IQutesValue term) => new Or(this, GetQuantumValue(term), QubitValue.GetDefaultValue());
    public override QutesResult Not() => new Not(this);

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

    public static explicit operator QuintValue(QubitValue qubit) => new(qubit);
}

public class QucharValue : QuintValue
{
    public override int DefaultSize => CompilerFlags.Current.QucharSizeInQubit;

    public QucharValue() : base()
    {
    }

    public QucharValue(StateVector initialStateVector) : base(initialStateVector)
    {
    }

    public QucharValue(char value) : this(QucharParser.Parse($"'{value}'"))
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

public class QuintValue : QuantumValue
{
    public virtual int DefaultSize => CompilerFlags.Current.QuintSizeInQubit;
    public int MinValue => -(int)(Math.Ceiling(Math.Pow(2, DefaultSize))/2);
    public int MaxValue => (int)(Math.Floor(Math.Pow(2, DefaultSize))/2) - 1;

    public QuintValue()
    {
        Register = new(DefaultSize);
    }

    public QuintValue(StateVector initialStateVector) : this()
    {
        InitialStateVector = initialStateVector;
    }

    public QuintValue(QubitValue qubit) : this()
    {
        this.Register.Qubits[0] = qubit.Register.Qubits.First();
        this.InitialStateVector = StateVector.Default(DefaultSize);

        //The following could cause double initialization of the first qubit, but each StatePreparation (in Qiskit) overwrites previous ones, so we are good.
        var qubitStateVector = qubit.InitialStateVector?.Amplitudes[0..2] ?? StateVector.Default(QubitValue.DefaultSize).Amplitudes[0..2];
        this.InitialStateVector.Amplitudes[0] = qubitStateVector[0];
        this.InitialStateVector.Amplitudes[1] = qubitStateVector[1];
    }

    public QuintValue(int value) : this()
    {
        InitialStateVector = QuintParser.Parse(value.ToString());
    }
    
    public QuintValue(IntValue value) : this(value.Value)
    {
    }
    
    public QuintValue(FullyQualifiedRange range) : this()
    {
        var termList = new List<int>();
        for(var i = range.Start.Value; i < range.End.Value; i++)
        {
            if (i < MinValue || i > MaxValue)
            {
                throw new ArgumentException("RangeValue exceeds the bounds of the QuintValue size.");
            }
            termList.Add(i);
        }
        InitialStateVector = QuintParser.Parse($"{{{string.Join(',', termList)}}}");
    }

    public static QuintValue Superposition() => new(StateVector.Superposition(CompilerFlags.Current.QuintSizeInQubit));

    public override TypeSymbol Type { get; } = TypeSymbol.Quint;
    public override QuantumRegister Register { get; protected set; }
    public StateVector? InitialStateVector { get; private set { field = value; Register.InitialStateVector = value; } }

    public static QuintValue GetDefaultValue() => new();

    public override QutesResult Addition(IQutesValue term) => new Addition(this, GetQuantumValue(term), GetDefaultValue());
    public override QutesResult Subtraction(IQutesValue term) => new Subtraction(this, GetQuantumValue(term), GetDefaultValue());
    public override QutesResult Multiply(IQutesValue term) => new Multiply(this, GetQuantumValue(term), GetDefaultValue());
    public override QutesResult Divide(IQutesValue term) => new Divide(this, GetQuantumValue(term), GetDefaultValue());
    public override QutesResult Module(IQutesValue term) => new Module(this, GetQuantumValue(term), GetDefaultValue());

    public override QutesResult LowerThan(IQutesValue term) => new LowerThan(this, GetQuantumValue(term), QubitValue.GetDefaultValue());
    public override QutesResult LowerEqualThan(IQutesValue term) => new LowerEqualThan(this, GetQuantumValue(term), QubitValue.GetDefaultValue());
    public override QutesResult GreaterThan(IQutesValue term) => new GreaterThan(this, GetQuantumValue(term), QubitValue.GetDefaultValue());
    public override QutesResult GreaterEqualThan(IQutesValue term) => new GreaterEqualThan(this, GetQuantumValue(term), QubitValue.GetDefaultValue());

    public override QutesResult Minus() => new TwosComplement(this, GetDefaultValue());
    public override QutesResult InplacePreIncrement() => new Addition(this, this, new QuintValue(1));
    public override QutesResult InplacePostIncrement() => new Addition(this, this, new QuintValue(1));
    public override QutesResult InplacePreDecrement() => new Subtraction(this, this, new QuintValue(1));
    public override QutesResult InplacePostDecrement() => new Subtraction(this, this, new QuintValue(1));

    public override bool TryConvertTo(TypeSymbol targetType, out IQutesValue result)
    {
        if (targetType == Type)
        {
            result = this;
            return true;
        }
        if (targetType == TypeSymbol.Qubit)
        {
            result = new QubitValue(this);
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

public class QustringValue(string initialValue) : QuantumArrayValue(initialValue.Select(c => AnonymousValueSymbol.Default(new QucharValue(c))).ToList(), TypeSymbol.Quchar)
{
    public override QutesResult LowerThan(IQutesValue term) => new LowerThan(this, QuantumValue.GetQuantumValue(term), QubitValue.GetDefaultValue());
    public override QutesResult LowerEqualThan(IQutesValue term) => new LowerEqualThan(this, QuantumValue.GetQuantumValue(term), QubitValue.GetDefaultValue());
    public override QutesResult GreaterThan(IQutesValue term) => new GreaterThan(this, QuantumValue.GetQuantumValue(term), QubitValue.GetDefaultValue());
    public override QutesResult GreaterEqualThan(IQutesValue term) => new GreaterEqualThan(this, QuantumValue.GetQuantumValue(term), QubitValue.GetDefaultValue());

    public static QustringValue GetDefaultValue() => new(string.Empty);
}
