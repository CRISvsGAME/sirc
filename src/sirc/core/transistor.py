"""
SIRC Core Transistor Module.

Defines the Transistor base class and the NMOS and PMOS device types. A
Transistor contains exactly three Nodes: gate, source, and drain. It only stores
the structure and the Simulator will determine whether a conduction path exists.
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Protocol
from sirc.core.logic import LogicValue
from sirc.core.node import Node


class Conductive(Protocol):  # pylint: disable=too-few-public-methods
    """Protocol for objects capable of reporting conduction state."""

    def is_conducting(self) -> bool:
        """Returns True if the device is currently conducting."""
        ...  # pylint: disable=unnecessary-ellipsis


@dataclass(slots=True)
class Transistor:
    """
    Base class for a three-terminal transistor device.

    This class defines ONLY structural information and minimal helper behaviour.
    All electrical evaluation, propagation, and node-group management are
    performed exclusively by the Simulator.

    Attributes:
        gate:   The Node controlling the transistor.
        source: The source Node.
        drain:  The drain Node.
    """

    gate: Node
    source: Node
    drain: Node

    # --------------------------------------------------------------------------
    # Simulator-Queried Conduction Rule
    # --------------------------------------------------------------------------

    def is_conducting(self) -> bool:
        """
        Return True if the transistor forms a conduction path between source and
        drain, based on its gate Node's resolved LogicValue. Subclasses (NMOS,
        PMOS) override this with device-type behaviour.
        """
        raise NotImplementedError("Transistor.is_conducting() must be implemented.")

    # --------------------------------------------------------------------------
    # Structural Helpers
    # --------------------------------------------------------------------------

    def terminals(self) -> tuple[Node, Node, Node]:
        """Return (gate, source, drain) for inspection by the Simulator."""
        return (self.gate, self.source, self.drain)

    def conduction_nodes(self) -> tuple[Node, Node]:
        """
        Return the conduction terminals (source, drain). The Simulator uses this
        to connect/disconnect nodes dynamically when is_conducting() evaluates
        True/False.
        """
        return (self.source, self.drain)

    def __repr__(self) -> str:
        """Return debug representation."""
        name = self.__class__.__name__
        return f"<{name} gate={self.gate} source={self.source} drain={self.drain}>"


class NMOS(Transistor):
    """
    NMOS transistor.

    Conduction Rule:
        - Conducts when gate is LogicValue.ONE.
        - Non-conducting for ZERO, X, or Z.
    """

    def is_conducting(self) -> bool:
        g = self.gate.value
        return g is LogicValue.ONE


class PMOS(Transistor):
    """
    PMOS transistor.

    Conduction Rule:
        - Conducts when gate is LogicValue.ZERO.
        - Non-conducting for ONE, X, or Z.
    """

    def is_conducting(self) -> bool:
        g = self.gate.value
        return g is LogicValue.ZERO
