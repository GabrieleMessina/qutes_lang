using System.Text;
using QutesLang.Symbols.Types;

namespace QutesLang.GrammarFrontend;

public abstract class CircuitOperation
{
    public abstract void ApplyToQiskitCircuit(IQuantumCircuit circuit, StringBuilder stringBuilder);
    /// <summary>
    /// This is called before circuit creation, usefull for creating python instances that you need throughout the execution.
    /// </summary>
    /// <param name="stringBuilder"></param>
    public virtual void ApplyQiskitRequirements(StringBuilder stringBuilder) { }
    public abstract IQuantumValue Destination { get; }
    public abstract IEnumerable<QuantumRegister> RegistersInvolved { get; }

    protected void Compose(IQuantumCircuit circuit, string gateName, IEnumerable<QuantumRegister> registers, StringBuilder stringBuilder)
    {
        var qubitStringList = string.Join(',', registers.Select(r => r.QubitStringList));
        stringBuilder.AppendLine($"{circuit.Name}.compose({gateName}, [{qubitStringList}], inplace=True)");
    }
}

public class Empty(IQuantumValue target) : CircuitOperation
{
    public override IQuantumValue Destination => target;
    public override IEnumerable<QuantumRegister> RegistersInvolved => [target.Register];

    public override void ApplyToQiskitCircuit(IQuantumCircuit circuit, StringBuilder stringBuilder)
    {
        // No operation to apply for Empty
        return;
    }
}

public class ComposeCircuit(IQuantumCircuit other) : CircuitOperation
{
    public override IQuantumValue Destination => null!;
    public override IEnumerable<QuantumRegister> RegistersInvolved => [..other.QuantumVariables.Values];

    public override void ApplyToQiskitCircuit(IQuantumCircuit circuit, StringBuilder stringBuilder)
    {
        var registersToCompose = other.QuantumVariables.Values.ToList();
        if(circuit is ControlledCircuit controlledCircuit)
        {
            registersToCompose.Add(controlledCircuit.ControlRegister);
        }
        Compose(circuit, other.Name, registersToCompose, stringBuilder);
    }
}

public class StatePreparation(QuantumRegister target, StateVector stateVector) : CircuitOperation
{
    public override IQuantumValue Destination => null!;
    public override IEnumerable<QuantumRegister> RegistersInvolved => [target];

    public override void ApplyToQiskitCircuit(IQuantumCircuit circuit, StringBuilder stringBuilder)
    {
        var stateName = target.Name + "_state_prep";
        stringBuilder.AppendLine($"{stateName} = StatePreparation({stateVector.ToPythonString()}, normalize=True)");
        Compose(circuit, stateName, [target], stringBuilder);
    }
}



public class CNOT(IQuantumValue control, IQuantumValue target) : CircuitOperation
{
    public override IQuantumValue Destination => target;
    public override IEnumerable<QuantumRegister> RegistersInvolved => [control.Register, target.Register];

    public override void ApplyToQiskitCircuit(IQuantumCircuit circuit, StringBuilder stringBuilder)
    {
        stringBuilder.AppendLine($"{circuit.Name}.cx([{control.QubitStringList}],[{target.QubitStringList}])");
    }
}
public class Hadamard(IQuantumValue target) : CircuitOperation
{
    public override IQuantumValue Destination => target;
    public override IEnumerable<QuantumRegister> RegistersInvolved => [target.Register];

    public override void ApplyToQiskitCircuit(IQuantumCircuit circuit, StringBuilder stringBuilder)
    {
        stringBuilder.AppendLine($"{circuit.Name}.h([{target.QubitStringList}])");
    }
}
public class MultiHadamard(IEnumerable<IQuantumValue> controls) : CircuitOperation
{
    public override IQuantumValue Destination => null!;
    public override IEnumerable<QuantumRegister> RegistersInvolved => [..controls.Select(c => c.Register)];

    public override void ApplyToQiskitCircuit(IQuantumCircuit circuit, StringBuilder stringBuilder)
    {
        var controlList = string.Join(",", controls.Select(c => c.QubitStringList));
        stringBuilder.AppendLine($"{circuit.Name}.h([{controlList}])");
    }
}
public class PauliY(IQuantumValue target) : CircuitOperation
{
    public override IQuantumValue Destination => target;
    public override IEnumerable<QuantumRegister> RegistersInvolved => [target.Register];

