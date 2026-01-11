"""
SIRC Core Node Module.

Defines the Node class used by the SIRC simulation engine. Nodes represent
logical connection points in the circuit. Connectivity between Nodes is owned
and managed by the Simulator, which groups Nodes to resolve LogicValues.
"""

from __future__ import annotations
from enum import IntEnum
from sirc.core import LogicValue


class NodeKind(IntEnum):
    """Node Kind"""

    BASE = 0
    GATE = 1

    def __str__(self) -> str:
        """Return compact string form ('0', '1')."""
        return str(self.value)

    def __repr__(self) -> str:
        """Return readable debug representation."""
        return f"NodeKind.{self.name}"


class Node:
    """
    A Node is a passive logical connection point in the SIRC circuit model.

    A Node holds one default LogicValue and participates in connectivity managed
    by the Simulator. A Node performs no resolution or computation by itself;
    all evaluation and propagation are handled entirely by the Simulator.
    """

    __slots__ = ("_id", "_kind", "_default_value", "_resolved_value")

    def __init__(self, node_id: int, kind: NodeKind = NodeKind.BASE) -> None:
        """Create a Node with default and resolved LogicValue set to Z."""
        self._id: int = node_id
        self._kind: NodeKind = kind
        self._default_value: LogicValue = LogicValue.Z
        self._resolved_value: LogicValue = LogicValue.Z

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
    # Properties
    # --------------------------------------------------------------------------

    @property
    def id(self) -> int:
        """Return the unique identifier of this Node."""
        return self._id

    @property
    def kind(self) -> NodeKind:
        """Return the kind of this Node."""
        return self._kind

    # --------------------------------------------------------------------------
    # Debug Representation
    # --------------------------------------------------------------------------

    def __repr__(self) -> str:
        """Return a debug representation of this Node."""
        return (
            f"<Node id={self._id} kind={self._kind!r} "
            f"default_value={self._default_value!r} "
            f"resolved_value={self._resolved_value!r}>"
        )
