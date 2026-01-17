using QutesLang.Symbols.Types;

namespace QutesLang.GrammarFrontend;

public class ClassicalRegister(int size)
{
    public string? Name { get; set; }
    public int Size { get; set; } = size;
}

public class QuantumRegister
{
    public QuantumRegister(int size, StateVector? initialStateVector = null)
    {
        Qubits = Enumerable.Range(0, size).Select(i => new CircuitQubit()).ToList();
        InitialStateVector = initialStateVector;
        ClassicalRegister = new(Qubits.Count);
    }

    public QuantumRegister(IEnumerable<QuantumRegister> registers)
    {
        Registers = registers.ToList();
        Qubits = registers.SelectMany(r => r.Qubits).ToList();
        InitialStateVector = null;
        ClassicalRegister = new (Qubits.Count);
    }

    public string? Name { get; set { field = value; ClassicalRegister.Name = $"c_{value}"; } }
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
}
