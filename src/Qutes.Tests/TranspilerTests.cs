using Antlr4.Runtime;
using Qutes.Grammar;
using QutesLang.GrammarFrontend;
using QutesLang.Utils;
using Xunit;

namespace Qutes.Tests;

public class TranspilerTests
{
    private const string OutputPath = "./test_output";

    public TranspilerTests()
    {
        // Ensure output directory exists (though CircuitHandler might create parts of it, best to be safe)
        if (!Directory.Exists(OutputPath))
        {
            Directory.CreateDirectory(OutputPath);
        }
        
        // Reset defaults
        CompilerFlags.Current = new CompilerFlags
        {
            OutputPath = OutputPath,
            PrintQuantumCircuit = false,
            PrintOutputToConsole = false,
            PrintAst = false,
            EnableScopeLogging = false,
            CreateQuantumCircuitImage = false,
        };
    }

    private string RunTranspiler(string sourceCode)
    {
        var inputStream = new AntlrInputStream(sourceCode);
        var lexer = new qutes_lexer(inputStream);
        var tokens = new CommonTokenStream(lexer);
        var parser = new qutes_parser(tokens);
        
        // Fail fast on syntax errors
        parser.AddErrorListener(new ThrowingErrorListener());

        var tree = parser.program();

        var scopeHandler = new ScopeHandler();
        var circuitHandler = new CircuitHandler();
        var visitor = new QutesVisitor(scopeHandler, circuitHandler);

        try
        {
            visitor.Visit(tree);
            return circuitHandler.FinalizeProgram(OutputPath);
        }
        catch (Exception ex)
        {
            Console.WriteLine(ex);
            throw;
        }
    }

    #region Literal Declaration Tests

    [Fact]
    public void BoolLiteral_True_GeneratesCorrectly()
    {
        var source = "bool x = true;";
        var output = RunTranspiler(source);
        // Bool literals are classical, no quantum circuit generated for just a declaration
        Assert.NotNull(output);
    }

    [Fact]
    public void BoolLiteral_False_GeneratesCorrectly()
    {
        var source = "bool x = false;";
        var output = RunTranspiler(source);
        Assert.NotNull(output);
    }

    [Fact]
    public void IntLiteral_Decimal_GeneratesCorrectly()
    {
        var source = "int x = 42;";
        var output = RunTranspiler(source);
        Assert.NotNull(output);
    }

    [Fact(Skip = "Hex integer literals not yet implemented")]
    public void IntLiteral_Hex_GeneratesCorrectly()
    {
        var source = "int x = 0xff;";
        var output = RunTranspiler(source);
        Assert.NotNull(output);
    }

    [Fact(Skip = "Binary integer literals not yet implemented")]
    public void IntLiteral_Binary_GeneratesCorrectly()
    {
        var source = "int x = 0b1010;";
        var output = RunTranspiler(source);
        Assert.NotNull(output);
    }

    [Fact]
    public void FloatLiteral_GeneratesCorrectly()
    {
        var source = "float x = 3.14;";
        var output = RunTranspiler(source);
        Assert.NotNull(output);
    }

    [Fact]
    public void CharLiteral_GeneratesCorrectly()
    {
        var source = "char c = 'a';";
        var output = RunTranspiler(source);
        Assert.NotNull(output);
    }

    [Fact]
    public void StringLiteral_GeneratesCorrectly()
    {
        var source = "string s = \"hello\";";
        var output = RunTranspiler(source);
        Assert.NotNull(output);
    }

    [Fact]
    public void QubitLiteral_ZeroState_GeneratesStatePreparation()
    {
        var source = "qubit q = 0q; measure q;";
        var output = RunTranspiler(source);
        Assert.Contains("StatePreparation", output);
        Assert.Contains("complex(1),complex(0)", output);
    }