    public override void ApplyToQiskitCircuit(IQuantumCircuit circuit, StringBuilder stringBuilder)
    {
        stringBuilder.AppendLine($"{circuit.Name}.y([{target.QubitStringList}])");
    }
}
public class PauliZ(IQuantumValue target) : CircuitOperation
{
    public override IQuantumValue Destination => target;
    public override IEnumerable<QuantumRegister> RegistersInvolved => [target.Register];

    public override void ApplyToQiskitCircuit(IQuantumCircuit circuit, StringBuilder stringBuilder)
    {
        stringBuilder.AppendLine($"{circuit.Name}.z([{target.QubitStringList}])");
    }
}
public class Measure(IQuantumValue target) : CircuitOperation
{
    public override IQuantumValue Destination => target;
    public override IEnumerable<QuantumRegister> RegistersInvolved => [target.Register];

    public override void ApplyToQiskitCircuit(IQuantumCircuit circuit, StringBuilder stringBuilder)
    {
        stringBuilder.AppendLine($"{circuit.Name}.measure({target.Register.Name}, {target.Register.ClassicalRegister.Name})");
    }
}
public class MultiMeasure(IEnumerable<IQuantumValue> targets) : CircuitOperation
{
    public override IQuantumValue Destination => null!;
    public override IEnumerable<QuantumRegister> RegistersInvolved => [..targets.Select(c => c.Register)];

    public override void ApplyToQiskitCircuit(IQuantumCircuit circuit, StringBuilder stringBuilder)
    {
        var targetList = string.Join(",", targets.Select(c => c.Register.Name));
        var classicalTargetList = string.Join(",", targets.Select(c => c.Register.ClassicalRegister.Name));
        stringBuilder.AppendLine($"{circuit.Name}.measure([{targetList}], [{classicalTargetList}])");
    }
}
public class MeasureAll() : CircuitOperation
{
    public override IQuantumValue Destination => null!;
    public override IEnumerable<QuantumRegister> RegistersInvolved => [];

    public override void ApplyToQiskitCircuit(IQuantumCircuit circuit, StringBuilder stringBuilder)
    {
        foreach(var register in circuit.Registers.Elements)
        {
            stringBuilder.AppendLine($"{circuit.Name}.measure({register.Name}, {register.ClassicalRegister.Name})");
        }
    }
}
public class Barrier(IEnumerable<IQuantumValue> targets) : CircuitOperation
{
    public override IQuantumValue Destination => null!;
    public override IEnumerable<QuantumRegister> RegistersInvolved => [..targets.Select(t => t.Register)];

    public override void ApplyToQiskitCircuit(IQuantumCircuit circuit, StringBuilder stringBuilder)
    {
        var targetList = string.Join(",", targets.Select(t => t.QubitStringList));
        stringBuilder.AppendLine($"{circuit.Name}.barrier([{targetList}])");
    }
}
public class MultiBarrier(IEnumerable<IQuantumValue> controls) : CircuitOperation
{
    public override IQuantumValue Destination => null!;
    public override IEnumerable<QuantumRegister> RegistersInvolved => [..controls.Select(c => c.Register)];

    public override void ApplyToQiskitCircuit(IQuantumCircuit circuit, StringBuilder stringBuilder)
    {
        var controlList = string.Join(",", controls.Select(c => c.QubitStringList));
        stringBuilder.AppendLine($"{circuit.Name}.barrier([{controlList}])");
    }
}
public class BarrierAll() : CircuitOperation
{
    public override IQuantumValue Destination => null!;
    public override IEnumerable<QuantumRegister> RegistersInvolved => [];

    public override void ApplyToQiskitCircuit(IQuantumCircuit circuit, StringBuilder stringBuilder)
    {
        stringBuilder.AppendLine($"{circuit.Name}.barrier()");
    }
}
public class MCP(IEnumerable<IQuantumValue> controls, IQuantumValue target, FloatValue rotationAngle) : CircuitOperation
{
    public override IQuantumValue Destination => target;
    public override IEnumerable<QuantumRegister> RegistersInvolved => [..controls.Select(c => c.Register), target.Register];

