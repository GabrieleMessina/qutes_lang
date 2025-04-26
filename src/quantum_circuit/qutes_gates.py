from quantum_circuit.quantum_circuit import QuantumCircuit
import math, utils

class QutesGates:
    #Rotation gate (not controlled), k=2^p
    @staticmethod
    def left_rot_power_2(n:int, k:int, block_size:int=1):
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
    @staticmethod
    def right_rot_generic(n:int, k:int, block_size:int=1):
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
    @staticmethod
    def crot(n:int, k:int, block_size:int=1):
        rot_gate = QutesGates.left_rot(n, k, block_size)
        c_rot_gate = rot_gate.control(1)
        return c_rot_gate
    
    #Right Rotation gate
    @staticmethod
    def right_rot(n:int, k:int, block_size:int=1):
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
    @staticmethod
    def left_rot(n:int, k:int, block_size:int=1):
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

    @staticmethod
    def identity(n:int):
        return QuantumCircuit(n, name=f'identity_{n}').to_gate(label=f'identity_{n}')
    