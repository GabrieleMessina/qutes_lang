using QutesLang.GrammarFrontend;

namespace QutesLang.Symbols.Types;

public interface IQuantumType : IQutesType
{
    public int Size { get; }
    public QuantumRegister Register { get; }
    public string QubitStringList => $"{string.Join(",", Register.Qubits.Select(c => c!.Id))}";

    #region Operations
    CircuitOperation LeftShift(QuintType positions) => throw new InvalidOperationException($"Operator {nameof(LeftShift)} cannot be applied to {this.GetType().Name} and {positions.GetType().Name}.");
    CircuitOperation RightShift(QuintType positions) => throw new InvalidOperationException($"Operator {nameof(RightShift)} cannot be applied to {this.GetType().Name} and {positions.GetType().Name}.");
    CircuitOperation Swap(IQuantumType term)
    {
        return this.GetType() == term.GetType()
            ? new Swap(this, term)
            : throw new InvalidOperationException($"Operator {nameof(Swap)} cannot be applied to {this.GetType().Name} and {term.GetType().Name}.");
    }

    // Arithmetic operations
    CircuitOperation Addition(IQuantumType term) => throw new InvalidOperationException($"Operator {nameof(Addition)} cannot be applied to {this.GetType().Name} and {term.GetType().Name}.");
    CircuitOperation Subtraction(IQuantumType term) => throw new InvalidOperationException($"Operator {nameof(Subtraction)} cannot be applied to {this.GetType().Name} and {term.GetType().Name}.");
    CircuitOperation Multiply(IQuantumType term) => throw new InvalidOperationException($"Operator {nameof(Multiply)} cannot be applied to {this.GetType().Name} and {term.GetType().Name}.");
    CircuitOperation Divide(IQuantumType term) => throw new InvalidOperationException($"Operator {nameof(Divide)} cannot be applied to {this.GetType().Name} and {term.GetType().Name}.");
    CircuitOperation Module(IQuantumType term) => throw new InvalidOperationException($"Operator {nameof(Module)} cannot be applied to {this.GetType().Name} and {term.GetType().Name}.");

    // Comparison operations
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

    // Logical operations
    CircuitOperation And(IQuantumType term) => throw new InvalidOperationException($"Operator {nameof(And)} cannot be applied to {this.GetType().Name} and {term.GetType().Name}.");
    CircuitOperation Or(IQuantumType term) => throw new InvalidOperationException($"Operator {nameof(Or)} cannot be applied to {this.GetType().Name} and {term.GetType().Name}.");
    CircuitOperation Not() => throw new InvalidOperationException($"Operator {nameof(Not)} cannot be applied to {this.GetType().Name}.");

    // Unary operations
    CircuitOperation Plus() => new Empty(this);
    CircuitOperation Minus() => throw new InvalidOperationException($"Operator {nameof(Minus)} cannot be applied to {this.GetType().Name}.");
    CircuitOperation InplacePreIncrement() => throw new InvalidOperationException($"Operator {nameof(InplacePreIncrement)} cannot be applied to {this.GetType().Name}.");
    CircuitOperation InplacePostIncrement() => throw new InvalidOperationException($"Operator {nameof(InplacePostIncrement)} cannot be applied to {this.GetType().Name}.");
    CircuitOperation InplacePreDecrement() => throw new InvalidOperationException($"Operator {nameof(InplacePreDecrement)} cannot be applied to {this.GetType().Name}.");   
    CircuitOperation InplacePostDecrement() => throw new InvalidOperationException($"Operator {nameof(InplacePostDecrement)} cannot be applied to {this.GetType().Name}.");   
    #endregion Operations
}