"""Unit tests for Device Simulator Dependency Module."""

from sirc.simulator import IdentificationFactory

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
