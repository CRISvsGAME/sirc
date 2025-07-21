"""
SIRC Core Transistor Module.

Defines the abstract Transistor class and its NMOS and PMOS implementations. A
Transistor is a three-terminal digital switch with gate, source, and drain
Nodes. Transistors do not resolve logic or perform any electrical computation;
the Simulator evaluates each device's conduction state based on its gate value.
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from sirc.core.node import Node


class Transistor(ABC):
    """
    Abstract class for three-terminal transistor devices.

    Each Transistor contains:
        - gate  : Node controlling conduction
        - source: One side of the controlled channel
        - drain : The other side of the controlled channel

    This class defines only structural information and simple access helpers.
    Device-specific conduction rules are implemented by subclasses. All logic
    evaluation and node-group management is performed entirely by the Simulator.
    """

    __slots__ = ("gate", "source", "drain")

    def __init__(self) -> None:
        """
        Create a new transistor with dedicated gate, source, and drain Nodes.
        All Nodes begin in high-impedance (Z) state with no drivers. These Nodes
        belong exclusively to this device and are never shared.
        """
        self.gate = Node()
        self.source = Node()
        self.drain = Node()

    # --------------------------------------------------------------------------
    # Abstract Methods
    # --------------------------------------------------------------------------

    @abstractmethod
    def is_conducting(self) -> bool:
        """
        Return True if this transistor is currently conducting.

        A conducting transistor forms an electrical path between its source and
        drain. The Simulator uses this result to determine whether the two Nodes
        should be treated as members of the same node-group.
        """
        raise NotImplementedError("Must be implemented by subclasses.")
