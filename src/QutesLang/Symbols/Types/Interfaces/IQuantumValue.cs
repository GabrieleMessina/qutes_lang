using QutesLang.GrammarFrontend;
using QutesLang.GrammarFrontend.Operations;

namespace QutesLang.Symbols.Types.Interfaces;

public interface IQuantumValue : IQutesValue
{
    public int Size { get; }
    public QuantumRegister Register { get; }
    public string QubitStringList => Register.QubitStringList;
    CircuitOperation Addition(IQuantumValue term);
    CircuitOperation And(IQuantumValue term);
    CircuitOperation Divide(IQuantumValue term);
    CircuitOperation Exp(IQuantumValue term);
    CircuitOperation GreaterEqualThan(IQuantumValue term);
    CircuitOperation GreaterThan(IQuantumValue term);
    CircuitOperation InplacePostDecrement();
    CircuitOperation InplacePostIncrement();
    CircuitOperation InplacePreDecrement();
    CircuitOperation InplacePreIncrement();
    CircuitOperation LeftShift(IntValue positions);
    CircuitOperation LeftShift(QuintValue positions);
    CircuitOperation LowerEqualThan(IQuantumValue term);
    CircuitOperation LowerThan(IQuantumValue term);
    CircuitOperation Minus();
    CircuitOperation Module(IQuantumValue term);
    CircuitOperation Multiply(IQuantumValue term);
    CircuitOperation Not();
    CircuitOperation Equals(IQuantumValue term);
    CircuitOperation NotEquals(IQuantumValue term);
    CircuitOperation Or(IQuantumValue term);
    CircuitOperation Plus();
    CircuitOperation RightShift(IntValue positions);
    CircuitOperation RightShift(QuintValue positions);
    CircuitOperation Subtraction(IQuantumValue term);
    CircuitOperation Swap(IQuantumValue term);
}