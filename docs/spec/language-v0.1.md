> Historical 0.1 contract. Superseded by [version 0.2](language-v0.2.md).
> Automatic main execution and measurement-free helpers below no longer apply.

# Language contract, working version 0.1

Status: implementation default, 2026-10-30. Grammar and examples are now concrete;
this is not a claim that the complete language has been implemented. See the
knowledge-base capability status. Builtin spellings remain changeable defaults.

## Syntax

[grammar.ebnf](grammar.ebnf) defines the syntax. UTF-8, ASCII identifiers, brace
blocks, explicit types, declarations with initializers, and conventional precedence.
Names are case-sensitive. Decimal integers are unsigned lexical tokens; unary
minus is applied before an initializer range check so `-128` is valid at 8 bits.
No classes, namespaces, implicit declarations, overloads, recursion, method calls,
bitwise source operators, ternary expressions, or assignment expressions.

All functions are top-level. Exactly one `main` is required by semantic checking,
not by parsing. Parameters and non-main return values may be quantum. Main takes
only construction-time classical arguments and returns classical data or void.
Return on all required paths and unsupported quantum-conditional returns are
semantic checks. Bare return is permitted only for void functions.

Parser implementation limits: at most 100,000 digits per integer token (Q1001),
64 nested parsing contexts and 128 syntax
tree edges from the root. Overly deep source is a Q1002 diagnostic, never a raw
recursion error. Offsets count source Unicode code points, end positions are
exclusive, and lines/columns start at one. CRLF is one line break; a leading BOM
does not count as a visible column. Raw control characters in literals must be
escaped. The untyped tree preserves grouping and source locations.

Parameters are read-only bindings; quantum parameters borrow storage without an
implicit copy. Ordinary local assignments are permitted with cleanup checks.
The compiler must not infer that every quantum state may be overwritten merely
because the source uses normal assignment syntax.

## Values, operations, and staging

Use the type/assignment/measurement contract in [core value semantics](value-semantics.md). Construction-
time classical int is arbitrary precision. Division truncates toward zero and
remainder has the dividend's sign. Division by zero is a diagnostic. Boolean
conditions do not accept integer truthiness. No implicit quantum-to-classical
conversion; measurement is explicit.

Quantum integer operators: +, +=, signed comparisons, and named rotations. `-`,
`-=`, multiplication, division, remainder, and ++/-- are classical-only in V1;
adding a negative classical constant is allowed. Both quantum operands of an
addition must have the resolved width. Quantum comparisons produce qubit predicates.
Classical predicates use ordinary short-circuit behavior; quantum predicate
operands are effect-free and represented coherently.

`superposition()` is context-typed only by an initializing qubit/quint declaration.
It is not a random sampler and is not a generic reset operation. `measure(value)`
returns a classical snapshot and leaves the source available. Rotations take a
quint and a nonnegative construction-time integer count. No builtin aliases.

Classical measured values cannot drive construction-time loops, indices, array
sizes, or rotation counts. V1 supports them in comparisons/Boolean combinations
for feedforward and in returned results. General arithmetic on measured values
is deferred. Quantum if bodies cannot change their predicate dependencies.

Measurement is allowed in main outside if bodies; helpers remain measurement-free.
An expanded construction-time loop may include measurement when it is in main
and outside an if body; allocate distinct snapshot bits for each expanded occurrence.
No observation-driven loops, conditional measurement, or hidden measurement.
Consequently, a measurement on the right of `&&`/`||` with a runtime left operand
is rejected with Q2004: eager evaluation would violate short-circuit semantics,
and conditional measurement is outside V1. Read previously measured snapshots
instead. Construction-time short-circuiting can skip an observation normally.

## Configuration and encodings

`qutes.toml` contains a single `[qutes]` table. Keys match CompilerConfig fields:
quint_bits, alphabet, qustring_capacity, max_simulation_qubits, max_simulation_shots,
max_loop_iterations, max_evaluation_steps, max_classical_bits. Overrides take priority. Unknown keys
or invalid values are errors. Settings are part of every build's identity.
External input JSON has a 100,000-digit integer-token limit and a 512-level nesting
limit before type validation. Compiler-authored embedded artifact integers instead
honor the configured classical memory bound; global Python digit settings are unchanged.

Integers encode modulo 2**width and decode with the high bit as sign. Alphabet
codes follow configuration order. Unused codes are invalid. String storage is
fixed-capacity, padded with code zero, with a separate construction-time logical
length. Empty strings are distinct from strings containing the first alphabet
character. Nonzero padding is an internal invariant failure, not user text.

