"""
SIRC Core Transistor Module.

Defines the Transistor base class and the NMOS and PMOS device types. A
Transistor contains exactly three Nodes: gate, source, and drain. It only stores
the structure and the Simulator will determine whether a conduction path exists.
"""

from __future__ import annotations
from typing import Protocol


class Conductive(Protocol):  # pylint: disable=too-few-public-methods
    """Protocol for objects capable of reporting conduction state."""

    def is_conducting(self) -> bool:
        """Returns True if the device is currently conducting."""
        ...  # pylint: disable=unnecessary-ellipsis
