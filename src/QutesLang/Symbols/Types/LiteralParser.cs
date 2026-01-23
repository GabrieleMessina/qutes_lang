using System.Text;
using System.Text.RegularExpressions;

using CommunityToolkit.Diagnostics;

namespace QutesLang.Symbols.Types;

/// <summary>
/// Array of state amplitudes, for n qubits there are 2^n amplitudes, one for each possible basis state.
/// </summary>
/// <param name="amplitudes"></param>

public class StateVector(List<double> amplitudes)
{
    public List<double> Amplitudes { get; } = amplitudes;

    public static StateVector Default(int nQubit)
    {
        var amplitudes = Enumerable.Repeat(0.0d, (int)Math.Pow(2, nQubit)).ToList();
        amplitudes[0] = 1.0; // Set the first amplitude to 1.0 to represent the |0...0> state
        return new StateVector(amplitudes);
    }

    public static StateVector Superposition(int nQubit)
    {
        var amplitudes = Enumerable.Repeat(1.0d, (int)Math.Pow(2, nQubit)).ToList();
        return new StateVector(amplitudes);
    }

    public string ToPythonString()
    {
        var sb = new StringBuilder();
        sb.Append('[');
        foreach (var amplitude in Amplitudes)
        {
            sb.Append($"complex({amplitude}),");
        }
        sb.Append(']');
        return sb.ToString();
    }
}

public class BoolParser
{
    public static bool Parse(string input)
    {
        HashSet<string> allowedValues = ["true", "false", "1", "0"];
        var literal = input.ToLower();
        Guard.IsTrue(allowedValues.Contains(literal), $"Invalid boolean literal '{literal}'. Allowed values are: {string.Join(", ", allowedValues)}");
        var value = literal == "true" || literal == "1";
        return value;
    }
}

public partial class QubitParser
{
    // [float, float]q
    [GeneratedRegex(@"^\[\s*([-+]?[0-9]*\.?[0-9]+)\s*,\s*([-+]?[0-9]*\.?[0-9]+)\s*\]q$", RegexOptions.IgnoreCase | RegexOptions.Compiled)]
    private static partial Regex AmplitudeVectorRegex();

    // [bool, bool?]q
    [GeneratedRegex(@"^\[\s*(true|false|0|1)(?:\s*,\s*(true|false|0|1))?\s*\]q$", RegexOptions.IgnoreCase | RegexOptions.Compiled)]
    private static partial Regex BoolVectorRegex();

    // bool q
    [GeneratedRegex(@"^(true|false|0|1)q$", RegexOptions.IgnoreCase | RegexOptions.Compiled)]
    private static partial Regex SingleBoolRegex();

    // |0>, |1>, |+>, |->
    [GeneratedRegex(@"^\|(.+)\>$", RegexOptions.Compiled)]
    private static partial Regex CanonRegex();

    public static StateVector Parse(string input)
    {
        if (string.IsNullOrWhiteSpace(input)) throw new ArgumentException("Input cannot be null or whitespace.", nameof(input));

        input = input.Replace(" ", string.Empty);

        // Match Float Amplitude Vector: [0.7, 0.3]q
        var floatMatch = AmplitudeVectorRegex().Match(input);
        if (floatMatch.Success)
        {
            var alpha = double.Parse(floatMatch.Groups[1].Value);
            var beta = double.Parse(floatMatch.Groups[2].Value);
            return new StateVector([alpha, beta]);
        }

        // Match Bool Vector: [true, false]q or [0]q
        var boolMatch = BoolVectorRegex().Match(input);
        if (boolMatch.Success)
        {
            var bool1 = BoolParser.Parse(boolMatch.Groups[1].Value);
            var bool2 = BoolParser.Parse(boolMatch.Groups[2].Success ? boolMatch.Groups[2].Value : "0");
            var alpha= bool1 ? 1.0d : 0.0d;
            var beta = bool2 ? 1.0d : 0.0d;
            return new StateVector([alpha, beta]); //normalizzation is handled by the StateVector class
        }

        // Match Single Bool: true q or 1q
        var singleBoolMatch = SingleBoolRegex().Match(input);
        if (singleBoolMatch.Success)
        {
            var value = BoolParser.Parse(singleBoolMatch.Groups[1].Value);
            return new StateVector(value ? [0.0d, 1.0d] : [1.0d, 0.0d]);
        }

        // Match Canonical: |0>
        var canonMatch = CanonRegex().Match(input);
        if (canonMatch.Success)
        {
            return canonMatch.Groups[1].Value switch
            {
                "0" => new StateVector([1.0d, 0.0d]),
                "1" => new StateVector([0.0d, 1.0d]),
                "+" => new StateVector([1.0d, 1.0d]),
                "-" => new StateVector([1.0d, -1.0d]),
                _ => throw new ArgumentException($"Invalid canonical state: |{canonMatch.Groups[1].Value}>"),
            };
        }
        throw new ArgumentException($"Invalid qubit literal format: {input}");
    }
}

