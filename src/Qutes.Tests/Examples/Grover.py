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
qubit_8 = Qubit()
qubit_9 = Qubit()
qubit_1 = Qubit()
qubit_2 = Qubit()
qubit_3 = Qubit()
qubit_4 = Qubit()
qubit_5 = Qubit()
qubit_6 = Qubit()
qubit_7 = Qubit()
qubit_14 = Qubit()
qubit_15 = Qubit()
qubit_16 = Qubit()
qubit_17 = Qubit()
qubit_18 = Qubit()
qubit_21 = Qubit()
qubit_22 = Qubit()
qubit_10 = Qubit()
qubit_19 = Qubit()
qubit_20 = Qubit()
# Quantum registers declaration for main
main_pattern = QuantumRegister(name='main_pattern', bits=[qubit_8,qubit_9])
c_main_pattern = ClassicalRegister(size=2, name='c_main_pattern')
main_array = QuantumRegister(name='main_array', bits=[qubit_1,qubit_2,qubit_3,qubit_4,qubit_5,qubit_6,qubit_7])
c_main_array = ClassicalRegister(size=7, name='c_main_array')
rotation_1 = QuantumRegister(name='rotation_1', bits=[qubit_14,qubit_15,qubit_16])
c_rotation_1 = ClassicalRegister(size=3, name='c_rotation_1')
grover_result_1 = QuantumRegister(name='grover_result_1', bits=[qubit_17])
c_grover_result_1 = ClassicalRegister(size=1, name='c_grover_result_1')
controlled_circuit_3_controlled_circuit_2_esm_result_1 = QuantumRegister(name='controlled_circuit_3_controlled_circuit_2_esm_result_1', bits=[qubit_18])
c_controlled_circuit_3_controlled_circuit_2_esm_result_1 = ClassicalRegister(size=1, name='c_controlled_circuit_3_controlled_circuit_2_esm_result_1')
equality_2_0 = QuantumRegister(name='equality_2_0', bits=[qubit_21])
c_equality_2_0 = ClassicalRegister(size=1, name='c_equality_2_0')
equality_2_1 = QuantumRegister(name='equality_2_1', bits=[qubit_22])
c_equality_2_1 = ClassicalRegister(size=1, name='c_equality_2_1')
main_found = QuantumRegister(name='main_found', bits=[qubit_10])
c_main_found = ClassicalRegister(size=1, name='c_main_found')
equality_1_0 = QuantumRegister(name='equality_1_0', bits=[qubit_19])
c_equality_1_0 = ClassicalRegister(size=1, name='c_equality_1_0')
equality_1_1 = QuantumRegister(name='equality_1_1', bits=[qubit_20])
c_equality_1_1 = ClassicalRegister(size=1, name='c_equality_1_1')
# ================ Circuit circuit_1 =====================
# Qubits declaration for circuit_1
# Quantum registers declaration for circuit_1
# Circuit declaration: circuit_1
circuit_1 = QuantumCircuit(main_array,rotation_1,main_pattern,grover_result_1,equality_1_0,equality_1_1)
# Operation: ESM
# Operation: RightShift
right_shift_7_1_2 = QutesGates.crot(7, 2**2, 1).inverse()
circuit_1.compose(right_shift_7_1_2, [qubit_16,qubit_1,qubit_2,qubit_3,qubit_4,qubit_5,qubit_6,qubit_7], inplace=True)
right_shift_7_1_1 = QutesGates.crot(7, 2**1, 1).inverse()
circuit_1.compose(right_shift_7_1_1, [qubit_15,qubit_1,qubit_2,qubit_3,qubit_4,qubit_5,qubit_6,qubit_7], inplace=True)
right_shift_7_1_0 = QutesGates.crot(7, 2**0, 1).inverse()
circuit_1.compose(right_shift_7_1_0, [qubit_14,qubit_1,qubit_2,qubit_3,qubit_4,qubit_5,qubit_6,qubit_7], inplace=True)
# Operation: Equals
circuit_1.cx(qubit_1, qubit_19)
circuit_1.cx(qubit_8, qubit_19)
circuit_1.cx(qubit_2, qubit_20)
circuit_1.cx(qubit_9, qubit_20)
circuit_1.x([qubit_19,qubit_20])
circuit_1.mcx([qubit_19,qubit_20], qubit_17)
circuit_1.x([qubit_19,qubit_20])
circuit_1.cx(qubit_8, qubit_19)
circuit_1.cx(qubit_1, qubit_19)
circuit_1.cx(qubit_9, qubit_20)
circuit_1.cx(qubit_2, qubit_20)
# Operation: LeftShift
left_shift_7_1_0 = QutesGates.crot(7, 2**0, 1)
circuit_1.compose(left_shift_7_1_0, [qubit_14,qubit_1,qubit_2,qubit_3,qubit_4,qubit_5,qubit_6,qubit_7], inplace=True)
left_shift_7_1_1 = QutesGates.crot(7, 2**1, 1)
circuit_1.compose(left_shift_7_1_1, [qubit_15,qubit_1,qubit_2,qubit_3,qubit_4,qubit_5,qubit_6,qubit_7], inplace=True)
left_shift_7_1_2 = QutesGates.crot(7, 2**2, 1)
circuit_1.compose(left_shift_7_1_2, [qubit_16,qubit_1,qubit_2,qubit_3,qubit_4,qubit_5,qubit_6,qubit_7], inplace=True)
# Print for circuit circuit_1
print(circuit_1.decompose(reps=0).draw())
circuit_1.decompose(reps=0).draw(output='mpl', filename='./circuit_images/circuit_1_20260202_122658.png', style='iqp', fold=1000)
print('Quantum circuit image saved to: ./circuit_images/circuit_1_20260202_122658.png')

