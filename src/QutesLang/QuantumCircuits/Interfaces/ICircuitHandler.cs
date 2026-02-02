using QutesLang.GrammarFrontend;
using QutesLang.GrammarFrontend.Operations;

namespace QutesLang.QuantumCircuits.Interfaces;

public interface ICircuitHandler
{
    IQuantumCircuit DeclareNewQuantumGate(string? name = null, IQuantumCircuit? circuit = null);
    string FinalizeProgram(string outputPath);
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