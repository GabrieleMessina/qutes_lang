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

public class AnonymousValueSymbol : ValueSymbol
{
    //TODO: fix the type symbol creation here.
    public AnonymousValueSymbol(IQutesType value, Scope scope, int astTokenIndex) : base(VariableNameGuid.New(), value, new TypeSymbol(value.GetType().Name, scope, astTokenIndex), scope, astTokenIndex)
    {
    }

    public AnonymousValueSymbol(IQutesType value, TypeSymbol type, Scope scope, int astTokenIndex) : base(VariableNameGuid.New(), value, type, scope, astTokenIndex)
    {
    }
}

public class ValueSymbol(string qualifiedName, IQutesType value, TypeSymbol type, Scope scope, int astTokenIndex) : Symbol(scope, astTokenIndex)
{
    public string QualifiedName { get; } = qualifiedName;
    public IQutesType Value { get; set; } = value;
    public TypeSymbol Type { get; } = type;
}

public class QualifiedNameSymbol(string qualifiedName, Scope scope, int astTokenIndex) : Symbol(scope, astTokenIndex)
{
    public string QualifiedName { get; } = qualifiedName;
}


public class TypeSymbol(string name, Scope scope, int astTokenIndex) : Symbol(scope, astTokenIndex)
{
    //TODO: should we handle this with a QutesType instead of symbol?
    public string Name { get; } = name;
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


/// <summary>
/// Represent an array symbol, which contains a collection of elements with the same type.
/// </summary>
/// <param name="elements">The collection of symbols that make up the elements of the tuple.</param>
/// <param name="scope">The scope in which the tuple symbol is defined.</param>
/// <param name="astTokenIndex">The index of the associated abstract syntax tree (AST) token for this symbol.</param>
public class ArraySymbol(IEnumerable<Symbol> elements, TypeSymbol type, Scope scope, int astTokenIndex) : Symbol(scope, astTokenIndex)
{
    //TODO: valutare di rendere questa classe generic e anche valuesymbol, in modo da poter forzare il fatto che 
    // Elements debba essere una collection di IIQutesType dello stesso tipo.
    public IEnumerable<Symbol> Elements { get; } = elements;
}