"""Unit tests for Node module."""

import pytest
from sirc.core import LogicValue, Node, NodeKind

# ------------------------------------------------------------------------------
# Construction Tests
# ------------------------------------------------------------------------------


def test_node_kind_default():
    """A new Node must have the default kind of BASE."""
    n = Node(1)
    assert n.kind is NodeKind.BASE


def test_node_initial_state():
    """A new Node must have LogicValue Z default and resolved value."""
    n = Node(1)
    assert n.default_value is LogicValue.Z  # Default Value
    assert n.resolved_value is LogicValue.Z  # Resolved Value


def test_node_stores_id():
    """A Node must store the provided node_id as its id_ attribute."""
    a = Node(1)
    b = Node(2)
    assert a.id_ == 1
    assert b.id_ == 2


def test_node_kind_explicit():
    """A Node can be constructed with an explicit kind."""
    n = Node(1, kind=NodeKind.GATE)
    assert n.kind is NodeKind.GATE


# ------------------------------------------------------------------------------
# Default Value Handling Tests
# ------------------------------------------------------------------------------


@pytest.mark.parametrize("value", tuple(LogicValue))
def test_set_default_value(value: LogicValue):
    """Setting default value must update the Node's stored default value."""
    n = Node(1)
    n.default_value = value
    assert n.default_value is value


# ------------------------------------------------------------------------------
# Resolved Value Handling Tests
# ------------------------------------------------------------------------------


@pytest.mark.parametrize("value", tuple(LogicValue))
def test_set_resolved_value(value: LogicValue):
    """Setting resolved value must update the Node's stored resolved value."""
    n = Node(1)
    n.resolved_value = value
    assert n.resolved_value is value


# ------------------------------------------------------------------------------
# Debug Representation Tests
# ------------------------------------------------------------------------------


def test_repr():
    """__repr__ must return the expected debug representation."""
    n = Node(1)
    n.resolved_value = LogicValue.ZERO
    assert repr(n) == (
        "<Node id=1 kind=NodeKind.BASE "
        "default_value=LogicValue.Z resolved_value=LogicValue.ZERO>"
    )
