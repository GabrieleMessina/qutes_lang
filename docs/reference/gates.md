# Gates

Gate calls are statements. `mut qubit` means the gate updates the qubit you pass. Use a mutable variable or an array element at a known index. Apply gates to an entire array with a loop.

| Signature | Action on the target |
| --- | --- |
| `void hadamard(mut qubit q)` | Maps 0 to equal positive amplitudes for 0 and 1. Starting from 1 gives a negative amplitude for 1. Applying it twice restores the input. |
| `void not(mut qubit q)` | Exchanges the amplitudes for 0 and 1. |
| `void phaseFlip(mut qubit q)` | Changes the sign of the amplitude for 1. |
| `void phase(mut qubit q, float angle)` | Multiplies the amplitude for 1 by exp(i × angle). Supply a finite construction-time angle in radians. |
| `void swap(mut qubit a, mut qubit b)` | Exchanges the states of two distinct qubits, including their correlations with other wires. |

## Make a phase visible

```qutes
qubit q = false;
hadamard(q);
phase(q, pi);
hadamard(q);
return measure(q);
```

The phase adds a relative minus sign. The last Hadamard turns it into a measurable 1. Changing the angle to 0 gives 0 instead. For a controlled gate, wrap the call in `if (control) { ... }`. A qubit control stays coherent, while a measured Boolean controls the gate from its recorded bit.
