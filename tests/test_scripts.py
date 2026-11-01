"""Public 0.2 script semantics: no legacy source adapter or automatic main."""
import pytest
from qutes.compiler import compile_source
from qutes.checker import analyze
from qutes.parser import parse
from qutes.config import CompilerConfig
from qutes.diagnostics import DiagnosticError


def compiled(source, inputs=None):
    return compile_source(source, inputs=inputs, config=CompilerConfig(quint_bits=3))


def value(source, inputs=None):
    return compiled(source, inputs).run(shots=16, seed=7)['outcomes'][0]['value']


@pytest.mark.parametrize('source,expected', [
    ('', None), ('int main() { return 7; }', None),
    ('int main() { return 7; } return main();', 7),
    ('return answer(); int answer() { return 42; }', 42),
    ('int x=1; void inc() { x+=1; } inc(); inc(); return x;', 3),
    ('int x=1; void a(){ b(); } void b(){x+=2;} a(); return x;', 3),
    ('int x=1; int f(){int x=7; return x;} int y=f(); return [x,y];', [1,7]),
    ('int x=1; void inc(){x+=1;} for(int i=0;i<3;i++){inc();} return x;', 4),
    ('int x=0; void inc(){x+=1;} while(x<3){inc();} return x;', 3),
    ('int[] xs=[1,2]; void edit(){xs[1]=3;} edit(); return xs;', [1,3]),
    ('quint q=1; void inc(){q+=1;} inc(); return measure(q);', 2),
    ('quint q=1; int sample(){return measure(q);} int a=sample(); q+=1; return [a,sample()];', [1,2]),
    ('quint q=1; int sample(quint v){return measure(v);} return sample(q);', 1),
    ('qubit q=false; bool read(){return measure(q);} bool a=read(); if(a){q=true;} return measure(q);', False),
    ('int main(){quint q=1; return measure(q);} return main();', 1),
    ('return; int f(){return 1;}', None),
])
def test_script_execution(source, expected):
    assert value(source) == expected


def test_input_declarations_bind_and_remain_mutable():
    source = 'input int increment; quint q=1; void next(){q+=increment;} next(); increment=1; next(); return measure(q);'
    result = compiled(source, {'increment':1})
    assert result.run(shots=8)['outcomes'][0]['value'] == 3
    assert result.metadata['inputs'] == {'increment':1}
    assert value('input int[] xs; return xs;', {'xs':[1,2]}) == [1,2]


@pytest.mark.parametrize('inputs', [{}, {'n':True}, {'n':1,'extra':2}])
def test_input_schema_errors(inputs):
    with pytest.raises(DiagnosticError, match='Q2001'):
        compiled('input int n; return n;', inputs)


@pytest.mark.parametrize('source,code', [
    ('f(); int x=1; void f(){x+=1;}', 'Q2002'),
    ('f(); int x=1; void f(){g();} void g(){int a=x;}', 'Q2002'),
    ('int x=x;', 'Q2002'),
    ('{ int x=1; } return x;', 'Q2002'),
    ('input quint q;', 'Q2001'),
    ('void f(){input int x;} f();', 'Q1002'),
    ('input int x=1;', 'Q1002'),
    ('quint q=1; return q;', 'Q2005'),
    ('return 1; return;', 'Q2005'),
    ('return 1; return true;', 'Q2005'),
    ('input bool b; if(b){return 1;}', 'Q2005'),
    ('quint q=1; int sample(){return measure(q);} if(true){sample();}', 'Q2004'),
    ('quint q=1; int a(){return b();} int b(){return measure(q);} if(true){a();}', 'Q2004'),
    ('quint q=1; void f(quint p){q+=1;} f(q);', 'Q2004'),
    ('quint[] qs=[1,2]; void f(quint p){qs[0]+=1;} f(qs[1]);', 'Q2004'),
    ('qubit q=superposition(); void flip(){q=true;} if(q){flip();}', 'Q2004'),
    ('qubit q=superposition(); int n=0; void set(){n=1;} if(q){set();}', 'Q2004'),
    ('qubit q=superposition(); void f(){qubit r=superposition();} if(q){f();}', 'Q2004'),
    ('qubit q=superposition(); bool b=measure(q); bool f(){return measure(q);} bool c=b&&f();', 'Q2004'),
    ('quint q=1; int n=1; void sample(){n=measure(q);} sample(); int a=n+1;', 'Q2003'),
])
def test_script_safety_diagnostics(source, code):
    with pytest.raises(DiagnosticError) as failure:
        compiled(source)
    assert failure.value.code == code, str(failure.value)


