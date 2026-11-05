# Project knowledge base

This is the durable handoff for any human, agent, or model continuing Qutes.
Read in this order:

1. [STATUS](STATUS.md): what exists, current work, blockers, exact next step.
2. [TASKS](TASKS.md): ordered work, dependencies, and completion evidence.
3. [DECISIONS](DECISIONS.md): user choices versus working defaults.
4. [LEDGER](LEDGER.md): chronological work and findings, including failures.
5. [VALIDATION](VALIDATION.md): reproducible checks and their limitations.
6. [Development plan](../../DEVELOPMENT_PLAN.md): the short product roadmap (contracts live in the specification).

Authority: current user instructions > recorded user decisions > active language
specification > roadmap > examples. Conflicts must be recorded and resolved, not
silently interpreted. Implementation behavior is not automatically the spec.

Each work batch should leave enough information for a fresh agent to explain
what changed, why, how it was checked, and what to do next. At an interruption,
check the working tree as well as these records: the last batch may be uncommitted.
