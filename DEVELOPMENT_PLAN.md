# Qutes development plan

Updated: 2026-10-31

Status: V1 research implementation completed at KB-011; see the
[release audit](docs/release-audit.md) for requirement coverage and evidence.
This document supersedes the earlier conversational plan where they differ.
See [current status](docs/knowledge/STATUS.md) for implemented capabilities and
[the ledger](docs/knowledge/LEDGER.md) for progress; roadmap items are not claims
of existing compiler support.

## 1. Goal and release boundary

Build a strongly typed, high-level quantum language with a compact C#-inspired
syntax. Users express values, arithmetic, functions, and control flow. The
compiler manages storage, circuit construction, and automatic uncomputation.

V1 is a reliable command-line research tool that emits readable Qiskit Python,
runs locally using Qiskit Aer, decodes results, and reports resource requirements.
Its audience does not need C# experience or knowledge of gate-level programming.

Development is mostly performed by an AI implementation agent. Small tasks,
explicit semantic contracts, independent verification, and review gates are part
of the delivery plan, not optional polish.

## 2. Decisions and amendments

### Confirmed direction

- Native quantum types: `qubit`, `quint`, `quchar`, and `qustring`.
- Signed fixed-width `quint`, using two's complement and wraparound addition.
- Plain type names with project-wide sizes and compiler overrides, rather than
  explicit width parameters in every declaration.
- Configurable character alphabet and fixed-capacity quantum strings.
- Fixed-length arrays, user functions, `if`, `while`, `for`, and `foreach`.
- Coherent quantum conditions in `if`; loop bounds and array indices must be
  known during circuit construction.
- Addition and bit rotation; zero-filling shifts are not a V1 feature.
- Correlated quantum value copying with separate storage.
- Familiar assignment, including `number = number + 2`, `number += 2`, and
  `number = rotateLeft(number, 1)`, subject to compiler safety checks.
- Automatic uncomputation with explicit rejection of unsupported dependencies.
- Mid-circuit measurement and same-circuit measurement-driven `if`.
- Measurement is NON-CONSUMING: later operations act on the measured variable's
  post-measurement state. Each classical measurement result is a snapshot.
- Simulator-first delivery; later support for hybrid classical/quantum pipelines.

### Superseded proposals

- Do not enforce initialization once followed only by function-based evolution.
- Do not replace ordinary operators with `.add()` or mutation-only functions.
- Do not treat measurement as ending the source variable's lifetime.
- Do not issue use-after-measurement errors merely because a value was measured.
- Do not introduce `mut` or `ref` parameters as an already-approved feature.

### Working defaults, not separately approved requirements

These fill remaining details for the first specification milestone. Change them
in the specification before implementing a different behavior.

- Working names: Qutes, `.qut`, and the `qutes` command.
- Preparation spelling: `superposition()`; measurement spelling: `measure(x)`.
  The user questioned the earlier `uniform()` and `observe()` names, but did not
  explicitly select replacements. These names remain provisional. Keep them
  centralized and settle them at the specification review gate.
- `superposition()` prepares an equal, positive-amplitude superposition across
  the declared `qubit` or `quint` domain. Arbitrary state preparation is deferred.
- Keep the original V1 read-only function parameter model. Functions may return
  new quantum values; explicit mutation parameters are a later extension unless
  the specification review changes this choice.
- Default integer width: 8 bits. Default alphabet: ASCII in code-point order.
  Default quantum string capacity: 2 characters.
- Default simulator qubit limit: 24, configurable. Generation of larger circuits
  is allowed; local execution checks limits before simulation.
- Default maximum shots per local run: 1,000,000, configurable. Report reserved
  wires and pre-decomposition gate costs; check qubit limits again after transpilation.
- Default total loop-expansion limit: 10,000 iterations per build, plus a bounded
  evaluator step budget so construction cannot hang outside loop accounting.
- Array literals use `[1, 2, 3]`; sized construction uses `new quint[3]`.
- No namespaces, classes, accessibility modifiers, inheritance, overloads,
  generics, recursion, references, closures, or large standard library in V1.

