import numpy as np
import math

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister

class Quint():
    def __init__(self, size:int = 1):
        self.size = size

    def sum(self, other):
        return quantum_sum(self.size, self, other)

def full_adder_gate():
    # Creating a circuit with 8 quantum bits and 2 classical bits
    qc = QuantumCircuit(8)

    # Preparing inputs
    qc.x(0) # Comment this line to make Qbit0 = |0>
    qc.x(1) # Comment this line to make Qbit1 = |0>
    qc.x(2) # Comment this line to make Qbit2 = |0> ( carry-in bit )

    # AND gate1 implementation
    qc.ccx(0,1,3)

    # OR gate1 implementation
    qc.cx(0,4) 
    qc.cx(1,4)

    # OR gate2 implementation
    qc.cx(2,5) 
    qc.cx(4,5)

    # AND gate2 implementation
    qc.ccx(2,4,6)

    # OR gate implementation
    qc.x(3)
    qc.x(6)
    qc.ccx(3,6,7)
    qc.x(7)

    gate_add = qc.to_gate()
    gate_add.name = "full_adder"
    return gate_add

def quantum_sum(number_bits_number, a, b):
    a_qbits = QuantumRegister(number_bits_number, "a_qbits")
    b_qbits = QuantumRegister(number_bits_number, "b_qbits")
    carry = QuantumRegister(1, "carry")
    ancilla = QuantumRegister(5, "ancilla")
    results = ClassicalRegister(number_bits_number+1, "results")
    ainput = ClassicalRegister(number_bits_number, "ainput")
    binput = ClassicalRegister(number_bits_number, "binput")
    # carryinput = ClassicalRegister(1, "carryinput")
    qc = QuantumCircuit(a_qbits, b_qbits, carry, ancilla, results, ainput, binput)
    qc.h(a_qbits)
    qc.h(b_qbits)
    
    qc.barrier()

    for i in range(number_bits_number):
        qc.swap(carry, ancilla[4])
        qc.reset(ancilla)
        qc = qc.compose(full_adder_gate(), [a_qbits[i], b_qbits[i], carry] + ancilla[:])
        qc.measure(ancilla[2], results[i]) # bit a bit sum
        qc.barrier()
    
    qc.measure(ancilla[4], results[number_bits_number]) # last carry
    qc.measure(a_qbits, ainput) # last carry
    qc.measure(b_qbits, binput) # last carry

    print_circuit(qc)
    cnt = run(qc,100)
    print("a | b | sum")
    counts(cnt)
    print("\nTotal count:",cnt)
