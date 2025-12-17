using QutesLang.Symbols;

namespace QutesLang.GrammarFrontend;
public class ScopeHandler : IScopeHandler
{
    private readonly Stack<Scope> stack = new();

    public Scope CreateScope()
    {
        return new Scope(Guid.NewGuid().ToString(), GetCurrentScope());
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