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
- D041 (implementation): runtime guards are immutable Boolean circuits over stable
  snapshot IDs. Sign-extend integer operands; do not truncate classical constants.
  Text guards include logical length and alphabet semantics.
- D042 (clarification of existing effect contract): reject measurement on the RHS
  of runtime short-circuit Boolean operators. Eager emission violates semantics,
  while conditional measurement is explicitly deferred. Snapshot reads are allowed.
- D043 (ownership correction): only explicitly named main quantum values survive
  to shot end. Anonymous helper results and computed arguments remain temporaries
  and must be cleaned, or receive a dependency diagnostic if cleanup is impossible.
- D044 (delivery): generated Python embeds source, effective config, inputs, result
  layout and metadata. The bound circuit is readable Qiskit; new input bindings
  recompile the source using the installed Qutes runtime. Canonical JSON comparison
  distinguishes Boolean/float inputs from integers. No silent frozen specialization.
- D045 (resource defaults): cap shots per call at 1,000,000, configurable. Check
  reserved qubit limits before backend construction and again after transpilation.
  Compilation/generation can exceed the simulation limit, subject to construction
  budgets. Cost reports are pre-decomposition estimates, not device gate counts.
- D046 (delivery): CLI configuration discovery reads source-adjacent qutes.toml
  only; explicit config and then CLI overrides take precedence. Python APIs use
  explicit settings. Artifact replacement is atomic and protects the source file.
- D047 (execution): programs with no measurement have a known classical output;
  run returns that result with backend classical-output and executes no simulator.
  Generated modules depend on Qutes plus the optional backend, rather than pretending
  that a static Qiskit-only file can specialize arbitrary new classical inputs.
- D048 (packaging): replace psutil 5.9.0 with 7.0.0 in the reproducibility pins.
  The clean Python 3.13 Windows install proved 5.9.0 requires unavailable C++ build
  tools. 7.0.0 provides a compatible wheel. No global packages are changed.
- D049 (user request / implementation): print or export the completed compiler
  circuit with --print-circuit and --save-circuit FOLDER on full compiler commands.
  This view includes cleanup/measurement before backend-specific decomposition.
  PNG is default; SVG is optional. Text goes to stderr with --json; image paths
  are returned in circuit_diagram. These options do not alter compilation identity.
- D050 (implementation): use optional Qiskit/Matplotlib visualization with headless
  file rendering and no external LaTeX processes. File names include source stem
  and build-hash prefix; repeat builds atomically replace their image, differing
  bindings/settings get distinct names. Guard image size before rasterization.

- D051 (user approved): migrate to ANTLR 4.13.2 now; commit generated Python
  frontend sources, pin runtime/generator, keep quantum semantics outside grammar.
- D052 (user approved, supersedes entry rules in D033/D043): only top-level
  statements execute automatically; main is ordinary. Explicit classical script
  return, inferred type, no implicit last-expression output. Script globals live
  to shot end; ordinary function locals must clean.
- D053 (user approved): root input TYPE name declarations replace main arguments;
  functions can read/write globals; initialization order is checked transitively.
- D054 (user approved): functions can measure with inferred transitive effects;
  preserve readonly borrows, non-consuming measurement and conditional restrictions.
- D055 (implementation): diagnostic recovery reports at most ten errors and never
  compiles repaired input. Source offsets, stable codes and first-error exception
  fields stay compatible; structured hints and related locations are additive.

- D056 (implementation): every helper call specializes against current globals;
  do not cache by parameter stages alone. Shared global symbol IDs survive inlining;
  function-local ownership remains separate. Read/write effects include global IDs.
- D057 (implementation): input declarations bind when reached and remain mutable;
  input metadata retains original bindings. Functions may appear anywhere, but
  accessing a not-yet-executed global declaration is rejected transitively.
- D058 (implementation): runtime short-circuit RHS cannot measure or write globals;
  statically skipped RHS is typechecked without propagating its state/effects.
- D059 (user preservation): leave edited snapshots.qut untouched. Publish/test the
  canonical script as measurement_snapshots.qut; the preserved file has no automatic
  main execution under 0.2. No exception or hidden migration in the compiler.

