using QutesLang.QuantumCircuits;
using QutesLang.QuantumCircuits.Operations;
using QutesLang.Symbols.Types.Interfaces;

namespace QutesLang.Symbols.Types;

public class ClassicalArrayValue(IEnumerable<ValueSymbol> values, TypeSymbol elementsType) : ArrayValue, IClassicalValue
{
    public override TypeSymbol Type { get; } = new(QutesType.classicalArray, elementsType);
    public override IEnumerable<ValueSymbol> Values { get; protected set; } = values;

    public object GetValueAsObject() => Values;
    public void SetValueFromObject(object value) => Values = (IEnumerable<ValueSymbol>)value;
    public static ClassicalArrayValue GetDefaultValue(TypeSymbol elementType) => new([], elementType);

    public override QutesResult LeftShift(IQutesValue positions)
    {
        if(positions is not IntValue intValue)
            throw new InvalidOperationException($"Can only left shift {nameof(ClassicalArrayValue)} by an {nameof(IntValue)}.");
        var n = intValue.Value % Values.Count();
        var result = Values.Skip(n).Concat(Values.Take(n).Reverse());
        return new ClassicalArrayValue(result, elementsType);
    }

    public override QutesResult RightShift(IQutesValue positions)
    {
        if (positions is not IntValue intValue)
            throw new InvalidOperationException($"Can only right shift {nameof(ClassicalArrayValue)} by an {nameof(IntValue)}.");
        var n = intValue.Value % Values.Count();
        var result = Values.Skip(Values.Count() - n).Concat(Values.Take(Values.Count() - n));
        return new ClassicalArrayValue(result, elementsType);
    }

    public override QutesResult Addition(IQutesValue term) => new ClassicalArrayValue(Values.Concat(Values), elementsType);

    public override QutesResult Subtraction(IQutesValue term) => new ClassicalArrayValue(Values.Except(Values), elementsType);

    public override QutesResult Multiply(IQutesValue term)
    {
        if(term is not IntValue intTerm)
            throw new InvalidOperationException($"Can only multiply {nameof(ClassicalArrayValue)} by an {nameof(IntValue)}.");

        //Create new symbols starting from original array values.
        var values = 
            Enumerable.Range(0, intTerm.Value-1).SelectMany(_ => Values) //only create new registers for the multiplied(missing) part
            .Select(v => AnonymousValueSymbol.Default(
                Type.NestedValue!.GetValueFromType(
                    ((IClassicalValue)v.Value).GetValueAsObject()))) //TODO: is it better to create new instances or is it better to reuse the same instances?
            .ToList();
        return new ClassicalArrayValue([..Values, ..values], elementsType); //prepend original values
    }

    public override QutesResult Equals(IQutesValue term) => new BoolValue(!Values.Any() && !Values.Except(Values).Any());

    public override QutesResult NotEquals(IQutesValue term) => new BoolValue(Values.Any() || Values.Except(Values).Any());
}

public class QuantumArrayValue : ArrayValue, IQuantumValue
{
    public QuantumArrayValue(IEnumerable<ValueSymbol> values, TypeSymbol elementType)
    {
        Values = values;
        SingleElementSize = Count > 0 ? QubitCount / Count : elementType.GetSize();
        Type = new(QutesType.quantumArray, elementType);
    }

    public override TypeSymbol Type { get; }
    public override IEnumerable<ValueSymbol> Values { get; protected set; }
    private string Guid { get; } = VariableNameGuid.New("qarray");
    public QuantumRegister Register => new(
        Values.Select(v => v.Value).Cast<IQuantumValue>()
        .Select(v => v.Register).Reverse() //Reverse to match Qiskit LSB ordering.
    ) { Name = Guid }; //Values register can change over time, we need to retrieve it every time from the current values.

    /// <summary>
    /// Total size in qubits of the Quantum Array
    /// </summary>
    public int QubitCount => Register.Size;

    /// <summary>
    /// Size in qubits of a single element in the Quantum Array
    /// </summary>
    public int SingleElementSize { get; }

    public string QubitStringList => Register.QubitStringList;


    public static QuantumArrayValue GetDefaultValue(TypeSymbol elementsType) => new([], elementsType);

    public override QutesResult LeftShift(IQutesValue positions)
    {
        if (positions is IntValue intValue)
            return new LeftShift(this, intValue);
        if (positions is QuintValue quintValue)
            return new LeftShift(this, quintValue);
        throw new InvalidOperationException($"Can only left shift {nameof(QuantumArrayValue)} by an {nameof(IntValue)} or {nameof(QuintValue)}.");
    }

    public override QutesResult Multiply(IQutesValue term)
    {
        if (term is not IntValue intTerm)
            throw new InvalidOperationException($"Can only multiply {nameof(QuantumArrayValue)} by an {nameof(IntValue)}.");

        //Create new quantum registers in |0> state
        var finalValues =
            Enumerable.Range(0, intTerm.Value-1).SelectMany(_ => Values) //only create new registers for the multiplied(missing) part
            .Select(v => AnonymousValueSymbol.Default(
                Type.NestedValue!.GetDefaultValueFromType()))
            .ToList();

        //Copy corresponding original values to newly created registers.
        var originalValues = this.Values.ToList();
        var originalCount = originalValues.Count;
        List<CircuitOperation> operations = [];
        for (int i = 0; i < finalValues.Count; i++) //Act on new values only
        {
            operations.Add(new Copy((IQuantumValue)originalValues[i % originalCount].Value, (IQuantumValue)finalValues[i].Value));
        }

        return new Composition(operations, new QuantumArrayValue([..Values, ..finalValues], Type.NestedValue!));
    }

    public override QutesResult RightShift(IQutesValue positions)
    {
        if (positions is IntValue intValue)
            return new RightShift(this, intValue);
        if (positions is QuintValue quintValue)
            return new RightShift(this, quintValue);
        throw new InvalidOperationException($"Can only right shift {nameof(QuantumArrayValue)} by an {nameof(IntValue)} or {nameof(QuintValue)}.");
    }
}
