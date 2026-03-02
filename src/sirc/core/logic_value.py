"""
SIRC Core Logic Module.

Defines the internal four-state digital logic values used throughout the SIRC
simulation engine. The logic rules follow the four-state resolution semantics
defined by IEEE 1800-2023.

Representation
--------------
LogicValue is intentionally encoded as a 3-bit driver-presence mask:

    ZERO = 0b001
    ONE  = 0b010
    X    = 0b100
    Z    = 0b000

This encoding allows multiple drivers to be accumulated using bitwise OR:

    bit 0 set (0b001) -> at least one ZERO driver present
    bit 1 set (0b010) -> at least one ONE driver present
    bit 2 set (0b100) -> at least one X driver present
    zero mask (0b000) -> no non-Z drivers are present

Resolution
----------
The final resolved LogicValue is obtained by indexing RESOLVE_TABLE:

    RESOLVE_TABLE[mask] -> LogicValue
    0b000 -> Z
    0b001 -> ZERO
    0b010 -> ONE
    0b011 -> X
    0b100 -> X
    0b101 -> X
    0b110 -> X
    0b111 -> X
"""

from __future__ import annotations
from enum import IntEnum, unique
from typing import Iterable


@unique
class LogicValue(IntEnum):
    """
    Internal four-state digital logic value used by SIRC.

    Values:
        ZERO (0) -> logical low
        ONE  (1) -> logical high
        X        -> unknown or conflicting value
        Z        -> undriven or high-impedance value
    """

    ZERO = 0b001
    ONE = 0b010
    X = 0b100
    Z = 0b000

    # --------------------------------------------------------------------------
    # Driver Resolution
    # --------------------------------------------------------------------------

    @staticmethod
    def resolve_all(values: Iterable[LogicValue]) -> LogicValue:
        """
        Resolve multiple driver values into a single LogicValue.

        The iterable is reduced into a 3-bit driver-presence mask using bitwise
        OR, which is then used to index RESOLVE_TABLE for the final value.

        Args:
            values: Iterable of LogicValue driver values.

        Returns:
            LogicValue: The resolved value or Z if no values are provided.
        """
        mask = 0b000

        for value in values:
            mask |= value

        return RESOLVE_TABLE[mask]

    @staticmethod
    def resolve_mask(mask: int) -> LogicValue:
        """
        Resolve a precomputed 3-bit driver-presence mask.

        The caller is responsible for providing a valid mask in the inclusive
        range [0b000, 0b111].

        Args:
            mask: Integer mask in the inclusive range [0b000, 0b111].

        Returns:
            LogicValue: The resolved value.
        """
        return RESOLVE_TABLE[mask]

    # --------------------------------------------------------------------------
    # Display Helpers
    # --------------------------------------------------------------------------

    def __str__(self) -> str:
        """Return compact string form ('0', '1', 'X', 'Z')."""
        if self is ZERO:
            return "0"

        if self is ONE:
            return "1"

        if self is X:
            return "X"

        return "Z"

    def __repr__(self) -> str:
        """Return debug representation."""
        return f"LogicValue.{self.name}"


ZERO: LogicValue = LogicValue.ZERO
ONE: LogicValue = LogicValue.ONE
X: LogicValue = LogicValue.X
Z: LogicValue = LogicValue.Z

RESOLVE_TABLE: tuple[LogicValue, ...] = (Z, ZERO, ONE, X, X, X, X, X)
