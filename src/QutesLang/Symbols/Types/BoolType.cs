using QutesLang.GrammarFrontend;

namespace QutesLang.Symbols.Types;

//todo: rename al type suffix to value?

public class ClassType(string qualifiedClassName) : IQutesType
{
}


public class BoolType(bool value) : IClassicalType
{
    public bool Value { get; set; } = value;

    public object GetValueAsObject() => Value;
    public static BoolType GetDefaultValue() => new(false);

    public IQutesType LShift(IntType positions) => null!;

    public IQutesType RShift(IntType positions) => null!;

    public IQutesType Swap(IClassicalType positions) => null!;

    public IQutesType Addition(IClassicalType term) => null!;

    public IQutesType Subtraction(IClassicalType term) => null!;

    public BoolType LowerThan(IClassicalType term) => null!;

    public BoolType LowerEqualThan(IClassicalType term) => null!;

    public BoolType GreaterThan(IClassicalType term) => null!;

    public BoolType GreaterEqualThan(IClassicalType term) => null!;

    public BoolType Equals(IClassicalType term) => null!;

    public BoolType NotEquals(IClassicalType term) => null!;

    public BoolType And(IClassicalType term) => null!;

    public BoolType Or(IClassicalType term) => null!;
}

public class IntType(int value) : IClassicalType
{
    public int Value { get; set; } = value;
    public object GetValueAsObject() => Value;
    public static IntType GetDefaultValue() => new(0);

    public IQutesType LShift(IntType positions) => null!;

    public IQutesType RShift(IntType positions) => null!;

    public IQutesType Swap(IClassicalType positions) => null!;

    public IQutesType Addition(IClassicalType term) => null!;

    public IQutesType Subtraction(IClassicalType term) => null!;

    public BoolType LowerThan(IClassicalType term) => null!;

    public BoolType LowerEqualThan(IClassicalType term) => null!;

    public BoolType GreaterThan(IClassicalType term) => null!;

    public BoolType GreaterEqualThan(IClassicalType term) => null!;

    public BoolType Equals(IClassicalType term) => null!;

    public BoolType NotEquals(IClassicalType term) => null!;

    public BoolType And(IClassicalType term) => null!;

    public BoolType Or(IClassicalType term) => null!;
}

public class FloatType(float value) : IClassicalType
{
    public float Value { get; set; } = value;
    public object GetValueAsObject() => Value;
    public static FloatType GetDefaultValue() => new(0f);

    public IQutesType LShift(IntType positions) => null!;

    public IQutesType RShift(IntType positions) => null!;

    public IQutesType Swap(IClassicalType positions) => null!;

    public IQutesType Addition(IClassicalType term) => null!;

    public IQutesType Subtraction(IClassicalType term) => null!;

    public BoolType LowerThan(IClassicalType term) => null!;

    public BoolType LowerEqualThan(IClassicalType term) => null!;

    public BoolType GreaterThan(IClassicalType term) => null!;

    public BoolType GreaterEqualThan(IClassicalType term) => null!;

    public BoolType Equals(IClassicalType term) => null!;

    public BoolType NotEquals(IClassicalType term) => null!;

    public BoolType And(IClassicalType term) => null!;

    public BoolType Or(IClassicalType term) => null!;
}

public class StringType(string value) : IClassicalType
{
    public string Value { get; set; } = value;
    public object GetValueAsObject() => Value;
    public static StringType GetDefaultValue() => new("");

    public IQutesType LShift(IntType positions) => null!;

    public IQutesType RShift(IntType positions) => null!;

    public IQutesType Swap(IClassicalType positions) => null!;

    public IQutesType Addition(IClassicalType term) => null!;

    public IQutesType Subtraction(IClassicalType term) => null!;

    public BoolType LowerThan(IClassicalType term) => null!;

    public BoolType LowerEqualThan(IClassicalType term) => null!;

    public BoolType GreaterThan(IClassicalType term) => null!;

    public BoolType GreaterEqualThan(IClassicalType term) => null!;

    public BoolType Equals(IClassicalType term) => null!;

    public BoolType NotEquals(IClassicalType term) => null!;

    public BoolType And(IClassicalType term) => null!;

    public BoolType Or(IClassicalType term) => null!;
}

public class ClassicalArrayType(IEnumerable<Symbol> values) : IClassicalType
{
    public IEnumerable<Symbol> Values { get; } = values;
    public object GetValueAsObject() => Values;
    public static ClassicalArrayType GetDefaultValue() => new([]);

    public IQutesType LShift(IntType positions) => null!;

    public IQutesType RShift(IntType positions) => null!;

    public IQutesType Swap(IClassicalType positions) => null!;

    public IQutesType Addition(IClassicalType term) => null!;

    public IQutesType Subtraction(IClassicalType term) => null!;

    public BoolType LowerThan(IClassicalType term) => null!;

    public BoolType LowerEqualThan(IClassicalType term) => null!;

    public BoolType GreaterThan(IClassicalType term) => null!;

    public BoolType GreaterEqualThan(IClassicalType term) => null!;

    public BoolType Equals(IClassicalType term) => null!;

    public BoolType NotEquals(IClassicalType term) => null!;

