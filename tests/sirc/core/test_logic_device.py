"""Unit tests for LogicDevice module."""

from typing import Protocol
import pytest
from sirc.core import (
    LogicValue,
    Node,
    LogicDevice,
    LogicDeviceKind,
    VDD,
    GND,
    Input,
    Probe,
    Port,
)

DEVICES: list[tuple[type[LogicDevice], int, int, LogicDeviceKind]] = [
    (VDD, 1, 1, LogicDeviceKind.VDD),
    (GND, 2, 2, LogicDeviceKind.GND),
    (Input, 3, 3, LogicDeviceKind.INPUT),
    (Probe, 4, 4, LogicDeviceKind.PROBE),
    (Port, 5, 5, LogicDeviceKind.PORT),
]


# pylint: disable=too-few-public-methods
class LogicDeviceConstructor(Protocol):
    """Callable constructor for LogicDevice subclasses used in tests."""

    def __call__(self, device_id: int, node: Node) -> LogicDevice: ...


# ------------------------------------------------------------------------------
# Construction Tests
# ------------------------------------------------------------------------------


@pytest.mark.parametrize("device_class, device_id, node_id, expected_kind", DEVICES)
def test_device_stores_id_and_kind(
    device_class: LogicDeviceConstructor,
    device_id: int,
    node_id: int,
    expected_kind: LogicDeviceKind,
):
    """A LogicDevice must store the provided ID and device kind."""
    device = device_class(device_id, Node(node_id))
    assert device.id_ == device_id
    assert device.kind is expected_kind


# ------------------------------------------------------------------------------
# Driving Behaviour Tests
# ------------------------------------------------------------------------------


def test_vdd_drives_one():
    """VDD must drive LogicValue.ONE onto its terminal Node."""
    vdd = VDD(1, Node(1))
    assert vdd.node.default_value is LogicValue.ONE


def test_gnd_drives_zero():
    """GND must drive LogicValue.ZERO onto its terminal Node."""
    gnd = GND(1, Node(1))
    assert gnd.node.default_value is LogicValue.ZERO


def test_input_defaults_to_z():
    """Input terminal Node must default to LogicValue.Z."""
    inp = Input(1, Node(1))
    assert inp.node.default_value is LogicValue.Z


@pytest.mark.parametrize("value", tuple(LogicValue))
def test_input_set_value(value: LogicValue):
    """Input.set_value() must update the terminal Node default_value."""
    inp = Input(1, Node(1))
    inp.set_value(value)
    assert inp.node.default_value is value


# ------------------------------------------------------------------------------
# Probe Tests
# ------------------------------------------------------------------------------


def test_probe_defaults_to_z():
    """Probe terminal Node must default to LogicValue.Z."""
    probe = Probe(1, Node(1))
    assert probe.node.default_value is LogicValue.Z


@pytest.mark.parametrize("value", tuple(LogicValue))
def test_probe_sample(value: LogicValue):
    """Probe.sample() must return the terminal Node resolved_value."""
    probe = Probe(1, Node(1))
    probe.node.resolved_value = value
    assert probe.sample() is value


# ------------------------------------------------------------------------------
# Port Tests
# ------------------------------------------------------------------------------


def test_port_defaults_to_z():
    """Port terminal Node must default to LogicValue.Z."""
    port = Port(1, Node(1))
    assert port.node.default_value is LogicValue.Z


# ------------------------------------------------------------------------------
# Debug Representation Tests
# ------------------------------------------------------------------------------


@pytest.mark.parametrize("device_class, device_id, node_id, expected_kind", DEVICES)
def test_repr(
    device_class: LogicDeviceConstructor,
    device_id: int,
    node_id: int,
    expected_kind: LogicDeviceKind,
):
    """__repr__ must include class name, ID, kind, and terminal Node."""
    device = device_class(device_id, Node(node_id))
    assert repr(device) == (
        f"<{type(device).__name__} id={device_id} kind={expected_kind!r} "
        f"terminal={device.node!r}>"
    )
