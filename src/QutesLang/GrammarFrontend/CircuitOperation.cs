using System.Text;
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
public abstract class CircuitOperation(IEnumerable<QuantumRegister> registersInvolved, IQuantumValue destination)
{
    public virtual IQuantumValue Destination { get; protected set; } = destination;
    public virtual IEnumerable<QuantumRegister> RegistersInvolved { get; } = registersInvolved;
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
public class Composition(ICollection<CircuitOperation> circuitOperations, IQuantumValue destination) : CircuitOperation(circuitOperations.SelectMany(c => c.RegistersInvolved), destination)
{
    /// <summary>
    /// Only for convenience of use in derived classes.
    /// </summary>
    /// <remarks>
    /// If you use this constructor, <b>you must override</b> <see cref="CircuitOperations"/> and <see cref="Destination"/> properties.
    /// </remarks>
    protected Composition() : this([], null!)
    {
    }

    public virtual ICollection<CircuitOperation> CircuitOperations { get; } = circuitOperations;

    public sealed override void ApplyQiskitRequirements(StringBuilder stringBuilder)
    {
        foreach (var op in CircuitOperations)
        {
            op.ApplyQiskitRequirements(stringBuilder);
        }
    }

    public sealed override void ApplyToQiskitCircuit(IQuantumCircuit circuit, StringBuilder stringBuilder)
    {
        foreach (var op in CircuitOperations)
        {
            op.ApplyToQiskitCircuit(circuit, stringBuilder);
        }
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
public class ComposeCircuit(IQuantumCircuit other) : CircuitOperation([.. other.QuantumVariables.Values], null!)
{
    public override void ApplyToQiskitCircuit(IQuantumCircuit circuit, StringBuilder stringBuilder)
    {
        var registersToCompose = other.QuantumVariables.Values.ToList();
        if(circuit is ControlledCircuit controlledCircuit)
        {
            registersToCompose.Add(controlledCircuit.ControlRegister);
        }
        AddGateInCircuit(circuit, other.Name, registersToCompose, stringBuilder);
    }
}
public class StatePreparation(QuantumRegister target, StateVector stateVector) : CircuitOperation([target], null!)
{
    public override void ApplyToQiskitCircuit(IQuantumCircuit circuit, StringBuilder stringBuilder)
    {
        var stateName = target.Name + "_state_prep";
        stringBuilder.AppendLine($"{stateName} = StatePreparation({stateVector.ToPythonString()}, normalize=True)");
        AddGateInCircuit(circuit, stateName, [target], stringBuilder);
    }
}
public class CNOT(IQuantumValue control, IQuantumValue target) : CircuitOperation([control.Register, target.Register], target)
{
    public override void ApplyToQiskitCircuit(IQuantumCircuit circuit, StringBuilder stringBuilder)
    {
        stringBuilder.AppendLine($"{circuit.Name}.cx([{control.QubitStringList}],[{Destination.QubitStringList}])");
    }
}
public class Hadamard(IQuantumValue target) : CircuitOperation([target.Register], target)
{
    public override void ApplyToQiskitCircuit(IQuantumCircuit circuit, StringBuilder stringBuilder)
    {
        stringBuilder.AppendLine($"{circuit.Name}.h([{Destination.QubitStringList}])");
    }
}
public class MultiHadamard(IEnumerable<IQuantumValue> controls) : CircuitOperation([..controls.Select(c => c.Register)], null!)
{
    public override void ApplyToQiskitCircuit(IQuantumCircuit circuit, StringBuilder stringBuilder)
    {
        var controlList = string.Join(",", controls.Select(c => c.QubitStringList));
        stringBuilder.AppendLine($"{circuit.Name}.h([{controlList}])");
    }
}
public class PauliY(IQuantumValue target) : CircuitOperation([target.Register], target)
{
    public override void ApplyToQiskitCircuit(IQuantumCircuit circuit, StringBuilder stringBuilder)
    {
        stringBuilder.AppendLine($"{circuit.Name}.y([{Destination.QubitStringList}])");
    }
}
public class PauliZ(IQuantumValue target) : CircuitOperation([target.Register], target)
{
    public override void ApplyToQiskitCircuit(IQuantumCircuit circuit, StringBuilder stringBuilder)
    {
        stringBuilder.AppendLine($"{circuit.Name}.z([{Destination.QubitStringList}])");
    }
}
public class Measure(IQuantumValue target) : CircuitOperation([target.Register], target)
{
    public override void ApplyToQiskitCircuit(IQuantumCircuit circuit, StringBuilder stringBuilder)
    {
        stringBuilder.AppendLine($"{circuit.Name}.measure({Destination.Register.Name}, {Destination.Register.ClassicalRegister.Name})");
    }
}
public class MultiMeasure(IEnumerable<IQuantumValue> targets) : CircuitOperation([..targets.Select(c => c.Register)], null!)
{
    public override void ApplyToQiskitCircuit(IQuantumCircuit circuit, StringBuilder stringBuilder)
    {
        var targetList = string.Join(",", targets.Select(c => c.Register.Name));
        var classicalTargetList = string.Join(",", targets.Select(c => c.Register.ClassicalRegister.Name));
        stringBuilder.AppendLine($"{circuit.Name}.measure([{targetList}], [{classicalTargetList}])");
    }
}
public class MeasureAll() : CircuitOperation([], null!)
{
    public override void ApplyToQiskitCircuit(IQuantumCircuit circuit, StringBuilder stringBuilder)
    {
        foreach(var register in circuit.Registers.Elements)
        {
            stringBuilder.AppendLine($"{circuit.Name}.measure({register.Name}, {register.ClassicalRegister.Name})");
        }
    }
}
public class Barrier(IEnumerable<IQuantumValue> targets) : CircuitOperation([..targets.Select(t => t.Register)], null!)
{
    public override void ApplyToQiskitCircuit(IQuantumCircuit circuit, StringBuilder stringBuilder)
    {
        var targetList = string.Join(",", targets.Select(t => t.QubitStringList));
        stringBuilder.AppendLine($"{circuit.Name}.barrier([{targetList}])");
    }
}
public class MultiBarrier(IEnumerable<IQuantumValue> controls) : CircuitOperation([..controls.Select(c => c.Register)], null!)
{
    public override void ApplyToQiskitCircuit(IQuantumCircuit circuit, StringBuilder stringBuilder)
    {
        var controlList = string.Join(",", controls.Select(c => c.QubitStringList));
        stringBuilder.AppendLine($"{circuit.Name}.barrier([{controlList}])");
    }
}
public class BarrierAll() : CircuitOperation([], null!)
{
    public override void ApplyToQiskitCircuit(IQuantumCircuit circuit, StringBuilder stringBuilder)
    {
        stringBuilder.AppendLine($"{circuit.Name}.barrier()");
    }
}
public class MCP(IEnumerable<IQuantumValue> controls, IQuantumValue target, FloatValue rotationAngle) : CircuitOperation([..controls.Select(c => c.Register), target.Register], target)
{
    public override void ApplyToQiskitCircuit(IQuantumCircuit circuit, StringBuilder stringBuilder)
    {
        var controlList = string.Join(",", controls.Select(c => c.QubitStringList));
        stringBuilder.AppendLine($"{circuit.Name}.mcp({rotationAngle.Value},[{controlList}],[{Destination.QubitStringList}])");
    }
}
public class MCX(IEnumerable<IQuantumValue> controls, IQuantumValue target) : CircuitOperation([..controls.Select(c => c.Register), target.Register], target)
{
    public override void ApplyToQiskitCircuit(IQuantumCircuit circuit, StringBuilder stringBuilder)
    {
        //TODO: qiskit doesn't handle case where both control and target are lists with more than 1 element. (true for all Multi Controlled Gate and Swap)
        var controlList = string.Join(",", controls.Select(c => c.QubitStringList));
        stringBuilder.AppendLine($"{circuit.Name}.mcx([{controlList}],[{Destination.QubitStringList}])");
    }
}
public class MCY(IEnumerable<IQuantumValue> controls, IQuantumValue target) : CircuitOperation([..controls.Select(c => c.Register), target.Register], target)
{
    public override void ApplyToQiskitCircuit(IQuantumCircuit circuit, StringBuilder stringBuilder)
    {
        var controlList = string.Join(",", controls.Select(c => c.QubitStringList));
        stringBuilder.AppendLine($"{circuit.Name}.mcy([{controlList}], [{Destination.QubitStringList}])");
    }
}
public class MCZ(IEnumerable<IQuantumValue> controls, IQuantumValue target) : CircuitOperation([..controls.Select(c => c.Register), target.Register], target)
{
    public override void ApplyToQiskitCircuit(IQuantumCircuit circuit, StringBuilder stringBuilder)
    {
        var controlList = string.Join(",", controls.Select(c => c.QubitStringList));
        stringBuilder.AppendLine($"{circuit.Name}.mcz([{controlList}], [{Destination.QubitStringList}])");
    }
}
public class Swap(IQuantumValue a, IQuantumValue b) : CircuitOperation([a.Register, b.Register], a)
{
    public override void ApplyToQiskitCircuit(IQuantumCircuit circuit, StringBuilder stringBuilder)
    {
        stringBuilder.AppendLine($"{circuit.Name}.swap([{Destination.QubitStringList}], [{b.QubitStringList}])");
    }
}
public class MultiSwap(IEnumerable<IQuantumValue> controls, IQuantumValue target) : CircuitOperation([..controls.Select(c => c.Register), target.Register], target)
{
    public override void ApplyToQiskitCircuit(IQuantumCircuit circuit, StringBuilder stringBuilder)
    {
        var controlList = string.Join(",", controls.Select(c => c.QubitStringList));
        stringBuilder.AppendLine($"{circuit.Name}.swap([{controlList}], [{Destination.QubitStringList}])");
    }
}
public class Or(IQuantumValue a, IQuantumValue b, IQuantumValue destination) : CircuitOperation([a.Register, b.Register, destination.Register], destination)
{
    public override void ApplyToQiskitCircuit(IQuantumCircuit circuit, StringBuilder stringBuilder)
    {
        //TODO: implemement quantum OR operation.
    }
}
public class And(IQuantumValue a, IQuantumValue b, IQuantumValue destination) : CircuitOperation([a.Register, b.Register, destination.Register], destination)
{
    public override void ApplyToQiskitCircuit(IQuantumCircuit circuit, StringBuilder stringBuilder)
    {
        //TODO: implemement quantum AND operation.
    }
}
public class Not(IQuantumValue target) : CircuitOperation([target.Register], target)
{
    public override void ApplyToQiskitCircuit(IQuantumCircuit circuit, StringBuilder stringBuilder)
    {
        stringBuilder.AppendLine($"{circuit.Name}.x([{Destination.QubitStringList}])");
    }
}
public class Equals(IQuantumValue a, IQuantumValue b, IQuantumValue destination) : CircuitOperation([a.Register, b.Register, destination.Register], destination)
{
    public override void ApplyToQiskitCircuit(IQuantumCircuit circuit, StringBuilder stringBuilder)
    {
        //TODO: implemement quantum == operation.
    }
}
public class NotEquals(IQuantumValue a, IQuantumValue b, IQuantumValue destination) : CircuitOperation([a.Register, b.Register, destination.Register], destination)
{
    public override void ApplyToQiskitCircuit(IQuantumCircuit circuit, StringBuilder stringBuilder)
    {
        //TODO: implemement quantum != operation.
    }
}
public class LowerThan(IQuantumValue a, IQuantumValue b, IQuantumValue destination) : CircuitOperation([a.Register, b.Register, destination.Register], destination)
{
    public override void ApplyToQiskitCircuit(IQuantumCircuit circuit, StringBuilder stringBuilder)
    {
        //TODO: implemement quantum < operation.
    }
}
public class LowerEqualThan(IQuantumValue a, IQuantumValue b, IQuantumValue destination) : CircuitOperation([a.Register, b.Register, destination.Register], destination)
{
    public override void ApplyToQiskitCircuit(IQuantumCircuit circuit, StringBuilder stringBuilder)
    {
        //TODO: implemement quantum <= operation.
    }
}
public class GreaterThan(IQuantumValue a, IQuantumValue b, IQuantumValue destination) : CircuitOperation([a.Register, b.Register, destination.Register], destination)
{
    public override void ApplyToQiskitCircuit(IQuantumCircuit circuit, StringBuilder stringBuilder)
    {
        //TODO: implemement quantum > operation.
    }
}
public class GreaterEqualThan(IQuantumValue a, IQuantumValue b, IQuantumValue destination) : CircuitOperation([a.Register, b.Register, destination.Register], destination)
{
    public override void ApplyToQiskitCircuit(IQuantumCircuit circuit, StringBuilder stringBuilder)
    {
        //TODO: implemement quantum >= operation.
    }
}
public class RightShift : LeftShift
{
    public RightShift(QuantumArrayValue target, QuintValue offset) : base(target, offset)
    {
    }
    public RightShift(QuantumArrayValue target, IntValue offset) : base(target, offset)
    {
    }

    public override void ApplyToQiskitCircuit(IQuantumCircuit circuit, StringBuilder stringBuilder)
    {
        if (target != Destination)
        {
            new Copy(target, Destination).ApplyToQiskitCircuit(circuit, stringBuilder);
        }

        for (int i = QuintValue.DefaultSize - 1; i >= 0; i--)
        {
            var gateName = $"right_shift_{target.Count}_{target.SingleElementSize}_{i}";
            stringBuilder.AppendLine($"{gateName} = QutesGates.crot({target.Count}, 2**{i}, {target.SingleElementSize}).inverse()");
            AddGateInCircuit(circuit, gateName, [offset.Register.Qubits.ElementAt(i), ..Destination.Register.Qubits], stringBuilder);
        }
    }
}
public class LeftShift : CircuitOperation
{
    protected readonly QuantumArrayValue target;
    protected readonly QuintValue offset;

    public override IQuantumValue Destination { get; protected set; } //Is a QuantumArrayValue
    public LeftShift(QuantumArrayValue target, QuintValue offset) : base([target.Register, offset.Register], target)
    {
        //TODO: if offset is power of 2, we can optimize the operation.
        //TODO: if offset is classic, we can do the operation in preprocessing, is this better?
        this.target = target;
        this.Destination = target;
        this.offset = offset;
    }
    public LeftShift(QuantumArrayValue target, IntValue offset) : this(target, new QuintValue(offset.Value))
    {
    }
    public LeftShift(QuantumArrayValue target, QuantumArrayValue destination, QuintValue offset) : base([target.Register, destination.Register, offset.Register], destination)
    {
        this.target = target;
        this.Destination = destination;
        this.offset = offset;
    }
    public LeftShift(QuantumArrayValue target, QuantumArrayValue destination, IntValue offset) : this(target, destination, new QuintValue(offset.Value))
    {
    }

    public override void ApplyToQiskitCircuit(IQuantumCircuit circuit, StringBuilder stringBuilder)
    {
        if(target != Destination){
            new Copy(target, Destination).ApplyToQiskitCircuit(circuit, stringBuilder);
        }

        for (int i = 0; i < QuintValue.DefaultSize; i++)
        {
            var gateName = $"left_shift_{target.Count}_{target.SingleElementSize}_{i}";
            stringBuilder.AppendLine($"{gateName} = QutesGates.crot({target.Count}, 2**{i}, {target.SingleElementSize})");
            AddGateInCircuit(circuit, gateName, [offset.Register.Qubits.ElementAt(i), ..Destination.Register.Qubits], stringBuilder);
        }
    }
}
public class Copy(IQuantumValue target, IQuantumValue destination) : CircuitOperation([target.Register, destination.Register], destination)
{
    private static bool ReguirementsApplied = false;
    private static readonly string GateName = "copy";

    public override void ApplyQiskitRequirements(StringBuilder stringBuilder)
    {
        if (!ReguirementsApplied)
        {
            ReguirementsApplied = true;
            stringBuilder.AppendLine($"{GateName} = ModularAdderGate({QuintValue.DefaultSize}, label='{GateName}')");
        }
    }

    public override void ApplyToQiskitCircuit(IQuantumCircuit circuit, StringBuilder stringBuilder)
    {
        AddGateInCircuit(circuit, GateName, [target.Register, Destination.Register], stringBuilder);
    }
}

public class TwosComplement(IQuantumValue target, IQuantumValue destination) : Composition(
    [
        new Not(target).Into(destination),
        new Addition(destination, new QuintValue(1), destination)
    ], destination)
{
}

public class Addition(IQuantumValue a, IQuantumValue b, IQuantumValue destination) : CircuitOperation([a.Register, b.Register, destination.Register], destination)
{
    private static bool ReguirementsApplied = false;
    private static readonly string GateName = "adder";

    public override void ApplyQiskitRequirements(StringBuilder stringBuilder)
    {
        if (!ReguirementsApplied)
        {
            ReguirementsApplied = true;
            stringBuilder.AppendLine($"{GateName} = ModularAdderGate({QuintValue.DefaultSize})");
        }
    }

    public override void ApplyToQiskitCircuit(IQuantumCircuit circuit, StringBuilder stringBuilder)
    {
        if(a != Destination && b != Destination)
        {
            AddGateInCircuit(circuit, GateName, [b.Register, Destination.Register], stringBuilder);
            AddGateInCircuit(circuit, GateName, [a.Register, Destination.Register], stringBuilder);
        }
        else if(a == Destination)
        {
            AddGateInCircuit(circuit, GateName, [b.Register, Destination.Register], stringBuilder);
        }
        else if(b == Destination)
        {
            AddGateInCircuit(circuit, GateName, [a.Register, Destination.Register], stringBuilder);
        }
    }
}

public class Subtraction(IQuantumValue a, IQuantumValue b, IQuantumValue destination) : Composition(
    [
        new TwosComplement(b, destination),
        new Addition(a, destination, destination)
    ], destination)
{
}

public class Multiply(IQuantumValue a, IQuantumValue b, IQuantumValue destination) : CircuitOperation([a.Register, b.Register, destination.Register], destination)
{
    public override void ApplyToQiskitCircuit(IQuantumCircuit circuit, StringBuilder stringBuilder)
    {
        //TODO: implemement quantum Multiply operation.
    }
}
public class Divide(IQuantumValue a, IQuantumValue b, IQuantumValue destination) : CircuitOperation([a.Register, b.Register, destination.Register], destination)
{
    public override void ApplyToQiskitCircuit(IQuantumCircuit circuit, StringBuilder stringBuilder)
    {
        //TODO: implemement quantum Divide operation.
    }
}
public class Module(IQuantumValue a, IQuantumValue b, IQuantumValue destination) : CircuitOperation([a.Register, b.Register, destination.Register], destination)
{
    public override void ApplyToQiskitCircuit(IQuantumCircuit circuit, StringBuilder stringBuilder)
    {
        //TODO: implemement quantum Module operation.
    }
}
