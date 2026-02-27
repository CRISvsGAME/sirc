"""
SIRC Core Logic Module.

Defines the four-state digital logic values used throughout the SIRC simulation
engine. The logic rules follow the four-state resolution semantics defined by
IEEE 1800-2023, but the terminology used here follows SIRC conventions.
"""

from __future__ import annotations
from enum import IntEnum, unique
from typing import Iterable


@unique
class LogicValue(IntEnum):
    """
    Four-state digital logic value used by Nodes and drivers in SIRC.

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
    # Helper Properties
    # --------------------------------------------------------------------------

    @property
    def is_zero(self) -> bool:
        """Return True if this value is ZERO."""
        return self is ZERO

    @property
    def is_one(self) -> bool:
        """Return True if this value is ONE."""
        return self is ONE

    @property
    def is_x(self) -> bool:
        """Return True if this value is unknown (X)."""
        return self is X

    @property
    def is_z(self) -> bool:
        """Return True if this value is high-impedance (Z)."""
        return self is Z

    # --------------------------------------------------------------------------
    # Two-Driver Resolution
    # --------------------------------------------------------------------------

    def resolve(self, other: LogicValue) -> LogicValue:
        """
        Resolve two driver values into a single LogicValue.

        Args:
            other: The second LogicValue driving the same Node.

        Returns:
            LogicValue: The resolved value.

        Resolution Table (N = Node):
             N | 0 | 1 | X | Z
            ---+---+---+---+---
             0 | 0 | X | X | 0
            ---+---+---+---+---
             1 | X | 1 | X | 1
            ---+---+---+---+---
             X | X | X | X | X
            ---+---+---+---+---
             Z | 0 | 1 | X | Z
        """

        z_value = Z

        if self is other or other is z_value:
            return self

        if self is z_value:
            return other

        return X

    # --------------------------------------------------------------------------
    # Multi-Driver Resolution
    # --------------------------------------------------------------------------

    @staticmethod
    def resolve_all(values: Iterable[LogicValue]) -> LogicValue:
        """
        Resolve multiple driver values into a single LogicValue.

        Args:
            values: Iterable of LogicValue instances.

        Returns:
            LogicValue: The resolved value or Z if no values are provided.
        """
        mask = 0b000

        for value in values:
            if value:
                mask |= value

        return RESOLVE_TABLE[mask]

    @staticmethod
    def resolve_all_byte(mask: int) -> LogicValue:
        """
        Resolve multiple driver values represented as a byte mask.

        Args:
            mask: An 8-bit integer where each bit represents a LogicValue:
                - Bit  0 (0b001): ZERO
                - Bit  1 (0b010): ONE
                - Bit  2 (0b100): X
                - Mask 0 (0b000): Z

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
        """Return readable debug representation."""
        return f"LogicValue.{self.name}"


ZERO: LogicValue = LogicValue.ZERO
ONE: LogicValue = LogicValue.ONE
X: LogicValue = LogicValue.X
Z: LogicValue = LogicValue.Z

RESOLVE_TABLE: tuple[LogicValue, ...] = (Z, ZERO, ONE, X, X, X, X, X)
