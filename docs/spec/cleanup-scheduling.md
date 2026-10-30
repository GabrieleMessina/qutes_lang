# Versioned cleanup and reversible operations

Implementation status: `cleanup.Scheduler` and the reversible Qiskit adapter are
implemented and tested independently of source lowering. They do not yet accept
an entire constructed source program. Measurement checkpoints and dynamic branch
integration remain pending; no CLI command claims those capabilities.

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
intermediate recipes. Arbitrary external input states cannot be erased. Ordinary
overwrite of an unknown root is rejected; reversible updates remain accepted.
The dependency analysis is deliberately conservative about cancelled dependencies.

Overwriting a basis-derived value records its cleanup plus replacement preparation
as one reversible history step. Older consumers can therefore still reconstruct
the old version. The composite step records every other touched register at its
entry version, including released registers whose entry state is zero.

## Evidence and boundaries

Tests compare complete complex amplitudes against independently constructed
expected states, with arbitrary entangled reference inputs. They cover changed
inputs, multiple dependencies, released intermediate recomputation, overwrite,
cyclic rejection, root ownership, controlled arithmetic, and zero scratch output.
This evidence establishes the scheduler and gate adapter, not full source-language
execution or measurement-safe cleanup. See the current knowledge-base checkpoint.

The distinction between basis computation and superposition preparation is informed
by [Silq's documented qfree restrictions](https://silq.ethz.ch/documentation).
Qutes does not expose those annotations in source syntax. The addition adapter
uses [Qiskit's ModularAdderGate contract](https://quantum.cloud.ibm.com/docs/en/api/qiskit/qiskit.circuit.library.ModularAdderGate),
verified against the installed pinned Qiskit version rather than assuming latest
online documentation implies runtime compatibility.
