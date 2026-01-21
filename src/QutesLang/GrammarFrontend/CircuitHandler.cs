using System.Text;

namespace QutesLang.GrammarFrontend;

public class CircuitHandler(BackendProvider backendProvider = BackendProvider.Qiskit) : ICircuitHandler
{
    public IQuantumCircuit Current => circuitsStack.Peek();
    private readonly Stack<IQuantumCircuit> circuitsStack = [];
    private readonly Stack<IQuantumCircuit> circuitsDeclared = [];

    public IQuantumCircuit CreateNewCircuit()
    {
        return new QuantumCircuit(includeClassicalBits: circuitsStack.Count == 0);  // Include classical bits only in the main circuit
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

    //TODO: better handle circuit that needs local parameter like user defined quantum functions and quantum oracle (e.g. required for grover).
    private string FinalizeQiskitCircuit()
    {
        var stringBuilder = new StringBuilder();

        AppendPythonCode(stringBuilder);

        stringBuilder.AppendLine("from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister");
        stringBuilder.AppendLine("from qiskit.circuit import Qubit");
        stringBuilder.AppendLine("from qiskit.primitives import StatevectorSampler");
        stringBuilder.AppendLine("from qiskit.circuit.library import StatePreparation, ModularAdderGate, grover_operator as GroverOperator");

        stringBuilder.AppendLine("# Operation Requirements");
        foreach (var circuit in circuitsDeclared)
        {
            ((QuantumCircuit)circuit).ApplyQiskitRequirements(stringBuilder);
        }
        DeclareRegistersInvolvedInOperations();

        // Declare qubits
        stringBuilder.AppendLine($"# Qubits declaration");
        foreach (var qubit in Registers.SelectMany(r => r.Qubits))
        {
            stringBuilder.AppendLine($"{qubit.Id} = Qubit()");
        }

        // Declare quantum registers
        stringBuilder.AppendLine($"# Quantum registers declaration");
        foreach (var qreg in Registers)
        {
            var qubitRefs = string.Join(',', qreg.Qubits.Select(q => q.Id));
            stringBuilder.AppendLine($"{qreg.Name} = QuantumRegister(name='{qreg.Name}', bits=[{qubitRefs}])");
            stringBuilder.AppendLine($"{qreg.ClassicalRegister.Name} = ClassicalRegister(size={qreg.ClassicalRegister.Size}, name='{qreg.ClassicalRegister.Name}')");
        }

        foreach (var circuit in circuitsDeclared) // Processed in stack order to maintain correct dependencies
        {
            ((QuantumCircuit)circuit).FinalizeQiskitCircuit(Registers.ToList(), stringBuilder);
        }

        stringBuilder.AppendLine("# Qiskit execution");
        var mainCircuit = circuitsStack.Last();
        var mainCircuitName = mainCircuit.Name;
        stringBuilder.AppendLine("sampler = StatevectorSampler()");
        stringBuilder.AppendLine($"result = sampler.run([{mainCircuitName}], shots={CompilerFlags.Current.NumberOfIterations}).result()");
        
        var measuredVars = circuitsStack.SelectMany(c => c.Operations).Where(o => o is Measure).Select(m => m.Destination);

        string VarNames = string.Join(", ", measuredVars.Select(qv => $"'{qv.Register.Name}'"));
        string VarSizes = string.Join(", ", measuredVars.Select(qv => $"'{qv.Register.Name}': {qv.Register.Qubits.Count}"));
        string VarToClreg = string.Join(", ", measuredVars.Select(qv => $"'{qv.Register.Name}': '{qv.Register.ClassicalRegister.Name}'"));

        stringBuilder.AppendLine("# Result pretty print");
        stringBuilder.AppendLine($"var_names = [{VarNames}]");
        stringBuilder.AppendLine($"var_sizes = {{{VarSizes}}}");
        stringBuilder.AppendLine($"var_to_clreg = {{{VarToClreg}}}");
        stringBuilder.AppendLine("print_pretty_results_mapped(result, var_names, var_sizes, var_to_clreg)");

        return stringBuilder.ToString();
    }

    public void PushOperation(CircuitOperation operation)
    {
        Current.PushOperation(operation);
    }

    public virtual Dictionary<string, QuantumRegister> QuantumVariables { get; protected set; } = [];
    public virtual ReferenceCounter<QuantumRegister> Registers { get; protected set; } = [];

    private void DeclareRegistersInvolvedInOperations()
    {
        // Registers consolidation
        var usedRegister = GetUsedRegister();
        //FreeUnusedRegister(usedRegister); //TODO: not working because not everything is an operation: e.g. if(a) => a never used because no op is associted.
        DeclareMissingRegister(usedRegister); //e.g. registers that where declared in parent circuit
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
        Current.DeclareQuantumVariable(name, register);
    }

    public void UpdateQuantumVariable(string name, QuantumRegister registerNewValue)
    {
        if (!QuantumVariables.TryGetValue(name, out QuantumRegister? register))
        {
            throw new InvalidOperationException($"Quantum variable with name {name} not declared.");
        }

        Registers.Remove(register);
        Registers.Add(registerNewValue);
        QuantumVariables[name] = registerNewValue;
        Current.UpdateQuantumVariable(name, register);
    }

    private static void AppendPythonCode(StringBuilder stringBuilder)
    {
        var tabularPrint = File.ReadAllText(Path.Combine(Environment.CurrentDirectory, "PythonCode", "PrintTabularStateVectorResults.py"));
        var qutesGate = File.ReadAllText(Path.Combine(Environment.CurrentDirectory, "PythonCode", "QutesGates.py"));
        stringBuilder.AppendLine(tabularPrint);
        stringBuilder.AppendLine();
        stringBuilder.AppendLine(qutesGate);
        stringBuilder.AppendLine();
    }

    private HashSet<QuantumRegister> GetUsedRegister()
    {
        List<QuantumRegister> registerUsed = [];
        foreach (var operation in circuitsDeclared.SelectMany(c => c.Operations))
        {
            registerUsed.AddRange(operation.RegistersInvolved);
        }

        return registerUsed.ToHashSet();
    }

    private void FreeUnusedRegister(HashSet<QuantumRegister> qubitsUsed)
    {
        IEnumerable<QuantumRegister> registerDeclared = [.. Registers];
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
                DeclareQuantumVariable(register.Name ?? VariableNameGuid.New("ancilla"), register);
            }
        }
    }
}

