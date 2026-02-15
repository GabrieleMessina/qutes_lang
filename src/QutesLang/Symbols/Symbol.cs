using QutesLang.QuantumCircuits.Interfaces;
using QutesLang.Symbols.Types;
using QutesLang.Symbols.Types.Interfaces;

using static Qutes.Grammar.qutes_parser;

namespace QutesLang.Symbols;

//Scope reference and AST token index could be useful in the future for error reporting and debugging.
// For instance, we could use the AST token index to point to the exact location in the source code where the symbol was defined or used.
// or to show a forward reference error or a hiding warning.
// Scope could be useful to show the symbol fully qualified name including its scope hierarchy.
public class Symbol(Scope scope, int astTokenIndex)
{
    public Scope Scope { get; } = scope;
    public int AstTokenIndex { get; } = astTokenIndex;

    public override string ToString()
    {
        return $"[{GetType().Name}], Scope: {(Scope != null ? Scope.Id : "null")}, AST Token Index: {AstTokenIndex}";
    }
}

//TODO: is it better to join FunctionSymbol and FunctionValue into a single class?
public class FunctionSymbol(string qualifiedName, ValueSymbol? outputSymbol, IEnumerable<ValueSymbol> inputParamTypes, TypeSymbol outputType, IQuantumCircuit gate, StatementContext body, FunctionDeclarationParamsContext? variableDeclaration, Scope innerScope, int astTokenIndex) : Symbol(innerScope, astTokenIndex)
{
    public string QualifiedName { get; } = qualifiedName;
    public ValueSymbol? OutputSymbol { get; set; } = outputSymbol; //null for void functions. Why not voidValue?
    public IEnumerable<ValueSymbol> InputParamTypes { get; set; } = inputParamTypes; //symbols already declared for the function to work on.
    public TypeSymbol OutputType { get; } = outputType;
    public StatementContext Body { get; } = body;
    public FunctionDeclarationParamsContext? VariableDeclaration { get; } = variableDeclaration;
    public IQuantumCircuit Gate { get; } = gate;
    public Scope InnerScope { get; } = innerScope;

    public override string ToString()
    {
        return $"{OutputType} '{QualifiedName}'({string.Join(", ", InputParamTypes)})";
    }
}

public class AnonymousValueSymbol(IQutesValue value, Scope scope, int astTokenIndex) : ValueSymbol(new QualifiedNameSymbol(VariableNameGuid.New(), scope, astTokenIndex), value, scope, astTokenIndex)
{
    public static AnonymousValueSymbol Default(IQutesValue value)
    {
        return new(value, null!, default);
    }
}

public class NamedValueSymbol : ValueSymbol
{
    public NamedValueSymbol(QualifiedNameSymbol qualifiedName, IQutesValue value, Scope scope, int astTokenIndex) : base(qualifiedName, value, scope, astTokenIndex)
    {
        HandleReferenceCount(null, value);
    }

    public override void SetValue(IQutesValue newValue)
    {
        HandleReferenceCount(Value, newValue);
        Value = newValue;
    }

    private static void HandleReferenceCount(IQutesValue? oldValue, IQutesValue? newValue)
    {
        if (oldValue is IQuantumValue oldQuantumValue)
        {
            oldQuantumValue.Register.Free();
        }
        if (newValue is IQuantumValue newQuantumValue)
        {
            newQuantumValue.Register.Retain();
        }
    }
}
public abstract class ValueSymbol(QualifiedNameSymbol qualifiedName, IQutesValue value, Scope scope, int astTokenIndex) : Symbol(scope, astTokenIndex)
{
    public QualifiedNameSymbol QualifiedName { get; } = qualifiedName;
    public IQutesValue Value { get; protected set; } = value;
    public TypeSymbol Type => Value.Type;

    public virtual void SetValue(IQutesValue newValue)
    {
        Value = newValue;
    }

    public override string ToString()
    {
        return $"{Type} '{QualifiedName}' = {Value}";
    }
}

public class QualifiedNameSymbol(string qualifiedName, Scope scope, int astTokenIndex) : Symbol(scope, astTokenIndex)
{
    public string RawStringName { get; } = qualifiedName;
    public string[] NameParts => RawStringName.Split('.');
    public bool IsMemberAccess => NameParts.Length > 1;

