
namespace QutesLang.GrammarFrontend;

public interface ICircuitHandler
{
    public QuantumCircuit Current { get; }
    QuantumCircuit CreateNewCircuit();
    string FinalizeCircuit();

    void PushOperation(CircuitOperation operation);
    void DeclareQuantumVariable(string name, IEnumerable<CircuitQubit> values);
    void UpdateQuantumVariable(string name, IEnumerable<CircuitQubit> values);
}

public interface IQuantumCircuit
{
    public string Name { get; }
    List<CircuitOperation> Operations { get; }
    public Dictionary<string, QuantumRegister> QuantumVariables { get; }
    public ReferenceCounter<CircuitQubit> Qubits { get; }
    void PushOperation(CircuitOperation operation);
    void DeclareQuantumVariable(string name, IEnumerable<CircuitQubit> values);
    void UpdateQuantumVariable(string name, IEnumerable<CircuitQubit> values);
    void MakeControlledBy(IEnumerable<CircuitQubit> controlQubits);
}