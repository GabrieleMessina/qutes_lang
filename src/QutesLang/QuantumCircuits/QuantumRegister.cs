using QutesLang.Symbols.Types;

namespace QutesLang.GrammarFrontend;

public class ClassicalRegister(QuantumRegister quantumRegister)
{
    public string Name => $"c_{QuantumRegister.Name}";
    public int Size { get; set; } = quantumRegister.Qubits.Count;
    public QuantumRegister QuantumRegister { get; } = quantumRegister;
}

public class QuantumRegister
{
    public QuantumRegister(int size, StateVector? initialStateVector = null)
    {
        Qubits = Enumerable.Range(0, size).Select(i => new CircuitQubit()).ToList();
        InitialStateVector = initialStateVector;
        ClassicalRegister = new(this);
    }

    public QuantumRegister(IEnumerable<QuantumRegister> registers)
    {
        Registers = registers.ToList();
        Qubits = registers.SelectMany(r => r.Qubits).ToList();
        InitialStateVector = null;
        ClassicalRegister = new(this);
    }

    public string Name { get; set; } = VariableNameGuid.New("qreg");
    public ClassicalRegister ClassicalRegister { get; set; }

    /// <summary>
    /// Contains all qubits in this quantum register or, if this encodes an array type, all qubits in all sub-registers.
    /// </summary>
    public List<CircuitQubit> Qubits { get; }

    /// <summary>
    /// This is only set if this QuantumRegister instance encodes an array type.
    /// Gets the collection of quantum registers that compose the array, or null.
    /// </summary>
    public ICollection<QuantumRegister>? Registers { get; }

    /// <summary>
    /// Contains the initial state vector to which the qubits in this register should be initialized.
    /// </summary>
    public StateVector? InitialStateVector { get; set; }

    public string QubitStringList => $"{string.Join(",", Qubits.Select(c => c!.Id))}";

    public override string ToString()
    {
        return $"QReg.{Name}{{{QubitStringList}}}";
    }
}
