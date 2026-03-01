"""Unit tests for LogicDevice module."""

import pytest
from sirc.core import LogicValue, Node, LogicDeviceKind, VDD, GND, Input, Probe, Port

# ------------------------------------------------------------------------------
# Rail Tests
# ------------------------------------------------------------------------------


def test_vdd_id_and_kind():
    """VDD must have correct device identification and kind."""
    v = VDD(1, Node(1))
    assert v.id_ == 1
    assert v.kind is LogicDeviceKind.VDD


def test_vdd_default_state():
    """VDD must drive LogicValue.ONE."""
    v = VDD(1, Node(1))
    assert v.node.default_value is LogicValue.ONE
    assert isinstance(v.node, Node)


def test_gnd_id_and_kind():
    """GND must have correct device identification and kind."""
    g = GND(1, Node(1))
    assert g.id_ == 1
    assert g.kind is LogicDeviceKind.GND


def test_gnd_default_state():
    """GND must drive LogicValue.ZERO."""
    g = GND(1, Node(1))
    assert g.node.default_value is LogicValue.ZERO
    assert isinstance(g.node, Node)


def test_vdd_and_gnd_nodes_are_unique():
    """VDD and GND must have distinct terminal Nodes."""
    v = VDD(1, Node(1))
    g = GND(2, Node(2))
    assert v.node is not g.node


# ------------------------------------------------------------------------------
# Input Device Tests
# ------------------------------------------------------------------------------


def test_input_id_and_kind():
    """Input must have correct device identification and kind."""
    i = Input(1, Node(1))
    assert i.id_ == 1
    assert i.kind is LogicDeviceKind.INPUT


def test_input_default_state():
    """Input terminal must default to LogicValue.Z."""
    i = Input(1, Node(1))
    assert i.node.default_value is LogicValue.Z
    assert isinstance(i.node, Node)


def test_input_set_value_updates_value():
    """Input must drive the value set by set_value()."""
    i = Input(1, Node(1))
    i.set_value(LogicValue.ONE)
    assert i.node.default_value is LogicValue.ONE
    i.set_value(LogicValue.ZERO)
    assert i.node.default_value is LogicValue.ZERO
    i.set_value(LogicValue.X)
    assert i.node.default_value is LogicValue.X
    i.set_value(LogicValue.Z)
    assert i.node.default_value is LogicValue.Z


def test_input_terminal_node_is_unique():
    """Each Input instance must have its own unique terminal Node."""
    a = Input(1, Node(1))
    b = Input(2, Node(2))
    assert a.node is not b.node


# ------------------------------------------------------------------------------
# Probe Device Tests
# ------------------------------------------------------------------------------


def test_probe_id_and_kind():
    """Probe must have correct device identification and kind."""
    p = Probe(1, Node(1))
    assert p.id_ == 1
    assert p.kind is LogicDeviceKind.PROBE


def test_probe_default_state():
    """Probe terminal must default to LogicValue.Z."""
    p = Probe(1, Node(1))
    assert p.node.default_value is LogicValue.Z
    assert isinstance(p.node, Node)


def test_probe_sample_reads_node_value():
    """Probe.sample() must return the LogicValue present on its terminal Node."""
    p = Probe(1, Node(1))
    n = p.node
    n.resolved_value = LogicValue.ONE
    assert p.sample() is LogicValue.ONE
    n.resolved_value = LogicValue.ZERO
    assert p.sample() is LogicValue.ZERO
    n.resolved_value = LogicValue.X
    assert p.sample() is LogicValue.X
    n.resolved_value = LogicValue.Z
    assert p.sample() is LogicValue.Z


def test_probe_terminal_node_is_unique():
    """Each Probe instance must have its own unique terminal Node."""
    a = Probe(1, Node(1))
    b = Probe(2, Node(2))
    assert a.node is not b.node


# ------------------------------------------------------------------------------
# Port Device Tests
# ------------------------------------------------------------------------------


def test_port_id_and_kind():
    """Port must have correct device identification and kind."""
    p = Port(1, Node(1))
    assert p.id_ == 1
    assert p.kind is LogicDeviceKind.PORT


def test_port_default_state():
    """Port terminal must default to LogicValue.Z."""
    p = Port(1, Node(1))
    assert p.node.default_value is LogicValue.Z
    assert isinstance(p.node, Node)


def test_port_terminal_node_is_unique():
    """Each Port instance must have its own unique terminal Node."""
    a = Port(1, Node(1))
    b = Port(2, Node(2))
    assert a.node is not b.node


# ------------------------------------------------------------------------------
# Debug Representation Tests
# ------------------------------------------------------------------------------


@pytest.mark.parametrize("device_class", [VDD, GND, Input, Probe, Port])
def test_repr_contains_class_value_terminal_info(device_class: type):
    """__repr__ must include class name and terminal information."""
    d = device_class(1, Node(1))
    r = repr(d)
    assert r.startswith(f"<{device_class.__name__} ")
    assert f"id={d.id_}" in r
    assert f"kind=LogicDeviceKind.{d.kind.name}" in r
    assert "terminal=" in r
    assert r.endswith(">")
