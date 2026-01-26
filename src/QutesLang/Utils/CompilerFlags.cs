namespace QutesLang.Utils;

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
    public int QustringSizeInQubit => (int)Math.Ceiling(Math.Log2(QustringAlphabet.Length));
    public string OutputPath { get; set; } = "./"; //TODO: in python we should check that dir exists.
    public string CircuitImagesFolder => "./circuit_images";
    public string SourceFilePath { get; set; } = string.Empty;

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
