using System.Text;

using QutesLang.Symbols.Types;

namespace QutesLang.GrammarFrontend;

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

public class Not(IQuantumValue target) : CircuitOperation([target.Register], target)
{
    public override void ApplyToQiskitCircuit(IQuantumCircuit circuit, StringBuilder stringBuilder)
    {
        stringBuilder.AppendLine($"{circuit.Name}.x([{Destination.QubitStringList}])");
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
