using System.Text;

using QutesLang.QuantumCircuits.Operations;
using QutesLang.QuantumCircuits.Interfaces;

namespace QutesLang.QuantumCircuits;

public interface ICircuitContext : IDisposable
{
}

public class CircuitContext(IQuantumCircuit circuit, IQuantumCircuit parentCircuit) : ICircuitContext
{
    public Action<IQuantumCircuit, IQuantumCircuit>? OnDispose { get; set; }

    public void Dispose()
    {
        OnDispose?.Invoke(circuit, parentCircuit);
    }
}

public class CircuitHandler : ICircuitHandler
{
    private readonly QuantumCircuit MainCircuit;
    private readonly Stack<IQuantumCircuit> CircuitsDeclared = [];
    private readonly BackendProvider BackendProvider;
    private IQuantumCircuit CurrentCircuit;

    public CircuitHandler(BackendProvider backendProvider = BackendProvider.Qiskit)
    {
        this.BackendProvider = backendProvider;
        MainCircuit = new(backendProvider, name: "main", includeClassicalBits: true, handleStatePreparation: true);
        CurrentCircuit = MainCircuit;
        CircuitsDeclared.Push(MainCircuit);
    }

    public string FinalizeProgram(string outputPath)
    {
        return BackendProvider switch
        {
            BackendProvider.Qiskit => FinalizeQiskitProgram(outputPath),
            _ => throw new NotImplementedException($"Backend provider {BackendProvider} is not supported."),
        };
    }

    private string FinalizeQiskitProgram(string outputPath)
    {
        var stringBuilderMain = new StringBuilder();
        var stringBuilderLib = new StringBuilder();

        // Library code
        stringBuilderLib.AppendLine("# Auto-generated Qiskit code from QutesLang");
        AppendPythonCode(stringBuilderLib);
        File.WriteAllText(Path.Combine(outputPath, "QutesLib.py"), stringBuilderLib.ToString());

        // Main program
        stringBuilderMain.AppendLine("from QutesLib import *");
        stringBuilderMain.AppendLine("from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister");
        stringBuilderMain.AppendLine("from qiskit.circuit import Qubit");
        stringBuilderMain.AppendLine("from qiskit.primitives import StatevectorSampler");
        stringBuilderMain.AppendLine("from qiskit.circuit.library import StatePreparation, ModularAdderGate, MultiplierGate, OrGate, AndGate, grover_operator as GroverOperator");

        // in python, check that image folder exists or create it.
        stringBuilderMain.AppendLine("import os");
        stringBuilderMain.AppendLine($"os.makedirs(r'{CompilerFlags.Current.CircuitImagesFolder}', exist_ok=True)");

        stringBuilderMain.AppendLine("# Operation Requirements");
        foreach (var circuit in CircuitsDeclared)
        {
            ((QuantumCircuit)circuit).ApplyQiskitRequirements(stringBuilderMain);
        }

        MainCircuit.FinalizeQiskitCircuit([], stringBuilderMain); // Finalize main circuit

        stringBuilderMain.AppendLine("# Qiskit execution");
        stringBuilderMain.AppendLine("sampler = StatevectorSampler()");
        stringBuilderMain.AppendLine($"result = sampler.run([{MainCircuit.Name}], shots={CompilerFlags.Current.NumberOfIterations}).result()");

        var measuredVars = MainCircuit.Operations.Where(o => o is Measure).Select(m => m.Destination);

        string VarNames = string.Join(", ", measuredVars.Select(qv => $"'{qv.Register.Name}'"));
        string VarSizes = string.Join(", ", measuredVars.Select(qv => $"'{qv.Register.Name}': {qv.Register.Qubits.Count}"));
        string VarToClreg = string.Join(", ", measuredVars.Select(qv => $"'{qv.Register.Name}': '{qv.Register.ClassicalRegister.Name}'"));

        stringBuilderMain.AppendLine("# Result pretty print");
        stringBuilderMain.AppendLine($"var_names = [{VarNames}]");
        stringBuilderMain.AppendLine($"var_sizes = {{{VarSizes}}}");
        stringBuilderMain.AppendLine($"var_to_clreg = {{{VarToClreg}}}");
        stringBuilderMain.AppendLine("print_pretty_results_mapped(result, var_names, var_sizes, var_to_clreg)");

        var outputCode = stringBuilderMain.ToString();
        File.WriteAllText(Path.Combine(outputPath, "output.py"), outputCode);
        return outputCode;
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

    public ICircuitContext SetCurrentContext(IQuantumCircuit circuit)
    {
        var context = new CircuitContext(circuit, CurrentCircuit)
        {
            OnDispose = (disposedCircuit, parentCircuit) =>
            {
                CurrentCircuit = parentCircuit;
            }
        };
        CurrentCircuit = circuit;
        return context;
    }

    public IQuantumCircuit DeclareNewQuantumGate(string? name = null, IQuantumCircuit? circuit = null)
    {
        var newCircuit = circuit ?? new QuantumCircuit(BackendProvider, name);
        CircuitsDeclared.Push(newCircuit);
        return newCircuit;
    }

    public void PushOperation(CircuitOperation operation)
    {
        CurrentCircuit.PushOperation(operation);
    }

    public void DeclareQuantumVariable(string name, QuantumRegister values)
    {
        CurrentCircuit.DeclareQuantumVariable(name, values);
    }

    public void UpdateQuantumVariable(string name, QuantumRegister values)
    {
        CurrentCircuit.UpdateQuantumVariable(name, values);
    }

    public void AddDependentCircuit(IQuantumCircuit circuit)
    {
        CurrentCircuit.AddDependentCircuit(circuit);
    }
}

public class QuantumCircuit(BackendProvider backendProvider, string? name = null, bool includeClassicalBits = false, bool handleStatePreparation = false) : IQuantumCircuit
{
    public virtual string Name { get; protected set; } = name ?? VariableNameGuid.New(prefix: "circuit");
    public virtual List<IQuantumCircuit> DependentCircuits { get; protected set; } = [];
    public virtual List<CircuitOperation> Operations { get; protected set; } = [];
    public virtual Dictionary<string, QuantumRegister> LocalQuantumVariables { get; protected set; } = [];
    public virtual List<QuantumRegister> LocalRegisters => Operations.SelectMany(op => op.RegistersInvolved).Distinct().ToList();
    public BackendProvider BackendProvider { get; } = backendProvider;
    public bool IncludeClassicalBits { get; } = includeClassicalBits; //Some circuits (sub-circuits) may not need classical bits, e.g. circuits that should be composed with GroverOperator since GroverOperator doesn't allow coposition with circuit with classical registers.
    public bool HandleStatePreparation { get; } = handleStatePreparation;