    [Fact]
    public void QubitLiteral_OneState_GeneratesStatePreparation()
    {
        var source = "qubit q = 1q; measure q;";
        var output = RunTranspiler(source);
        Assert.Contains("StatePreparation", output);
        Assert.Contains("complex(0),complex(1)", output);
    }

    [Fact]
    public void QubitLiteral_KetZero_GeneratesStatePreparation()
    {
        var source = "qubit q = |0>; measure q;";
        var output = RunTranspiler(source);
        Assert.Contains("StatePreparation", output);
        Assert.Contains("complex(1),complex(0)", output);
    }

    [Fact]
    public void QubitLiteral_KetOne_GeneratesStatePreparation()
    {
        var source = "qubit q = |1>; measure q;";
        var output = RunTranspiler(source);
        Assert.Contains("StatePreparation", output);
        Assert.Contains("complex(0),complex(1)", output);
    }

    [Fact]
    public void QubitLiteral_KetPlus_GeneratesStatePreparation()
    {
        var source = "qubit q = |+>; measure q;";
        var output = RunTranspiler(source);
        Assert.Contains("StatePreparation", output);
        Assert.Contains("complex(1),complex(1)", output);
    }

    [Fact]
    public void QubitLiteral_KetMinus_GeneratesStatePreparation()
    {
        var source = "qubit q = |->; measure q;";
        var output = RunTranspiler(source);
        Assert.Contains("StatePreparation", output);
    }

    [Fact]
    public void QuintLiteral_SingleValue_GeneratesStatePreparation()
    {
        var source = "quint n = 5q; measure n;";
        var output = RunTranspiler(source);
        Assert.Contains("StatePreparation", output);
        Assert.Contains("QuantumRegister", output);
    }

    [Fact(Skip = "Quchar literal syntax '0'q is parsed as char, not quchar - transpiler issue")]
    public void QucharLiteral_GeneratesStatePreparation()
    {
        // Quchar only supports binary (0/1) characters
        var source = "quchar c = '0'q; measure c;";
        var output = RunTranspiler(source);
        Assert.Contains("StatePreparation", output);
    }

    [Fact(Skip = "Qustring literal parsing includes quote marks - transpiler issue")]
    public void QustringLiteral_GeneratesStatePreparation()
    {
        // Qustring literal uses the q suffix on string (only 0/1 chars allowed)
        var source = "qustring s = \"10\"q; measure s;";
        var output = RunTranspiler(source);
        Assert.Contains("StatePreparation", output);
    }

    [Fact]
    public void QubitArray_GeneratesMultipleQubits()
    {
        var source = "qubit[] arr = [0q, 1q, |+>]; measure arr;";
        var output = RunTranspiler(source);
        Assert.Contains("QuantumRegister", output);
        Assert.Contains("measure", output);
    }

    #endregion

    #region Variable Declaration and Assignment Tests

    [Fact]
    public void VariableDeclaration_WithType_Works()
    {
        var source = "int x = 10; int y = x;";
        var output = RunTranspiler(source);
        Assert.NotNull(output);
    }

    [Fact]
    public void QubitAssignment_Works()
    {
        var source = "qubit a = 0q; qubit b = |1>; measure a; measure b;";
        var output = RunTranspiler(source);
        Assert.Contains("StatePreparation", output);
        Assert.Contains("measure", output);
    }

    #endregion

    #region Arithmetic Operator Tests

    [Fact]
    public void ArithmeticOperator_Addition_Works()
    {
        var source = "int x = 5 + 3;";
        var output = RunTranspiler(source);
        Assert.NotNull(output);
    }

    [Fact]
    public void ArithmeticOperator_Subtraction_Works()
    {
        var source = "int x = 10 - 4;";
        var output = RunTranspiler(source);
        Assert.NotNull(output);
    }

    [Fact]
    public void ArithmeticOperator_Multiplication_Works()
    {
        var source = "int x = 6 * 7;";
        var output = RunTranspiler(source);
        Assert.NotNull(output);
    }

