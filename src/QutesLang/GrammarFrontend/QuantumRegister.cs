namespace QutesLang.GrammarFrontend;

public class QuantumRegister(string name, IEnumerable<CircuitQubit> qubits)
{
    public string Name { get; } = name;
    public IEnumerable<CircuitQubit> Qubits { get; } = qubits;
}