public partial class QucharParser
{
    // 'A'q
    [GeneratedRegex(@"^'(.{1})'q$", RegexOptions.Compiled)]
    private static partial Regex CharLiteralRegex();
    public static StateVector Parse(string input)
    {
        if (string.IsNullOrWhiteSpace(input)) throw new ArgumentException("Input cannot be null or whitespace.", nameof(input));
        var match = CharLiteralRegex().Match(input);
        if (match.Success)
        {
            var alphabet = CompilerFlags.Current.QustringAlphabet;
            var size = CompilerFlags.Current.QustringSizeInQubit;
            var character = match.Groups[1].Value[0];
            var qutesEncodedChar = alphabet.IndexOf(character);
            if(qutesEncodedChar == -1) throw new ArgumentException($"Invalid quchar literal: {input}, valid characters are: {string.Join(", ", alphabet)}");
            return QuintParser.Parse($"{qutesEncodedChar}q", size);
        }
        throw new ArgumentException($"Invalid quchar literal format: {input}");
    }
}

public partial class QuintParser
{
    // Integer Literal: 5q
    [GeneratedRegex(@"^(\d+)q$", RegexOptions.IgnoreCase | RegexOptions.Compiled)]
    private static partial Regex IntLiteralRegex();

    // Integer List: [0, 1, 0, 1]q
    [GeneratedRegex(@"^\[\s*((?:\d+\s*,?\s*)+)\]q$", RegexOptions.IgnoreCase | RegexOptions.Compiled)]
    private static partial Regex IntListRegex();

    public static StateVector Parse(string input, int? sizeInQubit = null)
    {
        if (string.IsNullOrWhiteSpace(input)) throw new ArgumentException("Input cannot be null or whitespace.", nameof(input));

        input = input.Replace(" ", string.Empty);

        // Try Parsing as a Single Qubit Literal first
        try
        {
            return QubitParser.Parse(input);
        }
        catch (ArgumentException)
        {
            // If it's not a single qubit, we proceed to Quint-specific rules
        }

        var size = sizeInQubit ?? CompilerFlags.Current.QuintSizeInQubit;
        var bitCount = (int)Math.Pow(2, size);

        // Match Integer Literal: 5q
        var intMatch = IntLiteralRegex().Match(input);
        if (intMatch.Success)
        {
            int value = int.Parse(intMatch.Groups[1].Value);
            input = $"[{value}]q"; // Reuse the integer list parsing logic
        }

        // Match Integer List: [0, 2, 7]q
        var intListMatch = IntListRegex().Match(input);
        if (intListMatch.Success)
        {
            var content = intListMatch.Groups[1].Value;
            var elements = content.Split(',', StringSplitOptions.RemoveEmptyEntries).Select(int.Parse);

            var amplitudes = new double[bitCount]; //TODO: Expensive! optimize allocation
            foreach (var part in elements)
            {
                amplitudes[part] += 1.0d;
            }
            return new StateVector(amplitudes.ToList());
        }
        throw new ArgumentException($"Invalid quint literal format: {input}");
    }
}

public partial class QustringParser
{
    // This pattern identifies escaped quotes
    [GeneratedRegex(@"^""((?:[^""\\]|\\.)*)""\s*q$", RegexOptions.Compiled)]
    private static partial Regex StringLiteralRegex();

    public static StateVector Parse(string input)
    {
        if (string.IsNullOrWhiteSpace(input)) throw new ArgumentException("Input cannot be null or whitespace.", nameof(input));

        // We only Trim() start/end, we do NOT remove internal spaces like in Qubit/Quint parsers
        // because spaces inside the string literal are valid data.
        input = input.Trim();

        var match = StringLiteralRegex().Match(input);
        if (match.Success)
        {
            var content = match.Groups[1].Value;

            // Handle basic escape sequences if necessary (e.g. unescaping \" to ")
            content = Regex.Unescape(content);

            // Convert string to bytes. 
            // We use ASCII to ensure a fixed 8-qubit width per character.
            // "A" (65) -> 01000001 -> |0>|1>|0>|0>|0>|0>|0>|1>
            byte[] bytes = Encoding.ASCII.GetBytes(content);

            var amplitudes = new List<double>();

            foreach (byte b in bytes)
            {
                string binary = Convert.ToString(b, 2);
                foreach (char bit in binary)
                {
                    //amplitudes.Add(bit == '1' ? (0.0, 1.0) : (1.0, 0.0)); //TODO: migrate qustring to be an array of quchar
                }
            }
            return new StateVector(amplitudes);
        }

        throw new ArgumentException($"Invalid qustring literal format: {input}");
    }
}