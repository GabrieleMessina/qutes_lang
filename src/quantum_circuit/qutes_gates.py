from quantum_circuit.quantum_circuit import QuantumCircuit
from quantum_circuit.classical_register import ClassicalRegister
from quantum_circuit.quantum_circuit_handler import QuantumCircuitHandler
from symbols.types import Qubit, Quint, QutesDataType

class QutesGates():
    def __init__(self, ciruit_handler : QuantumCircuitHandler, variables_handler : 'VariablesHandler'):
        self.ciruit_handler = ciruit_handler
        self.variables_handler = variables_handler
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
    
    def sum(self, var_a_symbol:'Symbol', var_b_symbol:'Symbol') -> 'Symbol':
        self.count+=1
        handler = self.ciruit_handler

        var_a_name = var_a_symbol.name
        var_b_name = var_b_symbol.name
        var_a = var_a_symbol.quantum_register
        var_b = var_b_symbol.quantum_register
        number_bits_number = max(var_a.size, var_b.size)

        if(var_a.size != number_bits_number):
            var_a = self.ciruit_handler.replace_quantum_register(var_a_name, var_a.value.update_size_with_padding(number_bits_number))
        if(var_b.size != number_bits_number):
            var_b = self.ciruit_handler.replace_quantum_register(var_b_name, var_b.value.update_size_with_padding(number_bits_number))

        carry = handler.declare_quantum_register(f"carry{self.count}", Qubit())
        ancilla = handler.declare_quantum_register(f"ancilla{self.count}", Quint.init_from_size(5))
        result_symbol = self.variables_handler.declare_variable(QutesDataType.quint, f"results{self.count}", max(var_a_symbol.ast_token_index, var_b_symbol.ast_token_index), Quint.init_from_size(number_bits_number+1))
        results = result_symbol.quantum_register
        
        # TODO: who calls full adder gate needs to handle the clening of the first 3 qubits, in, out and carry
        # Note that the circuit is not invertible after measuring something seeing that the state collapses.
        for i in range(number_bits_number):
            handler.push_swap_operation(carry, ancilla[4])
            handler.push_reset_operation(ancilla)
            quantum_registers = [var_a[i], var_b[i], carry] + ancilla[:]
            handler.push_compose_circuit_operation(self.__full_adder_gate(), quantum_registers)
            handler.push_cnot_operation(ancilla[2], results[i]) # bit a bit sum 

        handler.push_cnot_operation(ancilla[4], results[number_bits_number]) # last carry

        return result_symbol