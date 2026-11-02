# Source lowering status and API

`lowering.lower(constructed_program)` connects construction IR to versioned
storage, cleanup schedules, backend-independent gates, and result descriptors.
`Program.to_qiskit()` emits a QuantumCircuit. This is an API available from a
checkout/install. The public `qutes.compiler.compile_source` API and
check/build/run/explain commands compose these passes; see [the guide](../guide.md).

```python
from qutes.checker import analyze
from qutes.config import CompilerConfig
from qutes.construction import construct
from qutes.lowering import lower
from qutes.parser import parse

source = "quint n=5; n=n+2; return measure(n);"
program = lower(construct(analyze(parse(source, "example.qut"),
                                  CompilerConfig(quint_bits=4))))
circuit = program.to_qiskit()
# After execution, decode each shot's complete classical memory as an integer:
# program.result.decode(memory) returns 7 for this program.
```

## Implemented subset

- Scalar qubit/quint initialization, superposition preparation, correlated copies,
  addition, rotation, Boolean negation, reversible self-updates, safe overwrite.
- Nested arithmetic expression temporaries automatically cleaned; operands are
  evaluated using pre-assignment values. Distinct-output doubling is supported;
  overlapping in-place doubling produces Q3001.
- Signed comparisons, Boolean conjunction/disjunction/negation, coherent if/else,
  nested controls, branch-local cleanup, and conditional overwrite. Comparisons
  compute XOR-difference scratch, detect the first differing bit (with reversed
  sign-bit ordering), then clean scratch. No exponential truth table is generated.
- Lexical scopes, owned helper-result transfers, borrowed parameters, construction-
  time loops/functions already expanded by the preceding pass.
- Non-consuming measurements with separate snapshots, signed integer/Boolean
  and text result decoding, array snapshots, classical result arrays/predicates.
- Same-circuit runtime if/else over snapshot comparisons and Boolean expressions,
  including signed constants of different widths, text equality, indexed results,
  predicate helpers, and nesting with coherent controls. See [feedforward](feedforward.md).
- Quantum arrays with separate element storage, indexed updates, value copies,
  borrowed foreach views, owned function returns, and empty-array results.
- Configured character encodings and fixed-capacity padded strings with separate
  logical lengths. Text comparisons include length. String-index reads borrow
  bit views; observation uses a copied view, explicit measurement, and checkpoint
  cleanup, preserving the parent's post-measurement state.
- Source spans, allocation manifests, cleanup events, deterministic operation IR,
  bounded scheduler work. No hidden measurement/reset fallback.

All lexical-scope temporaries must be clean before leaving their scope. The script's
explicitly named values are live circuit outputs until shot completion; they are not
silently reset by source lowering. Released storage remains physically reserved
so historical recipes can be reconstructed. This increases qubit requirements.
Anonymous helper results/computed arguments must be cleaned too; an escaping
helper result does not automatically become a user-owned script value.

All 18 positive source cases have exact output-distribution tests and execute
through Aer. All 16 negative corpus cases now produce
their intended category through the complete applicable pipeline. Additional
source tests verify full complex states, local scratch, nested arithmetic,
function ownership, measurement checkpoints, and explicit unsafe cleanup errors.

## Resource and delivery boundaries

Physical wire reuse remains deferred; reports count all reserved wires. Delivery
now includes deterministic Python artifacts, resource reports, and bounded Aer execution.
Unsupported lowering produces a source-located diagnostic; it is never ignored.
The core lowering API does not by itself satisfy release readiness.

Conditional overwrite guards the whole transformation: both old-value cleanup and
replacement preparation. Guarding only the new preparation would erase the old
value on the unselected branch. Quantum condition storage remains unchanged and
its version is captured in each controlled history step. Scope cleanup preserves
those controls. Contradictory controls emit no operation. Full-state tests cover
signed boundaries, reference entanglement, identical operands, nested predicates,
changed condition inputs after a branch, and clean branch-local storage.

## Collection layout and lengths

Whole-array replacement evaluates the RHS into separate storage before updating
elements, preserving pre-assignment values. Unconditional self-permutations can
transfer existing element storage without extra qubits. Quantum-conditional
replacement uses the normal guarded cleanup path and may reject a dependency
cycle; it must never implement a conditional permutation by unconditional rebinding.

Construction tracks string-array element lengths through copies, helper borrows,
owned returns, indexed replacement, foreach views, and measurement snapshots.
Dynamic branches must agree on each element's length, not just the array length.
Lowering keeps the corresponding physical-storage lengths and joins both arms.
Snapshot descriptors freeze the observed text length even after source overwrite.

Quantum type widths are checked against the construction budget before encoding
large constants or allocating bit tuples. Actual allocations also charge the
scheduler budget. Foreach retains the V1 array-only contract; strings support
construction-time indexed access, including for loops over their Length.
