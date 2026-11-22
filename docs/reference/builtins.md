# Preparation and value operations

Signatures use the Qutes convention of placing the result before the name. A capitalized placeholder such as `Element` stands for the corresponding concrete type in your program.

## superposition

```text
QuantumType superposition()
QuantumType superposition(ValueType[] values)
QuantumType superposition(ValueType[] values, probabilities: weights)
QuantumType superposition(ValueType[] values, amplitudes: weights)
```

Use these forms when initializing a `qubit` or `quint`. Without arguments the preparation covers every representable value. An explicit list selects distinct, representable values and gives them equal weight by default. List contents and weights must be known at construction.

```qutes
quint draw = superposition([-1, 2], probabilities: [0.25, 0.75]);
return measure(draw);
```

Each shot returns −1 with probability ¼ or 2 with probability ¾. Probability weights must be nonnegative and sum to one. Amplitude weights are numbers whose squared magnitudes sum to one. Both lists must match the value list in length. Normalization tolerates rounding error up to 1e-12. Preparation creates a new quantum value.

## complex

```text
complex complex(float real, float imag)
```

Construct a complex number from its real and imaginary parts. For example, `complex(0.0, 1.0)` represents i. In `amplitudes: [complex(0.6, 0), complex(0, 0.8)]` the probabilities are 0.36 and 0.64. The relative phase also affects later interference.

## rotateLeft and rotateRight

```text
quint rotateLeft(quint value, int amount)
quint rotateRight(quint value, int amount)
```

Rotate the fixed-width bit pattern by a nonnegative construction-time count. Bits passing one end reappear at the other. To update a variable, assign the expression back to it: `value = rotateLeft(value, 1);`. With four bits, rotating 0100 left once gives 1000, interpreted as −8.

## copy

```text
Element[] copy(Element[] arrayOrSlice)
```

Allocate independent array storage and copy the elements. For quantum elements this copies basis values coherently. The original and the copy can be correlated. For a worked example of a slice and its copy, see [Arrays and text](collections.md).

See also [gates](gates.md), [measurement](measurement.md), and [search](search.md).
