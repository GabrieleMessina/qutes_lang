# Language contract, version 0.3

Extends [language-v0.2](language-v0.2.md), retaining scripts, inputs, functions,
assignment and non-consuming measurement. See the knowledge base for validation
evidence and environment limits. Package 0.3.0.dev0; generated artifact schema 4.

## Membership

`pattern in sequence` has comparison precedence. A scalar tests element membership;
a sequence tests a contiguous run. Resolve against the right element type first:
`"AB" in words` tests whole entries, whereas `["AB","CD"] in words` tests a run.
Strings/qustrings support character indexing, Length, foreach, and matching with
character arrays, without becoming assignment-compatible with char arrays.

Left character/text `?` matches exactly one character, including quantum patterns.
There is no star wildcard or literal-question-mark escape. A classical wildcard
does not require an alphabet entry; storing a quantum question mark does.
Empty sequence patterns match all sequences; oversized patterns never match.
Repeated/overlapping matches combine by OR. Classical operands yield bool;
any quantum operand yields qubit. Measured/runtime operands are deferred.
Operands evaluate once, left to right. Matching preserves branch amplitudes and
does not measure, reset, or amplify. Work qubits are uncomputed automatically.

## Search contract

`search(collection, oracle)` accepts a named pure one-element quantum predicate
returning qubit. It returns the selected quantum value, retaining its index as
owned quantum state. Strings in a searched collection must have equal lengths;
empty collections fail. Classical collections lift to quantum element types.
The configurable failure probability defaults to 0.01, conditional on at least
one match within each collection basis branch. No hidden measurement or retries.
No matches yields a nonmatching candidate. The program may measure the oracle
on the result. Quantum data and selected values may become entangled.

```csharp
qubit accepts(qustring text) { return "?B" in text; }
string[] texts = ["AA", "AB", "BB"];
qustring candidate = search(texts, accepts);
return measure(candidate);
```

Use alphabet `AB` and capacity 2 for a small simulation. `search` is a builtin
expression, with exactly two arguments. The second is a function name, not a
function call or arbitrary function-valued expression. No general first-class
functions are introduced. A string collection yields quchar; bool/int/char/string
arrays yield qubit/quint/quchar/qustring respectively, including quantum arrays.
Duplicate positions retain their weight. Search does not generate a domain of
all possible values and does not enumerate all successful values classically.

The oracle takes exactly one quantum element parameter and returns qubit. It can
call helpers and capture construction-time classical globals, specialized at each
call. Transitively reject measurement, preparation, nested search, global writes,
runtime-classical inputs and extra quantum captures. Readonly parameter and alias
rules apply. Search cannot execute under a quantum/runtime condition. Oracle
locals may use supported reversible calculations; scratch must clean.

The compiler prepares a uniform private index over exactly N entries, constructs
controlled indexed access, computes the oracle, marks its phase, and uncomputes.
Yoder-Low-Chuang fixed-point amplification uses the conservative lower bound 1/N
when there is a match. The schedule is chosen from `search_failure_probability`
(finite, strictly between 0 and 1; default 0.01), without enumerating oracle
answers. With quantum data, each data branch has its own matching positions; a
branch with no matches stays unsuccessful. Input branch probabilities are
preserved, but phases and entanglement can change.

The returned value owns its retained index and reversible preparation workspace.
Workspace is zero after every oracle use and at return; the index remains live.
The index is necessary even for duplicate values. Copies retain correlations.
Moves/returns transfer ownership. Scope cleanup reverses the entire preparation
using captured input versions when legal; measurement or live dependencies can
make cleanup impossible. Such cases report Q3001, never hidden measurement/reset.
Named script results can remain live until shot completion. In particular,
measuring a local search result and then attempting to erase its unobserved index
is deliberately rejected. Reversible updates of its visible post-measurement value
remain supported. Quantum indexing syntax and mixed quantum string lengths are
still deferred.

`check`/`explain` metadata reports the algorithm, oracle calls, retained index and
workspace qubits, and failure target. Indexed access is a linear controlled-copy
network; oracle query complexity does not imply an end-to-end speedup. Resource
budgets fail before execution rather than weakening the target. Simulation limits
are unchanged; larger circuits may compile but require more qubits than allowed
for local simulation.

## Distribution and compatibility

New generated modules import `qutes.artifact_v4`. Existing schema-3 modules keep
their original executable circuits through `qutes.artifact_v3`; changed inputs
respecialize with the current compiler. Modules generated under 0.1 or 0.2
fail with a rebuild instruction before executing or specializing their embedded
source. Rebuild with `qutes build SOURCE.qut`. Existing 0.2 source remains valid
except that `search` is now a reserved builtin name. The Python compilation and
generated build/run interfaces remain available. Both configuration and phase
angles participate in deterministic generation; config participates in build ID.


## Presentation metadata

Named Qiskit registers partition the physical wire order after allocation;
source aliases never allocate extra wires. Search value, retained index and work
retain distinct logical identities but one owner. Shared physical wires use stable
work names; exclusive wires retain source names where their physical order permits. Source mappings record half-open
scheduled-operation ranges and function invocation contexts. Cleanup annotations
distinguish zeroed target wires from temporarily restored dependency wires.
Construction `bind` annotations carry names only, not additional computation.
Artifact 4 explicitly distinguishes logical allocation/source IDs from physical
operation/register IDs. See [wire allocation](wire-allocation.md) for intervals,
proofs, config switches and physical/logical diagram contracts.


Qutes console/image views fold source operations by default. `--unfold N|all`
reveals source and then backend levels; optional `--unfold-only` selects comma-
separated kinds/functions, opening their ancestor paths. Source mappings and
regions are presentation metadata, not gates. Measurement and runtime control
remain visible. Cleanup markers are confined to diagrams; executable gates and
measurement ordering are unchanged. Image names include view hashes; build IDs do
not depend on rendering options. Alphabet warning QW0001 is nonfatal and does not
alter settings. CLI JSON and compilation metadata expose warnings without printing
from the Python compilation API. See the CLI walkthrough for interfaces and limits.