- D060 (delivery): package 0.2.0.dev0, language 0.2, artifact schema 2. Generated
  modules use qutes.artifact_v2 and validate metadata before both cached and newly
  bound paths. Retire runtime.layout_from_metadata via an explicit import-time
  migration error so old modules cannot silently reinterpret embedded source.
- D061 (correctness): join global stages/shapes across every function exit, including
  early returns. A later assignment on another path cannot erase a runtime stage.
- D062 (borrow precision): direct quantum loads/indices borrow aliases; computed
  arguments own materialized values and do not borrow their source dependencies.
  Array-element borrows conservatively protect the whole backing array.
- D063 (distribution): ANTLR whitespace normalization is deterministic across OSes;
  generated Python is compiler source, not an ignored build product. Java is needed
  only for regeneration; core installations depend solely on the Python runtime.

- D064 (user approved): `in` is coherent membership/contiguous sequence matching;
  strings are character sequences for sequence operations, not assignment aliases
  of char arrays. Left text `?` matches one character, including quantum patterns.
- D065 (user approved): `search(collection, oracle)` searches entries, not the
  support of a whole candidate array. A named pure oracle receives one quantum
  element and returns qubit. Return a quantum selected value, retain the index,
  and measure explicitly. Equal string entry lengths initially; empty input fails.
- D066 (user approved): automatic Yoder-Low-Chuang fixed-point amplification,
  configurable failure probability default 0.01. Guarantee is conditional on an
  existing match in each data branch. No hidden measurement, retries, enumeration,
  or no-match proof. Duplicate positions retain their weight. Account for linear
  indexed-access circuit cost rather than promising end-to-end speedup.
- D067 (implementation): `[] in []` uses an empty int sequence context, since no
  values constrain the type; other empty literals infer from the opposite operand.
  Existing declaration rules for uncontextualized empty arrays remain unchanged.

- D068 (delivery): version 0.3/artifact 3; retire artifact_v2 imports with rebuild
  instructions before execution or specialization. search is a reserved builtin.
- D069 (implementation): retained selection index and zero workspace share the
  selected value owner. Explicit visible-view measurement invalidates coherence
  without claiming a full-owner checkpoint. Reversible updates remain legal;
  impossible erasure of hidden selection state fails Q3001.
- D070 (implementation): conservatively preflight classical membership comparisons
  and charge quantum character expansion to existing construction work budgets.
  Pure known Boolean factors simplify without changing operand evaluation order.

- D071 (user edit and explicit commit authorization, 2026-11-04): default quint
  width is now 4 and alphabet ABC, superseding D011's original 8-bit/ASCII defaults.
  Include the user's config.py, .gitignore and snapshots.qut edits in this delivery;
  preserve their content. The ignore change excludes grammar/.antlr.
- D072 (implementation): place the complete operation tour in examples/language
  with its own adjacent config (3-bit quint, alphabet AB?, capacity 2, limit 24).
  This makes runnable examples independent of global default changes. Existing
  examples and the user's snapshot experiment remain in place.

- D073 (user approved, 2026-11-05): circuit folding is presentation-only; executable
  circuit structure stays unchanged except named registers. Include depth/filter
  unfolding and cleanup annotations. Defer physical wire reuse.
- D074 (user approved): wildcard predicates do not prepare superpositions. Warn
  once when alphabet contains ?, without changing encoding or rejecting valid use.
- D075 (user approved): retain language 0.3/artifact schema 3; additive provenance
  and warnings metadata. Archive historical roadmap and move contracts into specs.

- D076 (implementation of approved rendering scope): view options belong to the
  renderer/CLI, not CompilerConfig/build identity. Image filenames include a view
  hash. Mixed functions retain measurements/control flow and fold reversible parts.
- D077 (correctness): each cleanup annotation links to a distinct region ID, even
  when zero-operation events share spans/names/ranges. Inverse oracle cleanup is
  labeled recomputation and never receives a false zero-state marker.
- D078 (resource guard): preflight wide lazy backend definitions conservatively
  before generation, then charge expanded instruction/wire references incrementally.
  Exhaustion is Q4001, never silent truncation. No new wire allocation or reuse.

