# Two measurements, one prediction

**20 minutes.** A learner who can read a conditional can do this experiment. Open Bell pair in the browser or run the [canonical program](../../examples/language/41_bell_gates.qut) locally.

1. **Predict (3 min).** Alice and Bob start false. Hadamard gives Alice two possible measurement outcomes. The conditional flips Bob coherently when Alice is true. Write down the pairs you expect.
2. **Run (4 min).** Run 64 shots. You should see only [false,false] and [true,true]. Each has ideal probability one half. Counts can differ.
3. **Edit (5 min).** Insert `not(bob);` directly before the return. Predict the outcomes before running again. Explain which line changed the relationship.
4. **Discuss (5 min).** Can a single result tell you whether the bits agree on every shot? Which measurement would tell you about relative phase? Computational-basis counts alone do not establish coherence. Remove the edit, undo the entangling operation with the same conditional flip and a Hadamard on Alice, and predict the all-false output.
5. **Reflect (3 min).** Compare conditional quantum control with recording a measurement. Where does this program first obtain classical information?

**Instructor notes.** The single flip produces only [false,true] and [true,false]. A roughly even split is expected over many shots. Undoing the preparation tests interference. Finish with the [wire-reuse example](../../examples/language/39_wire_reuse.qut) to show how scoped temporaries become reusable wires.
