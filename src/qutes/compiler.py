"""Public source compilation API; no Qiskit import or execution on compilation."""

from dataclasses import dataclass
import hashlib
import importlib.metadata

from qutes import __version__, ir
from qutes.backend_ops import applications
from qutes.checker import analyze
from qutes.config import CompilerConfig
from qutes.construction import construct
from qutes.diagnostics import DiagnosticError
from qutes.gates import Measurement
from qutes.lowering import Program, lower
from qutes.parser import parse
from qutes.serialization import json_text

LANGUAGE_VERSION = "0.2"
ARTIFACT_VERSION = 2


def dependency_versions():
    versions = {}
    for name in ("antlr4-python3-runtime", "qiskit", "qiskit-aer", "numpy"):
        try:
            versions[name] = importlib.metadata.version(name)
        except importlib.metadata.PackageNotFoundError:
            versions[name] = None
    return versions


def resources(program: Program, span):
    counts = {"gate_applications": 0, "library_adders": 0, "operand_references": 0,
              "measurement_bits": 0, "max_quantum_controls": 0, "classical_guarded_operations": 0,
              "classical_expression_nodes": 0}
    for operation in program.operations:
        if isinstance(operation, Measurement):
            counts["measurement_bits"] += len(operation.qubits)
            continue
        counts["classical_guarded_operations"] += bool(operation.classical_controls or operation.conditions)
        pending = [condition for condition, _ in operation.conditions]
        while pending:
            condition = pending.pop()
            counts["classical_expression_nodes"] += 1
            if counts["classical_expression_nodes"] > program.config.max_evaluation_steps:
                raise DiagnosticError("Q4001", "classical condition expansion exceeds the construction budget", operation.span or span)
            pending.extend(condition.arguments)
        for application in applications(operation):
            counts["gate_applications"] += 1
            counts["library_adders"] += application.kind == "add"
            counts["operand_references"] += len(application.qubits)
            counts["max_quantum_controls"] = max(counts["max_quantum_controls"], len(application.controls))
            if counts["operand_references"] > program.config.max_evaluation_steps:
                raise DiagnosticError("Q4001", "backend expansion exceeds the construction budget", operation.span or span)
    return {**counts, "allocated_qubits": program.qubit_count,
            "search_oracle_calls": sum(item["oracle_calls"] for item in program.searches),
            "retained_search_index_qubits": sum(len(item.retained_index_bits) for item in program.allocations if not item.released),
            "search_workspace_qubits": sum(len(item.scratch_bits) for item in program.allocations),
            "classical_bits": program.classical_bit_count,
            "scheduled_operations": len(program.operations),
            "cleanup_events": len(program.cleanup_events),
            "cleaned_qubits_at_end": sum(len(item.bits) for item in program.allocations if item.released),
            "wire_reuse": False,
            "simulation_limit_qubits": program.config.max_simulation_qubits,
            "simulation_within_limit": program.qubit_count <= program.config.max_simulation_qubits,
            "statevector_bytes": 1 << (program.qubit_count + 4) if program.qubit_count <= 60 else None,
            "statevector_bytes_power_of_two": program.qubit_count + 4,
            "estimate_scope": "scheduled gates and library adders, before device decomposition"}


@dataclass(frozen=True)
class Compilation:
    source: str
    source_path: str
    inputs: dict
    program: Program
    metadata: dict

    def build(self):
        from qutes.runtime import ResultLayout, checked_build
        return checked_build(self.program.to_qiskit, ResultLayout(self.program.result, self.metadata))

    def run(self, *, shots=1024, seed=None):
        from qutes.runtime import ResultLayout, execute
        return execute(self.program.to_qiskit, ResultLayout(self.program.result, self.metadata), shots=shots, seed=seed)


def compile_source(source: str, *, path="<input>", inputs=None, config=None) -> Compilation:
    config = config or CompilerConfig()
    try:
        syntax = parse(source, path)
        constructed = construct(analyze(syntax, config), inputs)
        program = lower(constructed)
    except DiagnosticError as error:
        for item in error.diagnostics:
            item.source = source
        raise
    source_hash = hashlib.sha256(source.encode("utf-8")).hexdigest()
    identity = {"source_sha256": source_hash, "config": config.to_dict(), "inputs": constructed.inputs,
                "compiler_version": __version__, "language_version": LANGUAGE_VERSION}
    metadata = {**identity, "artifact_schema": ARTIFACT_VERSION, "source_path": path,
                "build_sha256": hashlib.sha256(json_text(identity).encode("utf-8")).hexdigest(),
                "dependency_versions": dependency_versions(), "result_layout": ir.to_dict(program.result),
                "resources": resources(program, syntax.span),
                "searches": list(program.searches),
                "allocations": ir.to_dict(program.allocations), "cleanup": ir.to_dict(program.cleanup_events),
                "construction": {"evaluation_steps": constructed.evaluation_steps,
                                 "loop_iterations": constructed.loop_iterations}}
    return Compilation(source, path, constructed.inputs, program, metadata)
