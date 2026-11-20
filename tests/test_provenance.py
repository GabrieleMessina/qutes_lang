from pathlib import Path

import pytest

from qutes.compiler import compile_source
from qutes.codegen import python_source
from qutes.config import CompilerConfig
from qutes.provenance import cleanup_annotations


def compile(source):
    return compile_source(source, config=CompilerConfig(quint_bits=3, alphabet="AB"))


@pytest.mark.backend
def test_named_registers_generated_parity_and_snapshots():
    c = compile('quint number=1; int before=measure(number); number+=1; return [before,measure(number)];')
    circuit, _ = c.build()
    assert [r.name for r in circuit.qregs] == ["number"]
    assert circuit.cregs[0].name == "before"
    namespace = {"__name__": "generated"}
    exec(python_source(c), namespace)
    assert namespace["build"]()[0] == circuit
    assert namespace["run"](shots=8, seed=1)["outcomes"][0]["value"] == [1, 2]


def test_calls_aliases_returns_and_shadowed_names():
    c = compile('''quint next(quint value) { quint number=value+1; return number; }
quint number=0; quint a=next(number); quint b=next(number); return measure(b);''')
    mappings = c.program.source_mappings
    aliases = [m for m in mappings if m.name == "value"]
    assert len(aliases) == 2 and aliases[0].bits == aliases[1].bits == (0, 1, 2)
    assert aliases[0].context != aliases[1].context
    a = next(m for m in mappings if m.name == "a")
    assert any(m.name == "number" and m.bits == a.bits and m.context for m in mappings)
    names = [r.name for r in c.program.registers]
    assert len(names) == len(set(names))
    assert len([r for r in c.program.regions if r.kind == "function" and r.label == "next"]) == 2
    assert all(0 <= m.operation_start <= m.operation_end <= len(c.program.operations) for m in mappings)


def test_array_reordering_and_foreach_views():
    c = compile('quint[] values=[0,1]; values=[values[1],values[0]]; foreach(quint element in values) { quint copy=element+1; } return measure(values);')
    mappings = [m for m in c.program.source_mappings if m.name == "values[0]"]
    assert [m.bits for m in mappings] == [(0, 1, 2), (6, 7, 8)]
    assert mappings[0].operation_end == mappings[1].operation_start
    assert [m.bits for m in c.program.source_mappings if m.name == "element"] == [(6, 7, 8), (9, 10, 11)]


@pytest.mark.backend
def test_search_storage_partition_and_classical_name_collision():
    c = compile('qubit accepts(quint n) { return n==1; } quint chosen=search([0,1],accepts); int chosen_index=measure(chosen); return chosen_index;')
    circuit, _ = c.build()
    names = [r.name for r in circuit.qregs]
    assert [r.name for r in c.program.logical_program.registers if not r.classical][:3] == ["chosen", "chosen_index", "chosen_work"]
    assert circuit.cregs[0].name == "chosen_index_2"
    assert sum(r.size for r in circuit.qregs) == c.program.qubit_count


def test_comparison_cleanup_ranges_and_preserved_resources():
    p = Path("examples/language/12_quantum_ordering.qut")
    c = compile_source(p.read_text(), config=CompilerConfig.load(p.parent / "qutes.toml"))
    assert c.program.logical_program.qubit_count == 19
    assert c.program.qubit_count == 10
    assert c.metadata["resources"]["gate_applications"] == 51
    assert len([r for r in c.program.regions if r.kind == "compare"]) == 4
    assert len(cleanup_annotations(c.program)) == 8
    for region in c.program.regions:
        if region.parent is not None:
            parent = c.program.regions[region.parent]
            assert parent.operation_start <= region.operation_start <= region.operation_end <= parent.operation_end
    for annotation in cleanup_annotations(c.program):
        assert not set(annotation["zero_bits"]) & set(annotation["restored_bits"])


def test_membership_provenance_survives_expression_expansion():
    c = compile('qustring text="AB"; return measure("A?" in text);')
    assert any(r.kind == "membership" for r in c.program.regions)


def test_classical_snapshot_rebinding_closes_old_mapping():
    c = compile('qubit bit=false; bool result=measure(bit); bit=!bit; result=measure(bit); return result;')
    mappings = [m for m in c.program.source_mappings if m.name == "result"]
    assert len(mappings) == 2 and mappings[0].bits != mappings[1].bits
    assert mappings[0].operation_end == mappings[1].operation_start


@pytest.mark.backend
def test_legacy_v3_module_without_presentation_fields_still_runs():
    from dataclasses import replace
    c = compile_source(
        'input int start; quint n=start; return measure(n);', inputs={"start": 1}, config=CompilerConfig(quint_bits=3))
    legacy_metadata = {k: v for k, v in c.metadata.items() if k not in
                       {"registers", "source_mappings", "regions", "cleanup_annotations", "warnings"}}
    legacy_metadata["artifact_schema"] = 3
    legacy_metadata["language_version"] = "0.3"
    legacy_metadata["config"].pop("wire_reuse", None)
    source = python_source(replace(c, metadata=legacy_metadata)).replace("qutes.artifact_v5", "qutes.artifact_v3")
    lines = source.splitlines()
    lines = [line for line in lines if "qc.add_register(" not in line]
    source = "\n".join(lines).replace("qc = QuantumCircuit()", "qc = QuantumCircuit(3, 3)")
    namespace = {"__name__": "legacy_generated"}
    exec(source, namespace)
    assert namespace["build"]()[0].qregs[0].name == "q"
    assert namespace["run"](shots=4)["outcomes"][0]["value"] == 1
    with pytest.raises(ValueError, match="rebuild"):
        namespace["run"]({"start": 2}, shots=4)
