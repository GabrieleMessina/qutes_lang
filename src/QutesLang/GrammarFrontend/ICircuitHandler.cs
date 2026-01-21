
namespace QutesLang.GrammarFrontend;

public interface ICircuitHandler
{
    IQuantumCircuit Current { get; }
    IQuantumCircuit CreateNewCircuit();
    string FinalizeCircuit();

    void PushOperation(CircuitOperation operation);
    void DeclareQuantumVariable(string name, QuantumRegister values);
    void UpdateQuantumVariable(string name, QuantumRegister values);
    IQuantumCircuit PopCircuit();
    void PushCircuit(IQuantumCircuit circuit);
}

public interface IQuantumCircuit
{
    string Name { get; }
    List<CircuitOperation> Operations { get; }
    Dictionary<string, QuantumRegister> LocalQuantumVariables { get; }
    ReferenceCounter<QuantumRegister> LocalRegisters { get; }

    void PushOperation(CircuitOperation operation);
    void DeclareQuantumVariable(string name, QuantumRegister values);
    void UpdateQuantumVariable(string name, QuantumRegister values);
    IQuantumCircuit MakeControlledBy(QuantumRegister controlRegister, bool onCondition = true);
}