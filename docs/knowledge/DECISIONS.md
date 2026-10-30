# Decision register

Date of initial register: 2026-10-30. Status is explicit to avoid inventing approval.

| ID | Status / origin | Decision and reason |
| --- | --- | --- |
| D001 | Accepted / user | Compact C#-style high-level language; strong types; Qiskit target; future hybrid pipelines. Syntax clarity is a primary product goal. |
| D002 | Accepted / user | Types qubit/quint/quchar/qustring, arrays, user functions, if/while/for/foreach, automatic cleanup, addition, bit rotation. |
| D003 | Accepted / user | Simulator-first reliable research tool; primarily AI implementation with durable handoff records. |
| D004 | Accepted / user | Signed wraparound quint; project-fixed widths/defaults with compiler overrides; configurable alphabet. |
| D005 | Accepted / user | Correlated value copies; ordinary assignment and self-update, including `n = n + 2`. Reject unsupported unsafe cases. |
| D006 | Accepted / user | Quantum if and construction-time classical loops; same-circuit measured if in V1; measured loops deferred. |
| D007 | Accepted / user | Measurement is non-consuming. Keep the quantum value live in its post-measurement state; classical results are snapshots. |
| D008 | Rejected / user | Initialize-once/function-only evolution was explicitly withdrawn. Do not resurrect it. |
| D009 | Working default / prior plan | Builtins `superposition()` and `measure(x)`. Centralize names; do not add competing aliases. No explicit user selection of final spelling yet. |
| D010 | Working default / prior plan | Read-only borrowed function parameters; no mut/ref API. Helpers measurement-free; main may measure outside branches. Keeps initial effects/cleanup tractable. |
| D011 | Working default / prior plan | quint width 8; ASCII alphabet; string capacity 2; simulation limit 24 qubits; loop expansion limit 10,000. Tests use smaller configurations. |
| D012 | Implementation / start authorization | Proceed with documented defaults and automated specification checks. Record evidence; do not claim separate human review. Material intent changes require discussion. |
| D013 | Implementation | Python 3.13 environment already available with Qiskit 2.3.0/Aer 0.17.2. Verify this pair before claiming compatibility; do not upgrade global packages. |
| D014 | Accepted / user | Local Git history, commits for coherent completed work, not every edit. No remote/push requested. |
| D015 | Implementation / working syntax | Require braces for branch/loop bodies; bracket array literals; ASCII identifiers and UTF-8 text; no assignment expressions. Concrete grammar is in docs/spec. |
| D016 | Implementation / reproducibility | Validate the existing pinned environment without changing global packages. Use tools/check.py with workspace-local temporary directories because the host's default pytest temp directory is inaccessible. |
| D017 | Implementation / semantic default | Classical integer division truncates toward zero; remainder follows the dividend. Logical strings use code-zero padding and a distinct known length. |
| D018 | Implementation / scope | Backend probes and the independent test oracle are experiments, not a compiler backend or automatic-cleanup engine. Acceptance manifest checks do not claim semantic execution. |

All updates add or amend a decision here and explain the change in LEDGER. Earlier
conversation examples suggesting measurement consumption are superseded by D007.
