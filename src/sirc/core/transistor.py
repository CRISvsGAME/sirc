"""
SIRC Core Transistor Module.

Defines Transistor, a lightweight public handle for simulator-owned
three-terminal transistor switches.

A Transistor has gate, source, and drain Nodes. It does not own runtime state
and does not compute conduction. Transistor topology, kind, and conduction state
are stored in DeviceSimulatorState dense arrays and read through this object's
id_.

In the Simulator, the source-drain channel is treated as an undirected switch;
source and drain are interchangeable.
"""

from __future__ import annotations
from enum import IntEnum
from typing import Final, TYPE_CHECKING
from .node import Node

if TYPE_CHECKING:
    from ..simulator import DeviceSimulatorState

NMOS_TRANSISTOR_KIND: Final[int] = 0
PMOS_TRANSISTOR_KIND: Final[int] = 1


class TransistorKind(IntEnum):
    """Transistor Kind"""

    NMOS = NMOS_TRANSISTOR_KIND
    PMOS = PMOS_TRANSISTOR_KIND

    def __repr__(self) -> str:
        """Return readable debug representation."""
        return f"TransistorKind.{self.name}"


class Transistor:
    """
    A lightweight public handle for a simulator-owned transistor.

    Transistor does not own runtime state. Its kind, gate/source/drain Nodes,
    and current conduction state are stored in DeviceSimulatorState dense
    arrays. The simulator is responsible for creation, validation, conduction
    evaluation, and node-group propagation.
    """

    __slots__ = ("_state", "id_")

    def __init__(self, state: DeviceSimulatorState, transistor_id: int) -> None:
        """Create a Transistor handle bound to simulator state."""
        self._state: DeviceSimulatorState = state
        self.id_: int = transistor_id

    @property
    def kind(self) -> TransistorKind:
        """Return the TransistorKind of this Transistor."""
        return TransistorKind(self._state.transistor_kinds[self.id_])

    @property
    def gate(self) -> Node:
        """Return the gate Node of this Transistor."""
        gate_id = self._state.transistor_gates[self.id_]
        return self._state.nodes[gate_id]

    @property
    def source(self) -> Node:
        """Return the source Node of this Transistor."""
        source_id = self._state.transistor_sources[self.id_]
        return self._state.nodes[source_id]

    @property
    def drain(self) -> Node:
        """Return the drain Node of this Transistor."""
        drain_id = self._state.transistor_drains[self.id_]
        return self._state.nodes[drain_id]

    @property
    def conducting(self) -> bool:
        """Return Transistor conduction state as determined by the Simulator."""
        return self._state.transistor_conducting[self.id_]

    # --------------------------------------------------------------------------
    # Debug Representation
    # --------------------------------------------------------------------------

    def __repr__(self) -> str:
        """Return a debug representation of this Transistor."""
        return (
            f"<Transistor id={self.id_} kind={self.kind!r} "
            f"gate={self.gate!r} source={self.source!r} "
            f"drain={self.drain!r} conducting={self.conducting!r}>"
        )
