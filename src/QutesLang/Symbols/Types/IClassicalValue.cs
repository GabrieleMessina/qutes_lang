namespace QutesLang.Symbols.Types;

public interface IClassicalValue : IQutesValue
{
    public abstract object GetValueAsObject();
    public abstract void SetValueFromObject(object value);

    #region Operations
    // Bitwise operations
    IQutesValue LeftShift(IntValue positions) => throw new InvalidOperationException($"Operator {nameof(LeftShift)} cannot be applied to {this.Type} and {positions.Type}.");
    IQutesValue RightShift(IntValue positions) => throw new InvalidOperationException($"Operator {nameof(RightShift)} cannot be applied to {this.Type} and {positions.Type}.");
    IQutesValue Swap(IClassicalValue term)
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
    IQutesValue Addition(IClassicalValue term) => throw new InvalidOperationException($"Operator {nameof(Addition)} cannot be applied to {this.Type} and {term.Type}.");
    IQutesValue Subtraction(IClassicalValue term) => throw new InvalidOperationException($"Operator {nameof(Subtraction)} cannot be applied to {this.Type} and {term.Type}.");
    IQutesValue Multiply(IClassicalValue term) => throw new InvalidOperationException($"Operator {nameof(Multiply)} cannot be applied to {this.Type} and {term.Type}.");
    IQutesValue Divide(IClassicalValue term) => throw new InvalidOperationException($"Operator {nameof(Divide)} cannot be applied to {this.Type} and {term.Type}.");
    IQutesValue Module(IClassicalValue term) => throw new InvalidOperationException($"Operator {nameof(Module)} cannot be applied to {this.Type} and {term.Type}.");
    IQutesValue Exp(IClassicalValue term) => throw new InvalidOperationException($"Operator {nameof(Exp)} cannot be applied to {this.Type} and {term.Type}.");

    // Comparison operations
    BoolValue LowerThan(IClassicalValue term) => throw new InvalidOperationException($"Operator {nameof(LowerThan)} cannot be applied to {this.Type} and {term.Type}.");
    BoolValue LowerEqualThan(IClassicalValue term) => throw new InvalidOperationException($"Operator {nameof(LowerEqualThan)} cannot be applied to {this.Type} and {term.Type}.");
    BoolValue GreaterThan(IClassicalValue term) => throw new InvalidOperationException($"Operator {nameof(GreaterThan)} cannot be applied to {this.Type} and {term.Type}.");
    BoolValue GreaterEqualThan(IClassicalValue term) => throw new InvalidOperationException($"Operator {nameof(GreaterEqualThan)} cannot be applied to {this.Type} and {term.Type}.");

    BoolValue Equals(IClassicalValue term)
    {
        if (this.Type != term.Type)
            throw new InvalidOperationException($"Operator {nameof(Equals)} cannot be applied to {this.Type} and {term.Type}.");
        
        var a = this.GetValueAsObject();
        var b = term.GetValueAsObject();
        return new BoolValue(a.Equals(b));
    }
    BoolValue NotEquals(IClassicalValue term)
    {
        if (this.Type != term.Type)
            throw new InvalidOperationException($"Operator {nameof(NotEquals)} cannot be applied to {this.Type} and {term.Type}.");
        
        var a = this.GetValueAsObject();
        var b = term.GetValueAsObject();
        return new BoolValue(a.Equals(b) == false);
    }

    // Logical operations
    BoolValue And(IClassicalValue term) => throw new InvalidOperationException($"Operator {nameof(And)} cannot be applied to {this.Type} and {term.Type}.");
    BoolValue Or(IClassicalValue term) => throw new InvalidOperationException($"Operator {nameof(Or)} cannot be applied to {this.Type} and {term.Type}.");
    BoolValue Not() => throw new InvalidOperationException($"Operator {nameof(Not)} cannot be applied to {this.Type}.");

    // Unary operations
    IQutesValue Plus() => this;
    IQutesValue Minus() => throw new InvalidOperationException($"Operator {nameof(Minus)} cannot be applied to {this.Type}.");
    IQutesValue InplacePreIncrement() => throw new InvalidOperationException($"Operator {nameof(InplacePreIncrement)} cannot be applied to {this.Type}.");
    IQutesValue InplacePostIncrement() => throw new InvalidOperationException($"Operator {nameof(InplacePostIncrement)} cannot be applied to {this.Type}.");
    IQutesValue InplacePreDecrement() => throw new InvalidOperationException($"Operator {nameof(InplacePreDecrement)} cannot be applied to {this.Type}.");
    IQutesValue InplacePostDecrement() => throw new InvalidOperationException($"Operator {nameof(InplacePostDecrement)} cannot be applied to {this.Type}.");
    #endregion Operations
}