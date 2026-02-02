using QutesLang.GrammarFrontend;
using QutesLang.GrammarFrontend.Operations;
using QutesLang.Symbols.Types.Interfaces;

namespace QutesLang.Symbols.Types;

public abstract class ClassicalScalarValue : IClassicalValue
{
    public abstract TypeSymbol Type { get; }

    public abstract object GetValueAsObject();
    public abstract void SetValueFromObject(object value);

    public override string ToString()
    {
        return $"{GetValueAsObject()}";
    }

    #region Operations
    // Bitwise operations
    public virtual IQutesValue LeftShift(IntValue positions) => throw new InvalidOperationException($"Operator {nameof(LeftShift)} cannot be applied to {this.Type} and {positions.Type}.");
    public virtual IQutesValue RightShift(IntValue positions) => throw new InvalidOperationException($"Operator {nameof(RightShift)} cannot be applied to {this.Type} and {positions.Type}.");
    public virtual IQutesValue Swap(IClassicalValue term)
    {
        if (this.Type != term.Type)
        {
            throw new InvalidOperationException($"Cannot swap different types: {this.Type} and {term.Type}");
        }
        var temp = this.GetValueAsObject();
        this.SetValueFromObject(term.GetValueAsObject());
        term.SetValueFromObject(temp);
        return this;
    }

    // Arithmetic operations
    public virtual IQutesValue Addition(IClassicalValue term) => throw new InvalidOperationException($"Operator {nameof(Addition)} cannot be applied to {this.Type} and {term.Type}.");
    public virtual IQutesValue Subtraction(IClassicalValue term) => throw new InvalidOperationException($"Operator {nameof(Subtraction)} cannot be applied to {this.Type} and {term.Type}.");
    public virtual IQutesValue Multiply(IClassicalValue term) => throw new InvalidOperationException($"Operator {nameof(Multiply)} cannot be applied to {this.Type} and {term.Type}.");
    public virtual IQutesValue Divide(IClassicalValue term) => throw new InvalidOperationException($"Operator {nameof(Divide)} cannot be applied to {this.Type} and {term.Type}.");
    public virtual IQutesValue Module(IClassicalValue term) => throw new InvalidOperationException($"Operator {nameof(Module)} cannot be applied to {this.Type} and {term.Type}.");
    public virtual IQutesValue Exp(IClassicalValue term) => throw new InvalidOperationException($"Operator {nameof(Exp)} cannot be applied to {this.Type} and {term.Type}.");

    // Comparison operations
    public virtual BoolValue LowerThan(IClassicalValue term) => throw new InvalidOperationException($"Operator {nameof(LowerThan)} cannot be applied to {this.Type} and {term.Type}.");
    public virtual BoolValue LowerEqualThan(IClassicalValue term) => throw new InvalidOperationException($"Operator {nameof(LowerEqualThan)} cannot be applied to {this.Type} and {term.Type}.");
    public virtual BoolValue GreaterThan(IClassicalValue term) => throw new InvalidOperationException($"Operator {nameof(GreaterThan)} cannot be applied to {this.Type} and {term.Type}.");
    public virtual BoolValue GreaterEqualThan(IClassicalValue term) => throw new InvalidOperationException($"Operator {nameof(GreaterEqualThan)} cannot be applied to {this.Type} and {term.Type}.");

    public virtual BoolValue Equals(IClassicalValue term)
    {
        if (this.Type != term.Type)
            throw new InvalidOperationException($"Operator {nameof(Equals)} cannot be applied to {this.Type} and {term.Type}.");

        var a = this.GetValueAsObject();
        var b = term.GetValueAsObject();
        return new BoolValue(a.Equals(b));
    }
    public virtual BoolValue NotEquals(IClassicalValue term)
    {
        if (this.Type != term.Type)
            throw new InvalidOperationException($"Operator {nameof(NotEquals)} cannot be applied to {this.Type} and {term.Type}.");

        var a = this.GetValueAsObject();
        var b = term.GetValueAsObject();
        return new BoolValue(a.Equals(b) == false);
    }

