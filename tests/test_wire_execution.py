"""Physical execution compared to unchanged logical schedules and final states."""
from dataclasses import replace
from pathlib import Path
import json

import numpy as np
import pytest
from qiskit.quantum_info import Statevector

from qutes.cli import main
from qutes.codegen import python_source
from qutes.compiler import compile_source
from qutes.config import CompilerConfig
from qutes.gates import Measurement
from qutes.qiskit_backend import emit_operations

pytestmark = pytest.mark.backend
CONFIG = CompilerConfig(quint_bits=2, alphabet="AB")


@pytest.mark.parametrize("source", [
    'quint n=superposition(); { quint a=n+1; } { quint b=n+-2; }',
    'qubit n=superposition(); qubit r=n; { qubit a=!n; r=!a; }',
    'quint n=superposition(); quint result=0; { quint a=n+1; result+=a; n+=1; }',
    'quint next(quint n) { quint a=n+1; return a; } quint n=superposition(); { quint a=next(n); } quint result=next(n);',
    'qubit good(qubit n) { return !n; } qubit s=superposition(); qubit[] data=[s,!s,true]; qubit selected=search(data,good); { qubit v=!s; }',
    'qubit good(qubit n) { return n; } { qubit a=search([false,true],good); } qubit b=search([true,false],good);',
    'qubit good(qubit n) { return n; } qubit[] data=[true,false]; { qubit a=search(data,good); data[0]=!data[0]; }',
    'qustring text="AB"; { qubit matches="A?" in text; } { qubit other="?B" in text; }',
])
def test_mapping_preserves_phases_correlations_and_certified_zero(source):
    compiled = compile_source(source, config=CONFIG)
    logical = compiled.program.logical_program
    allocation = compiled.program.wire_allocation
    physical = Statevector.from_instruction(compiled.build()[0]).data
    reference = Statevector.from_instruction(logical.to_qiskit()).data
    live = {b for storage in logical.allocations if not storage.released
            for b in storage.bits if b not in storage.scratch_bits}
    lookup = allocation.lookup()
    expected = np.zeros_like(physical)
    for index, amplitude in enumerate(reference):
        if any(index >> b & 1 for b in range(logical.qubit_count) if b not in live):
            assert abs(amplitude) < 1e-10
        else:
            output = sum(((index >> b) & 1) << lookup.at(b, len(logical.operations)) for b in live)
            expected[output] = amplitude
    np.testing.assert_allclose(physical, expected, atol=1e-10)
    # Semantic certificates are checked independently against logical prefix states.
    for proof in logical.zero_certificates:
        prefix = emit_operations(logical.qubit_count, 0, logical.operations[:proof.boundary])
        state = Statevector.from_instruction(prefix).data
        assert sum(abs(a) ** 2 for i, a in enumerate(state) if any(i >> b & 1 for b in proof.bits)) < 1e-12


@pytest.mark.parametrize("source,expected", [
    ('quint n=0; { quint local=n+1; int snapshot=measure(local); n+=1; } return measure(n);', 1),
    ('quint n=1; int before=measure(n); n+=1; { quint t=n+1; } if(before==1) { n+=1; } return [before,measure(n)];', [1,-1]),
    ('quint[] data=[0,1]; data=[data[1],data[0]]; foreach(quint x in data) { quint local=x+1; } return measure(data);', [1,0]),
])
def test_measurement_feedforward_aliases_and_generated_parity(source, expected):
    for enabled in (True, False):
        c = compile_source(source, config=replace(CONFIG, wire_reuse=enabled))
        namespace = {"__name__": "generated"}
        exec(python_source(c), namespace)
        assert namespace["build"]()[0] == c.build()[0]
        assert c.run(shots=16, seed=17)["outcomes"][0]["value"] == expected
        assert namespace["run"](shots=16, seed=17)["outcomes"][0]["value"] == expected
        logical_ops = c.program.logical_program.operations
        for i, (original, mapped) in enumerate(zip(logical_ops, c.program.operations, strict=True)):
            lookup = c.program.wire_allocation.lookup()
            if isinstance(original, Measurement):
                assert mapped == replace(original, qubits=tuple(lookup.at(b, i) for b in original.qubits))
            else:
                assert mapped == replace(original, targets=tuple(lookup.at(b,i) for b in original.targets),
                    inputs=tuple(lookup.at(b,i) for b in original.inputs),
                    controls=tuple((lookup.at(b,i), v) for b,v in original.controls))


