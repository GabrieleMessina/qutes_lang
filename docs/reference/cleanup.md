# Assignment, cleanup and wire reuse

Quantum values can be updated, measured, passed to functions and returned. Qutes tracks how each value was computed so it can release temporary storage at the end of its lifetime.

## Reversible updates

```qutes
quint counter = 1;
{
    quint next = counter + 1;
}
counter += 1;
return measure(counter);
```

The inner block creates a temporary. Leaving the block lets the compiler reverse its calculation and restore its work wires to zero. The outer counter remains available and the result is 2.

A temporary can depend on an older version of a value. The compiler can sometimes reconstruct that version to undo the work. A phase, basis change, measurement or live external dependency can make that proof fail. Replacing an unknown register with a constant can also erase information. Qutes reports a cleanup diagnostic when it cannot implement the update safely.

## Read a resource report

`qutes explain FILE` distinguishes logical allocations made over the program’s lifetime from physical qubits required at the same time. A wire certified to be zero may be reused later. Measurement leaves a qubit in its observed state and by itself does not certify a reusable zero.

Compare the report with `qutes explain FILE --no-wire-reuse`. For diagrams, `--wire-view logical` shows the original allocations and `--wire-view physical` shows the actual simulator wires. The view changes the drawing. The reuse setting changes allocation. Try the [wire reuse experiment](https://qutes-lang.web.app/play.html#reuse) to see the difference.
