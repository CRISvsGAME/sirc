"""Unit tests for sirc.core.transistor module."""

from sirc.core.logic import LogicValue
from sirc.core.node import Node
from sirc.core.transistor import Transistor, NMOS, PMOS

# ------------------------------------------------------------------------------
# Transistor Construction Tests
# ------------------------------------------------------------------------------


def test_transistor_has_three_distinct_nodes():
    """Each Transistor must have unique gate, source, and drain Nodes."""
    t = NMOS()
    assert isinstance(t.gate, Node)
    assert isinstance(t.source, Node)
    assert isinstance(t.drain, Node)
    assert t.gate is not t.source
    assert t.gate is not t.drain
    assert t.source is not t.drain


def test_transistor_initial_node_state():
    """Transistor Nodes must default to LogicValue.Z and have no drivers."""
    t = PMOS()
    assert t.gate.value is LogicValue.Z
    assert t.source.value is LogicValue.Z
    assert t.drain.value is LogicValue.Z
    assert not t.gate.get_drivers()
    assert not t.source.get_drivers()
    assert not t.drain.get_drivers()


# ------------------------------------------------------------------------------
# Structural Helper Tests
# ------------------------------------------------------------------------------


def test_terminals_returns_gate_source_drain():
    """terminals() must return (gate, source, drain) Nodes in order."""
    t = NMOS()
    g, s, d = t.terminals()
    assert g is t.gate
    assert s is t.source
    assert d is t.drain


def test_conduction_nodes_returns_source_and_drain():
    """conduction_nodes() must return (source, drain) Nodes in order."""
    t = PMOS()
    s, d = t.conduction_nodes()
    assert s is t.source
    assert d is t.drain


# ------------------------------------------------------------------------------
# NMOS Conduction Tests
# ------------------------------------------------------------------------------


def test_nmos_conduction_rules():
    """NMOS must conduct only when gate is LogicValue.ONE."""
    t = NMOS()
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
    t = PMOS()
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
    nmos = NMOS()
    pmos = PMOS()
    assert isinstance(nmos, Transistor)
    assert isinstance(pmos, Transistor)
    assert hasattr(nmos, "is_conducting")
    assert hasattr(pmos, "is_conducting")


# ------------------------------------------------------------------------------
# Debug Representation Tests
# ------------------------------------------------------------------------------


def test_nmos_repr_format():
    """NMOS __repr__ must include class name and terminal fields."""
    t = NMOS()
    r = repr(t)
    assert "NMOS" in r
    assert "gate=" in r
    assert "source=" in r
    assert "drain=" in r
    assert r.startswith("<NMOS ")
    assert r.endswith(">")


def test_pmos_repr_format():
    """PMOS __repr__ must include class name and terminal fields."""
    t = PMOS()
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
    nmos = NMOS()
    pmos = PMOS()
    assert nmos.gate is not pmos.gate
    assert nmos.source is not pmos.source
    assert nmos.drain is not pmos.drain


# ------------------------------------------------------------------------------
# Stress & Stability Tests
# ------------------------------------------------------------------------------


def test_multiple_transistors_construction():
    """Creating many Transistor instances must yield unique Nodes."""
    ts = [NMOS() for _ in range(1000)]
    ids = {id(t.gate) for t in ts}
    assert len(ids) == 1000
    ids = {id(t.source) for t in ts}
    assert len(ids) == 1000
    ids = {id(t.drain) for t in ts}
    assert len(ids) == 1000
