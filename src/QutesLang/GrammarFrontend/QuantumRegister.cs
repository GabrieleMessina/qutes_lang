namespace QutesLang.GrammarFrontend;

public class QuantumRegister
{
    public QuantumRegister(int size, string? name = null)
    {
        Name = name;
        Qubits = Enumerable.Range(0, size).Select(i => new CircuitQubit()).ToList(); //ToList is important here.
    }

    public QuantumRegister(IEnumerable<CircuitQubit> qubits, string? name = null)
    {
        Name = name;
        Qubits = qubits;
    }

    public string? Name { get; set; }
    public IEnumerable<CircuitQubit> Qubits { get; }
}
