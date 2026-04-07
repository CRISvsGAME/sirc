from ..core.logic_device import LogicDevice as LogicDevice
from ..core.node import Node as Node
from ..core.transistor import Transistor as Transistor

class DeviceSimulatorState:
    nodes: list[Node]
    node_kinds: list[int]
    node_default_values: list[int]
    node_resolved_values: list[int]
    devices: list[LogicDevice]
    device_kinds: list[int]
    device_nodes: list[int]
    transistors: list[Transistor]
    transistor_kinds: list[int]
    transistor_gates: list[int]
    transistor_sources: list[int]
    transistor_drains: list[int]
    transistor_conducting: list[bool]
    wire_edges: list[tuple[int, int]]
    wire_edge_index: dict[tuple[int, int], int]
    wire_edge_a: list[int]
    wire_edge_b: list[int]
    wire_edge_keys: list[int]
    wire_edge_key_index: dict[int, int]
    static_neighbors: list[list[int]]
    dynamic_neighbors: list[list[int]]
    components: list[list[int]]
    component_id: list[int]
    def __init__(self) -> None: ...
