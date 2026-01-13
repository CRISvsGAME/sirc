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
from .logic_value import LogicValue
from .node import Node, NodeKind


class TransistorKind(IntEnum):
    """Transistor Kind"""

    NMOS = 0
    PMOS = 1

    def __str__(self) -> str:
        """Return compact string form ('0', '1')."""
        return str(self.value)

    def __repr__(self) -> str:
        """Return readable debug representation."""
        return f"TransistorKind.{self.name}"


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

    __slots__ = ("_id", "_kind", "_gate", "_source", "_drain")

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

        The provided Nodes must have correct kinds (GATE for gate, BASE for
        source and drain) and must be distinct. Nodes are registered and managed
        by the Simulator as part of the circuit topology.
        """
        if gate.kind is not NodeKind.GATE:
            raise TypeError("Transistor gate must be a Node with kind=GATE")

        if source.kind is not NodeKind.BASE:
            raise TypeError("Transistor source must be a Node with kind=BASE")

        if drain.kind is not NodeKind.BASE:
            raise TypeError("Transistor drain must be a Node with kind=BASE")

        if gate is source or gate is drain or source is drain:
            raise ValueError("Gate, source, and drain must be distinct Nodes")

        self._id: int = transistor_id
        self._kind: TransistorKind = kind
        self._gate: Node = gate
        self._source: Node = source
        self._drain: Node = drain

    # --------------------------------------------------------------------------
    # Properties
    # --------------------------------------------------------------------------

    @property
    def id(self) -> int:
        """Return the unique identifier of this Transistor."""
        return self._id

    @property
    def kind(self) -> TransistorKind:
        """Return the kind of this Transistor."""
        return self._kind

    @property
    def gate(self) -> Node:
        """Return the gate Node of this Transistor."""
        return self._gate

    @property
    def source(self) -> Node:
        """Return the source Node of this Transistor."""
        return self._source

    @property
    def drain(self) -> Node:
        """Return the drain Node of this Transistor."""
        return self._drain

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
        return (self._gate, self._source, self._drain)

    def conduction_nodes(self) -> tuple[Node, Node]:
        """
        Return the (source, drain) Nodes involved in conduction.

        Used by the Simulator when establishing or removing connectivity.
        """
        return (self._source, self._drain)

    # --------------------------------------------------------------------------
    # Debug Representation
    # --------------------------------------------------------------------------

    def __repr__(self) -> str:
        """Return a debug representation of this Transistor."""
        name = self.__class__.__name__
        return (
            f"<{name} id={self._id} kind={self._kind!r} "
            f"gate={self._gate!r} source={self._source!r} drain={self._drain!r}>"
        )


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

    def __init__(
        self, transistor_id: int, gate: Node, source: Node, drain: Node
    ) -> None:
        super().__init__(transistor_id, TransistorKind.NMOS, gate, source, drain)

    def is_conducting(self) -> bool:
        g = self._gate.resolved_value
        return g is LogicValue.ONE


# ------------------------------------------------------------------------------
# PMOS Transistor Implementation
# ------------------------------------------------------------------------------


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
        super().__init__(transistor_id, TransistorKind.PMOS, gate, source, drain)

    def is_conducting(self) -> bool:
        g = self._gate.resolved_value
        return g is LogicValue.ZERO
