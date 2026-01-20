"""SIRC Device Simulator Dependency Module."""

from __future__ import annotations
from ..core.node import Node, NodeKind
from ..core.logic_device import LogicDevice, VDD, GND, Input, Probe, Port
from ..core.transistor import Transistor, NMOS, PMOS


class IdentificationFactory:
    """Identification Factory"""

    __slots__ = ("_next_node_id", "_next_device_id", "_next_transistor_id")

    def __init__(self) -> None:
        """Initialize the Identification Factory."""
        self._next_node_id: int = 0
        self._next_device_id: int = 0
        self._next_transistor_id: int = 0

    def allocate_node_id(self) -> int:
        """Allocate a unique Node ID."""
        node_id = self._next_node_id
        self._next_node_id += 1
        return node_id

    def allocate_device_id(self) -> int:
        """Allocate a unique Device ID."""
        device_id = self._next_device_id
        self._next_device_id += 1
        return device_id

    def allocate_transistor_id(self) -> int:
        """Allocate a unique Transistor ID."""
        transistor_id = self._next_transistor_id
        self._next_transistor_id += 1
        return transistor_id


class NodeFactory:
    """Node Factory"""

    __slots__ = ("_id_factory",)

    def __init__(self, id_factory: IdentificationFactory) -> None:
        """Initialize the Node Factory."""
        self._id_factory = id_factory

    def create_base_node(self) -> Node:
        """Create a new BASE Node with a unique ID."""
        node_id = self._id_factory.allocate_node_id()
        return Node(node_id, NodeKind.BASE)

    def create_gate_node(self) -> Node:
        """Create a new GATE Node with a unique ID."""
        node_id = self._id_factory.allocate_node_id()
        return Node(node_id, NodeKind.GATE)


class LogicDeviceFactory:
    """Logic Device Factory"""

    __slots__ = ("_id_factory", "_node_factory")

    def __init__(
        self, id_factory: IdentificationFactory, node_factory: NodeFactory
    ) -> None:
        """Initialize the Logic Device Factory."""
        self._id_factory = id_factory
        self._node_factory = node_factory

    def create_vdd(self) -> VDD:
        """Create a new VDD device with a unique ID and terminal Node."""
        device_id = self._id_factory.allocate_device_id()
        node = self._node_factory.create_base_node()
        return VDD(device_id, node)

    def create_gnd(self) -> GND:
        """Create a new GND device with a unique ID and terminal Node."""
        device_id = self._id_factory.allocate_device_id()
        node = self._node_factory.create_base_node()
        return GND(device_id, node)

    def create_input(self) -> Input:
        """Create a new Input device with a unique ID and terminal Node."""
        device_id = self._id_factory.allocate_device_id()
        node = self._node_factory.create_base_node()
        return Input(device_id, node)

    def create_probe(self) -> Probe:
        """Create a new Probe device with a unique ID and terminal Node."""
        device_id = self._id_factory.allocate_device_id()
        node = self._node_factory.create_base_node()
        return Probe(device_id, node)

    def create_port(self) -> Port:
        """Create a new Port device with a unique ID and terminal Node."""
        device_id = self._id_factory.allocate_device_id()
        node = self._node_factory.create_base_node()
        return Port(device_id, node)


class TransistorFactory:
    """Transistor Factory"""

    __slots__ = ("_id_factory", "_node_factory")

    def __init__(
        self, id_factory: IdentificationFactory, node_factory: NodeFactory
    ) -> None:
        """Initialize the Transistor Factory."""
        self._id_factory = id_factory
        self._node_factory = node_factory

    def create_nmos(self) -> NMOS:
        """Create a new NMOS transistor with a unique ID and terminal Nodes."""
        transistor_id = self._id_factory.allocate_transistor_id()
        gate = self._node_factory.create_gate_node()
        source = self._node_factory.create_base_node()
        drain = self._node_factory.create_base_node()
        return NMOS(transistor_id, gate, source, drain)

    def create_pmos(self) -> PMOS:
        """Create a new PMOS transistor with a unique ID and terminal Nodes."""
        transistor_id = self._id_factory.allocate_transistor_id()
        gate = self._node_factory.create_gate_node()
        source = self._node_factory.create_base_node()
        drain = self._node_factory.create_base_node()
        return PMOS(transistor_id, gate, source, drain)


# pylint: disable=too-few-public-methods
class DeviceSimulatorState:
    """Device Simulator State"""

    __slots__ = ("nodes", "devices", "transistors", "wires")

    def __init__(self) -> None:
        """Initialize the Device Simulator State."""
        self.nodes: list[Node] = []
        self.devices: list[LogicDevice] = []
        self.transistors: list[Transistor] = []
        self.wires: list[tuple[int, int]] = []
