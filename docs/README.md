# Qutes language reference

[Run your first program](reference/getting-started.md) in the browser, in VS Code or with the portable compiler. For a guided course with editable experiments, open the [quantum programming tutorial](https://qutes-lang.web.app/tutorial.html).

## Writing Qutes

- [Types and expressions](reference/types.md) — declarations, numeric widths, operators and comparisons.
- [Arrays and text](reference/collections.md) — indexing, slices, aliases, copies and pattern matching.
- [Functions and control flow](reference/control-flow.md) — parameters, mutation, coherent controls, measured conditions and loops.
- [Assignment, cleanup and wire reuse](reference/cleanup.md) — temporary storage and the difference between logical values and physical wires.

## Gates and built-ins

- [Gates](reference/gates.md) — hadamard, not, phaseFlip, phase and swap.
- [Preparation and value operations](reference/builtins.md) — superposition, complex, rotateLeft, rotateRight and copy.
- [Measuring a quantum value](reference/measurement.md) — measure, decoded results and post-measurement state.
- [Searching a collection](reference/search.md) — search, oracle requirements and success probability.

## Tools

- [Editing and debugging](reference/editors.md) — playground and VS Code controls, breakpoints and state inspection.
- [Command-line reference](reference/cli.md) — check, run, build, explain, parse, analyze and construct.
- [Inputs and configuration](reference/configuration.md) — JSON inputs, project settings, encodings and resource limits.
- [Qiskit and Python](reference/python.md) — standalone circuits, generated modules and the source API.
- [Diagnostics](reference/diagnostics.md) — compiler codes and examples of how to resolve them.

## Specification history

The [specifications on GitHub](https://github.com/GabrieleMessina/qutes_lang/tree/qutes2.0/docs/spec) record the language design across revisions, including the older version-numbered contracts and the compiler’s lowering and wire-allocation rules.
