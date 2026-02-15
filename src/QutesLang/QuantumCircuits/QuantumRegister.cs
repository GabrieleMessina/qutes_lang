using QutesLang.Symbols.Types;

namespace QutesLang.QuantumCircuits;

public class QuantumRegister
{
    public QuantumRegister(int size, StateVector? initialStateVector = null)
    {
        Qubits = Enumerable.Range(0, size).ToList().Select(i => CircuitQubitPool.Acquire()).ToList();
        InitialStateVector = initialStateVector;
        ClassicalRegister = new(this);
    }

    public QuantumRegister(IEnumerable<QuantumRegister> registers)
    {
        Registers = registers.ToList();
        Qubits = registers.SelectMany(r => r.Qubits).ToList();
        CircuitQubitPool.Acquire(Qubits);
        InitialStateVector = null;
        ClassicalRegister = new(this);
    }

    public string Name { get; set; } = VariableNameGuid.New("qreg");

    /// <summary>
    /// The size of the quantum register, in qubits. If this QuantumRegister encodes an array type, this is the total size of all qubits in all sub-registers.
    /// </summary>
    public int Size => Qubits.Count;

    /// <summary>
    /// The classical register associated with this quantum register, used to store measurement results. If this QuantumRegister encodes an array type, this is the classical register associated with the entire array.
    /// </summary>
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

    /// <summary>
    /// 0 reference by default, incremented only when assigned.
    /// </summary>
    private readonly AccessCounter anyReferenceToRegister = new (); 

    public IEnumerable<CircuitQubit> Free()
    {
        anyReferenceToRegister.Decrement();
        if(!anyReferenceToRegister)
        {
            return CircuitQubitPool.Free(Qubits);
        }
        return [];
    }

    public void Retain()
    {
        anyReferenceToRegister.Increment();
    }

    public string QubitStringList => $"{string.Join(",", Qubits.Select(c => c!.Id))}";

    public override string ToString()
    {
        return $"QReg.{Name}{{{QubitStringList}}}";
    }
}