## 3. Language contract to formalize before parser implementation

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
order; default ASCII contains 128. Use the minimum whole number of bits needed
for its codes. Reject unsupported literals, duplicate entries, and unused codes
at decoding. No automatic normalization or general Unicode text processing is
implied by custom characters.

Quantum strings have fixed capacity and a construction-time logical length.
Support literals, copies, equality, indexing, `.Length`, and measurement. Padding
is internal. Reject overlong strings and branch joins with incompatible logical
lengths. Concatenation, resizing, and superpositions of different logical string
lengths are deferred. `superposition()` does not accept text types in V1.

## 4. Architecture and interfaces

Implement in Python, with separate components:

1. Lexer/parser with a documented grammar and source locations.
2. Name resolution, typing, staging, and inferred effect analysis.
3. Structured typed intermediate representation with value versions and branches.
4. Dependency/lifetime analysis and automatic uncomputation.
5. Circuit lowering and storage allocation.
6. Qiskit Python generation, Aer execution, and result decoding.

Do not emit circuits directly from parser visitors. Do not implement the
independent reference evaluator by calling the circuit-lowering implementation.

Commands: `qutes check`, `qutes build`, `qutes run`, and `qutes explain`.
Generated modules expose `build(inputs)` returning a circuit and result layout,
and `run(inputs, shots, seed)` returning decoded results and execution metadata.
Inputs are classical; each shot starts a fresh execution.

Output metadata includes compiler/language and dependency versions, source
identity, effective settings, ordered result layout, and resource estimates.
Keep language signedness and character order independent from Qiskit bit-string
display conventions. Provide readable diagnostics with stable codes/source spans
and a machine-readable representation.

Keep orchestration, circuit building, execution, and decoding separate so later
hybrid pipelines can connect quantum stages with classical work. Do not assume
live quantum state survives separate jobs.

## 5. Specification review and correctness gates

Before the full parser, create an executable acceptance corpus and small backend
probes for the highest-risk behavior. These must cover:

- `number = number + 2`, `+=`, rotation assignment, and rejected unsafe overwrites.
- Correlated copies; changing a source before its dependents are cleaned.
- Coherent comparisons, controlled branch bodies, and clean temporary predicates.
- Measurement followed by further evolution and a second measurement.
- Two live measurement snapshots with different results after an update.
- Measurement of one member of a correlated pair, with correct remaining state.
- Cleanup before measurement and rejection of unsupported cross-boundary cleanup.
- A classical measurement result controlling a later operation in the same circuit.
- Non-power-of-two alphabets, negative integer results, and array result ordering.

For example, using the provisional measurement name:

```csharp
quint number = 5;
int before = measure(number);
number = number + 2;
int after = measure(number);
return after;
```

This must produce 7, while the reference execution records `before` as 5. The
measurement must neither consume `number` nor make `before` track its later value.

Test layers:

- Parser/typing: precedence, scopes, initialization, conversions, function returns,
  staging errors, and intentional unsupported-feature diagnostics.
- Arithmetic: exhaustive small-width basis cases, signed overflow/comparisons,
  rotation boundaries, and operand overlap.
- Quantum semantics: independent complex-state comparisons up to global phase,
  entangled reference inputs, correlated copies, and clean scratch registers.
  Probability-only agreement is insufficient for coherent operations.
- Measurement: independently check branch probabilities and conditional states;
  measurement creates branches or mixtures, not one deterministic pure state.
- Integration: executable generated Python, deterministic builds, resource guards,
  bounded construction, seeded execution smoke tests, and installation checks.

Use tiny widths/alphabets for exhaustive tests. Quantum arithmetic and cleanup
must pass independent verification before adding optimization. Never weaken an
acceptance test merely to match generated code.

## 6. Schedule and delivery process

Planning baseline: 22 weeks, with up to 8 additional weeks reserved for correctness
and integration. These are estimates, not commitments based on AI generation
speed. Reforecast after the cleanup prototype and again after dynamic execution.

