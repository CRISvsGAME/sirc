"""Unit tests for sirc.simulator.device module."""

from sirc.simulator.device import DeviceSimulator
from sirc.core.logic import LogicValue
from sirc.core.node import Node
from sirc.core.device import LogicDevice, VDD, GND, Input, Probe, Port
from sirc.core.transistor import Transistor, NMOS, PMOS

# ------------------------------------------------------------------------------
# Simulator Construction Tests
# ------------------------------------------------------------------------------


def test_simulator_initial_state():
    """Simulator must start with no devices, no transistors, and no nodes."""
    sim = DeviceSimulator()
    assert not sim.devices
    assert not sim.transistors
    assert not sim.nodes


# ------------------------------------------------------------------------------
# Device Registration Tests
# ------------------------------------------------------------------------------


def test_register_single_device():
    """Registering a single device adds it and its terminal node."""
    sim = DeviceSimulator()
    vdd = VDD()
    sim.register_device(vdd)
    assert vdd in sim.devices
    assert vdd.terminal in sim.nodes


def test_register_multiple_devices():
    """Registering multiple devices adds them and their terminal nodes."""
    sim = DeviceSimulator()
    devices: list[LogicDevice] = [VDD(), GND(), Input(), Probe(), Port()]
    sim.register_devices(devices)
    for d in devices:
        assert d in sim.devices
        assert d.terminal in sim.nodes


def test_unregister_signle_device():
    """Unregistering a single device removes it and its terminal node."""
    sim = DeviceSimulator()
    gnd = GND()
    sim.register_device(gnd)
    sim.unregister_device(gnd)
    assert gnd not in sim.devices
    assert gnd.terminal not in sim.nodes


def test_unregister_multiple_devices():
    """Unregistering multiple devices removes them and their terminal nodes."""
    sim = DeviceSimulator()
    devices: list[LogicDevice] = [VDD(), GND(), Input(), Probe(), Port()]
    sim.register_devices(devices)
    sim.unregister_devices(devices)
    for d in devices:
        assert d not in sim.devices
        assert d.terminal not in sim.nodes


def test_register_single_transistor():
    """Registering a transistor adds it and its terminal nodes."""
    sim = DeviceSimulator()
    nmos = NMOS()
    sim.register_transistor(nmos)
    assert nmos in sim.transistors
    assert nmos.gate in sim.nodes
    assert nmos.source in sim.nodes
    assert nmos.drain in sim.nodes


def test_register_multiple_transistors():
    """Registering multiple transistors adds them and their terminal nodes."""
    sim = DeviceSimulator()
    transistors: list[Transistor] = [NMOS(), PMOS()]
    sim.register_transistors(transistors)
    for t in transistors:
        assert t in sim.transistors
        assert t.gate in sim.nodes
        assert t.source in sim.nodes
        assert t.drain in sim.nodes


def test_unregister_single_transistor():
    """Unregistering a transistor removes it and its terminal nodes."""
    sim = DeviceSimulator()
    pmos = PMOS()
    sim.register_transistor(pmos)
    sim.unregister_transistor(pmos)
    assert pmos not in sim.transistors
    assert pmos.gate not in sim.nodes
    assert pmos.source not in sim.nodes
    assert pmos.drain not in sim.nodes


def test_unregister_multiple_transistors():
    """Unregistering multiple transistors removes them and their terminal nodes."""
    sim = DeviceSimulator()
    transistors: list[Transistor] = [NMOS(), PMOS()]
    sim.register_transistors(transistors)
    sim.unregister_transistors(transistors)
    for t in transistors:
        assert t not in sim.transistors
        assert t.gate not in sim.nodes
        assert t.source not in sim.nodes
        assert t.drain not in sim.nodes


# ------------------------------------------------------------------------------
# Connectivity Tests
# ------------------------------------------------------------------------------


def test_connect_creates_bidirectional_connection():
    """Connecting two nodes creates a bidirectional connection."""
    sim = DeviceSimulator()
    a = Node()
    b = Node()
    sim.connect(a, b)
    assert a in b.get_connections()
    assert b in a.get_connections()


def test_disconnect_removes_bidirectional_connection():
    """Disconnecting two nodes removes the bidirectional connection."""
    sim = DeviceSimulator()
    a = Node()
    b = Node()
    sim.connect(a, b)
    sim.disconnect(a, b)
    assert a not in b.get_connections()
    assert b not in a.get_connections()


# ------------------------------------------------------------------------------
# Static Behavior Tick Tests
# ------------------------------------------------------------------------------


def test_tick_with_simple_devices():
    """Devices must drive their terminal Nodes after a tick()."""
    sim = DeviceSimulator()
    inp = Input()
    probe = Probe()
    sim.register_devices([inp, probe])
    sim.connect(inp.terminal, probe.terminal)
    inp.set_value(LogicValue.ONE)
    sim.tick()
    assert probe.sample() is LogicValue.ONE
    inp.set_value(LogicValue.ZERO)
    sim.tick()
    assert probe.sample() is LogicValue.ZERO


# ------------------------------------------------------------------------------
# Dynamic Behavior Tick Tests
# ------------------------------------------------------------------------------


def test_tick_cmos_inverter():
    """CMOS inverter must function correctly."""
    sim = DeviceSimulator()
    vdd = VDD()
    gnd = GND()
    inp = Input()
    probe = Probe()
    inp_port = Port()
    out_port = Port()
    pmos = PMOS()
    nmos = NMOS()
    sim.register_devices([vdd, gnd, inp, probe, inp_port, out_port])
    sim.register_transistors([pmos, nmos])
    sim.connect(inp.terminal, inp_port.terminal)
    sim.connect(inp_port.terminal, pmos.gate)
    sim.connect(inp_port.terminal, nmos.gate)
    sim.connect(vdd.terminal, pmos.source)
    sim.connect(gnd.terminal, nmos.source)
    sim.connect(pmos.drain, out_port.terminal)
    sim.connect(nmos.drain, out_port.terminal)
    sim.connect(out_port.terminal, probe.terminal)
    # Input = 0 → Probe = 1
    inp.set_value(LogicValue.ZERO)
    sim.tick()
    assert probe.sample() is LogicValue.ONE
    # Input = 1 → Probe = 0
    inp.set_value(LogicValue.ONE)
    sim.tick()
    assert probe.sample() is LogicValue.ZERO
