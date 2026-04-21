from enum import IntEnum
from typing import Final, Iterable

Z: Final[int]
ZERO: Final[int]
ONE: Final[int]
X: Final[int]
RESOLVE_TABLE: Final[tuple[int, ...]]

class LogicValue(IntEnum):
    Z = 0
    ZERO = 1
    ONE = 2
    X = 4
    @staticmethod
    def resolve(values: Iterable[int]) -> LogicValue: ...
