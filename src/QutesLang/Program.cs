using System.Data;
using Antlr4.Runtime;
using Qutes.Grammar;
using QutesLang.GrammarFrontend;
using System.CommandLine;

var logSymbolsScope = CommandLine.CreateOption(
    ["-scopes", "--log-scopes"],
    () => CompilerFlags.Current.EnableScopeLogging,
    "Toggle symbols scope print on console.");
var logAstTree = CommandLine.CreateOption(
    ["-ast", "--print-ast"],
    () => CompilerFlags.Current.PrintAst,
    "Toggle syntax tree print on console.");
var logOutput = CommandLine.CreateOption(
    ["--output-in-console"],
    () => CompilerFlags.Current.PrintOutputToConsole,
    "Toggle output print on console.");
var logQuantumCircuit = CommandLine.CreateOption(
    ["-circuit", "--print-circuit"],
    () => CompilerFlags.Current.PrintQuantumCircuit,
    "Toggle quantum circuit print on console.");
var saveCircuitAsImage = CommandLine.CreateOption(
    ["-image", "--print-circuit-image"],
    () => CompilerFlags.Current.CreateQuantumCircuitImage,
    "Toggle circuit export as image instead of console print as text.");
var logVerbose = CommandLine.CreateOption(
    ["-v", "--verbose"],
    () => CompilerFlags.Current.VerboseLogging,
    "Print all log as verbose on console.");
var numberOfIterations = CommandLine.CreateOption(
    ["-runs", "--iterations"],
    () => CompilerFlags.Current.NumberOfIterations,
    "Set number of iteration for quantum circuit run.",
    value => value <= 0 ? (false, "Number of iterations must be positive.") : (true, string.Empty));
var quintSizeInQubit = CommandLine.CreateOption(
    ["-quint", "--quint-size"],
    () => CompilerFlags.Current.QuintSizeInQubit,
    "Set quint size in qubit.",
    value => value <= 0 ? (false, "Quint size in qubit must be positive.") : (true, string.Empty));
var qustringAlphabet = CommandLine.CreateOption(
    ["-quint", "--quint-size"],
    () => CompilerFlags.Current.QustringAlphabet,
    "Set quint size in qubit.",
    value => value.Length == 0 ? (false, "Qustring alphabet must not be empty.") : (true, string.Empty));
var outputPath = CommandLine.CreateOption(
    ["-o", "--output"],
    () => CompilerFlags.Current.OutputPath,
    "Set output file path.")
    .AcceptLegalFilePathsOnly();
var filePath = CommandLine.CreateArgument<string>("file-path",
    "Path to Qutes Lang source file.");

var rootCommand = new RootCommand("Compile Qutes Lang source code.")
{
    logSymbolsScope,
    logAstTree,
    logQuantumCircuit,
    saveCircuitAsImage,
    logVerbose,
    numberOfIterations,
    quintSizeInQubit,
    qustringAlphabet,
    filePath,
    outputPath
};

rootCommand.SetAction(HandleParams);
return rootCommand.Parse(args).Invoke();

void HandleParams(ParseResult result)
{
    CompilerFlags.Current.VerboseLogging = result.GetRequiredValue(logSymbolsScope);
    CompilerFlags.Current.PrintAst = result.GetRequiredValue(logAstTree);
    CompilerFlags.Current.PrintQuantumCircuit = result.GetRequiredValue(logQuantumCircuit);
    CompilerFlags.Current.CreateQuantumCircuitImage = result.GetRequiredValue(saveCircuitAsImage);
    CompilerFlags.Current.VerboseLogging = result.GetRequiredValue(logVerbose);
    CompilerFlags.Current.NumberOfIterations = result.GetRequiredValue(numberOfIterations);
    CompilerFlags.Current.QuintSizeInQubit = result.GetRequiredValue(quintSizeInQubit);
    CompilerFlags.Current.QustringAlphabet = result.GetRequiredValue(qustringAlphabet);
    CompilerFlags.Current.OutputPath = result.GetRequiredValue(outputPath);
    CompilerFlags.Current.SourceFilePath = result.GetRequiredValue(filePath);

    if (CompilerFlags.Current.VerboseLogging)
    {
        CompilerFlags.Current.PrintFlags();
    }

    RunProgram(CompilerFlags.Current);
}

static void RunProgram(CompilerFlags flags)
{
    var source = new FileStream(flags.SourceFilePath, FileMode.Open);
    var lexer = new qutes_lexer(new AntlrInputStream(source));
    var tokens = new CommonTokenStream(lexer);
    var parser = new qutes_parser(tokens);
    parser.RemoveErrorListeners();
    parser.AddErrorListener(new QutesErrorListener());
    var tree = parser.program();

    if (parser.NumberOfSyntaxErrors > 0)
    {
        throw new SyntaxErrorException(parser.NumberOfSyntaxErrors.ToString());
    }

    var scopeHandler = new ScopeHandler();
    var circuitHandler = new CircuitHandler();
    var visitor = new QutesVisitor(scopeHandler, circuitHandler);
    try
    {
        if (flags.VerboseLogging)
        {
            Console.WriteLine("================ Execution ================");
        }
        var result = visitor.Visit(tree);
        var pythonCode = circuitHandler.FinalizeProgram(flags.OutputPath);

        if (flags.PrintAst)
        {
            Console.WriteLine("================ AST ================");
            Console.WriteLine(tree.ToStringTree(parser));
        }
        if (flags.PrintOutputToConsole)
        {
            Console.WriteLine("================ Output ================");
            Console.WriteLine(pythonCode);
        }
    }
    catch (Exception ex)
    {
        File.WriteAllText(Path.Combine(flags.OutputPath, "output.py"), $"[Error] {ex}");
        Console.WriteLine($"[Error] {ex}");
        return;
    }
    finally
    {
        if (flags.EnableScopeLogging)
        {
            Console.WriteLine("================ Scope Tree ================");
            Console.WriteLine(scopeHandler.GetCurrentScope());
        }
    }
}