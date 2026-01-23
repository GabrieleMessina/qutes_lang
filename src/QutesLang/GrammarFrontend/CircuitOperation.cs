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
    //public required IQuantumCircuit Gate { get; set; }
    //public required ICircuitHandler CircuitHandler { get; set; }

    public override void ApplyQiskitRequirements(StringBuilder stringBuilder)
    {
        //TODO: WIP, all operations (or the more complex ones), could declare their gates.
        // This way we can have better circuit printing and also reuse gates (in the future).
        // Note that the gate reuse is possibile only for input of the same kind,
        // So we could have for example Measure_qubit and Measure_quinteger gates.
        //Gate = CircuitHandler.DeclareNewQuantumGate();
        //Gate.DeclareQuantumVariable(nameof(target), Destination.Register);
    }

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
        foreach(var register in circuit.LocalRegisters)
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
    private readonly List<QuantumRegister> Ancillae = [];
    private int nBitToCompare;

    public override void ApplyQiskitRequirements(StringBuilder stringBuilder)
    {
        nBitToCompare = Math.Min(a.Size, b.Size);
        var ancillaPrefix = VariableNameGuid.New("equality");
        for (int i = 0; i < nBitToCompare; i++)
        {
            var reg = new QuantumRegister(size: 1) { Name = $"{ancillaPrefix}_{i}" };
            Ancillae.Add(reg);
            RegistersInvolved.Add(reg);
        }
    }

    public override void ApplyToQiskitCircuit(IQuantumCircuit circuit, StringBuilder stringBuilder)
    {
        for (int i = 0; i < nBitToCompare; i++)
        {
            stringBuilder.AppendLine($"{circuit.Name}.cx({a.Register.Qubits[i].Id}, {Ancillae[i].Qubits[0].Id})");
            stringBuilder.AppendLine($"{circuit.Name}.cx({b.Register.Qubits[i].Id}, {Ancillae[i].Qubits[0].Id})");
        }
        // Now, all ancillae qubits are 0 if corresponding bits are equal, we need to AND them all into destination
        var ancillaQubitList = string.Join(",", Ancillae.Select(r => r.Qubits[0].Id));
        stringBuilder.AppendLine($"{circuit.Name}.x([{ancillaQubitList}])");
        stringBuilder.AppendLine($"{circuit.Name}.mcx([{ancillaQubitList}], {Destination.Register.Qubits[0].Id})");
        stringBuilder.AppendLine($"{circuit.Name}.x([{ancillaQubitList}])");

        // Uncompute ancillae
        for (int i = 0; i < nBitToCompare; i++)
        {
            stringBuilder.AppendLine($"{circuit.Name}.cx({b.Register.Qubits[i].Id}, {Ancillae[i].Qubits[0].Id})");
            stringBuilder.AppendLine($"{circuit.Name}.cx({a.Register.Qubits[i].Id}, {Ancillae[i].Qubits[0].Id})");
        }
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

        for (int i = offset.Size - 1; i >= 0; i--)
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

        for (int i = 0; i < offset.Size; i++)
        {
            var gateName = $"left_shift_{target.Count}_{target.SingleElementSize}_{i}";
            stringBuilder.AppendLine($"{gateName} = QutesGates.crot({target.Count}, 2**{i}, {target.SingleElementSize})");
            AddGateInCircuit(circuit, gateName, [offset.Register.Qubits.ElementAt(i), ..Destination.Register.Qubits], stringBuilder);
        }
    }
}
public class Copy(IQuantumValue target, IQuantumValue destination) : CircuitOperation([target.Register, destination.Register], destination)
{
    private readonly int size = Math.Min(target.Size, destination.Size);
    private static bool ReguirementsApplied = false;
    private static readonly string GateName = "copy";

    public override void ApplyQiskitRequirements(StringBuilder stringBuilder)
    {
        if (!ReguirementsApplied)
        {
            ReguirementsApplied = true;
            stringBuilder.AppendLine($"{GateName} = ModularAdderGate({size}, label='{GateName}')");
        }
    }

    public override void ApplyToQiskitCircuit(IQuantumCircuit circuit, StringBuilder stringBuilder)
    {
        AddGateInCircuit(circuit, GateName, [..target.Register.Qubits[..size], ..Destination.Register.Qubits[..size]], stringBuilder);
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
    private readonly int size = Math.Min(a.Size, b.Size);
    private static bool ReguirementsApplied = false;
    private static readonly string GateName = "adder";

    public override void ApplyQiskitRequirements(StringBuilder stringBuilder)
    {
        if (!ReguirementsApplied)
        {
            ReguirementsApplied = true;
            stringBuilder.AppendLine($"{GateName} = ModularAdderGate({size})");
        }
    }

    public override void ApplyToQiskitCircuit(IQuantumCircuit circuit, StringBuilder stringBuilder)
    {
        if(a != Destination && b != Destination)
        {
            AddGateInCircuit(circuit, GateName, [..b.Register.Qubits[..size], ..Destination.Register.Qubits[..size]], stringBuilder);
            AddGateInCircuit(circuit, GateName, [..a.Register.Qubits[..size], ..Destination.Register.Qubits[..size]], stringBuilder);
        }
        else if(a == Destination)
        {
            AddGateInCircuit(circuit, GateName, [..b.Register.Qubits[..size], ..Destination.Register.Qubits[..size]], stringBuilder);
        }
        else if(b == Destination)
        {
            AddGateInCircuit(circuit, GateName, [..a.Register.Qubits[..size], ..Destination.Register.Qubits[..size]], stringBuilder);
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
public class Grover(IQuantumValue pattern, QuantumArrayValue array, IQuantumCircuit predicate, IQuantumValue reflection) : CircuitOperation([pattern.Register, array.Register, ..predicate.LocalRegisters, reflection.Register], null!)
{
    public override void ApplyToQiskitCircuit(IQuantumCircuit circuit, StringBuilder stringBuilder)
    {
        var groverId = VariableNameGuid.New("grover");
        var nIteration = 1; //total search space (rotations = 8) / number of solutions. even if higher accuracy could be achieved with more iterations, it requires a lot more computational power.
        stringBuilder.AppendLine($"{groverId} = GroverOperator({predicate.Name}, reflection_qubits=[{reflection.QubitStringList}], insert_barriers=True, name='{groverId}')");
        stringBuilder.AppendLine($"{groverId} = {groverId}.power({nIteration})");
        AddGateInCircuit(circuit, groverId, predicate.LocalRegisters, stringBuilder);
        
        QuantumCircuit.PrintCircuit(groverId, stringBuilder, decomposeLevel: 1);
        QuantumCircuit.SaveCircuitImage(groverId, stringBuilder, decomposeLevel: 1);
    }
}
/// <summary>
/// Exact String Matching quantum algorithm implementation.
/// Returns the index of the first occurrence of the pattern in the target array, or -1 if the pattern is not found.
/// </summary
/// <param name="target"></param>
/// <param name="pattern"></param>
/// <param name="rotation">A quint value representing the index of the found pattern in the array.</param>
public class ESM(IQuantumValue pattern, QuantumArrayValue array, QuintValue rotation, QubitValue result) : Composition(
    [//TODO: can i really encode -1 if no match is found?
        new RightShift(array, rotation),
        new Equals(array, pattern, result),
        new LeftShift(array, rotation),
    ], rotation)
{
}