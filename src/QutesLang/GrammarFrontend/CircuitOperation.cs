using System.Text;
using QutesLang.Symbols.Types;

namespace QutesLang.GrammarFrontend;

public abstract class CircuitOperation
{
    public abstract void ApplyToQiskitCircuit(IQuantumCircuit circuit, StringBuilder stringBuilder);
    public abstract IQuantumType Destination { get; }
    public abstract IEnumerable<QuantumRegister> RegistersInvolved { get; }
}

public class Empty(IQuantumType target) : CircuitOperation
{
    public override IQuantumType Destination => target;
    public override IEnumerable<QuantumRegister> RegistersInvolved => [target.Register];

    public override void ApplyToQiskitCircuit(IQuantumCircuit circuit, StringBuilder stringBuilder)
    {
        // No operation to apply for Empty
        return;
    }
}

public class ComposeCircuit(IQuantumCircuit other) : CircuitOperation
{
    public override IQuantumType Destination => null!;
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

public class CNOT(IQuantumType control, IQuantumType target) : CircuitOperation
{
    public override IQuantumType Destination => target;
    public override IEnumerable<QuantumRegister> RegistersInvolved => [control.Register, target.Register];

    public override void ApplyToQiskitCircuit(IQuantumCircuit circuit, StringBuilder stringBuilder)
    {
        stringBuilder.AppendLine($"{circuit.Name}.cx([{control.QubitStringList}],[{target.QubitStringList}])");
    }
}
public class Hadamard(IQuantumType target) : CircuitOperation
{
    public override IQuantumType Destination => target;
    public override IEnumerable<QuantumRegister> RegistersInvolved => [target.Register];

    public override void ApplyToQiskitCircuit(IQuantumCircuit circuit, StringBuilder stringBuilder)
    {
        stringBuilder.AppendLine($"{circuit.Name}.h([{target.QubitStringList}])");
    }
}
public class MultiHadamard(IEnumerable<IQuantumType> controls) : CircuitOperation
{
    public override IQuantumType Destination => null!;
    public override IEnumerable<QuantumRegister> RegistersInvolved => [..controls.Select(c => c.Register)];

    public override void ApplyToQiskitCircuit(IQuantumCircuit circuit, StringBuilder stringBuilder)
    {
        var controlList = string.Join(",", controls.Select(c => c.QubitStringList));
        stringBuilder.AppendLine($"{circuit.Name}.h([{controlList}])");
    }
}
public class PauliY(IQuantumType target) : CircuitOperation
{
    public override IQuantumType Destination => target;
    public override IEnumerable<QuantumRegister> RegistersInvolved => [target.Register];

    public override void ApplyToQiskitCircuit(IQuantumCircuit circuit, StringBuilder stringBuilder)
    {
        stringBuilder.AppendLine($"{circuit.Name}.y([{target.QubitStringList}])");
    }
}
public class PauliZ(IQuantumType target) : CircuitOperation
{
    public override IQuantumType Destination => target;
    public override IEnumerable<QuantumRegister> RegistersInvolved => [target.Register];

    public override void ApplyToQiskitCircuit(IQuantumCircuit circuit, StringBuilder stringBuilder)
    {
        stringBuilder.AppendLine($"{circuit.Name}.z([{target.QubitStringList}])");
    }
}
public class Measure(IQuantumType target) : CircuitOperation
{
    public override IQuantumType Destination => target;
    public override IEnumerable<QuantumRegister> RegistersInvolved => [target.Register];

    public override void ApplyToQiskitCircuit(IQuantumCircuit circuit, StringBuilder stringBuilder)
    {
        //TODO: we need to define classical bits to measure into. 
        stringBuilder.AppendLine($"{circuit.Name}.measure([{target.QubitStringList}])");
    }
}
public class MultiMeasure(IEnumerable<IQuantumType> controls) : CircuitOperation
{
    public override IQuantumType Destination => null!;
    public override IEnumerable<QuantumRegister> RegistersInvolved => [..controls.Select(c => c.Register)];

    public override void ApplyToQiskitCircuit(IQuantumCircuit circuit, StringBuilder stringBuilder)
    {
        var controlList = string.Join(",", controls.Select(c => c.QubitStringList));
        stringBuilder.AppendLine($"{circuit.Name}.measure([{controlList}])");
    }
}
public class MeasureAll() : CircuitOperation
{
    public override IQuantumType Destination => null!;
    public override IEnumerable<QuantumRegister> RegistersInvolved => [];

    public override void ApplyToQiskitCircuit(IQuantumCircuit circuit, StringBuilder stringBuilder)
    {
        stringBuilder.AppendLine($"{circuit.Name}.measure_all()");
    }
}
public class Barrier(IEnumerable<IQuantumType> targets) : CircuitOperation
{
    public override IQuantumType Destination => null!;
    public override IEnumerable<QuantumRegister> RegistersInvolved => [..targets.Select(t => t.Register)];

