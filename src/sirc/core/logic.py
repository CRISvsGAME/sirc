"""
SIRC Core Logic Module.

Defines the four-state digital logic values used throughout the SIRC simulation
engine. The logic rules follow the four-state resolution semantics defined by
IEEE 1800-2023, but the terminology used here follows SIRC conventions.
"""

from __future__ import annotations
from enum import Enum, unique
from typing import Iterable


@unique
class LogicValue(Enum):
    """
    Four-state digital logic value used by Nodes and drivers in SIRC.

    Values:
        ZERO (0) -> logical low
        ONE  (1) -> logical high
        X        -> unknown or conflicting value
        Z        -> undriven or high-impedance value
    """

    ZERO = "0"
    ONE = "1"
    X = "X"
    Z = "Z"

    # --------------------------------------------------------------------------
    # Helper Properties
    # --------------------------------------------------------------------------

    @property
    def is_zero(self) -> bool:
        """Return True if this value is ZERO."""
        return self is LogicValue.ZERO

    @property
    def is_one(self) -> bool:
        """Return True if this value is ONE."""
        return self is LogicValue.ONE

    @property
    def is_x(self) -> bool:
        """Return True if this value is unknown (X)."""
        return self is LogicValue.X

    @property
    def is_z(self) -> bool:
        """Return True if this value is high-impedance (Z)."""
        return self is LogicValue.Z

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
        result = self

        if self is not other:

            if self.is_x or other.is_x:
                result = LogicValue.X

            elif self.is_z and other.is_z:
                result = LogicValue.Z

            elif (self.is_zero and other.is_one) or (self.is_one and other.is_zero):
                result = LogicValue.X

            elif self.is_z:
                result = other

            elif other.is_z:
                result = self

        return result

    # --------------------------------------------------------------------------
    # Multi-Driver Resolution
    # --------------------------------------------------------------------------

    @staticmethod
    def resolve_all(values: Iterable[LogicValue]) -> LogicValue:
        """
        Resolve multiple driver values into a single LogicValue.

        Args:
            values: Iterable of LogicValue instances.

        Raises:
            ValueError: If no values are provided.

        Returns:
            LogicValue: The resolved value.
        """
        iterator = iter(values)

        try:
            result = next(iterator)
        except StopIteration as e:
            raise ValueError("resolve_all() requires at least one LogicValue.") from e

        for value in iterator:
            result = result.resolve(value)
            if result.is_x:
                return LogicValue.X

        return result

    # --------------------------------------------------------------------------
    # Display Helpers
    # --------------------------------------------------------------------------

    def __str__(self) -> str:
        """Return compact string form ('0', '1', 'X', 'Z')."""
        return self.value

    def __repr__(self) -> str:
        """Return readable debug representation."""
        return f"LogicValue.{self.name}"
