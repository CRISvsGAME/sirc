"""
SIRC Core Device Module.

Defines the LogicDevice base class and several common logic devices: VDD, GND,
Input, Probe, and Port. A LogicDevice owns exactly one terminal Node and may
drive a single LogicValue onto that Node. LogicDevices do not perform any logic
resolution. The Simulator handles all evaluation and propagation.
"""

from __future__ import annotations
from abc import ABC
from sirc.core.logic import LogicValue
from sirc.core.node import Node


class LogicDevice(ABC):
    """
    Abstract class for single-terminal logic devices.

    Each LogicDevice owns one Node and may drive one LogicValue onto it. This
    class defines only structural information. The Simulator is responsible for
    injecting driver values and resolving all electrical behaviour.
    """

    __slots__ = ("_node", "_value")

    def __init__(self) -> None:
        """Create a new LogicDevice with a terminal Node and default Z value."""
        self._node = Node()
        self._value = LogicValue.Z

    # --------------------------------------------------------------------------
    # Properties
    # --------------------------------------------------------------------------

    @property
    def terminal(self) -> Node:
        """Return the terminal Node of this LogicDevice."""
        return self._node

    @property
    def value(self) -> LogicValue:
        """Return the LogicValue driven by this LogicDevice."""
        return self._value