    public override void ApplyToQiskitCircuit(IQuantumCircuit circuit, StringBuilder stringBuilder)
    {
        var controlList = string.Join(",", controls.Select(c => c.QubitStringList));
        stringBuilder.AppendLine($"{circuit.Name}.mcp({rotationAngle.Value},[{controlList}],[{target.QubitStringList}])");
    }
}
public class MCX(IEnumerable<IQuantumValue> controls, IQuantumValue target) : CircuitOperation
{
    public override IQuantumValue Destination => target;
    public override IEnumerable<QuantumRegister> RegistersInvolved => [..controls.Select(c => c.Register), target.Register];

    public override void ApplyToQiskitCircuit(IQuantumCircuit circuit, StringBuilder stringBuilder)
    {
        //TODO: qiskit doesn't handle case where both control and target are lists with more than 1 element. (true for all Multi Controlled Gate and Swap)
        var controlList = string.Join(",", controls.Select(c => c.QubitStringList));
        stringBuilder.AppendLine($"{circuit.Name}.mcx([{controlList}],[{target.QubitStringList}])");
    }
}
public class MCY(IEnumerable<IQuantumValue> controls, IQuantumValue target) : CircuitOperation
{
    public override IQuantumValue Destination => target;
    public override IEnumerable<QuantumRegister> RegistersInvolved => [..controls.Select(c => c.Register), target.Register];

    public override void ApplyToQiskitCircuit(IQuantumCircuit circuit, StringBuilder stringBuilder)
    {
        var controlList = string.Join(",", controls.Select(c => c.QubitStringList));
        stringBuilder.AppendLine($"{circuit.Name}.mcy([{controlList}], [{target.QubitStringList}])");
    }
}
public class MCZ(IEnumerable<IQuantumValue> controls, IQuantumValue target) : CircuitOperation
{
    public override IQuantumValue Destination => target;
    public override IEnumerable<QuantumRegister> RegistersInvolved => [..controls.Select(c => c.Register), target.Register];

    public override void ApplyToQiskitCircuit(IQuantumCircuit circuit, StringBuilder stringBuilder)
    {
        var controlList = string.Join(",", controls.Select(c => c.QubitStringList));
        stringBuilder.AppendLine($"{circuit.Name}.mcz([{controlList}], [{target.QubitStringList}])");
    }
}
public class Swap(IQuantumValue a, IQuantumValue b) : CircuitOperation
{
    public override IQuantumValue Destination => a;
    public override IEnumerable<QuantumRegister> RegistersInvolved => [a.Register, b.Register];

    public override void ApplyToQiskitCircuit(IQuantumCircuit circuit, StringBuilder stringBuilder)
    {
        stringBuilder.AppendLine($"{circuit.Name}.swap([{a.QubitStringList}], [{b.QubitStringList}])");
    }
}
public class MultiSwap(IEnumerable<IQuantumValue> controls, IQuantumValue target) : CircuitOperation
{
    public override IQuantumValue Destination => target;
    public override IEnumerable<QuantumRegister> RegistersInvolved => [..controls.Select(c => c.Register), target.Register];

    public override void ApplyToQiskitCircuit(IQuantumCircuit circuit, StringBuilder stringBuilder)
    {
        var controlList = string.Join(",", controls.Select(c => c.QubitStringList));
        stringBuilder.AppendLine($"{circuit.Name}.swap([{controlList}], [{target.QubitStringList}])");
    }
}
public class Or(IQuantumValue a, IQuantumValue b, IQuantumValue destination) : CircuitOperation
{
    public override IQuantumValue Destination => destination;
    public override IEnumerable<QuantumRegister> RegistersInvolved => [a.Register, b.Register, destination.Register];

    public override void ApplyToQiskitCircuit(IQuantumCircuit circuit, StringBuilder stringBuilder)
    {
        //TODO: implemement quantum OR operation.
    }
}
public class And(IQuantumValue a, IQuantumValue b, IQuantumValue destination) : CircuitOperation
{
    public override IQuantumValue Destination => destination;
    public override IEnumerable<QuantumRegister> RegistersInvolved => [a.Register, b.Register, destination.Register];

