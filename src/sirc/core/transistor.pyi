import abc
from abc import ABC, abstractmethod
from sirc.core.logic import LogicValue as LogicValue
from sirc.core.node import Node as Node

class Transistor(ABC, metaclass=abc.ABCMeta):
    gate: Node
    source: Node
    drain: Node
    def __init__(self) -> None: ...
    @abstractmethod
    def is_conducting(self) -> bool: ...
    def terminals(self) -> tuple[Node, Node, Node]: ...
    def conduction_nodes(self) -> tuple[Node, Node]: ...

class NMOS(Transistor):
    def is_conducting(self) -> bool: ...

class PMOS(Transistor):
    def is_conducting(self) -> bool: ...
