using System.Text;

namespace QutesLang.GrammarFrontend;

public enum BackendProvider
{
    Qiskit,
}

public class CircuitHandler(BackendProvider backendProvider = BackendProvider.Qiskit) : ICircuitHandler
{
    public QuantumCircuit Current => circuits.Last();
    private readonly Stack<QuantumCircuit> circuits = [];

    public QuantumCircuit CreateNewCircuit()
    {
        var circuit = new QuantumCircuit();
        circuits.Push(circuit);
        return circuit;
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

        foreach (var circuit in circuits) // Processed in reverse order to maintain correct dependencies
        {
            circuit.FinalizeQiskitCircuit();
        }
        return stringBuilder.ToString();
    }

    public void PushOperation(CircuitOperation operation)
    {
        Current.PushOperation(operation);
    }

    public void DeclareQuantumVariable(string name, IEnumerable<CircuitQubit> values)
    {
        Current.DeclareQuantumVariable(name, values);
    }

    public void UpdateQuantumVariable(string name, IEnumerable<CircuitQubit> values)
    {
        Current.UpdateQuantumVariable(name, values);
    }
}
public class QuantumCircuit : IQuantumCircuit
{
    public string Name { get; private set; } = VariableNameGuid.New(prefix: "circuit");
    public List<CircuitOperation> Operations { get; } = [];
    public Dictionary<string, QuantumRegister> QuantumVariables { get; } = [];
    public ReferenceCounter<CircuitQubit> Qubits { get; } = new();
    public IEnumerable<CircuitQubit> ControlQubits { get; private set; } = [];

    public void PushOperation(CircuitOperation operation)
    {
        Operations.Add(operation);
    }

    public void MakeControlledBy(IEnumerable<CircuitQubit> controlQubits)
    {
        ControlQubits = controlQubits;
    }

    public void DeclareQuantumVariable(string name, IEnumerable<CircuitQubit> values)
    {
        if (QuantumVariables.ContainsKey(name))
        {
            throw new InvalidOperationException($"Quantum variable with name {name} already declared.");
        }

        var registerQubits = new HashSet<CircuitQubit>();
        foreach (var value in values)
        {
            registerQubits.Add(value);
            Qubits.Add(value);
        }
        QuantumVariables[name] = new (name, registerQubits);
    }

    public void UpdateQuantumVariable(string name, IEnumerable<CircuitQubit> values)
    {
        if (!QuantumVariables.TryGetValue(name, out QuantumRegister? register))
        {
            throw new InvalidOperationException($"Quantum variable with name {name} not declared.");
        }

        // Remove old qubits from reference counter
        foreach (var qubit in register.Qubits)
        {
            Qubits.Remove(qubit);
        }

        var registerQubits = new HashSet<CircuitQubit>();
        foreach (var value in values)
        {
            registerQubits.Add(value);
            Qubits.Add(value);
        }

        register.Qubits = registerQubits;
    }

    public string FinalizeQiskitCircuit()
    {
        var stringBuilder = new StringBuilder();

        // Registers consolidation
        var usedQubits = GetUsedQubits();
        FreeUnusedQubits(usedQubits);
        DeclareMissingQubits(usedQubits); //e.g. registers that where declared in parent circuit

        // Declare qubits
        foreach (var qubit in Qubits.Elements)
        {
            stringBuilder.AppendLine($"{qubit.Id} = Qubit()");
        }

        // Declare quantum registers
        foreach (var qreg in QuantumVariables.Values)
        {
            var qubitRefs = string.Join(',', qreg.Qubits.Select(q => q.Id));
            stringBuilder.AppendLine($"{qreg.Name} = QuantumRegister(name='{qreg.Name}', bits=[{qubitRefs}])");
        }
        var quantumRegisterNames = string.Join(',', QuantumVariables.Select(qr => qr.Value.Name));
        stringBuilder.AppendLine($"{Name} = QuantumCircuit({quantumRegisterNames})");

        // Apply operations
        foreach (var operation in Operations)
        {
            operation.ApplyToQiskitCircuit(this, stringBuilder);
        }

        if (ControlQubits.Any())
        {
            stringBuilder.AppendLine($"{Name} = {Name}.control({ControlQubits.Count()}, label='controlled_{Name}')");
        }

        // Draw the circuit
        stringBuilder.AppendLine($"print({Name}.draw())");
        return stringBuilder.ToString();
    }

    private HashSet<CircuitQubit> GetUsedQubits()
    {
        List<CircuitQubit> qubitsUsed = [];
        foreach (var operation in Operations)
        {
            qubitsUsed.AddRange(operation.QubitInvolved);
        }
        return qubitsUsed.ToHashSet();
    }

    private void FreeUnusedQubits(HashSet<CircuitQubit> qubitsUsed)
    {
        //TODO: fix, we are deleting qubits but not registers.
        IEnumerable<CircuitQubit> qubitDeclared = [..Qubits.Elements];
        foreach (var qubit in qubitDeclared)
        {
            if (!qubitsUsed.Contains(qubit))
            {
                Qubits.Remove(qubit);
            }
        }
    }
    private void DeclareMissingQubits(HashSet<CircuitQubit> usedRegisters)
    {
        //TODO: we cannot declare a huge register with all this qubits, we need to track which registers where linked to each qubit.
    }
}