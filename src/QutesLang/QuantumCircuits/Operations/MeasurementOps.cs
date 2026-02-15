using System.Text;

using QutesLang.QuantumCircuits.Interfaces;
using QutesLang.Symbols.Types.Interfaces;

namespace QutesLang.QuantumCircuits.Operations;

public class Measure(IQuantumValue target) : CircuitOperation([target.Register], target)
{
    public override void ApplyQiskitRequirements(StringBuilder stringBuilder)
    {
        //TODO: all operations (or the more complex ones), could declare their gates.
        // This way we can have better circuit printing and also reuse gates (in the future).
        // Note that the gate reuse is possibile only for input of the same kind,
        // So we could have for example Measure_qubit and Measure_quinteger gates.
    }

    public override void ApplyToQiskitCircuit(IQuantumCircuit circuit, StringBuilder stringBuilder)
    {
        stringBuilder.AppendLine($"{circuit.Name}.measure({Destination.Register.Name}, {Destination.Register.ClassicalRegister.Name})");
    }
}

public class MultiMeasure(IEnumerable<IQuantumValue> targets) : CircuitOperation([.. targets.Select(c => c.Register)], null!)
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
        foreach (var register in circuit.LocalRegisters)
        {
            stringBuilder.AppendLine($"{circuit.Name}.measure({register.Name}, {register.ClassicalRegister.Name})");
        }
    }
}

public class Barrier(IEnumerable<IQuantumValue> targets) : CircuitOperation([.. targets.Select(t => t.Register)], null!)
{
    public override void ApplyToQiskitCircuit(IQuantumCircuit circuit, StringBuilder stringBuilder)
    {
        var targetList = string.Join(",", targets.Select(t => t.QubitStringList));
        stringBuilder.AppendLine($"{circuit.Name}.barrier([{targetList}])");
    }
}

public class MultiBarrier(IEnumerable<IQuantumValue> controls) : CircuitOperation([.. controls.Select(c => c.Register)], null!)
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
