using System.Collections;
using System.Diagnostics.CodeAnalysis;
using System.Runtime.CompilerServices;

using CommunityToolkit.Diagnostics;

namespace QutesLang.Utils;

public static partial class QutesLanguageGuard
{
    public static IEnumerable<T> AreAllAssignableToType<T>(IEnumerable values, [CallerArgumentExpression(nameof(values))] string name = "")
    {
        foreach (var value in values)
        {
            IsAssignableToType<T>(value!, name);
        }

        return values.Cast<T>();
    }

    public static T IsAssignableToType<T>(object value, [CallerArgumentExpression(nameof(value))] string name = "")
    {
        if (value is T castedValue)
        {
            return castedValue;
        }
        ThrowArgumentExceptionForIsAssignableToType<T>(value, name);
        return default;
    }

    /// <summary>
    /// Throws an <see cref="ArgumentException"/> when <see cref="IsAssignableToType"/> fails.
    /// </summary>
    [DoesNotReturn]
    public static void ThrowArgumentExceptionForIsAssignableToType(object value, Type type, string name)
    {
        throw new ArgumentException($"Parameter {name} must be assignable to type {type.ToTypeString()}, was {value.GetType().ToTypeString()}.", name);
    }

    /// <summary>
    /// Throws an <see cref="ArgumentException"/> when <see cref="IsAssignableToType{T}"/> fails.
    /// </summary>
    /// <typeparam name="T">The type being checked against.</typeparam>
    [DoesNotReturn]
    public static void ThrowArgumentExceptionForIsAssignableToType<T>(object value, string name)
    {
        throw new ArgumentException($"Parameter {name} must be assignable to type {typeof(T).ToTypeString()}, was {value.GetType().ToTypeString()}.", name);
    }
}