"""Immutable Boolean circuits over recorded measurement bits, without Qiskit."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Predicate:
    op: str
    arguments: tuple[Predicate, ...] = ()
    value: bool | int | None = None

    def __post_init__(self):
        arity = {"literal": 0, "bit": 0, "not": 1, "and": 2, "or": 2, "xor": 2}
        if self.op not in arity or len(self.arguments) != arity[self.op]:
            raise ValueError("invalid classical predicate operation")
        if self.op == "literal" and type(self.value) is not bool:
            raise ValueError("predicate literal requires a Boolean")
        if self.op == "bit" and (type(self.value) is not int or self.value < 0):
            raise ValueError("predicate bit requires a nonnegative identifier")

    def nodes(self):
        """Postorder traversal; shared expressions are visited once."""
        visited = set()
        pending = [(self, False)]
        while pending:
            node, ready = pending.pop()
            if id(node) in visited:
                continue
            if ready:
                visited.add(id(node))
                yield node
            else:
                pending.append((node, True))
                pending.extend((argument, False) for argument in reversed(node.arguments))

    @property
    def bits(self):
        return frozenset(node.value for node in self.nodes() if node.op == "bit")

    def evaluate(self, memory: int) -> bool:
        values = {}
        for node in self.nodes():
            arguments = [values[id(argument)] for argument in node.arguments]
            if node.op == "literal": value = node.value
            elif node.op == "bit": value = bool((memory >> node.value) & 1)
            elif node.op == "not": value = not arguments[0]
            elif node.op == "and": value = arguments[0] and arguments[1]
            elif node.op == "or": value = arguments[0] or arguments[1]
            else: value = arguments[0] != arguments[1]
            values[id(node)] = value
        return values[id(self)]


FALSE = Predicate("literal", value=False)
TRUE = Predicate("literal", value=True)


def literal(value: bool) -> Predicate:
    if type(value) is not bool:
        raise ValueError("predicate literal requires a Boolean")
    return TRUE if value else FALSE


def invert(value: Predicate) -> Predicate:
    if value.op == "literal":
        return literal(not value.value)
    if value.op == "not":
        return value.arguments[0]
    return Predicate("not", (value,))


def combine(op: str, a: Predicate, b: Predicate) -> Predicate:
    if a == b:
        return FALSE if op == "xor" else a
    if a.op == "literal":
        if op == "and": return b if a.value else FALSE
        if op == "or": return TRUE if a.value else b
        if op == "xor": return invert(b) if a.value else b
    if b.op == "literal":
        return combine(op, b, a)
    return Predicate(op, (a, b))


def all_of(values) -> Predicate:
    values = list(values)
    while len(values) > 1:
        values = [combine("and", values[i], values[i + 1]) if i + 1 < len(values) else values[i]
                  for i in range(0, len(values), 2)]
    return values[0] if values else TRUE


def compare(a: tuple[Predicate, ...], b: tuple[Predicate, ...], op: str, *, signed=False) -> Predicate:
    """Balanced bit comparator, least-significant bits first; no unsigned cast."""
    if len(a) != len(b) or not a:
        raise ValueError("comparison requires equally sized nonempty bit lists")
    if op in {"==", "!="}:
        equal = all_of(invert(combine("xor", x, y)) for x, y in zip(a, b))
        return invert(equal) if op == "!=" else equal
    if op in {">", "<="}:
        a, b = b, a
    if signed:
        a, b = (*a[:-1], invert(a[-1])), (*b[:-1], invert(b[-1]))
    pairs = [(invert(combine("xor", x, y)), combine("and", invert(x), y)) for x, y in zip(a, b)]
    while len(pairs) > 1:
        merged = []
        for index in range(0, len(pairs), 2):
            if index + 1 == len(pairs):
                merged.append(pairs[index])
                continue
            low, high = pairs[index:index + 2]
            merged.append((combine("and", low[0], high[0]),
                           combine("or", high[1], combine("and", high[0], low[1]))))
        pairs = merged
    less = pairs[0][1]
    return invert(less) if op in {"<=", ">="} else less
