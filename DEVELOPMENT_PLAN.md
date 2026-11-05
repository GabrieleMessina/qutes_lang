# Qutes product roadmap

Qutes is a strongly typed quantum language with compact C#-inspired syntax. Users
express values and computations; the compiler manages circuits and uncomputation.

## Current authority

- [Language 0.3](docs/spec/language-v0.3.md) and [core value semantics](docs/spec/value-semantics.md): language contracts.
- [Status](docs/knowledge/STATUS.md), [tasks](docs/knowledge/TASKS.md), and [decisions](docs/knowledge/DECISIONS.md): delivered work and active choices.
- [Historical development plan](docs/history/development-plan-v0.3.md): original milestones and rationale, retained rather than treated as current implementation status.

## Current increment

Improve circuit register names, source-level diagrams, cleanup annotations,
unfolding controls, resource formatting, and CLI guidance. Rendering must preserve
execution semantics. Wildcard matching remains distinct from state preparation.
See T021-T023 in the knowledge base for delivery checkpoints.

## Future work

- Safe physical reuse of zeroed wires after their final required lifetime.
- Explicit preparation of quantum text distributions.
- Hybrid quantum/classical pipelines and runtime-dependent iteration.
- Broader arithmetic and collection capabilities, with explicit semantic contracts.

These are directions, not implemented features. Preserve familiar assignment,
non-consuming measurement, explicit measurement boundaries, phase/correlation
correctness, and deliberate rejection of impossible cleanup. Never insert hidden
measurement/reset or promise an overall speedup from oracle-query counts alone.
