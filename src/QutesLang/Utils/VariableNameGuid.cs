namespace QutesLang.Utils;

public static class VariableNameGuid
{
    private static int SequenceNumber = 1;
    public static string New(string prefix = "var")
    {
#if DEBUG
        return $"{prefix}_{SequenceNumber++}";
#else
        return $"{prefix}_{Guid.NewGuid():N}";
#endif
    }
}
