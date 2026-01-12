"""Unit tests for Node module."""

from sirc.core import LogicValue, Node, NodeKind

# ------------------------------------------------------------------------------
# Construction Tests
# ------------------------------------------------------------------------------


def test_node_kind_default():
    """A new Node must have the default kind of BASE."""
    n = Node(1)
    assert n.kind == NodeKind.BASE


def test_node_initial_state():
    """A new Node must have LogicValue Z default and resolved value"""
    n = Node(1)
    assert n.default_value is LogicValue.Z  # Default Value
    assert n.resolved_value is LogicValue.Z  # Resolved Value


def test_nodes_are_distinct():
    """Different Nodes must be distinct instances."""
    a = Node(1)
    b = Node(2)
    assert a is not b
    assert a != b


# ------------------------------------------------------------------------------
# Default Value Handling Tests
# ------------------------------------------------------------------------------


def test_set_default_value():
    """Setting default value must update the Node's stored default value."""
    n = Node(1)
    n.set_default_value(LogicValue.ZERO)
    assert n.default_value is LogicValue.ZERO
    n.set_default_value(LogicValue.ONE)
    assert n.default_value is LogicValue.ONE
    n.set_default_value(LogicValue.Z)
    assert n.default_value is LogicValue.Z
    n.set_default_value(LogicValue.X)
    assert n.default_value is LogicValue.X


# ------------------------------------------------------------------------------
# Resolved Value Handling Tests
# ------------------------------------------------------------------------------


def test_set_resolved_value():
    """Setting resolved value must update the Node's stored resolved value."""
    n = Node(1)
    n.set_resolved_value(LogicValue.ZERO)
    assert n.resolved_value is LogicValue.ZERO
    n.set_resolved_value(LogicValue.ONE)
    assert n.resolved_value is LogicValue.ONE
    n.set_resolved_value(LogicValue.Z)
    assert n.resolved_value is LogicValue.Z
    n.set_resolved_value(LogicValue.X)
    assert n.resolved_value is LogicValue.X


# ------------------------------------------------------------------------------
# Debug Representation Tests
# ------------------------------------------------------------------------------


def test_repr_contains_default_and_resolved_values():
    """__repr__ must include default and resolved values."""
    n = Node(1)
    n.set_resolved_value(LogicValue.ONE)
    r = repr(n)
    assert "Node" in r
    assert "id=1" in r
    assert "kind=NodeKind.BASE" in r
    assert "default_value=LogicValue.Z" in r
    assert "resolved_value=LogicValue.ONE" in r


def test_repr_format():
    """__repr__ must have correct format."""
    n = Node(1)
    n.set_resolved_value(LogicValue.ONE)
    r = repr(n)
    assert r.startswith("<Node ")
    assert r.endswith(">")
