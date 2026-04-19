"""
SIRC Core Logic Module.

Four-state logical value encoding and mask-based resolution primitives.

Resolved-value domain
---------------------

Representation:
    A resolved value is one of the four canonical logical states:

        Z    = 0b000
        ZERO = 0b001
        ONE  = 0b010
        X    = 0b100

    LogicValue is the semantic IntEnum wrapper for canonical resolved values.

Meaning:
    Z    -> no non-Z driver.
    ZERO -> resolved logical 0.
    ONE  -> resolved logical 1.
    X    -> resolved unknown or conflict.

    Every resolved value is a valid driver-presence mask and resolves to itself.

Driver-presence-mask domain
---------------------------

Representation:
    A driver-presence mask is a non-bool int in the inclusive range 0b000..0b111.

        bit 0 set -> at least one ZERO driver is present.
        bit 1 set -> at least one ONE driver is present.
        bit 2 set -> at least one X driver is present.
        0b000     -> no non-Z driver is present.

    Masks compose with bitwise OR.

Meaning:
    Driver-presence masks are accumulation values.

    These masks are valid but non-canonical:

        0b011 -> ZERO + ONE
        0b101 -> ZERO + X
        0b110 -> ONE  + X
        0b111 -> ZERO + ONE + X

Resolution:
    RESOLVE_TABLE[mask] maps any valid mask to a canonical resolved value:

        0b000 -> Z
        0b001 -> ZERO
        0b010 -> ONE
        0b011 -> X
        0b100 -> X
        0b101 -> X
        0b110 -> X
        0b111 -> X

Module contract
---------------

API boundary:
    resolve(values) accepts LogicValue members, resolved raw values, accumulated
    masks, or any valid mix of these.

Execution contract:
    Core logic is unchecked.
    Callers must provide valid masks.
    Simulator hot paths use raw integer constants and RESOLVE_TABLE directly.
    LogicValue is for semantic/debug representation.
    Validation belongs at external/public input boundaries, not here.
"""

from __future__ import annotations
from enum import IntEnum, unique
from typing import Final, Iterable

Z: Final[int] = 0b000
ZERO: Final[int] = 0b001
ONE: Final[int] = 0b010
X: Final[int] = 0b100

RESOLVE_TABLE: Final[tuple[int, ...]] = (Z, ZERO, ONE, X, X, X, X, X)
_STRING_TABLE: Final[tuple[str, ...]] = ("Z", "0", "1", "X", "X", "X", "X", "X")


@unique
class LogicValue(IntEnum):
    """Semantic IntEnum wrapper for canonical resolved logic values."""

    Z = Z
    ZERO = ZERO
    ONE = ONE
    X = X

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
