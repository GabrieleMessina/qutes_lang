using QutesLang.Exceptions;

namespace QutesLang.Symbols;

public class Scope(string id, Scope? parent)
{
    public Scope? Parent { get; } = parent;
    public readonly Dictionary<string, ValueSymbol> SymbolTable = [];
    public readonly Dictionary<string, FunctionSymbol> FunctionTable  = [];

    public void DefineVariable(ValueSymbol symbol)
    {
        if (SymbolTable.ContainsKey(symbol.QualifiedName))
        {
            throw new VariableAlreadyDeclaredException($"Variable with name '{symbol.QualifiedName}' already declared.");
        }
        SymbolTable[symbol.QualifiedName] = symbol;
    }

    public void DefineFunction(FunctionSymbol symbol)
    {
        if (FunctionTable.ContainsKey(symbol.QualifiedName))
        {
            throw new VariableAlreadyDeclaredException($"Variable with name '{symbol.QualifiedName}' already declared.");
        }
        FunctionTable[symbol.QualifiedName] = symbol;
    }

    public ValueSymbol ResolveVariable(string name)
    {
        if (SymbolTable.TryGetValue(name, out ValueSymbol? symbol))
        {
            return symbol;
        }
        else if (Parent != null)
        {
            return Parent.ResolveVariable(name);
        }
        else
        {
            throw new VariableNotDeclaredException($"Variable with name '{name}' not declared.");
        }
    }

    public FunctionSymbol ResolveFunction(string name)
    {
        if (FunctionTable.TryGetValue(name, out FunctionSymbol? function))
        {
            return function;
        }
        else if (Parent != null)
        {
            return Parent.ResolveFunction(name);
        }
        else
        {
            throw new VariableNotDeclaredException($"Function with name '{name}' not declared.");
        }
    }
}