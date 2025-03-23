from typing import Generic, TypeVar, Type

T = TypeVar("T")

class QutesType(Generic[T]):
    def __init__(self, t_type: Type[T]):
        super().__init__()
        self.t_type = t_type

    @staticmethod
    def get_default_value():
        raise NotImplementedError("get_default_value method must be implemented in derived class")

    def __to_printable__(self) -> str:
        raise NotImplementedError("__to_printable__ method must be implemented in derived class")

    def __str__(self) -> str:
        return f"{self.__to_printable__()}"

    def __repr__(self) -> str:
        return f"{self.__class__.__qualname__}:{self.__to_printable__()}"