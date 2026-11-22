# Functions and control flow

Write a script directly at the top level. Functions have an explicit return type and can be called before their definition. A function named `main` is called only if your script calls it. Variables must be initialized before use, including root variables accessed through a function.

## Parameters and mutation

```qutes
void flipWhenSet(qubit control, mut qubit target) {
    if (control) { not(target); }
}

qubit enable = true;
qubit lamp = false;
flipWhenSet(enable, lamp);
return measure(lamp);
```

This returns `true`. Parameters are read-only unless marked `mut`. Here `target` borrows the caller’s qubit and the gate changes `lamp`. Passing the same qubit twice would ask the gate to write its own control. Borrow checks also apply to overlapping slices, global variables and nested calls. A mutable array parameter can rebind its caller’s variable. Recursion is unsupported.

## Three kinds of condition

| Condition | When its value is used | Effect of `if` |
| --- | --- | --- |
| Construction-time classical value | While building the circuit | Selects which block to build |
| Quantum predicate | During coherent execution | Controls operations while preserving the superposition |
| Previously measured value | During a shot | Applies operations depending on the recorded result |

Use braces and optional `else` or `else if` blocks. Keep quantum controls unchanged inside their controlled operations. Measurement inside conditional bodies is restricted, including when hidden inside a function. For classical feedforward, measure before the dynamic branch.

## Loops

```qutes
int[] values = [2, 4, 6];
int total = 0;
foreach (int value in values) { total += value; }
return total;
```

This returns 12. Use `foreach (int value, int i in values)` to obtain the zero-based index as well. The iteration variables are read-only. A range such as `0..values.Length` excludes its upper endpoint.

`for (int i = 0; i < 3; i++)` and `while (condition)` expand during construction. Their conditions and iteration counts must be resolvable before a shot. Size allocations and mutable indices likewise require construction-time values. Supply these as [inputs](configuration.md) when they should vary between builds.
