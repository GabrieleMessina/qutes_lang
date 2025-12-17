
namespace QutesLang.GrammarFrontend;

public interface IQuantumCircuitHandler
{
    void PushOperation(CircuitOperation operation);
    string FinalizeCircuit();
    IEnumerable<CircuitQubit> DeclareQuantumRegister(string name, IEnumerable<CircuitQubit?> values);
}