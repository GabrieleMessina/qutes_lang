namespace QutesLang.Symbols;

public class Scope(string id, Scope? parent)
{
    public Scope? Parent { get; } = parent;
    public Dictionary<string, ValueSymbol> SymbolTable { get; } = parent?.SymbolTable.ToDictionary(entry => entry.Key, entry => entry.Value) ?? [];
    public Dictionary<string, FunctionSymbol> FunctionTable { get; } = parent?.FunctionTable.ToDictionary(entry => entry.Key, entry => entry.Value) ?? [];
}