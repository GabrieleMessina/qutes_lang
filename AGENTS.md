# Instructions for contributors and implementation agents

## Resume before changing code

1. Read `docs/knowledge/README.md`, then STATUS, TASKS, and DECISIONS.
2. Read the latest LEDGER and VALIDATION entries and inspect `git status`/`git log`.
3. Read the relevant language specification and acceptance cases. The development
   plan is the roadmap; knowledge-base status says what actually exists.
4. Choose the first unblocked task. Do not mistake planned or parsed syntax for
   implemented/validated semantics.

## Continuity contract

- Maintain a knowledge base in the repository. Record each meaningful work batch,
  finding, decision, failed attempt, and verification result in LEDGER.
- Keep STATUS and TASKS current at checkpoints and before ending work. Include a
  concrete next action, limitations, environment commands, and blockers.
- Put lasting decisions in DECISIONS with a reason and status. Distinguish user
  decisions from implementer defaults and unverified hypotheses.
- Record exact validation commands, results, environment, and limits in VALIDATION.
- Update existing records rather than leaving contradictory summaries. Retain the
  ledger's history; corrections should be explicit.
- Do not claim independent human review has occurred. The user's authorization to
  start permits implementation of documented working defaults; material semantic
  changes require a decision record and discussion when product intent is unclear.

## Implementation and validation

- Follow the active language specification and `DEVELOPMENT_PLAN.md` roadmap; maintain familiar assignment and non-consuming
  measurement. No function-only evolution rule and no use-after-measurement error.
- Separate parsing, typing/staging, cleanup, circuit lowering, and execution.
- Keep the reference semantics independent of backend circuit construction.
- Test phases/correlations and scratch cleanup, not only classical counts.
- Unsupported cases must fail deliberately. Never silently substitute measurement
  for uncomputation, or claim the entire compiler exists because probes pass.
- Use small deterministic tests and bounded simulator workloads.
- Do not spawn other agents unless the user explicitly requests delegation.

## Git

- Commit coherent completed units with related code, tests, and knowledge updates.
- Do not make a commit for every file or command. Avoid amend/rewrite of history
  unless explicitly requested; do not add a remote or push without authorization.
- Before a commit inspect the diff, run relevant checks, and record their results.
- Never commit local environments, caches, generated build products, or secrets.
