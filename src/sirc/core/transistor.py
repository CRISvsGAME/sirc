"""
SIRC Core Transistor Module.

Defines the abstract Transistor class and its NMOS and PMOS implementations. A
Transistor is a three-terminal digital switch with gate, source, and drain
Nodes. Transistors do not resolve logic or perform any electrical computation;
the Simulator evaluates each device's conduction state based on its gate value.
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from sirc.core.logic import LogicValue
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

    # --------------------------------------------------------------------------
    # Public Methods
    # --------------------------------------------------------------------------

    def terminals(self) -> tuple[Node, Node, Node]:
        """
        Return a tuple of (gate, source, drain) Nodes.

        Used by the Simulator for registration and structural traversal.
        """
        return (self.gate, self.source, self.drain)

    def conduction_nodes(self) -> tuple[Node, Node]:
        """
        Return the (source, drain) Nodes involved in conduction.

        Used by the Simulator when establishing or removing connectivity.
        """
        return (self.source, self.drain)

    # --------------------------------------------------------------------------
    # Debug Representation
    # --------------------------------------------------------------------------

    def __repr__(self) -> str:
        """Return a debug representation of this Transistor."""
        name = self.__class__.__name__
        return f"<{name} gate={self.gate} source={self.source} drain={self.drain}>"


# ------------------------------------------------------------------------------
# NMOS Transistor Implementation
# ------------------------------------------------------------------------------


class NMOS(Transistor):
    """
    NMOS transistor device.

    Conduction Rule:
        - Conducts when the gate value is LogicValue.ONE.
        - Non-conducting for ZERO, X, or Z.
    """

    def is_conducting(self) -> bool:
        g = self.gate.value
        return g is LogicValue.ONE
