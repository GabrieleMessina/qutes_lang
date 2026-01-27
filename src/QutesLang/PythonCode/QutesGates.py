from qiskit import QuantumCircuit, QuantumRegister
import math
from qiskit.circuit.library import QFT


def is_power_of_two(n):
    return (n != 0) and (n & (n - 1) == 0)


class QutesGates:
    # Rotation gate (not controlled), k=2^p
    @staticmethod
    def left_rot_power_2(n: int, k: int, block_size: int = 1):
        n = n * block_size
        qc = QuantumCircuit(n, name=f"rot_power_2_of_{k}")
        if k > 0:
            stop = int(math.log2(n)) - int(math.log2(k * block_size)) + 2
            for i in range(block_size, stop):
                for j in range(0, int(n / (k * (2**i)))):
                    for x in range(j * k * (2**i), k * ((j * 2**i + 1))):
                        for offset in range(block_size):
                            inizio_swap = x + k * offset
                            fine_swap = x + 2 ** (i - 1) * k + k * offset
                            qc.swap(inizio_swap, fine_swap)
        # print(qc.draw(output='text'))
        rot_gate = qc.to_gate(label=f"rot_power_2_of_{k}")
        return rot_gate

    # Rotation gate (not controlled), k=any
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
        qc = QuantumCircuit(total_qubits, name=f"block_rot_{k}")

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

        return qc.to_gate(label=f"block_rot_{k}")

    # Controlled Rotation gate
    @staticmethod
    def crot(n: int, k: int, block_size: int = 1):
        rot_gate = QutesGates.left_rot(n, k, block_size)
        c_rot_gate = rot_gate.control(1)
        return c_rot_gate

    # Right Rotation gate
    @staticmethod
    def right_rot(n: int, k: int, block_size: int = 1):
        # rot_gate = QutesGates.identity(n)
        if is_power_of_two(n):
            if is_power_of_two(k):
                rot_gate = QutesGates.left_rot_power_2(n, k, block_size).inverse()
            else:
                # TODO: if k is not power of 2, but n is, then we need to compose multiple left_rot_power_2
                rot_gate = QutesGates.right_rot_generic(n, k, block_size)
        else:
            rot_gate = QutesGates.right_rot_generic(n, k, block_size)
        return rot_gate

    # Left Rotation gate
    @staticmethod
    def left_rot(n: int, k: int, block_size: int = 1):
        # rot_gate = QutesGates.identity(n)
        if is_power_of_two(n):
            if is_power_of_two(k):
                rot_gate = QutesGates.left_rot_power_2(n, k, block_size)
            else:
                # TODO: if k is not power of 2, but n is, then we need to compose multiple left_rot_power_2
                rot_gate = QutesGates.right_rot_generic(n, k, block_size).inverse()
        else:
            rot_gate = QutesGates.right_rot_generic(n, k, block_size).inverse()
        return rot_gate

    @staticmethod
    def qft_unitary_increment(n: int):
        CIRCUIT_NAME = "QFT +1 increment"
        qc = QuantumCircuit(n, name=CIRCUIT_NAME)

        N = 1 << (n - 1)  # 2^(n-1)

        qc.append(QFT(n), range(n))

        for i in range(n):
            qc.p(pow(2, i) * math.pi / N, i)

        qc.append(QFT(n, inverse=True), range(n))
        return qc.to_gate(label=CIRCUIT_NAME)

    @staticmethod
    def carry_look_ahead_increment(n: int):
        """
        Generates a Quantum Gate that performs the increment operation (Input + 1)
        using a Quantum Carry Look-Ahead (QCLA) architecture.

        Args:
            n (int): Number of qubits in the input register. Must be a power of 2.

        Returns:
            Gate: A composite Qiskit Gate acting on (a_reg, s_reg, tree_reg).
                - a_reg (n): Input
                - s_reg (n): Output (Sum)
                - tree_reg (n - log2(n) - 1): Ancilla for intermediate tree nodes
        """
        # Verify that n is a power of 2
        if n < 2 or (n & (n - 1)) != 0:
            raise ValueError("The length (n) must be a power of 2.")

        # 1. Configure Registers
        # Tree register size: Total internal nodes - Nodes that are powers of 2 (which go into s_reg)
        # A complete binary tree has N-1 internal nodes. Log2(N) are pure prefixes.
        num_tree_qubits = n - int(math.log2(n)) - 1

        a_reg = QuantumRegister(n, "a_in")  # Input bits
        s_reg = QuantumRegister(n, "s_out")  # Sum/Carry bits
        tree_reg = QuantumRegister(
            num_tree_qubits, "tree_anc"
        )  # Ancilla for intermediate nodes

        CIRCUIT_NAME = f"QCLA_+1_increment"
        qc = QuantumCircuit(a_reg, s_reg, tree_reg, name=CIRCUIT_NAME)

        # Dictionary to track where tree nodes are stored
        # Key: (start_index, end_index) -> Value: Qubit
        nodes_map = {}

        # Stack to store tree operations for uncomputation
        # Format: (control1, control2, target)
        tree_computation_history = []

        # --- PHASE 0: Initialization ---
        # Initialize the leaves of the node map with input qubits
        for i in range(n):
            nodes_map[(i, i)] = a_reg[i]

        # --- PHASE 1: Build Product Tree (Logarithmic Prefix Tree) ---
        # This populates s_reg with carries that are powers of 2 and tree_reg with partial products
        levels = int(math.log2(n))
        tree_idx = 0  # Iterator for tree qubits

        for lev in range(levels):
            step = 2 ** (lev + 1)
            half_step = 2**lev

            for i in range(0, n, step):
                # Define ranges for children and current node
                left_range = (i, i + half_step - 1)
                right_range = (i + half_step, i + step - 1)
                current_range = (i, i + step - 1)

                # Retrieve children qubits
                q_left = nodes_map[left_range]
                q_right = nodes_map[right_range]

                # Determine target qubit
                # If it starts at 0, it is a pure prefix -> goes into s_reg (it acts as Carry C_{2^k})
                if i == 0:
                    # Note: C_2 goes into s_reg[2], C_4 into s_reg[4]...
                    # s_reg[k] represents the carry input to bit k.
                    # The node covering [0...k-1] is the carry for k.
                    target_idx = i + step
                    if target_idx < n:
                        q_target = s_reg[target_idx]
                    else:
                        # Last carry out (overflow), not mapped for internal modulo calculation
                        continue
                else:
                    # Intermediate node -> goes into tree_reg
                    q_target = tree_reg[tree_idx]
                    tree_idx += 1

                # Execute gate and save to map and history
                qc.ccx(q_left, q_right, q_target)
                nodes_map[current_range] = q_target
                tree_computation_history.append((q_left, q_right, q_target))

        # --- PHASE 2: Compute Missing Carries (Filling the gaps) ---
        # Calculate C_i for all i that are not powers of 2.
        # Uses LSB logic: C_i = C_prev * Node(prev...i-1)

        # C_0 = 1 (Carry In for the +1 increment operation)
        qc.x(s_reg[0])

        # C_1 = a_0 AND C_0. Since C_0 is 1, C_1 = a_0
        qc.cx(a_reg[0], s_reg[1])

        for i in range(3, n):
            # If i is a power of 2, it was already computed in the tree phase
            if (i & (i - 1)) == 0:
                continue

            # 1. Find LSB and previous index
            # Example: i=13 (1101), lsb=1, prev=12
            lsb = i & (-i)
            prev_idx = i - lsb

            # 2. Retrieve operand qubits
            # prev_carry is C_{prev_idx}, found in s_reg[prev_idx]
            q_prev_carry = s_reg[prev_idx]

            # The node covering the gap [prev_idx ... i-1]
            q_gap_node = nodes_map[(prev_idx, i - 1)]

            # Target is the current carry
            q_target = s_reg[i]

            # 3. Compute C_i
            qc.ccx(q_prev_carry, q_gap_node, q_target)

        # --- PHASE 3: Uncompute Tree Ancillas ---
        # Reverse tree operations to clean tree_reg.
        # Crucial for reversible quantum computation.
        # IMPORTANT: Done BEFORE the final sum (XOR), because sums dirty s_reg.
        # However, s_reg currently contains valid CARRIES. We must not uncompute those.
        for c1, c2, target in reversed(tree_computation_history):
            if target._register.name != "s_out":
                # uncompute only if target is in tree_reg
                qc.ccx(c1, c2, target)

        # --- PHASE 4: Compute Final Sums ---
        # S_i = C_i XOR A_i. (Note: Here C_i is in s_reg, A_i in a_reg)
        # After this operation, s_reg will contain the Sums S_i.
        for i in range(n):
            qc.cx(a_reg[i], s_reg[i])

        # Convert to Gate
        increment_gate = qc.to_gate(label=CIRCUIT_NAME)

        return increment_gate

    @staticmethod
    def twos_complement(n: int):
        CIRCUIT_NAME = "complement_2"
        qc = QuantumCircuit(n, name=CIRCUIT_NAME)

        # Step 1: Bitwise NOT
        for i in range(n):
            qc.x(i)

        # Add 1 using QFT +1 increment
        # TODO: choose the best way to add 1 dinamically
        qft_increment_gate = QutesGates.qft_unitary_increment(n)
        qc.append(qft_increment_gate, range(n))

        return qc.to_gate(label=CIRCUIT_NAME)
