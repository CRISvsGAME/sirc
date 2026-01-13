"""Unit tests for Transistor module."""

import pytest
from sirc.core import LogicValue, Node, NodeKind, Transistor, NMOS, PMOS

# ------------------------------------------------------------------------------
# Transistor Construction Tests
# ------------------------------------------------------------------------------


def test_transistor_has_three_distinct_nodes():
    """Each Transistor must have unique gate, source, and drain Nodes."""
    g = Node(1, kind=NodeKind.GATE)
    s = Node(2)
    d = Node(3)
    t = NMOS(1, g, s, d)
    assert isinstance(t.gate, Node)
    assert isinstance(t.source, Node)
    assert isinstance(t.drain, Node)
    assert t.gate is not t.source
    assert t.gate is not t.drain
    assert t.source is not t.drain


def test_transistor_rejects_non_gate_node_as_gate():
    """Transistor must raise TypeError if gate Node is not kind=GATE."""
    g = Node(1)  # BASE Default
    s = Node(2)
    d = Node(3)
    with pytest.raises(TypeError):
        NMOS(1, g, s, d)
    with pytest.raises(TypeError):
        PMOS(2, g, s, d)


def test_transistor_rejects_gate_used_as_conduction_node():
    """Transistor must raise TypeError if source or drain Node is kind=GATE."""
    g = Node(1, kind=NodeKind.GATE)
    s = Node(2, kind=NodeKind.GATE)
    d = Node(3)
    with pytest.raises(TypeError):
        NMOS(1, g, s, d)
    with pytest.raises(TypeError):
        PMOS(2, g, s, d)
    with pytest.raises(TypeError):
        NMOS(3, g, d, s)
    with pytest.raises(TypeError):
        PMOS(4, g, d, s)


def test_transistor_rejects_shared_nodes():
    """Transistor must raise ValueError if gate, source, and drain Nodes are not distinct."""
    g = Node(1, kind=NodeKind.GATE)
    n = Node(2)
    with pytest.raises(ValueError):
        NMOS(1, g, n, n)
    with pytest.raises(ValueError):
        PMOS(1, g, n, n)


# ------------------------------------------------------------------------------
# Structural Helper Tests
# ------------------------------------------------------------------------------


def test_terminals_returns_gate_source_drain():
    """terminals() must return (gate, source, drain) Nodes in order."""
    g = Node(1, kind=NodeKind.GATE)
    s = Node(2)
    d = Node(3)
    t = NMOS(1, g, s, d)
    g, s, d = t.terminals()
    assert g is t.gate
    assert s is t.source
    assert d is t.drain


def test_conduction_nodes_returns_source_and_drain():
    """conduction_nodes() must return (source, drain) Nodes in order."""
    g = Node(1, kind=NodeKind.GATE)
    s = Node(2)
    d = Node(3)
    t = PMOS(1, g, s, d)
    s, d = t.conduction_nodes()
    assert s is t.source
    assert d is t.drain


# ------------------------------------------------------------------------------
# NMOS Conduction Tests
# ------------------------------------------------------------------------------


def test_nmos_conduction_rules():
    """NMOS must conduct only when gate is LogicValue.ONE."""
    g = Node(1, kind=NodeKind.GATE)
    s = Node(2)
    d = Node(3)
    t = NMOS(1, g, s, d)
    # Gate = 0 → off
    t.gate.set_resolved_value(LogicValue.ZERO)
    assert not t.is_conducting()
    # Gate = 1 → on
    t.gate.set_resolved_value(LogicValue.ONE)
    assert t.is_conducting()
    # Gate = X → off
    t.gate.set_resolved_value(LogicValue.X)
    assert not t.is_conducting()
    # Gate = Z → off
    t.gate.set_resolved_value(LogicValue.Z)
    assert not t.is_conducting()


# ------------------------------------------------------------------------------
# PMOS Conduction Tests
# ------------------------------------------------------------------------------


