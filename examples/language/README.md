# Qutes language tour

These 38 small programs cover the operations implemented in Qutes 0.3. Each file
is independent. All have been executed with the supplied configuration and the
24-qubit simulator limit; the largest currently uses **21 qubits**. Counts include
reserved work qubits, even after cleanup. Classical-only programs use zero qubits.

## Run an example

From the repository root in Windows PowerShell:

```powershell
.\.venv\Scripts\python.exe tools/qutes.py run examples/language/10_quantum_addition.qut --shots 64 --seed 17
.\.venv\Scripts\python.exe tools/qutes.py run examples/language/07_inputs.qut --inputs examples/language/07_inputs.json
.\.venv\Scripts\python.exe tools/qutes.py explain examples/language/33_search_strings.qut
.\.venv\Scripts\python.exe tools/qutes.py check examples/language/33_search_strings.qut --print-circuit
```

On Linux replace `.\.venv\Scripts\python.exe` with `.venv/bin/python` (or the
Python executable for your project environment). An installed `qutes` command
also works. Add `--save-circuit artifacts/tour-circuits --circuit-format svg` to
`check`, `build`, `run` or `explain` to save a diagram; image export needs the
visualization extra. `build FILE -o artifacts/example.qiskit.py` generates Python.

The CLI automatically reads the adjacent [qutes.toml](qutes.toml). No overrides or
raised qubit limit are necessary. It fixes:

- Three-bit signed `quint`, ranging from **-4 to 3**, with wraparound addition.
- Quantum alphabet **AB?**, two qubits per character, and text capacity **2**.
- Simulator limit **24** and search failure bound **0.01**.

These settings are specific to the tour. The compiler's current defaults are
four-bit `quint` and alphabet `ABC`. Classical text is not restricted to either
quantum alphabet. Changing widths, capacity, or alphabet can increase circuit size
and change numerical results. The Python compilation API needs an explicit
`CompilerConfig.load("examples/language/qutes.toml")`; it does not discover config.

## Examples and expected results

Array positions in the results follow the order of each file's `return` expression.
Alternatives separated by **or** are possible results of different shots, not a
promise to see every alternative in a small run. Search results are probabilistic:
the listed matches have at least 99% total probability under ideal execution when
a match exists; occasional nonmatches are allowed. No-match search returns an
ordinary candidate that can be checked with the oracle.

### Classical values and program structure

| Example | Operations | Qubits | Expected result |
| --- | --- | ---: | --- |
| [01_classical_arithmetic.qut](01_classical_arithmetic.qut) | int, +, -, unary +, unary -, *, /, %, =, +=, -=, ++, -- | 0 | `[8, 8, -8, 14, 20, 5, -2, -1]` |
| [02_classical_logic.qut](02_classical_logic.qut) | bool, !, &&, &#124;&#124;, ==, !=, <, <=, >, >= | 0 | `[true, true, true, true, true, true, true, true, false]` |
| [03_classical_arrays.qut](03_classical_arrays.qut) | array literals, new, indexing, indexed assignment, .Length, array assignment | 0 | `[1, 3, 3, 4, 3]` |
| [04_classical_text.qut](04_classical_text.qut) | char, string, text indexing, text equality, escapes | 0 | All 5 results are `true` |
| [05_control_flow.qut](05_control_flow.qut) | if, else if, else, while, for, foreach, block scope | 0 | `11` |
| [06_functions_globals.qut](06_functions_globals.qut) | functions, void, return, globals, forward calls, main | 0 | `6` |
| [07_inputs.qut](07_inputs.qut) | input, classical scalar inputs, classical array inputs | 0 | All 6 results are `true` |

### Quantum values, arithmetic and control

| Example | Operations | Qubits | Expected result |
| --- | --- | ---: | --- |
| [08_qubit_snapshots.qut](08_qubit_snapshots.qut) | qubit, superposition(), quantum value copy, measure(), post-measurement evolution | 2 | `[false, false, true]` or `[true, true, false]` |
| [09_quint_superposition.qut](09_quint_superposition.qut) | quint, superposition(), signed wraparound, post-measurement addition | 3 | `[sample, sample + 2]`, wrapping into -4..3 |
| [10_quantum_addition.qut](10_quantum_addition.qut) | quantum +, quantum +=, negative constant addition | 9 | `[3, 1, 3]` |
| [11_bit_rotations.qut](11_bit_rotations.qut) | rotateLeft(), rotateRight() | 3 | `[2, 1]` |
| [12_quantum_ordering.qut](12_quantum_ordering.qut) | quantum <, quantum <=, quantum >, quantum >= | 19 | `[true, true, false, true]` |
| [13_quantum_equality.qut](13_quantum_equality.qut) | quantum ==, quantum != | 11 | All 2 results are `true` |
| [14_quantum_logic.qut](14_quantum_logic.qut) | quantum !, quantum &&, quantum &#124;&#124;, qubit equality | 9 | `[true, false, true, false, true]` or `[false, true, true, true, false]` |
| [15_coherent_if.qut](15_coherent_if.qut) | quantum if, quantum else | 4 | `-1` or `1` |
| [16_measurement_feedforward.qut](16_measurement_feedforward.qut) | runtime comparisons, runtime Boolean logic, measurement feedforward | 4 | `1` or `2` |

### Quantum collections, functions and cleanup

