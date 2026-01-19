namespace QutesLang.Utils;

public class CompilerFlags
{
    public static CompilerFlags Current { get; set; } = new CompilerFlags();

    public bool EnableScopeLogging { get; set; } = true;
}