    // Logical operations
    public virtual BoolValue And(IClassicalValue term) => throw new InvalidOperationException($"Operator {nameof(And)} cannot be applied to {this.Type} and {term.Type}.");
    public virtual BoolValue Or(IClassicalValue term) => throw new InvalidOperationException($"Operator {nameof(Or)} cannot be applied to {this.Type} and {term.Type}.");
    public virtual BoolValue Not() => throw new InvalidOperationException($"Operator {nameof(Not)} cannot be applied to {this.Type}.");

    // Unary operations
    public virtual IQutesValue Plus() => this;
    public virtual IQutesValue Minus() => throw new InvalidOperationException($"Operator {nameof(Minus)} cannot be applied to {this.Type}.");
    public virtual IQutesValue InplacePreIncrement() => throw new InvalidOperationException($"Operator {nameof(InplacePreIncrement)} cannot be applied to {this.Type}.");
    public virtual IQutesValue InplacePostIncrement() => throw new InvalidOperationException($"Operator {nameof(InplacePostIncrement)} cannot be applied to {this.Type}.");
    public virtual IQutesValue InplacePreDecrement() => throw new InvalidOperationException($"Operator {nameof(InplacePreDecrement)} cannot be applied to {this.Type}.");
    public virtual IQutesValue InplacePostDecrement() => throw new InvalidOperationException($"Operator {nameof(InplacePostDecrement)} cannot be applied to {this.Type}.");
    #endregion Operations
}

public abstract class QuantumScalarValue : IQuantumValue
{
    public abstract int Size { get; }
    public abstract QuantumRegister Register { get; protected set; }
    public abstract TypeSymbol Type { get; }

    public override string ToString()
    {
        return $"({Type}) {Register}";
    }

    #region Operations
    // Bitwise operations
    public virtual CircuitOperation LeftShift(QuintValue positions) => throw new InvalidOperationException($"Operator {nameof(LeftShift)} cannot be applied to {this.Type} and {positions.Type}.");
    public virtual CircuitOperation LeftShift(IntValue positions) => throw new InvalidOperationException($"Operator {nameof(LeftShift)} cannot be applied to {this.Type} and {positions.Type}.");
    public virtual CircuitOperation RightShift(QuintValue positions) => throw new InvalidOperationException($"Operator {nameof(RightShift)} cannot be applied to {this.Type} and {positions.Type}.");
    public virtual CircuitOperation RightShift(IntValue positions) => throw new InvalidOperationException($"Operator {nameof(RightShift)} cannot be applied to {this.Type} and {positions.Type}.");
    public virtual CircuitOperation Swap(IQuantumValue term)
    {
        return this.Type == term.Type
            ? new Swap(this, term)
            : throw new InvalidOperationException($"Operator {nameof(Swap)} cannot be applied to {this.Type} and {term.Type}.");
    }

    // Arithmetic operations
    public virtual CircuitOperation Addition(IQuantumValue term) => throw new InvalidOperationException($"Operator {nameof(Addition)} cannot be applied to {this.Type} and {term.Type}.");
    public virtual CircuitOperation Subtraction(IQuantumValue term) => throw new InvalidOperationException($"Operator {nameof(Subtraction)} cannot be applied to {this.Type} and {term.Type}.");
    public virtual CircuitOperation Multiply(IQuantumValue term) => throw new InvalidOperationException($"Operator {nameof(Multiply)} cannot be applied to {this.Type} and {term.Type}.");
    public virtual CircuitOperation Divide(IQuantumValue term) => throw new InvalidOperationException($"Operator {nameof(Divide)} cannot be applied to {this.Type} and {term.Type}.");
    public virtual CircuitOperation Module(IQuantumValue term) => throw new InvalidOperationException($"Operator {nameof(Module)} cannot be applied to {this.Type} and {term.Type}.");
    public virtual CircuitOperation Exp(IQuantumValue term) => throw new InvalidOperationException($"Operator {nameof(Exp)} cannot be applied to {this.Type} and {term.Type}.");

