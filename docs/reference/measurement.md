# Measuring a quantum value

`measure(value)` reads a quantum value in the computational basis and returns a classical result for the current shot. You can save that result, return it, or use it in later operations that support a measured condition.

## Signature

```text
ClassicalType measure(QuantumType value)
```

`QuantumType` stands for the type you pass in. `ClassicalType` is its classical counterpart. For example, measuring a `qubit` returns a `bool`, and measuring a `quint[]` returns an `int[]` of the same length.

## Use a qubit after measuring it

```qutes
qubit coin = false;
hadamard(coin);
bool first = measure(coin);
not(coin);
return [first, measure(coin)];
```

The Hadamard gives the first measurement an equal chance of returning either bit. Measurement leaves the qubit in the state corresponding to that result. The next gate flips the qubit, while `first` keeps its recorded value. The only possible pairs are `[false, true]` and `[true, false]`. Remove the flip and the two readings agree on every shot.

## Read a register

```qutes
quint[] values = [1, 2];
return measure(values);
```

With the standard configuration this returns `[1, 2]`. Qutes decodes each register using its type. If several values are in superposition, one shot gives one joint outcome. Repeating the program starts each shot from its original preparation.

## When does the result become available?

The result belongs to an execution of the circuit. You can use a measured boolean to control a later flip. A size used to allocate an array must already be known when the circuit is built, so a measurement cannot supply it.

Try the [measurement snapshots experiment](https://qutes-lang.web.app/play.html#snapshots). It adds a correlated copy of the coin. Compare the first two returned bits with the third after the flip.