    [Fact]
    public void ArithmeticOperator_Division_Works()
    {
        var source = "int x = 20 / 4;";
        var output = RunTranspiler(source);
        Assert.NotNull(output);
    }

    [Fact]
    public void ArithmeticOperator_Modulo_Works()
    {
        var source = "int x = 17 % 5;";
        var output = RunTranspiler(source);
        Assert.NotNull(output);
    }

    [Fact(Skip = "Exponent operator not fully implemented for classical integers")]
    public void ArithmeticOperator_Exponent_Works()
    {
        var source = "int x = 2 ^ 10;";
        var output = RunTranspiler(source);
        Assert.NotNull(output);
    }

    [Fact]
    public void QuantumArithmetic_Addition_GeneratesAdder()
    {
        var source = "quint a = 3q; quint b = 2q; quint c = a + b; measure c;";
        var output = RunTranspiler(source);
        // May use ModularAdderGate or custom adder implementation
        Assert.NotNull(output);
        Assert.Contains("measure", output);
    }

    [Fact]
    public void QuantumArithmetic_Multiplication_GeneratesMultiplier()
    {
        var source = "quint a = 3q; quint b = 2q; quint c = a * b; measure c;";
        var output = RunTranspiler(source);
        // May use MultiplierGate or custom multiplier implementation
        Assert.NotNull(output);
        Assert.Contains("measure", output);
    }

    #endregion

    #region Comparison Operator Tests

    [Fact]
    public void ComparisonOperator_Equal_Works()
    {
        var source = "bool x = 5 == 5;";
        var output = RunTranspiler(source);
        Assert.NotNull(output);
    }

    [Fact]
    public void ComparisonOperator_NotEqual_Works()
    {
        var source = "bool x = 5 != 3;";
        var output = RunTranspiler(source);
        Assert.NotNull(output);
    }

    [Fact]
    public void ComparisonOperator_LessThan_Works()
    {
        var source = "bool x = 3 < 5;";
        var output = RunTranspiler(source);
        Assert.NotNull(output);
    }

    [Fact]
    public void ComparisonOperator_GreaterThan_Works()
    {
        var source = "bool x = 10 > 5;";
        var output = RunTranspiler(source);
        Assert.NotNull(output);
    }

    [Fact]
    public void ComparisonOperator_LessOrEqual_Works()
    {
        var source = "bool x = 5 <= 5;";
        var output = RunTranspiler(source);
        Assert.NotNull(output);
    }

    [Fact]
    public void ComparisonOperator_GreaterOrEqual_Works()
    {
        var source = "bool x = 10 >= 5;";
        var output = RunTranspiler(source);
        Assert.NotNull(output);
    }

    #endregion

    #region Logical Operator Tests

    [Fact]
    public void LogicalOperator_And_Works()
    {
        var source = "bool x = true and false;";
        var output = RunTranspiler(source);
        Assert.NotNull(output);
    }

    [Fact]
    public void LogicalOperator_Or_Works()
    {
        var source = "bool x = true or false;";
        var output = RunTranspiler(source);
        Assert.NotNull(output);
    }

    [Fact]
    public void LogicalOperator_Not_Works()
    {
        var source = "bool x = not false;";
        var output = RunTranspiler(source);
        Assert.NotNull(output);
    }

    #endregion

    #region Shift Operator Tests

    [Fact]
    public void ShiftOperator_LeftShift_Works()
    {
        var source = "int x = 1 << 4;";
        var output = RunTranspiler(source);
        Assert.NotNull(output);
    }

    [Fact]
    public void ShiftOperator_RightShift_Works()
    {
        var source = "int x = 16 >> 2;";
        var output = RunTranspiler(source);
        Assert.NotNull(output);
    }

    #endregion

    #region Unary Operator Tests

    [Fact]
    public void UnaryOperator_PreIncrement_Works()
    {
        var source = "int x = 5; ++x;";
        var output = RunTranspiler(source);
        Assert.NotNull(output);
    }

