using QutesLang.Symbols;

namespace QutesLang.GrammarFrontend;

public class ScopeHandler : IScopeHandler
{
    private readonly Stack<Scope> stack = new();

    public Scope CreateScope(string id = "")
    {
        return new Scope(id + VariableNameGuid.New("scope"), GetCurrentScope());
    }

    public Scope? GetCurrentScope()
    {
        return stack.TryPeek(out var scope) ? scope : null;
    }

    public Scope PopScope()
    {
        return stack.Pop();
    }

    public void PushScope(Scope scope)
    {
        stack.Push(scope);
    }
}