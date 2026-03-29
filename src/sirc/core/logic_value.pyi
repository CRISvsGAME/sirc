from enum import IntEnum
from typing import Final, Iterable

ZERO: Final[int]
ONE: Final[int]
X: Final[int]
Z: Final[int]
RESOLVE_TABLE: Final[tuple[int, ...]]
STRING_TABLE: Final[tuple[str, ...]]

class LogicValue(IntEnum):
    ZERO = ZERO
    ONE = ONE
    X = X
    Z = Z
    @staticmethod
    def resolve_all(values: Iterable[int]) -> LogicValue: ...
    @staticmethod
    def resolve_mask(mask: int) -> LogicValue: ...
