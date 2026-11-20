# Qutes 0.4 delivery audit

Contract: [language0.4](spec/language-v0.4.md). Detailed evidence and final status:
[VALIDATION](knowledge/VALIDATION.md), [STATUS](knowledge/STATUS.md). This is an
implementation/automated validation record, not independent human review.

| Approved scope | Implementation and evidence |
| --- | --- |
| Arrays, aliases, views, copy, mutable parameters and readonly | Cells/owners/views in construction; concrete borrow regions; full backing retention; test_v04_references.py |
| Float/complex, inputs/outputs and widening | Finite binary64 numeric module, JSON/Python codec; test_v04_types.py and test_v04_delivery.py |
| Readable live operations and coherent/feedforward control | Atomic unitary histories, backend-neutral gates and Qiskit lowering; test_v04_operations.py |
| Bell, teleportation, QFT and inverse circuits | Independent complete state/operator/DFT comparisons and external-reference correlations |
| Explicit finite preparation | Sparse prefix rotations, leaf phases, exact X for forced bits; reversible preparation records; test_v04_preparation.py |
| Signed subtraction/negation | Inverse modular addition/two's complement; exhaustive small-width and complex-state checks |
| Coherent indexed reads | Bounded finite-set/interval proofs and controlled access; all supported collections, aliases, tiny amplitudes, joins and cleanup; test_v04_indexing.py |
| Indexed foreach/ranges/slices | Static expansion, readonly loop bindings, mutable/read-only views, bounds and retained allocation tests |
| Generated compatibility | Schema5; cached3/4 execution and rejection before changed-input compilation; test_v04_delivery.py |
| Diagrams and physical reuse | Console/SVG/PNG, compact/unfolded phase-bearing circuits, unchanged execution, zero certificates and reuse comparisons |
| Migration and examples | Explicit copy where old examples intended copying; 50 tour files, all <=24 qubits; snapshots/user images preserved |
| Distribution | Windows/Linux suites, parser reproduction, 26 walkthrough commands, isolated wheel and core-only checks in V030 |

Conservative boundaries remain intentional. Bounds proofs may lose precision after
the finite-set cap. Cleanup cannot replay through incompatible live unitary effects;
only closed private components qualify for joint inversion. Measured or externally
dependent local states may therefore require restructuring. No hidden reset or
measurement substitutes for a proof. Quantum arrays use basis-value copies, never
general state cloning. Ranges/slice bounds remain construction-time values.

Old schema3/4 modules use an unversioned compiler import, so their adapter checks
the immediate published _binding(inputs) frame before that fallback can execute.
This bounded compatibility mechanism neither patches globals nor changes plain
Python compilation calls. Review old array assignments and rebuild to change inputs.

No hardware testing, hosted CI run, Python3.12 execution or general quantum speedup
is claimed. Existing Python3.13.5 Windows/Debian environments use pinned ANTLR4.13.2,
Qiskit2.3.0, Aer0.17.2 and NumPy2.1.3. See V030 for exact commands/results/limits.
