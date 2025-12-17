using QutesLang.GrammarFrontend;

namespace QutesLang.Symbols.Types;

public interface IClassicalType : IQutesType
{
    public abstract object GetValueAsObject();

    #region Operations
    IQutesType LShift(IntType positions);
    IQutesType RShift(IntType positions);
    IQutesType Swap(IClassicalType positions);

    IQutesType Addition(IClassicalType term);
    IQutesType Subtraction(IClassicalType term);

    BoolType LowerThan(IClassicalType term);
    BoolType LowerEqualThan(IClassicalType term);
    BoolType GreaterThan(IClassicalType term);
    BoolType GreaterEqualThan(IClassicalType term);

    BoolType Equals(IClassicalType term);
    BoolType NotEquals(IClassicalType term);

    BoolType And(IClassicalType term);
    BoolType Or(IClassicalType term);
    #endregion Operations
}