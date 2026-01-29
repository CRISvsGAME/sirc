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
        self._state.devices.append(device)
        self._state.nodes.append(device.terminal)

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

        self._state.wires.append((a, b))

    def _reference_build_topology(self) -> None:
        """Reference Build Topology"""

    def _reference_tick(self) -> None:
        """Reference Tick"""

    def _compiled_build_topology(self) -> None:
        """Compiled Build Topology"""

    def _compiled_tick(self) -> None:
        """Compiled Tick"""

    def build_topology(self) -> None:
        """Build Topology"""
        self._reference_build_topology()

    def tick(self) -> None:
        """Tick"""
        self._reference_tick()