# ================ Circuit circuit_2 =====================
# Qubits declaration for circuit_2
# Quantum registers declaration for circuit_2
# Circuit declaration: circuit_2
circuit_2 = QuantumCircuit(main_found)
# Operation: Not
circuit_2.x([qubit_10])
# Print for circuit circuit_2
print(circuit_2.decompose(reps=0).draw())
circuit_2.decompose(reps=0).draw(output='mpl', filename='./circuit_images/circuit_2_20260202_122658.png', style='iqp', fold=1000)
print('Quantum circuit image saved to: ./circuit_images/circuit_2_20260202_122658.png')

# ================ Circuit controlled_circuit_2 =====================
# Qubits declaration for controlled_circuit_2
# Quantum registers declaration for controlled_circuit_2
# Circuit declaration: controlled_circuit_2
controlled_circuit_2 = QuantumCircuit(controlled_circuit_3_controlled_circuit_2_esm_result_1,main_found)
# Print for circuit controlled_circuit_2
print(controlled_circuit_2.decompose(reps=0).draw())
controlled_circuit_2.decompose(reps=0).draw(output='mpl', filename='./circuit_images/controlled_circuit_2_20260202_122658.png', style='iqp', fold=1000)
print('Quantum circuit image saved to: ./circuit_images/controlled_circuit_2_20260202_122658.png')

controlled_circuit_2 = circuit_2.control(1, ctrl_state='1', label='controlled_circuit_2')
# ================ Circuit circuit_3 =====================
# Qubits declaration for circuit_3
# Quantum registers declaration for circuit_3
# Circuit declaration: circuit_3
circuit_3 = QuantumCircuit(main_found)
# Operation: Hadamard
circuit_3.h([qubit_10])
# Print for circuit circuit_3
print(circuit_3.decompose(reps=0).draw())
circuit_3.decompose(reps=0).draw(output='mpl', filename='./circuit_images/circuit_3_20260202_122658.png', style='iqp', fold=1000)
print('Quantum circuit image saved to: ./circuit_images/circuit_3_20260202_122658.png')

