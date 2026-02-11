namespace QutesLang.Extensions;

public static class StringExtensions
{
    public static string OrFallback(this string str, string fallback) => string.IsNullOrEmpty(str) ? fallback : str;
}
