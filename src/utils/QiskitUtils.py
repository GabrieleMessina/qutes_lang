import numpy as np
import math

from qiskit import IBMQ, Aer
#from qiskit.providers.ibmq import least_busy
from qiskit import QuantumCircuit, transpile, QuantumRegister, ClassicalRegister
from qiskit.circuit import Qubit
#from qiskit.providers.aer import QasmSimulator
from qiskit.visualization import plot_histogram
from qiskit.visualization import plot_bloch_vector
import matplotlib.pyplot as plt
#from PIL import Image as mpimg
import matplotlib.image as mpimg
from qiskit.extensions import Initialize


def normalizza(v):
    v = v/np.linalg.norm(v)
    return v

def random_state(nqubits):
    state = np.random.rand(2**nqubits)   # the sum of amplitudes-squared must equal one
    state = state/np.linalg.norm(state) # normalization
    return state

# function used to print a circuit
def print_circuit(circuit):
    print(circuit.draw())

# function used for drawing images
def draw_circuit(circuit):
    circuit.draw(output='mpl',filename="image.jpg")
    fig, ax = plt.subplots()
    im = mpimg.imread('image.jpg')
    ax.axis('off')
    ax.imshow(im)

# function used for drawing images with inverse calssical bits
def draw_circuit_reverse(circuit):
    circuit.draw(output='mpl',filename="image.jpg", reverse_bits=True)
    fig, ax = plt.subplots()
    im = mpimg.imread('image.jpg')
    ax.axis('off')
    ax.imshow(im)

def showBS(state):
    im = plot_bloch_vector(state, title="Bloch Sphere")
    im.savefig("bloch.jpg") 
    fig, ax = plt.subplots()
    im = mpimg.imread('bloch.jpg')
    ax.axis('off')
    ax.imshow(im)

def counts(vec):
    print("COUNTS:")
    for i in vec:
            print(" - " + str(i) +" : "+ str(vec[i]))

def revcounts(vec):
    print("COUNTS:")
    for i in vec:
            print(" - " + str(i)[::-1] +" : "+ str(vec[i]))

# simulate the execution of a Quantum Circuit and get the results
def run(circuit, shots):
    # Use Aer's qasm_simulator
    #results = aer_sim.run(dj_circuit).result()
    #answer = results.get_counts()

    #simulator = QasmSimulator()
    simulator = Aer.get_backend('aer_simulator')

    # compile the circuit down to low-level QASM instructions
    # supported by the backend (not needed for simple circuits)
    compiled_circuit = transpile(circuit, simulator)

    # Execute the circuit on the qasm simulator
    job = simulator.run(compiled_circuit, shots=shots)
    
    # Grab results from the job
    result = job.result()  
    cnt = result.get_counts(compiled_circuit)
    return cnt

# simulate the execution of a Quantum Circuit with a single run and get the output
def get_output(circuit, output_list):
    result = run(circuit,1)
    for i in result:
        out = i
    out = str(out)[::-1]
    output = ''
    for b in output_list:
        output = output+out[b]
    return output

# definition 1
# initial_state_zero = [1,0]
# initial_state_one = [0,1]
# a = QuantumRegister(1,"a")
# b = QuantumRegister(1,"b")
# a_sum_b = QuantumRegister(1,"sum")
# carry = QuantumRegister(1,"carry")
# res = ClassicalRegister(2,"2^")
# circuit = QuantumCircuit(a, b, a_sum_b, carry, res)
# circuit.barrier()
# circuit.cx(a,a_sum_b)
# circuit.cx(b,a_sum_b)
# circuit.mcx([a,b], carry)
# circuit.barrier()
# circuit.measure(a_sum_b, res[0])
# circuit.measure(carry, res[1])
# print(circuit.draw())


# definition 2
'''
qr = QuantumRegister(3, 'q')
anc = QuantumRegister(2, 'ancilla')
cr = ClassicalRegister(3, 'c')
circuit = QuantumCircuit(qr, anc, cr)
circuit.h(qr)
circuit.x(qr[1:3])
circuit.barrier()
circuit.x(4)
print(circuit.draw())
draw_circuit(circuit)
'''



### Qline initializations ###

# initialization of a single qubit line
'''
circuit = QuantumCircuit(3)  # Create a quantum circuit with one qubit
initial_state = [0,1]   # Define initial_state as |1>
circuit.initialize(initial_state, 0) # Apply initialisation operation to the 0th qubit
circuit.measure_all()
draw_circuit(circuit)
'''





# initialization to specific values
'''
circuit = QuantumCircuit(1)  # Create a quantum circuit with one qubit
initial_state = [3/5,4/5]   # the sum of amplitudes-squared must equal one
circuit.initialize(initial_state, 0) # Apply initialisation operation to the 0th qubit
circuit.measure_all()
draw_circuit(circuit)  # Let's view our circuit
res = run(circuit,1000)
counts(res)
'''





# initialization to a random normalized value
'''
circuit = QuantumCircuit(4)  # Create a quantum circuit with one qubit
initial_state = random_state(3)
circuit.initialize(initial_state, [0,1,3]) # Apply initialisation operation to the 0th qubit
circuit.measure_all()
draw_circuit(circuit)  # Let's view our circuit
'''





# initialization multiple qubit lines
'''
nqubits = 6
circuit = QuantumCircuit(nqubits)  # Create a quantum circuit with multiple qubits
initial_state = random_state(nqubits)
circuit.initialize(initial_state, range(nqubits)) # Apply initialisation operation to the all qubit lines
circuit.measure_all()
#draw_circuit(circuit)  # Let's view our circuit
draw_circuit_reverse(circuit)  # Let's view our circuit
'''







### Circuit composition ###


# adding external circuit: compose
'''
circuit = QuantumCircuit(4)
circuit.x([0,2])
circuit.barrier()

qc = QuantumCircuit(2) # the two circuit must be compatible
qc.h(0)
qc.x(1)
qc.cx(0,1)

circuit = circuit.compose(qc,[2,3])
circuit.barrier()
circuit = circuit.compose(qc,[0,2])
circuit.barrier()
draw_circuit(circuit)  # Let's view our circuit
'''





# adding external circuit as a gate: to_gate()
'''
circuit = QuantumCircuit(4)
circuit.x([0,2])
#circuit.barrier()

qc = QuantumCircuit(2)
qc.h(0)
qc.x(1)
qc.cx(0,1)

gatec = qc.to_gate()
gatec.name = "Corr"
circuit = circuit.compose(gatec,[2,3])
circuit.barrier()
circuit = circuit.compose(gatec,[0,2])
circuit.barrier()
draw_circuit(circuit)  # Let's view our circuit
print(circuit.draw())
'''





# apply a gate if a classical register has a specific value
'''
reg0 = QuantumRegister(2,"d")
reg1 = ClassicalRegister(1,"r1")
reg2 = ClassicalRegister(1,"r2")
qc = QuantumCircuit(reg0,reg1,reg2)
qc.h([0,1])
qc.measure(0,0)
qc.measure(1,1)
qc.x(0).c_if(reg1,1)
qc.x(0).c_if(reg2,0)
print_circuit(qc)
draw_circuit(qc)
'''




# measuring all qbits
'''
circuit.measure(0,0)
circuit.measure(1,1)
circuit.measure(2,2)
'''


# measuring all qbits
'''
circuit.measure_all()
'''





# Returns counts
'''
qc = QuantumCircuit(2,2)
qc.h([0,1])
qc.measure(0,0)
qc.measure(1,1)
cnt = run(qc,1000)
print_circuit(qc)
counts(cnt)
#print("\nTotal count:",cnt)
'''


    





