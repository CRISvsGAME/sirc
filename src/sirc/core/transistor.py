"""
SIRC Core Transistor Module.

Defines the Transistor base class and the NMOS and PMOS device types. A
Transistor contains exactly three Nodes: gate, source, and drain. It only stores
the structure and the Simulator will determine whether a conduction path exists.
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Protocol
from sirc.core.node import Node


class Conductive(Protocol):  # pylint: disable=too-few-public-methods
    """Protocol for objects capable of reporting conduction state."""

    def is_conducting(self) -> bool:
        """Returns True if the device is currently conducting."""
        ...  # pylint: disable=unnecessary-ellipsis


@dataclass(slots=True)
class Transistor:
    """
    Base class for a three-terminal transistor device.

    This class defines ONLY structural information and minimal helper behaviour.
    All electrical evaluation, propagation, and node-group management are
    performed exclusively by the Simulator.

    Attributes:
        gate:   The Node controlling the transistor.
        source: The source Node.
        drain:  The drain Node.
    """

    gate: Node
    source: Node
    drain: Node
