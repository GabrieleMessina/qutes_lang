
using System.Data;
using Antlr4.Runtime;
using Qutes.Grammar;
using QutesLang.GrammarFrontend;
using System.CommandLine;


var logSymbolsScope = new Option<bool>(
    ["-scope", "--log_symbols_scope"],
    "Toggle symbols scope print on console.");
var logAstTree = new Option<bool>(
    ["-tree", "--log_ast_tree"],
    "Toggle syntax tree print on console.");
var logQuantumCircuit = new Option<bool>(
    ["-circuit", "--log_quantum_circuit"],
    "Toggle quantum circuit print on console.");
var saveCircuitAsImage = new Option<bool>(
    ["-image", "--print_circuit_as_image"],
    "Toggle circuit export as image instead of console print as text.");
var logVerbose = new Option<bool>(
    ["-v", "--verbose"],
    "Print all log as verbose on console.");
var numberOfIterations = new Option<int>(
    ["-iter", "--number_of_iterations"],
    () => 100,
    "Set number of iteration for quantum circuit run.");
var filePath = new Argument<string>(
    "file_path",
    "The file path of the Qutes source code.");

var rootCommand = new RootCommand
{
    Description = "Compile Qutes Lang source code."
};
rootCommand.Add(logSymbolsScope);
rootCommand.Add(logAstTree);
rootCommand.Add(logQuantumCircuit);
rootCommand.Add(saveCircuitAsImage);
rootCommand.Add(logVerbose);
rootCommand.Add(numberOfIterations);
rootCommand.Add(filePath);

rootCommand.SetHandler(HandleParams, logSymbolsScope, logAstTree, logQuantumCircuit, saveCircuitAsImage, logVerbose, numberOfIterations, filePath);

return rootCommand.InvokeAsync(args).Result;

void HandleParams(bool logSymbolsScopeValue, bool logAstTreeValue, bool logQuantumCircuitValue, bool saveCircuitAsImageValue,
    bool logVerboseValue, int numberOfIterationsValue, string filePathValue)
{
    Console.WriteLine($"logSymbolsScope: {logSymbolsScopeValue}");
    Console.WriteLine($"logAstTree: {logAstTreeValue}");
    Console.WriteLine($"logQuantumCircuit: {logQuantumCircuitValue}");
    Console.WriteLine($"saveCircuitAsImage: {saveCircuitAsImageValue}");
    Console.WriteLine($"logVerbose: {logVerboseValue}");
    Console.WriteLine($"numberOfIterations: {numberOfIterationsValue}");
    Console.WriteLine($"filePath: {filePathValue}");
    
    var source = new FileStream(filePathValue, FileMode.Open);
    var lexer = new qutes_lexer(new AntlrInputStream(source));
    var tokens = new CommonTokenStream(lexer);
    var parser = new qutes_parser(tokens);
    parser.RemoveErrorListeners();
    parser.AddErrorListener(new QutesErrorListener());
    var tree = parser.program();

    if (parser.NumberOfSyntaxErrors > 0){
        throw new SyntaxErrorException(parser.NumberOfSyntaxErrors.ToString());
    }

    var scopeHandler = new ScopeHandler();
    var circuitHandler = new CircuitHandler();
    var visitor = new QutesVisitor(scopeHandler, circuitHandler);
    var result = visitor.Visit(tree);

    var pythonCode = circuitHandler.FinalizeCircuit();

    Console.WriteLine("Result:");
    Console.WriteLine(result);
}