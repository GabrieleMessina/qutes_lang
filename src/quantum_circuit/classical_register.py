from qiskit import ClassicalRegister as cr

class ClassicalRegister(cr):
    measured_values:list = None
    measured_counts:list = None