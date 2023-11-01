import numpy as np
import math

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister

class Quint():
    def __init__(self, size:int = 1):
        self.size = size

    def sum(self, other):
        return quantum_sum(self.size, self, other)


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