- D079 (user approved, 2026-11-05): implement fixed-schedule certified-zero wire
  allocation first; do not reschedule cleanup or introduce measurement/reset.
  Reconstructed logical values receive new lifetime epochs. This supersedes the
  physical-reuse deferral in D073/D078. Default physical diagrams, optional logical.
- D080 (implementation of approved plan): semantic zero certificates are distinct
  from presentation annotations and published only after successful transactions.
  Unknown/nonzero state remains allocated; last use or measurement is insufficient.
  New builds will use artifact 4; preserve artifact 3 cached execution compatibility.

- D081 (implementation): Program operations/registers/qubit_count are physical after
  compile_source; logical_program retains the original schedule. Allocation/source
  binding metadata explicitly labels its logical coordinate system. Snapshot IDs
  and result layouts remain classical and unchanged. Diagram annotations map at
  the outgoing lifetime boundary and omit zero-only allocations with no wires.

- D082 (user approved,2026-11-20): language0.4 follows language-v0.4.md. Public
  hadamard/not/phaseFlip/phase/swap use if for controlled operations. mut includes
  classical/quantum parameters; readonly applies generally.
- D083 (user approved): T[] arrays/slices share storage by default, copy explicitly
  copies basis values. Text retains value semantics. Returned slices retain and
  report the whole backing allocation. Supersedes implicit array-copy contracts.
- D084 (user approved): float/complex, qubit/quint finite preparation, strict
  normalization1e-12, static proven bounds for coherent reads, signed subtraction
  and negation. Version0.4/artifact5; old3/4 cached execution remains, changed-input
  respecialization requires rebuild.
- D085 (implementation): existing variables named copy remain legal; call-position
  copy resolves the new builtin. Avoid unrelated breakage in scalar-copy examples.

- D086 (implementation): construction uses cells, array identities and views;
  concrete element overlap checks occur during construction after loop expansion.
  analyze remains an intermediate inspection, not a complete compilation check.
  Slices/ranges were implemented in checkpoint1 because reference borrowing needs
  concrete view regions. Mutable transitive rebinding disallows temporary slices.
- D087 (implementation): array literal rebinding creates fresh storage, including
  permutations; retained aliases keep old backing. Old conditional whole-array
  replacement becomes element writes. Source mappings follow new allocation IDs.

- D088 (implementation,0.4): explicit Hadamard/phase/swap updates carry atomic
  unitary history records. Independent dependency replay cannot cross them.
  A completely private connected component may be inverted jointly; any outside
  quantum dependency, measurement or released member prevents that fallback.
  Controlled NOT on an independent quantum root is also a phase-effect barrier,
  including equivalent q=!q syntax, to avoid erasing phase kickback on cleanup.
  This is conservative: some valid ancilla-erasure schemes remain Q3001.

- D089 (implementation): sparse preparation uses conditional prefix rotations and
  leaf phases, with a replayable inverse and no reset, enumeration of the complete
  basis domain or extra selection index. Zero weights are allowed; duplicate basis
  entries are not. Existing independent private preparation under measured control
  remains valid; quantum-controlled preparation remains forbidden.

- D090 (implementation): bounds propagation uses signed finite sets capped at256,
  then conservative enclosing intervals. Arithmetic wraps; joins union supports.
  Only exactly zero supplied amplitudes can be excluded. No measurement result,
  simulation sample or probability cutoff proves bounds. Bounds checking occurs
  in construction after calls/inputs/reference updates, not the type-only pass.
  Indexed reads use controlled XOR copies with no index preparation or amplification.

- D091 (compatibility implementation): schema3/4 adapters inspect only the immediate
  published _binding(inputs) frame because old templates pass metadata without input
  arguments, then call an unversioned compiler. Reject differing inputs before that
  call; preserve cached execution. No globals patching or compiler interception.
- D092 (safety audit): transitive element updates are not array-reference rebinding.
  Global aliases cannot bypass an active mutable borrow; disjoint regions remain
  accessible. A mutable binding may replace a readonly view with new storage;
  writes through the view and rebinding a readonly declaration remain forbidden.

