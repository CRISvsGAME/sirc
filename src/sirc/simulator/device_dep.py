"""SIRC Device Simulator Dependency Module."""

from __future__ import annotations


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