public class ControlledCircuit : QuantumCircuit
{
    private readonly bool onCondition;

    public IQuantumCircuit InnerCircuit { get; private set; }
    public QuantumRegister ControlRegister { get; }
    public override string Name { get; protected set; }

    public override Dictionary<string, QuantumRegister> LocalQuantumVariables => GetQuantumVariables();
    public override ReferenceCounter<QuantumRegister> LocalRegisters => GetRegisters();

    public ControlledCircuit(IQuantumCircuit innerCircuit, QuantumRegister controlRegister, bool onCondition = true)
    {
        InnerCircuit = innerCircuit;
        ControlRegister = controlRegister;
        this.onCondition = onCondition;
        Name = "controlled_" + innerCircuit.Name;
        LocalQuantumVariables = new(innerCircuit.LocalQuantumVariables);
        LocalRegisters = [..innerCircuit.LocalRegisters];
        DeclareQuantumVariable(controlRegister.Name ?? "control", controlRegister);
    }

    public override void FinalizeQiskitCircuit(ICollection<QuantumRegister> alreadyDeclaredRegisters, StringBuilder stringBuilder)
    {
        base.FinalizeQiskitCircuit(alreadyDeclaredRegisters, stringBuilder);
        var controlBitCount = ControlRegister.Qubits.Count;
        stringBuilder.AppendLine($"{Name} = {InnerCircuit.Name}.control({controlBitCount}, ctrl_state='{new string(onCondition?'1':'0', controlBitCount)}', label='{Name}')");
    }

