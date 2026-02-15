namespace QutesLang.QuantumCircuits;

public class ClassicalRegister(QuantumRegister quantumRegister)
{
    public string Name => $"c_{QuantumRegister.Name}";
    public int Size { get; set; } = quantumRegister.Qubits.Count;
    public QuantumRegister QuantumRegister { get; } = quantumRegister;
}
