from qiskit import QuantumCircuit
import math

def is_power_of_two(n):
    return (n != 0) and (n & (n-1) == 0)

class QutesGates:
    #Rotation gate (not controlled), k=2^p
    @staticmethod
    def left_rot_power_2(n:int, k:int, block_size:int=1):
        n = n*block_size
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
    # @staticmethod
    # def right_rot_generic(n:int, k:int, block_size:int=1):
    #     n = n*block_size
    #     qc = QuantumCircuit(n, name=f'rot_generic_of_{k}')
    #     if(k > 0):
    #         for w in range(k):
    #             for i in range(0, n-1, block_size):
    #                 for j in range(block_size):
    #                     qc.swap((i+j)%n, (i+j+1)%n)
    #     # print(qc.draw(output='text'))
    #     rot_gate = qc.to_gate(label=f'rot_generic_of_{k}')
    #     return rot_gate
    @staticmethod
    def right_rot_generic(num_blocks: int, k: int, block_size: int = 3):
        """
        Rotates 'num_blocks' of size 'block_size' to the right 'k' times.
        Total qubits = num_blocks * block_size.
        """
        total_qubits = num_blocks * block_size
        qc = QuantumCircuit(total_qubits, name=f'block_rot_{k}')

        if k > 0:
            for _ in range(k):
                # To Rotate Right (shift elements 0->1, 1->2, ... last->0):
                # We treat the system as a bubble sort moving the last block to the front.
                
                # Iterate backwards from the last block index down to 1
                for b in range(num_blocks - 1, 0, -1):
                    
                    # Calculate the starting qubit index for the two blocks we are swapping
                    # Left block starts at: (b-1) * size
                    # Right block starts at: b * size
                    start_left = (b - 1) * block_size
                    start_right = b * block_size
                    
                    # Perform the Block Swap
                    # We swap every qubit in the left block with its partner in the right block
                    for j in range(block_size):
                        qc.swap(start_left + j, start_right + j)

        return qc.to_gate(label=f'block_rot_{k}')

    #Controlled Rotation gate
    @staticmethod
    def crot(n:int, k:int, block_size:int=1):
        rot_gate = QutesGates.left_rot(n, k, block_size)
        c_rot_gate = rot_gate.control(1)
        return c_rot_gate
    
    #Right Rotation gate
    @staticmethod
    def right_rot(n:int, k:int, block_size:int=1):
        # rot_gate = QutesGates.identity(n)
        if(is_power_of_two(n)):
            if(is_power_of_two(k)):
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
        # rot_gate = QutesGates.identity(n)
        if(is_power_of_two(n)):
            if(is_power_of_two(k)):
                rot_gate = QutesGates.left_rot_power_2(n, k, block_size)
            else:
                # TODO: if k is not power of 2, but n is, then we need to compose multiple left_rot_power_2
                rot_gate = QutesGates.right_rot_generic(n, k, block_size).inverse()
        else:
            rot_gate = QutesGates.right_rot_generic(n, k, block_size).inverse()
        return rot_gate
    