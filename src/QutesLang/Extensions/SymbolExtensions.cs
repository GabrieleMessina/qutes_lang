using QutesLang.Symbols;
using QutesLang.Symbols.Types;
using QutesLang.Symbols.Types.Interfaces;

namespace QutesLang.Extensions;

public static class SymbolExtensions
{

    /// <summary>
    /// Returns the symbol as the specified type T, or throws an ArgumentException if it is not of that type.
    /// </summary>
    /// <typeparam name="T">The type to which the symbol should be cast.</typeparam>
    /// <param name="symbol">The symbol to cast.</param>
    /// <returns></returns>
    public static T As<T>(this Symbol symbol) where T : Symbol
    {
        return QutesLanguageGuard.IsAssignableToType<T>(symbol, nameof(symbol));
    }

    /// <summary>
    /// Casts all elements of the specified symbol sequence to the specified derived type, ensuring type safety.
    /// </summary>
    /// <remarks>If any element in the sequence is not assignable to type T, an exception is thrown. This
    /// method is useful when working with symbol collections that are known to contain only a specific derived
    /// type.</remarks>
    /// <typeparam name="T">The type to which all symbols in the sequence must be assignable. Must derive from Symbol.</typeparam>
    /// <param name="symbols">The sequence of symbols to cast to type T. All elements must be assignable to T.</param>
    /// <returns>An enumerable collection of symbols cast to type T.</returns>
    public static ICollection<T> As<T>(this IEnumerable<Symbol> symbols) where T : Symbol //TODO: interface is not easy to understand, probably a rename could improve.
    {
        return [..QutesLanguageGuard.AreAllAssignableToType<T>(symbols, nameof(symbols))];
    }

    /// <summary>
    /// Asserts that the given symbol, which is expected to be a ValueSymbol, contains a value of type T and returns it.
    /// </summary>
    /// <typeparam name="T">The type of the value contained within the ValueSymbol.</typeparam>
    /// <param name="symbol">The symbol to check.</param>
    /// <returns></returns>
    public static T Contains<T>(this Symbol symbol) where T : IQutesValue
    {
        return symbol.As<ValueSymbol>().Value.As<T>();
    }

    /// <summary>
    /// Asserts that all values within the given TupleValue are of type ValueSymbol and returns their contained values as type T.
    /// </summary>
    /// <typeparam name="T">The type of the value contained within the ValueSymbol.</typeparam>
    /// <param name="tuple">The tuple to check.</param>
    /// <returns></returns>
    public static ICollection<T> Of<T>(this TupleValue tuple) where T : IQutesValue
    {
        return [..tuple.Values.As<ValueSymbol>().Select(s => s.Value.As<T>())];
    }

    /// <summary>
    /// Asserts that all values within the given ArrayValue are of type ValueSymbol and returns their contained values as type T.
    /// </summary>
    /// <typeparam name="T">The type of the value contained within the ValueSymbol.</typeparam>
    /// <param name="array">The array to check.</param>
    /// <returns></returns>
    public static ICollection<T> Of<T>(this ArrayValue array) where T : IQutesValue
    {
        return [..array.Values.As<ValueSymbol>().Select(s => s.Value.As<T>())];
    }
}
