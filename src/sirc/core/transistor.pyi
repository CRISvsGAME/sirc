from ..simulator import DeviceSimulatorState as DeviceSimulatorState
from .node import Node as Node
from enum import IntEnum
from typing import Final

NMOS_TRANSISTOR_KIND: Final[int]
PMOS_TRANSISTOR_KIND: Final[int]

class TransistorKind(IntEnum):
    NMOS = NMOS_TRANSISTOR_KIND
    PMOS = PMOS_TRANSISTOR_KIND

class Transistor:
    id_: int
    def __init__(self, state: DeviceSimulatorState, transistor_id: int) -> None: ...
    @property
    def kind(self) -> TransistorKind: ...
    @property
    def gate(self) -> Node: ...
    @property
    def source(self) -> Node: ...
    @property
    def drain(self) -> Node: ...
    @property
    def conducting(self) -> bool: ...
