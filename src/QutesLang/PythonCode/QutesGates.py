from qiskit import QuantumCircuit, QuantumRegister
import math

def is_power_of_two(n):
    return (n != 0) and (n & (n-1) == 0)

class QutesGates:
    @staticmethod
    def left_rot_power_2(n:int, k:int, block_size:int=1):
        """
        Left rotation by k element-positions using a butterfly swap network.
        Requires both (n * block_size) and k to be powers of 2.
        """
        n = n*block_size
        assert k == 0 or is_power_of_two(k), f"k={k} must be a power of 2"
        assert n == 0 or is_power_of_two(n), f"Total qubit count n*block_size={n} must be a power of 2"
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
        rot_gate = qc.to_gate(label=f'rot_power_2_of_{k}')
        return rot_gate  
    
    @staticmethod
    def left_rot_generic(num_blocks: int, k: int, block_size: int = 3):
        """
        Rotates 'num_blocks' of size 'block_size' to the left 'k' times.
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

        rot_gate = qc.to_gate(label=f'block_rot_{k}')
        return rot_gate

    @staticmethod
    def crot(n:int, k:int, block_size:int=1):
        rot_gate = QutesGates.left_rot(n, k, block_size)
        c_rot_gate = rot_gate.control(1)
        return c_rot_gate
    
    @staticmethod
    def right_rot(n:int, k:int, block_size:int=1):
        if(is_power_of_two(n * block_size)):
            rot_gate = QutesGates._compose_left_rot_power_2(n, k, block_size).inverse()
        else:
            rot_gate = QutesGates.left_rot_generic(n, k, block_size).inverse()
        return rot_gate
    
    @staticmethod
    def left_rot(n:int, k:int, block_size:int=1):
        if(is_power_of_two(n * block_size)):
            rot_gate = QutesGates._compose_left_rot_power_2(n, k, block_size)
        else:
            rot_gate = QutesGates.left_rot_generic(n, k, block_size)
        return rot_gate

    @staticmethod
    def _compose_left_rot_power_2(n:int, k:int, block_size:int=1):
        """Decomposes k into powers of 2 and composes multiple left_rot_power_2 gates."""
        total_qubits = n * block_size
        qc = QuantumCircuit(total_qubits, name=f'composed_rot_{k}')
        bit = 0
        remaining = k
        while remaining > 0:
            if remaining & 1:
                gate = QutesGates.left_rot_power_2(n, 2**bit, block_size)
                qc.append(gate, range(total_qubits))
            remaining >>= 1
            bit += 1
        return qc.to_gate(label=f'block_rot_power_2_{k}')

    @staticmethod
    def greater_than(d):
        xr = QuantumRegister(d,'x')
        yr = QuantumRegister(d,'y')
        out = QuantumRegister(1,'out')
        qc = QuantumCircuit(xr,yr,out)
        for idx in range(d):
            i = d - 1 - idx #Suppose LSB ordering
            qc.x(yr[i])
            qc.mcx([xr[i]]+list(yr[i:]), out)
            qc.x(yr[i])
            if(idx<d-1):
                qc.cx(xr[i],yr[i])
                qc.x(yr[i])
        for idx in range(d-1):
            j = idx + 1
            qc.x(yr[j])
            qc.cx(xr[j],yr[j])
        qc = qc.to_gate(label='>')
        return qc

    @staticmethod
    def less_than(d):
        xr = QuantumRegister(d,'x')
        yr = QuantumRegister(d,'y')
        out = QuantumRegister(1,'out')
        qc = QuantumCircuit(xr,yr,out)
        gt = QutesGates.greater_than(d)
        qc.append(gt, [*yr, *xr, out[0]])  # x < y <==> y > x
        qc = qc.to_gate(label='<')
        return qc

    @staticmethod
    def greater_equal(d):
        xr = QuantumRegister(d,'x')
        yr = QuantumRegister(d,'y')
        out = QuantumRegister(1,'out')
        qc = QuantumCircuit(xr,yr,out)
        lt = QutesGates.less_than(d)
        qc.append(lt, [*xr, *yr, out[0]])  # compute x < y
        qc.x(out)  # x >= y <==> NOT(x < y)
        qc = qc.to_gate(label='>=')
        return qc

    @staticmethod
    def less_equal(d):
        xr = QuantumRegister(d,'x')
        yr = QuantumRegister(d,'y')
        out = QuantumRegister(1,'out')
        qc = QuantumCircuit(xr,yr,out)
        gt = QutesGates.greater_than(d)
        qc.append(gt, [*xr, *yr, out[0]])  # compute x > y
        qc.x(out)  # x <= y <==> NOT(x > y)
        qc = qc.to_gate(label='<=')
        return qc
    