| Example | Operations | Qubits | Expected result |
| --- | --- | ---: | --- |
| [17_quantum_integer_arrays.qut](17_quantum_integer_arrays.qut) | quint[], new quantum array, quantum indexed update, quantum foreach, quantum array copy | 15 | `[2, 1, 3]` |
| [18_quantum_boolean_arrays.qut](18_quantum_boolean_arrays.qut) | qubit[], quantum array assignment, whole-array measurement | 5 | `[false, true]` or `[true, false]` |
| [19_quantum_text.qut](19_quantum_text.qut) | quchar, qustring, quantum text ==, quantum text !=, text snapshots | 21 | All 5 results are `true` |
| [20_quantum_text_iteration.qut](20_quantum_text_iteration.qut) | qustring foreach, quchar comparisons | 11 | `true` |
| [21_quantum_character_arrays.qut](21_quantum_character_arrays.qut) | quchar[], character indexed assignment | 4 | `["B", "B"]` |
| [22_quantum_string_arrays.qut](22_quantum_string_arrays.qut) | qustring[], string element replacement | 8 | `["A?", "B"]` |
| [23_automatic_cleanup.qut](23_automatic_cleanup.qut) | automatic uncomputation, versioned cleanup | 9 | `[0, 2]` |
| [24_quantum_functions.qut](24_quantum_functions.qut) | quantum function return, readonly parameter | 9 | `[0, 2]` |
| [25_measurement_helpers.qut](25_measurement_helpers.qut) | measurement helper | 3 | `[1, 2]` |

### Membership and patterns

| Example | Operations | Qubits | Expected result |
| --- | --- | ---: | --- |
| [26_classical_membership.qut](26_classical_membership.qut) | scalar in array, sequence in array, char in string, string in string, string/char[] matching, string in string[], string[] in string[], wildcards, empty patterns | 0 | `false` at positions 3, 8, 13, 14; all others `true` |
| [27_quantum_numeric_membership.qut](27_quantum_numeric_membership.qut) | quantum scalar in classical array | 12 | `[false, false]` or `[true, true]` |
| [28_quantum_sequence_membership.qut](28_quantum_sequence_membership.qut) | quantum sequence in quantum array, overlapping membership | 17 | `[false, false]` or `[true, true]` |
| [29_text_membership.qut](29_text_membership.qut) | classical pattern in quantum string | 7 | `true` |
| [30_quantum_wildcards.qut](30_quantum_wildcards.qut) | quantum wildcard pattern | 10 | `[false, false]` or `[true, true]` |
| [31_quantum_text_pattern.qut](31_quantum_text_pattern.qut) | quantum string in classical string[] | 19 | `true` |

### Automatic search

| Example | Operations | Qubits | Expected result |
| --- | --- | ---: | --- |
| [32_search_numbers.qut](32_search_numbers.qut) | search(), numeric oracle, non-power-of-two search, duplicates | 12 | Usually `1`; a nonmatch is possible |
| [33_search_strings.qut](33_search_strings.qut) | string search, membership oracle | 13 | Usually `"AB"` or `"BB"`; a nonmatch is possible |
| [34_search_characters.qut](34_search_characters.qut) | character search | 9 | Usually `"B"`; a nonmatch is possible |
| [35_search_quantum_collection.qut](35_search_quantum_collection.qut) | Boolean search, quantum collection search | 7 | Usually `true`; a nonmatch is possible |
| [36_search_no_matches.qut](36_search_no_matches.qut) | no-match search, checking a search result | 16 | `false` |

### Scripts and text assignment

| Example | Operations | Qubits | Expected result |
| --- | --- | ---: | --- |
| [37_library_only.qut](37_library_only.qut) | function-only scripts, no implicit output | 0 | No returned value; `main` is not called |
| [38_text_assignment.qut](38_text_assignment.qut) | whole-string assignment, logical length changes, immutable text snapshots | 4 | `["A?", "B"]` |

## Important distinctions

- `superposition()` initializes a `qubit` or `quint`; there is no text/array
  superposition initializer in this release. Arrays can contain quantum values.
- Quantum integers support addition, signed comparisons and bit rotations.
  Quantum subtraction via `-`, multiplication/division/remainder, `++`/`--`, and
  zero-filling `<<`/`>>` shifts are not implemented. Add a negative constant when
  you need constant subtraction.
- `in` computes a match flag without amplification. `search(collection, oracle)`
  amplifies matching collection entries and returns a quantum selected value.
  The oracle takes one element and returns `qubit`. Search does not enumerate
  every match or generate every possible text.
- Strings support indexing, `.Length`, `foreach` and sequence matching. Use
  `quchar[]` for indexed character updates; whole strings can be replaced.
  String and character-array types are not interchangeable in assignments.
- Loop bounds and indices must be known during circuit construction. A quantum
  condition controls an `if`; it does not make a quantum-dependent loop valid.
- Functions have readonly parameters, can access script globals, and may measure
  outside conditional bodies. Search oracles must remain pure. `main` executes
  only when called; script output requires an explicit `return`.
- Measurement leaves a value available in its post-measurement state. Classical
  snapshots retain their earlier values. Measurement is not allowed inside
  conditional bodies, including through helpers.
- Search retains selection state internally. Keep measured search results at
  script scope as shown; measuring a local result can make its cleanup impossible.

## Verification

[catalog.json](catalog.json) records feature coverage, inputs, allowed outputs and
preferred search matches. [The regression check](../../tests/test_language_examples.py)
executes every listed file at 64 shots with seed 17 and enforces the 24-qubit limit,
including the backend's post-transpilation check. To rerun it:

```powershell
.\.venv\Scripts\python.exe tools/check.py -q tests/test_language_examples.py
```

The examples complement the [language contract](../../docs/spec/language-v0.3.md).
They deliberately demonstrate supported operations rather than programs that fail.
