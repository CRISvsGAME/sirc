from ..simulator import DeviceSimulatorState as DeviceSimulatorState
from .logic_value import LogicValue as LogicValue
from enum import IntEnum
from typing import Final

BASE_NODE_KIND: Final[int]
GATE_NODE_KIND: Final[int]

class NodeKind(IntEnum):
    BASE = BASE_NODE_KIND
    GATE = GATE_NODE_KIND

class Node:
    id_: int
    def __init__(self, state: DeviceSimulatorState, node_id: int) -> None: ...
    @property
    def kind(self) -> NodeKind: ...
    @property
    def default_value(self) -> LogicValue: ...
    @property
    def resolved_value(self) -> LogicValue: ...
