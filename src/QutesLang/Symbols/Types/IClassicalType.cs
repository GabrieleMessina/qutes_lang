namespace QutesLang.Symbols.Types;

public interface IClassicalType : IQutesValue
{
    public abstract object GetValueAsObject();
    public abstract void SetValueFromObject(object value);

    #region Operations
    IQutesValue LeftShift(IntValue positions) => throw new InvalidOperationException($"Operator {nameof(LeftShift)} cannot be applied to {this.GetType().Name} and {positions.GetType().Name}.");
    IQutesValue RightShift(IntValue positions) => throw new InvalidOperationException($"Operator {nameof(RightShift)} cannot be applied to {this.GetType().Name} and {positions.GetType().Name}.");
    IQutesValue Swap(IClassicalType term)
    {
        if (this.GetType() != term.GetType())
        {
            throw new InvalidOperationException($"Cannot swap different types: {this.GetType().Name} and {term.GetType().Name}");
        }
        var temp = this.GetValueAsObject();
        this.SetValueFromObject(term.GetValueAsObject());
        term.SetValueFromObject(temp);
        return this;
    }

    // Arithmetic operations
    IQutesValue Addition(IClassicalType term) => throw new InvalidOperationException($"Operator {nameof(Addition)} cannot be applied to {this.GetType().Name} and {term.GetType().Name}.");
    IQutesValue Subtraction(IClassicalType term) => throw new InvalidOperationException($"Operator {nameof(Subtraction)} cannot be applied to {this.GetType().Name} and {term.GetType().Name}.");
    IQutesValue Multiply(IClassicalType term) => throw new InvalidOperationException($"Operator {nameof(Multiply)} cannot be applied to {this.GetType().Name} and {term.GetType().Name}.");
    IQutesValue Divide(IClassicalType term) => throw new InvalidOperationException($"Operator {nameof(Divide)} cannot be applied to {this.GetType().Name} and {term.GetType().Name}.");
    IQutesValue Module(IClassicalType term) => throw new InvalidOperationException($"Operator {nameof(Module)} cannot be applied to {this.GetType().Name} and {term.GetType().Name}.");
    IQutesValue Exp(IClassicalType term) => throw new InvalidOperationException($"Operator {nameof(Exp)} cannot be applied to {this.GetType().Name} and {term.GetType().Name}.");

    // Comparison operations
    BoolValue LowerThan(IClassicalType term) => throw new InvalidOperationException($"Operator {nameof(LowerThan)} cannot be applied to {this.GetType().Name} and {term.GetType().Name}.");
    BoolValue LowerEqualThan(IClassicalType term) => throw new InvalidOperationException($"Operator {nameof(LowerEqualThan)} cannot be applied to {this.GetType().Name} and {term.GetType().Name}.");
    BoolValue GreaterThan(IClassicalType term) => throw new InvalidOperationException($"Operator {nameof(GreaterThan)} cannot be applied to {this.GetType().Name} and {term.GetType().Name}.");
    BoolValue GreaterEqualThan(IClassicalType term) => throw new InvalidOperationException($"Operator {nameof(GreaterEqualThan)} cannot be applied to {this.GetType().Name} and {term.GetType().Name}.");

    BoolValue Equals(IClassicalType term)
    {
        if (this.GetType() != term.GetType())
            throw new InvalidOperationException($"Operator {nameof(Equals)} cannot be applied to {this.GetType().Name} and {term.GetType().Name}.");
        
        var a = this.GetValueAsObject();
        var b = term.GetValueAsObject();
        return new BoolValue(a.Equals(b));
    }
    BoolValue NotEquals(IClassicalType term)
    {
        if (this.GetType() != term.GetType())
            throw new InvalidOperationException($"Operator {nameof(NotEquals)} cannot be applied to {this.GetType().Name} and {term.GetType().Name}.");
        
        var a = this.GetValueAsObject();
        var b = term.GetValueAsObject();
        return new BoolValue(a.Equals(b) == false);
    }

    // Logical operations
    BoolValue And(IClassicalType term) => throw new InvalidOperationException($"Operator {nameof(And)} cannot be applied to {this.GetType().Name} and {term.GetType().Name}.");
    BoolValue Or(IClassicalType term) => throw new InvalidOperationException($"Operator {nameof(Or)} cannot be applied to {this.GetType().Name} and {term.GetType().Name}.");
    BoolValue Not() => throw new InvalidOperationException($"Operator {nameof(Not)} cannot be applied to {this.GetType().Name}.");

    // Unary operations
    IQutesValue Plus() => this;
    IQutesValue Minus() => throw new InvalidOperationException($"Operator {nameof(Minus)} cannot be applied to {this.GetType().Name}.");
    IQutesValue InplacePreIncrement() => throw new InvalidOperationException($"Operator {nameof(InplacePreIncrement)} cannot be applied to {this.GetType().Name}.");
    IQutesValue InplacePostIncrement() => throw new InvalidOperationException($"Operator {nameof(InplacePostIncrement)} cannot be applied to {this.GetType().Name}.");
    IQutesValue InplacePreDecrement() => throw new InvalidOperationException($"Operator {nameof(InplacePreDecrement)} cannot be applied to {this.GetType().Name}.");
    IQutesValue InplacePostDecrement() => throw new InvalidOperationException($"Operator {nameof(InplacePostDecrement)} cannot be applied to {this.GetType().Name}.");
    #endregion Operations
}