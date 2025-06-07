"""Unit tests for sirc.core.transistor module."""

from sirc.core.node import Node
from sirc.core.transistor import Transistor

# ------------------------------------------------------------------------------
# Base Class Tests
# ------------------------------------------------------------------------------


def test_transistor_has_three_terminals():
    """A Transistor must store exactly three terminal Nodes."""
    g = Node()
    s = Node()
    d = Node()
    t = Transistor(g, s, d)
    assert t.gate is g
    assert t.source is s
    assert t.drain is d
    assert t.terminals() == (g, s, d)


def test_transistor_conduction_nodes():
    """conduction_nodes() must return (source, drain)."""
    g = Node()
    s = Node()
    d = Node()
    t = Transistor(g, s, d)
    assert t.conduction_nodes() == (s, d)