# ================ Circuit controlled_circuit_3 =====================
# Qubits declaration for controlled_circuit_3
# Quantum registers declaration for controlled_circuit_3
# Circuit declaration: controlled_circuit_3
controlled_circuit_3 = QuantumCircuit(controlled_circuit_3_controlled_circuit_2_esm_result_1,main_found)
# Print for circuit controlled_circuit_3
print(controlled_circuit_3.decompose(reps=0).draw())
controlled_circuit_3.decompose(reps=0).draw(output='mpl', filename='./circuit_images/controlled_circuit_3_20260202_122658.png', style='iqp', fold=1000)
print('Quantum circuit image saved to: ./circuit_images/controlled_circuit_3_20260202_122658.png')

controlled_circuit_3 = circuit_3.control(1, ctrl_state='0', label='controlled_circuit_3')
# Circuit declaration: main
main = QuantumCircuit(main_pattern,main_array,rotation_1,grover_result_1,controlled_circuit_3_controlled_circuit_2_esm_result_1,equality_2_0,equality_2_1,main_found,equality_1_0,equality_1_1, c_main_pattern,c_main_array,c_rotation_1,c_grover_result_1,c_controlled_circuit_3_controlled_circuit_2_esm_result_1,c_equality_2_0,c_equality_2_1,c_main_found,c_equality_1_0,c_equality_1_1)
# Register initialization for main
qreg_9_state_prep = StatePreparation([complex(1),complex(0),], normalize=True)
main.compose(qreg_9_state_prep, [qubit_8], inplace=True)
qreg_10_state_prep = StatePreparation([complex(1),complex(0),], normalize=True)
main.compose(qreg_10_state_prep, [qubit_9], inplace=True)
qreg_1_state_prep = StatePreparation([complex(0),complex(1),], normalize=True)
main.compose(qreg_1_state_prep, [qubit_1], inplace=True)
qreg_2_state_prep = StatePreparation([complex(0),complex(1),], normalize=True)
main.compose(qreg_2_state_prep, [qubit_2], inplace=True)
qreg_3_state_prep = StatePreparation([complex(0),complex(1),], normalize=True)
main.compose(qreg_3_state_prep, [qubit_3], inplace=True)
qreg_4_state_prep = StatePreparation([complex(1),complex(0),], normalize=True)
main.compose(qreg_4_state_prep, [qubit_4], inplace=True)
qreg_5_state_prep = StatePreparation([complex(0),complex(1),], normalize=True)
main.compose(qreg_5_state_prep, [qubit_5], inplace=True)
qreg_6_state_prep = StatePreparation([complex(0),complex(1),], normalize=True)
main.compose(qreg_6_state_prep, [qubit_6], inplace=True)
qreg_7_state_prep = StatePreparation([complex(0),complex(1),], normalize=True)
main.compose(qreg_7_state_prep, [qubit_7], inplace=True)
rotation_1_state_prep = StatePreparation([complex(1),complex(1),complex(1),complex(1),complex(1),complex(1),complex(1),complex(1),], normalize=True)
main.compose(rotation_1_state_prep, [qubit_14,qubit_15,qubit_16], inplace=True)
grover_result_1_state_prep = StatePreparation([complex(1),complex(-1),], normalize=True)
main.compose(grover_result_1_state_prep, [qubit_17], inplace=True)
main_found_state_prep = StatePreparation([complex(1),complex(0),], normalize=True)
main.compose(main_found_state_prep, [qubit_10], inplace=True)
# Operation: Grover
grover_1 = GroverOperator(circuit_1, reflection_qubits=[qubit_14,qubit_15,qubit_16], insert_barriers=True, name='grover_1')
grover_1 = grover_1.power(1)
main.compose(grover_1, [qubit_1,qubit_2,qubit_3,qubit_4,qubit_5,qubit_6,qubit_7,qubit_14,qubit_15,qubit_16,qubit_8,qubit_9,qubit_17,qubit_19,qubit_20], inplace=True)
print(grover_1.decompose(reps=1).draw())
grover_1.decompose(reps=1).draw(output='mpl', filename='./circuit_images/grover_1_20260202_122658.png', style='iqp', fold=1000)
print('Quantum circuit image saved to: ./circuit_images/grover_1_20260202_122658.png')
# Operation: ESM
# Operation: RightShift
right_shift_7_1_2 = QutesGates.crot(7, 2**2, 1).inverse()
main.compose(right_shift_7_1_2, [qubit_16,qubit_1,qubit_2,qubit_3,qubit_4,qubit_5,qubit_6,qubit_7], inplace=True)
right_shift_7_1_1 = QutesGates.crot(7, 2**1, 1).inverse()
main.compose(right_shift_7_1_1, [qubit_15,qubit_1,qubit_2,qubit_3,qubit_4,qubit_5,qubit_6,qubit_7], inplace=True)
right_shift_7_1_0 = QutesGates.crot(7, 2**0, 1).inverse()
main.compose(right_shift_7_1_0, [qubit_14,qubit_1,qubit_2,qubit_3,qubit_4,qubit_5,qubit_6,qubit_7], inplace=True)
# Operation: Equals
main.cx(qubit_1, qubit_21)
main.cx(qubit_8, qubit_21)
main.cx(qubit_2, qubit_22)
main.cx(qubit_9, qubit_22)
main.x([qubit_21,qubit_22])
main.mcx([qubit_21,qubit_22], qubit_18)
main.x([qubit_21,qubit_22])
main.cx(qubit_8, qubit_21)
main.cx(qubit_1, qubit_21)
main.cx(qubit_9, qubit_22)
main.cx(qubit_2, qubit_22)
# Operation: LeftShift
left_shift_7_1_0 = QutesGates.crot(7, 2**0, 1)
main.compose(left_shift_7_1_0, [qubit_14,qubit_1,qubit_2,qubit_3,qubit_4,qubit_5,qubit_6,qubit_7], inplace=True)
left_shift_7_1_1 = QutesGates.crot(7, 2**1, 1)
main.compose(left_shift_7_1_1, [qubit_15,qubit_1,qubit_2,qubit_3,qubit_4,qubit_5,qubit_6,qubit_7], inplace=True)
left_shift_7_1_2 = QutesGates.crot(7, 2**2, 1)
main.compose(left_shift_7_1_2, [qubit_16,qubit_1,qubit_2,qubit_3,qubit_4,qubit_5,qubit_6,qubit_7], inplace=True)
# Operation: Measure
main.measure(rotation_1, c_rotation_1)
# Operation: ComposeCircuit
controlled_circuit_2_gate = controlled_circuit_2.to_gate(label='controlled_circuit_2')
main.compose(controlled_circuit_2_gate, [qubit_18,qubit_10], inplace=True)
# Operation: ComposeCircuit
controlled_circuit_3_gate = controlled_circuit_3.to_gate(label='controlled_circuit_3')
main.compose(controlled_circuit_3_gate, [qubit_18,qubit_10], inplace=True)
# Operation: Measure
main.measure(main_found, c_main_found)
# Print for circuit main
print(main.decompose(reps=0).draw())
main.decompose(reps=0).draw(output='mpl', filename='./circuit_images/main_20260202_122658.png', style='iqp', fold=1000)
print('Quantum circuit image saved to: ./circuit_images/main_20260202_122658.png')

# Qiskit execution
sampler = StatevectorSampler()
result = sampler.run([main], shots=1024).result()
# Result pretty print
var_names = ['rotation_1', 'main_found']
var_sizes = {'rotation_1': 3, 'main_found': 1}
var_to_clreg = {'rotation_1': 'c_rotation_1', 'main_found': 'c_main_found'}
print_pretty_results_mapped(result, var_names, var_sizes, var_to_clreg)
