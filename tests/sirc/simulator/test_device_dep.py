"""Unit tests for Device Simulator Dependency Module."""

from sirc.core import NodeKind
from sirc.simulator import IdentificationFactory, NodeFactory

# ------------------------------------------------------------------------------
# Identification Factory Tests
# ------------------------------------------------------------------------------


def test_identification_factory_allocates_monotonic_node_ids():
    """IdentificationFactory must allocate monotonic Node IDs."""
    factory = IdentificationFactory()
    node_ids = [factory.allocate_node_id() for _ in range(100)]
    for i in range(100):
        assert node_ids[i] == i


def test_identification_factory_allocates_monotonic_device_ids():
    """IdentificationFactory must allocate monotonic Device IDs."""
    factory = IdentificationFactory()
    device_ids = [factory.allocate_device_id() for _ in range(100)]
    for i in range(100):
        assert device_ids[i] == i


def test_identification_factory_allocates_monotonic_transistor_ids():
    """IdentificationFactory must allocate monotonic Transistor IDs."""
    factory = IdentificationFactory()
    transistor_ids = [factory.allocate_transistor_id() for _ in range(100)]
    for i in range(100):
        assert transistor_ids[i] == i


def test_identification_factory_counters_are_independent():
    """IdentificationFactory must maintain independent counters."""
    factory = IdentificationFactory()
    for i in range(100):
        assert factory.allocate_node_id() == i
        assert factory.allocate_device_id() == i
        assert factory.allocate_transistor_id() == i


# ------------------------------------------------------------------------------
# Node Factory Tests
# ------------------------------------------------------------------------------


def test_node_factory_creates_base_nodes():
    """NodeFactory must create BASE Nodes with monotonic IDs."""
    factory = NodeFactory(IdentificationFactory())
    base_nodes = [factory.create_base_node() for _ in range(100)]
    for i in range(100):
        assert base_nodes[i].id == i
        assert base_nodes[i].kind == NodeKind.BASE


def test_node_factory_creates_gate_nodes():
    """NodeFactory must create GATE Nodes with monotonic IDs."""
    factory = NodeFactory(IdentificationFactory())
    gate_nodes = [factory.create_gate_node() for _ in range(100)]
    for i in range(100):
        assert gate_nodes[i].id == i
        assert gate_nodes[i].kind == NodeKind.GATE


def test_node_factory_ids_are_shared_between_base_and_gate():
    """NodeFactory must allocate shared IDs for BASE and GATE Nodes."""
    factory = NodeFactory(IdentificationFactory())
    a = factory.create_base_node()
    b = factory.create_gate_node()
    c = factory.create_base_node()
    d = factory.create_gate_node()
    assert a.id == 0
    assert a.kind == NodeKind.BASE
    assert b.id == 1
    assert b.kind == NodeKind.GATE
    assert c.id == 2
    assert c.kind == NodeKind.BASE
    assert d.id == 3
    assert d.kind == NodeKind.GATE
