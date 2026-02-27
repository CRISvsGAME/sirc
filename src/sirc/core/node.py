"""
SIRC Core Node Module.

Defines the Node class used by the SIRC simulation engine. Nodes represent
logical connection points in the circuit. Connectivity between Nodes is owned
and managed by the Simulator, which groups Nodes to resolve LogicValues.
"""

from __future__ import annotations
from enum import IntEnum
from .logic_value import LogicValue, Z


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


BASE_NODE_KIND: NodeKind = NodeKind.BASE
GATE_NODE_KIND: NodeKind = NodeKind.GATE


# pylint: disable=too-few-public-methods
class Node:
    """
    A Node is a passive logical connection point in the SIRC circuit model.

    A Node holds one default LogicValue and participates in connectivity managed
    by the Simulator. A Node performs no resolution or computation by itself;
    all evaluation and propagation are handled entirely by the Simulator.
    """

    __slots__ = ("id_", "kind", "default_value", "resolved_value")

    def __init__(self, node_id: int, kind: NodeKind = BASE_NODE_KIND) -> None:
        """Create a Node with default and resolved LogicValue set to Z."""
        self.id_: int = node_id
        self.kind: NodeKind = kind
        self.default_value: LogicValue = Z
        self.resolved_value: LogicValue = Z

    # --------------------------------------------------------------------------
    # Debug Representation
    # --------------------------------------------------------------------------

    def __repr__(self) -> str:
        """Return a debug representation of this Node."""
        return (
            f"<Node id={self.id_} kind={self.kind!r} "
            f"default_value={self.default_value!r} "
            f"resolved_value={self.resolved_value!r}>"
        )
