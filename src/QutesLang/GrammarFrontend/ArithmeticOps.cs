using System.Text;

using QutesLang.Symbols.Types;

namespace QutesLang.GrammarFrontend;

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
    private string GateName => $"adder_{size}";

    public override void ApplyQiskitRequirements(StringBuilder stringBuilder)
    {
        stringBuilder.AppendLine($"{GateName} = ModularAdderGate({size})");
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
    private readonly int size = Math.Min(a.Size, b.Size);

    public override void ApplyQiskitRequirements(StringBuilder stringBuilder)
    {
        var gateName = $"multiplier_{size}";
        stringBuilder.AppendLine($"{gateName} = MultiplierGate(num_state_qubits = {size}, num_result_qubits = {size})"); //We don't handle overflow
    }

    public override void ApplyToQiskitCircuit(IQuantumCircuit circuit, StringBuilder stringBuilder)
    {
        if (a == Destination || b == Destination || a == b)
        {
            throw new InvalidOperationException("Multiply must be executed on 3 different registers.");
        }

        var gateName = $"multiplier_{size}";
        //TODO: gate crash if num_result_qubits is not 2*num_state_qubits, we need a way to make the computation and then drop qubits.
        AddGateInCircuit(circuit, gateName, [.. a.Register.Qubits[..size], .. b.Register.Qubits[..size], .. Destination.Register.Qubits[..size]], stringBuilder);
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