    public override void ApplyToQiskitCircuit(IQuantumCircuit circuit, StringBuilder stringBuilder)
    {
        var targetList = string.Join(",", targets.Select(t => t.QubitStringList));
        stringBuilder.AppendLine($"{circuit.Name}.barrier([{targetList}])");
    }
}
public class MultiBarrier(IEnumerable<IQuantumType> controls) : CircuitOperation
{
    public override IQuantumType Destination => null!;
    public override IEnumerable<QuantumRegister> RegistersInvolved => [..controls.Select(c => c.Register)];

    public override void ApplyToQiskitCircuit(IQuantumCircuit circuit, StringBuilder stringBuilder)
    {
        var controlList = string.Join(",", controls.Select(c => c.QubitStringList));
        stringBuilder.AppendLine($"{circuit.Name}.barrier([{controlList}])");
    }
}
public class BarrierAll() : CircuitOperation
{
    public override IQuantumType Destination => null!;
    public override IEnumerable<QuantumRegister> RegistersInvolved => [];

    public override void ApplyToQiskitCircuit(IQuantumCircuit circuit, StringBuilder stringBuilder)
    {
        stringBuilder.AppendLine($"{circuit.Name}.barrier()");
    }
}
public class MCP(IEnumerable<IQuantumType> controls, IQuantumType target, FloatType rotationAngle) : CircuitOperation
{
    public override IQuantumType Destination => target;
    public override IEnumerable<QuantumRegister> RegistersInvolved => [..controls.Select(c => c.Register), target.Register];

    public override void ApplyToQiskitCircuit(IQuantumCircuit circuit, StringBuilder stringBuilder)
    {
        var controlList = string.Join(",", controls.Select(c => c.QubitStringList));
        stringBuilder.AppendLine($"{circuit.Name}.mcp({rotationAngle.Value},[{controlList}],[{target.QubitStringList}])");
    }
}
public class MCX(IEnumerable<IQuantumType> controls, IQuantumType target) : CircuitOperation
{
    public override IQuantumType Destination => target;
    public override IEnumerable<QuantumRegister> RegistersInvolved => [..controls.Select(c => c.Register), target.Register];

    public override void ApplyToQiskitCircuit(IQuantumCircuit circuit, StringBuilder stringBuilder)
    {
        //TODO: qiskit doesn't handle case where both control and target are lists with more than 1 element. (true for all Multi Controlled Gate and Swap)
        var controlList = string.Join(",", controls.Select(c => c.QubitStringList));
        stringBuilder.AppendLine($"{circuit.Name}.mcx([{controlList}],[{target.QubitStringList}])");
    }
}
public class MCY(IEnumerable<IQuantumType> controls, IQuantumType target) : CircuitOperation
{
    public override IQuantumType Destination => target;
    public override IEnumerable<QuantumRegister> RegistersInvolved => [..controls.Select(c => c.Register), target.Register];

    public override void ApplyToQiskitCircuit(IQuantumCircuit circuit, StringBuilder stringBuilder)
    {
        var controlList = string.Join(",", controls.Select(c => c.QubitStringList));
        stringBuilder.AppendLine($"{circuit.Name}.mcy([{controlList}], [{target.QubitStringList}])");
    }
}
public class MCZ(IEnumerable<IQuantumType> controls, IQuantumType target) : CircuitOperation
{
    public override IQuantumType Destination => target;
    public override IEnumerable<QuantumRegister> RegistersInvolved => [..controls.Select(c => c.Register), target.Register];

    public override void ApplyToQiskitCircuit(IQuantumCircuit circuit, StringBuilder stringBuilder)
    {
        var controlList = string.Join(",", controls.Select(c => c.QubitStringList));
        stringBuilder.AppendLine($"{circuit.Name}.mcz([{controlList}], [{target.QubitStringList}])");
    }
}
public class Swap(IQuantumType a, IQuantumType b) : CircuitOperation
{
    public override IQuantumType Destination => a;
    public override IEnumerable<QuantumRegister> RegistersInvolved => [a.Register, b.Register];

    public override void ApplyToQiskitCircuit(IQuantumCircuit circuit, StringBuilder stringBuilder)
    {
        stringBuilder.AppendLine($"{circuit.Name}.swap([{a.QubitStringList}], [{b.QubitStringList}])");
    }
}
public class MultiSwap(IEnumerable<IQuantumType> controls, IQuantumType target) : CircuitOperation
{
    public override IQuantumType Destination => target;
    public override IEnumerable<QuantumRegister> RegistersInvolved => [..controls.Select(c => c.Register), target.Register];

