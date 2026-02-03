using QutesLang.GrammarFrontend;
using QutesLang.GrammarFrontend.Operations;
using QutesLang.Symbols.Types.Interfaces;

namespace QutesLang.Symbols.Types;

public class QubitValue() : QuantumScalarValue
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
        InitialStateVector = QubitParser.Parse(value ? "1q" : "0q");
    }

    public override TypeSymbol Type { get; } = TypeSymbol.Qubit;
    public override int Size { get; } = DefaultSize;
    public override QuantumRegister Register { get; protected set; } = new(DefaultSize);
    public StateVector? InitialStateVector { get; private set { field = value; Register.InitialStateVector = value; } }

    public static QubitValue GetDefaultValue() => new();
    public static QubitValue Superposition() => PlusState();
    public static QubitValue PlusState() => new(QubitParser.Parse("|+>"));
    public static QubitValue MinusState() => new(QubitParser.Parse("|->"));

    public override CircuitOperation And(IQuantumValue term) => new And(this, term, QubitValue.GetDefaultValue());
    public override CircuitOperation Or(IQuantumValue term) => new Or(this, term, QubitValue.GetDefaultValue());
    public override CircuitOperation Not() => new Not(this);

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
    public override int DefaultSize => CompilerFlags.Current.QustringSizeInQubit;

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

public class QuintValue : QuantumScalarValue
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
        InitialStateVector = QuintParser.Parse(value.ToString() + "q");
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
        InitialStateVector = QuintParser.Parse($"[{string.Join(',', termList)}]q");
    }

    public static QuintValue Superposition() => new(StateVector.Superposition(CompilerFlags.Current.QuintSizeInQubit));

    public override TypeSymbol Type { get; } = TypeSymbol.Quint;
    public override int Size => DefaultSize;
    public override QuantumRegister Register { get; protected set; }
    public StateVector? InitialStateVector { get; private set { field = value; Register.InitialStateVector = value; } }

    public static QuintValue GetDefaultValue() => new();

    public override CircuitOperation Addition(IQuantumValue term) => new Addition(this, term, GetDefaultValue());
    public override CircuitOperation Subtraction(IQuantumValue term) => new Subtraction(this, term, GetDefaultValue());
    public override CircuitOperation Multiply(IQuantumValue term) => new Multiply(this, term, GetDefaultValue());
    public override CircuitOperation Divide(IQuantumValue term) => new Divide(this, term, GetDefaultValue());
    public override CircuitOperation Module(IQuantumValue term) => new Module(this, term, GetDefaultValue());

    public override CircuitOperation LowerThan(IQuantumValue term) => new LowerThan(this, term, QubitValue.GetDefaultValue());
    public override CircuitOperation LowerEqualThan(IQuantumValue term) => new LowerEqualThan(this, term, QubitValue.GetDefaultValue());
    public override CircuitOperation GreaterThan(IQuantumValue term) => new GreaterThan(this, term, QubitValue.GetDefaultValue());
    public override CircuitOperation GreaterEqualThan(IQuantumValue term) => new GreaterEqualThan(this, term, QubitValue.GetDefaultValue());

    public override CircuitOperation Minus() => new TwosComplement(this, GetDefaultValue());
    public override CircuitOperation InplacePreIncrement() => new Addition(this, this, new QuintValue(1));
    public override CircuitOperation InplacePostIncrement() => new Addition(this, this, new QuintValue(1));
    public override CircuitOperation InplacePreDecrement() => new Subtraction(this, this, new QuintValue(1));
    public override CircuitOperation InplacePostDecrement() => new Subtraction(this, this, new QuintValue(1));

    public virtual bool TryConvertTo(TypeSymbol targetType, out IQutesValue result)
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
    public override CircuitOperation LowerThan(IQuantumValue term) => new LowerThan(this, term, QubitValue.GetDefaultValue());
    public override CircuitOperation LowerEqualThan(IQuantumValue term) => new LowerEqualThan(this, term, QubitValue.GetDefaultValue());
    public override CircuitOperation GreaterThan(IQuantumValue term) => new GreaterThan(this, term, QubitValue.GetDefaultValue());
    public override CircuitOperation GreaterEqualThan(IQuantumValue term) => new GreaterEqualThan(this, term, QubitValue.GetDefaultValue());

    public static QustringValue GetDefaultValue() => new(string.Empty);
}