    public override void ApplyToQiskitCircuit(IQuantumCircuit circuit, StringBuilder stringBuilder)
    {
        //TODO: implemement quantum AND operation.
    }
}
public class Not(IQuantumValue target) : CircuitOperation
{
    public override IQuantumValue Destination => target;
    public override IEnumerable<QuantumRegister> RegistersInvolved => [target.Register];

    public override void ApplyToQiskitCircuit(IQuantumCircuit circuit, StringBuilder stringBuilder)
    {
        //TODO: implemement quantum NOT operation.
    }
}
public class Equals(IQuantumValue a, IQuantumValue b, IQuantumValue destination) : CircuitOperation
{
    public override IQuantumValue Destination => destination;
    public override IEnumerable<QuantumRegister> RegistersInvolved => [a.Register, b.Register, destination.Register];

    public override void ApplyToQiskitCircuit(IQuantumCircuit circuit, StringBuilder stringBuilder)
    {
        //TODO: implemement quantum == operation.
    }
}
public class NotEquals(IQuantumValue a, IQuantumValue b, IQuantumValue destination) : CircuitOperation
{
    public override IQuantumValue Destination => destination;
    public override IEnumerable<QuantumRegister> RegistersInvolved => [a.Register, b.Register, destination.Register];

    public override void ApplyToQiskitCircuit(IQuantumCircuit circuit, StringBuilder stringBuilder)
    {
        //TODO: implemement quantum != operation.
    }
}
public class LowerThan(IQuantumValue a, IQuantumValue b, IQuantumValue destination) : CircuitOperation
{
    public override IQuantumValue Destination => destination;
    public override IEnumerable<QuantumRegister> RegistersInvolved => [a.Register, b.Register, destination.Register];

    public override void ApplyToQiskitCircuit(IQuantumCircuit circuit, StringBuilder stringBuilder)
    {
        //TODO: implemement quantum < operation.
    }
}
public class LowerEqualThan(IQuantumValue a, IQuantumValue b, IQuantumValue destination) : CircuitOperation
{
    public override IQuantumValue Destination => destination;
    public override IEnumerable<QuantumRegister> RegistersInvolved => [ a.Register,  b.Register,  destination.Register];

    public override void ApplyToQiskitCircuit(IQuantumCircuit circuit, StringBuilder stringBuilder)
    {
        //TODO: implemement quantum <= operation.
    }
}
public class GreaterThan(IQuantumValue a, IQuantumValue b, IQuantumValue destination) : CircuitOperation
{
    public override IQuantumValue Destination => destination;
    public override IEnumerable<QuantumRegister> RegistersInvolved => [ a.Register,  b.Register,  destination.Register];

    public override void ApplyToQiskitCircuit(IQuantumCircuit circuit, StringBuilder stringBuilder)
    {
        //TODO: implemement quantum > operation.
    }
}
public class GreaterEqualThan(IQuantumValue a, IQuantumValue b, IQuantumValue destination) : CircuitOperation
{
    public override IQuantumValue Destination => destination;
    public override IEnumerable<QuantumRegister> RegistersInvolved => [ a.Register,  b.Register,  destination.Register];

    public override void ApplyToQiskitCircuit(IQuantumCircuit circuit, StringBuilder stringBuilder)
    {
        //TODO: implemement quantum >= operation.
    }
}
public class RightShift : CircuitOperation
{
    private readonly IQuantumValue a;
    private readonly QuintValue offset;

    public override IQuantumValue Destination => a;
    public override IEnumerable<QuantumRegister> RegistersInvolved => [a.Register, offset.Register];
    public RightShift(IQuantumValue a, QuintValue offset)
    {
        this.a = a;
        this.offset = offset;
    }
    public RightShift(IQuantumValue a, IntValue offset)
    {
        this.a = a;
        this.offset = new QuintValue(QuintParser.Parse(offset.Value.ToString()));
    }

    public override void ApplyToQiskitCircuit(IQuantumCircuit circuit, StringBuilder stringBuilder)
    {
        //TODO: implemement quantum >> operation.
    }
}
public class LeftShift : CircuitOperation
{
    private readonly IQuantumValue a;
    private readonly QuintValue offset;

