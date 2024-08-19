from grammar_frontend.qutes_parser import QutesParser
from symbols.types import Qubit, QuantumType
from qiskit.quantum_info import Statevector
from quantum_circuit.state_preparation import StatePreparation
import utils 

class Quint(QuantumType['Quint']):
    def __init__(self, qubits:StatePreparation = StatePreparation("0")):
        super().__init__(Quint)
        self.qubit_state:StatePreparation = qubits
        self.size:int = len(self.qubit_state)

    def get_default_value():
        return "0"
    
    def get_default_superposition_value():
        return "+"
    
    def get_default_size_in_qubit():
        return 1

    def init_from_string(literal : str) -> 'Quint':
        init_state = StatePreparation("0")
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
                    counts[integer] += 1

                #Create a binary string from counts
                counts_str = ""
                for count in counts:
                    counts_str += str(count)
                init_state = StatePreparation(counts_str)
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
    
    def init_from_integer(literal : int | bool, initial_size:int = -1) -> 'Quint':
        binary_rapresentation = utils.binary(literal)
        if(initial_size != -1 and len(binary_rapresentation) < initial_size):
            binary_rapresentation += "0"*(initial_size - len(binary_rapresentation))
        return Quint(StatePreparation(binary_rapresentation))

    def init_from_size(number_of_bits : int, init_in_superposition:bool = False) -> 'Quint':
        template = Quint.get_default_superposition_value() if init_in_superposition else Quint.get_default_value()
        return Quint(StatePreparation(template*number_of_bits))
    
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
            
    def update_size_with_padding(self, new_size : int) -> 'Quint':
        #TODO: qubit state is not reliable, we should add the qubit needed to expand the quint directly into the circuit.
        if (self.size < new_size):
            old_state = self.qubit_state
            new_state = Statevector(old_state).expand(Statevector(Quint.get_default_value()*(new_size - self.size)))
            return Quint(new_state)
        return self

    def to_classical_type(self) -> int:
        bin_number = str.join("", [str(value) for value in self.qubit_state.params])
        return int(bin_number, 2)
    
    def __to_printable__(self) -> str:
        return f"{self.qubit_state}"