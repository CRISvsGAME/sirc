from .logic_value import LogicValue as LogicValue, Z as Z
from enum import IntEnum

class NodeKind(IntEnum):
    BASE = 0
    GATE = 1

BASE_NODE_KIND: NodeKind
GATE_NODE_KIND: NodeKind

class Node:
    id_: int
    kind: NodeKind
    default_value: LogicValue
    resolved_value: LogicValue
    def __init__(self, node_id: int, kind: NodeKind = ...) -> None: ...