def test_pmos_conduction_rules():
    """PMOS must conduct only when gate is LogicValue.ZERO."""
    g = Node(1, kind=NodeKind.GATE)
    s = Node(2)
    d = Node(3)
    t = PMOS(1, g, s, d)
    # Gate = 0 → on
    t.gate.set_resolved_value(LogicValue.ZERO)
    assert t.is_conducting()
    # Gate = 1 → off
    t.gate.set_resolved_value(LogicValue.ONE)
    assert not t.is_conducting()
    # Gate = X → off
    t.gate.set_resolved_value(LogicValue.X)
    assert not t.is_conducting()
    # Gate = Z → off
    t.gate.set_resolved_value(LogicValue.Z)
    assert not t.is_conducting()


# ------------------------------------------------------------------------------
# Polymorphism Tests
# ------------------------------------------------------------------------------


def test_nmos_and_pmos_share_same_interface():
    """NMOS and PMOS must both be Transistor subclasses with is_conducting()."""
    ng = Node(1, kind=NodeKind.GATE)
    ns = Node(2)
    nd = Node(3)
    nmos = NMOS(1, ng, ns, nd)
    pg = Node(4, kind=NodeKind.GATE)
    ps = Node(5)
    pd = Node(6)
    pmos = PMOS(1, pg, ps, pd)
    assert isinstance(nmos, Transistor)
    assert isinstance(pmos, Transistor)
    assert hasattr(nmos, "is_conducting")
    assert hasattr(pmos, "is_conducting")


# ------------------------------------------------------------------------------
# Debug Representation Tests
# ------------------------------------------------------------------------------


def test_nmos_repr_format():
    """NMOS __repr__ must include class name and terminal fields."""
    g = Node(1, kind=NodeKind.GATE)
    s = Node(2)
    d = Node(3)
    t = NMOS(1, g, s, d)
    r = repr(t)
    assert "NMOS" in r
    assert "gate=" in r
    assert "source=" in r
    assert "drain=" in r
    assert r.startswith("<NMOS ")
    assert r.endswith(">")


def test_pmos_repr_format():
    """PMOS __repr__ must include class name and terminal fields."""
    g = Node(1, kind=NodeKind.GATE)
    s = Node(2)
    d = Node(3)
    t = PMOS(1, g, s, d)
    r = repr(t)
    assert "PMOS" in r
    assert "gate=" in r
    assert "source=" in r
    assert "drain=" in r
    assert r.startswith("<PMOS ")
    assert r.endswith(">")


# ------------------------------------------------------------------------------
# Isolation Tests
# ------------------------------------------------------------------------------


def test_transistor_nodes_are_not_shared_between_instances():
    """Each Transistor instance must have its own unique Nodes."""
    ng = Node(1, kind=NodeKind.GATE)
    ns = Node(2)
    nd = Node(3)
    nmos = NMOS(1, ng, ns, nd)
    pg = Node(4, kind=NodeKind.GATE)
    ps = Node(5)
    pd = Node(6)
    pmos = PMOS(1, pg, ps, pd)
    assert nmos.gate is not pmos.gate
    assert nmos.source is not pmos.source
    assert nmos.drain is not pmos.drain


# ------------------------------------------------------------------------------
# Stress & Stability Tests
# ------------------------------------------------------------------------------


def test_multiple_transistors_construction():
    """Creating many Transistor instances must preserve node identity uniqueness."""
    ts = [
        NMOS(i, Node(i * 3 + 1, kind=NodeKind.GATE), Node(i * 3 + 2), Node(i * 3 + 3))
        for i in range(1000)
    ]
    ids = {id(t.gate) for t in ts}
    assert len(ids) == 1000
    ids = {id(t.source) for t in ts}
    assert len(ids) == 1000
    ids = {id(t.drain) for t in ts}
    assert len(ids) == 1000
