using QutesLang.GrammarFrontend;

namespace QutesLang.Symbols.Types;

public interface IQuantumType : IQutesType
{
    public int Size { get; }
    public IEnumerable<CircuitQubit?> Qubits { get; }
    public string QubitStringList => $"[{string.Join(",", Qubits.Select(c => c!.Id))}]";

    #region Operations
    CircuitOperation LeftShift(QuintType positions) => throw new InvalidOperationException($"Operator {nameof(LeftShift)} cannot be applied to {this.GetType().Name} and {positions.GetType().Name}.");
    CircuitOperation RightShift(QuintType positions) => throw new InvalidOperationException($"Operator {nameof(RightShift)} cannot be applied to {this.GetType().Name} and {positions.GetType().Name}.");
    CircuitOperation Swap(IQuantumType term)
    {
        return this.GetType() == term.GetType()
            ? new Swap(this, term)
            : throw new InvalidOperationException($"Operator {nameof(Swap)} cannot be applied to {this.GetType().Name} and {term.GetType().Name}.");
    }

    CircuitOperation Addition(IQuantumType term) => throw new InvalidOperationException($"Operator {nameof(Addition)} cannot be applied to {this.GetType().Name} and {term.GetType().Name}.");
    CircuitOperation Subtraction(IQuantumType term) => throw new InvalidOperationException($"Operator {nameof(Subtraction)} cannot be applied to {this.GetType().Name} and {term.GetType().Name}.");

    CircuitOperation LowerThan(IQuantumType term) => throw new InvalidOperationException($"Operator {nameof(LowerThan)} cannot be applied to {this.GetType().Name} and {term.GetType().Name}.");
    CircuitOperation LowerEqualThan(IQuantumType term) => throw new InvalidOperationException($"Operator {nameof(LowerEqualThan)} cannot be applied to {this.GetType().Name} and {term.GetType().Name}.");
    CircuitOperation GreaterThan(IQuantumType term) => throw new InvalidOperationException($"Operator {nameof(GreaterThan)} cannot be applied to {this.GetType().Name} and {term.GetType().Name}.");
    CircuitOperation GreaterEqualThan(IQuantumType term) => throw new InvalidOperationException($"Operator {nameof(GreaterEqualThan)} cannot be applied to {this.GetType().Name} and {term.GetType().Name}.");

    CircuitOperation Equals(IQuantumType term)
    {
        if (this.GetType() != term.GetType())
            throw new InvalidOperationException($"Operator {nameof(Equals)} cannot be applied to {this.GetType().Name} and {term.GetType().Name}.");
        return new Equals(this, term, this);
    }
    CircuitOperation NotEquals(IQuantumType term)
    {
        if (this.GetType() != term.GetType())
            throw new InvalidOperationException($"Operator {nameof(NotEquals)} cannot be applied to {this.GetType().Name} and {term.GetType().Name}.");
        return new NotEquals(this, term, this);
    }

    CircuitOperation And(IQuantumType term) => throw new InvalidOperationException($"Operator {nameof(And)} cannot be applied to {this.GetType().Name} and {term.GetType().Name}.");
    CircuitOperation Or(IQuantumType term) => throw new InvalidOperationException($"Operator {nameof(Or)} cannot be applied to {this.GetType().Name} and {term.GetType().Name}.");
    #endregion Operations
}