"""
SIRC Device Simulator Module.

Provides the DeviceSimulator class, responsible for evaluating a circuit
composed of Nodes, LogicDevices, and Transistors. The simulator performs
fixed-point iteration to resolve driver values, establish dynamic conduction
paths, and propagate LogicValues across connected node-groups.
"""

from __future__ import annotations
from sirc.core.node import Node
from sirc.core.device import LogicDevice
from sirc.core.transistor import Transistor


class DeviceSimulator:
    """
    Simulator for evaluating SIRC logic devices and transistors.

    The DeviceSimulator maintains registered devices, transistors, and nodes.
    Each tick clears drivers, applies device outputs, resolves node-groups via
    DFS, and updates dynamic connectivity created by transistor conduction.
    Fixed-point iteration continues until the circuit reaches a stable state.
    """

    def __init__(self) -> None:
        """SIRC"""
        self.devices: set[LogicDevice] = set()
        self.transistors: set[Transistor] = set()
        self.nodes: set[Node] = set()
