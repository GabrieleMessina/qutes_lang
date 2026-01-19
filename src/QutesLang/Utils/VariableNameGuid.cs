namespace QutesLang.Utils;

public static class VariableNameGuid
{
#if DEBUG
    private static readonly Dictionary<string, int> CountByPrefix = [];
#endif

    public static string New(string prefix = "var")
    {
#if DEBUG
        CountByPrefix[prefix] = CountByPrefix.TryGetValue(prefix, out var count) ? count + 1 : 1;
        return $"{prefix}_{CountByPrefix[prefix]}";
#else
        return $"{prefix}_{Guid.NewGuid():N}";
#endif
    }
}
