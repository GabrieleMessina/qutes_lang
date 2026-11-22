# Searching a collection

```text
QuantumElement search(Collection collection, Predicate oracle)
```

`search` returns a candidate from a nonempty collection. Supply the name of a function that takes one quantum element and returns a `qubit` marking a match. Check the candidate with that predicate when your program needs to know whether it succeeded.

```qutes
qubit accepts(quint number) { return number == 1; }
int[] numbers = [0, 1, 1];
quint candidate = search(numbers, accepts);
return measure(candidate);
```

The predicate marks both positions holding 1. Search amplifies marked positions and returns their element value. With no match it still returns a candidate. Repeated values retain their weight as separate positions. Use [membership](collections.md) if the desired answer is simply whether a value occurs.

## Collections and predicates

A string supplies characters. Arrays can supply Boolean, integer, character or string elements, classical or quantum. The candidate has the corresponding quantum type. String entries must have equal length. With a quantum collection the candidate can remain entangled with its source.

The oracle may calculate with its argument and capture construction-time classical globals. Its temporary work must be reversible. Measurement, state preparation, nested searches, global writes and captures of other quantum data are forbidden in the oracle. Invoke search outside quantum or measurement-dependent branches.

## Accuracy and cost

The compiler builds a fixed-point amplification circuit. The configured `search_failure_probability` bounds the failure probability for a collection branch containing at least one match. Its default is 0.01. Smaller bounds can make the circuit larger. Use `qutes explain` to inspect the resources and `--unfold-only` with the oracle name to inspect its gates.
