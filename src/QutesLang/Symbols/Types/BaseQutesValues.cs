using System.Runtime.CompilerServices;

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
    public virtual IQutesValue LeftShift(IQutesValue positions) => throw new InvalidOperationException($"Operator {nameof(LeftShift)} cannot be applied to {this.Type} and {positions.Type}.");
    public virtual IQutesValue RightShift(IQutesValue positions) => throw new InvalidOperationException($"Operator {nameof(RightShift)} cannot be applied to {this.Type} and {positions.Type}.");
    public virtual IQutesValue Swap(IQutesValue term)
    {
        if (this.Type != term.Type)
            throw new InvalidOperationException($"Cannot swap different types: {this.Type} and {term.Type}");

        var classicalValue = term.As<IClassicalValue>();
        var temp = this.GetValueAsObject();
        this.SetValueFromObject(classicalValue.GetValueAsObject());
        classicalValue.SetValueFromObject(temp);
        return this;
    }

    // Arithmetic operations
    public virtual IQutesValue Addition(IQutesValue term) => throw new InvalidOperationException($"Operator {nameof(Addition)} cannot be applied to {this.Type} and {term.Type}.");
    public virtual IQutesValue Subtraction(IQutesValue term) => throw new InvalidOperationException($"Operator {nameof(Subtraction)} cannot be applied to {this.Type} and {term.Type}.");
    public virtual IQutesValue Multiply(IQutesValue term) => throw new InvalidOperationException($"Operator {nameof(Multiply)} cannot be applied to {this.Type} and {term.Type}.");
    public virtual IQutesValue Divide(IQutesValue term) => throw new InvalidOperationException($"Operator {nameof(Divide)} cannot be applied to {this.Type} and {term.Type}.");
    public virtual IQutesValue Module(IQutesValue term) => throw new InvalidOperationException($"Operator {nameof(Module)} cannot be applied to {this.Type} and {term.Type}.");
    public virtual IQutesValue Exp(IQutesValue term) => throw new InvalidOperationException($"Operator {nameof(Exp)} cannot be applied to {this.Type} and {term.Type}.");

    // Comparison operations
    public virtual BoolValue LowerThan(IQutesValue term) => throw new InvalidOperationException($"Operator {nameof(LowerThan)} cannot be applied to {this.Type} and {term.Type}.");
    public virtual BoolValue LowerEqualThan(IQutesValue term) => throw new InvalidOperationException($"Operator {nameof(LowerEqualThan)} cannot be applied to {this.Type} and {term.Type}.");
    public virtual BoolValue GreaterThan(IQutesValue term) => throw new InvalidOperationException($"Operator {nameof(GreaterThan)} cannot be applied to {this.Type} and {term.Type}.");
    public virtual BoolValue GreaterEqualThan(IQutesValue term) => throw new InvalidOperationException($"Operator {nameof(GreaterEqualThan)} cannot be applied to {this.Type} and {term.Type}.");

    public virtual BoolValue Equals(IQutesValue term)
    {
        if (this.Type != term.Type)
            throw new InvalidOperationException($"Operator {nameof(Equals)} cannot be applied to {this.Type} and {term.Type}.");

        var classicalValue = term.As<IClassicalValue>();
        var a = this.GetValueAsObject();
        var b = classicalValue.GetValueAsObject();
        return new BoolValue(a.Equals(b));
    }
    public virtual BoolValue NotEquals(IQutesValue term)
    {
        if (this.Type != term.Type)
            throw new InvalidOperationException($"Operator {nameof(NotEquals)} cannot be applied to {this.Type} and {term.Type}.");

        var classicalValue = term.As<IClassicalValue>();
        var a = this.GetValueAsObject();
        var b = classicalValue.GetValueAsObject();
        return new BoolValue(a.Equals(b) == false);
    }

    // Logical operations
    public virtual BoolValue And(IQutesValue term) => throw new InvalidOperationException($"Operator {nameof(And)} cannot be applied to {this.Type} and {term.Type}.");
    public virtual BoolValue Or(IQutesValue term) => throw new InvalidOperationException($"Operator {nameof(Or)} cannot be applied to {this.Type} and {term.Type}.");
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

    public static IQuantumValue GetQuantumValue(IQutesValue term, [CallerMemberName] string operationName = "")
    {
        if (term is not IQuantumValue quantumValue)
            throw new InvalidOperationException($"Operation {operationName} cannot be applied to {term.Type} type.");

        return quantumValue;
    }

    #region Operations
    // Bitwise operations
    public virtual CircuitOperation LeftShift(IQutesValue positions) => throw new InvalidOperationException($"Operator {nameof(LeftShift)} cannot be applied to {this.Type} and {positions.Type}.");
    public virtual CircuitOperation RightShift(IQutesValue positions) => throw new InvalidOperationException($"Operator {nameof(RightShift)} cannot be applied to {this.Type} and {positions.Type}.");
    public virtual CircuitOperation Swap(IQutesValue term)
    {
        if (this.Type != term.Type)
            throw new InvalidOperationException($"Operator {nameof(Swap)} cannot be applied to {this.Type} and {term.Type}.");

        var quantumValue = term.As<IQuantumValue>();
        return new Swap(this, quantumValue);
    }

    // Arithmetic operations
    public virtual CircuitOperation Addition(IQutesValue term) => throw new InvalidOperationException($"Operator {nameof(Addition)} cannot be applied to {this.Type} and {term.Type}.");
    public virtual CircuitOperation Subtraction(IQutesValue term) => throw new InvalidOperationException($"Operator {nameof(Subtraction)} cannot be applied to {this.Type} and {term.Type}.");
    public virtual CircuitOperation Multiply(IQutesValue term) => throw new InvalidOperationException($"Operator {nameof(Multiply)} cannot be applied to {this.Type} and {term.Type}.");
    public virtual CircuitOperation Divide(IQutesValue term) => throw new InvalidOperationException($"Operator {nameof(Divide)} cannot be applied to {this.Type} and {term.Type}.");
    public virtual CircuitOperation Module(IQutesValue term) => throw new InvalidOperationException($"Operator {nameof(Module)} cannot be applied to {this.Type} and {term.Type}.");
    public virtual CircuitOperation Exp(IQutesValue term) => throw new InvalidOperationException($"Operator {nameof(Exp)} cannot be applied to {this.Type} and {term.Type}.");

    // Comparison operations
    public virtual CircuitOperation LowerThan(IQutesValue term) => throw new InvalidOperationException($"Operator {nameof(LowerThan)} cannot be applied to {this.Type} and {term.Type}.");
    public virtual CircuitOperation LowerEqualThan(IQutesValue term) => throw new InvalidOperationException($"Operator {nameof(LowerEqualThan)} cannot be applied to {this.Type} and {term.Type}.");
    public virtual CircuitOperation GreaterThan(IQutesValue term) => throw new InvalidOperationException($"Operator {nameof(GreaterThan)} cannot be applied to {this.Type} and {term.Type}.");
    public virtual CircuitOperation GreaterEqualThan(IQutesValue term) => throw new InvalidOperationException($"Operator {nameof(GreaterEqualThan)} cannot be applied to {this.Type} and {term.Type}.");
    public virtual CircuitOperation Equals(IQutesValue term)
    {
        if (this.Type != term.Type)
            throw new InvalidOperationException($"Operator {nameof(Equals)} cannot be applied to {this.Type} and {term.Type}.");

        var quantumValue = term.As<IQuantumValue>();
        return new Equals(this, quantumValue, this);
    }
    public virtual CircuitOperation NotEquals(IQutesValue term)
    {
        if (this.Type != term.Type)
            throw new InvalidOperationException($"Operator {nameof(NotEquals)} cannot be applied to {this.Type} and {term.Type}.");

        var quantumValue = term.As<IQuantumValue>();
        return new NotEquals(this, quantumValue, this);
    }

    // Logical operations
    public virtual CircuitOperation And(IQutesValue term) => throw new InvalidOperationException($"Operator {nameof(And)} cannot be applied to {this.Type} and {term.Type}.");
    public virtual CircuitOperation Or(IQutesValue term) => throw new InvalidOperationException($"Operator {nameof(Or)} cannot be applied to {this.Type} and {term.Type}.");
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
    /// <summary>
    /// Array elements, this cannot be a list of IQutesValue because we need to store also the symbol information,
    /// otherwise, we wouldn't be able to return a unique symbol when array is accessed.
    /// </summary>
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

    public override string ToString()
    {
        return "[" + string.Join(", ", Values) + "]";
    }
}