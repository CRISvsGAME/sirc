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

    __slots__ = ("_node",)

    def __init__(self) -> None:
        """Create a new LogicDevice with a terminal Node and default Z value."""
        self._node = Node()

    # --------------------------------------------------------------------------
    # Properties
    # --------------------------------------------------------------------------

    @property
    def terminal(self) -> Node:
        """Return the terminal Node of this LogicDevice."""
        return self._node

    @property
    def terminal_default_value(self) -> LogicValue:
        """Return the default LogicValue of the terminal Node."""
        return self._node.default_value

    @property
    def terminal_resolved_value(self) -> LogicValue:
        """Return the resolved LogicValue of the terminal Node."""
        return self._node.resolved_value

    # --------------------------------------------------------------------------
    # Debug Representation
    # --------------------------------------------------------------------------

    def __repr__(self) -> str:
        """Return a debug representation of this LogicDevice."""
        cls = self.__class__.__name__
        return (
            f"<{cls} terminal_default_value={self._node.default_value!r} "
            f"terminal_resolved_value={self.terminal_resolved_value!r}>"
        )


# ------------------------------------------------------------------------------
# Power Rail
# ------------------------------------------------------------------------------


class VDD(LogicDevice):
    """
    Logic "1" power rail device.

    This device permanently drives its terminal Node with LogicValue.ONE.
    """

    def __init__(self) -> None:
        super().__init__()
        self._node.set_default_value(LogicValue.ONE)


# ------------------------------------------------------------------------------
# Ground Rail
# ------------------------------------------------------------------------------


class GND(LogicDevice):
    """
    Logic "0" ground rail device.

    This device permanently drives its terminal Node with LogicValue.ZERO.
    """

    def __init__(self) -> None:
        super().__init__()
        self._node.set_default_value(LogicValue.ZERO)


# ------------------------------------------------------------------------------
# Input Device
# ------------------------------------------------------------------------------


class Input(LogicDevice):
    """
    Logic signal input device.

    This device allows external setting of its driven LogicValue.
    """

    def set_value(self, value: LogicValue) -> None:
        """Set the LogicValue driven by this Input device."""
        self._node.set_default_value(value)


# ------------------------------------------------------------------------------
# Probe Device
# ------------------------------------------------------------------------------


class Probe(LogicDevice):
    """
    Logic signal probe device.

    This device allows sampling of the LogicValue present on its terminal Node.
    """

    def sample(self) -> LogicValue:
        """Return the current resolved LogicValue of the terminal Node."""
        return self._node.resolved_value


# ------------------------------------------------------------------------------
# Port Device
# ------------------------------------------------------------------------------


class Port(LogicDevice):
    """
    Logic signal port device.

    This device is a passive connection point for linking circuit Nodes.
    """