    // Comparison operations
    public virtual CircuitOperation LowerThan(IQuantumValue term) => throw new InvalidOperationException($"Operator {nameof(LowerThan)} cannot be applied to {this.Type} and {term.Type}.");
    public virtual CircuitOperation LowerEqualThan(IQuantumValue term) => throw new InvalidOperationException($"Operator {nameof(LowerEqualThan)} cannot be applied to {this.Type} and {term.Type}.");
    public virtual CircuitOperation GreaterThan(IQuantumValue term) => throw new InvalidOperationException($"Operator {nameof(GreaterThan)} cannot be applied to {this.Type} and {term.Type}.");
    public virtual CircuitOperation GreaterEqualThan(IQuantumValue term) => throw new InvalidOperationException($"Operator {nameof(GreaterEqualThan)} cannot be applied to {this.Type} and {term.Type}.");
    public virtual CircuitOperation Equals(IQuantumValue term)
    {
        if (this.Type != term.Type)
            throw new InvalidOperationException($"Operator {nameof(Equals)} cannot be applied to {this.Type} and {term.Type}.");
        return new Equals(this, term, this);
    }
    public virtual CircuitOperation NotEquals(IQuantumValue term)
    {
        if (this.Type != term.Type)
            throw new InvalidOperationException($"Operator {nameof(NotEquals)} cannot be applied to {this.Type} and {term.Type}.");
        return new NotEquals(this, term, this);
    }

    // Logical operations
    public virtual CircuitOperation And(IQuantumValue term) => throw new InvalidOperationException($"Operator {nameof(And)} cannot be applied to {this.Type} and {term.Type}.");
    public virtual CircuitOperation Or(IQuantumValue term) => throw new InvalidOperationException($"Operator {nameof(Or)} cannot be applied to {this.Type} and {term.Type}.");
    public virtual CircuitOperation Not() => throw new InvalidOperationException($"Operator {nameof(Not)} cannot be applied to {this.Type}.");

    // Unary operations
    public virtual CircuitOperation Plus() => new Empty(this);
    public virtual CircuitOperation Minus() => throw new InvalidOperationException($"Operator {nameof(Minus)} cannot be applied to {this.Type}.");
    public virtual CircuitOperation InplacePreIncrement() => throw new InvalidOperationException($"Operator {nameof(InplacePreIncrement)} cannot be applied to {this.Type}.");
    public virtual CircuitOperation InplacePostIncrement() => throw new InvalidOperationException($"Operator {nameof(InplacePostIncrement)} cannot be applied to {this.Type}.");
    public virtual CircuitOperation InplacePreDecrement() => throw new InvalidOperationException($"Operator {nameof(InplacePreDecrement)} cannot be applied to {this.Type}.");
    public virtual CircuitOperation InplacePostDecrement() => throw new InvalidOperationException($"Operator {nameof(InplacePostDecrement)} cannot be applied to {this.Type}.");
    #endregion Operations
}

public abstract class ArrayValue : IQutesValue
{
    public abstract IEnumerable<ValueSymbol> Values { get; protected set; }
    public abstract TypeSymbol Type { get; }

    public virtual bool TryConvertTo(TypeSymbol targetType, out IQutesValue result)
    {
        if (Type == targetType)
        {
            result = this;
            return true;
        }
        else
        {
            var newArray = CastAllElementsToType(targetType.NestedValue!);
            result = newArray;
            return true;
        }
    }

    private ArrayValue CastAllElementsToType(TypeSymbol elementsType)
    {
        var castedValues = new List<ValueSymbol>();
        foreach (var symbol in Values)
        {
            if (symbol.Value.TryConvertTo(elementsType, out var castedValue))
            {
                castedValues.Add(new AnonymousValueSymbol(castedValue, null!, default)); //TODO: check scope and astTokenIndex how to handle here. And if really necessay in general.
            }
            else
            {
                throw new InvalidCastException($"Cannot cast value of type {symbol.Type} to {elementsType}");
            }
        }

        if (elementsType.IsQuantum())
        {
            return new QuantumArrayValue(castedValues, elementsType);

        }
        else
        {
            return new ClassicalArrayValue(castedValues, elementsType);
        }
    }
}