namespace QutesLang.Symbols.Types;

public interface IClassicalValue : IQutesValue
{
    public abstract object GetValueAsObject();
    public abstract void SetValueFromObject(object value);
    IQutesValue Addition(IClassicalValue term);
    BoolValue And(IClassicalValue term);
    IQutesValue Divide(IClassicalValue term);
    BoolValue Equals(IClassicalValue term);
    IQutesValue Exp(IClassicalValue term);
    BoolValue GreaterEqualThan(IClassicalValue term);
    BoolValue GreaterThan(IClassicalValue term);
    IQutesValue InplacePostDecrement();
    IQutesValue InplacePostIncrement();
    IQutesValue InplacePreDecrement();
    IQutesValue InplacePreIncrement();
    IQutesValue LeftShift(IntValue positions);
    BoolValue LowerEqualThan(IClassicalValue term);
    BoolValue LowerThan(IClassicalValue term);
    IQutesValue Minus();
    IQutesValue Module(IClassicalValue term);
    IQutesValue Multiply(IClassicalValue term);
    BoolValue Not();
    BoolValue NotEquals(IClassicalValue term);
    BoolValue Or(IClassicalValue term);
    IQutesValue Plus();
    IQutesValue RightShift(IntValue positions);
    IQutesValue Subtraction(IClassicalValue term);
    IQutesValue Swap(IClassicalValue term);
}