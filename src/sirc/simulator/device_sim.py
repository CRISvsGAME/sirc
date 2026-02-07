"""
SIRC Device Simulator Module.

Provides the DeviceSimulator class, responsible for evaluating a circuit
composed of Nodes, LogicDevices, and Transistors. The simulator performs
fixed-point iteration to resolve driver values, establish dynamic conduction
paths, and propagate LogicValues across connected node-groups.
"""

from __future__ import annotations
from ..core.node import Node
from ..core.logic_device import LogicDevice, VDD, GND, Input, Probe, Port
from ..core.transistor import Transistor, NMOS, PMOS
from .device_dep import (
    IdentificationFactory,
    NodeFactory,
    LogicDeviceFactory,
    TransistorFactory,
    DeviceSimulatorState,
)


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

    # --------------------------------------------------------------------------
    # Device Creation and Registration
    # --------------------------------------------------------------------------

    def _register_device(self, device: LogicDevice) -> None:
        """
        Register a LogicDevice and its terminal Node. Must be called exactly
        once per created device; registration order must match allocated IDs.
        """
        state = self._state
        state.devices.append(device)
        state.nodes.append(device.terminal)

    def create_vdd(self) -> VDD:
        """Create and register a new VDD device."""
        vdd_device = self._device_f.create_vdd()
        self._register_device(vdd_device)
        return vdd_device

    def create_gnd(self) -> GND:
        """Create and register a new GND device."""
        gnd_device = self._device_f.create_gnd()
        self._register_device(gnd_device)
        return gnd_device

    def create_input(self) -> Input:
        """Create and register a new Input device."""
        input_device = self._device_f.create_input()
        self._register_device(input_device)
        return input_device

    def create_probe(self) -> Probe:
        """Create and register a new Probe device."""
        probe_device = self._device_f.create_probe()
        self._register_device(probe_device)
        return probe_device

    def create_port(self) -> Port:
        """Create and register a new Port device."""
        port_device = self._device_f.create_port()
        self._register_device(port_device)
        return port_device

    # --------------------------------------------------------------------------
    # Transistor Creation and Registration
    # --------------------------------------------------------------------------

    def _register_transistor(self, transistor: Transistor) -> None:
        """
        Register a Transistor and its terminal Nodes. Must be called exactly
        once per created transistor; registration order must match allocated IDs.
        """
        state = self._state
        state.transistors.append(transistor)
        state.nodes.extend(transistor.terminals())

    def create_nmos(self) -> NMOS:
        """Create and register a new NMOS transistor."""
        nmos = self._transistor_f.create_nmos()
        self._register_transistor(nmos)
        return nmos

    def create_pmos(self) -> PMOS:
        """Create and register a new PMOS transistor."""
        pmos = self._transistor_f.create_pmos()
        self._register_transistor(pmos)
        return pmos

    # --------------------------------------------------------------------------
    # Logical Connection
    # --------------------------------------------------------------------------

    def connect(self, node_a: Node, node_b: Node) -> None:
        """Record an undirected wire connection between two Nodes."""
        a = node_a.id
        b = node_b.id

        if a == b:
            return

        if a > b:
            a, b = b, a

        edge = (a, b)
        state = self._state
        wires_cache = state.wires_cache

        if edge not in wires_cache:
            wires = state.wires
            index = len(wires)
            wires.append(edge)
            wires_cache[edge] = index

    def disconnect(self, node_a: Node, node_b: Node) -> None:
        """Remove an undirected wire connection between two Nodes."""
        a = node_a.id
        b = node_b.id

        if a == b:
            return

        if a > b:
            a, b = b, a

        edge = (a, b)
        state = self._state
        wires_cache = state.wires_cache
        index = wires_cache.pop(edge, None)

        if index is not None:
            wires = state.wires
            last_edge = wires.pop()
            if index < len(wires):
                wires[index] = last_edge
                wires_cache[last_edge] = index

    def _reference_build_static_topology(self) -> None:
        """Reference Build Static Topology"""
        state = self._state
        node_count = len(state.nodes)

        static_neighbors: list[list[int]] = [[] for _ in range(node_count)]
        dynamic_neighbors: list[list[int]] = [[] for _ in range(node_count)]

        for a, b in state.wires:
            static_neighbors[a].append(b)
            static_neighbors[b].append(a)

        state.reference_static_neighbors = static_neighbors
        state.reference_dynamic_neighbors = dynamic_neighbors

    def _reference_build_dynamic_topology(self) -> None:
        """Reference Build Dynamic Topology"""
        state = self._state
        transistors = state.transistors
        dynamic_neighbors = state.reference_dynamic_neighbors

        for neighbors in dynamic_neighbors:
            neighbors.clear()

        for transistor in transistors:
            if transistor.is_conducting():
                source_id = transistor.source.id
                drain_id = transistor.drain.id
                dynamic_neighbors[source_id].append(drain_id)
                dynamic_neighbors[drain_id].append(source_id)

    def _reference_build_components(self) -> None:
        """Reference Build Components"""
        state = self._state
        node_count = len(state.nodes)

        if not node_count:
            state.reference_components = []
            state.reference_component_id = []
            return

        static_neighbors = state.reference_static_neighbors
        dynamic_neighbors = state.reference_dynamic_neighbors
        visited = [False] * node_count
        components: list[list[int]] = []
        component_id = [-1] * node_count

        cid = 0

        for start in range(node_count):
            if visited[start]:
                continue

            visited[start] = True
            stack = [start]
            component: list[int] = []

            while stack:
                node = stack.pop()
                component.append(node)
                component_id[node] = cid

                for neighbor in static_neighbors[node]:
                    if not visited[neighbor]:
                        visited[neighbor] = True
                        stack.append(neighbor)

                for neighbor in dynamic_neighbors[node]:
                    if not visited[neighbor]:
                        visited[neighbor] = True
                        stack.append(neighbor)

            components.append(component)

            cid += 1

        state.reference_components = components
        state.reference_component_id = component_id

    def _reference_tick(self) -> None:
        """Reference Tick"""
        self._reference_build_dynamic_topology()
        self._reference_build_components()

    def _compiled_build_topology(self) -> None:
        """Compiled Build Topology"""

    def _compiled_tick(self) -> None:
        """Compiled Tick"""

    def build_topology(self) -> None:
        """Build Topology"""
        self._reference_build_static_topology()

    def tick(self) -> None:
        """Tick"""
        self._reference_tick()