def test_config_cli_identity_limits_and_respecialization(tmp_path, capsys):
    source = 'input int count; quint n=1; for(int i=0;i<count;i++) { quint t=n+1; } return measure(n);'
    config = replace(CONFIG, max_simulation_qubits=4)
    reused = compile_source(source, inputs={"count": 3}, config=config)
    baseline = compile_source(source, inputs={"count": 3}, config=replace(config, wire_reuse=False))
    assert reused.program.qubit_count == 4
    assert baseline.program.qubit_count == 8
    assert reused.metadata["build_sha256"] != baseline.metadata["build_sha256"]
    assert reused.metadata["resources"]["simulation_within_limit"]
    assert not baseline.metadata["resources"]["simulation_within_limit"]
    namespace = {"__name__": "generated"}
    exec(python_source(reused), namespace)
    outcome = namespace["run"]({"count": 5}, shots=4)
    assert outcome["build"]["resources"]["allocated_qubits"] == 4
    assert outcome["build"]["artifact_schema"] == 4
    assert outcome["outcomes"][0]["value"] == 1
    path = tmp_path / "example.qut"
    path.write_text('quint n=1; { quint t=n+1; } { quint t=n+1; }')
    for flag, enabled in [("--wire-reuse", True), ("--no-wire-reuse", False)]:
        assert main(["check", str(path), flag, "--json"]) == 0
        assert json.loads(capsys.readouterr().out)["metadata"]["resources"]["wire_reuse"] is enabled
    for invalid in (1, "false", None):
        with pytest.raises(ValueError, match="Boolean"):
            CompilerConfig(wire_reuse=invalid)


@pytest.mark.parametrize("source", [
    'qubit source=superposition(); qubit retained=source; '
    '{ qubit t=source; bool before=measure(t); } '
    '{ qubit other=!source; } bool result=measure(source); source=!source; '
    'if(result) { retained=!retained; }',
    'qubit good(qubit x){return x;} qubit source=superposition(); '
    'qubit[] data=[source,!source]; qubit selected=search(data,good); '
    'bool before=measure(selected); selected=!selected; { qubit t=!source; }',
    'qubit predicate=superposition(); quint n=0; '
    'if(predicate) { quint t=n+1; n+=1; } else { quint t=n+-1; n+=-1; } '
    'bool observed=measure(predicate); if(observed) { quint t=n+1; n+=1; }',
])
def test_joint_classical_and_remaining_quantum_state(source):
    from tests.test_measurement_cleanup import branches_for
    program = compile_source(source, config=CONFIG).program
    logical = program.logical_program
    physical_branches = {branch.snapshots: branch for branch in branches_for(program)}
    logical_branches = {branch.snapshots: branch for branch in branches_for(logical)}
    assert physical_branches.keys() == logical_branches.keys()
    live = {bit for a in logical.allocations if not a.released for bit in a.bits if bit not in a.scratch_bits}
    lookup = program.wire_allocation.lookup()
    for snapshots, expected_branch in logical_branches.items():
        actual = physical_branches[snapshots]
        assert actual.probability == pytest.approx(expected_branch.probability)
        expected = np.zeros_like(actual.state)
        for index, amplitude in enumerate(expected_branch.state):
            if any(index >> bit & 1 for bit in range(logical.qubit_count) if bit not in live):
                assert abs(amplitude) < 1e-10
            else:
                physical_index = sum(((index >> bit) & 1) << lookup.at(bit, len(program.operations)) for bit in live)
                expected[physical_index] = amplitude
        np.testing.assert_allclose(actual.state, expected, atol=1e-10)
