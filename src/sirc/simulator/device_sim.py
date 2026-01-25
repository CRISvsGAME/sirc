"""
SIRC Device Simulator Module.

Provides the DeviceSimulator class, responsible for evaluating a circuit
composed of Nodes, LogicDevices, and Transistors. The simulator performs
fixed-point iteration to resolve driver values, establish dynamic conduction
paths, and propagate LogicValues across connected node-groups.
"""

from __future__ import annotations
from .device_dep import (
    IdentificationFactory,
    NodeFactory,
    LogicDeviceFactory,
    TransistorFactory,
    DeviceSimulatorState,
)


# pylint: disable=too-few-public-methods
class DeviceSimulator:
    """
    Simulator for evaluating SIRC logic devices and transistors.

    The DeviceSimulator maintains registered devices, transistors, and nodes.
    Each tick clears drivers, applies device outputs, resolves node-groups via
    DFS, and updates dynamic connectivity created by transistor conduction.
    Fixed-point iteration continues until the circuit reaches a stable state.
    """

    __slots__ = ("_id_f", "_node_f", "_device_f", "_transistor_f", "_state")

    def __init__(self) -> None:
        """Initialize factories and empty simulator state."""
        self._id_f = IdentificationFactory()
        self._node_f = NodeFactory(self._id_f)
        self._device_f = LogicDeviceFactory(self._id_f, self._node_f)
        self._transistor_f = TransistorFactory(self._id_f, self._node_f)
        self._state = DeviceSimulatorState()
