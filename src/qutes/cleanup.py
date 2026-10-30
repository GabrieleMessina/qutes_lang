"""Version-aware synthesis of reversible cleanup schedules.

Every accepted update has a recorded inverse and versions of its read operands.
Cleanup temporarily restores those versions, applies the inverse, then restores
the current inputs. Temporary restoration may not read the value being erased.
Physical wires remain reserved so a released basis computation can be recomputed.
This module has no Qiskit dependency and never substitutes measurement for cleanup.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from qutes.diagnostics import DiagnosticError, Span
from qutes.gates import Gate, inverse


@dataclass(frozen=True)
class Version:
    storage: int
    number: int


@dataclass(frozen=True)
class Step:
    gates: tuple[Gate, ...]
    dependencies: tuple[Version, ...]


@dataclass
class Storage:
    id: int
    name: str
    bits: tuple[int, ...]
    span: Span
    history: list[Step] = field(default_factory=list)
    version: int = -1  # -1 is the all-zero allocation, before initialization.
    released: bool = False
    root: bool = False
    external: bool = False


@dataclass(frozen=True)
class CleanupEvent:
    storage: int
    name: str
    from_version: int
    operation_start: int
    operation_end: int
    restored_inputs: tuple[Version, ...]
    span: Span


class Scheduler:
    def __init__(self, *, max_steps: int = 100_000):
        self.storages: list[Storage] = []
        self.bit_owner: dict[int, int] = {}
        self.operations: list[Gate] = []
        self.events: list[CleanupEvent] = []
        self.qubit_count = 0
        self.max_steps = max_steps
        self.work = 0
        self.active_moves: set[tuple[int, int]] = set()

    def fail(self, message: str, storage: Storage, code="Q3001"):
        raise DiagnosticError(code, message, storage.span)

    def tick(self, storage: Storage, count=1):
        self.work += count
        if self.work > self.max_steps:
            self.fail("quantum cleanup scheduling budget exceeded", storage, "Q4001")

    def allocate(self, width: int, name: str, span: Span) -> Storage:
        if type(width) is not int or width < 1:
            raise ValueError("storage width must be a positive integer")
        bits = tuple(range(self.qubit_count, self.qubit_count + width))
        self.qubit_count += width
        storage = Storage(len(self.storages), name, bits, span)
        self.storages.append(storage)
        self.bit_owner.update((bit, storage.id) for bit in bits)
        return storage

    def dependencies(self, gates: tuple[Gate, ...], target: Storage, *, auxiliary=False):
        identifiers = set()
        for gate in gates:
            if not gate.bits <= self.bit_owner.keys():
                raise ValueError("operation refers to unallocated bits")
            if not auxiliary and not set(gate.targets) <= set(target.bits):
                raise ValueError("update mutates another storage")
            identifiers.update(self.bit_owner[bit] for bit in gate.bits)
        identifiers.discard(target.id)
        dependencies = []
        for identifier in sorted(identifiers):
            source = self.storages[identifier]
            if not auxiliary and (source.released or source.version < 0):
                self.fail(f"{target.name} reads unavailable value {source.name}", target)
            dependencies.append(Version(identifier, source.version))
        return tuple(dependencies)

    def initialize(self, target: Storage, gates: tuple[Gate, ...], *, external=False):
        if target.history or target.version != -1 or target.released:
            raise ValueError("storage already initialized")
        dependencies = self.dependencies(gates, target)
        target.root = external or any(gate.kind == "h" for gate in gates)
        target.external = external
        if target.root and dependencies:
            self.fail("superposition preparation cannot depend on quantum inputs", target)
        target.history.append(Step(gates, dependencies))
        target.version = 0
        self.emit(gates, target)

    def update(self, target: Storage, gates: tuple[Gate, ...]):
        if target.released or target.version != len(target.history) - 1 or target.version < 0:
            raise ValueError("cannot update unavailable storage")
        if any(gate.kind == "h" for gate in gates):
            self.fail("an update cannot introduce a new superposition", target)
        dependencies = self.dependencies(gates, target)
        target.history.append(Step(gates, dependencies))
        target.version += 1
        self.emit(gates, target)

    def emit(self, gates: tuple[Gate, ...], target: Storage):
        self.tick(target, max(1, len(gates)))
        self.operations.extend(gates)

    def _apply(self, target: Storage, index: int, backwards: bool, forbidden: frozenset[int]):
        step = target.history[index]
        conflicts = {version.storage for version in step.dependencies} & forbidden
        if conflicts:
            conflict = self.storages[min(conflicts)]
            self.fail(f"cannot clean {conflict.name}: restoring {target.name} would read the value being erased", conflict)
        before = tuple(storage.version for storage in self.storages)
        start = len(self.operations)
        for dependency in step.dependencies:
            self._move(self.storages[dependency.storage], dependency.number, forbidden | {target.id})
        restore = inverse(self.operations[start:])
        self.emit(inverse(step.gates) if backwards else step.gates, target)
        target.version = index - 1 if backwards else index
        # The restoration prefix cannot read target (the forbidden set above).
        # Therefore its inverse remains valid after target changes.
        self.emit(restore, target)
        for storage, version in zip(self.storages, before):
            if storage is not target:
                storage.version = version

    def _move(self, target: Storage, version: int, forbidden: frozenset[int]):
        self.tick(target)
        if target.version == version:
            return
        if target.id in forbidden:
            self.fail(f"cleanup has a cyclic version dependency involving {target.name}", target)
        key = (target.id, version)
        if key in self.active_moves:
            self.fail(f"cleanup has a cyclic version dependency involving {target.name}", target)
        if len(self.active_moves) >= 128:
            self.fail("quantum cleanup dependency nesting limit exceeded", target, "Q4001")
        if not -1 <= version < len(target.history):
            raise ValueError("unknown storage version")
        if target.root and target.version == -1:
            self.fail(f"cannot recreate the independent quantum state of {target.name}", target)
        self.active_moves.add(key)
        try:
            while target.version != version:
                backwards = target.version > version
                index = target.version if backwards else target.version + 1
                self._apply(target, index, backwards, forbidden)
        finally:
            self.active_moves.remove(key)

    def _depends_on(self, source: Storage, identifier: int) -> bool:
        pending = [source.id]
        visited = set()
        while pending:
            current = pending.pop()
            if current in visited:
                continue
            visited.add(current)
            for step in self.storages[current].history:
                for dependency in step.dependencies:
                    if dependency.storage == identifier:
                        return True
                    pending.append(dependency.storage)
        return False

    def _root_guard(self, target: Storage):
        if target.external:
            self.fail(f"cannot erase the unknown input state of {target.name}", target)
        if target.root:
            for source in self.storages:
                if source is not target and not source.released and self._depends_on(source, target.id):
                    self.fail(f"cannot clean {target.name}: live value {source.name} still depends on its quantum state", target)

    def release(self, target: Storage):
        if target.released or target.version < 0:
            raise ValueError("storage already released or uninitialized")
        self._root_guard(target)
        before = tuple(storage.version for storage in self.storages)
        start = len(self.operations)
        try:
            self._move(target, -1, frozenset())
        except DiagnosticError:
            del self.operations[start:]
            for storage, version in zip(self.storages, before):
                storage.version = version
            raise
        target.released = True
        touched = {self.bit_owner[bit] for gate in self.operations[start:] for bit in gate.bits}
        touched.discard(target.id)
        self.events.append(CleanupEvent(target.id, target.name, before[target.id], start,
                                        len(self.operations), tuple(Version(i, before[i]) for i in sorted(touched)), target.span))

    def overwrite(self, target: Storage, preparation: tuple[Gate, ...]):
        """Erase a basis-derived old value and initialize its replacement atomically.

        The composite update retains the old recipe so other values may still
        depend on an older version. Independent quantum roots are not overwritable.
        """
        if target.root:
            self.fail(f"cannot overwrite the unknown quantum value of {target.name}; use a reversible update", target)
        if target.released or target.version < 0:
            raise ValueError("cannot overwrite unavailable storage")
        if any(gate.kind == "h" for gate in preparation):
            self.fail("superposition is an initializer, not a reset operation", target)
        self.dependencies(preparation, target)
        before = tuple(storage.version for storage in self.storages)
        start = len(self.operations)
        try:
            self._move(target, -1, frozenset())
            self.emit(preparation, target)
            gates = tuple(self.operations[start:])
        except DiagnosticError:
            del self.operations[start:]
            for storage, version in zip(self.storages, before):
                storage.version = version
            raise
        target.version = before[target.id]
        dependencies = self.dependencies(gates, target, auxiliary=True)
        target.history.append(Step(gates, dependencies))
        target.version += 1

    def release_scope(self, identifiers: set[int]):
        """Prefer reverse allocation order, retrying after dependents are cleaned."""
        pending = sorted((i for i in identifiers if not self.storages[i].released), reverse=True)
        while pending:
            failure = None
            for identifier in pending.copy():
                try:
                    self.release(self.storages[identifier])
                except DiagnosticError as error:
                    if error.code != "Q3001":
                        raise
                    failure = error
                else:
                    pending.remove(identifier)
                    break
            else:
                assert failure is not None
                raise failure
