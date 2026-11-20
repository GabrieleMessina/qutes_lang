# Core value semantics

Extracted from the historical development plan. The active [0.4 contract](language-v0.4.md)
supersedes earlier array copying, readonly-only parameters, arithmetic and indexing
restrictions below. Read 0.3 for membership/search and 0.2 for script amendments.

### Syntax and types

Use braces, semicolons, explicit declarations, conventional precedence, top-level
functions, and executable top-level statements (0.2). The name `main` has no special
execution behavior; call it explicitly if desired. Require initialization before use. Classical
types are `bool`, `int`, `char`, `string`, and `void`, with one-dimensional arrays.
Construction-time classical integers have arbitrary precision.

Each compilation uses one resolved integer width, character alphabet, and string
capacity. Compiler options override project settings, which override defaults.
Record the effective settings in generated artifacts. Reject out-of-range
integer initializers and conversions; quantum addition itself wraps.

Supported quantum arithmetic is addition, `+=`, and `rotateLeft`/`rotateRight`.
Rotation counts are nonnegative construction-time integers reduced modulo the
width. Rotations include the sign bit; they are not arithmetic shifts. Support
signed integer comparisons and Boolean combinations of quantum predicates.

No implicit conversion from a quantum value to a classical value is permitted.
Measurement makes that boundary explicit. Safe lifting of construction-time
classical values into matching quantum types is supported.

### Assignment, copying, and automatic cleanup

Specify these separately; syntax alone is not the semantic rule:

1. Initialization creates a value, including preparation and computed expressions.
2. `quint b = a` creates a correlated basis-value copy, not an independent clone
   of an arbitrary quantum state. It is not an alias for the same register.
3. A reversible self-update such as `a = a + 2` may reuse storage.
4. General reassignment needs dependency analysis and may require temporary
   versions. It is accepted only when all required cleanup is established.

Evaluate assignment right-hand sides using the pre-assignment values. Analyze
overlapping operands explicitly: `a += b` with distinct registers must not be
treated as the same case as `a += a`. Doubling modulo a fixed width loses
information if represented only in the original register. V1 should reject a
self-overwrite such as `a = a + a` when it cannot establish safe cleanup, rather
than using an invalid in-place adder.

Track computations, source versions, preparation effects, and measurement
boundaries. Preserve dependencies until they are no longer needed; distinguish
user values from scratch registers. Clean scratch storage before reuse. Reject
unsupported programs with source-level explanations instead of hidden measurement
or silently retained garbage.

Functions borrow their quantum parameters read-only, without implicit copies.
Quantum return values may depend on caller-owned inputs; track those lifetimes
through inlining. Reject returns that strand required local quantum information.
Returned owned storage is transferred to the caller, not cleaned at function exit.

### Three execution categories

The compiler infers categories without requiring staging keywords:

| Category | V1 behavior |
| --- | --- |
| Construction-time classical | Evaluate while building the circuit; supports ordinary classical arithmetic and loops. |
| Quantum | Lower operations and coherent conditions to circuits without measurement. |
| Runtime classical | Results of measurement; usable in supported conditions and outputs, not construction-time loops or indexing. |

For coherent `if`, compute the predicate, control the branch operations, and clean
the predicate. Initially require condition inputs to remain unchanged in both
branches. Branches must be measurement-free, cannot introduce fresh
superpositions, and cannot alter construction-time classical state or storage
shape. Quantum Boolean predicate operands must be effect-free; do not apply
ordinary short-circuit evaluation when both predicates must be represented.

All loops expand during construction. Known classical input parameters may
determine their iteration sequence. Exceeding the expansion or evaluation budget
is an intentional diagnostic. Quantum-dependent loops and measurement-driven
loops are deferred, even though Qiskit provides classical dynamic loop operations.

Measurement-driven `if` lowers to classical feedforward, not coherent control.
Its conditions support comparisons and Boolean combinations of observed values.
Its bodies perform supported measurement-free quantum operations. General
arithmetic on observed values, conditional observations, and dynamic allocation
are deferred. Preserve compatible live-value and shape information at branch joins.

### Non-consuming measurement

`measure` maps quantum scalars and arrays to their classical counterparts.
Decode `quint` as signed; decode text through the effective alphabet and length.

- The quantum source remains usable in its post-measurement state.
- Every measurement creates a distinct classical snapshot. Later evolution or
  measurement must not overwrite earlier snapshots that remain live.
- A later operation must use the post-measurement state, not an earlier version
  of the value or the original preparation assumptions.
- Measurement may change correlated values' joint state. Never model it as a
  read-only classical lookup.
- Do not invert a computation through a measurement boundary as though the
  measurement were reversible. Clean temporary computations before the boundary
  when required and possible; reject unresolved cases.
- Explicit measurement can permit subsequent conditional clearing or known-state
  reinitialization. Accept such assignments only when dependency checks succeed;
  do not add an implicit measurement to make an overwrite work.
- Physical reuse of storage is an implementation detail and must preserve this
  logical behavior.

Since 0.2, measurement is allowed in scripts and functions outside conditional
bodies. Effects are inferred transitively; indirect conditional measurement fails. This allows multiple observations interleaved with
evolution and measurement-driven branches without adding conditional measurement
merging to the first release.

### Arrays and text

Arrays are homogeneous, one-dimensional, and fixed in length during circuit
construction. Numeric arrays created by size start at zero; Boolean arrays start
at false. Text-element defaults use the first configured alphabet character or
the empty string, respectively. Support literals, indexing, indexed assignment,
`.Length`, `foreach`, copying, and measurement. Reject out-of-range or unavailable
runtime indices. `foreach` exposes a read-only element view without allocating a
copy per iteration. Use indexed assignment to update elements.

The alphabet contains at least two distinct Unicode scalar values in explicit
order; the current default ABC contains three. Use the minimum whole number of bits needed
for its codes. Reject unsupported literals, duplicate entries, and unused codes
at decoding. No automatic normalization or general Unicode text processing is
implied by custom characters.

Quantum strings have fixed capacity and a construction-time logical length.
Support literals, copies, equality, indexing, `.Length`, and measurement. Padding
is internal. Reject overlong strings and branch joins with incompatible logical
lengths. Concatenation, resizing, and superpositions of different logical string
lengths are deferred. `superposition()` does not accept text types in V1.

