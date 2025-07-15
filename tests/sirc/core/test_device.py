"""Unit tests for sirc.core.device module."""

from sirc.core.logic import LogicValue
from sirc.core.node import Node
from sirc.core.device import VDD, GND, Input

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


# ------------------------------------------------------------------------------
# Input Device Tests
# ------------------------------------------------------------------------------


def test_input_default_state():
    """Input must default to driving LogicValue.Z."""
    i = Input()
    assert i.value is LogicValue.Z
    assert isinstance(i.terminal, Node)


def test_input_set_value_updates_value():
    """Input must drive the value set by set_value()."""
    i = Input()
    i.set_value(LogicValue.ONE)
    assert i.value is LogicValue.ONE
    i.set_value(LogicValue.ZERO)
    assert i.value is LogicValue.ZERO
    i.set_value(LogicValue.X)
    assert i.value is LogicValue.X
    i.set_value(LogicValue.Z)
    assert i.value is LogicValue.Z


def test_input_terminal_node_is_unique():
    """Each Input instance must have its own unique terminal Node."""
    a = Input()
    b = Input()
    assert a.terminal is not b.terminal
