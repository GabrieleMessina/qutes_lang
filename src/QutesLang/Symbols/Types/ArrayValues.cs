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

    public virtual IQutesValue LeftShift(IntValue positions)
    {
        var n = positions.Value % Values.Count();
        var result = Values.Skip(n).Concat(Values.Take(n).Reverse());
        return new ClassicalArrayValue(result, elementsType);
    }

    public virtual IQutesValue RightShift(IntValue positions)
    {
        var n = positions.Value % Values.Count();
        var result = Values.Skip(Values.Count() - n).Concat(Values.Take(Values.Count() - n));
        return new ClassicalArrayValue(result, elementsType);
    }

    public virtual IQutesValue Addition(IClassicalValue term) => new ClassicalArrayValue(Values.Concat(Values), elementsType);

    public virtual IQutesValue Subtraction(IClassicalValue term) => new ClassicalArrayValue(Values.Except(Values), elementsType);

    public virtual BoolValue Equals(IClassicalValue term) => new(!Values.Any() && !Values.Except(Values).Any());

    public virtual BoolValue NotEquals(IClassicalValue term) => new(Values.Any() || Values.Except(Values).Any());

    public virtual BoolValue And(IClassicalValue term)
    {
        throw new NotImplementedException();
    }

    public virtual IQutesValue Divide(IClassicalValue term)
    {
        throw new NotImplementedException();
    }

    public virtual IQutesValue Exp(IClassicalValue term)
    {
        throw new NotImplementedException();
    }

    public virtual BoolValue GreaterEqualThan(IClassicalValue term)
    {
        throw new NotImplementedException();
    }

    public virtual BoolValue GreaterThan(IClassicalValue term)
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

    public virtual BoolValue LowerEqualThan(IClassicalValue term)
    {
        throw new NotImplementedException();
    }

    public virtual BoolValue LowerThan(IClassicalValue term)
    {
        throw new NotImplementedException();
    }

    public virtual IQutesValue Minus()
    {
        throw new NotImplementedException();
    }

    public virtual IQutesValue Module(IClassicalValue term)
    {
        throw new NotImplementedException();
    }

    public virtual IQutesValue Multiply(IClassicalValue term)
    {
        throw new NotImplementedException();
    }

    public virtual BoolValue Not()
    {
        throw new NotImplementedException();
    }

    public virtual BoolValue Or(IClassicalValue term)
    {
        throw new NotImplementedException();
    }

    public virtual IQutesValue Plus()
    {
        throw new NotImplementedException();
    }

    public virtual IQutesValue Swap(IClassicalValue term)
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

    public virtual CircuitOperation Addition(IQuantumValue term)
    {
        throw new NotImplementedException();
    }

    public virtual CircuitOperation And(IQuantumValue term)
    {
        throw new NotImplementedException();
    }

    public virtual CircuitOperation Divide(IQuantumValue term)
    {
        throw new NotImplementedException();
    }

    public virtual CircuitOperation Exp(IQuantumValue term)
    {
        throw new NotImplementedException();
    }

    public virtual CircuitOperation GreaterEqualThan(IQuantumValue term)
    {
        throw new NotImplementedException();
    }

    public virtual CircuitOperation GreaterThan(IQuantumValue term)
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

    public virtual CircuitOperation LeftShift(QuintValue positions) => new LeftShift(this, positions);
    public virtual CircuitOperation LeftShift(IntValue positions) => new LeftShift(this, positions);

    public virtual CircuitOperation LowerEqualThan(IQuantumValue term)
    {
        throw new NotImplementedException();
    }

    public virtual CircuitOperation LowerThan(IQuantumValue term)
    {
        throw new NotImplementedException();
    }

    public virtual CircuitOperation Minus()
    {
        throw new NotImplementedException();
    }

    public virtual CircuitOperation Module(IQuantumValue term)
    {
        throw new NotImplementedException();
    }

    public virtual CircuitOperation Multiply(IQuantumValue term)
    {
        throw new NotImplementedException();
    }

    public virtual CircuitOperation Not()
    {
        throw new NotImplementedException();
    }

    public virtual CircuitOperation NotEquals(IQuantumValue term)
    {
        throw new NotImplementedException();
    }

    public virtual CircuitOperation Equals(IQuantumValue term)
    {
        throw new NotImplementedException();
    }

    public virtual CircuitOperation Or(IQuantumValue term)
    {
        throw new NotImplementedException();
    }

    public virtual CircuitOperation Plus()
    {
        throw new NotImplementedException();
    }

    public virtual CircuitOperation RightShift(QuintValue positions) => new RightShift(this, positions);
    public virtual CircuitOperation RightShift(IntValue positions) => new RightShift(this, positions);

    public virtual CircuitOperation Subtraction(IQuantumValue term)
    {
        throw new NotImplementedException();
    }

    public virtual CircuitOperation Swap(IQuantumValue term)
    {
        throw new NotImplementedException();
    }
}
