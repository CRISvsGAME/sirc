"""Unit tests for sirc.core.device module."""

import pytest
from sirc.core.logic import LogicValue
from sirc.core.node import Node
from sirc.core.device import VDD, GND, Input, Probe, Port

# ------------------------------------------------------------------------------
# Rail Tests
# ------------------------------------------------------------------------------


def test_vdd_default_state():
    """VDD must drive LogicValue.ONE."""
    v = VDD()
    assert v.terminal_default_value is LogicValue.ONE
    assert isinstance(v.terminal, Node)


def test_gnd_default_state():
    """GND must drive LogicValue.ZERO."""
    g = GND()
    assert g.terminal_default_value is LogicValue.ZERO
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
    assert i.terminal_default_value is LogicValue.Z
    assert isinstance(i.terminal, Node)


def test_input_set_value_updates_value():
    """Input must drive the value set by set_value()."""
    i = Input()
    i.set_value(LogicValue.ONE)
    assert i.terminal_default_value is LogicValue.ONE
    i.set_value(LogicValue.ZERO)
    assert i.terminal_default_value is LogicValue.ZERO
    i.set_value(LogicValue.X)
    assert i.terminal_default_value is LogicValue.X
    i.set_value(LogicValue.Z)
    assert i.terminal_default_value is LogicValue.Z


def test_input_terminal_node_is_unique():
    """Each Input instance must have its own unique terminal Node."""
    a = Input()
    b = Input()
    assert a.terminal is not b.terminal


# ------------------------------------------------------------------------------
# Probe Device Tests
# ------------------------------------------------------------------------------


def test_probe_default_state():
    """Probe must default to driving LogicValue.Z."""
    p = Probe()
    assert p.terminal_default_value is LogicValue.Z
    assert isinstance(p.terminal, Node)


def test_probe_sample_reads_node_value():
    """Probe.sample() must return the LogicValue present on its terminal Node."""
    p = Probe()
    n = p.terminal
    n.set_resolved_value(LogicValue.ONE)
    assert p.sample() is LogicValue.ONE
    n.set_resolved_value(LogicValue.ZERO)
    assert p.sample() is LogicValue.ZERO
    n.set_resolved_value(LogicValue.X)
    assert p.sample() is LogicValue.X
    n.set_resolved_value(LogicValue.Z)
    assert p.sample() is LogicValue.Z


def test_probe_terminal_node_is_unique():
    """Each Probe instance must have its own unique terminal Node."""
    a = Probe()
    b = Probe()
    assert a.terminal is not b.terminal


# ------------------------------------------------------------------------------
# Port Device Tests
# ------------------------------------------------------------------------------


def test_port_default_state():
    """Port must default to driving LogicValue.Z."""
    p = Port()
    assert p.terminal_default_value is LogicValue.Z
    assert isinstance(p.terminal, Node)


def test_port_terminal_node_is_unique():
    """Each Port instance must have its own unique terminal Node."""
    a = Port()
    b = Port()
    assert a.terminal is not b.terminal


# ------------------------------------------------------------------------------
# Debug Representation Tests
# ------------------------------------------------------------------------------


@pytest.mark.parametrize("device_class", [VDD, GND, Input, Probe, Port])
def test_repr_contains_class_value_terminal_info(device_class: type):
    """__repr__ must include class name and terminal information."""
    d = device_class()
    r = repr(d)
    assert r.startswith(f"<{device_class.__name__} ")
    assert "terminal_default_value=" in r
    assert "terminal_resolved_value=" in r
    assert r.endswith(">")