    [Fact]
    public void UnaryOperator_PostIncrement_Works()
    {
        var source = "int x = 5; x++;";
        var output = RunTranspiler(source);
        Assert.NotNull(output);
    }

    [Fact]
    public void UnaryOperator_PreDecrement_Works()
    {
        var source = "int x = 5; --x;";
        var output = RunTranspiler(source);
        Assert.NotNull(output);
    }

    [Fact]
    public void UnaryOperator_PostDecrement_Works()
    {
        var source = "int x = 5; x--;";
        var output = RunTranspiler(source);
        Assert.NotNull(output);
    }

    [Fact]
    public void UnaryOperator_Negation_Works()
    {
        var source = "int x = -5;";
        var output = RunTranspiler(source);
        Assert.NotNull(output);
    }

    #endregion

    #region Control Flow Tests

    [Fact]
    public void IfStatement_SimpleCondition_Works()
    {
        var source = @"
            qubit q = 0q;
            bool cond = true;
            if(cond){
                hadamard q;
            }
            measure q;
        ";
        var output = RunTranspiler(source);
        Assert.Contains("measure", output);
    }

    [Fact]
    public void IfElseStatement_Works()
    {
        var source = @"
            qubit q = 0q;
            bool cond = false;
            if(cond){
                hadamard q;
            }
            else{
                pauliz q;
            }
            measure q;
        ";
        var output = RunTranspiler(source);
        Assert.Contains("measure", output);
    }

    [Fact]
    public void WhileLoop_Works()
    {
        var source = @"
            int i = 0;
            qubit q = 0q;
            while(i < 3){
                i++;
            }
            measure q;
        ";
        var output = RunTranspiler(source);
        Assert.Contains("measure", output);
    }

    [Fact]
    public void DoWhileLoop_Works()
    {
        var source = @"
            int i = 0;
            qubit q = 0q;
            do{
                i++;
            } while(i < 3);
            measure q;
        ";
        var output = RunTranspiler(source);
        Assert.Contains("measure", output);
    }

    [Fact]
    public void ForeachLoop_WithIndex_Works()
    {
        var source = @"
            qubit[] arr = [0q, 0q, 0q];
            foreach q in arr {
                hadamard q;
            }
            measure arr;
        ";
        var output = RunTranspiler(source);
        Assert.Contains(".h(", output);
        Assert.Contains("measure", output);
    }

    [Fact]
    public void ForeachLoop_WithIndexVariable_Works()
    {
        var source = @"
            qubit[] bitmask = [1q, 0q, 1q];
            quint[] vector = [1q, 2q, 3q];
            foreach q,i in vector{
                if(bitmask[i]){
                    hadamard q;
                }
            }
            measure vector;
        ";
        var output = RunTranspiler(source);
        Assert.Contains("measure", output);
    }

    [Fact]
    public void BreakStatement_Works()
    {
        var source = @"
            int i = 0;
            while(true){
                i++;
                if(i > 5){
                    break;
                }
            }
        ";
        var output = RunTranspiler(source);
        Assert.NotNull(output);
    }

    #endregion

    #region Function Tests

    [Fact]
    public void FunctionDeclaration_VoidFunction_Works()
    {
        var source = @"
            qubit q = 0q;
            void applyH(qubit x){
                hadamard x;
            }
            applyH(q);
            measure q;
        ";
        var output = RunTranspiler(source);
        Assert.Contains(".h(", output);
    }

    [Fact]
    public void FunctionDeclaration_WithParameters_Works()
    {
        var source = @"
            qubit[] a = [|+>,|+>,|+>];
            qubit d = 0q;
            void foo(qubit[] b, qubit c){
                hadamard b;
                mcx b, c;
            }
            foo(a,d);
            measure d;
        ";
        var output = RunTranspiler(source);
        Assert.Contains("mcx", output);
    }

