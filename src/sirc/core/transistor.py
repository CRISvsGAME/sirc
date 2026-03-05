"""
SIRC Core Transistor Module.

Defines the abstract Transistor class and its NMOS and PMOS implementations. A
Transistor is a three-terminal digital switch with gate, source, and drain
Nodes. Transistors do not resolve logic or perform any electrical computation;
the Simulator evaluates each device's conduction state based on its gate value.

In the Simulator, the source-drain channel is treated as an undirected switch;
source and drain are interchangeable.
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from enum import IntEnum
from .logic_value import ZERO, ONE
from .node import Node


class TransistorKind(IntEnum):
    """Transistor Kind"""

    NMOS = 0
    PMOS = 1

    def __repr__(self) -> str:
        """Return readable debug representation."""
        return f"TransistorKind.{self.name}"


NMOS_TRANSISTOR_KIND: TransistorKind = TransistorKind.NMOS
PMOS_TRANSISTOR_KIND: TransistorKind = TransistorKind.PMOS


class Transistor(ABC):
    """
    Abstract class for three-terminal transistor devices.

    Each Transistor contains:
        - gate  : Node controlling conduction
        - source: One side of the controlled channel
        - drain : The other side of the controlled channel

    This class defines structural information only. Device-specific conduction
    rules are implemented by subclasses. All logic evaluation and node-group
    management are performed entirely by the Simulator.
    """

    __slots__ = ("id_", "kind", "gate", "source", "drain")

    # pylint: disable=too-many-arguments, too-many-positional-arguments
    def __init__(
        self,
        transistor_id: int,
        kind: TransistorKind,
        gate: Node,
        source: Node,
        drain: Node,
    ) -> None:
        """
        Create a new transistor with gate, source, and drain Nodes.

        The Simulator is expected to provide correctly typed and distinct Nodes:
        GATE for gate, BASE for source and drain. Nodes are registered and
        managed by the Simulator as part of the circuit topology.
        """
        self.id_: int = transistor_id
        self.kind: TransistorKind = kind
        self.gate: Node = gate
        self.source: Node = source
        self.drain: Node = drain

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
    # Debug Representation
    # --------------------------------------------------------------------------

    def __repr__(self) -> str:
        """Return a debug representation of this Transistor."""
        name = self.__class__.__name__
        return (
            f"<{name} id={self.id_} kind={self.kind!r} "
            f"gate={self.gate!r} source={self.source!r} drain={self.drain!r}>"
        )


# ------------------------------------------------------------------------------
# NMOS Transistor Implementation
# ------------------------------------------------------------------------------


# pylint: disable=too-few-public-methods
class NMOS(Transistor):
    """
    NMOS transistor device.

    Conduction Rule:
        - Conducts when the gate value is LogicValue.ONE.
        - Non-conducting for ZERO, X, or Z.
    """

    def __init__(
        self, transistor_id: int, gate: Node, source: Node, drain: Node
    ) -> None:
        super().__init__(transistor_id, NMOS_TRANSISTOR_KIND, gate, source, drain)

    def is_conducting(self) -> bool:
        return self.gate.resolved_value is ONE


# ------------------------------------------------------------------------------
# PMOS Transistor Implementation
# ------------------------------------------------------------------------------


# pylint: disable=too-few-public-methods
class PMOS(Transistor):
    """
    PMOS transistor device.

    Conduction Rule:
        - Conducts when the gate value is LogicValue.ZERO.
        - Non-conducting for ONE, X, or Z.
    """

    def __init__(
        self, transistor_id: int, gate: Node, source: Node, drain: Node
    ) -> None:
        super().__init__(transistor_id, PMOS_TRANSISTOR_KIND, gate, source, drain)

    def is_conducting(self) -> bool:
        return self.gate.resolved_value is ZERO