| Weeks | Milestone | Exit evidence |
| --- | --- | --- |
| 1-2 | Semantic contract and feasibility | Approved syntax corpus; grammar/effect rules; provisional names resolved; backend probes for arithmetic, cleanup, repeated measurement, and feedforward. |
| 3-5 | Compiler foundation | Parser, typed IR, diagnostics, bounded classical evaluator, independent small-state evaluator. |
| 6-10 | Arithmetic and cleanup | Addition, rotations, copies, safe reassignment, dependency/lifetime analysis verified on coherent states. |
| 11-13 | Functions and control flow | User functions, coherent `if`, classical loops, branch cleanup, and expansion errors. |
| 14-16 | Arrays and text | Encoding, arrays, strings, `foreach`, configuration, and resource accounting. |
| 17-19 | Observation and feedforward | Non-consuming measurement, preserved snapshots, measurement boundaries, classical conditionals, and decoding. |
| 20-22 | Research release | Packaging, examples, documentation, regression suite, reproducible builds, and release report. |
| Reserve: 4-8 weeks | Contingency | Resolve correctness/backend/resource defects without silently changing semantics. |

The current workspace began empty. Bootstrap a usable Python environment, verify
a compatible Qiskit/Aer combination with the early probes, and lock exact
dependencies. Validate Windows and add Linux CI compatibility coverage.

For mostly autonomous development, use versioned specifications, short decision
records, and small tickets. Every ticket states behavior, exclusions, acceptance
tests, verification commands, and completion evidence. Separate implementation
and verification passes. Review gates are the language contract, cleanup
feasibility, integrated dynamic execution, and release acceptance.

No feature is complete without positive and negative tests plus relevant quantum
semantic evidence. Unsupported behavior produces a deliberate source-level error,
not a backend exception or an approximation.

## 7. Later roadmap

- Hybrid execution foundation (initial estimate 6-10 additional weeks): classical
  orchestration, multiple stages, parameter binding, repeated evaluations, and
  bounded measurement-driven loops.
- Higher-level algorithms (8-12 weeks): predicate-based search and selected
  optimization workflows, including preparation, interference, and observation.
- Hardware execution (6-10 weeks): backend capabilities, submission, job tracking,
  hardware resource reports, and noise-aware verification.
- Developer experience: editor integration, richer diagnostics, debugging views,
  and broader distribution as a separately estimated milestone.

V1's preparation, basis-value computations, and observation are a foundation;
they are not by themselves a promise of quantum speedup or a complete algorithm
library. Re-estimate the later roadmap using V1 implementation evidence.

## 8. Technical references

- [Modular Synthesis of Efficient Quantum Uncomputation](https://arxiv.org/abs/2406.14227)
- [IBM: classical feedforward and control flow](https://quantum.cloud.ibm.com/docs/en/guides/classical-feedforward-and-control-flow)
- [IBM: classical expressions](https://quantum.cloud.ibm.com/docs/en/api/qiskit/circuit_classical)
- [IBM: bit ordering](https://quantum.cloud.ibm.com/docs/en/guides/bit-ordering)
- [Qiskit Aer simulator guide](https://qiskit.github.io/qiskit-aer/tutorials/1_aersimulator.html)

## Approved 0.2 increment: scripts and ANTLR (2026-11-01)

1. Replace handwritten lexing/parsing with ANTLR 4.13.2 and retain the AST/IR
   boundary. Commit generated Python and reproducible generator/hash checks.
2. Execute ordered top-level statements; infer explicit classical return types.
   Main is ordinary; functions share readable/writable globals, and root input
   declarations replace main arguments. Infer call effects, including measurement,
   while retaining cleanup, readonly borrow, dynamic-control, and staging rules.
3. Migrate examples/docs/tests, version generated artifacts, reject legacy imports
   before execution/respecialization, and validate full suites plus installed
   packages on Windows/Linux. Preserve user experiments and maintain the ledger.

These decisions supersede earlier main-only entry/measurement assumptions. The
active specification is docs/spec/language-v0.2.md; checkpoint evidence is in the
knowledge base. Runtime-driven loops and hybrid orchestration remain future scope.
