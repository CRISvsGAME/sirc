from enum import IntEnum
from typing import Iterable

class LogicValue(IntEnum):
    ZERO = 1
    ONE = 2
    X = 4
    Z = 0
    @staticmethod
    def resolve_all(values: Iterable[LogicValue]) -> LogicValue: ...
    @staticmethod
    def resolve_mask(mask: int) -> LogicValue: ...

ZERO: LogicValue
ONE: LogicValue
X: LogicValue
Z: LogicValue
RESOLVE_TABLE: tuple[LogicValue, ...]
