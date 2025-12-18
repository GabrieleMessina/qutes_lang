using QutesLang.GrammarFrontend;

namespace QutesLang.Symbols.Types;

public interface IClassicalType : IQutesType
{
    public abstract object GetValueAsObject();
    public abstract void SetValueFromObject(object value);

    #region Operations
    IQutesType LeftShift(IntType positions) => throw new InvalidOperationException($"Operator {nameof(LeftShift)} cannot be applied to {this.GetType().Name} and {positions.GetType().Name}.");
    IQutesType RightShift(IntType positions) => throw new InvalidOperationException($"Operator {nameof(RightShift)} cannot be applied to {this.GetType().Name} and {positions.GetType().Name}.");
    IQutesType Swap(IClassicalType term)
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
    IQutesType Addition(IClassicalType term) => throw new InvalidOperationException($"Operator {nameof(Addition)} cannot be applied to {this.GetType().Name} and {term.GetType().Name}.");
    IQutesType Subtraction(IClassicalType term) => throw new InvalidOperationException($"Operator {nameof(Subtraction)} cannot be applied to {this.GetType().Name} and {term.GetType().Name}.");
    IQutesType Multiply(IClassicalType term) => throw new InvalidOperationException($"Operator {nameof(Multiply)} cannot be applied to {this.GetType().Name} and {term.GetType().Name}.");
    IQutesType Divide(IClassicalType term) => throw new InvalidOperationException($"Operator {nameof(Divide)} cannot be applied to {this.GetType().Name} and {term.GetType().Name}.");
    IQutesType Module(IClassicalType term) => throw new InvalidOperationException($"Operator {nameof(Module)} cannot be applied to {this.GetType().Name} and {term.GetType().Name}.");

    // Comparison operations
    BoolType LowerThan(IClassicalType term) => throw new InvalidOperationException($"Operator {nameof(LowerThan)} cannot be applied to {this.GetType().Name} and {term.GetType().Name}.");
    BoolType LowerEqualThan(IClassicalType term) => throw new InvalidOperationException($"Operator {nameof(LowerEqualThan)} cannot be applied to {this.GetType().Name} and {term.GetType().Name}.");
    BoolType GreaterThan(IClassicalType term) => throw new InvalidOperationException($"Operator {nameof(GreaterThan)} cannot be applied to {this.GetType().Name} and {term.GetType().Name}.");
    BoolType GreaterEqualThan(IClassicalType term) => throw new InvalidOperationException($"Operator {nameof(GreaterEqualThan)} cannot be applied to {this.GetType().Name} and {term.GetType().Name}.");

    BoolType Equals(IClassicalType term)
    {
        if (this.GetType() != term.GetType())
            throw new InvalidOperationException($"Operator {nameof(Equals)} cannot be applied to {this.GetType().Name} and {term.GetType().Name}.");
        
        var a = this.GetValueAsObject();
        var b = term.GetValueAsObject();
        return new BoolType(a.Equals(b));
    }
    BoolType NotEquals(IClassicalType term)
    {
        if (this.GetType() != term.GetType())
            throw new InvalidOperationException($"Operator {nameof(NotEquals)} cannot be applied to {this.GetType().Name} and {term.GetType().Name}.");
        
        var a = this.GetValueAsObject();
        var b = term.GetValueAsObject();
        return new BoolType(a.Equals(b) == false);
    }

    // Logical operations
    BoolType And(IClassicalType term) => throw new InvalidOperationException($"Operator {nameof(And)} cannot be applied to {this.GetType().Name} and {term.GetType().Name}.");
    BoolType Or(IClassicalType term) => throw new InvalidOperationException($"Operator {nameof(Or)} cannot be applied to {this.GetType().Name} and {term.GetType().Name}.");
    BoolType Not() => throw new InvalidOperationException($"Operator {nameof(Not)} cannot be applied to {this.GetType().Name}.");

    // Unary operations
    IQutesType Plus() => this;
    IQutesType Minus() => throw new InvalidOperationException($"Operator {nameof(Minus)} cannot be applied to {this.GetType().Name}.");
    IQutesType InplacePreIncrement() => throw new InvalidOperationException($"Operator {nameof(InplacePreIncrement)} cannot be applied to {this.GetType().Name}.");
    IQutesType InplacePostIncrement() => throw new InvalidOperationException($"Operator {nameof(InplacePostIncrement)} cannot be applied to {this.GetType().Name}.");
    IQutesType InplacePreDecrement() => throw new InvalidOperationException($"Operator {nameof(InplacePreDecrement)} cannot be applied to {this.GetType().Name}.");
    IQutesType InplacePostDecrement() => throw new InvalidOperationException($"Operator {nameof(InplacePostDecrement)} cannot be applied to {this.GetType().Name}.");
    #endregion Operations
}