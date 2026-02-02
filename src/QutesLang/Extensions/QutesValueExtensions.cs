using QutesLang.Symbols.Types.Interfaces;

namespace QutesLang.Extensions;

public static class QutesValueExtensions
{

    /// <summary>
    /// Returns the value as the specified type T, or throws an ArgumentException if it is not of that type.
    /// </summary>
    /// <typeparam name="T"></typeparam>
    /// <param name="value"></param>
    /// <returns></returns>
    public static T As<T>(this IQutesValue value) where T : IQutesValue
    {
        return QutesLanguageGuard.IsAssignableToType<T>(value, nameof(value));
    }

    /// <summary>
    /// Casts each element of the specified sequence to the specified type T, ensuring all elements are assignable to T.
    /// </summary>
    /// <remarks>If any element in the sequence is not assignable to type T, an exception is thrown. This
    /// method is useful for safely projecting a heterogeneous collection of IQutesValue elements to a specific
    /// subtype.</remarks>
    /// <typeparam name="T">The target type to cast each element to. Must implement IQutesValue.</typeparam>
    /// <param name="values">The sequence of IQutesValue elements to cast. Cannot be null.</param>
    /// <returns>An IEnumerable<T> containing each element of the input sequence cast to type T.</returns>
    public static ICollection<T> As<T>(this IEnumerable<IQutesValue> values) where T : IQutesValue
    {
        return [.. QutesLanguageGuard.AreAllAssignableToType<T>(values, nameof(values))];
    }
}
