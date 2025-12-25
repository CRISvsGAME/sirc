"""
SIRC Core Node Module.

Defines the Node class used by the SIRC simulation engine. Nodes represent
logical connection points in the circuit. Multiple Nodes may be connected,
forming an electrical group that collectively resolves a single LogicValue.
"""

from __future__ import annotations
from sirc.core.logic import LogicValue


class Node:
    """
    A Node is a passive logical connection point in the SIRC circuit model.

    A Node holds one default LogicValue and may be directly connected
    to other Nodes. A Node performs no resolution or computation by itself;
    all evaluation and propagation are handled entirely by the Simulator.
    """

    __slots__ = ("_default_value", "_resolved_value", "_connections")

    def __init__(self) -> None:
        """Create an isolated Node with default LogicValue Z."""
        self._default_value: LogicValue = LogicValue.Z
        self._resolved_value: LogicValue = LogicValue.Z
        self._connections: set[Node] = set()

    # --------------------------------------------------------------------------
    # Default Value Handling (Device-Controlled)
    # --------------------------------------------------------------------------

    def set_default_value(self, value: LogicValue) -> None:
        """
        Set the default LogicValue to this Node.

        Args:
            value: The default LogicValue to set.
        """
        self._default_value = value

    @property
    def default_value(self) -> LogicValue:
        """Return the current default LogicValue of this Node."""
        return self._default_value

    # --------------------------------------------------------------------------
    # Resolved Value Handling (Simulator-Controlled)
    # --------------------------------------------------------------------------

    def set_resolved_value(self, value: LogicValue) -> None:
        """
        Set the resolved LogicValue of this Node.

        Args:
            value: The resolved LogicValue to set.
        """
        self._resolved_value = value

    @property
    def resolved_value(self) -> LogicValue:
        """Return the current resolved LogicValue of this Node."""
        return self._resolved_value

    # --------------------------------------------------------------------------
    # Connectivity
    # --------------------------------------------------------------------------

    def add_connection(self, other: Node) -> None:
        """INTERNAL USE ONLY: Add a direct connection to another Node."""
        self._connections.add(other)

    def remove_connection(self, other: Node) -> None:
        """INTERNAL USE ONLY: Remove a direct connection to another Node."""
        self._connections.discard(other)

    def connect(self, other: Node) -> None:
        """
        Create a bidirectional connection between this Node and another.

        Args:
            other: The Node to connect to.
        """
        if self is other:
            return

        self.add_connection(other)
        other.add_connection(self)

    def disconnect(self, other: Node) -> None:
        """
        Remove the bidirectional connection between this Node and another.

        Args:
            other: The Node to disconnect from.
        """
        if self is other:
            return

        self.remove_connection(other)
        other.remove_connection(self)

    def get_connections(self) -> set[Node]:
        """Return all directly connected Nodes as a set."""
        return self._connections

    # --------------------------------------------------------------------------
    # Debug Representation
    # --------------------------------------------------------------------------

    def __repr__(self) -> str:
        """Return a debug representation of this Node."""
        return (
            f"<Node default_value={self._default_value!r} "
            f"resolved_value={self._resolved_value!r}>"
        )
