using QutesLang.Symbols.Types;

namespace QutesLang.Symbols;

//TODO: maybe the scope in here is useless.
public class Symbol(Scope scope, int astTokenIndex)
{
    
}

public class FunctionSymbol(IEnumerable<IQutesType> inputParamTypes, IQutesType outputType, Scope scope, int astTokenIndex):Symbol(scope, astTokenIndex)
{
}

public class AnonymousValueSymbol(IQutesType value, Scope scope, int astTokenIndex) : ValueSymbol(VariableNameGuid.New(), value, scope, astTokenIndex)
{
}

public class ValueSymbol(string qualifiedName, IQutesType value, Scope scope, int astTokenIndex) : Symbol(scope, astTokenIndex)
{
    public string QualifiedName { get; } = qualifiedName;
    public IQutesType Value { get; } = value;
}

public class QualifiedNameSymbol(string qualifiedName, Scope scope, int astTokenIndex) : Symbol(scope, astTokenIndex)
{
    public string QualifiedName { get; } = qualifiedName;
}

public class TypeSymbol(string typeName, Scope scope, int astTokenIndex):Symbol(scope, astTokenIndex)
{
}

public class TupleSymbol(IEnumerable<Symbol> elements, Scope scope, int astTokenIndex) : Symbol(scope, astTokenIndex)
{
    public IEnumerable<Symbol> Elements { get; } = elements;
}

public class ArraySymbol(IEnumerable<Symbol> elements, Scope scope, int astTokenIndex) : Symbol(scope, astTokenIndex)
{
    //TODO: valutare di rendere questa classe generic e anche valuesymbol, in modo da poter forzare il fatto che 
    // Elements debba essere una collection di IIQutesType dello stesso tipo.
    public IEnumerable<Symbol> Elements { get; } = elements;
}