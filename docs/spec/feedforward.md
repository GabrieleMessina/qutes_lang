# Measurement-driven conditions

Runtime `if` conditions compile to immutable Boolean expressions over recorded
snapshot bits. The expressions are backend-independent (`classical.Predicate`);
`feedforward.predicate` converts typed result values, and the Qiskit adapter emits
classical `if_test` operations. The quantum source stays live and may evolve.

Signed integer comparisons sign-extend both operands before comparison, including
classical constants outside the observed register's range. They never truncate
such constants or interpret negative integers as unsigned. Balanced equality/less-
than networks avoid linear nesting depth and exponential truth tables. Conditions
also support Boolean combinations, helper results, and indexed array/text results.

Text equality uses the configured alphabet and logical lengths. A classical
literal outside the alphabet cannot equal a valid observed text value; it is not
an implicit quantum conversion. Earlier text snapshots retain their original
length when the source changes. Array result ordering remains source ordering.

Guards apply to every branch operation, including the whole cleanup/replacement
sequence for overwrite. They compose with coherent quantum controls. Inversion
retains the same immutable guard. Conditional array permutations never use the
unconditional storage-transfer optimization. Some dependency cycles are still
rejected with Q3001 instead of retaining hidden garbage.

Measurements inside conditional bodies remain outside V1. A direct measurement
in a short-circuited runtime RHS is likewise rejected: emitting it eagerly would
change the program. Explicitly measure first and combine snapshots when both
observations are intended. Construction-time short-circuiting remains supported.

The adapter constructs fresh Qiskit expression nodes for each tree occurrence,
because backend expression nodes may be mutable. It uses the documented
[classical expressions](https://quantum.cloud.ibm.com/docs/en/api/qiskit/circuit_classical)
and [feedforward APIs](https://quantum.cloud.ibm.com/docs/en/guides/classical-feedforward-and-control-flow).
Online examples may target newer Qiskit; compatibility is established by tests on
the pinned Qiskit 2.3.0 / Aer 0.17.2 environment, not inferred from those examples.

Evidence includes exhaustive small signed comparators, exact conditional complex
states, immutable snapshot checks, and execution of all positive source examples
through Aer. Hardware capability/submission support is a later roadmap item.