    public override void ApplyToQiskitCircuit(IQuantumCircuit circuit, StringBuilder stringBuilder)
    {
        var controlList = string.Join(",", controls.Select(c => c.QubitStringList));
        stringBuilder.AppendLine($"{circuit.Name}.swap([{controlList}], [{target.QubitStringList}])");
    }
}
public class Or(IQuantumType a, IQuantumType b, IQuantumType destination) : CircuitOperation
{
    public override IQuantumType Destination => destination;
    public override IEnumerable<QuantumRegister> RegistersInvolved => [a.Register, b.Register, destination.Register];

    public override void ApplyToQiskitCircuit(IQuantumCircuit circuit, StringBuilder stringBuilder)
    {
        //TODO: implemement quantum OR operation.
    }
}
public class And(IQuantumType a, IQuantumType b, IQuantumType destination) : CircuitOperation
{
    public override IQuantumType Destination => destination;
    public override IEnumerable<QuantumRegister> RegistersInvolved => [a.Register, b.Register, destination.Register];

    public override void ApplyToQiskitCircuit(IQuantumCircuit circuit, StringBuilder stringBuilder)
    {
        //TODO: implemement quantum AND operation.
    }
}
public class Not(IQuantumType a, IQuantumType b, IQuantumType destination) : CircuitOperation
{
    public override IQuantumType Destination => destination;
    public override IEnumerable<QuantumRegister> RegistersInvolved => [a.Register, b.Register, destination.Register];

    public override void ApplyToQiskitCircuit(IQuantumCircuit circuit, StringBuilder stringBuilder)
    {
        //TODO: implemement quantum NOT operation.
    }
}
public class Equals(IQuantumType a, IQuantumType b, IQuantumType destination) : CircuitOperation
{
    public override IQuantumType Destination => destination;
    public override IEnumerable<QuantumRegister> RegistersInvolved => [a.Register, b.Register, destination.Register];

    public override void ApplyToQiskitCircuit(IQuantumCircuit circuit, StringBuilder stringBuilder)
    {
        //TODO: implemement quantum == operation.
    }
}
public class NotEquals(IQuantumType a, IQuantumType b, IQuantumType destination) : CircuitOperation
{
    public override IQuantumType Destination => destination;
    public override IEnumerable<QuantumRegister> RegistersInvolved => [a.Register, b.Register, destination.Register];

    public override void ApplyToQiskitCircuit(IQuantumCircuit circuit, StringBuilder stringBuilder)
    {
        //TODO: implemement quantum != operation.
    }
}
public class LowerThan(IQuantumType a, IQuantumType b, IQuantumType destination) : CircuitOperation
{
    public override IQuantumType Destination => destination;
    public override IEnumerable<QuantumRegister> RegistersInvolved => [a.Register, b.Register, destination.Register];

    public override void ApplyToQiskitCircuit(IQuantumCircuit circuit, StringBuilder stringBuilder)
    {
        //TODO: implemement quantum < operation.
    }
}
public class LowerEqualThan(IQuantumType a, IQuantumType b, IQuantumType destination) : CircuitOperation
{
    public override IQuantumType Destination => destination;
    public override IEnumerable<QuantumRegister> RegistersInvolved => [ a.Register,  b.Register,  destination.Register];

    public override void ApplyToQiskitCircuit(IQuantumCircuit circuit, StringBuilder stringBuilder)
    {
        //TODO: implemement quantum <= operation.
    }
}
public class GreaterThan(IQuantumType a, IQuantumType b, IQuantumType destination) : CircuitOperation
{
    public override IQuantumType Destination => destination;
    public override IEnumerable<QuantumRegister> RegistersInvolved => [ a.Register,  b.Register,  destination.Register];

    public override void ApplyToQiskitCircuit(IQuantumCircuit circuit, StringBuilder stringBuilder)
    {
        //TODO: implemement quantum > operation.
    }
}
public class GreaterEqualThan(IQuantumType a, IQuantumType b, IQuantumType destination) : CircuitOperation
{
    public override IQuantumType Destination => destination;
    public override IEnumerable<QuantumRegister> RegistersInvolved => [ a.Register,  b.Register,  destination.Register];

    public override void ApplyToQiskitCircuit(IQuantumCircuit circuit, StringBuilder stringBuilder)
    {
        //TODO: implemement quantum >= operation.
    }
}
public class RightShift : CircuitOperation
{
    private readonly IQuantumType a;
    private readonly QuintType offset;

