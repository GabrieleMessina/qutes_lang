from quantum_circuit.quantum_circuit import QuantumCircuit
from quantum_circuit.quantum_register import QuantumRegister
from quantum_circuit.classical_register import ClassicalRegister
from quantum_circuit.quantum_circuit_handler import QuantumCircuitHandler
from symbols.types import Qubit, Quint, Qustring, QutesDataType
from qiskit.circuit.library import GroverOperator
import math, utils

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
        #TODO: this should be a push_sum_operation in circuit handler?
        self.count+=1
        handler = self.ciruit_handler

        var_a_name = var_a_symbol.name
        var_b_name = var_b_symbol.name
        var_a = var_a_symbol.quantum_register
        var_b = var_b_symbol.quantum_register
        number_bits_number = max(var_a.size, var_b.size)

        if(var_a.size != number_bits_number):
            var_a = self.ciruit_handler.create_and_assign_quantum_register(var_a_name, var_a.value.update_size_with_padding(number_bits_number))
        if(var_b.size != number_bits_number):
            var_b = self.ciruit_handler.create_and_assign_quantum_register(var_b_name, var_b.value.update_size_with_padding(number_bits_number))

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
    
    #Rotation gate (not controlled), k=2^p 
    def left_rot_power_2(n, k, block_size=1):
        qc = QuantumCircuit(n, name=f'rot_power_2_of_{k}')
        if(k > 0):
            stop = (int(math.log2(n)) - int(math.log2(k*block_size)) + 2)
            for i in range(block_size, stop):
                for j in range(0, int(n/(k*(2**i)))):
                    for x in range(j*k*(2**i), k*((j*2**i+1))):
                        for offset in range(block_size):
                            inizio_swap = x + k*offset
                            fine_swap = x + 2**(i-1)*k + k*offset
                            qc.swap(inizio_swap, fine_swap)
        # print(qc.draw(output='text'))
        rot_gate = qc.to_gate(label=f'rot_power_2_of_{k}')
        return rot_gate  
    
    #Rotation gate (not controlled), k=any
    def right_rot_generic(n, k, block_size=1):
        qc = QuantumCircuit(n, name=f'rot_generic_of_{k}')
        if(k > 0):
            for w in range(k):
                for i in range(0, n-1, block_size):
                    for j in range(block_size):
                        qc.swap((i+j)%n, (i+j+1)%n)
        # print(qc.draw(output='text'))
        rot_gate = qc.to_gate(label=f'rot_generic_of_{k}')
        return rot_gate  

    #Controlled Rotation gate 
    def crot(n, k, block_size=1):
        rot_gate = QutesGates.left_rot(n, k, block_size)
        c_rot_gate = rot_gate.control(1)
        return c_rot_gate
    
    #Right Rotation gate 
    def right_rot(n, k, block_size=1):
        rot_gate = QutesGates.identity(n)
        if(utils.is_power_of_two(n)):
            if(utils.is_power_of_two(k)):
                rot_gate = QutesGates.left_rot_power_2(n, k, block_size).inverse()
            else:
                # TODO: if k is not power of 2, but n is, then we need to compose multiple left_rot_power_2
                rot_gate = QutesGates.right_rot_generic(n, k, block_size) 
        else:
            rot_gate = QutesGates.right_rot_generic(n, k, block_size)
        return rot_gate
    
    #Left Rotation gate 
    def left_rot(n, k, block_size=1):
        rot_gate = QutesGates.identity(n)
        if(utils.is_power_of_two(n)):
            if(utils.is_power_of_two(k)):
                rot_gate = QutesGates.left_rot_power_2(n, k, block_size)
            else:
                # TODO: if k is not power of 2, but n is, then we need to compose multiple left_rot_power_2
                rot_gate = QutesGates.right_rot_generic(n, k, block_size).inverse()
        else:
            rot_gate = QutesGates.right_rot_generic(n, k, block_size).inverse()
        return rot_gate
    
    def identity(n):
        return QuantumCircuit(n, name=f'identity_{n}').to_gate(label=f'identity_{n}')
    