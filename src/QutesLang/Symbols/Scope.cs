namespace QutesLang.Symbols;

public class Scope(string id, Scope? parent)
{
    public Dictionary<string, ValueSymbol> SymbolTable { get; } = [];
}