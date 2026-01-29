using QutesLang.GrammarFrontend;
using QutesLang.Symbols.Types;

using static Qutes.Grammar.qutes_parser;

namespace QutesLang.Symbols;

//Scope reference and AST token index could be useful in the future for error reporting and debugging.
// For instance, we could use the AST token index to point to the exact location in the source code where the symbol was defined or used.
// or to show a forward reference error or a hiding warning.
// Scope could be useful to show the symbol fully qualified name including its scope hierarchy.
public class Symbol(Scope scope, int astTokenIndex)
{
    public override string ToString()
    {
        return $"[{GetType().Name}], Scope: {(scope != null ? scope.Id : "null")}, AST Token Index: {astTokenIndex}";
    }
}

public class FunctionSymbol(string qualifiedName, ValueSymbol? outputSymbol, IEnumerable<ValueSymbol> inputParamTypes, TypeSymbol outputType, IQuantumCircuit gate, StatementContext body, FunctionDeclarationParamsContext? variableDeclaration, Scope innerScope, int astTokenIndex) : Symbol(innerScope, astTokenIndex)
{
    public string QualifiedName { get; } = qualifiedName;
    public ValueSymbol? OutputSymbol { get; set; } = outputSymbol; //null for void functions.
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

public class AnonymousValueSymbol(IQutesValue value, Scope scope, int astTokenIndex) : ValueSymbol(VariableNameGuid.New(), value, scope, astTokenIndex)
{
    public static AnonymousValueSymbol Default(IQutesValue value)
    {
        return new(value, null!, default);
    }
}

public class ValueSymbol(string qualifiedName, IQutesValue value, Scope scope, int astTokenIndex) : Symbol(scope, astTokenIndex)
{
    public string QualifiedName { get; } = qualifiedName;
    public IQutesValue Value { get; set; } = value;
    public TypeSymbol Type { get; set; } = value.Type;

    public override string ToString()
    {
        return $"{Type} '{QualifiedName}' = {Value}";
    }
}

public class QualifiedNameSymbol(string qualifiedName, Scope scope, int astTokenIndex) : Symbol(scope, astTokenIndex)
{
    public string QualifiedName { get; } = qualifiedName;
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
}