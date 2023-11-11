from symbols.quantum_circuit_handler import QuantumCircuit, QuantumRegister, ClassicalRegister
from symbols.quantum_circuit_handler import QuantumCircuitHandler
from symbols.qutes_types import Qubit, Quint

class QutesGates():
    def __init__(self, ciruit_handler : QuantumCircuitHandler):
        self.ciruit_handler = ciruit_handler
        self.count = int()

    def __full_adder_gate(self):
        # Creating a circuit with 8 quantum bits
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
        self.count+=1
        handler = self.ciruit_handler

        var_a = self.ciruit_handler._varname_to_register[var_a_name]
        var_b = self.ciruit_handler._varname_to_register[var_b_name]
        number_bits_number = max(var_a.size, var_b.size)

        if(var_a.size != number_bits_number):
            var_a = self.ciruit_handler.replace_quantum_register(var_a_name, var_a.value.update_size_with_padding(number_bits_number))
        if(var_b.size != number_bits_number):
            var_b = self.ciruit_handler.replace_quantum_register(var_b_name, var_b.value.update_size_with_padding(number_bits_number))

        carry = handler.declare_quantum_register(f"carry{self.count}", Qubit())
        ancilla = handler.declare_quantum_register(f"ancilla{self.count}", Quint().init_from_size(5))

        results = ClassicalRegister(number_bits_number+1, f"results{self.count}")
        ainput = ClassicalRegister(number_bits_number, f"ainput{self.count}")
        binput = ClassicalRegister(number_bits_number, f"binput{self.count}")
        handler._classic_registers.append(results)
        handler._classic_registers.append(ainput)
        handler._classic_registers.append(binput)
        
        for i in range(number_bits_number):
            handler.push_swap_operation(carry, ancilla[4])
            handler.push_reset_operation(ancilla)
            handler.push_compose_circuit_operation(self.__full_adder_gate(), [var_a[i], var_b[i], carry] + ancilla[:])
            handler.push_measure_operation(ancilla[2], results[i]) # bit a bit sum

        handler.push_measure_operation(ancilla[4], results[number_bits_number]) # last carry
        handler.push_measure_operation(var_a, ainput)
        handler.push_measure_operation(var_b, binput)