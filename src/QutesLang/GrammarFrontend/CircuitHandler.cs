using System.Text;

namespace QutesLang.GrammarFrontend;

public class CircuitHandler(BackendProvider backendProvider = BackendProvider.Qiskit) : IQuantumCircuitHandler
{
    private readonly List<CircuitOperation> operations = [];
    private readonly Dictionary<string, QuantumRegister> quantumRegisters = [];
    private readonly ReferenceCounter<CircuitQubit> circuitQubits = new();

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

        var registerQubits = new HashSet<CircuitQubit>();
        foreach (var value in values)
        {
            var qubit = new CircuitQubit();
            registerQubits.Add(value ?? qubit);
            circuitQubits.Add(value ?? qubit);
        }
        quantumRegisters[name] = new (name, registerQubits);
        return registerQubits;
    }

    public IEnumerable<CircuitQubit> UpdateQuantumRegister(string name, IEnumerable<CircuitQubit?> values)
    {
        if (!quantumRegisters.TryGetValue(name, out QuantumRegister? register))
        {
            throw new InvalidOperationException($"Quantum register with name {name} not declared.");
        }

        // Remove old qubits from reference counter
        foreach (var qubit in register.Qubits)
        {
            circuitQubits.Remove(qubit);
        }

        var registerQubits = new HashSet<CircuitQubit>();
        foreach (var value in values)
        {
            var qubit = new CircuitQubit();
            registerQubits.Add(value ?? qubit);
            circuitQubits.Add(value ?? qubit);
        }

        register.Qubits = registerQubits;
        return registerQubits;
    }

    public string FinalizeCircuit()
    {
        return backendProvider switch
        {
            BackendProvider.Qiskit => FinalizeQiskitCircuit(),
            _ => throw new NotImplementedException($"Backend provider {backendProvider} is not supported."),
        };
    }

    private string FinalizeQiskitCircuit()
    {
        var stringBuilder = new StringBuilder();
        stringBuilder.AppendLine("from qiskit import QuantumCircuit, QuantumRegister");
        stringBuilder.AppendLine("from qiskit.circuit import Qubit");
        stringBuilder.AppendLine("from qiskit.primitives import StatevectorSampler");

        // Declare qubits
        foreach (var qubit in circuitQubits.Elements)
        {
            stringBuilder.AppendLine($"{qubit.Id} = Qubit()");
        }

        // Declare quantum registers
        foreach (var qreg in quantumRegisters.Values)
        {
            var qubitRefs = string.Join(',', qreg.Qubits.Select(q => q.Id));
            stringBuilder.AppendLine($"{qreg.Name} = QuantumRegister(name='{qreg.Name}', bits=[{qubitRefs}])");
        }
        var quantumRegisterNames = string.Join(',', quantumRegisters.Select(qr => qr.Value.Name));
        stringBuilder.AppendLine($"circuit = QuantumCircuit({quantumRegisterNames})");

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