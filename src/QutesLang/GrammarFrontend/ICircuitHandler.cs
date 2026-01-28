
namespace QutesLang.GrammarFrontend;

public interface ICircuitHandler
{
    IQuantumCircuit DeclareNewQuantumGate(IQuantumCircuit? circuit = null);
    string FinalizeProgram(string outputPath);
    IQuantumCircuit DeclareNewQuantumGate(string? name = null, IQuantumCircuit? circuit = null);
    string FinalizeProgram();

    void PushOperation(CircuitOperation operation);
    void DeclareQuantumVariable(string name, QuantumRegister values);
    void UpdateQuantumVariable(string name, QuantumRegister values);
    void AddDependentCircuit(IQuantumCircuit circuit);
    ICircuitContext SetCurrentContext(IQuantumCircuit circuit);
}

public interface IQuantumCircuit
{
    string Name { get; }
    List<CircuitOperation> Operations { get; }
    Dictionary<string, QuantumRegister> LocalQuantumVariables { get; }
    List<QuantumRegister> LocalRegisters { get; }

    void PushOperation(CircuitOperation operation);
    void DeclareQuantumVariable(string name, QuantumRegister values);
    void UpdateQuantumVariable(string name, QuantumRegister registerNewValue);
    IQuantumCircuit MakeControlledBy(QuantumRegister controlRegister, bool onCondition = true);
    void AddDependentCircuit(IQuantumCircuit circuit);
}