    private Dictionary<string, QuantumRegister> GetQuantumVariables()
    {
        return new([..InnerCircuit.LocalQuantumVariables.AsEnumerable(), KeyValuePair.Create("", ControlRegister)]);
    }

    private ReferenceCounter<QuantumRegister> GetRegisters()
    {
        var registers = new ReferenceCounter<QuantumRegister>(InnerCircuit.LocalRegisters)
        {
            ControlRegister
        };
        return registers;
    }
}

public class QuantumCircuit(bool includeClassicalBits = false) : IQuantumCircuit
{
    public virtual string Name { get; protected set; } = VariableNameGuid.New(prefix: "circuit");
    public virtual List<CircuitOperation> Operations { get; protected set; } = [];
    public virtual Dictionary<string, QuantumRegister> LocalQuantumVariables { get; protected set; } = [];
    public virtual ReferenceCounter<QuantumRegister> LocalRegisters { get; protected set; } = [];
    public bool IncludeClassicalBits { get; } = includeClassicalBits; //Some circuits (sub-circuits) may not need classical bits, e.g. circuits that should be composed with GroverOperator since GroverOperator doesn't allow coposition with circuit with classical registers.

    private void DeclareRegistersInvolvedInOperations()
    {
        // Registers consolidation
        var usedRegister = GetUsedRegister();
        //FreeUnusedRegister(usedRegister); //TODO: not working because not everything is an operation: e.g. if(a) => a never used because no op is associted. Actually this should be an equality operation so it should work.
        DeclareMissingRegister(usedRegister); //e.g. registers that where declared in parent circuit
    }

    public void PushOperation(CircuitOperation operation)
    {
        Operations.Add(operation); // Always add the operation, even if it's a composition, some logic can be handled by it.
        if (operation is Composition composition)
        {
            foreach (var part in composition.CircuitOperations)
            {
                PushOperation(part); // Handle nested compositions
            }
        }
    }

    public IQuantumCircuit MakeControlledBy(QuantumRegister controlRegister, bool onCondition = true)
    {
        return new ControlledCircuit(this, controlRegister, onCondition);
    }

    public void DeclareQuantumVariable(string name, QuantumRegister register)
    {
        if (LocalQuantumVariables.ContainsKey(name))
        {
            throw new InvalidOperationException($"Quantum variable with name {name} already declared.");
        }

        register.Name ??= name;

        LocalRegisters.Add(register);
        LocalQuantumVariables[name] = register;
    }

    public void UpdateQuantumVariable(string name, QuantumRegister registerNewValue)
    {
        if (!LocalQuantumVariables.TryGetValue(name, out QuantumRegister? register))
        {
            throw new InvalidOperationException($"Quantum variable with name {name} not declared.");
        }

        LocalRegisters.Remove(register);
        LocalRegisters.Add(registerNewValue);
        LocalQuantumVariables[name] = registerNewValue;
    }

    public virtual void ApplyQiskitRequirements(StringBuilder stringBuilder)
    {
        foreach (var operation in Operations)
        {
            operation.ApplyQiskitRequirements(stringBuilder);
        }
    }

