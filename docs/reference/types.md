# Types and expressions

A declaration gives a value a type and a name. Write `quint score = 3;` to prepare a quantum integer, or `int score = 3;` to calculate with a classical integer. A script executes its top-level statements in order and returns a classical result.

| Classical | Quantum | Values |
| --- | --- | --- |
| `bool` | `qubit` | `false` or `true` |
| `int` | `quint` | Signed integers. The quantum register has a configured bit width. |
| `char` | `quchar` | One character, written with single quotes. Quantum characters use the configured alphabet. |
| `string` | `qustring` | Text in double quotes. Quantum text has fixed capacity and a known logical length. |
| `float` | | Finite, construction-time floating-point value, such as `0.25` or `1e-3` |
| `complex` | | Finite, construction-time real and imaginary components |
| `void` | | Function with no returned value |

## Numbers and assignment

```qutes
quint score = 3;
score += 2;
return measure(score);
```

This returns 5 with the default four-bit register. Initial values must fit the signed range −8 through 7. Subsequent quantum additions and subtractions wrap at that width. For example, adding 1 to 7 gives −8. A quantum assignment must preserve enough information for [cleanup](cleanup.md).

Integer arithmetic includes `+`, `-`, `*`, `/` and `%` on construction-time integers. Quantum integers support addition, subtraction and negation. Use [rotations](builtins.md) to move their bits cyclically. Multiplication and division of quantum integers are unsupported. Classical integers widen to `float` and then `complex` when required. `pi` is available for angles in radians.

## Expressions and comparisons

From tighter to looser binding: calls, indexing and member access; unary `!`, `+` and `-`; multiplication, division and remainder; addition and subtraction; range `..`; ordering and membership; equality; `&&`; `||`. Use parentheses when combining comparisons. Qutes spells equality `==`, inequality `!=` and assignment `=`.

A comparison such as `score < 3` can yield a qubit when the operands are quantum. Put it in an `if` to control a gate, or [measure](measurement.md) it to obtain a classical bit. Construction-time Boolean expressions short-circuit. Read a measurement into a variable before combining its result with another condition.

## Source notation

Names may contain letters, digits and underscores and start with a letter or underscore. Terminate declarations, updates and returns with a semicolon. Use braces for blocks. Use `//` for a line comment or `/* ... */` for a block comment. Arrays use `Type[]` and are described in [Arrays and text](collections.md).
