"""SIRC Device Simulator Dependency Module."""

from __future__ import annotations
from ..core.node import Node, NodeKind


class IdentificationFactory:
    """Identification Factory"""

    __slots__ = ("_next_node_id", "_next_device_id", "_next_transistor_id")

    def __init__(self) -> None:
        """Initialize the Identification Factory."""
        self._next_node_id: int = 0
        self._next_device_id: int = 0
        self._next_transistor_id: int = 0

    def allocate_node_id(self) -> int:
        """Allocate a unique Node ID."""
        node_id = self._next_node_id
        self._next_node_id += 1
        return node_id

    def allocate_device_id(self) -> int:
        """Allocate a unique Device ID."""
        device_id = self._next_device_id
        self._next_device_id += 1
        return device_id

    def allocate_transistor_id(self) -> int:
        """Allocate a unique Transistor ID."""
        transistor_id = self._next_transistor_id
        self._next_transistor_id += 1
        return transistor_id


class NodeFactory:
    """Node Factory"""

    __slots__ = ("_id_factory",)

    def __init__(self, id_factory: IdentificationFactory) -> None:
        """Initialize the Node Factory."""
        self._id_factory = id_factory

    def create_base_node(self) -> Node:
        """Create a new BASE Node with a unique ID."""
        node_id = self._id_factory.allocate_node_id()
        return Node(node_id, NodeKind.BASE)

    def create_gate_node(self) -> Node:
        """Create a new GATE Node with a unique ID."""
        node_id = self._id_factory.allocate_node_id()
        return Node(node_id, NodeKind.GATE)