    public override IQuantumType Destination => a;
    public override IEnumerable<QuantumRegister> RegistersInvolved => [a.Register, offset.Register];
    public RightShift(IQuantumType a, QuintType offset)
    {
        this.a = a;
        this.offset = offset;
    }
    public RightShift(IQuantumType a, IntType offset)
    {
        this.a = a;
        this.offset = new QuintType(offset.Value.ToString());
    }

    public override void ApplyToQiskitCircuit(IQuantumCircuit circuit, StringBuilder stringBuilder)
    {
        //TODO: implemement quantum >> operation.
    }
}
public class LeftShift : CircuitOperation
{
    private readonly IQuantumType a;
    private readonly QuintType offset;

    public override IQuantumType Destination => a;
    public override IEnumerable<QuantumRegister> RegistersInvolved => [ a.Register,  offset.Register];
    public LeftShift(IQuantumType a, QuintType offset)
    {
        this.a = a;
        this.offset = offset;
    }
    public LeftShift(IQuantumType a, IntType offset)
    {
        this.a = a;
        this.offset = new QuintType(offset.Value.ToString());
    }

    public override void ApplyToQiskitCircuit(IQuantumCircuit circuit, StringBuilder stringBuilder)
    {
        //TODO: implemement quantum >> operation.
    }
}
public class Addition(IQuantumType a, IQuantumType b, IQuantumType destination) : CircuitOperation
{
    public override IQuantumType Destination => destination;
    public override IEnumerable<QuantumRegister> RegistersInvolved => [ a.Register,  b.Register,  destination.Register];

    public override void ApplyToQiskitCircuit(IQuantumCircuit circuit, StringBuilder stringBuilder)
    {
        //TODO: implemement quantum sum operation.
    }
}
public class Subtraction(IQuantumType a, IQuantumType b, IQuantumType destination) : CircuitOperation
{
    public override IQuantumType Destination => destination;
    public override IEnumerable<QuantumRegister> RegistersInvolved => [ a.Register,  b.Register,  destination.Register];

    public override void ApplyToQiskitCircuit(IQuantumCircuit circuit, StringBuilder stringBuilder)
    {
        //TODO: implemement quantum subtraction operation.
    }
}
public class Multiply(IQuantumType a, IQuantumType b, IQuantumType destination) : CircuitOperation
{
    public override IQuantumType Destination => destination;
    public override IEnumerable<QuantumRegister> RegistersInvolved => [ a.Register,  b.Register,  destination.Register];

    public override void ApplyToQiskitCircuit(IQuantumCircuit circuit, StringBuilder stringBuilder)
    {
        //TODO: implemement quantum Multiply operation.
    }
}
public class Divide(IQuantumType a, IQuantumType b, IQuantumType destination) : CircuitOperation
{
    public override IQuantumType Destination => destination;
    public override IEnumerable<QuantumRegister> RegistersInvolved => [ a.Register,  b.Register,  destination.Register];

    public override void ApplyToQiskitCircuit(IQuantumCircuit circuit, StringBuilder stringBuilder)
    {
        //TODO: implemement quantum Divide operation.
    }
}
public class Module(IQuantumType a, IQuantumType b, IQuantumType destination) : CircuitOperation
{
    public override IQuantumType Destination => destination;
    public override IEnumerable<QuantumRegister> RegistersInvolved => [ a.Register,  b.Register,  destination.Register];

    public override void ApplyToQiskitCircuit(IQuantumCircuit circuit, StringBuilder stringBuilder)
    {
        //TODO: implemement quantum Module operation.
    }
}
public class Opposite(IQuantumType a, IQuantumType destination) : CircuitOperation
{
    public override IQuantumType Destination => destination;
    public override IEnumerable<QuantumRegister> RegistersInvolved => [ a.Register,  destination.Register];

    public override void ApplyToQiskitCircuit(IQuantumCircuit circuit, StringBuilder stringBuilder)
    {
        //TODO: implemement quantum Opposite operation.
    }
}
public class Increment(IQuantumType a, IQuantumType destination, int amount = 1) : CircuitOperation
{
    public override IQuantumType Destination => destination;
    public override IEnumerable<QuantumRegister> RegistersInvolved => [ a.Register,  destination.Register];

    public override void ApplyToQiskitCircuit(IQuantumCircuit circuit, StringBuilder stringBuilder)
    {
        //TODO: implemement quantum Increment operation.
    }
}
public class Decrement(IQuantumType a, IQuantumType destination, int amount = 1) : CircuitOperation
{
    public override IQuantumType Destination => destination;
    public override IEnumerable<QuantumRegister> RegistersInvolved => [ a.Register,  destination.Register];

    public override void ApplyToQiskitCircuit(IQuantumCircuit circuit, StringBuilder stringBuilder)
    {
        //TODO: implemement quantum Decrement operation.
    }
}
