from grammar_frontend.shared.qutes_parser import QutesParser
from symbols.types import Qubit, QuantumType
from qiskit.quantum_info import Statevector
from quantum_circuit.state_preparation import StatePreparation
import utils 

class Quint(QuantumType['Quint']):
    size_in_qubit = 4
    __state_vector_single_value = [complex(0)]
    __state_vector_size = 2 ** (size_in_qubit)
    
    def __init__(self, qubits:StatePreparation = None):
        super().__init__(Quint, Quint.size_in_qubit)
        self.size:int = Quint.size_in_qubit
        if qubits is None:
            state = Quint.__state_vector_single_value * Quint.__state_vector_size
            state[0] = complex(1)
            qubits = StatePreparation(state)
        if(qubits.num_qubits != Quint.size_in_qubit):
            qubits.params.extend(Quint.__state_vector_single_value * (Quint.__state_vector_size - 2 ** qubits.num_qubits))
            qubits = StatePreparation(qubits.params)
        self.qubit_state:StatePreparation = qubits

    @staticmethod
    def get_default_value():
        return Quint(None)

    @staticmethod
    def get_default_superposition_value():
        return Quint(StatePreparation([complex(1)] * Quint.__state_vector_size))

    @staticmethod
    def get_default_size_in_qubit():
        return Quint.size_in_qubit

    @staticmethod
    def init_from_string(literal : str) -> 'Quint':
        init_state = StatePreparation(Quint.__state_vector_single_value * Quint.__state_vector_size)
        qubit_literal_postfix = QutesParser.literal_to_string(QutesParser.QUBIT_LITERAL_POSTFIX)
        literal = literal.removesuffix(qubit_literal_postfix)
        if(literal.startswith(QutesParser.literal_to_string(QutesParser.SQUARE_PARENTHESIS_OPEN))):
            literal = literal.removesuffix(QutesParser.literal_to_string(QutesParser.SQUARE_PARENTHESIS_CLOSE))
            literal = literal.removeprefix(QutesParser.literal_to_string(QutesParser.SQUARE_PARENTHESIS_OPEN))
            quint_literals = literal.replace(' ', '').split(qubit_literal_postfix)
            #we have an array of integer that this quint can take on
            if(len(quint_literals) == 1):
                int_literals = [int(i) for i in quint_literals[0].replace(' ', '').split(',')]
                max_value_to_represent = max(int_literals)
                number_of_qubits = len(utils.binary(max_value_to_represent))
                counts = [0] * (2**number_of_qubits)

                for integer in int_literals:
                    two_comp_value = int(utils.int_to_twos_comp(integer, number_of_qubits), 2)
                    counts[two_comp_value] += 1
                init_state = StatePreparation(counts)
            #we have an array of qubits that indicates the single qubits state the quint can take on
            else: 
                init_state = None
                for qubit_literal in quint_literals:
                    if(len(qubit_literal)>0):
                        bit_init_state = Statevector(Qubit.from_string(qubit_literal.removeprefix(',') + qubit_literal_postfix).qubit_state)
                        if(init_state == None):
                            init_state = bit_init_state
                        else:
                            init_state = init_state.tensor(bit_init_state)
                init_state = StatePreparation(init_state)
        #we have a simple integer that the quint can take on
        else:
            return Quint.init_from_integer(int(literal))
        return Quint(init_state)

    @staticmethod
    def init_from_integer(literal : int | bool) -> 'Quint':
        bitstring = utils.int_to_twos_comp(literal, Quint.size_in_qubit)
        state_vector_index = int(bitstring, 2)
        state_vector = Quint.__state_vector_single_value * Quint.__state_vector_size
        state_vector[state_vector_index] = complex(1)
        return Quint(StatePreparation(state_vector))
    @staticmethod
    def fromValue(var_value : any) -> 'Quint':
        try:
            if(isinstance(var_value, Qubit)):
                return Quint(var_value.qubit_state)
            if(isinstance(var_value, str)):
                return Quint.init_from_string(var_value)
            if(isinstance(var_value, int)):
                return Quint.init_from_integer(var_value)
            if(isinstance(var_value, bool)):
                return Quint.init_from_integer(var_value)
            if(isinstance(var_value, list)):
                return Quint.init_from_integer(int("".join([str(int(i)) for i in var_value]), 2))
            raise TypeError(f"Cannot convert {type(var_value)} to quint.")
        except Exception as e:
            raise TypeError(f"Cannot convert {type(var_value)} to quint: {e}.")

    def to_classical_type(self) -> int:
        bin_number = str.join("", [str(value) for value in self.qubit_state.params])
        return int(bin_number, 2)
    
    def __to_printable__(self) -> str:
        return f"{self.qubit_state}"