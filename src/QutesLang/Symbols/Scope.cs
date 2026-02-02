using System.Text;

using QutesLang.Exceptions;

namespace QutesLang.Symbols;

public class Scope(string id, Scope? parent)
{
    public string Id { get; } = id;
    public Scope? Parent { get; } = parent;
    public readonly Dictionary<string, ValueSymbol> SymbolTable = [];
    public readonly Dictionary<string, FunctionSymbol> FunctionTable = [];

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
        if (CompilerFlags.Current.EnableScopeLogging)
        {
            Console.WriteLine($"[Scope] Trying to resolve variable '{name}' in scope:\n{this}");
        }

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
        if (CompilerFlags.Current.EnableScopeLogging)
        {
            Console.WriteLine($"[Scope] Trying to resolve function '{name}' in scope:\n{this}");
        }

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

    public override string ToString()
    {
        var sb = new StringBuilder();
        sb.AppendLine($"Scope: {Id}");

        sb.AppendLine("Variables:");
        if (SymbolTable.Count == 0)
        {
            sb.AppendLine("  (none)");
        }
        else
        {
            foreach (var kvp in SymbolTable)
            {
                sb.AppendLine($"  {kvp.Key}: {kvp.Value.Type}");
            }
        }

        sb.AppendLine("Functions:");
        if (FunctionTable.Count == 0)
        {
            sb.AppendLine("  (none)");
        }
        else
        {
            foreach (var kvp in FunctionTable)
            {
                sb.AppendLine($"  {kvp.Key}");
            }
        }

        if (Parent != null)
        {
            sb.AppendLine("Inherited:");
            var parentOutput = Parent.ToString();
            foreach (var line in parentOutput.Split([Environment.NewLine], StringSplitOptions.RemoveEmptyEntries))
            {
                sb.AppendLine($"  {line}");
            }
        }

        return sb.ToString();
    }
}