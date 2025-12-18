namespace QutesLang.Utils;

public static class VariableNameGuid
{
    public static string New()
    {
        return $"var_{Guid.NewGuid():N}";
    }
}
