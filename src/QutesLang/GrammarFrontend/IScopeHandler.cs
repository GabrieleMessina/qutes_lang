using QutesLang.Symbols;

namespace QutesLang.GrammarFrontend;

public interface IScopeHandler
{
    Scope? GetCurrentScope();
    Scope CreateScope();
    void PushScope(Scope scope);
    Scope PopScope();
}