"""Unit tests for sirc.core.transistor module."""

import pytest
from sirc.core.logic import LogicValue
from sirc.core.node import Node
from sirc.core.transistor import Transistor, NMOS

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


def test_transistor_is_conducting_not_implemented():
    """The base class must raise NotImplementedError."""
    t = Transistor(Node(), Node(), Node())
    with pytest.raises(NotImplementedError):
        t.is_conducting()


def test_transistor_repr_contains_name_and_nodes():
    """__repr__ must include class name and terminal nodes."""
    g = Node()
    s = Node()
    d = Node()
    t = Transistor(g, s, d)
    r = repr(t)
    assert "Transistor" in r
    assert "gate=" in r
    assert "source=" in r
    assert "drain=" in r


def test_transistor_repr_format():
    """__repr__ must have correct format."""
    g = Node()
    s = Node()
    d = Node()
    t = Transistor(g, s, d)
    r = repr(t)
    assert r.startswith("<Transistor ")
    assert r.endswith(">")


# ------------------------------------------------------------------------------
# NMOS Tests
# ------------------------------------------------------------------------------


def test_nmos_conducting_rules():
    """NMOS must conduct only when gate is LogicValue.ONE."""
    g = Node()
    s = Node()
    d = Node()
    nmos = NMOS(g, s, d)
    # Gate = 0 → off
    g.set_resolved_value(LogicValue.ZERO)
    assert not nmos.is_conducting()
    # Gate = 1 → on
    g.set_resolved_value(LogicValue.ONE)
    assert nmos.is_conducting()
    # Gate = X → off
    g.set_resolved_value(LogicValue.X)
    assert not nmos.is_conducting()
    # Gate = Z → off
    g.set_resolved_value(LogicValue.Z)
    assert not nmos.is_conducting()
