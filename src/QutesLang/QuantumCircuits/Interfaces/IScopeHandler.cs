using QutesLang.Symbols;

namespace QutesLang.QuantumCircuits.Interfaces;

public interface IScopeHandler
{
    Scope GetCurrentScope();
    Scope CreateScope(string id = "");
    void PushScope(Scope scope);
    Scope PopScope();
}