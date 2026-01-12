"""Unit tests for LogicDevice module."""

import pytest
from sirc.core import LogicValue, Node, LogicDeviceKind, VDD, GND, Input, Probe, Port

# ------------------------------------------------------------------------------
# Rail Tests
# ------------------------------------------------------------------------------


def test_vdd_id_and_kind():
    """VDD must have correct device identification and kind."""
    v = VDD(1, Node(1))
    assert v.id == 1
    assert v.kind is LogicDeviceKind.VDD


def test_vdd_default_state():
    """VDD must drive LogicValue.ONE."""
    v = VDD(1, Node(1))
    assert v.terminal_default_value is LogicValue.ONE
    assert isinstance(v.terminal, Node)


def test_gnd_id_and_kind():
    """GND must have correct device identification and kind."""
    g = GND(1, Node(1))
    assert g.id == 1
    assert g.kind is LogicDeviceKind.GND


def test_gnd_default_state():
    """GND must drive LogicValue.ZERO."""
    g = GND(1, Node(1))
    assert g.terminal_default_value is LogicValue.ZERO
    assert isinstance(g.terminal, Node)


def test_vdd_and_gnd_nodes_are_unique():
    """VDD and GND must have distinct terminal Nodes."""
    v = VDD(1, Node(1))
    g = GND(2, Node(2))
    assert v.terminal is not g.terminal


# ------------------------------------------------------------------------------
# Input Device Tests
# ------------------------------------------------------------------------------


def test_input_id_and_kind():
    """Input must have correct device identification and kind."""
    i = Input(1, Node(1))
    assert i.id == 1
    assert i.kind is LogicDeviceKind.INPUT


def test_input_default_state():
    """Input terminal must default to LogicValue.Z."""
    i = Input(1, Node(1))
    assert i.terminal_default_value is LogicValue.Z
    assert isinstance(i.terminal, Node)


def test_input_set_value_updates_value():
    """Input must drive the value set by set_value()."""
    i = Input(1, Node(1))
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
    a = Input(1, Node(1))
    b = Input(2, Node(2))
    assert a.terminal is not b.terminal


# ------------------------------------------------------------------------------
# Probe Device Tests
# ------------------------------------------------------------------------------


def test_probe_id_and_kind():
    """Probe must have correct device identification and kind."""
    p = Probe(1, Node(1))
    assert p.id == 1
    assert p.kind is LogicDeviceKind.PROBE


def test_probe_default_state():
    """Probe terminal must default to LogicValue.Z."""
    p = Probe(1, Node(1))
    assert p.terminal_default_value is LogicValue.Z
    assert isinstance(p.terminal, Node)


def test_probe_sample_reads_node_value():
    """Probe.sample() must return the LogicValue present on its terminal Node."""
    p = Probe(1, Node(1))
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
    a = Probe(1, Node(1))
    b = Probe(2, Node(2))
    assert a.terminal is not b.terminal


# ------------------------------------------------------------------------------
# Port Device Tests
# ------------------------------------------------------------------------------


def test_port_id_and_kind():
    """Port must have correct device identification and kind."""
    p = Port(1, Node(1))
    assert p.id == 1
    assert p.kind is LogicDeviceKind.PORT


def test_port_default_state():
    """Port terminal must default to LogicValue.Z."""
    p = Port(1, Node(1))
    assert p.terminal_default_value is LogicValue.Z
    assert isinstance(p.terminal, Node)


def test_port_terminal_node_is_unique():
    """Each Port instance must have its own unique terminal Node."""
    a = Port(1, Node(1))
    b = Port(2, Node(2))
    assert a.terminal is not b.terminal


# ------------------------------------------------------------------------------
# Debug Representation Tests
# ------------------------------------------------------------------------------


@pytest.mark.parametrize("device_class", [VDD, GND, Input, Probe, Port])
def test_repr_contains_class_value_terminal_info(device_class: type):
    """__repr__ must include class name and terminal information."""
    d = device_class(1, Node(1))
    r = repr(d)
    assert r.startswith(f"<{device_class.__name__} ")
    assert f"id={d.id}" in r
    assert f"kind=LogicDeviceKind.{d.kind.name}" in r
    assert "terminal_default_value=" in r
    assert "terminal_resolved_value=" in r
    assert r.endswith(">")
