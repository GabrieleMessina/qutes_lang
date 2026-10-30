# Work ledger

Append meaningful batches, failures, choices, checks, and handoff points. Use stable
entry IDs; do not rewrite history to hide failures.

## KB-001 — 2026-10-30 — Repository and continuity bootstrap

- User requested implementation, a knowledge-base workflow, and logical commits.
- Inspected workspace and ancestor instructions: only DEVELOPMENT_PLAN.md existed;
  no applicable ancestor AGENTS.md was found.
- PATH `python` and `py` failed as inaccessible Windows application aliases.
- Registry inspection found `C:\ProgramData\anaconda3\python.exe` (3.13.5).
  Confirmed installed Qiskit 2.3.0, Aer 0.17.2, NumPy 2.1.3, pytest 8.3.4.
- Initialized local Git on main; existing Git author identity is available. No
  remote created and no global settings/packages changed.
- Added contributor instructions, ignored generated artifacts, and this knowledge
  base with status, tasks, decisions, validation, and links to the roadmap.
- Initial Git staging failed because this environment protects `.git` writes.
  Retry uses the elevated Git operation authorized by the user's commit request;
  no file-permission changes or deletion of lock files are needed.
- Next: semantic contract, executable acceptance inventory, dependency pins, and
  independent backend feasibility checks. See T002-T004.

## KB-002 — 2026-10-30 — Specification and backend feasibility

- Committed KB-001 as `a29edbf`. Git's whitespace check caught extra blank EOF
  lines before that commit; normalized them and established LF attributes.
- Added a working EBNF grammar and language contract, diagnostic categories, and
  33 source examples (17 positive, 16 negative). Their semantic execution remains
  pending; the manifest records the intended first failure stage and outcomes.
- Added a Python package skeleton, central builtin vocabulary, validated config,
  signed arithmetic codecs, and configurable text encoding. Added exact installed
  dependency pins; no global packages were changed.
- Built an independent small-state oracle based on index permutations/projections,
  plus separately constructed Qiskit experiments. Checked coherent addition and
  rotation, correlated copy, compute/use/uncompute, and dynamic measurement with
  subsequent evolution and retained classical snapshots.
- First direct pytest attempt: 34 passed, 1 fixture setup error caused by the host
  temporary directory. No semantic test failed. Added tools/check.py to use fresh
  task-owned artifact directories and disable unrelated pytest plugin autoload.
- Second run passed all 35 then-existing tests. Installed IBM runtime contributes
  deprecation warnings through Qiskit plugin discovery; this is documented rather
  than hidden. Added corpus integrity and unchanged-repeat-measurement checks.
- Names remain documented working defaults; no independent human review is claimed.
- Next checkpoint: final M1 verification, then parser/source-location work T005.
