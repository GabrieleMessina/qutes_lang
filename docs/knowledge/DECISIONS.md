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
| D019 | Implementation / frontend | Provide a developer `parse` command, explicitly syntax-only. Do not label it `check` before semantic validation exists. Export structured AST/diagnostic JSON with spans. |
| D020 | Implementation / bounded tooling | Bound parsing contexts at 64 and AST depth at 128, including flat operator/postfix chains; excessive input gets Q1002 instead of a recursion traceback. Preserve raw newline offsets. |

All updates add or amend a decision here and explain the change in LEDGER. Earlier
conversation examples suggesting measurement consumption are superseded by D007.

- D021 (implementation): typed IR is separate from syntax and explicitly marks
  cleanup as unverified. Expose developer `analyze`, not full `check`, until the
  cleanup/construction passes exist.
- D022 (implementation): stage-specialize classical helper parameters so measured
  predicates can use helpers without permitting deferred runtime arithmetic.
- D023 (implementation): retain original read-only parameter defaults; do not
  interpret the user's withdrawn evolution proposal as authorization for mut/ref.

- D024 (implementation): foreach is a borrowed element view, so quantum predicate
  protection includes its backing collection, not just the iteration name.
- D025 (implementation): construction emits scoped, call-free/loop-free symbolic
  IR with explicit owned-result moves. Scope annotations do not waive cleanup.
- D026 (implementation): global construction budgets include allocation element
  counts; max_classical_bits=65536 is configurable and errors instead of wrapping.
- D027 (implementation): expose developer `construct` with explicit cleanup-not-
  verified status. Full build/run commands wait for verified lowering.
- D028 (implementation): keep physical bits reserved after cleanup while their
  computation recipes may be needed again. Correct version reconstruction takes
  priority over qubit reuse; resource accounting must expose the resulting cost.
- D029 (implementation): restore captured input versions temporarily during
  cleanup, but reject any restoration that reads the value being erased. Bound
  both scheduling work and dependency depth; never replace failure with reset.
- D030 (implementation): basis-value overwrite retains cleanup plus preparation
  as a reversible history step, preserving older consumers. Independent unknown
  quantum roots still require reversible updates. Measurement support is pending.
- D031 (implementation, extends D030): an explicit measurement records a versioned
  classical checkpoint without consuming its source. Cleanup may use those bits;
  retain prior basis histories for older consumers. A measured value can be safely
  overwritten when its checkpoint-based cleanup schedule is valid.
- D032 (implementation): indirect measurement conservatively invalidates original
  preparations of connected roots. Without a direct checkpoint, reject root erase
  rather than incorrectly reversing H or inserting hidden measurement.
- D033 (implementation): at program end, main's still-live quantum values remain
  circuit outputs until shot completion. Lexical/local temporaries are cleaned;
  end-of-shot disposal is not represented as in-program reset.
- D034 (environment): use Python stream capture in the Windows test runner. Native
  descriptor capture intermittently caused Aer DLL initialization/invalid-handle
  failures. This does not skip tests or change packages; explicit flags may override.
- D035 (implementation): comparisons use reversible XOR-difference scratch and
  first-differing-bit predicates, including signed sign-bit ordering. Avoid
  exponential truth-table synthesis; preserve exact phases and clean scratch.
- D036 (implementation): conditional overwrite guards both old-value cleanup and
  replacement preparation. Capture control versions in histories; reject cleanup
  that would mutate its condition. This preserves the unselected branch's value.
- D037 (implementation): arrays own separate element storage. String indexing is a
  borrowed bit view; observing it uses a temporary copy plus explicit measurement
  and checkpoint cleanup. No implicit observation is introduced.
- D038 (implementation): track each string-array element's logical length through
  construction and lowering; branch joins must agree per element. Snapshot lengths
  remain frozen when their source text changes.
- D039 (implementation): unconditional array self-permutations transfer existing
  element storage. Conditional cases retain the guarded cleanup path; never apply
  unconditional rebinding inside either quantum or runtime-classical branches.
- D040 (resource default): reject quantum type widths above the construction budget
  before encoding large constants/allocating padded arrays, and charge actual bit
  allocations to the scheduler budget. Foreach remains array-only as specified.
