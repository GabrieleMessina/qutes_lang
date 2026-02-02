using System.Text;

using QutesLang.Symbols.Types;

namespace QutesLang.GrammarFrontend;

public class Or(IQuantumValue a, IQuantumValue b, IQuantumValue destination) : CircuitOperation([a.Register, b.Register, destination.Register], destination)
{
    public override void ApplyToQiskitCircuit(IQuantumCircuit circuit, StringBuilder stringBuilder)
    {
        var size = a.Size + b.Size;
        var gateName = "or_gate_" + size;
        stringBuilder.AppendLine($"{gateName} = OrGate({size})");
        AddGateInCircuit(circuit, gateName, [.. a.Register.Qubits, .. b.Register.Qubits, .. Destination.Register.Qubits], stringBuilder);
    }
}

public class And(IQuantumValue a, IQuantumValue b, IQuantumValue destination) : CircuitOperation([a.Register, b.Register, destination.Register], destination)
{
    public override void ApplyToQiskitCircuit(IQuantumCircuit circuit, StringBuilder stringBuilder)
    {
        var size = a.Size + b.Size;
        var gateName = "and_gate_" + size;
        stringBuilder.AppendLine($"{gateName} = AndGate({size})");
        AddGateInCircuit(circuit, gateName, [.. a.Register.Qubits, .. b.Register.Qubits, .. Destination.Register.Qubits], stringBuilder);
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
