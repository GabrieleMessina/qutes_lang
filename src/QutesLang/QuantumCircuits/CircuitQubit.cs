namespace QutesLang.GrammarFrontend;

public class CircuitQubit
{
    public string Id { get; set; } = VariableNameGuid.New("qubit");

    public override string ToString()
    {
        return $"Qubit{{{Id}}}";
    }
}
