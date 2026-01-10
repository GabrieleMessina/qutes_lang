using QutesLang.GrammarFrontend;

namespace QutesLang.Symbols.Types;

public interface IQuantumType : IQutesValue
{
    public int Size { get; }
    public QuantumRegister Register { get; }
    public string QubitStringList => Register.QubitStringList;

    #region Operations
    CircuitOperation LeftShift(QuintValue positions) => throw new InvalidOperationException($"Operator {nameof(LeftShift)} cannot be applied to {this.Type} and {positions.Type}.");
    CircuitOperation RightShift(QuintValue positions) => throw new InvalidOperationException($"Operator {nameof(RightShift)} cannot be applied to {this.Type} and {positions.Type}.");
    CircuitOperation Swap(IQuantumType term)
    {
        return this.Type == term.Type
            ? new Swap(this, term)
            : throw new InvalidOperationException($"Operator {nameof(Swap)} cannot be applied to {this.Type} and {term.Type}.");
    }

    // Arithmetic operations
    CircuitOperation Addition(IQuantumType term) => throw new InvalidOperationException($"Operator {nameof(Addition)} cannot be applied to {this.Type} and {term.Type}.");
    CircuitOperation Subtraction(IQuantumType term) => throw new InvalidOperationException($"Operator {nameof(Subtraction)} cannot be applied to {this.Type} and {term.Type}.");
    CircuitOperation Multiply(IQuantumType term) => throw new InvalidOperationException($"Operator {nameof(Multiply)} cannot be applied to {this.Type} and {term.Type}.");
    CircuitOperation Divide(IQuantumType term) => throw new InvalidOperationException($"Operator {nameof(Divide)} cannot be applied to {this.Type} and {term.Type}.");
    CircuitOperation Module(IQuantumType term) => throw new InvalidOperationException($"Operator {nameof(Module)} cannot be applied to {this.Type} and {term.Type}.");
    CircuitOperation Exp(IQuantumType term) => throw new InvalidOperationException($"Operator {nameof(Exp)} cannot be applied to {this.Type} and {term.Type}.");

    // Comparison operations
    CircuitOperation LowerThan(IQuantumType term) => throw new InvalidOperationException($"Operator {nameof(LowerThan)} cannot be applied to {this.Type} and {term.Type}.");
    CircuitOperation LowerEqualThan(IQuantumType term) => throw new InvalidOperationException($"Operator {nameof(LowerEqualThan)} cannot be applied to {this.Type} and {term.Type}.");
    CircuitOperation GreaterThan(IQuantumType term) => throw new InvalidOperationException($"Operator {nameof(GreaterThan)} cannot be applied to {this.Type} and {term.Type}.");
    CircuitOperation GreaterEqualThan(IQuantumType term) => throw new InvalidOperationException($"Operator {nameof(GreaterEqualThan)} cannot be applied to {this.Type} and {term.Type}.");
    CircuitOperation Equals(IQuantumType term)
    {
        if (this.Type != term.Type)
            throw new InvalidOperationException($"Operator {nameof(Equals)} cannot be applied to {this.Type} and {term.Type}.");
        return new Equals(this, term, this);
    }
    CircuitOperation NotEquals(IQuantumType term)
    {
        if (this.Type != term.Type)
            throw new InvalidOperationException($"Operator {nameof(NotEquals)} cannot be applied to {this.Type} and {term.Type}.");
        return new NotEquals(this, term, this);
    }

    // Logical operations
    CircuitOperation And(IQuantumType term) => throw new InvalidOperationException($"Operator {nameof(And)} cannot be applied to {this.Type} and {term.Type}.");
    CircuitOperation Or(IQuantumType term) => throw new InvalidOperationException($"Operator {nameof(Or)} cannot be applied to {this.Type} and {term.Type}.");
    CircuitOperation Not() => throw new InvalidOperationException($"Operator {nameof(Not)} cannot be applied to {this.Type}.");

    // Unary operations
    CircuitOperation Plus() => new Empty(this);
    CircuitOperation Minus() => throw new InvalidOperationException($"Operator {nameof(Minus)} cannot be applied to {this.Type}.");
    CircuitOperation InplacePreIncrement() => throw new InvalidOperationException($"Operator {nameof(InplacePreIncrement)} cannot be applied to {this.Type}.");
    CircuitOperation InplacePostIncrement() => throw new InvalidOperationException($"Operator {nameof(InplacePostIncrement)} cannot be applied to {this.Type}.");
    CircuitOperation InplacePreDecrement() => throw new InvalidOperationException($"Operator {nameof(InplacePreDecrement)} cannot be applied to {this.Type}.");   
    CircuitOperation InplacePostDecrement() => throw new InvalidOperationException($"Operator {nameof(InplacePostDecrement)} cannot be applied to {this.Type}.");   
    #endregion Operations
}