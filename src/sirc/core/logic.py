"""
SIRC Core Logic Module.

Defines the four-state digital logic values used throughout the SIRC simulation
engine. The logic rules follow the four-state resolution semantics defined by
IEEE 1800-2023, but the terminology used here follows SIRC conventions.
"""

from __future__ import annotations
from enum import Enum, unique


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
