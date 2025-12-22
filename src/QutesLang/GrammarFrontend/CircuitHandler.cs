using System.Linq;
using System.Text;

namespace QutesLang.GrammarFrontend;

public enum BackendProvider
{
    Qiskit,
}

public class CircuitHandler(BackendProvider backendProvider = BackendProvider.Qiskit) : ICircuitHandler
{
    public IQuantumCircuit Current => circuitsStack.Peek();
    private readonly Stack<IQuantumCircuit> circuitsStack = [];
    private readonly Stack<IQuantumCircuit> circuitsDeclared = [];

    public IQuantumCircuit CreateNewCircuit()
    {
        return new QuantumCircuit();
    }

    public void PushCircuit(IQuantumCircuit circuit)
    {
        circuitsStack.Push(circuit);
        circuitsDeclared.Push(circuit);
    }

    public IQuantumCircuit PopCircuit()
    {
        return circuitsStack.Pop();
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

        foreach (var circuit in circuitsDeclared) // Processed in stack order to maintain correct dependencies
        {
            ((QuantumCircuit)circuit).FinalizeQiskitCircuit(stringBuilder);
        }
        return stringBuilder.ToString();
    }

    public void PushOperation(CircuitOperation operation)
    {
        Current.PushOperation(operation);
    }

    public void DeclareQuantumVariable(string name, QuantumRegister values)
    {
        Current.DeclareQuantumVariable(name, values);
    }

    public void UpdateQuantumVariable(string name, QuantumRegister values)
    {
        Current.UpdateQuantumVariable(name, values);
    }
}

public class ControlledCircuit : QuantumCircuit
{
    private readonly bool onCondition;

    public IQuantumCircuit InnerCircuit { get; private set; }
    public QuantumRegister ControlRegister { get; }
    public override string Name { get; protected set; }

    public override Dictionary<string, QuantumRegister> QuantumVariables => GetQuantumVariables();
    public override ReferenceCounter<QuantumRegister> Registers => GetRegisters();

    public ControlledCircuit(IQuantumCircuit innerCircuit, QuantumRegister controlRegister, bool onCondition = true)
    {
        InnerCircuit = innerCircuit;
        ControlRegister = controlRegister;
        this.onCondition = onCondition;
        Name = "controlled_" + innerCircuit.Name;
        QuantumVariables = new(innerCircuit.QuantumVariables);
        Registers = new(innerCircuit.Registers);
        DeclareQuantumVariable(controlRegister.Name ?? "control", controlRegister);
    }

    public override void FinalizeQiskitCircuit(StringBuilder stringBuilder)
    {
        base.FinalizeQiskitCircuit(stringBuilder);
        var controlBitCount = ControlRegister.Qubits.Count();
        stringBuilder.AppendLine($"{Name} = {InnerCircuit.Name}.control({controlBitCount}, ctrl_state='{new string(onCondition?'1':'0', controlBitCount)}', label='{Name}')");
    }

    private Dictionary<string, QuantumRegister> GetQuantumVariables()
    {
        return new([..InnerCircuit.QuantumVariables.AsEnumerable(), KeyValuePair.Create("", ControlRegister)]);
    }

    private ReferenceCounter<QuantumRegister> GetRegisters()
    {
        var registers = new ReferenceCounter<QuantumRegister>(InnerCircuit.Registers);
        registers.Add(ControlRegister);
        return registers;
    }
}

public class QuantumCircuit : IQuantumCircuit
{
    public virtual string Name { get; protected set; } = VariableNameGuid.New(prefix: "circuit");
    public virtual List<CircuitOperation> Operations { get; protected set; } = [];
    public virtual Dictionary<string, QuantumRegister> QuantumVariables { get; protected set; } = [];
    public virtual ReferenceCounter<QuantumRegister> Registers { get; protected set; } = new();

    public void PushOperation(CircuitOperation operation)
    {
        Operations.Add(operation);
    }

    public IQuantumCircuit MakeControlledBy(QuantumRegister controlRegister, bool onCondition = true)
    {
        return new ControlledCircuit(this, controlRegister, onCondition);
    }

    public void DeclareQuantumVariable(string name, QuantumRegister register)
    {
        if (QuantumVariables.ContainsKey(name))
        {
            throw new InvalidOperationException($"Quantum variable with name {name} already declared.");
        }

        register.Name ??= name;

        Registers.Add(register);
        QuantumVariables[name] = register;
    }

    public void UpdateQuantumVariable(string name, QuantumRegister registerNewValue)
    {
        if (!QuantumVariables.TryGetValue(name, out QuantumRegister? register))
        {
            throw new InvalidOperationException($"Quantum variable with name {name} not declared.");
        }

        QuantumVariables[name] = registerNewValue;
    }

    public virtual void FinalizeQiskitCircuit(StringBuilder stringBuilder)
    {
        // Registers consolidation
        var usedRegister = GetUsedRegister();
        //FreeUnusedRegister(usedRegister); //TODO: not working because not everything is an operation: e.g. if(a) => a never used because no op is associted.
        DeclareMissingRegister(usedRegister); //e.g. registers that where declared in parent circuit

        // Declare qubits
        foreach (var qubit in Registers.Elements.SelectMany(r=>r.Qubits))
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

        // Draw the circuit
        stringBuilder.AppendLine($"print({Name}.draw())");
    }

    private HashSet<QuantumRegister> GetUsedRegister()
    {
        List<QuantumRegister> registerUsed = [];
        foreach (var operation in Operations)
        {
            registerUsed.AddRange(operation.RegistersInvolved);
        }

        return registerUsed.ToHashSet();
    }

    private void FreeUnusedRegister(HashSet<QuantumRegister> qubitsUsed)
    {
        IEnumerable<QuantumRegister> registerDeclared = [..Registers.Elements];
        foreach (var register in registerDeclared)
        {
            if (!qubitsUsed.Contains(register))
            {
                Registers.Remove(register);
            }
        }
    }

    private void DeclareMissingRegister(HashSet<QuantumRegister> usedRegisters)
    {
        foreach (var register in usedRegisters)
        {
            if (!QuantumVariables.ContainsValue(register))
            {
                DeclareQuantumVariable(register.Name!, register);
            }
        }
    }
}