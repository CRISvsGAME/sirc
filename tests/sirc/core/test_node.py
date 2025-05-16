"""Unit tests for sirc.core.node module."""

from sirc.core.logic import LogicValue
from sirc.core.node import Node

# ------------------------------------------------------------------------------
# Construction Tests
# ------------------------------------------------------------------------------


def test_node_initial_state():
    """A new Node must have Z value, no drivers, and no connections."""
    n = Node()
    assert n.value is LogicValue.Z
    assert not n.get_drivers()
    assert not n.get_connections()


def test_nodes_are_distinct():
    """Different Nodes must be distinct instances."""
    a = Node()
    b = Node()
    assert a is not b
    assert a != b


# ------------------------------------------------------------------------------
# Value Handling Tests
# ------------------------------------------------------------------------------


def test_set_resolved_value():
    """Setting resolved value must update the Node's stored value."""
    n = Node()
    n.set_resolved_value(LogicValue.ZERO)
    assert n.value is LogicValue.ZERO
    n.set_resolved_value(LogicValue.ONE)
    assert n.value is LogicValue.ONE
    n.set_resolved_value(LogicValue.Z)
    assert n.value is LogicValue.Z
    n.set_resolved_value(LogicValue.X)
    assert n.value is LogicValue.X


# ------------------------------------------------------------------------------
# Driver Management Tests
# ------------------------------------------------------------------------------


def test_add_driver():
    """add_driver() must append drivers in order."""
    n = Node()
    n.add_driver(LogicValue.ZERO)
    n.add_driver(LogicValue.ONE)
    n.add_driver(LogicValue.X)
    n.add_driver(LogicValue.Z)
    assert n.get_drivers() == (
        LogicValue.ZERO,
        LogicValue.ONE,
        LogicValue.X,
        LogicValue.Z,
    )


def test_add_many_drivers():
    """add_driver() must handle many drivers."""
    count = 1000000
    n = Node()
    for _ in range(count):
        n.add_driver(LogicValue.ZERO)
    assert len(n.get_drivers()) == count


def test_clear_drivers():
    """clear_drivers() must remove all drivers."""
    n = Node()
    n.add_driver(LogicValue.ZERO)
    n.add_driver(LogicValue.ONE)
    n.add_driver(LogicValue.X)
    n.add_driver(LogicValue.Z)
    n.clear_drivers()
    assert not n.get_drivers()