    public virtual void FinalizeQiskitCircuit(ICollection<QuantumRegister> globalRegisters, StringBuilder stringBuilder)
    {
        stringBuilder.AppendLine($"# ================ Circuit {Name} =====================");

        DeclareRegistersInvolvedInOperations();

        // Declare local qubits
        stringBuilder.AppendLine($"# Qubits declaration for {Name}");
        foreach (var qubit in LocalRegisters.SelectMany(r => r.Qubits))
        {
            stringBuilder.AppendLine($"{qubit.Id} = Qubit()");
        }

        // Declare local quantum registers
        stringBuilder.AppendLine($"# Quantum registers declaration for {Name}");
        foreach (var qreg in LocalRegisters)
        {
            var qubitRefs = string.Join(',', qreg.Qubits.Select(q => q.Id));
            stringBuilder.AppendLine($"{qreg.Name} = QuantumRegister(name='{qreg.Name}', bits=[{qubitRefs}])");
            stringBuilder.AppendLine($"{qreg.ClassicalRegister.Name} = ClassicalRegister(size={qreg.ClassicalRegister.Size}, name='{qreg.ClassicalRegister.Name}')");
        }
        var quantumRegisterNames = string.Join(',', globalRegisters.Select(qr => qr.Name));
        var classicalRegisterNames = string.Join(',', globalRegisters.Select(qr => qr.ClassicalRegister.Name).Where(name => name != null));

        // Declare circuit
        stringBuilder.AppendLine($"# Circuit declaration: {Name}");
        if (IncludeClassicalBits)
        {
            stringBuilder.AppendLine($"{Name} = QuantumCircuit({quantumRegisterNames}, {classicalRegisterNames})");
        }
        else
        {
            stringBuilder.AppendLine($"{Name} = QuantumCircuit({quantumRegisterNames})");
        }

        if (IncludeClassicalBits)//TODO: add another bool to check whether state preparation must be done for this circuit.
        {
            // Initialize qubits to desired state
            stringBuilder.AppendLine($"# Register initialization for {Name}");
            var registersToInitialize = LocalRegisters
            .SelectMany(q => q.Registers ?? [q]) // If no sub-registers(qreg is not an array), use the register itself
            .Distinct();
            foreach (var qreg in registersToInitialize)
            {
                var initialState = qreg.InitialStateVector;
                if (initialState != null)
                {
                    new StatePreparation(qreg, initialState).ApplyToQiskitCircuit(this, stringBuilder);
                }
            }
        }

        // Apply operations
        foreach (var operation in Operations)
        {
            stringBuilder.AppendLine($"# Operation: {operation.GetType().Name}");
            operation.ApplyToQiskitCircuit(this, stringBuilder);
        }

        // Print or save circuit image if required
        stringBuilder.AppendLine($"# Print for circuit {Name}");
        PrintCircuit(Name, stringBuilder);
        SaveCircuitImage(Name, stringBuilder);
        stringBuilder.AppendLine();
    }

    public static void PrintCircuit(string circuitName, StringBuilder stringBuilder, int decomposeLevel = 0)
    {
        if (!CompilerFlags.Current.PrintQuantumCircuit)
        {
            return;
        }
        stringBuilder.AppendLine($"print({circuitName}.decompose(reps={decomposeLevel}).draw())");
    }

    public static void SaveCircuitImage(string circuitName, StringBuilder stringBuilder, int decomposeLevel = 0)
    {
        if (!CompilerFlags.Current.CreateQuantumCircuitImage)
        {
            return;
        }

        var timestamp = DateTime.Now.ToString("yyyyMMdd_HHmmss");
        var filePath = $"{Path.Combine(CompilerFlags.Current.OutputPath, circuitName)}_{timestamp}.png";
        stringBuilder.AppendLine($"{circuitName}.decompose(reps={decomposeLevel}).draw(output='mpl', filename='{filePath}', style='iqp', fold=1000)");
        stringBuilder.AppendLine($"print('Quantum circuit image saved to: {filePath}')");
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
        IEnumerable<QuantumRegister> registerDeclared = [..LocalRegisters];
        foreach (var register in registerDeclared)
        {
            if (!qubitsUsed.Contains(register))
            {
                LocalRegisters.Remove(register);
            }
        }
    }

    private void DeclareMissingRegister(HashSet<QuantumRegister> usedRegisters)
    {
        foreach (var register in usedRegisters)
        {
            if (!LocalQuantumVariables.ContainsValue(register))
            {
                DeclareQuantumVariable(register.Name ?? VariableNameGuid.New("ancilla"), register);
            }
        }
    }
}