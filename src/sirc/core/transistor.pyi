from dataclasses import dataclass
from sirc.core.logic import LogicValue as LogicValue
from sirc.core.node import Node as Node
from typing import Protocol

class Conductive(Protocol):
    def is_conducting(self) -> bool: ...

@dataclass(slots=True)
class Transistor:
    gate: Node
    source: Node
    drain: Node
    def is_conducting(self) -> bool: ...
    def terminals(self) -> tuple[Node, Node, Node]: ...
    def conduction_nodes(self) -> tuple[Node, Node]: ...

class NMOS(Transistor):
    def is_conducting(self) -> bool: ...

class PMOS(Transistor):
    def is_conducting(self) -> bool: ...
