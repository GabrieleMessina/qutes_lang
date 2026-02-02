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
qubit_13 = Qubit()
qubit_14 = Qubit()
qubit_15 = Qubit()
qubit_4 = Qubit()
qubit_16 = Qubit()
qubit_17 = Qubit()
qubit_18 = Qubit()
qubit_7 = Qubit()
qubit_19 = Qubit()
qubit_20 = Qubit()
qubit_21 = Qubit()
qubit_13 = Qubit()
qubit_14 = Qubit()
qubit_15 = Qubit()
qubit_16 = Qubit()
qubit_17 = Qubit()
qubit_18 = Qubit()
qubit_19 = Qubit()
qubit_20 = Qubit()
qubit_21 = Qubit()
# Quantum registers declaration for main
controlled_circuit_1_qreg_5 = QuantumRegister(name='controlled_circuit_1_qreg_5', bits=[qubit_1])
c_controlled_circuit_1_qreg_5 = ClassicalRegister(size=1, name='c_controlled_circuit_1_qreg_5')
qreg_9 = QuantumRegister(name='qreg_9', bits=[qubit_13,qubit_14,qubit_15])
c_qreg_9 = ClassicalRegister(size=3, name='c_qreg_9')
controlled_circuit_2_qreg_6 = QuantumRegister(name='controlled_circuit_2_qreg_6', bits=[qubit_4])
c_controlled_circuit_2_qreg_6 = ClassicalRegister(size=1, name='c_controlled_circuit_2_qreg_6')
qreg_10 = QuantumRegister(name='qreg_10', bits=[qubit_16,qubit_17,qubit_18])
c_qreg_10 = ClassicalRegister(size=3, name='c_qreg_10')
controlled_circuit_3_qreg_7 = QuantumRegister(name='controlled_circuit_3_qreg_7', bits=[qubit_7])
c_controlled_circuit_3_qreg_7 = ClassicalRegister(size=1, name='c_controlled_circuit_3_qreg_7')
qreg_11 = QuantumRegister(name='qreg_11', bits=[qubit_19,qubit_20,qubit_21])
c_qreg_11 = ClassicalRegister(size=3, name='c_qreg_11')
main_vector = QuantumRegister(name='main_vector', bits=[qubit_13,qubit_14,qubit_15,qubit_16,qubit_17,qubit_18,qubit_19,qubit_20,qubit_21])
c_main_vector = ClassicalRegister(size=9, name='c_main_vector')
# ================ Circuit circuit_1 =====================
# Qubits declaration for circuit_1
# Quantum registers declaration for circuit_1
# Circuit declaration: circuit_1
circuit_1 = QuantumCircuit(qreg_9)
# Operation: Hadamard
circuit_1.h([qubit_13,qubit_14,qubit_15])
# Print for circuit circuit_1
print(circuit_1.decompose(reps=0).draw())
circuit_1.decompose(reps=0).draw(output='mpl', filename='./circuit_images/circuit_1_20260202_122637.png', style='iqp', fold=1000)
print('Quantum circuit image saved to: ./circuit_images/circuit_1_20260202_122637.png')

# ================ Circuit controlled_circuit_1 =====================
# Qubits declaration for controlled_circuit_1
# Quantum registers declaration for controlled_circuit_1
# Circuit declaration: controlled_circuit_1
controlled_circuit_1 = QuantumCircuit(controlled_circuit_1_qreg_5,qreg_9)
# Print for circuit controlled_circuit_1
print(controlled_circuit_1.decompose(reps=0).draw())
controlled_circuit_1.decompose(reps=0).draw(output='mpl', filename='./circuit_images/controlled_circuit_1_20260202_122637.png', style='iqp', fold=1000)
print('Quantum circuit image saved to: ./circuit_images/controlled_circuit_1_20260202_122637.png')

controlled_circuit_1 = circuit_1.control(1, ctrl_state='1', label='controlled_circuit_1')
# ================ Circuit circuit_2 =====================
# Qubits declaration for circuit_2
# Quantum registers declaration for circuit_2
# Circuit declaration: circuit_2
circuit_2 = QuantumCircuit(qreg_10)
# Operation: Hadamard
circuit_2.h([qubit_16,qubit_17,qubit_18])
# Print for circuit circuit_2
print(circuit_2.decompose(reps=0).draw())
circuit_2.decompose(reps=0).draw(output='mpl', filename='./circuit_images/circuit_2_20260202_122637.png', style='iqp', fold=1000)
print('Quantum circuit image saved to: ./circuit_images/circuit_2_20260202_122637.png')

# ================ Circuit controlled_circuit_2 =====================
# Qubits declaration for controlled_circuit_2
# Quantum registers declaration for controlled_circuit_2
# Circuit declaration: controlled_circuit_2
controlled_circuit_2 = QuantumCircuit(controlled_circuit_2_qreg_6,qreg_10)
# Print for circuit controlled_circuit_2
print(controlled_circuit_2.decompose(reps=0).draw())
controlled_circuit_2.decompose(reps=0).draw(output='mpl', filename='./circuit_images/controlled_circuit_2_20260202_122637.png', style='iqp', fold=1000)
print('Quantum circuit image saved to: ./circuit_images/controlled_circuit_2_20260202_122637.png')

