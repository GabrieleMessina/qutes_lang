using QutesLang.GrammarFrontend;
using QutesLang.GrammarFrontend.Operations;
using QutesLang.Symbols.Types.Interfaces;

namespace QutesLang.Symbols.Types;

public class ClassicalArrayValue(IEnumerable<ValueSymbol> values, TypeSymbol elementsType) : ArrayValue, IClassicalValue
{
    public override IEnumerable<ValueSymbol> Values { get; protected set; } = values;

    public override TypeSymbol Type { get; } = new(QutesType.classicalArray, elementsType);

    public object GetValueAsObject() => Values;
    public void SetValueFromObject(object value) => Values = (IEnumerable<ValueSymbol>)value;
    public static ClassicalArrayValue GetDefaultValue(TypeSymbol elementType) => new([], elementType);

    public virtual IQutesValue LeftShift(IQutesValue positions)
    {
        if(positions is not IntValue intValue)
            throw new InvalidOperationException($"Can only left shift {nameof(ClassicalArrayValue)} by an {nameof(IntValue)}.");
        var n = intValue.Value % Values.Count();
        var result = Values.Skip(n).Concat(Values.Take(n).Reverse());
        return new ClassicalArrayValue(result, elementsType);
    }

    public virtual IQutesValue RightShift(IQutesValue positions)
    {
        if (positions is not IntValue intValue)
            throw new InvalidOperationException($"Can only right shift {nameof(ClassicalArrayValue)} by an {nameof(IntValue)}.");
        var n = intValue.Value % Values.Count();
        var result = Values.Skip(Values.Count() - n).Concat(Values.Take(Values.Count() - n));
        return new ClassicalArrayValue(result, elementsType);
    }

    public virtual IQutesValue Addition(IQutesValue term) => new ClassicalArrayValue(Values.Concat(Values), elementsType);

    public virtual IQutesValue Subtraction(IQutesValue term) => new ClassicalArrayValue(Values.Except(Values), elementsType);

    public virtual IQutesValue Multiply(IQutesValue term)
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

    public virtual BoolValue Equals(IQutesValue term) => new(!Values.Any() && !Values.Except(Values).Any());

    public virtual BoolValue NotEquals(IQutesValue term) => new(Values.Any() || Values.Except(Values).Any());

    public virtual BoolValue And(IQutesValue term)
    {
        throw new NotImplementedException();
    }

    public virtual IQutesValue Divide(IQutesValue term)
    {
        throw new NotImplementedException();
    }

    public virtual IQutesValue Exp(IQutesValue term)
    {
        throw new NotImplementedException();
    }

    public virtual BoolValue GreaterEqualThan(IQutesValue term)
    {
        throw new NotImplementedException();
    }

    public virtual BoolValue GreaterThan(IQutesValue term)
    {
        throw new NotImplementedException();
    }

    public virtual IQutesValue InplacePostDecrement()
    {
        throw new NotImplementedException();
    }

    public virtual IQutesValue InplacePostIncrement()
    {
        throw new NotImplementedException();
    }

    public virtual IQutesValue InplacePreDecrement()
    {
        throw new NotImplementedException();
    }

    public virtual IQutesValue InplacePreIncrement()
    {
        throw new NotImplementedException();
    }

    public virtual BoolValue LowerEqualThan(IQutesValue term)
    {
        throw new NotImplementedException();
    }

    public virtual BoolValue LowerThan(IQutesValue term)
    {
        throw new NotImplementedException();
    }

    public virtual IQutesValue Minus()
    {
        throw new NotImplementedException();
    }

    public virtual IQutesValue Module(IQutesValue term)
    {
        throw new NotImplementedException();
    }

    public virtual BoolValue Not()
    {
        throw new NotImplementedException();
    }

    public virtual BoolValue Or(IQutesValue term)
    {
        throw new NotImplementedException();
    }

    public virtual IQutesValue Plus()
    {
        throw new NotImplementedException();
    }

    public virtual IQutesValue Swap(IQutesValue term)
    {
        throw new NotImplementedException();
    }
}

