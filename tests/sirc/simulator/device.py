"""Unit tests for sirc.simulator.device module."""

from sirc.simulator.device import DeviceSimulator

# ------------------------------------------------------------------------------
# Simulator Construction Tests
# ------------------------------------------------------------------------------


def test_simulator_initial_state():
    """Simulator must start with no devices, no transistors, and no nodes."""
    sim = DeviceSimulator()
    assert not sim.devices
    assert not sim.transistors
    assert not sim.nodes
