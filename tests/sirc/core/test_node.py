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


def test_get_drivers():
    """get_drivers() must return an immutable tuple copy."""
    n = Node()
    n.add_driver(LogicValue.ZERO)
    n.add_driver(LogicValue.ONE)
    n.add_driver(LogicValue.X)
    n.add_driver(LogicValue.Z)
    drivers = n.get_drivers()
    assert isinstance(drivers, tuple)
    assert drivers == (LogicValue.ZERO, LogicValue.ONE, LogicValue.X, LogicValue.Z)


# ------------------------------------------------------------------------------
# Connectivity Tests
# ------------------------------------------------------------------------------


def test_connect_bidirectional():
    """connect() must create symmetric connections."""
    a = Node()
    b = Node()
    a.connect(b)
    assert a in b.get_connections()
    assert b in a.get_connections()
    assert len(a.get_connections()) == 1
    assert len(b.get_connections()) == 1


def test_connect_no_duplicates():
    """connect() must not create duplicate connections."""
    a = Node()
    b = Node()
    a.connect(b)
    b.connect(a)
    assert a.get_connections() == (b,)
    assert b.get_connections() == (a,)


def test_connect_self_noop():
    """Connecting a Node to itself must do nothing."""
    n = Node()
    n.connect(n)
    assert not n.get_connections()


def test_disconnect_bidirectional():
    """disconnect() must remove symmetric connections."""
    a = Node()
    b = Node()
    a.connect(b)
    b.disconnect(a)
    assert not a.get_connections()
    assert not b.get_connections()


def test_disconnect_self_noop():
    """Disconnecting a Node from itself must do nothing."""
    n = Node()
    n.disconnect(n)
    assert not n.get_connections()


def test_add_connection_internal_only():
    """add_connection() must add a one-way connection."""
    a = Node()
    b = Node()
    a.add_connection(b)
    assert b in a.get_connections()
    assert a not in b.get_connections()
    assert len(a.get_connections()) == 1
    assert len(b.get_connections()) == 0


def test_remove_connection_internal_only():
    """remove_connection() must remove a one-way connection."""
    a = Node()
    b = Node()
    a.add_connection(b)
    a.remove_connection(b)
    assert not a.get_connections()
    assert not b.get_connections()


def test_get_connections():
    """get_connections() must return an immutable tuple copy."""
    a = Node()
    b = Node()
    a.connect(b)
    connections = a.get_connections()
    assert isinstance(connections, tuple)
    assert connections == (b,)


def test_isolated_node_connections():
    """An isolated Node must have no connections."""
    a = Node()
    b = Node()
    c = Node()
    a.connect(b)
    assert c not in a.get_connections()
    assert c not in b.get_connections()
    assert not c.get_connections()


# ------------------------------------------------------------------------------
# Debug Representation Tests
# ------------------------------------------------------------------------------


def test_repr_contains_value_and_drivers():
    """__repr__ must include value and drivers"""
    n = Node()
    n.add_driver(LogicValue.ONE)
    r = repr(n)
    assert "Node" in r
    assert "value=LogicValue.Z" in r
    assert "drivers=(LogicValue.ONE,)" in r


def test_repr_format():
    """__repr__ must have correct format."""
    n = Node()
    n.add_driver(LogicValue.ONE)
    r = repr(n)
    assert r.startswith("<Node ")
    assert r.endswith(">")