public class QuantumArrayValue : ArrayValue, IQuantumValue
{
    public QuantumArrayValue(IEnumerable<ValueSymbol> values, TypeSymbol elementType)
    {
        Values = values;
        Register = new(Values.Select(v => v.Value).Cast<IQuantumValue>().Select(v => v.Register));
        Size = Register.Qubits.Count;
        Count = Values.Count();
        SingleElementSize = Count > 0 ? Size / Count : 0;
        Type = new(QutesType.quantumArray, elementType);
    }

    public override TypeSymbol Type { get; }

    /// <summary>
    /// Total size in qubits of the Quantum Array
    /// </summary>
    public int Size { get; }

    /// <summary>
    /// Number of elements in the Quantum Array
    /// </summary>
    public int Count { get; }

    /// <summary>
    /// Size in qubits of a single element in the Quantum Array
    /// </summary>
    public int SingleElementSize { get; }
    public QuantumRegister Register { get; }
    public override IEnumerable<ValueSymbol> Values { get; protected set; }

    public static QuantumArrayValue GetDefaultValue(TypeSymbol elementsType) => new([], elementsType);

    public virtual CircuitOperation Addition(IQutesValue term)
    {
        throw new NotImplementedException();
    }

    public virtual CircuitOperation And(IQutesValue term)
    {
        throw new NotImplementedException();
    }

    public virtual CircuitOperation Divide(IQutesValue term)
    {
        throw new NotImplementedException();
    }

    public virtual CircuitOperation Exp(IQutesValue term)
    {
        throw new NotImplementedException();
    }

    public virtual CircuitOperation GreaterEqualThan(IQutesValue term)
    {
        throw new NotImplementedException();
    }

    public virtual CircuitOperation GreaterThan(IQutesValue term)
    {
        throw new NotImplementedException();
    }

    public virtual CircuitOperation InplacePostDecrement()
    {
        throw new NotImplementedException();
    }

    public virtual CircuitOperation InplacePostIncrement()
    {
        throw new NotImplementedException();
    }

    public virtual CircuitOperation InplacePreDecrement()
    {
        throw new NotImplementedException();
    }

    public virtual CircuitOperation InplacePreIncrement()
    {
        throw new NotImplementedException();
    }

    public virtual CircuitOperation LeftShift(IQutesValue positions)
    {
        if (positions is IntValue intValue)
            return new LeftShift(this, intValue);
        if (positions is QuintValue quintValue)
            return new LeftShift(this, quintValue);
        throw new InvalidOperationException($"Can only left shift {nameof(QuantumArrayValue)} by an {nameof(IntValue)} or {nameof(QuintValue)}.");
    }

    public virtual CircuitOperation LowerEqualThan(IQutesValue term)
    {
        throw new NotImplementedException();
    }

    public virtual CircuitOperation LowerThan(IQutesValue term)
    {
        throw new NotImplementedException();
    }

    public virtual CircuitOperation Minus()
    {
        throw new NotImplementedException();
    }

    public virtual CircuitOperation Module(IQutesValue term)
    {
        throw new NotImplementedException();
    }

    public virtual CircuitOperation Multiply(IQutesValue term)
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

    public virtual CircuitOperation Not()
    {
        throw new NotImplementedException();
    }

    public virtual CircuitOperation NotEquals(IQutesValue term)
    {
        throw new NotImplementedException();
    }

    public virtual CircuitOperation Equals(IQutesValue term)
    {
        throw new NotImplementedException();
    }

    public virtual CircuitOperation Or(IQutesValue term)
    {
        throw new NotImplementedException();
    }

    public virtual CircuitOperation Plus()
    {
        throw new NotImplementedException();
    }

    public virtual CircuitOperation RightShift(IQutesValue positions)
    {
        if (positions is IntValue intValue)
            return new RightShift(this, intValue);
        if (positions is QuintValue quintValue)
            return new RightShift(this, quintValue);
        throw new InvalidOperationException($"Can only right shift {nameof(QuantumArrayValue)} by an {nameof(IntValue)} or {nameof(QuintValue)}.");
    }

    public virtual CircuitOperation Subtraction(IQutesValue term)
    {
        throw new NotImplementedException();
    }

    public virtual CircuitOperation Swap(IQutesValue term)
    {
        throw new NotImplementedException();
    }
}
