# Arrays and text

`Type[]` is a fixed-length array. Use a literal such as `[1, 2, 3]` or allocate with `new quint[3]`. The latter prepares three zero-valued quantum integers. The first element is at index 0 and `values.Length` gives the number of elements.

## Aliases, slices and copies

```qutes
int[] values = [1, 2, 3];
int[] tail = values[1..3];
int[] saved = copy(tail);
tail[0] = 7;
return [values[1], saved[0]];
```

This returns `[7, 2]`. The slice includes index 1 and excludes index 3. It shares its backing storage, so changing `tail[0]` changes `values[1]`. The separate array returned by `copy` keeps the old value. Returning an array from a function also shares its reference. Assigning a new array to a name rebinds that name while existing aliases keep their allocation.

A `readonly` binding prevents rebinding or writing through that name. Another mutable alias can still change the underlying elements. Copying a quantum array creates correlated basis values; measuring a copy can affect the joint state.

## Indexing in superposition

`values[index]` can read coherently with a `quint` index when the compiler can prove every possible index is in bounds. For three elements, `superposition([0, 2])` is a valid index preparation. A uniform signed integer can include negative indices. Use a known index when writing an element. Reading with a quantum index preserves correlations with the index and does not perform a search.

## Text and membership

Strings support `.Length`, indexing and iteration. A string assignment has value semantics. Slicing a string yields a read-only character view. Quantum text uses the project alphabet and capacity.

```qutes
qustring word = "AB";
qubit matches = "A?" in word;
return measure(matches);
```

This returns `true`. In a pattern on the left of `in`, `?` matches one character. An ordinary classical pattern can use it with the default alphabet. A scalar checks membership of one element; a sequence checks for a contiguous run. An empty sequence matches any sequence. For an array of strings, `"AB" in words` tests for a whole entry.

Classical operands yield `bool` and a quantum operand yields `qubit`. To amplify a matching element and obtain a candidate, use [search](search.md).
