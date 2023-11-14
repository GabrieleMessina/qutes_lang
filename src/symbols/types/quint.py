from qutes_parser import QutesParser
from utils.phase import Phase

class Quint():
    def init_from_str(self, literal : str) -> 'Quint':
        literal = literal.removesuffix(QutesParser.literaltostring(QutesParser.QUBIT_LITERAL_POSTFIX))
        self.__init__(int(literal))
        return self

    def init_from_size(self, size : int) -> 'Quint':
        self.__init__()
        self.size = size
        self.binary_value = "0"*size
        return self
    
    def __init__(self, value:int = int()):
        if(value < 0):
            self.phase : Phase = Phase.Negative
            value *= -1
        else:
            self.phase : Phase = Phase.Positive
        self._value : int = value #TODO: remove value and handle with cast
        self.binary_value : str = bin(self._value).removeprefix("0b")
        self.size : int = len(self.binary_value)

    @property
    def value(self):
        return self._value
    @value.setter 
    def value(self, new_value):
        self._value = new_value
        new_binary_value = bin(self._value).removeprefix("0b")
        #if quint was initialized with a size bigger than needed leave the size unaltered and fill with padding
        self.binary_value = new_binary_value if self.size <= len(new_binary_value) else new_binary_value + "0" * (len(new_binary_value) - self.size)
        self.size = len(self.binary_value)

    def get_quantum_state(self) -> str:
        return self.binary_value
    
    def update_size_with_padding(self, new_size : int, padding_value : str = "0") -> 'Quint':
        self.binary_value = self.binary_value + (padding_value*(new_size - self.size)) if self.size <= new_size else self.binary_value[:new_size-1]
        self.size = len(self.binary_value)
        return self
            

    def __to_printable__(self) -> str:
        return f"{self._value}q"

    def __str__(self) -> str:
        return self.__to_printable__()

    def __repr__(self) -> str:
        return self.__to_printable__()