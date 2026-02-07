namespace QutesLang.Symbols.Types.Interfaces;

public interface IClassicalValue : IQutesValue
{
    public abstract object GetValueAsObject();
    public abstract void SetValueFromObject(object value);
    IQutesValue Addition(IQutesValue term);
    BoolValue And(IQutesValue term);
    IQutesValue Divide(IQutesValue term);
    BoolValue Equals(IQutesValue term);
    IQutesValue Exp(IQutesValue term);
    BoolValue GreaterEqualThan(IQutesValue term);
    BoolValue GreaterThan(IQutesValue term);
    IQutesValue InplacePostDecrement();
    IQutesValue InplacePostIncrement();
    IQutesValue InplacePreDecrement();
    IQutesValue InplacePreIncrement();
    IQutesValue LeftShift(IQutesValue positions);
    BoolValue LowerEqualThan(IQutesValue term);
    BoolValue LowerThan(IQutesValue term);
    IQutesValue Minus();
    IQutesValue Module(IQutesValue term);
    IQutesValue Multiply(IQutesValue term);
    BoolValue Not();
    BoolValue NotEquals(IQutesValue term);
    BoolValue Or(IQutesValue term);
    IQutesValue Plus();
    IQutesValue RightShift(IQutesValue positions);
    IQutesValue Subtraction(IQutesValue term);
    IQutesValue Swap(IQutesValue term);
}