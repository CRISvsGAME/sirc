"""
SIRC Core Device Module.

Defines LogicDevice, a lightweight public handle for simulator-owned
single-terminal devices.

A LogicDevice is associated with exactly one terminal Node. The device kind
defines whether it represents GND, VDD, Input, Probe, or Port. LogicDevice does
not own simulation state; runtime data is stored in DeviceSimulatorState dense
arrays and read through this object's id_.
"""

from __future__ import annotations
from enum import IntEnum
from typing import Final, TYPE_CHECKING
from .node import Node

if TYPE_CHECKING:
    from ..simulator import DeviceSimulatorState

GND_DEVICE_KIND: Final[int] = 0
VDD_DEVICE_KIND: Final[int] = 1
INPUT_DEVICE_KIND: Final[int] = 2
PROBE_DEVICE_KIND: Final[int] = 3
PORT_DEVICE_KIND: Final[int] = 4


class LogicDeviceKind(IntEnum):
    """Logic Device Kind"""

    GND = GND_DEVICE_KIND
    VDD = VDD_DEVICE_KIND
    INPUT = INPUT_DEVICE_KIND
    PROBE = PROBE_DEVICE_KIND
    PORT = PORT_DEVICE_KIND

    def __repr__(self) -> str:
        """Return readable debug representation."""
        return f"LogicDeviceKind.{self.name}"


class LogicDevice:
    """
    A lightweight public handle for a simulator-owned single-terminal device.

    LogicDevice does not own runtime state. Its kind and terminal Node are
    stored in DeviceSimulatorState dense arrays. The simulator is responsible
    for creation, mutation, resolution, and propagation.
    """

    __slots__ = ("_state", "id_")

    def __init__(self, state: DeviceSimulatorState, device_id: int) -> None:
        """Create a LogicDevice handle bound to simulator state."""
        self._state: DeviceSimulatorState = state
        self.id_: int = device_id

    @property
    def kind(self) -> LogicDeviceKind:
        """Return the LogicDeviceKind of this LogicDevice."""
        return LogicDeviceKind(self._state.device_kinds[self.id_])

    @property
    def node(self) -> Node:
        """Return the terminal Node of this LogicDevice."""
        node_id = self._state.device_nodes[self.id_]
        return self._state.nodes[node_id]

    # --------------------------------------------------------------------------
    # Debug Representation
    # --------------------------------------------------------------------------

    def __repr__(self) -> str:
        """Return a debug representation of this LogicDevice."""
        return f"<LogicDevice id={self.id_} kind={self.kind!r} node={self.node!r}>"
