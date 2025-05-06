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

    It may hold zero or more driver LogicValues and may be directly connected
    to other Nodes. A Node performs no resolution or computation by itself;
    all evaluation and propagation are handled entirely by the Simulator.
    """

    __slots__ = ("_drivers", "_connections", "_value")

    def __init__(self) -> None:
        """Create an isolated Node with no drivers and a default Z value."""
        self._drivers: list[LogicValue] = []
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
