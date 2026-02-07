using QutesLang.GrammarFrontend;
using QutesLang.GrammarFrontend.Operations;

namespace QutesLang.Symbols.Types.Interfaces;

public interface IQuantumValue : IQutesValue
{
    public int Size { get; }
    public QuantumRegister Register { get; }
    public string QubitStringList => Register.QubitStringList;
    CircuitOperation Addition(IQutesValue term);
    CircuitOperation And(IQutesValue term);
    CircuitOperation Divide(IQutesValue term);
    CircuitOperation Exp(IQutesValue term);
    CircuitOperation GreaterEqualThan(IQutesValue term);
    CircuitOperation GreaterThan(IQutesValue term);
    CircuitOperation InplacePostDecrement();
    CircuitOperation InplacePostIncrement();
    CircuitOperation InplacePreDecrement();
    CircuitOperation InplacePreIncrement();
    CircuitOperation LeftShift(IQutesValue positions);
    CircuitOperation LowerEqualThan(IQutesValue term);
    CircuitOperation LowerThan(IQutesValue term);
    CircuitOperation Minus();
    CircuitOperation Module(IQutesValue term);
    CircuitOperation Multiply(IQutesValue term);
    CircuitOperation Not();
    CircuitOperation Equals(IQutesValue term);
    CircuitOperation NotEquals(IQutesValue term);
    CircuitOperation Or(IQutesValue term);
    CircuitOperation Plus();
    CircuitOperation RightShift(IQutesValue positions);
    CircuitOperation Subtraction(IQutesValue term);
    CircuitOperation Swap(IQutesValue term);
}