using System.Text;

namespace QutesLang.GrammarFrontend;

public class CircuitHandler(BackendProvider backendProvider = BackendProvider.Qiskit) : IQuantumCircuitHandler
{
    private readonly List<CircuitOperation> operations = [];
    private readonly Dictionary<string, QuantumRegister> quantumRegisters = [];
    private readonly List<CircuitQubit> circuitQubits = [];

    public void PushOperation(CircuitOperation operation)
    {
        operations.Add(operation);
    }

    public IEnumerable<CircuitQubit> DeclareQuantumRegister(string name, IEnumerable<CircuitQubit?> values)
    {
        if (quantumRegisters.ContainsKey(name))
        {
            throw new InvalidOperationException($"Quantum register with name {name} already declared.");
        }

        var registerQubits = new List<CircuitQubit>();
        foreach (var value in values)
        {
            if(value == null)
            {
                var qubit = new CircuitQubit();
                circuitQubits.Add(qubit);
                registerQubits.Add(qubit);
            }
            else
            {
                registerQubits.Add(value);
            }
        }
        quantumRegisters[name] = new (name, registerQubits);
        return registerQubits;
    }

    public string FinalizeCircuit()
    {
        switch (backendProvider)
        {
            case BackendProvider.Qiskit:
                return FinalizeQiskitCircuit();
            default:
                throw new NotImplementedException($"Backend provider {backendProvider} is not supported.");
        }
    }

    private string FinalizeQiskitCircuit()
    {
        var stringBuilder = new StringBuilder();
        stringBuilder.AppendLine("from qiskit import QuantumCircuit");

        // Declare qubits
        foreach (var qubit in circuitQubits)
        {
            stringBuilder.AppendLine($"{qubit.Id} = Qubit()");
        }

        // Declare quantum registers
        foreach (var qreg in quantumRegisters.Values)
        {
            var qubitRefs = string.Join(',', qreg.Qubits.Select(q => q.Id));
            stringBuilder.AppendLine($"{qreg.Name} = QuantumRegister({qreg.Name}, {qubitRefs})");
        }
        var quantumRegisterNames = string.Join(',', quantumRegisters.Select(qr => qr.Value.Name));
        stringBuilder.AppendLine($"circuit = QuantumCircuit([{quantumRegisterNames}])");

        // Apply operations
        foreach (var operation in operations)
        {
            operation.ApplyToQiskitCircuit(stringBuilder);
        }

        // Draw the circuit
        stringBuilder.AppendLine("print(circuit.draw())");
        return stringBuilder.ToString();
    }
}

public enum BackendProvider
{
    Qiskit,
}