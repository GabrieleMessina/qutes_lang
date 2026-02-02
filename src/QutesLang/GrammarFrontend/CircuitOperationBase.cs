using System.Text;

using CommunityToolkit.Diagnostics;

using QutesLang.Symbols.Types;

namespace QutesLang.GrammarFrontend;

/// <summary>
/// Base class for all quantum circuit operations
/// </summary>
/// <remarks>
/// Derived classes should use <see cref="Destination"/> so that in case of composition the destination can be updated by base class.
/// </remarks>
/// <param name="registersInvolved"></param>
/// <param name="destination"></param>
public abstract class CircuitOperation(ICollection<QuantumRegister> registersInvolved, IQuantumValue destination)
{
    public virtual IQuantumValue Destination { get; protected set; } = destination;
    public virtual ICollection<QuantumRegister> RegistersInvolved { get; } = registersInvolved;
    public abstract void ApplyToQiskitCircuit(IQuantumCircuit circuit, StringBuilder stringBuilder);
    /// <summary>
    /// This is called before circuit creation, usefull for creating python instances that you need throughout the execution.
    /// </summary>
    /// <param name="stringBuilder"></param>
    public virtual void ApplyQiskitRequirements(StringBuilder stringBuilder) { }

    public CircuitOperation Compose(CircuitOperation other)
    {
        if(other.Destination != Destination)
        {
            throw new InvalidOperationException("Cannot compose two CircuitOperations with different destinations.");
        }
        return new Composition([this, other], Destination);
    }

    public CircuitOperation Into(IQuantumValue newDestination)
    {
        if(newDestination != this.Destination)
        {
            var composition = new Composition([new Copy(this.Destination, newDestination), this], newDestination);
            this.Destination = newDestination;
            return composition;
        }
        return this;
    }

    protected static void AddGateInCircuit(IQuantumCircuit circuit, string gateName, IEnumerable<QuantumRegister> registers, StringBuilder stringBuilder)
    {
        var qubitStringList = string.Join(',', registers.Select(r => r.QubitStringList));
        stringBuilder.AppendLine($"{circuit.Name}.compose({gateName}, [{qubitStringList}], inplace=True)");
    }
    protected static void AddGateInCircuit(IQuantumCircuit circuit, string gateName, IEnumerable<CircuitQubit> qubits, StringBuilder stringBuilder)
    {
        var qubitStringList = string.Join(',', qubits.Select(r => r.Id));
        stringBuilder.AppendLine($"{circuit.Name}.compose({gateName}, [{qubitStringList}], inplace=True)");
    }
}

public class Composition(ICollection<CircuitOperation> circuitOperations, IQuantumValue destination) : CircuitOperation([], null!)
{
    public override IQuantumValue Destination { get; protected set; } = destination;
    public virtual ICollection<CircuitOperation> CircuitOperations { get; } = circuitOperations;
    public override void ApplyToQiskitCircuit(IQuantumCircuit circuit, StringBuilder stringBuilder)
    {
    }
}

public class Empty(IQuantumValue target) : CircuitOperation([target.Register], target)
{
    public override void ApplyToQiskitCircuit(IQuantumCircuit circuit, StringBuilder stringBuilder)
    {
        // No operation to apply for Empty
        return;
    }
}

public class ComposeCircuit(IQuantumCircuit other, ICollection<QuantumRegister> registersToCompose) : CircuitOperation([..other.LocalRegisters, ..registersToCompose], null!)
{
    public override void ApplyToQiskitCircuit(IQuantumCircuit circuit, StringBuilder stringBuilder)
    {
        if(circuit is ControlledCircuit controlledCircuit)
        {
            registersToCompose.Add(controlledCircuit.ControlRegister);
        }
        var gateName = $"{other.Name}_gate";
        stringBuilder.AppendLine($"{gateName} = {other.Name}.to_gate(label='{other.Name}')");
        AddGateInCircuit(circuit, gateName, registersToCompose, stringBuilder);
    }
}

public class Copy(IQuantumValue target, IQuantumValue destination) : CircuitOperation([target.Register, destination.Register], destination)
{
    private readonly int size = Math.Min(target.Size, destination.Size);
    private string GateName => $"copy_{size}";

    public override void ApplyQiskitRequirements(StringBuilder stringBuilder)
    {
        stringBuilder.AppendLine($"{GateName} = ModularAdderGate({size}, label='{GateName}')");
    }

    public override void ApplyToQiskitCircuit(IQuantumCircuit circuit, StringBuilder stringBuilder)
    {
        AddGateInCircuit(circuit, GateName, [..target.Register.Qubits[..size], ..Destination.Register.Qubits[..size]], stringBuilder);
    }
}
