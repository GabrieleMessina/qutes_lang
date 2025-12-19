namespace QutesLang.Utils;

public static class VariableNameGuid
{
    public static string New(string prefix = "var")
    {
        return $"{prefix}_{Guid.NewGuid():N}";
    }
}
