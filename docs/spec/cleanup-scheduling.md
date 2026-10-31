# Versioned cleanup and reversible operations

Implementation status: `cleanup.Scheduler`, measurement checkpoints, and the
Qiskit adapter are implemented. Source lowering includes coherent branches and
quantum collections and measured feedforward. See [source lowering](lowering.md)
for the exact supported subset and API.

## Storage and history

Each allocation owns distinct physical bits, ordered least-significant first.
Version -1 means all-zero storage. Initialization creates version 0; every update
records a reversible gate sequence and the exact versions of its other operands.
All later versions remain available as recipes, not additional physical copies.
The current implementation reserves physical bits for the whole circuit, including
released values; reuse/allocation optimization is a later task.

Allowed primitive operations are X, H preparation, correlated XOR copy, modular
addition, constant addition, and rotation. Controls have explicit true/false
values. Read operands may not overlap mutation targets. The adapter avoids
duplicating an operand when a control bit is also part of an addition source.

## Automatic cleanup

To undo a recorded update, restore the recorded versions of its inputs temporarily,
apply its inverse, and restore those inputs to their current versions. Released
basis-derived values can be recomputed into their reserved zero bits and cleaned
again. Temporary input restoration may neither mutate nor read the value being
erased. This prevents cyclic schedules such as erasing `b` after `b = a; a += b`.

Restoration applies recursively and is bounded by both a work budget and nesting
limit. Failures produce Q3001 (unsafe dependency) or Q4001 (resources). Failed
individual releases roll back emitted operations and logical versions. A scope
tries reverse allocation order and retries other locals when a dependency must
be cleaned first. Source spans and cleanup events explain the resulting schedule.

Independent superposition roots are different from computed basis values. A root
may be unprepared only when no live value depends on it, including through released
intermediate recipes. Unmeasured arbitrary external input states cannot be erased.
Overwrite of an unmeasured unknown root is rejected; reversible updates remain accepted.
The dependency analysis is deliberately conservative about cancelled dependencies.

Overwriting a basis-derived value records its cleanup plus replacement preparation
as one reversible history step. Older consumers can therefore still reconstruct
the old version. The composite step records every other touched register at its
entry version, including released registers whose entry state is zero.

Conditional overwrite guards the complete composite step, including cleanup of the
old value. It records the condition register's version like any other quantum read.
If restoring old inputs would mutate the condition, reject the schedule. Nested
controls are normalized; contradictory controls are identity operations.
Runtime conditions are immutable Boolean expressions over snapshot bits. They
guard the complete composite update as well, and survive inverse scheduling
unchanged. They do not borrow the corresponding quantum source's current value.

## Explicit measurement checkpoints

Each source measurement emits an operation with fresh classical bits and leaves
the register live. A checkpoint records its current version and result bits. To
clean it later, reverse subsequent basis updates to that version, then use the
recorded bits to conditionally flip it to zero. No additional measurement is added.
To reconstruct an earlier version, initialize from the same stable snapshot and
reverse/advance the recorded basis updates. Original histories are not discarded.

Measuring a dependent can also collapse a superposition root. Track connected
dependencies in both directions and invalidate the root's original preparation
as a cleanup recipe. Without its own explicit measurement checkpoint, such a root
cannot be cleaned by reversing its old H gates. This is conservative: the compiler
does not yet infer a root's value from an indirectly measured invertible copy.

A directly measured root can be cleaned or overwritten while correlated values
remain live: its measurement already made the observed basis value explicit.
Its old versions remain reconstructible from the snapshot, subject to the same
cycle and version checks. Future operations evolve the post-measurement state.

## Evidence and boundaries

Tests compare complete complex amplitudes against independently constructed
expected states, with arbitrary entangled reference inputs. They cover changed
inputs, multiple dependencies, released intermediate recomputation, overwrite,
cyclic rejection, root ownership, controlled arithmetic, and zero scratch output.
Exact projected-branch checks cover measurement cleanup and retained reference
entanglement; Aer executes emitted dynamic circuits. Source coverage is currently
the scalar subset, not the full language. See the current knowledge-base checkpoint.

The distinction between basis computation and superposition preparation is informed
by [Silq's documented qfree restrictions](https://silq.ethz.ch/documentation).
Qutes does not expose those annotations in source syntax. The addition adapter
uses [Qiskit's ModularAdderGate contract](https://quantum.cloud.ibm.com/docs/en/api/qiskit/qiskit.circuit.library.ModularAdderGate),
verified against the installed pinned Qiskit version rather than assuming latest
online documentation implies runtime compatibility.
