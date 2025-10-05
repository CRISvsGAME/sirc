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

    It may hold one or more driver LogicValues and may be directly connected
    to other Nodes. A Node performs no resolution or computation by itself;
    all evaluation and propagation are handled entirely by the Simulator.
    """

    __slots__ = ("_drivers", "_connections", "_value")

    def __init__(self) -> None:
        """Create an isolated Node with default Z driver and Z value."""
        self._drivers: list[LogicValue] = [LogicValue.Z]
        self._connections: set[Node] = set()
        self._value: LogicValue = LogicValue.Z

    # --------------------------------------------------------------------------
    # Value Handling (Simulator-Controlled)
    # --------------------------------------------------------------------------

    def set_resolved_value(self, value: LogicValue) -> None:
        """
        Set the resolved LogicValue of this Node.

        Args:
            value: The resolved LogicValue to set.
        """
        self._value = value

    @property
    def value(self) -> LogicValue:
        """Return the current resolved LogicValue of this Node."""
        return self._value

    # --------------------------------------------------------------------------
    # Driver Management
    # --------------------------------------------------------------------------

    def add_driver(self, value: LogicValue) -> None:
        """
        Add a driver LogicValue to this Node.

        Args:
            value: The LogicValue driving this Node.
        """
        self._drivers.append(value)

    def clear_drivers(self) -> None:
        """Reset the Node to default Z driver and Z value."""
        self._drivers[:] = [LogicValue.Z]
        self._value = LogicValue.Z

    def get_drivers(self) -> tuple[LogicValue, ...]:
        """Return all driver LogicValues as an immutable tuple."""
        return tuple(self._drivers)

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

    def get_connections(self) -> tuple[Node, ...]:
        """Return all directly connected Nodes as an immutable tuple."""
        return tuple(self._connections)

    # --------------------------------------------------------------------------
    # Debug Representation
    # --------------------------------------------------------------------------

    def __repr__(self) -> str:
        """Return a debug representation of this Node."""
        return f"<Node value={self._value!r} drivers={tuple(self._drivers)!r}>"
