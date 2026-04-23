"""
SIRC Core Node Module.

Node handle and node-kind representation primitives.

Node-kind domain
----------------

Representation:
    A node kind is one of the canonical raw node-kind integers:

        BASE_NODE_KIND = 0
        GATE_NODE_KIND = 1

    NodeKind is the semantic IntEnum wrapper for canonical node kinds.

Meaning:
    BASE -> ordinary circuit connection node.
    GATE -> transistor gate/control node.

    Node-kind values classify simulator-owned node records for topology,
    representation, serialization, and optional scheduling/caching.

    Node-kind values do not define connectivity, ownership, or evaluation
    behavior by themselves.

Node handle domain
------------------

Representation:
    A Node is a lightweight handle over a simulator-owned node record.

        Node._state -> DeviceSimulatorState
        Node.id_    -> dense node id

    Runtime node data is stored in DeviceSimulatorState dense arrays:

        node_kinds[id_]           -> raw node-kind integer
        node_default_values[id_]  -> raw logic value
        node_resolved_values[id_] -> raw logic value

Meaning:
    Node does not own simulation state, connectivity, drivers, or topology.

    Node reads simulator-owned arrays by id_ and exposes semantic/debug views:

        node.kind           -> NodeKind
        node.default_value  -> LogicValue
        node.resolved_value -> LogicValue

Module contract
---------------

Execution contract:
    Simulator hot paths use dense arrays, raw node ids, raw node-kind integers,
    and raw logic values directly.

    Node and NodeKind are representation/debug/serialization helpers.
    They are not simulator hot-path objects.

Ownership contract:
    DeviceSimulatorState owns runtime node data.
    DeviceSimulator owns creation, mutation, connectivity, and evaluation.
    Node owns only a state reference and node id.
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
    """Semantic IntEnum wrapper for canonical node kinds."""

    BASE = BASE_NODE_KIND
    GATE = GATE_NODE_KIND

    def __repr__(self) -> str:
        """Return debug representation."""
        return f"NodeKind.{self.name}"


class Node:
    """
    Lightweight handle over a simulator-owned node record.

    Node owns only a state reference and dense node id.
    Runtime node data is stored in DeviceSimulatorState arrays.
    """

    __slots__ = ("_state", "id_")

    def __init__(self, state: DeviceSimulatorState, node_id: int) -> None:
        """Create a Node handle."""
        self._state: DeviceSimulatorState = state
        self.id_: int = node_id

    @property
    def kind(self) -> NodeKind:
        """Return semantic node kind."""
        return NodeKind(self._state.node_kinds[self.id_])

    @property
    def default_value(self) -> LogicValue:
        """Return semantic default logic value."""
        return LogicValue(self._state.node_default_values[self.id_])

    @property
    def resolved_value(self) -> LogicValue:
        """Return semantic resolved logic value."""
        return LogicValue(self._state.node_resolved_values[self.id_])

    # --------------------------------------------------------------------------
    # Debug representation
    # --------------------------------------------------------------------------

    def __repr__(self) -> str:
        """Return a debug representation of this Node."""
        return (
            f"<Node id={self.id_} kind={self.kind!r} "
            f"default_value={self.default_value!r} "
            f"resolved_value={self.resolved_value!r}>"
        )
