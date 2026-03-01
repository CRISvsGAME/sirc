"""
SIRC Core Device Module.

Defines the LogicDevice base class and several common logic devices: VDD, GND,
Input, Probe, and Port. A LogicDevice is associated with exactly one terminal
Node and may drive a single LogicValue onto it. LogicDevices do not perform any
logic resolution; all evaluation and propagation are handled by the Simulator.
"""

from __future__ import annotations
from enum import IntEnum
from .logic_value import LogicValue, ZERO, ONE
from .node import Node


class LogicDeviceKind(IntEnum):
    """Logic Device Kind"""

    GND = 0
    VDD = 1
    INPUT = 2
    PROBE = 3
    PORT = 4

    def __str__(self) -> str:
        """Return compact string form ('0', '1', '2', '3', '4')."""
        return str(self.value)

    def __repr__(self) -> str:
        """Return readable debug representation."""
        return f"LogicDeviceKind.{self.name}"


GND_DEVICE_KIND: LogicDeviceKind = LogicDeviceKind.GND
VDD_DEVICE_KIND: LogicDeviceKind = LogicDeviceKind.VDD
INPUT_DEVICE_KIND: LogicDeviceKind = LogicDeviceKind.INPUT
PROBE_DEVICE_KIND: LogicDeviceKind = LogicDeviceKind.PROBE
PORT_DEVICE_KIND: LogicDeviceKind = LogicDeviceKind.PORT


# pylint: disable=too-few-public-methods
class LogicDevice:
    """
    Base class for single-terminal logic devices.

    Each LogicDevice is associated with one terminal Node and may drive one
    LogicValue onto it. This class defines only structural information. The
    Simulator is responsible for resolving all electrical behaviour.
    """

    __slots__ = ("id_", "kind", "node")

    def __init__(self, device_id: int, kind: LogicDeviceKind, node: Node) -> None:
        """Create a new LogicDevice with a terminal Node."""
        self.id_: int = device_id
        self.kind: LogicDeviceKind = kind
        self.node: Node = node

    # --------------------------------------------------------------------------
    # Debug Representation
    # --------------------------------------------------------------------------

    def __repr__(self) -> str:
        """Return a debug representation of this LogicDevice."""
        name = self.__class__.__name__
        return (
            f"<{name} id={self.id_} kind={self.kind!r} "
            f"terminal_default_value={self.node.default_value!r} "
            f"terminal_resolved_value={self.node.resolved_value!r}>"
        )


# ------------------------------------------------------------------------------
# Power Rail
# ------------------------------------------------------------------------------


class VDD(LogicDevice):
    """
    Logic "1" power rail device.

    This device permanently drives its terminal Node with LogicValue.ONE.
    """

    def __init__(self, device_id: int, node: Node) -> None:
        super().__init__(device_id, VDD_DEVICE_KIND, node)
        self.node.default_value = ONE


# ------------------------------------------------------------------------------
# Ground Rail
# ------------------------------------------------------------------------------


class GND(LogicDevice):
    """
    Logic "0" ground rail device.

    This device permanently drives its terminal Node with LogicValue.ZERO.
    """

    def __init__(self, device_id: int, node: Node) -> None:
        super().__init__(device_id, GND_DEVICE_KIND, node)
        self.node.default_value = ZERO


# ------------------------------------------------------------------------------
# Input Device
# ------------------------------------------------------------------------------


class Input(LogicDevice):
    """
    Logic signal input device.

    This device allows external setting of its driven LogicValue.
    """

    def __init__(self, device_id: int, node: Node) -> None:
        super().__init__(device_id, INPUT_DEVICE_KIND, node)

    def set_value(self, value: LogicValue) -> None:
        """Set the LogicValue driven by this Input device."""
        self.node.default_value = value


# ------------------------------------------------------------------------------
# Probe Device
# ------------------------------------------------------------------------------


class Probe(LogicDevice):
    """
    Logic signal probe device.

    This device allows sampling of the LogicValue present on its terminal Node.
    """

    def __init__(self, device_id: int, node: Node) -> None:
        super().__init__(device_id, PROBE_DEVICE_KIND, node)

    def sample(self) -> LogicValue:
        """Return the current resolved LogicValue of the terminal Node."""
        return self.node.resolved_value


# ------------------------------------------------------------------------------
# Port Device
# ------------------------------------------------------------------------------


class Port(LogicDevice):
    """
    Logic signal port device.

    This device is a passive connection point for linking circuit Nodes.
    """

    def __init__(self, device_id: int, node: Node) -> None:
        super().__init__(device_id, PORT_DEVICE_KIND, node)