controlled_circuit_2 = circuit_2.control(1, ctrl_state='1', label='controlled_circuit_2')
# ================ Circuit circuit_3 =====================
# Qubits declaration for circuit_3
# Quantum registers declaration for circuit_3
# Circuit declaration: circuit_3
circuit_3 = QuantumCircuit(qreg_11)
# Operation: Hadamard
circuit_3.h([qubit_19,qubit_20,qubit_21])
# Print for circuit circuit_3
print(circuit_3.decompose(reps=0).draw())
circuit_3.decompose(reps=0).draw(output='mpl', filename='./circuit_images/circuit_3_20260202_122637.png', style='iqp', fold=1000)
print('Quantum circuit image saved to: ./circuit_images/circuit_3_20260202_122637.png')

# ================ Circuit controlled_circuit_3 =====================
# Qubits declaration for controlled_circuit_3
# Quantum registers declaration for controlled_circuit_3
# Circuit declaration: controlled_circuit_3
controlled_circuit_3 = QuantumCircuit(controlled_circuit_3_qreg_7,qreg_11)
# Print for circuit controlled_circuit_3
print(controlled_circuit_3.decompose(reps=0).draw())
controlled_circuit_3.decompose(reps=0).draw(output='mpl', filename='./circuit_images/controlled_circuit_3_20260202_122637.png', style='iqp', fold=1000)
print('Quantum circuit image saved to: ./circuit_images/controlled_circuit_3_20260202_122637.png')

controlled_circuit_3 = circuit_3.control(1, ctrl_state='1', label='controlled_circuit_3')
# Circuit declaration: main
main = QuantumCircuit(controlled_circuit_1_qreg_5,qreg_9,controlled_circuit_2_qreg_6,qreg_10,controlled_circuit_3_qreg_7,qreg_11,main_vector, c_controlled_circuit_1_qreg_5,c_qreg_9,c_controlled_circuit_2_qreg_6,c_qreg_10,c_controlled_circuit_3_qreg_7,c_qreg_11,c_main_vector)
# Register initialization for main
controlled_circuit_1_qreg_5_state_prep = StatePreparation([complex(0),complex(1),], normalize=True)
main.compose(controlled_circuit_1_qreg_5_state_prep, [qubit_1], inplace=True)
qreg_9_state_prep = StatePreparation([complex(0),complex(1),complex(0),complex(0),complex(0),complex(0),complex(0),complex(0),], normalize=True)
main.compose(qreg_9_state_prep, [qubit_13,qubit_14,qubit_15], inplace=True)
controlled_circuit_2_qreg_6_state_prep = StatePreparation([complex(1),complex(0),], normalize=True)
main.compose(controlled_circuit_2_qreg_6_state_prep, [qubit_4], inplace=True)
qreg_10_state_prep = StatePreparation([complex(0),complex(0),complex(1),complex(0),complex(0),complex(0),complex(0),complex(0),], normalize=True)
main.compose(qreg_10_state_prep, [qubit_16,qubit_17,qubit_18], inplace=True)
controlled_circuit_3_qreg_7_state_prep = StatePreparation([complex(0),complex(1),], normalize=True)
main.compose(controlled_circuit_3_qreg_7_state_prep, [qubit_7], inplace=True)
qreg_11_state_prep = StatePreparation([complex(0),complex(0),complex(0),complex(1),complex(0),complex(0),complex(0),complex(0),], normalize=True)
main.compose(qreg_11_state_prep, [qubit_19,qubit_20,qubit_21], inplace=True)
# Operation: ComposeCircuit
controlled_circuit_1_gate = controlled_circuit_1.to_gate(label='controlled_circuit_1')
main.compose(controlled_circuit_1_gate, [qubit_1,qubit_13,qubit_14,qubit_15], inplace=True)
# Operation: ComposeCircuit
controlled_circuit_2_gate = controlled_circuit_2.to_gate(label='controlled_circuit_2')
main.compose(controlled_circuit_2_gate, [qubit_4,qubit_16,qubit_17,qubit_18], inplace=True)
# Operation: ComposeCircuit
controlled_circuit_3_gate = controlled_circuit_3.to_gate(label='controlled_circuit_3')
main.compose(controlled_circuit_3_gate, [qubit_7,qubit_19,qubit_20,qubit_21], inplace=True)
# Operation: Measure
main.measure(main_vector, c_main_vector)
# Print for circuit main
print(main.decompose(reps=0).draw())
main.decompose(reps=0).draw(output='mpl', filename='./circuit_images/main_20260202_122637.png', style='iqp', fold=1000)
print('Quantum circuit image saved to: ./circuit_images/main_20260202_122637.png')

# Qiskit execution
sampler = StatevectorSampler()
result = sampler.run([main], shots=1024).result()
# Result pretty print
var_names = ['main_vector']
var_sizes = {'main_vector': 9}
var_to_clreg = {'main_vector': 'c_main_vector'}
print_pretty_results_mapped(result, var_names, var_sizes, var_to_clreg)
