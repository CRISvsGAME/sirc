from .logic_value import LogicValue as LogicValue, ONE as ONE, ZERO as ZERO
from .node import Node as Node
from enum import IntEnum

class LogicDeviceKind(IntEnum):
    GND = 0
    VDD = 1
    INPUT = 2
    PROBE = 3
    PORT = 4

GND_DEVICE_KIND: LogicDeviceKind
VDD_DEVICE_KIND: LogicDeviceKind
INPUT_DEVICE_KIND: LogicDeviceKind
PROBE_DEVICE_KIND: LogicDeviceKind
PORT_DEVICE_KIND: LogicDeviceKind

class LogicDevice:
    id_: int
    kind: LogicDeviceKind
    node: Node
    def __init__(self, device_id: int, kind: LogicDeviceKind, node: Node) -> None: ...

class VDD(LogicDevice):
    def __init__(self, device_id: int, node: Node) -> None: ...

class GND(LogicDevice):
    def __init__(self, device_id: int, node: Node) -> None: ...

class Input(LogicDevice):
    def __init__(self, device_id: int, node: Node) -> None: ...
    def set_value(self, value: LogicValue) -> None: ...

class Probe(LogicDevice):
    def __init__(self, device_id: int, node: Node) -> None: ...
    def sample(self) -> LogicValue: ...

class Port(LogicDevice):
    def __init__(self, device_id: int, node: Node) -> None: ...
