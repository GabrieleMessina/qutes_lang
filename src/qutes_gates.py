from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from symbols.quantum_circuit_handler import QuantumCircuitHandler
from symbols.qutes_types import Qubit, Quint
from utils.QiskitUtils import run, counts

class QutesGates():
    def __init__(self, ciruit_handler : QuantumCircuitHandler):
        self.ciruit_handler = ciruit_handler

    def __full_adder_gate(self):
        # Creating a circuit with 8 quantum bits and 2 classical bits
        circuit = QuantumCircuit(8)

        # AND gate1 implementation
        circuit.ccx(0,1,3)

        # OR gate1 implementation
        circuit.cx(0,4) 
        circuit.cx(1,4)

        # OR gate2 implementation
        circuit.cx(2,5) 
        circuit.cx(4,5)

        # AND gate2 implementation
        circuit.ccx(2,4,6)

        # OR gate implementation
        circuit.x(3)
        circuit.x(6)
        circuit.ccx(3,6,7)
        circuit.x(7)

        gate_add = circuit.to_gate()
        gate_add.name = "full_adder"
        return gate_add

    def sum(self, var_a_name, var_b_name) -> None:
        handler = self.ciruit_handler

        a_qbits = self.ciruit_handler.varname_to_register[var_a_name]
        b_qbits = self.ciruit_handler.varname_to_register[var_b_name]
        number_bits_number = a_qbits.size

        carry = handler.declare_variable("carry", Qubit())
        ancilla = handler.declare_variable("ancilla", Quint().fromsize(5))

        results = ClassicalRegister(number_bits_number+1, "results")
        ainput = ClassicalRegister(number_bits_number, "ainput")
        binput = ClassicalRegister(number_bits_number, "binput")
        handler.classic_registers.append(results)
        handler.classic_registers.append(ainput)
        handler.classic_registers.append(binput)

        handler.push_hadamard_operation(a_qbits)
        handler.push_hadamard_operation(b_qbits)
        
        handler.push_barrier_operation()
        
        for i in range(number_bits_number):
            handler.push_swap_operation(carry, ancilla[4])
            handler.push_reset_operation(ancilla)
            handler.push_compose_circuit_operation(self.__full_adder_gate(), [a_qbits[i], b_qbits[i], carry] + ancilla[:])
            handler.push_measure_operation(ancilla[2], results[i]) # bit a bit sum
            handler.push_barrier_operation()

        handler.push_measure_operation(ancilla[4], results[number_bits_number]) # last carry
        handler.push_measure_operation(a_qbits, ainput)
        handler.push_measure_operation(b_qbits, binput)

    def qiskit_quantum_sum(self, number_bits_number):
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
            qc = qc.compose(self.__full_adder_gate(), [a_qbits[i], b_qbits[i], carry] + ancilla[:])
            qc.measure(ancilla[2], results[i]) # bit a bit sum
            qc.barrier()
        
        qc.measure(ancilla[4], results[number_bits_number]) # last carry
        qc.measure(a_qbits, ainput) # last carry
        qc.measure(b_qbits, binput) # last carry

        print(qc.draw())
        cnt = run(qc,100)
        print("a | b | sum")
        counts(cnt)
        print("\nTotal count:",cnt)
