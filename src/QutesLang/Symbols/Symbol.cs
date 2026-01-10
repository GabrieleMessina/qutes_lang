using QutesLang.Symbols.Types;

using static Qutes.Grammar.qutes_parser;

namespace QutesLang.Symbols;

//TODO: maybe the scope in here is useless.
public class Symbol(Scope scope, int astTokenIndex)
{
    
}

public class FunctionSymbol(string qualifiedName, IEnumerable<ValueSymbol> inputParamTypes, TypeSymbol outputType, StatementContext body, Scope scope, int astTokenIndex):Symbol(scope, astTokenIndex)
{
    public string QualifiedName { get; } = qualifiedName;
    public IEnumerable<ValueSymbol> InputParamTypes { get; } = inputParamTypes; //symbols already declared for the function to work on.
    public TypeSymbol OutputType { get; } = outputType;
    public StatementContext Body { get; } = body;
    public Scope Scope { get; } = scope;
}

public class AnonymousValueSymbol(IQutesValue value, Scope scope, int astTokenIndex) : ValueSymbol(VariableNameGuid.New(), value, scope, astTokenIndex)
{
}

public class ValueSymbol(string qualifiedName, IQutesValue value, Scope scope, int astTokenIndex) : Symbol(scope, astTokenIndex)
{
    public string QualifiedName { get; } = qualifiedName;
    public IQutesValue Value { get; set; } = value;
    public TypeSymbol Type { get; set; } = value.Type;
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

    public static TypeSymbol Bool() => new (QutesType.boolean);
    public static TypeSymbol Int() => new (QutesType.integer);
    public static TypeSymbol Char() => new (QutesType.character);
    public static TypeSymbol Float() => new (QutesType.floating);
    public static TypeSymbol String() => new (QutesType.@string);
    public static TypeSymbol Qubit() => new (QutesType.qubit);
    public static TypeSymbol Quint() => new (QutesType.quinteger);
    public static TypeSymbol Quchar() => new (QutesType.qucharacter);
    public static TypeSymbol Qustring() => new (QutesType.qustring);
    public static TypeSymbol Array(TypeSymbol elementsType) => new (elementsType.IsQuantum() ? QutesType.quantumArray : QutesType.classicalArray, elementsType);
    public static TypeSymbol Class() => new (QutesType.@class);
    public static TypeSymbol Void() => new (QutesType.@void);
}

/// <summary>
/// Represents a tuple symbol composed of multiple element symbols that can have different types.
/// </summary>
/// <param name="elements">The collection of symbols that make up the elements of the tuple.</param>
/// <param name="scope">The scope in which the tuple symbol is defined.</param>
/// <param name="astTokenIndex">The index of the associated abstract syntax tree (AST) token for this symbol.</param>
public class TupleSymbol(IEnumerable<Symbol> elements, Scope scope, int astTokenIndex) : Symbol(scope, astTokenIndex)
{
    public IEnumerable<Symbol> Elements { get; } = elements;
}