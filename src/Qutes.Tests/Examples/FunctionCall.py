from QutesLib import *
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.circuit import Qubit
from qiskit.primitives import StatevectorSampler
from qiskit.circuit.library import StatePreparation, ModularAdderGate, MultiplierGate, OrGate, AndGate, grover_operator as GroverOperator
import os
os.makedirs(r'./circuit_images', exist_ok=True)
# Operation Requirements
# ================ Circuit main =====================
# Qubits declaration for main
qubit_1 = Qubit()
qubit_2 = Qubit()
qubit_3 = Qubit()
qubit_4 = Qubit()
qubit_8 = Qubit()
# Quantum registers declaration for main
main_a = QuantumRegister(name='main_a', bits=[qubit_1,qubit_2,qubit_3])
c_main_a = ClassicalRegister(size=3, name='c_main_a')
main_d = QuantumRegister(name='main_d', bits=[qubit_4])
c_main_d = ClassicalRegister(size=1, name='c_main_d')
main_e = QuantumRegister(name='main_e', bits=[qubit_8])
c_main_e = ClassicalRegister(size=1, name='c_main_e')
# ================ Circuit foo =====================
# Qubits declaration for foo
# Quantum registers declaration for foo
# Circuit declaration: foo
foo = QuantumCircuit(main_a,main_d)
# Operation: Hadamard
foo.h([qubit_1,qubit_2,qubit_3])
# Operation: MCX
foo.mcx([qubit_1,qubit_2,qubit_3],[qubit_4])
# Print for circuit foo
print(foo.decompose(reps=0).draw())
foo.decompose(reps=0).draw(output='mpl', filename='./circuit_images/foo_20260202_122243.png', style='iqp', fold=1000)
print('Quantum circuit image saved to: ./circuit_images/foo_20260202_122243.png')

# Circuit declaration: main
main = QuantumCircuit(main_a,main_d,main_e, c_main_a,c_main_d,c_main_e)
# Register initialization for main
qreg_1_state_prep = StatePreparation([complex(1),complex(1),], normalize=True)
main.compose(qreg_1_state_prep, [qubit_1], inplace=True)
qreg_2_state_prep = StatePreparation([complex(1),complex(1),], normalize=True)
main.compose(qreg_2_state_prep, [qubit_2], inplace=True)
qreg_3_state_prep = StatePreparation([complex(1),complex(1),], normalize=True)
main.compose(qreg_3_state_prep, [qubit_3], inplace=True)
main_d_state_prep = StatePreparation([complex(1),complex(0),], normalize=True)
main.compose(main_d_state_prep, [qubit_4], inplace=True)
main_e_state_prep = StatePreparation([complex(1),complex(0),], normalize=True)
main.compose(main_e_state_prep, [qubit_8], inplace=True)
# Operation: ComposeCircuit
foo_gate = foo.to_gate(label='foo')
main.compose(foo_gate, [qubit_1,qubit_2,qubit_3,qubit_4], inplace=True)
# Operation: Measure
main.measure(main_e, c_main_e)
# Print for circuit main
print(main.decompose(reps=0).draw())
main.decompose(reps=0).draw(output='mpl', filename='./circuit_images/main_20260202_122243.png', style='iqp', fold=1000)
print('Quantum circuit image saved to: ./circuit_images/main_20260202_122243.png')

# Qiskit execution
sampler = StatevectorSampler()
result = sampler.run([main], shots=1024).result()
# Result pretty print
var_names = ['main_e']
var_sizes = {'main_e': 1}
var_to_clreg = {'main_e': 'c_main_e'}
print_pretty_results_mapped(result, var_names, var_sizes, var_to_clreg)
