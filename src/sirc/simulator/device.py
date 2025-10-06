"""
SIRC Device Simulator Module.

Provides the DeviceSimulator class, responsible for evaluating a circuit
composed of Nodes, LogicDevices, and Transistors. The simulator performs
fixed-point iteration to resolve driver values, establish dynamic conduction
paths, and propagate LogicValues across connected node-groups.
"""

from __future__ import annotations
from typing import Iterable
from sirc.core.logic import LogicValue
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

    # --------------------------------------------------------------------------
    # Device Registration
    # --------------------------------------------------------------------------

    def register_device(self, device: LogicDevice) -> None:
        """
        Register a LogicDevice and its terminal Node with the simulator.

        Args:
            device: The LogicDevice to register.
        """
        self.devices.add(device)
        self.nodes.add(device.terminal)

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
        self.transistors.add(transistor)
        self.nodes.update(transistor.terminals())

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
        self.devices.discard(device)
        self.nodes.discard(device.terminal)

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
        self.transistors.discard(transistor)
        self.nodes.difference_update(transistor.terminals())

    def unregister_transistors(self, transistors: Iterable[Transistor]) -> None:
        """
        Unregister multiple Transistors and terminal Nodes from the simulator.

        Args:
            transistors: An iterable of Transistors to unregister.
        """
        for transistor in transistors:
            self.unregister_transistor(transistor)

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

    def _dfs(self, collection: Iterable[Node]) -> list[set[Node]]:
        """
        Perform depth-first search to identify connected node-groups.

        Args:
            collection: Iterable of Nodes to explore.

        Returns:
            List of sets, each containing Nodes in a connected group.
        """
        visited: set[Node] = set()
        stack: list[Node] = []
        groups: list[set[Node]] = []

        for start in collection:
            if start in visited:
                continue

            stack.append(start)
            group: set[Node] = set()

            while stack:
                node = stack.pop()

                if node in visited:
                    continue

                visited.add(node)
                group.add(node)

                for neighbor in node.get_connections():
                    if neighbor not in visited:
                        stack.append(neighbor)

            groups.append(group)

        return groups

    def _resolve_groups(self, groups: list[set[Node]]) -> None:
        """
        Resolve LogicValues for each connected node-group.

        Args:
            groups: List of node-groups to resolve.
        """
        for group in groups:
            drivers: list[LogicValue] = []

            for node in group:
                drivers.extend(node.get_drivers())

            resolved_value: LogicValue = LogicValue.resolve_all(drivers)

            for node in group:
                node.set_resolved_value(resolved_value)

    def tick(self) -> None:
        """
        Execute a simulation tick to update device states and connectivity.

        This method performs the following steps:
            1. Clears all Node drivers.
            2. Applies LogicDevice outputs to their terminal Nodes.
            3. Repeatedly:
                a. Identifies connected node-groups via DFS.
                b. Resolves LogicValues for each group.
                c. Updates transistor conduction paths.
            4. Continues until a fixed-point state is reached.
        """
        for node in self.nodes:
            node.clear_drivers()

        for device in self.devices:
            device.terminal.add_driver(device.value)

        while True:
            groups = self._dfs(self.nodes)
            self._resolve_groups(groups)
            fixed_point = True

            for transistor in self.transistors:
                a, b = transistor.conduction_nodes()
                if transistor.is_conducting():
                    if a not in b.get_connections():
                        transistor.source.connect(transistor.drain)
                        fixed_point = False
                else:
                    if a in b.get_connections():
                        transistor.source.disconnect(transistor.drain)
                        fixed_point = False

            if fixed_point:
                break
