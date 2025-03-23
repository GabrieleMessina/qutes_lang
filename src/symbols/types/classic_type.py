from typing import TypeVar, Type
from symbols.types.qutes_type import QutesType
T = TypeVar("T")

class ClassicType(QutesType[T]):
    def __init__(self, t_type: Type[T], value: T):
        super().__init__(t_type)
        self.value = value

    @staticmethod
    def get_default_value():
        raise NotImplementedError("get_default_value method must be implemented in derived class")

    def __to_printable__(self) -> str:
        return self.value.__str__()

    def __str__(self) -> str:
        return f"{self.__to_printable__()}"

    def __float__(self):
        return float(self.value)

    def __int__(self):
        return int(self.value)

    def __bool__(self):
        return bool(self.value)

    def __repr__(self) -> str:
        return f"Qutes.{self.__class__.__qualname__}:{self.__to_printable__()}"

    def __or__(self, other):
        return Bool(self.value or other.value)

    def __and__(self, other):
        return Bool(self.value and other.value)

    def __xor__(self, other):
        return Bool(self.value ^ other.value)

    def __lt__(self, other):
        return Bool(self.value < other.value)

    def __le__(self, other):
        return Bool(self.value <= other.value)

    def __eq__(self, other):
        return Bool(self.value == other.value)

    def __ne__(self, other):
        return Bool(self.value != other.value)

    def __gt__(self, other):
        return Bool(self.value > other.value)

    def __ge__(self, other):
        return Bool(self.value >= other.value)

class Bool(ClassicType['bool']):
    def __init__(self, py_value: bool | str):
        literal = str(py_value)
        value = literal.lower() == "true" or literal.lower() == "1"
        super().__init__(Bool, value)

    def __invert__(self):
        return Bool(~self.value)

    def __lshift__(self, other):
        return Bool(self.value << other.value)

    def __rshift__(self, other):
        return Bool(self.value >> other.value)

    def __add__(self, other):
        return Bool(self.value + other.value)

    def __sub__(self, other):
        return Bool(self.value - other.value)

    def __mul__(self, other):
        return Bool(self.value * other.value)

    def __truediv__(self, other):
        return Bool(self.value / other.value)

    def __floordiv__(self, other):
        return Bool(self.value // other.value)

    def __mod__(self, other):
        return Bool(self.value % other.value)

    def __pow__(self, other):
        return Bool(self.value ** other.value)

class Int(ClassicType['int']):
    def __init__(self, py_value:int | str):
        literal = str(py_value)
        value = int(literal)
        super().__init__(Int, value)

    def __invert__(self):
        return Int(~self.value)

    def __lshift__(self, other):
        return Int(self.value << other.value)

    def __rshift__(self, other):
        return Int(self.value >> other.value)

    def __add__(self, other):
        return Int(self.value + other.value)

    def __sub__(self, other):
        return Int(self.value - other.value)

    def __mul__(self, other):
        return Int(self.value * other.value)

    def __truediv__(self, other):
        return Int(self.value / other.value)

    def __floordiv__(self, other):
        return Int(self.value // other.value)

    def __mod__(self, other):
        return Int(self.value % other.value)

    def __pow__(self, other):
        return Int(self.value ** other.value)

class Float(ClassicType['float']):
    def __init__(self, py_value:float|str):
        literal = str(py_value)
        value = float(literal)
        super().__init__(Float, value)

    def __add__(self, other):
        return Float(self.value + other.value)

    def __sub__(self, other):
        return Float(self.value - other.value)

    def __mul__(self, other):
        return Float(self.value * other.value)

    def __truediv__(self, other):
        return Float(self.value / other.value)

    def __floordiv__(self, other):
        return Float(self.value // other.value)

    def __mod__(self, other):
        return Float(self.value % other.value)

    def __pow__(self, other):
        return Float(self.value ** other.value)

class String(ClassicType['string']):
    def __init__(self, py_value:str):
        super().__init__(String, py_value)

    def __invert__(self):
        return String(~self.value)

    def __lshift__(self, other):
        return String(self.value << other.value)

    def __rshift__(self, other):
        return String(self.value >> other.value)

    def __add__(self, other):
        return String(self.value + other.value)

    def __sub__(self, other):
        return String(self.value - other.value)

    def __mul__(self, other):
        return String(self.value * other.value)

    def __truediv__(self, other):
        return String(self.value / other.value)

    def __floordiv__(self, other):
        return String(self.value // other.value)

    def __mod__(self, other):
        return String(self.value % other.value)

    def __pow__(self, other):
        return String(self.value ** other.value)

    def __getitem__(self, key):
        return String(self.value[key])

    def __setitem__(self, key:ClassicType, value:ClassicType):
        self.value[key.value] = value.value

    def __delitem__(self, key:ClassicType):
        del self.value[key.value]

    def __len__(self):
        return Int(len(self.value))

    def __contains__(self, item):
        return Bool(item in self.value)

    def __sizeof__(self):
        return Int(self.value.__sizeof__())

class Char(ClassicType['char']):
    def __init__(self, py_value:str):
        super().__init__(Char, py_value[0])