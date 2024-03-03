from quantum_circuit.quantum_circuit import QuantumCircuit
from quantum_circuit.quantum_register import QuantumRegister
from quantum_circuit.classical_register import ClassicalRegister
from quantum_circuit.quantum_circuit_handler import QuantumCircuitHandler
from symbols.types import Qubit, Quint, Qustring, QutesDataType
from qiskit.circuit.library import GroverOperator
import math

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
    

    def ESM_Search(self,x,y):
        n = len(y)
        m = len(x)
        logn = int(math.log2(n))

        kr = QuantumRegister(logn, 'k', None)
        xr = QuantumRegister(m, 'x', None)
        yr = QuantumRegister(n, 'y', None)
        out = QuantumRegister(1, 'out', None)
        cr = ClassicalRegister(logn,'c')
        # cr = ClassicalRegister(1,'c')
        qc = QuantumCircuit(kr, xr,yr,out, cr)

        qc.h(kr)
        qc.x(out)
        qc.h(out)

        oracle = self.ESM_Oracle(x, y)
        grover_op = GroverOperator(oracle)

        n_results = 1
        n_iteration = math.floor(
            math.pi / (4 * math.asin(math.sqrt(n_results / 2**grover_op.num_qubits)))
        )
        print(f"Grover iterations: {n_iteration}")

        qc.compose(grover_op.power(n_iteration), inplace=True)

        qc.measure(out,cr)
        #qc.measure(kr,cr)
        self.ciruit_handler.print_circuit(grover_op.decompose())
        self.ciruit_handler.print_circuit(qc)
        res = self.ciruit_handler.__run__(qc,1000)
        self.ciruit_handler.__revcounts__(res)

    def Create_ESM_Oracle(self,len_array, to_match:Qustring):
        n = len_array
        m = len(to_match.qubit_state)
        logn = int(math.log2(n))

        kr = QuantumRegister(logn, 'k', None)
        xr = QuantumRegister(m, 'x', None)
        yr = QuantumRegister(n, 'y', None)
        out = QuantumRegister(1, 'out', None)
        #cr = ClassicalRegister(1,'c')
        qc = QuantumCircuit(kr,xr,yr,out)

        # initialize to_match
        for i in range(m):
            if (to_match.qubit_state[i].alpha == 0 and to_match.qubit_state[i].beta == 1):
                qc.x(xr[i])

        # rotate y
        for i in range(logn):
            qc = qc.compose(QutesGates.crot(n,2**i,1), [kr[i]]+yr[:] )
        # compare x and y[:m]
        for i in range(m):
            qc.cx(xr[i],yr[i])
            qc.x(yr[i])
        uncompute = qc.reverse_ops()
        qc.mcx(yr[:m],out)

        #uncompute
        # qc.compose(uncompute, inplace=True)
        for i in range(m):
            qc.x(yr[i])
            qc.cx(xr[i],yr[i])
        for i in range(logn):
            qc = qc.compose(QutesGates.crot(n,2**i,1).inverse(), [kr[i]]+yr[:] )        

        #qc.measure(out,cr)
        #self.ciruit_handler.print_circuit(qc)
        #res = self.ciruit_handler.__run__(qc,1000)
        #self.ciruit_handler.__revcounts__(res)
        #qc = qc.to_gate(label='ESM')
        return qc

    # performs exact string matching
    # checkf if x (length m) rotated by k pos. is equal to y[0..m-1]
    def ESM_Oracle(self,x,y):
        n = len(y)
        m = len(x)
        logn = int(math.log2(n))

        kr = QuantumRegister(logn, 'k', None)
        xr = QuantumRegister(m, 'x', None)
        yr = QuantumRegister(n, 'y', None)
        out = QuantumRegister(1, 'out', None)
        #cr = ClassicalRegister(1,'c')
        qc = QuantumCircuit(kr, xr,yr,out)

        # qc.h(kr)

        #if(k>=0):
        #    kbin = bin(k)[2:][::-1]
        #    for i in range(len(kbin)):
        #        if kbin[i]=='1':
        #            qc.x(kr[i])
        
        # initialize x
        for i in range(m):
            if x[i]=='1':
                qc.x(xr[i])
        # initialize y
        for i in range(n):
            if y[i]=='1':
                qc.x(yr[i])
        # rotate y
        for i in range(logn):
            qc = qc.compose(QutesGates.crot(n,2**i,1), [kr[i]]+yr[:] )
        # compare x and y[:m]
        for i in range(m):
            qc.cx(xr[i],yr[i])
            qc.x(yr[i])
        uncompute = qc.reverse_ops()
        qc.mcx(yr[:m],out)

        #uncompute
        # qc.compose(uncompute, inplace=True)
        for i in range(m):
            qc.x(yr[i])
            qc.cx(xr[i],yr[i])
        for i in range(logn):
            qc = qc.compose(QutesGates.crot(n,2**i,1).inverse(), [kr[i]]+yr[:] )        
        for i in range(m):
            if x[i]=='1':
                qc.x(xr[i])
        for i in range(n):
            if y[i]=='1':
                qc.x(yr[i])
        #qc.measure(out,cr)
        #self.ciruit_handler.print_circuit(qc)
        #res = self.ciruit_handler.__run__(qc,1000)
        #self.ciruit_handler.__revcounts__(res)
        #qc = qc.to_gate(label='ESM')
        return qc
    
    #Rotation gate (not controlled), k=2^p 
    def rot(n, k, block_size=1):
        qc = QuantumCircuit(n, name=f'rot_k={k}')
        stop = (int(math.log2(n)) - int(math.log2(k*block_size)) + 2)
        for i in range(block_size, stop):
            for j in range(0, int(n/(k*(2**i)))):
                for x in range(j*k*(2**i), k*((j*2**i+1))):
                    for offset in range(block_size):
                        inizio_swap = x + k*offset
                        fine_swap = x + 2**(i-1)*k + k*offset
                        qc.swap(inizio_swap, fine_swap)
                
        #qkt.draw_circuit(qc)             
        rot_gate = qc.to_gate(label='Rot_'+str(k))
        return rot_gate  

    #Controlled Rotation gate 
    def crot(n, k, block_size=1):
        # Creiamo il gate di rotazione come prima
        rot_gate = QutesGates.rot(n, k, block_size)
        # Aggiungiamo un qubit di controllo al gate per renderlo controllato
        c_rot_gate = rot_gate.control(1)
        return c_rot_gate
    