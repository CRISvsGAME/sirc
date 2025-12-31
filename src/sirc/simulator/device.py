"""
SIRC Device Simulator Module.

Provides the DeviceSimulator class, responsible for evaluating a circuit
composed of Nodes, LogicDevices, and Transistors. The simulator performs
fixed-point iteration to resolve driver values, establish dynamic conduction
paths, and propagate LogicValues across connected node-groups.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Iterable
from sirc.core.logic import LogicValue
from sirc.core.node import Node
from sirc.core.device import LogicDevice
from sirc.core.transistor import Transistor


@dataclass(eq=False)
class NodeComponent:
    """Node Component"""

    nodes: set[Node] = field(default_factory=set[Node])


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
        self._devices: set[LogicDevice] = set()
        self._nodes: set[Node] = set()
        self._node_components: set[NodeComponent] = set()
        self._dirty_node_components: set[NodeComponent] = set()
        self._find_node_component: dict[Node, NodeComponent] = {}
        self._gates: set[Node] = set()
        self._transistors: set[Transistor] = set()
        self._dirty_transistors: set[Transistor] = set()
        self._find_transistor: dict[Node, Transistor] = {}
        self._dirty: bool = True

    # --------------------------------------------------------------------------
    # Device Registration
    # --------------------------------------------------------------------------

    def register_device(self, device: LogicDevice) -> None:
        """
        Register a LogicDevice and its terminal Node with the simulator.

        Args:
            device: The LogicDevice to register.
        """
        self._devices.add(device)
        self._nodes.add(device.terminal)

    def register_devices(self, devices: Iterable[LogicDevice]) -> None:
        """
        Register multiple LogicDevices and terminal Nodes with the simulator.

        Args:
            devices: An iterable of LogicDevices to register.
        """
        for device in devices:
            self.register_device(device)

    def register_transistor(self, transistor: Transistor) -> None:
        """
        Register a Transistor and its terminal Nodes with the simulator.

        Args:
            transistor: The Transistor to register.
        """
        self._transistors.add(transistor)
        self._nodes.update(transistor.terminals())
        self._gates.add(transistor.gate)
        self._find_transistor[transistor.gate] = transistor

    def register_transistors(self, transistors: Iterable[Transistor]) -> None:
        """
        Register multiple Transistors and terminal Nodes with the simulator.

        Args:
            transistors: An iterable of Transistors to register.
        """
        for transistor in transistors:
            self.register_transistor(transistor)

    def unregister_device(self, device: LogicDevice) -> None:
        """
        Unregister a LogicDevice and its terminal Node from the simulator.

        Args:
            device: The LogicDevice to unregister.
        """
        self._devices.discard(device)
        self._nodes.discard(device.terminal)

    def unregister_devices(self, devices: Iterable[LogicDevice]) -> None:
        """
        Unregister multiple LogicDevices and terminal Nodes from the simulator.

        Args:
            devices: An iterable of LogicDevices to unregister.
        """
        for device in devices:
            self.unregister_device(device)

    def unregister_transistor(self, transistor: Transistor) -> None:
        """
        Unregister a Transistor and its terminal Nodes from the simulator.

        Args:
            transistor: The Transistor to unregister.
        """
        self._transistors.discard(transistor)
        self._nodes.difference_update(transistor.terminals())
        self._gates.discard(transistor.gate)
        self._find_transistor.pop(transistor.gate, None)

    def unregister_transistors(self, transistors: Iterable[Transistor]) -> None:
        """
        Unregister multiple Transistors and terminal Nodes from the simulator.

        Args:
            transistors: An iterable of Transistors to unregister.
        """
        for transistor in transistors:
            self.unregister_transistor(transistor)

    # --------------------------------------------------------------------------
    # Topology Management
    # --------------------------------------------------------------------------

    def build_topology(self) -> None:
        """Build Topology"""
        self._node_components: set[NodeComponent] = set()
        self._dirty_node_components: set[NodeComponent] = set()
        self._find_node_component: dict[Node, NodeComponent] = {}
        self._dirty_transistors: set[Transistor] = set()
        self._dirty: bool = True
        self._build_node_components()

    # --------------------------------------------------------------------------
    # Logical Connection
    # --------------------------------------------------------------------------

    def connect(self, a: Node, b: Node) -> None:
        """
        Create a bidirectional connection between two Nodes.

        Args:
            a: The first Node.
            b: The second Node.
        """
        a.connect(b)

    def disconnect(self, a: Node, b: Node) -> None:
        """
        Remove the bidirectional connection between two Nodes.

        Args:
            a: The first Node.
            b: The second Node.
        """
        a.disconnect(b)

    # --------------------------------------------------------------------------
    # Simulation Execution
    # --------------------------------------------------------------------------

    def _build_node_components(self) -> None:
        """Build Node Components"""
        visited: set[Node] = set()
        stack: list[Node] = []

        for start in self._nodes:
            if start in visited:
                continue

            stack.append(start)
            comp: NodeComponent = NodeComponent()

            while stack:
                node = stack.pop()

                if node in visited:
                    continue

                visited.add(node)
                comp.nodes.add(node)
                self._find_node_component[node] = comp

                for neighbor in node.get_connections():
                    if neighbor not in visited:
                        stack.append(neighbor)

            self._node_components.add(comp)
            self._dirty_node_components.add(comp)

    def _resolve_node_components(self) -> None:
        """Resolve Node Components"""
        for group in self._dirty_node_components:
            drivers: set[LogicValue] = set()

            for node in group.nodes:
                drivers.add(node.default_value)

            resolved_value: LogicValue = LogicValue.resolve_all(drivers)

            for node in group.nodes:
                if node in self._gates and resolved_value is not node.resolved_value:
                    self._dirty_transistors.add(self._find_transistor[node])

                node.set_resolved_value(resolved_value)

        self._dirty_node_components.clear()

    def _update_transistor_connections(self) -> None:
        """Update Transistor Connections"""
        for transistor in self._dirty_transistors:
            a, b = transistor.conduction_nodes()

            if transistor.is_conducting():
                a.connect(b)
            else:
                a.disconnect(b)

            self._dirty_node_components.add(self._find_node_component[a])
            self._dirty_node_components.add(self._find_node_component[b])

        self._dirty_transistors.clear()

    def _update_node_components(self) -> None:
        """Update Node Components"""
        groups_to_update: list[NodeComponent] = []
        groups_to_remove: list[NodeComponent] = []
        visited: set[Node] = set()
        stack: list[Node] = []

        for group in self._dirty_node_components:
            for start in group.nodes:
                if start in visited:
                    continue

                stack.append(start)
                comp: NodeComponent = NodeComponent()

                while stack:
                    node = stack.pop()

                    if node in visited:
                        continue

                    visited.add(node)
                    comp.nodes.add(node)
                    self._find_node_component[node] = comp

                    for neighbor in node.get_connections():
                        if neighbor not in visited:
                            stack.append(neighbor)

                groups_to_update.append(comp)

            groups_to_remove.append(group)

        self._node_components.difference_update(groups_to_remove)
        self._node_components.update(groups_to_update)
        self._dirty_node_components.clear()
        self._dirty_node_components.update(groups_to_update)

        if not groups_to_update:
            self._dirty = False

    def tick(self) -> None:
        """Tick"""
        while self._dirty:
            self._resolve_node_components()
            self._update_transistor_connections()
            self._update_node_components()