D093 (user): retain the two GitHub repositories, make isolated branches, keep the compiler at root and own reusable resources here. Website code is written fresh. Release uses MIT and static hosting.

D094 (implementation): distribute 0.4.0 via versioned GitHub release assets. Website bundles Pyodide and a bounded physical-program executor. Reuse compiler result decoding; retain Aer and independent test oracles for verification. Deploy from a tested website tag after a Firebase preview.

D095 (user): preserve the original rewrite commits via a merge on qutes2.0 and replace Git tag v0.4.0 with 2.0. Use the release tree as the merge result. The package version and bundle build revision identify the existing verified assets.

D096 (user): publish compiler package 2.0.0 and align website/download labels; rename the website branch to qutes2.0. Dispatch website workflows without waiting. Use a distinct immutable 2.0.0 release tag for the new package. Keep language-contract version 0.4 and artifact schema 5 compatible.

D097 (user): keep inspection inside Playground, teach programmers via an editable walkthrough, retain generated Python export and keep this website revision local for review.

D098 (user): expand Tutorial into a course, obtain a Sol agent review of the interface and functionality, and keep the revision local pending an explicit publication instruction. Implementation choices: teach toward a two-part teleportation project, validate lab observations against browser execution, and save drafts, progress and the self-reviewed final report in the learner’s browser.

D099 (user): ship portable one-folder distributions of the full 2.0.0 CLI with CPU Aer and image export. Attach them to the existing language release. Website publication is separate.

D100 (user): make the website Build page the entry point for platform downloads and the first local program. Keep this website revision local until the owner reviews it. The portable archives are the main path and the Python starter remains available in a disclosure.

D101 (user): publish the corrected first-run defaults under new asset names on release 2.0.0. Keep the website local for review. Use ABC for ordinary examples and explicitly opt in to AB? for examples 22 and 30, which store the marker.

D102 (user, active): the only uploaded 2.0.0 release assets should be the five revision r2 native platforms and one checksum file. This supersedes the asset retention part of D101. Keep all website changes local until the owner approves publication.

D103 (user, active): publish the reviewed website from qutes2.0 to production. Offer the five r2 native archives and retire the old site-hosted teaching ZIP. Delete obsolete implementation branches in both repositories after checking ancestry and open pull requests.

D104 (user, active): the website exports the circuit for the current input binding as one editable Qiskit Python file. It must run with Qiskit and Aer alone. Preserve the CLI export and its input respecialization. Keep both repositories and the preview local until publication is authorized.

D105 (user, active): publish the compiler to qutes2.0 before the website, deploy the website from its qutes2.0 branch, and execute the live playground download in an environment containing only Qiskit, Aer and their dependencies.

D106 (user): deploy the returning-browser cache fix after verification. Stable website URLs require HTTP revalidation. The browser can reuse unchanged bytes with entity tags, and the fix preserves tutorial progress.

D107 (user): prepare an English course companion and an English full workbook as different local website pages for university review. Use original materials with selected extensions. Share experiments in the language resources and compare formats before publication.

D108 (user): keep the full workbook, retire the companion, and review locally before publication.

D109 (user): use the workbook as the tutorial for everyone, with chapter contents and no university-specific framing or topic picker.

Use tutorial for the shared resource folder and workbook for the website renderer and tests, avoiding the existing tutorial.test.cjs name.

D110 (user). Publish five patched 2.0.1 archives on a new release and retain the earlier release URLs. Use protected pull requests for both release branches.

D111 (user). Share compiler-backed diagnostics and completion rules between the browser and desktop editors. Keep one Marketplace identity with five offline packages. Review locally before any publication. D112 (implementation). Embed the checksum-pinned native release archive in each VSIX and unpack it on demand. Limit graphical edits to uniquely mapped top-level qubit calls; show source and provenance for other operations. Preview adjacent Hadamard cancellations without modifying the running program.

D113 (implementation). VS Code Run and Debug launches the same complete circuit simulation as the toolbar. It supports cancellation and Debug Console output. Source-level stepping and breakpoints require separate simulator support. Version the extension update as 2.0.2 so existing installations can upgrade while reusing the verified 2.0.1 compiler.