    public BoolType And(IClassicalType term) => null!;

    public BoolType Or(IClassicalType term) => null!;
}

public class QubitType(string initialValue) : IQuantumType
{
    public int Size { get => throw new NotImplementedException(); set => throw new NotImplementedException(); }
    public IEnumerable<CircuitQubit?> Qubits { get => throw new NotImplementedException(); set => throw new NotImplementedException(); }

    public static QubitType GetDefaultValue() => new ("0q");

    public CircuitOperation Addition(IQuantumType term) => null!;

    public CircuitOperation And(IQuantumType positions) => null!;

    public CircuitOperation Equals(IQuantumType positions) => null!;

    public CircuitOperation GreaterEqualThan(IQuantumType term) => null!;

    public CircuitOperation GreaterThan(IQuantumType term) => null!;

    public CircuitOperation LowerEqualThan(IQuantumType term) => null!;

    public CircuitOperation LowerThan(IQuantumType term) => null!;

    public CircuitOperation LShift(QuintType positions) => null!;

    public CircuitOperation NotEquals(IQuantumType positions) => null!;

    public CircuitOperation Or(IQuantumType positions) => null!;

    public CircuitOperation RShift(QuintType positions) => null!;

    public CircuitOperation Subtraction(IQuantumType term) => null!;

    public CircuitOperation Swap(IQuantumType positions) => null!;
}

public class QuintType(string initialValue) : IQuantumType
{
    public int Size { get => throw new NotImplementedException(); set => throw new NotImplementedException(); }
    public IEnumerable<CircuitQubit?> Qubits { get => throw new NotImplementedException(); set => throw new NotImplementedException(); }

    public static QuintType GetDefaultValue() => new ("0q");

    public CircuitOperation Addition(IQuantumType term) => null!;

    public CircuitOperation And(IQuantumType positions) => null!;

    public CircuitOperation Equals(IQuantumType positions) => null!;

    public CircuitOperation GreaterEqualThan(IQuantumType term) => null!;

    public CircuitOperation GreaterThan(IQuantumType term) => null!;

    public CircuitOperation LowerEqualThan(IQuantumType term) => null!;

    public CircuitOperation LowerThan(IQuantumType term) => null!;

    public CircuitOperation LShift(QuintType positions) => null!;

    public CircuitOperation NotEquals(IQuantumType positions) => null!;

    public CircuitOperation Or(IQuantumType positions) => null!;

    public CircuitOperation RShift(QuintType positions) => null!;

    public CircuitOperation Subtraction(IQuantumType term) => null!;

    public CircuitOperation Swap(IQuantumType positions) => null!;
}

public class QustringType(string initialValue) : IQuantumType
{
    public int Size { get => throw new NotImplementedException(); set => throw new NotImplementedException(); }
    public IEnumerable<CircuitQubit?> Qubits { get => throw new NotImplementedException(); set => throw new NotImplementedException(); }

    public static QustringType GetDefaultValue() => new ("0");

    public CircuitOperation Addition(IQuantumType term) => null!;

    public CircuitOperation And(IQuantumType positions) => null!;

    public CircuitOperation Equals(IQuantumType positions) => null!;

    public CircuitOperation GreaterEqualThan(IQuantumType term) => null!;

    public CircuitOperation GreaterThan(IQuantumType term) => null!;

    public CircuitOperation LowerEqualThan(IQuantumType term) => null!;

    public CircuitOperation LowerThan(IQuantumType term) => null!;

    public CircuitOperation LShift(QuintType positions) => null!;

    public CircuitOperation NotEquals(IQuantumType positions) => null!;

    public CircuitOperation Or(IQuantumType positions) => null!;

    public CircuitOperation RShift(QuintType positions) => null!;

    public CircuitOperation Subtraction(IQuantumType term) => null!;

    public CircuitOperation Swap(IQuantumType positions) => null!;
}

public class QuantumArrayType(IEnumerable<Symbol> values) : IQuantumType
{
    public int Size { get => throw new NotImplementedException(); set => throw new NotImplementedException(); }
    public IEnumerable<CircuitQubit?> Qubits { get => throw new NotImplementedException(); set => throw new NotImplementedException(); }

    public static QuantumArrayType GetDefaultValue() => new([]);

    public CircuitOperation Addition(IQuantumType term) => null!;

    public CircuitOperation And(IQuantumType positions) => null!;

    public CircuitOperation Equals(IQuantumType positions) => null!;

    public CircuitOperation GreaterEqualThan(IQuantumType term) => null!;

    public CircuitOperation GreaterThan(IQuantumType term) => null!;

    public CircuitOperation LowerEqualThan(IQuantumType term) => null!;

    public CircuitOperation LowerThan(IQuantumType term) => null!;

    public CircuitOperation LShift(QuintType positions) => null!;

    public CircuitOperation NotEquals(IQuantumType positions) => null!;

    public CircuitOperation Or(IQuantumType positions) => null!;

    public CircuitOperation RShift(QuintType positions) => null!;

    public CircuitOperation Subtraction(IQuantumType term) => null!;

    public CircuitOperation Swap(IQuantumType positions) => null!;
}