from typing import TypeVar
from symbols.types import ClassicType

T = TypeVar("T")

class ClassicArrayType(ClassicType[list[T]]):
    def __init__(self, unit_class_type: T, array:list['Symbol']):
        super().__init__(ClassicArrayType, unit_class_type)
        self.unit_class_type = unit_class_type
        self.array:list['Symbol'] = array
        self.size = len(array)

    @staticmethod
    def get_default_value():
        return ClassicArrayType(bool, [])

    def __getitem__(self, key):
        return self.array[key]

    def __setitem__(self, key:ClassicType, value:ClassicType):
        self.array[key.value] = value.value

    def __delitem__(self, key:ClassicType):
        del self.array[key.value]

    def __iter__(self):
        return iter(self.array)

    def __len__(self):
        return len(self.array)

    def __contains__(self, item):
        return item in self.array

    def __reversed__(self):
        return reversed(self.array)

    def __sizeof__(self):
        return self.array.__sizeof__()