namespace QutesLang;

public class CompilerFlags
{
    public static CompilerFlags Current { get; set; } = new CompilerFlags();

    public bool EnableScopeLogging { get => field || VerboseLogging; set; } = false;
    public bool PrintAst { get => field || VerboseLogging; set; } = false;
    public bool PrintOutputToConsole { get => field || VerboseLogging; set; } = false;
    public bool PrintQuantumCircuit { get => field || VerboseLogging; set; } = true;
    public bool CreateQuantumCircuitImage { get; set; } = false;
    public bool VerboseLogging { get; set; } = false;
    public int NumberOfIterations { get; set; } = 1024;
    public int QuintSizeInQubit { get; set; } = 3;
    public char[] QustringAlphabet { get; set; } = "01".ToCharArray();
    public int QucharSizeInQubit => (int)Math.Ceiling(Math.Log2(QustringAlphabet.Length));
    public string OutputPath { get; set; } = "./output";
    public string CircuitImagesFolder => "./circuit_images";
    public string SourceFilePath { get; set; } = string.Empty;

    #region FeatureFlags
    /// <summary>
    /// At hoisting time we can immediatly create a quantum gate visiting the function body,
    /// or we can wait until each function call to visit the body and create the gate.
    /// In the first case we have a single gate but if classic operations are present inside the function
    /// they are evaluated only once at hoisting time.
    /// In the second case, we create a new gate at each function call, so classic operations are re-evaluated
    /// but we create multiple gates for the same function.
    /// </summary>
    /// <remarks>
    /// if the function tries to acces an input param that is an array, this call throws because the array is empty and we don't have any idea how many elemnts will be in there.
    /// and we can't create the circuit gate ither, because we don't now how many quantum register there will be inside.
    /// i thing this 2 considerations will allow me to take a decision about this flag.
    /// </remarks>
    public bool VisitFunctionBodyAtEachCall { get; set; } = true;


    #endregion FeatureFlags

    public void PrintFlags()
    {
        Console.WriteLine("========== Compiler Flags ===========");
        Console.WriteLine($"  {nameof(EnableScopeLogging)}: {EnableScopeLogging}");
        Console.WriteLine($"  {nameof(PrintAst)}: {PrintAst}");
        Console.WriteLine($"  {nameof(PrintOutputToConsole)}: {PrintOutputToConsole}");
        Console.WriteLine($"  {nameof(PrintQuantumCircuit)}: {PrintQuantumCircuit}");
        Console.WriteLine($"  {nameof(CreateQuantumCircuitImage)}: {CreateQuantumCircuitImage}");
        Console.WriteLine($"  {nameof(VerboseLogging)}: {VerboseLogging}");
        Console.WriteLine($"  {nameof(NumberOfIterations)}: {NumberOfIterations}");
        Console.WriteLine($"  {nameof(QuintSizeInQubit)}: {QuintSizeInQubit}");
        Console.WriteLine($"  {nameof(OutputPath)}: {OutputPath}");
        Console.WriteLine($"  {nameof(CircuitImagesFolder)}: {CircuitImagesFolder}");
        Console.WriteLine($"  {nameof(SourceFilePath)}: {SourceFilePath}");
    }
}