    public void AddDependentCircuit(IQuantumCircuit circuit)
    {
        if (!DependentCircuits.Contains(circuit))
        {
            DependentCircuits.Add(circuit);
        }
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
        return new ControlledCircuit(BackendProvider, this, controlRegister, onCondition, IncludeClassicalBits);
    }

    public void DeclareQuantumVariable(string name, QuantumRegister register)
    {
        var registerName = this.Name + "_" + name;
        if (LocalQuantumVariables.ContainsKey(registerName))
        {
            throw new InvalidOperationException($"Quantum variable with name {name} already declared.");
        }

        register.Name = registerName; //Make sure the register name is unique by prefixing it with circuit name.
        LocalRegisters.Add(register);
        LocalQuantumVariables[registerName] = register;
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

    public virtual void FinalizeQiskitCircuit(ICollection<QuantumRegister> alreadyDeclaredRegisters, StringBuilder stringBuilder)
    {
        stringBuilder.AppendLine($"# ================ Circuit {Name} =====================");

        var Registers =
            LocalRegisters
                .Union(DependentCircuits.SelectMany(c => c.LocalRegisters))
                .DistinctBy(r => r.Name)
                .ToList(); //TODO: right now all registers of dependent circuits are included, with the new implementation composition happens on different registers, so this is useless.

        // Declare qubits
        stringBuilder.AppendLine($"# Qubits declaration for {Name}");
        foreach (var qubit in Registers.Except(alreadyDeclaredRegisters).SelectMany(r => r.Qubits))
        {
            stringBuilder.AppendLine($"{qubit.Id} = Qubit()");
        }

        // Declare quantum registers
        stringBuilder.AppendLine($"# Quantum registers declaration for {Name}");
        foreach (var qreg in Registers.Except(alreadyDeclaredRegisters))
        {
            var qubitRefs = string.Join(',', qreg.Qubits.Select(q => q.Id));
            stringBuilder.AppendLine($"{qreg.Name} = QuantumRegister(name='{qreg.Name}', bits=[{qubitRefs}])");
            stringBuilder.AppendLine($"{qreg.ClassicalRegister.Name} = ClassicalRegister(size={qreg.ClassicalRegister.Size}, name='{qreg.ClassicalRegister.Name}')");
        }

        // Declare dependent circuit/gate/oracles
        foreach (var circuit in DependentCircuits)
        {
            switch (BackendProvider)
            {
                case BackendProvider.Qiskit:
                    ((QuantumCircuit)circuit).FinalizeQiskitCircuit(Registers, stringBuilder);
                    break;
                default:
                    break;
            }
        }

        var quantumRegisterNames = string.Join(',', Registers.Select(qr => qr.Name));
        var classicalRegisterNames = string.Join(',', Registers.Select(qr => qr.ClassicalRegister.Name).Where(name => name != null));

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

        if (HandleStatePreparation)
        {
            // Initialize qubits to desired state
            stringBuilder.AppendLine($"# Register initialization for {Name}");
            var registersToInitialize = Registers
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
        var filePath = $"{Path.Combine(CompilerFlags.Current.CircuitImagesFolder, circuitName)}_{timestamp}.png"; //TODO: maybe the timestamp should be taken from python so that same code different runs have different timestamp.
        filePath = filePath.Replace("\\", "/"); // For windows paths in python
        stringBuilder.AppendLine($"{circuitName}.decompose(reps={decomposeLevel}).draw(output='mpl', filename='{filePath}', style='iqp', fold=1000)");
        stringBuilder.AppendLine($"print('Quantum circuit image saved to: {filePath}')");
    }
}

public class ControlledCircuit : QuantumCircuit
{
    private readonly bool onCondition;

    public IQuantumCircuit InnerCircuit { get; private set; }
    public QuantumRegister ControlRegister { get; }
    public override string Name { get; protected set; }

    public override Dictionary<string, QuantumRegister> LocalQuantumVariables => GetQuantumVariables();
    public override List<QuantumRegister> LocalRegisters => GetRegisters();

    public ControlledCircuit(BackendProvider backendProvider, IQuantumCircuit innerCircuit, QuantumRegister controlRegister, bool onCondition = true, bool includeClassicalBits = false) : base(backendProvider, "controlled_" + innerCircuit.Name, includeClassicalBits)
    {
        InnerCircuit = innerCircuit;
        ControlRegister = controlRegister;
        this.onCondition = onCondition;
        Name = "controlled_" + innerCircuit.Name;
        LocalQuantumVariables = new(innerCircuit.LocalQuantumVariables);
        DeclareQuantumVariable(controlRegister.Name ?? "control", controlRegister);
    }

    public override void FinalizeQiskitCircuit(ICollection<QuantumRegister> alreadyDeclaredRegisters, StringBuilder stringBuilder)
    {
        base.FinalizeQiskitCircuit(alreadyDeclaredRegisters, stringBuilder);
        var controlBitCount = ControlRegister.Qubits.Count;
        stringBuilder.AppendLine($"{Name} = {InnerCircuit.Name}.control({controlBitCount}, ctrl_state='{new string(onCondition ? '1' : '0', controlBitCount)}', label='{Name}')");
    }

    private Dictionary<string, QuantumRegister> GetQuantumVariables()
    {
        return new([KeyValuePair.Create("control_" + InnerCircuit.Name, ControlRegister), .. InnerCircuit.LocalQuantumVariables.AsEnumerable()]);
    }

    private List<QuantumRegister> GetRegisters()
    {
        return [ControlRegister, .. InnerCircuit.LocalRegisters]; //order is important for circuit composition, where control register must be first.
    }
}