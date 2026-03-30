"""
SIRC Core Node Module.

Defines the Node class used by the SIRC simulation engine. Nodes represent
logical connection points in the circuit. Connectivity between Nodes is owned
and managed by the Simulator, which groups Nodes to resolve LogicValues.
"""

from __future__ import annotations
from enum import IntEnum
from typing import Final, TYPE_CHECKING
from .logic_value import LogicValue

if TYPE_CHECKING:
    from ..simulator import DeviceSimulatorState

BASE_NODE_KIND: Final[int] = 0
GATE_NODE_KIND: Final[int] = 1


class NodeKind(IntEnum):
    """Node Kind"""

    BASE = BASE_NODE_KIND
    GATE = GATE_NODE_KIND

    def __repr__(self) -> str:
        """Return readable debug representation."""
        return f"NodeKind.{self.name}"


# pylint: disable=too-few-public-methods
class Node:
    """
    A Node is a lightweight public handle for a simulator-owned node.

    Node does not own simulation state. Runtime values are stored in
    DeviceSimulatorState dense arrays and read through this object's id_.
    """

    __slots__ = ("_state", "id_")

    def __init__(self, state: DeviceSimulatorState, node_id: int) -> None:
        """Create a Node handle bound to simulator state."""
        self._state: DeviceSimulatorState = state
        self.id_: int = node_id

    @property
    def kind(self) -> NodeKind:
        """Return the NodeKind of this Node."""
        return NodeKind(self._state.node_kinds[self.id_])

    @property
    def default_value(self) -> LogicValue:
        """Return the default LogicValue of this Node."""
        return LogicValue(self._state.node_default_values[self.id_])

    @property
    def resolved_value(self) -> LogicValue:
        """Return the resolved LogicValue of this Node."""
        return LogicValue(self._state.node_resolved_values[self.id_])

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
