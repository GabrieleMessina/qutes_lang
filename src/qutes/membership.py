"""Independent sequence matching semantics, without circuit construction."""
from qutes.ir import Type


def is_sequence(type_: Type) -> bool:
    return type_.array or type_.name in {"string", "qustring"}


def pattern_is_element(left: Type, right: Type) -> bool:
    if not is_sequence(right):
        raise ValueError("the right operand of in must be an array or string")
    if left.classical == right.element.classical:
        return True
    if is_sequence(left) and left.element.classical == right.element.classical:
        return False
    raise ValueError("in requires compatible element types")


def element_matches(pattern, value, type_: Type) -> bool:
    if type_.name == "char":
        return pattern == "?" or pattern == value
    if type_.name == "string":
        return len(pattern) == len(value) and all(a == "?" or a == b for a, b in zip(pattern, value))
    return pattern == value


def matches(pattern, values, left: Type, right: Type) -> bool:
    elements = (pattern,) if pattern_is_element(left, right) else pattern
    return any(all(element_matches(p, values[i + j], right.element.classical)
                   for j, p in enumerate(elements))
               for i in range(len(values) - len(elements) + 1))
