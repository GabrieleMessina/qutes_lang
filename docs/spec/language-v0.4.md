# Qutes 0.4 approved contract

Approved 2026-11-20. This is the target contract, not a completion claim. Read the
knowledge-base STATUS for delivered behavior; unchanged rules remain in 0.3.

## References and access

T[] arrays use references: assignment shares storage; literals/new allocate;
copy(arrayOrSlice) explicitly copies values (quantum copies are correlated basis
copies, not arbitrary state cloning). Construction-time rebinding may change a
binding's array/length without changing old aliases. Allocations have fixed lengths.
Dynamic branches cannot choose array references/shapes. Array/slice returns share.
Half-open start..end ranges have static integer bounds; descending ranges fail.
Slices require 0 <= start <= end <= Length, are mutable by default and retain the
complete backing allocation until the final reference dies. Report retained wires.
Text keeps value semantics; text slices are read-only character views.

readonly restricts rebinding and writes through a binding, not other aliases or
explicit measurement. Parameters default readonly; mut allows caller-visible
mutation/rebinding for classical and quantum types. Evaluate locations once, left
to right. Temporary slices may be mut arguments only if the transitive callee does
not rebind that parameter. Reject conflicting borrows; allow proven disjoint ranges.
Indexed foreach (TYPE item, int i in values) exposes readonly item/index bindings.

## Numbers and quantum operations

Add static float/complex, arrays, arithmetic, inputs/outputs; finite binary64,
complex(real, imag), pi, widening int->float->complex, no implicit narrowing or
conversion to quantum integers. Complex JSON uses real/imag components with a
Python codec. Reject division by zero/nonfinite values.

superposition(values) and named probabilities: or amplitudes: overloads support
qubit/quint only. All arguments are static. Reject empty/duplicate/out-of-range
values, mismatched lengths and simultaneous weighting forms. Require nonnegative
probabilities summing to one or squared amplitude norm one, tolerance 1e-12,
rounding-only normalization. Preserve superposition(). No reset or text preparation.

Signed quint subtraction, unary negation and -= wrap modulo 2^quint_bits; minimum
negates to itself. Reject information-losing self-overwrites but allow separate
results and reversible self-updates. Validate lifted constants before encoding.

Statement-only hadamard(q), not(q), phaseFlip(q), phase(q, angle), swap(a,b) operate
on mutable qubit locations. Angles are static finite radians; swap needs distinct
locations. phaseFlip=phase(pi), not=q=!q. if supplies coherent/classical control;
no cx/cphase public builtins or whole-array broadcasting. Preserve predicate
protection, staging and conditional measurement/preparation restrictions.

values[quintIndex] returns a correlated quantum basis-value copy, never an lvalue.
Support Boolean/integer/character/string elements and equal logical string lengths.
Prove every signed index valid using conservative budgeted support sets/intervals;
never sample or drop tiny amplitudes. Access uses controlled copies, not Grover,
and uncomputes scratch. No quantum counterpart for float/complex.

## Safety and delivery

Track reference lifetimes, views, ownership and transitive mutations. Phase-aware
atomic multi-owner histories must prevent incompatible dependency replay, erased
observable phases and false zero certificates. Reject impossible cleanup without
reset/hidden measurement; preserve snapshots and certified wire reuse. Preparation
uses sparse reversible rotations/phases and an explicit inverse, not initialize.

Checkpoints: references/types; live operations; preparation/arithmetic; collection
access; integration. Release 0.4/artifact5; retain cached artifact3/4 execution but
require rebuild before old-artifact input respecialization. Migrate old array-copy
assumptions, preserve user files, keep examples within24 physical qubits. Validate
phases/correlations, Bell/teleportation/QFT, ownership/aliases, bounds, cleanup,
Windows/Linux, parser generation, packaging, generated/CLI/diagram/reuse paths.
