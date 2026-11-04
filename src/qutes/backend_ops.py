"""Shared reversible expansion for Qiskit execution, Python emission, and costs."""

from dataclasses import dataclass

from qutes.gates import Gate


@dataclass(frozen=True)
class Application:
    kind: str
    targets: tuple[int, ...]
    inputs: tuple[int, ...] = ()
    controls: tuple[tuple[int, bool], ...] = ()
    inverse: bool = False
    angle: float = 0.0

    @property
    def qubits(self):
        return tuple(bit for bit, _ in self.controls) + self.inputs + self.targets

    @property
    def control_state(self):
        return sum(int(value) << i for i, (_, value) in enumerate(self.controls))


def applications(operation: Gate):
    def application(kind, targets, extra=()):
        controls = dict(operation.controls)
        for bit in extra:
            if bit in controls and not controls[bit]:
                return
            controls[bit] = True
        yield Application(kind, tuple(targets), controls=tuple(controls.items()),
                          angle=-operation.angle if operation.inverse else operation.angle)

    def constant(amount, extra=()):
        amount %= 1 << len(operation.targets)
        for offset in range(len(operation.targets)):
            if (amount >> offset) & 1:
                for index in reversed(range(offset + 1, len(operation.targets))):
                    yield from application("x", (operation.targets[index],), (*extra, *operation.targets[offset:index]))
                yield from application("x", (operation.targets[offset],), extra)

    if operation.kind in {"x", "h", "ry", "phase"}:
        for target in operation.targets:
            yield from application(operation.kind, (target,))
    elif operation.kind == "copy":
        for source, target in zip(operation.inputs, operation.targets, strict=True):
            yield from application("x", (target,), (source,))
    elif operation.kind == "add_constant":
        yield from constant(-operation.amount if operation.inverse else operation.amount)
    elif operation.kind == "add":
        if {bit for bit, _ in operation.controls} & set(operation.inputs):
            for index, source in enumerate(operation.inputs):
                yield from constant(-(1 << index) if operation.inverse else 1 << index, (source,))
        else:
            yield Application("add", operation.targets, operation.inputs, operation.controls, operation.inverse)
    elif operation.kind == "rotate":
        count = (-operation.amount if operation.inverse else operation.amount) % len(operation.targets)
        for _ in range(count):
            for index in range(1, len(operation.targets)):
                yield from application("swap", (operation.targets[0], operation.targets[index]))
    else:
        raise ValueError(f"unsupported operation {operation.kind}")
