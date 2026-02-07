namespace QutesLang.Symbols.Types.Interfaces;

public interface IOperableValue : IQutesValue
{
    QutesResult Addition(IQutesValue term);
    QutesResult And(IQutesValue term);
    QutesResult CNot(IQutesValue term);
    QutesResult Divide(IQutesValue term);
    QutesResult Equals(IQutesValue term);
    QutesResult Exp(IQutesValue term);
    QutesResult GreaterEqualThan(IQutesValue term);
    QutesResult GreaterThan(IQutesValue term);
    QutesResult InplacePostDecrement();
    QutesResult InplacePostIncrement();
    QutesResult InplacePreDecrement();
    QutesResult InplacePreIncrement();
    QutesResult LeftShift(IQutesValue positions);
    QutesResult LowerEqualThan(IQutesValue term);
    QutesResult LowerThan(IQutesValue term);
    QutesResult Minus();
    QutesResult Module(IQutesValue term);
    QutesResult Multiply(IQutesValue term);
    QutesResult Not();
    QutesResult NotEquals(IQutesValue term);
    QutesResult Or(IQutesValue term);
    QutesResult Plus();
    QutesResult RightShift(IQutesValue positions);
    QutesResult Subtraction(IQutesValue term);
    QutesResult Swap(IQutesValue term);
}
