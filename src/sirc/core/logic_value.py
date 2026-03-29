"""
SIRC Core Logic Module.

Defines the internal four-state digital logic values used throughout the SIRC
simulation engine.

SIRC uses a compact four-state digital logic model inspired by the value
semantics of IEEE 1800-2023: logical low, logical high, unknown/conflicting, and
undriven/high-impedance.

Representation
--------------
Logic values are encoded as 3-bit driver-presence masks:

    ZERO = 0b001
    ONE  = 0b010
    X    = 0b100
    Z    = 0b000

This encoding allows multiple drivers or partially accumulated masks to be
combined using bitwise OR:

    bit 0 set (0b001) -> at least one ZERO driver present
    bit 1 set (0b010) -> at least one ONE driver present
    bit 2 set (0b100) -> at least one X driver present
    zero mask (0b000) -> no non-Z drivers are present

Resolution
----------
The final resolved logic value is obtained by indexing RESOLVE_TABLE:

    RESOLVE_TABLE[mask] -> raw LogicValue-compatible integer
    0b000 -> Z
    0b001 -> ZERO
    0b010 -> ONE
    0b011 -> X
    0b100 -> X
    0b101 -> X
    0b110 -> X
    0b111 -> X

The simulator hot path uses the raw integer constants and RESOLVE_TABLE
directly. LogicValue exists as a semantic/debug/API wrapper around the same
integer domain.
"""

from __future__ import annotations
from enum import IntEnum, unique
from typing import Final, Iterable

ZERO: Final[int] = 0b001
ONE: Final[int] = 0b010
X: Final[int] = 0b100
Z: Final[int] = 0b000

RESOLVE_TABLE: Final[tuple[int, ...]] = (Z, ZERO, ONE, X, X, X, X, X)
STRING_TABLE: Final[tuple[str, ...]] = ("Z", "0", "1", "X", "X", "X", "X", "X")


@unique
class LogicValue(IntEnum):
    """
    Semantic wrapper for SIRC's four-state logic value domain.

    Values:
        ZERO -> logical low
        ONE  -> logical high
        X    -> unknown or conflicting value
        Z    -> undriven or high-impedance value
    """

    ZERO = ZERO
    ONE = ONE
    X = X
    Z = Z

    # --------------------------------------------------------------------------
    # Driver Resolution
    # --------------------------------------------------------------------------

    @staticmethod
    def resolve_all(values: Iterable[int]) -> LogicValue:
        """
        Resolve multiple logic masks into a single LogicValue.

        The iterable is accumulated into a 3-bit driver-presence mask using
        bitwise OR, which is then resolved through RESOLVE_TABLE.

        Each value may represent either:
            - A single LogicValue-compatible driver value
            - A partially precomputed driver-presence mask

        Args:
            values: Iterable of valid mask-compatible logic integers.

        Returns:
            LogicValue: The resolved value, or Z if no values are provided.
        """
        mask = Z

        for value in values:
            mask |= value

        return LogicValue(RESOLVE_TABLE[mask])

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
        return LogicValue(RESOLVE_TABLE[mask])

    # --------------------------------------------------------------------------
    # Display Helpers
    # --------------------------------------------------------------------------

    def __str__(self) -> str:
        """Return compact string form ('0', '1', 'X', 'Z')."""
        return STRING_TABLE[self]

    def __repr__(self) -> str:
        """Return debug representation."""
        return f"LogicValue.{self.name}"
