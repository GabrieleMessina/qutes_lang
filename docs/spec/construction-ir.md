# Construction IR and ownership handoff

Status: implemented construction pass; quantum scalar/collection lowering is integrated. This is a
compiler interface, not new source syntax. `construct(typed_program, inputs)`
expands classical work while leaving quantum/runtime values symbolic.

Version0.4 updates the earlier normal form below: construction environments hold
mutable cells and array identities/views. Array aliases/rebinding do not allocate;
copy creates storage explicitly. Operations freeze use-time views so later aliases
cannot change already scheduled operands or measurement snapshots. Scope/root
records enumerate surviving quantum references, retaining complete slice backings.
Scalar owned results still move; returned arrays share references. Indexed foreach
and ranges expand statically. quantum_index expressions keep a stable index value
with proven signed support; only write indices must be classical constants.
See [0.4](language-v0.4.md) for the authoritative reference/borrow contracts.

## Normal form

- `Program.body` has no loops or function calls. `scope` and dynamic `if` preserve
  structure. Attached typed templates are provenance, not executable body code.
- Classical values become literals. Quantum operations/runtime predicates remain
  expression trees. Every quantum declaration and measurement gets a fresh symbol.
- Quantum `let` creates storage. A load initializer means correlated value copy;
  `move` instead transfers an owned helper result without cloning it.
- Measurement is a `let` of a `measure` expression. The new symbol is a classical
  snapshot; the source remains live. An unused result does not erase measurement.
- `assign` keeps target/RHS pre-update expressions. The next pass introduces
  storage versions. Compound lvalues and helper-based indices are evaluated once.
- Array lengths, indices, and rotation counts are concrete. Quantum foreach
  temporaries are materialized once before iteration and borrowed by element.

## Scopes and returns

`scope` has one body block, a kind (block/iteration/function), and expressions
identifying quantum results/dependencies escaping a return. Ordinary scope ends
have no escapes. Helpers borrow normalized arguments; computed arguments are
materialized before calling. Every invocation gets fresh local IDs.

Owned returns escape with `move`. A borrowed parameter returned by value is first
copied into owned return storage. Compound returns are materialized inside the
function scope. Nested returning blocks may preserve dependencies until the
parent materializes the expression.

These annotations do NOT prove cleanup. Validate every scope, particularly local
roots correlated with an escaping result. Reject unsafe cleanup rather than
silently retaining roots or resetting them. Function results must be transferred
to callers without allowing hidden escaped dependencies to bypass this check.

## Branches and budgets

Condition stage distinguishes coherent control from feedforward. Construct both
dynamic branches in isolated classical environments. Outer quantum identities stay
stable; resulting string/array shapes must agree. Temporary branch storage still
requires conditional cleanup. No conditional measurement/dynamic return is added.

Enforce global iteration/evaluation budgets. Charge array element counts before
host allocation. Classical integers do not wrap; `max_classical_bits` (65,536 by
default) bounds construction memory independently of quint width. Validate exact
script input names/types, resolved ranges, indices, encodings, lengths, and
shapes. Short-circuiting and early returns avoid unused execution.

## Next pass obligations

1. Resolve logical symbols into versions and source dependencies.
2. Distinguish copies, reversible updates, temporaries, and unsafe overwrites.
3. Prove cleanup for scopes, scratch storage, and measurement boundaries.
4. Preserve snapshots and post-measurement evolution.
5. Lower verified work into backend-neutral circuits, then Qiskit. Experiments
   using manually supplied inverses do not establish this automatic proof.

## Script globals and call effects (0.2)

Typed programs identify globals and inputs separately from functions. Input values
are validated before construction, then become available when each input declaration
executes. The script has an internal entry; user main is an ordinary function.
Each helper receives the current global environment plus its parameter bindings;
updated globals propagate back to the caller. Global quantum storage stays owned
by the script; locals/computed arguments retain their own cleanup scopes.

Analysis specializes each call for current stages/shapes and joins global states
across all function exits, including early returns. Effects record transitive
reads/writes/preparation/measurement. Borrowed load/index arguments protect their
quantum aliases; computed arguments materialize independent owned temporaries.
