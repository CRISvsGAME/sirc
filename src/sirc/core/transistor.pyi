import abc
from .logic_value import ONE as ONE, ZERO as ZERO
from .node import Node as Node
from abc import ABC, abstractmethod
from enum import IntEnum

class TransistorKind(IntEnum):
    NMOS = 0
    PMOS = 1

NMOS_TRANSISTOR_KIND: TransistorKind
PMOS_TRANSISTOR_KIND: TransistorKind

class Transistor(ABC, metaclass=abc.ABCMeta):
    id_: int
    kind: TransistorKind
    gate: Node
    source: Node
    drain: Node
    def __init__(self, transistor_id: int, kind: TransistorKind, gate: Node, source: Node, drain: Node) -> None: ...
    @abstractmethod
    def is_conducting(self) -> bool: ...
    @abstractmethod
    def is_conducting_byte(self) -> int: ...

class NMOS(Transistor):
    def __init__(self, transistor_id: int, gate: Node, source: Node, drain: Node) -> None: ...
    def is_conducting(self) -> bool: ...
    def is_conducting_byte(self) -> int: ...

class PMOS(Transistor):
    def __init__(self, transistor_id: int, gate: Node, source: Node, drain: Node) -> None: ...
    def is_conducting(self) -> bool: ...
    def is_conducting_byte(self) -> int: ...
