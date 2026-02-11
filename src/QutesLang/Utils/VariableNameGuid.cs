namespace QutesLang.Utils;

public static class VariableNameGuid
{
    private static readonly Dictionary<string, int> CountByPrefix = [];

    public static string New(string prefix = "var")
    {
        CountByPrefix[prefix] = CountByPrefix.TryGetValue(prefix, out var count) ? count + 1 : 1;
        return $"{prefix}_{CountByPrefix[prefix]}";
        //return $"{prefix}_{Guid.NewGuid():N}";
    }
}
