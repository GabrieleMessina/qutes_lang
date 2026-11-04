"""Aer execution and ordered result decoding, separate from source compilation."""

from dataclasses import dataclass

from qutes import ir
from qutes.config import CompilerConfig
from qutes.diagnostics import DiagnosticError, Position, Span
from qutes.lowering import Result
from qutes.serialization import json_text


@dataclass(frozen=True)
class ResultLayout:
    result: Result
    metadata: dict

    def decode(self, memory: int):
        return self.result.decode(memory)

    def to_dict(self):
        return ir.to_dict(self.result)


def result_from_data(data):
    return Result(ir.Type(**data["type"]), data["op"],
                  tuple(result_from_data(argument) for argument in data.get("arguments", ())),
                  data.get("value"), tuple(data.get("bits", ())), data.get("alphabet"),
                  data.get("length"), data.get("capacity"))


def __getattr__(name):
    if name == "layout_from_metadata":
        # Old generated modules import this at module load, before choosing their
        # cached circuit OR recompiling embedded 0.1 source with new bindings.
        raise ImportError("Qutes 0.1 generated module is incompatible with Qutes 0.3. "
                          "Migrate the source to top-level statements and rebuild it with 'qutes build'.")
    raise AttributeError(name)


def fail(layout, code, message):
    point = Position(0, 1, 1)
    raise DiagnosticError(code, message, Span(layout.metadata.get("source_path", "<runtime>"), point, point))


def checked_build(factory, layout):
    try:
        return factory(), layout
    except ImportError as error:
        fail(layout, "Q5001", f"Qiskit is unavailable; install qutes-lang[backend]: {error}")
    except DiagnosticError:
        raise
    except Exception as error:
        fail(layout, "Q5002", f"circuit construction failed: {error}")


def execute(build_circuit, layout: ResultLayout, *, shots=1024, seed=None):
    """Preflight before importing/allocating a simulator; aggregate decoded shots."""
    config = CompilerConfig.resolve(layout.metadata["config"])
    if type(shots) is not int or not 1 <= shots <= config.max_simulation_shots:
        fail(layout, "Q4001", f"shots must be between 1 and {config.max_simulation_shots}")
    if seed is not None and (type(seed) is not int or not 0 <= seed < 2**32):
        fail(layout, "Q4001", "seed must be an integer in 0..4294967295")
    resources = layout.metadata["resources"]
    if resources["allocated_qubits"] > config.max_simulation_qubits:
        fail(layout, "Q4001", f"circuit needs {resources['allocated_qubits']} qubits; simulation limit is {config.max_simulation_qubits}")
    if not resources["measurement_bits"]:
        outcomes = [{"value": layout.decode(0), "count": shots, "probability": 1.0}]
        backend = "classical-output"
        versions = {}
    else:
        try:
            from qiskit import transpile
            from qiskit_aer import AerSimulator
        except ImportError as error:
            fail(layout, "Q5001", f"Qiskit/Aer is unavailable; install qutes-lang[backend]: {error}")
        try:
            circuit = build_circuit()
            simulator = AerSimulator(method="statevector", max_parallel_threads=1)
            compiled = transpile(circuit, simulator, optimization_level=0, seed_transpiler=seed)
            if compiled.num_qubits > config.max_simulation_qubits:
                fail(layout, "Q4001", f"transpiled circuit needs {compiled.num_qubits} qubits; simulation limit is {config.max_simulation_qubits}")
            result = simulator.run(compiled, shots=shots, seed_simulator=seed).result()
            if not result.success:
                fail(layout, "Q5002", f"simulation failed: {result.status}")
            combined = {}
            for memory, count in result.get_counts().items():
                value = layout.decode(int(memory.replace(" ", ""), 2))
                key = json_text(value)
                if key not in combined:
                    combined[key] = {"value": value, "count": 0}
                combined[key]["count"] += count
            outcomes = [{**combined[key], "probability": combined[key]["count"] / shots} for key in sorted(combined)]
            backend = "qiskit-aer/statevector"
            from qutes.compiler import dependency_versions
            versions = dependency_versions()
        except DiagnosticError:
            raise
        except Exception as error:
            fail(layout, "Q5002", f"backend execution failed: {error}")
    return {"outcomes": outcomes, "execution": {"shots": shots, "seed": seed, "backend": backend,
                                                "dependency_versions": versions}, "build": layout.metadata}
