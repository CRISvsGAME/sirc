from ..simulator import DeviceSimulatorState as DeviceSimulatorState
from .node import Node as Node
from enum import IntEnum
from typing import Final

GND_DEVICE_KIND: Final[int]
VDD_DEVICE_KIND: Final[int]
INPUT_DEVICE_KIND: Final[int]
PROBE_DEVICE_KIND: Final[int]
PORT_DEVICE_KIND: Final[int]

class LogicDeviceKind(IntEnum):
    GND = GND_DEVICE_KIND
    VDD = VDD_DEVICE_KIND
    INPUT = INPUT_DEVICE_KIND
    PROBE = PROBE_DEVICE_KIND
    PORT = PORT_DEVICE_KIND

class LogicDevice:
    id_: int
    def __init__(self, state: DeviceSimulatorState, device_id: int) -> None: ...
    @property
    def kind(self) -> LogicDeviceKind: ...
    @property
    def node(self) -> Node: ...
