"""Unit tests for sirc.core.transistor module."""

from sirc.core.logic import LogicValue
from sirc.core.node import Node
from sirc.core.transistor import NMOS, PMOS

# ------------------------------------------------------------------------------
# Transistor Construction Tests
# ------------------------------------------------------------------------------


def test_transistor_has_three_distinct_nodes():
    """Each Transistor must have unique gate, source, and drain Nodes."""
    t = NMOS()
    assert isinstance(t.gate, Node)
    assert isinstance(t.source, Node)
    assert isinstance(t.drain, Node)
    assert t.gate is not t.source
    assert t.gate is not t.drain
    assert t.source is not t.drain


def test_transistor_initial_node_state():
    """Transistor Nodes must default to LogicValue.Z and have no drivers."""
    t = PMOS()
    assert t.gate.value is LogicValue.Z
    assert t.source.value is LogicValue.Z
    assert t.drain.value is LogicValue.Z
    assert not t.gate.get_drivers()
    assert not t.source.get_drivers()
    assert not t.drain.get_drivers()