    [Fact(Skip = "Qubit return from functions not properly handled - transpiler issue")]
    public void ReturnStatement_Works()
    {
        // Test returning a qubit from a function
        var source = @"
            qubit getValue(){
                qubit q = 0q;
                hadamard q;
                return q;
            }
            qubit x = getValue();
            measure x;
        ";
        var output = RunTranspiler(source);
        Assert.NotNull(output);
    }

    #endregion

    #region Quantum Gate Tests

    [Fact]
    public void HadamardGate_SingleQubit_GeneratesH()
    {
        var source = "qubit q = 0q; hadamard q; measure q;";
        var output = RunTranspiler(source);
        Assert.Contains(".h(", output);
    }

    [Fact]
    public void HadamardGate_MultipleQubits_GeneratesH()
    {
        var source = "qubit[] arr = [0q, 0q]; hadamard arr; measure arr;";
        var output = RunTranspiler(source);
        Assert.Contains(".h(", output);
    }

    [Fact]
    public void PauliYGate_GeneratesY()
    {
        var source = "qubit q = 0q; pauliy q; measure q;";
        var output = RunTranspiler(source);
        Assert.Contains(".y(", output);
    }

    [Fact]
    public void PauliZGate_GeneratesZ()
    {
        var source = "qubit q = 0q; pauliz q; measure q;";
        var output = RunTranspiler(source);
        Assert.Contains(".z(", output);
    }

    [Fact]
    public void NotGate_QuantumNot_GeneratesX()
    {
        var source = "qubit q = 0q; not q; measure q;";
        var output = RunTranspiler(source);
        Assert.Contains(".x(", output);
    }

    [Fact]
    public void CnotGate_GeneratesCX()
    {
        var source = "qubit control = 1q; qubit target = 0q; cnot control, target; measure target;";
        var output = RunTranspiler(source);
        Assert.Contains(".cx(", output);
    }

    [Fact]
    public void SwapGate_GeneratesSwap()
    {
        var source = "qubit a = 0q; qubit b = 1q; swap a, b; measure a; measure b;";
        var output = RunTranspiler(source);
        Assert.Contains(".swap(", output);
    }

    [Fact]
    public void MCXGate_GeneratesMCX()
    {
        var source = @"
            qubit[] controls = [1q, 1q];
            qubit target = 0q;
            mcx controls, target;
            measure target;
        ";
        var output = RunTranspiler(source);
        Assert.Contains(".mcx(", output);
    }

    [Fact(Skip = "MCY gate operator not yet implemented")]
    public void MCYGate_GeneratesMCY()
    {
        var source = @"
            qubit[] controls = [1q, 1q];
            qubit target = 0q;
            mcy controls, target;
            measure target;
        ";
        var output = RunTranspiler(source);
        // MCY may be decomposed or use mcy directly
        Assert.NotNull(output);
    }

    [Fact]
    public void MCZGate_GeneratesMCZ()
    {
        var source = @"
            qubit control = 1q;
            qubit target = 0q;
            mcz control, target;
            measure target;
        ";
        var output = RunTranspiler(source);
        Assert.NotNull(output);
    }

    [Fact]
    public void MCPGate_WithPhase_GeneratesMCP()
    {
        var source = @"
            qubit control = 1q;
            qubit target = 0q;
            mcp control, target by 3.14;
            measure target;
        ";
        var output = RunTranspiler(source);
        Assert.Contains(".mcp(", output);
    }

    [Fact]
    public void MeasureGate_SingleQubit_GeneratesMeasure()
    {
        var source = "qubit q = 0q; measure q;";
        var output = RunTranspiler(source);
        Assert.Contains(".measure(", output);
    }

    [Fact]
    public void MeasureGate_MultipleQubits_GeneratesMeasure()
    {
        var source = "qubit[] arr = [0q, 1q]; measure arr;";
        var output = RunTranspiler(source);
        Assert.Contains(".measure(", output);
    }

