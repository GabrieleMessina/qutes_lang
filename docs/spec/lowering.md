# Source lowering status and API

`lowering.lower(constructed_program)` connects construction IR to versioned
storage, cleanup schedules, backend-independent gates, and result descriptors.
`Program.to_qiskit()` emits a QuantumCircuit. This is an API available from a
checkout/install; full command-line build/run tooling is still pending.

```python
from qutes.checker import analyze
from qutes.config import CompilerConfig
from qutes.construction import construct
from qutes.lowering import lower
from qutes.parser import parse

source = "int main() { quint n=5; n=n+2; return measure(n); }"
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
- Lexical scopes, owned helper-result transfers, borrowed parameters, construction-
  time loops/functions already expanded by the preceding pass.
- Non-consuming measurements with separate snapshots, signed integer/Boolean
  result decoding, classical result arrays and predicates.
- Source spans, allocation manifests, cleanup events, deterministic operation IR,
  bounded scheduler work. No hidden measurement/reset fallback.

All lexical-scope temporaries must be clean before leaving their scope. Main's
remaining values are live circuit outputs until shot completion; they are not
silently reset by source lowering. Released storage remains physically reserved
so historical recipes can be reconstructed. This increases qubit requirements.

The positive source cases A001-A006 and A010-A012 have exact output-distribution
tests, and A004 executes through Aer. All 16 negative corpus cases now produce
their intended category through the complete applicable pipeline. Additional
source tests verify full complex states, local scratch, nested arithmetic,
function ownership, measurement checkpoints, and explicit unsafe cleanup errors.

## Pending integration

Quantum comparisons/Boolean combinations and dynamic if statements, quantum
arrays/text/indexing, feedforward predicates, full result codecs, allocation reuse,
resource reporting, program serialization, and CLI execution remain pending.
Unsupported lowering produces a source-located diagnostic; it is never ignored.
The parser/analyzer/constructor support more syntax than this lowerer currently
executes. A partial lowering API does not satisfy release readiness.

Next work must handle conditional overwrite as a whole transformation: both old
value cleanup and replacement preparation need the branch condition. Guarding only
the new preparation would erase the old value on the unselected branch. Quantum
condition storage must remain unchanged, and its version must be captured in every
controlled history step. Scope cleanup must preserve those controls too.