    public override IQuantumValue Destination => a;
    public override IEnumerable<QuantumRegister> RegistersInvolved => [ a.Register,  offset.Register];
    public LeftShift(IQuantumValue a, QuintValue offset)
    {
        this.a = a;
        this.offset = offset;
    }
    public LeftShift(IQuantumValue a, IntValue offset)
    {
        this.a = a;
        this.offset = new QuintValue(QuintParser.Parse(offset.Value.ToString()));
    }

    public override void ApplyToQiskitCircuit(IQuantumCircuit circuit, StringBuilder stringBuilder)
    {
        //TODO: implemement quantum >> operation.
    }
}
public class Addition(IQuantumValue a, IQuantumValue b, IQuantumValue destination) : CircuitOperation
{
    public override IQuantumValue Destination => destination;
    public override IEnumerable<QuantumRegister> RegistersInvolved => [ a.Register,  b.Register,  destination.Register];

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
        Compose(circuit, GateName, [b.Register, destination.Register], stringBuilder);
        Compose(circuit, GateName, [a.Register, destination.Register], stringBuilder);
    }
}

public class Subtraction(IQuantumValue a, IQuantumValue b, IQuantumValue destination) : CircuitOperation
{
    public override IQuantumValue Destination => destination;
    public override IEnumerable<QuantumRegister> RegistersInvolved => [ a.Register,  b.Register,  destination.Register];

    public override void ApplyToQiskitCircuit(IQuantumCircuit circuit, StringBuilder stringBuilder)
    {
        //TODO: implemement quantum subtraction operation.
    }
}
public class Multiply(IQuantumValue a, IQuantumValue b, IQuantumValue destination) : CircuitOperation
{
    public override IQuantumValue Destination => destination;
    public override IEnumerable<QuantumRegister> RegistersInvolved => [ a.Register,  b.Register,  destination.Register];

    public override void ApplyToQiskitCircuit(IQuantumCircuit circuit, StringBuilder stringBuilder)
    {
        //TODO: implemement quantum Multiply operation.
    }
}
public class Divide(IQuantumValue a, IQuantumValue b, IQuantumValue destination) : CircuitOperation
{
    public override IQuantumValue Destination => destination;
    public override IEnumerable<QuantumRegister> RegistersInvolved => [ a.Register,  b.Register,  destination.Register];

    public override void ApplyToQiskitCircuit(IQuantumCircuit circuit, StringBuilder stringBuilder)
    {
        //TODO: implemement quantum Divide operation.
    }
}
public class Module(IQuantumValue a, IQuantumValue b, IQuantumValue destination) : CircuitOperation
{
    public override IQuantumValue Destination => destination;
    public override IEnumerable<QuantumRegister> RegistersInvolved => [ a.Register,  b.Register,  destination.Register];

    public override void ApplyToQiskitCircuit(IQuantumCircuit circuit, StringBuilder stringBuilder)
    {
        //TODO: implemement quantum Module operation.
    }
}
public class Opposite(IQuantumValue a, IQuantumValue destination) : CircuitOperation
{
    public override IQuantumValue Destination => destination;
    public override IEnumerable<QuantumRegister> RegistersInvolved => [ a.Register,  destination.Register];

    public override void ApplyToQiskitCircuit(IQuantumCircuit circuit, StringBuilder stringBuilder)
    {
        //TODO: implemement quantum Opposite operation.
    }
}
public class Increment(IQuantumValue a, IQuantumValue destination, int amount = 1) : CircuitOperation
{
    public override IQuantumValue Destination => destination;
    public override IEnumerable<QuantumRegister> RegistersInvolved => [ a.Register,  destination.Register];

    public override void ApplyToQiskitCircuit(IQuantumCircuit circuit, StringBuilder stringBuilder)
    {
        //TODO: implemement quantum Increment operation.
    }
}
public class Decrement(IQuantumValue a, IQuantumValue destination, int amount = 1) : CircuitOperation
{
    public override IQuantumValue Destination => destination;
    public override IEnumerable<QuantumRegister> RegistersInvolved => [ a.Register,  destination.Register];

    public override void ApplyToQiskitCircuit(IQuantumCircuit circuit, StringBuilder stringBuilder)
    {
        //TODO: implemement quantum Decrement operation.
    }
}
