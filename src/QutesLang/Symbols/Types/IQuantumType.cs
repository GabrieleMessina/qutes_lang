using QutesLang.GrammarFrontend;

namespace QutesLang.Symbols.Types;

public interface IQuantumType : IQutesType
{
    public int Size { get; set; }
    public IEnumerable<CircuitQubit?> Qubits { get; set; }
    public string QubitStringList => $"[{string.Join(",", Qubits.Select(c => c!.Id))}]";

    #region Operations
    CircuitOperation LShift(QuintType positions);
    CircuitOperation RShift(QuintType positions);
    CircuitOperation Swap(IQuantumType positions);

    CircuitOperation Addition(IQuantumType term);
    CircuitOperation Subtraction(IQuantumType term);

    CircuitOperation LowerThan(IQuantumType term);
    CircuitOperation LowerEqualThan(IQuantumType term);
    CircuitOperation GreaterThan(IQuantumType term);
    CircuitOperation GreaterEqualThan(IQuantumType term);

    CircuitOperation Equals(IQuantumType positions);
    CircuitOperation NotEquals(IQuantumType positions);

    CircuitOperation And(IQuantumType positions);
    CircuitOperation Or(IQuantumType positions);
    #endregion Operations
}