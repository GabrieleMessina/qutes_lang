namespace QutesLang.QuantumCircuits;

public static class CircuitQubitPool
{
    private static readonly Dictionary<CircuitQubit, int> QubitReferences = [];
    
    /// <summary>
    /// Acquires a qubit from the pool incrementing its reference counter.
    /// </summary>
    /// <returns>The acquired qubit.</returns>
    public static CircuitQubit Acquire()
    {
        var qubit = QubitReferences.FirstOrDefault(r => r.Value == 0).Key ?? new();
        QubitReferences.TryAdd(qubit, 0);
        QubitReferences[qubit]++;
        return qubit;
    }

    /// <summary>
    /// Acquires multiple qubits from the pool.
    /// This only increments reference counter, the qubits are assumed to be already in the pool.
    /// </summary>
    /// <param name="qubits">The qubits to acquire.</param>
    public static void Acquire(IEnumerable<CircuitQubit> qubits)
    {
        foreach (var qubit in qubits)
        {
            QubitReferences[qubit]++;
        }
    }

    /// <summary>
    /// Releases a qubit back to the pool.
    /// </summary>
    /// <param name="qubit">The qubit to release.</param>
    /// <returns>True if the qubit was released, false otherwise.</returns>
    public static bool Free(CircuitQubit qubit)
    {
        QubitReferences[qubit]--;
        return QubitReferences[qubit] == 0;
    }
    
    /// <summary>
    /// Releases multiple qubits back to the pool.
    /// </summary>
    /// <param name="qubits">The qubits to release.</param>
    /// <returns>The qubits that were released.</returns>
    public static IEnumerable<CircuitQubit> Free(IEnumerable<CircuitQubit> qubits)
    {
        var freedQubit = new List<CircuitQubit>();
        foreach (var qubit in qubits)
        {
            if(Free(qubit)) freedQubit.Add(qubit);
        }
        return freedQubit;
    }
}
