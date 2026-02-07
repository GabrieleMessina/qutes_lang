using QutesLang.QuantumCircuits;

namespace QutesLang.Symbols.Types.Interfaces;

public interface IQuantumValue : IQutesValue
{
    public int QubitCount { get; }
    public QuantumRegister Register { get; }
    public string QubitStringList { get; }
}