Arrays have fixed construction-time length, one dimension, no quantum indexing,
and value-copy assignment. foreach is a read-only view, not a per-iteration copy.
The only property is `.Length`. Shape-changing dynamic branches are rejected.

## Storage and measurement boundaries

Expression evaluation uses pre-assignment values. Distinct source/target addition
is reversible; aliased doubling is not interchangeable with it. Track dependencies
and source versions before choosing storage reuse. Reject unsafe overwrites.

Scratch temporaries must be cleaned and disentangled before reuse. A known inverse
of a temporary computation is not by itself evidence that it is safe after its
inputs change or are measured. A measurement cut invalidates such assumptions;
analysis must establish a valid schedule or reject the program.

Every measurement snapshot has a separate logical identity. Two measurements of
the same unchanged register agree in an ideal execution. Evolving it afterward
does not retroactively change the earlier snapshot. Later operations use its
post-measurement state; correlated values are handled as part of the joint state.

## Stable diagnostic categories reserved for the checker

These codes express intended failures; parser/typing/cleanup support is tracked
separately. Diagnostics include path, one-based line/column, and a concise reason.

| Code | Meaning |
| --- | --- |
| Q0001 | Cannot read a source file as UTF-8 |
| Q0002 | Invalid or unreadable build configuration |
| Q0003 | Invalid or unreadable classical input JSON file |
| Q0004 | Artifact output failure or refused overwrite |
| Q1001 | Invalid token, escape, literal, or unterminated comment/string |
| Q1002 | Unexpected token or missing syntactic element |
| Q2001 | Invalid types, literal range, conversion, or unsupported operation |
| Q2002 | Invalid name, duplicate definition, builtin collision, or recursion |
| Q2003 | Wrong stage for loop/index/allocation/rotation |
| Q2004 | Forbidden effect: readonly parameter, measurement in helper/branch, predicate dependency mutation |
| Q2005 | Invalid return or entry-point contract |
| Q3001 | Cleanup cannot be established, unsafe overwrite, or invalid overlap |
| Q4001 | Construction budget, bounds, or resource limit exceeded |
| Q5001 | Optional Qiskit/Aer dependency unavailable |
| Q5002 | Backend circuit construction or execution failure |
| Q5003 | Circuit diagram rendering failure |

See `tests/acceptance/cases.json` for source examples with expected categories.
The corpus is a target contract. Type/stage/effect failures now run through the
analyzer; cleanup failures now run through scalar lowering. Every semantic-negative case must still
parse successfully. Frontend validation does not prove uncomputation safety.

## Typed analysis implementation

The typed IR records each expression's type, stage, source location, symbol reads,
effects, and known shape. Read-only classical helpers specialize for construction
or runtime inputs: comparisons can operate on measured values, while a helper
performing arithmetic on those values receives Q2003. Parameter values themselves
are not assumed constant; actual evaluation belongs to the construction pass.

Analysis checks both branches for types/effects, merges branch state, and forgets
loop-mutated constant values so the first iteration is never mistaken for the
final value. Dynamic branches cannot return or change outer classical variables.
Local construction-time loop variables inside a dynamic branch are permitted.
Both arms must agree on known collection shapes; unresolved shapes are checked
again during concrete circuit construction. Array lengths are fixed after creation.
String indexing is read-only in V1; replace a whole string or use a quchar array
when indexed updates are needed.

Classical short-circuiting suppresses evaluation faults in an unused operand but
does not hide name/type errors. Constant folding stops above 4096 result bits;
this is an analysis optimization limit, not a semantic integer-width limit.
Semantic traversal has the configured evaluation-step budget; call nesting is
bounded at 64 to avoid host recursion failure. The construction pass has its own
budget and must validate deferred ranges, bounds, and cleanup.

## Construction implementation

The bounded evaluator expands classical loops, specializes actual main inputs,
and inlines helpers while keeping quantum values symbolic. See
[construction-ir.md](construction-ir.md) for the downstream storage/cleanup contract.
Memory limits diagnose oversized classical integers instead of wrapping them.
`max_classical_bits` defaults to 65,536 and is configurable independently of quint
width. Loop iterations are counted globally, including nested loops and helpers.
Construction itself does not prove cleanup or generate a Qiskit program. The
subsequent [lowering pass](lowering.md) does so for scalars, arrays, text, and both
coherent and measured control flow. [Delivery interfaces](../guide.md) expose
complete check/build/run/explain commands and generated-module APIs.
