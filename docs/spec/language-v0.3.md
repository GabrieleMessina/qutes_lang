# Language contract, version 0.3 (implementation in progress)

Extends language-v0.2.md. Membership is implemented; search is being implemented.
This document does not imply that the release checkpoint has passed.

## Membership

`pattern in sequence` has comparison precedence. A scalar tests element membership;
a sequence tests a contiguous run. Resolve against the right element type first:
`"AB" in words` tests whole entries, whereas `["AB","CD"] in words` tests a run.
Strings/qustrings support character indexing, Length, foreach, and matching with
character arrays, without becoming assignment-compatible with char arrays.

Left character/text `?` matches exactly one character, including quantum patterns.
There is no star wildcard or literal-question-mark escape. A classical wildcard
does not require an alphabet entry; storing a quantum question mark does.
Empty sequence patterns match all sequences; oversized patterns never match.
Repeated/overlapping matches combine by OR. Classical operands yield bool;
any quantum operand yields qubit. Measured/runtime operands are deferred.
Operands evaluate once, left to right. Matching preserves branch amplitudes and
does not measure, reset, or amplify. Work qubits are uncomputed automatically.

## Approved search contract (pending implementation)

`search(collection, oracle)` accepts a named pure one-element quantum predicate
returning qubit. It returns the selected quantum value, retaining its index as
owned quantum state. Strings in a searched collection must have equal lengths;
empty collections fail. Classical collections lift to quantum element types.
The configurable failure probability defaults to 0.01, conditional on at least
one match within each collection basis branch. No hidden measurement or retries.
No matches yields a nonmatching candidate. The program may measure the oracle
on the result. Quantum data and selected values may become entangled.
