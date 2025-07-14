"""Unit tests for sirc.core.device module."""

from sirc.core.logic import LogicValue
from sirc.core.node import Node
from sirc.core.device import VDD, GND

# ------------------------------------------------------------------------------
# Rail Tests
# ------------------------------------------------------------------------------


def test_vdd_default_state():
    """VDD must drive LogicValue.ONE."""
    v = VDD()
    assert v.value is LogicValue.ONE
    assert isinstance(v.terminal, Node)


def test_gnd_default_state():
    """GND must drive LogicValue.ZERO."""
    g = GND()
    assert g.value is LogicValue.ZERO
    assert isinstance(g.terminal, Node)


def test_vdd_and_gnd_nodes_are_unique():
    """VDD and GND must have distinct terminal Nodes."""
    v = VDD()
    g = GND()
    assert v.terminal is not g.terminal