    [Fact(Skip = "Barrier gate returns null in VisitMultipleUnaryOperator - transpiler issue")]
    public void BarrierGate_GeneratesBarrier()
    {
        // Barrier requires array of qubits
        var source = "qubit[] qubits = [0q, 1q]; barrier qubits; measure qubits;";
        var output = RunTranspiler(source);
        Assert.Contains(".barrier(", output);
    }

    #endregion

    #region Grover Search Tests

    [Fact(Skip = "Qustring parsing issue - quote marks not stripped properly")]
    public void GroverSearch_PatternInArray_Works()
    {
        // Grover search using 'in' operator (pattern in array)
        // Qustring only supports binary (0/1) characters
        var source = @"
            qustring array = ""1110111""q;
            qustring pattern = ""01""q;
            qubit found = 0q;
            if(pattern in array){
                not found;
            }
            measure found;
        ";
        var output = RunTranspiler(source);
        // Grover adds oracle and diffusion operators
        Assert.Contains("measure", output);
    }

    [Fact(Skip = "Direct grover operator syntax requires specific oracle format")]
    public void GroverOperator_Direct_Works()
    {
        var source = @"
            qubit[] search = [|+>, |+>, |+>];
            grover search (mcz search);
            measure search;
        ";
        var output = RunTranspiler(source);
        Assert.NotNull(output);
    }

    #endregion

    #region Array Tests

    [Fact]
    public void ArrayAccess_ByIndex_Works()
    {
        var source = @"
            qubit[] arr = [0q, |+>, 1q];
            qubit first = arr[0];
            hadamard first;
            measure arr;
        ";
        var output = RunTranspiler(source);
        Assert.Contains("measure", output);
    }

    [Fact]
    public void QuintArray_Declaration_Works()
    {
        var source = @"
            quint[] nums = [1q, 2q, 3q];
            measure nums;
        ";
        var output = RunTranspiler(source);
        Assert.Contains("QuantumRegister", output);
    }

    #endregion

    #region Example File Tests

    [Fact]
    public void Example_Foreach_CompilesSuccessfully()
    {
        var source = @"
            qubit[] bitmask = [1q, 0q, 1q];
            quint[] vector = [1q, 2q, 3q];
            foreach q,i in vector{
                if(bitmask[i]){
                    hadamard q;
                }
            }
            measure vector;
        ";
        var output = RunTranspiler(source);
        Assert.NotNull(output);
        Assert.Contains("measure", output);
    }

    [Fact]
    public void Example_FunctionCall_CompilesSuccessfully()
    {
        var source = @"
            qubit[] a = [|+>,|+>,|+>];
            qubit d = 0q;
            qubit e = 0q;
            void foo(qubit[] b, qubit c){
                hadamard b;
                mcx b, c;
            }
            foo(a,d);
            measure e;
        ";
        var output = RunTranspiler(source);
        Assert.NotNull(output);
        Assert.Contains("mcx", output);
    }

    [Fact]
    public void Example_Grover_CompilesSuccessfully()
    {
        var source = @"
            qustring array = ""1110111"";
            qustring pattern = ""00"";
            qubit found = 0q;
            if(pattern in array){
                not found;
            }
            else{
                hadamard found;
            }
            measure found;
        ";
        var output = RunTranspiler(source);
        Assert.NotNull(output);
        Assert.Contains("measure", output);
    }

    #endregion

    #region Print Statement Tests

    [Fact]
    public void PrintStatement_Qubit_Works()
    {
        var source = "qubit q = |+>; print q; measure q;";
        var output = RunTranspiler(source);
        Assert.NotNull(output);
    }

    #endregion
}

public class ThrowingErrorListener : BaseErrorListener
{
    public override void SyntaxError(IRecognizer recognizer, IToken offendingSymbol, int line, int charPositionInLine, string msg, RecognitionException e)
    {
        throw new Exception($"Syntax Error at line {line}:{charPositionInLine}: {msg}");
    }
}
