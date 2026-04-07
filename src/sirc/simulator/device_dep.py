"""SIRC Device Simulator Dependency Module."""

from __future__ import annotations
from ..core.node import Node
from ..core.logic_device import LogicDevice
from ..core.transistor import Transistor


# pylint: disable=too-few-public-methods, too-many-instance-attributes
class DeviceSimulatorState:
    """
    Device Simulator State

    Centralised mutable state owned by DeviceSimulator. This structure stores
    both simulation entities and graph representations used during evaluation.

    Properties
    ----------
    nodes:
        Dense list of Node handles.
        Invariant: nodes[i].id_ == i.
        Nodes do not own runtime state; they read from node_* arrays.

    node_kinds:
        Dense array storing raw NodeKind values.
        Invariant: node_kinds[node_id] is BASE_NODE_KIND or GATE_NODE_KIND.

    node_default_values:
        Dense array storing raw LogicValue-compatible integers for each Node.
        Used as the node's baseline driver contribution before resolution.

    node_resolved_values:
        Dense array storing raw LogicValue-compatible integers for each Node.
        Written by the simulator during evaluation and exposed through Node.

    devices:
        Dense list of LogicDevice handles.
        Invariant: devices[i].id_ == i.
        Devices do not own runtime state; they read from device_* arrays.

    device_kinds:
        Dense array storing raw LogicDeviceKind values.
        Invariant: device_kinds[device_id] identifies GND, VDD, INPUT, PROBE, or PORT.

    device_nodes:
        Dense array mapping each LogicDevice to its terminal Node.
        Invariant: device_nodes[device_id] -> node_id.

    transistors:
        Dense list of Transistor handles.
        Invariant: transistors[i].id_ == i.
        Transistors do not own runtime state; they read from transistor_* arrays.

    transistor_kinds:
        Dense array storing raw TransistorKind values.
        Invariant: transistor_kinds[transistor_id] is NMOS_TRANSISTOR_KIND or PMOS_TRANSISTOR_KIND.

    transistor_gates:
        Dense array mapping each Transistor to its gate Node.
        Invariant: transistor_gates[transistor_id] -> gate node_id.

    transistor_sources:
        Dense array mapping each Transistor to its source-side channel Node.
        Invariant: transistor_sources[transistor_id] -> source node_id.

    transistor_drains:
        Dense array mapping each Transistor to its drain-side channel Node.
        Invariant: transistor_drains[transistor_id] -> drain node_id.

    transistor_conducting:
        Dense array storing current simulator-computed conduction state.
        Invariant: transistor_conducting[transistor_id] is True when the
        source-drain channel is currently connected.

    wire_edges:
        AoS static undirected edge list for user-defined Node connections.
        Each edge is stored canonically as (min_node_id, max_node_id).

    wire_edge_index:
        Mapping from canonical AoS edge tuple to index in wire_edges.
        Provides O(1) lookup, deduplication, and swap-remove deletion.

    wire_edge_a:
        SoA static wire edge endpoint array.
        Stores the first canonical node ID for each wire edge.

    wire_edge_b:
        SoA static wire edge endpoint array.
        Stores the second canonical node ID for each wire edge.
        Invariant: (wire_edge_a[i], wire_edge_b[i]) matches wire_edges[i].

    wire_edge_keys:
        Packed-SoA static wire edge array.
        Stores each canonical edge as (node_a << 32) | node_b.

    wire_edge_key_index:
        Mapping from packed canonical edge key to index in wire_edge_keys.
        Provides O(1) lookup, deduplication, and swap-remove deletion.
    """

    __slots__ = (
        "nodes",
        "node_kinds",
        "node_default_values",
        "node_resolved_values",
        "devices",
        "device_kinds",
        "device_nodes",
        "transistors",
        "transistor_kinds",
        "transistor_gates",
        "transistor_sources",
        "transistor_drains",
        "transistor_conducting",
        "wire_edges",
        "wire_edge_index",
        "wire_edge_a",
        "wire_edge_b",
        "wire_edge_keys",
        "wire_edge_key_index",
        "static_neighbors",
        "dynamic_neighbors",
        "components",
        "component_id",
    )

    def __init__(self) -> None:
        """Initialise the Device Simulator State."""
        self.nodes: list[Node] = []
        self.node_kinds: list[int] = []
        self.node_default_values: list[int] = []
        self.node_resolved_values: list[int] = []
        self.devices: list[LogicDevice] = []
        self.device_kinds: list[int] = []
        self.device_nodes: list[int] = []
        self.transistors: list[Transistor] = []
        self.transistor_kinds: list[int] = []
        self.transistor_gates: list[int] = []
        self.transistor_sources: list[int] = []
        self.transistor_drains: list[int] = []
        self.transistor_conducting: list[bool] = []
        self.wire_edges: list[tuple[int, int]] = []
        self.wire_edge_index: dict[tuple[int, int], int] = {}
        self.wire_edge_a: list[int] = []
        self.wire_edge_b: list[int] = []
        self.wire_edge_keys: list[int] = []
        self.wire_edge_key_index: dict[int, int] = {}
        self.static_neighbors: list[list[int]] = []
        self.dynamic_neighbors: list[list[int]] = []
        self.components: list[list[int]] = []
        self.component_id: list[int] = []
