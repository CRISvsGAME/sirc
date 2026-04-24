"""
SIRC Core Device Module.

LogicDevice handle and device-kind representation primitives.

Device-kind domain
------------------

Representation:
    A device kind is one of the canonical raw device-kind integers:

        GND_DEVICE_KIND   = 0
        VDD_DEVICE_KIND   = 1
        INPUT_DEVICE_KIND = 2
        PROBE_DEVICE_KIND = 3
        PORT_DEVICE_KIND  = 4

    LogicDeviceKind is the semantic IntEnum wrapper for canonical device kinds.

Meaning:
    GND   -> constant ZERO driver.
    VDD   -> constant ONE driver.
    INPUT -> externally mutable driver.
    PROBE -> observation terminal.
    PORT  -> reusable circuit/module boundary terminal.

    Device-kind values classify simulator-owned device records for topology,
    representation, serialization, and optional higher-level circuit assembly.

    Device-kind values do not define ownership, connectivity, or propagation
    behavior by themselves.

LogicDevice handle domain
-------------------------

Representation:
    A LogicDevice is a lightweight handle over a simulator-owned single-terminal
    device record.

        LogicDevice._state -> DeviceSimulatorState
        LogicDevice.id_    -> dense device id

    Runtime device data is stored in DeviceSimulatorState dense arrays:

        device_kinds[id_] -> raw device-kind integer
        device_nodes[id_] -> terminal node id

Meaning:
    LogicDevice does not own simulation state, connectivity, drivers, or
    propagation.

    LogicDevice reads simulator-owned arrays by id_ and exposes semantic/debug
    views:

        device.kind -> LogicDeviceKind
        device.node -> Node

Module contract
---------------

Execution contract:
    Simulator hot paths use dense arrays, raw device ids, raw device-kind
    integers, raw node ids, and raw logic values directly.

    LogicDevice and LogicDeviceKind are representation/debug/serialization
    helpers. They are not simulator hot-path objects.

Ownership contract:
    DeviceSimulatorState owns runtime device data.
    DeviceSimulator owns creation, mutation, connectivity, and propagation.
    LogicDevice owns only a state reference and device id.
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
    """Semantic IntEnum wrapper for canonical device kinds."""

    GND = GND_DEVICE_KIND
    VDD = VDD_DEVICE_KIND
    INPUT = INPUT_DEVICE_KIND
    PROBE = PROBE_DEVICE_KIND
    PORT = PORT_DEVICE_KIND

    def __repr__(self) -> str:
        """Return debug representation."""
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
