from _typeshed import Incomplete
from enum import IntEnum
from typing import Iterable

class LogicValue(IntEnum):
    ZERO = 1
    ONE = 2
    X = 4
    Z = 0
    @property
    def is_zero(self) -> bool: ...
    @property
    def is_one(self) -> bool: ...
    @property
    def is_x(self) -> bool: ...
    @property
    def is_z(self) -> bool: ...
    def resolve(self, other: LogicValue) -> LogicValue: ...
    @staticmethod
    def resolve_all(values: Iterable[LogicValue]) -> LogicValue: ...
    @staticmethod
    def resolve_all_byte(mask: int) -> LogicValue: ...

ZERO: Incomplete
ONE: Incomplete
X: Incomplete
Z: Incomplete
RESOLVE_TABLE: tuple[LogicValue, ...]