def test_inferred_transitive_effects_are_visible_in_ir():
    tree = analyze(parse('quint q=1; int a(){return b();} int b(){return measure(q);} return a();'))
    a = next(f for f in tree.functions if f.name == 'a')
    assert 'measure' in a.effects
    assert any(effect.startswith('read:') for effect in a.effects)


def test_spelling_hint():
    with pytest.raises(DiagnosticError) as failure:
        compiled('int number=1; return numbr;')
    assert failure.value.help == "Did you mean 'number'?"


def test_global_updates_cleanup_and_complex_amplitudes():
    import numpy as np
    from qiskit.quantum_info import Statevector
    from tests.reference import random_state
    compilation = compiled('''
        quint root=0; quint output=0;
        void update() {
            quint local=root+1;
            output+=local;
            root+=-2;
        }
        update();
    ''')
    program = compilation.program
    # Arbitrary complex input entangled with an external reference; all compiler
    # temporaries must end at zero, not merely give correct measurement counts.
    amplitudes = random_state(4, seed=71)
    initial = np.zeros(2**(program.qubit_count+1), dtype=complex)
    expected = np.zeros_like(initial)
    for index, amplitude in enumerate(amplitudes):
        root, reference = index & 7, index >> 3
        initial[root | (reference << program.qubit_count)] = amplitude
        expected[((root-2)&7) | (((root+1)&7)<<3) | (reference<<program.qubit_count)] = amplitude
    from qiskit import QuantumCircuit
    circuit = QuantumCircuit(program.qubit_count+1)
    circuit.compose(program.to_qiskit(), qubits=range(program.qubit_count), inplace=True)
    actual = Statevector(initial).evolve(circuit).data
    np.testing.assert_allclose(actual, expected, atol=1e-10)
    assert all(allocation.released for allocation in program.allocations[2:])


def test_helper_measurement_preserves_correlations_and_snapshot_order():
    from tests.test_lowering import distribution
    program = compiled('''
        qubit root=superposition(); qubit copy=root;
        bool sample(){ return measure(root); }
        bool before=sample();
        root=!root;
        return [before,measure(copy),sample()];
    ''').program
    assert distribution(program) == pytest.approx({'[false, false, true]':0.5, '[true, true, false]':0.5})


def test_nested_readonly_alias_cannot_write_global():
    with pytest.raises(DiagnosticError, match='Q2004'):
        compiled('quint q=1; void g(){q+=1;} void f(quint p){g();} f(q);')


def test_helpers_cannot_hide_unclean_local_roots_in_globals():
    with pytest.raises(DiagnosticError, match='Q3001'):
        compiled('qubit result=false; void f(){qubit root=superposition(); result=root;} f();')


def test_actual_global_stage_and_shape_are_checked_at_each_call():
    assert value('string s="A"; int size(){return s.Length;} int a=size(); s="ABC"; return [a,size()];') == [1,3]
    assert value('quint q=1; int n=1; int get(){return n;} int a=get(); n=measure(q); return [a,get()];') == [1,1]
    with pytest.raises(DiagnosticError, match='Q2003'):
        compiled('quint q=1; int n=1; int get(){return n+1;} int a=get(); n=measure(q); return get();')


def test_short_circuit_does_not_apply_skipped_global_effects():
    assert value('quint q=1; int n=1; bool sample(){n=measure(q);return true;} bool b=false&&sample(); return n+1;') == 2
    with pytest.raises(DiagnosticError, match='Q2004'):
        compiled('qubit q=false; bool b=measure(q); int n=0; bool set(){n=1;return true;} bool c=b&&set(); return n;')
