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
