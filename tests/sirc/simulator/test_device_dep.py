"""Unit tests for Device Simulator Dependency Module."""

from sirc.core import LogicValue, NodeKind, LogicDeviceKind, TransistorKind
from sirc.simulator import (
    IdentificationFactory,
    NodeFactory,
    LogicDeviceFactory,
    TransistorFactory,
)

# ------------------------------------------------------------------------------
# Identification Factory Tests
# ------------------------------------------------------------------------------


def test_identification_factory_allocates_monotonic_node_ids():
    """IdentificationFactory must allocate monotonic Node IDs."""
    factory = IdentificationFactory()
    node_ids = [factory.allocate_node_id() for _ in range(100)]
    for i, node_id in enumerate(node_ids):
        assert node_id == i


def test_identification_factory_allocates_monotonic_device_ids():
    """IdentificationFactory must allocate monotonic Device IDs."""
    factory = IdentificationFactory()
    device_ids = [factory.allocate_device_id() for _ in range(100)]
    for i, device_id in enumerate(device_ids):
        assert device_id == i


def test_identification_factory_allocates_monotonic_transistor_ids():
    """IdentificationFactory must allocate monotonic Transistor IDs."""
    factory = IdentificationFactory()
    transistor_ids = [factory.allocate_transistor_id() for _ in range(100)]
    for i, transistor_id in enumerate(transistor_ids):
        assert transistor_id == i


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
    for i, node in enumerate(base_nodes):
        assert node.id == i
        assert node.kind is NodeKind.BASE


def test_node_factory_creates_gate_nodes():
    """NodeFactory must create GATE Nodes with monotonic IDs."""
    factory = NodeFactory(IdentificationFactory())
    gate_nodes = [factory.create_gate_node() for _ in range(100)]
    for i, node in enumerate(gate_nodes):
        assert node.id == i
        assert node.kind is NodeKind.GATE


def test_node_factory_ids_are_shared_between_base_and_gate():
    """NodeFactory must allocate shared IDs for BASE and GATE Nodes."""
    factory = NodeFactory(IdentificationFactory())
    a = factory.create_base_node()
    b = factory.create_gate_node()
    c = factory.create_base_node()
    d = factory.create_gate_node()
    assert a.id == 0
    assert a.kind is NodeKind.BASE
    assert b.id == 1
    assert b.kind is NodeKind.GATE
    assert c.id == 2
    assert c.kind is NodeKind.BASE
    assert d.id == 3
    assert d.kind is NodeKind.GATE


# ------------------------------------------------------------------------------
# Logic Device Factory Tests
# ------------------------------------------------------------------------------


def test_logic_device_factory_creates_vdd_devices():
    """LogicDeviceFactory must create VDD devices with monotonic IDs."""
    id_factory = IdentificationFactory()
    node_factory = NodeFactory(id_factory)
    device_factory = LogicDeviceFactory(id_factory, node_factory)
    vdd_devices = [device_factory.create_vdd() for _ in range(100)]
    for i, device in enumerate(vdd_devices):
        assert device.id == i
        assert device.kind is LogicDeviceKind.VDD
        assert device.terminal.kind is NodeKind.BASE
        assert device.terminal.default_value is LogicValue.ONE


def test_logic_device_factory_creates_gnd_devices():
    """LogicDeviceFactory must create GND devices with monotonic IDs."""
    id_factory = IdentificationFactory()
    node_factory = NodeFactory(id_factory)
    device_factory = LogicDeviceFactory(id_factory, node_factory)
    gnd_devices = [device_factory.create_gnd() for _ in range(100)]
    for i, device in enumerate(gnd_devices):
        assert device.id == i
        assert device.kind is LogicDeviceKind.GND
        assert device.terminal.kind is NodeKind.BASE
        assert device.terminal.default_value is LogicValue.ZERO


def test_logic_device_factory_creates_input_devices():
    """LogicDeviceFactory must create Input devices with monotonic IDs."""
    id_factory = IdentificationFactory()
    node_factory = NodeFactory(id_factory)
    device_factory = LogicDeviceFactory(id_factory, node_factory)
    input_devices = [device_factory.create_input() for _ in range(100)]
    for i, device in enumerate(input_devices):
        assert device.id == i
        assert device.kind is LogicDeviceKind.INPUT
        assert device.terminal.kind is NodeKind.BASE
        assert device.terminal.default_value is LogicValue.Z


