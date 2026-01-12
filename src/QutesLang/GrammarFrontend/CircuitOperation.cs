using System.Text;
using QutesLang.Symbols.Types;

namespace QutesLang.GrammarFrontend;

public abstract class CircuitOperation
{
    public abstract void ApplyToQiskitCircuit(IQuantumCircuit circuit, StringBuilder stringBuilder);
    public abstract IQuantumValue Destination { get; }
    public abstract IEnumerable<QuantumRegister> RegistersInvolved { get; }
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
        var qubitToComposeWithOther = other.QuantumVariables.Values.SelectMany(qr => qr.Qubits).ToList();
        if(circuit is ControlledCircuit controlledCircuit)
        {
            qubitToComposeWithOther.AddRange(controlledCircuit.ControlRegister.Qubits);
        }
        var qubitStringList = string.Join(",", qubitToComposeWithOther.Select(q => q.Id));
        string clbitStringList = string.Empty;
        stringBuilder.AppendLine($"{circuit.Name}.compose({other.Name},[{qubitStringList}], [{clbitStringList}], inplace=True)");
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
        stringBuilder.AppendLine($"{circuit.Name}.compose({stateName}, [{target.QubitStringList}], inplace=True)");
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
        //TODO: we need to define classical bits to measure into. 
        stringBuilder.AppendLine($"{circuit.Name}.measure([{target.QubitStringList}])");
    }
}
public class MultiMeasure(IEnumerable<IQuantumValue> controls) : CircuitOperation
{
    public override IQuantumValue Destination => null!;
    public override IEnumerable<QuantumRegister> RegistersInvolved => [..controls.Select(c => c.Register)];

    public override void ApplyToQiskitCircuit(IQuantumCircuit circuit, StringBuilder stringBuilder)
    {
        var controlList = string.Join(",", controls.Select(c => c.QubitStringList));
        stringBuilder.AppendLine($"{circuit.Name}.measure([{controlList}])");
    }
}
public class MeasureAll() : CircuitOperation
{
    public override IQuantumValue Destination => null!;
    public override IEnumerable<QuantumRegister> RegistersInvolved => [];

    public override void ApplyToQiskitCircuit(IQuantumCircuit circuit, StringBuilder stringBuilder)
    {
        stringBuilder.AppendLine($"{circuit.Name}.measure_all()");
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

    public override void ApplyToQiskitCircuit(IQuantumCircuit circuit, StringBuilder stringBuilder)
    {
        //TODO: implemement quantum sum operation.
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