    public QualifiedNameSymbol EnclosingName => new (string.Join(".", NameParts[..^1]), Scope, AstTokenIndex);
    public QualifiedNameSymbol MemberName => new (NameParts[^1], Scope, AstTokenIndex);

    override public string ToString()
    {
        return RawStringName;
    }
}

public class TypeSymbol(QutesType type, TypeSymbol? nestedValue = null) : Symbol(null!, default), IEquatable<TypeSymbol>
{
    public QutesType Value { get; } = type;
    public TypeSymbol? NestedValue { get; } = nestedValue;
    public bool Equals(TypeSymbol? other)
    {
        if (other is null) return false;
        if (ReferenceEquals(this, other)) return true;
        return Value == other.Value && Equals(NestedValue, other.NestedValue);
    }

    public override bool Equals(object? obj) => Equals(obj as TypeSymbol);

    public override int GetHashCode() => HashCode.Combine(Value, NestedValue);

    public static bool operator ==(TypeSymbol? left, TypeSymbol? right) => Equals(left, right);

    public static bool operator !=(TypeSymbol? left, TypeSymbol? right) => !Equals(left, right);

    public override string ToString()
    {
        return NestedValue != null ? $"{NestedValue}[]" : Value.ToString();
    }

    public int GetSize()
    {
        return Value switch
        {
            QutesType.boolean => sizeof(bool),
            QutesType.integer => sizeof(int),
            QutesType.character => sizeof(char),
            QutesType.floating => sizeof(float),
            QutesType.qubit => 1,
            QutesType.quinteger => CompilerFlags.Current.QuintSizeInQubit,
            QutesType.qucharacter => CompilerFlags.Current.QucharSizeInQubit,
            QutesType.qustring => CompilerFlags.Current.QucharSizeInQubit,
            _ => throw new InvalidOperationException($"Cannot get size in qubits of type {Value}.")
        };
    }

    public static TypeSymbol FromType(Type value)
    {
        return value switch
        {
            Type t when t == typeof(BoolValue) => Bool,
            Type t when t == typeof(IntValue) => Int,
            Type t when t == typeof(CharValue) => Char,
            Type t when t == typeof(FloatValue) => Float,
            Type t when t == typeof(StringValue) => String,
            Type t when t == typeof(QubitValue) => Qubit,
            Type t when t == typeof(QuintValue) => Quint,
            Type t when t == typeof(QucharValue) => Quchar,
            Type t when t == typeof(QustringValue) => Qustring,
            //Type t when t == typeof(ArrayValue) => Array(),
            Type t when t == typeof(TupleValue) => Tuple,
            Type t when t == typeof(ClassValue) => Class,
            Type t when t == typeof(VoidValue) => Void,
            Type t when t == typeof(RangeValue) => Range,
            Type t when t == typeof(FunctionValue) => Function,
            _ => throw new ArgumentException($"Unsupported type: {value}"),
        };
    }

    public static TypeSymbol Bool { get; } = new(QutesType.boolean);
    public static TypeSymbol Int { get; } = new(QutesType.integer);
    public static TypeSymbol Char { get; } = new(QutesType.character);
    public static TypeSymbol Float { get; } = new(QutesType.floating);
    public static TypeSymbol String { get; } = new(QutesType.@string);
    public static TypeSymbol Qubit { get; } = new(QutesType.qubit);
    public static TypeSymbol Quint { get; } = new(QutesType.quinteger);
    public static TypeSymbol Quchar { get; } = new(QutesType.qucharacter);
    public static TypeSymbol Qustring { get; } = new(QutesType.qustring);
    public static TypeSymbol Array(TypeSymbol elementsType) => new(elementsType.IsQuantum() ? QutesType.quantumArray : QutesType.classicalArray, elementsType);
    public static TypeSymbol Tuple { get; } = new(QutesType.tuple);
    public static TypeSymbol Class { get; } = new(QutesType.@class);
    public static TypeSymbol Void { get; } = new(QutesType.@void);
    public static TypeSymbol Range { get; } = new(QutesType.range);
    public static TypeSymbol Function { get; } = new(QutesType.function);
}