def test_logic_device_factory_creates_probe_devices():
    """LogicDeviceFactory must create Probe devices with monotonic IDs."""
    id_factory = IdentificationFactory()
    node_factory = NodeFactory(id_factory)
    device_factory = LogicDeviceFactory(id_factory, node_factory)
    probe_devices = [device_factory.create_probe() for _ in range(100)]
    for i, device in enumerate(probe_devices):
        assert device.id == i
        assert device.kind is LogicDeviceKind.PROBE
        assert device.terminal.kind is NodeKind.BASE
        assert device.terminal.default_value is LogicValue.Z


def test_logic_device_factory_creates_port_devices():
    """LogicDeviceFactory must create Port devices with monotonic IDs."""
    id_factory = IdentificationFactory()
    node_factory = NodeFactory(id_factory)
    device_factory = LogicDeviceFactory(id_factory, node_factory)
    port_devices = [device_factory.create_port() for _ in range(100)]
    for i, device in enumerate(port_devices):
        assert device.id == i
        assert device.kind is LogicDeviceKind.PORT
        assert device.terminal.kind is NodeKind.BASE
        assert device.terminal.default_value is LogicValue.Z


def test_logic_device_factory_ids_are_shared():
    """LogicDeviceFactory must allocate shared IDs for all LogicDevices."""
    id_factory = IdentificationFactory()
    node_factory = NodeFactory(id_factory)
    device_factory = LogicDeviceFactory(id_factory, node_factory)
    vdd = device_factory.create_vdd()
    gnd = device_factory.create_gnd()
    input_ = device_factory.create_input()
    probe = device_factory.create_probe()
    port = device_factory.create_port()
    assert vdd.id == 0
    assert gnd.id == 1
    assert input_.id == 2
    assert probe.id == 3
    assert port.id == 4


# ------------------------------------------------------------------------------
# Transistor Factory Tests
# ------------------------------------------------------------------------------


def test_transistor_factory_creates_nmos_transistors():
    """TransistorFactory must create NMOS transistors with monotonic IDs."""
    id_factory = IdentificationFactory()
    node_factory = NodeFactory(id_factory)
    transistor_factory = TransistorFactory(id_factory, node_factory)
    nmos_transistors = [transistor_factory.create_nmos() for _ in range(100)]
    for i, transistor in enumerate(nmos_transistors):
        assert transistor.id == i
        assert transistor.kind is TransistorKind.NMOS
        assert transistor.gate.kind is NodeKind.GATE
        assert transistor.source.kind is NodeKind.BASE
        assert transistor.drain.kind is NodeKind.BASE
        assert transistor.gate is not transistor.source
        assert transistor.gate is not transistor.drain
        assert transistor.source is not transistor.drain

        base = i * 3
        assert transistor.gate.id == base + 0
        assert transistor.source.id == base + 1
        assert transistor.drain.id == base + 2


def test_transistor_factory_creates_pmos_transistors():
    """TransistorFactory must create PMOS transistors with monotonic IDs."""
    id_factory = IdentificationFactory()
    node_factory = NodeFactory(id_factory)
    transistor_factory = TransistorFactory(id_factory, node_factory)
    pmos_transistors = [transistor_factory.create_pmos() for _ in range(100)]
    for i, transistor in enumerate(pmos_transistors):
        assert transistor.id == i
        assert transistor.kind is TransistorKind.PMOS
        assert transistor.gate.kind is NodeKind.GATE
        assert transistor.source.kind is NodeKind.BASE
        assert transistor.drain.kind is NodeKind.BASE
        assert transistor.gate is not transistor.source
        assert transistor.gate is not transistor.drain
        assert transistor.source is not transistor.drain

        base = i * 3
        assert transistor.gate.id == base + 0
        assert transistor.source.id == base + 1
        assert transistor.drain.id == base + 2


def test_transistor_factory_ids_are_shared():
    """TransistorFactory must allocate shared IDs for all Transistors."""
    id_factory = IdentificationFactory()
    node_factory = NodeFactory(id_factory)
    transistor_factory = TransistorFactory(id_factory, node_factory)
    a = transistor_factory.create_nmos()
    b = transistor_factory.create_pmos()
    c = transistor_factory.create_nmos()
    d = transistor_factory.create_pmos()
    assert a.id == 0
    assert b.id == 1
    assert c.id == 2
    assert d.id == 3
