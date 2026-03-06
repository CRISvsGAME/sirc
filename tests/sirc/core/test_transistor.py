"""Unit tests for Transistor module."""

from typing import Protocol
import pytest
from sirc.core import LogicValue, Node, NodeKind, Transistor, TransistorKind, NMOS, PMOS

TRANSISTORS: list[tuple[type[Transistor], int, int, int, int, TransistorKind]] = [
    (NMOS, 1, 1, 2, 3, TransistorKind.NMOS),
    (PMOS, 2, 4, 5, 6, TransistorKind.PMOS),
]


# pylint: disable=too-few-public-methods
class TransistorConstructor(Protocol):
    """Callable constructor for Transistor subclasses used in tests."""

    def __call__(
        self,
        transistor_id: int,
        gate: Node,
        source: Node,
        drain: Node,
    ) -> Transistor: ...


# ------------------------------------------------------------------------------
# Transistor Construction Tests
# ------------------------------------------------------------------------------


@pytest.mark.parametrize(
    "transistor_class, transistor_id, gate_id, source_id, drain_id, expected_kind",
    TRANSISTORS,
)
# pylint: disable=too-many-arguments, too-many-positional-arguments
def test_transistor_stores_id_kind_and_terminals(
    transistor_class: TransistorConstructor,
    transistor_id: int,
    gate_id: int,
    source_id: int,
    drain_id: int,
    expected_kind: TransistorKind,
):
    """A transistor must store its ID, kind, and terminal Nodes."""
    g = Node(gate_id, kind=NodeKind.GATE)
    s = Node(source_id)
    d = Node(drain_id)
    t = transistor_class(transistor_id, g, s, d)
    assert t.id_ == transistor_id
    assert t.kind is expected_kind
    assert t.gate is g
    assert t.source is s
    assert t.drain is d


# ------------------------------------------------------------------------------
# NMOS Conduction Tests
# ------------------------------------------------------------------------------


@pytest.mark.parametrize(
    "gate_value, expected",
    [
        (LogicValue.ZERO, False),
        (LogicValue.ONE, True),
        (LogicValue.X, False),
        (LogicValue.Z, False),
    ],
)
def test_nmos_conduction_rules(gate_value: LogicValue, expected: bool):
    """NMOS must conduct only when gate is LogicValue.ONE."""
    g = Node(1, kind=NodeKind.GATE)
    s = Node(2)
    d = Node(3)
    t = NMOS(1, g, s, d)
    t.gate.resolved_value = gate_value
    assert t.is_conducting() is expected


# ------------------------------------------------------------------------------
# PMOS Conduction Tests
# ------------------------------------------------------------------------------


@pytest.mark.parametrize(
    "gate_value, expected",
    [
        (LogicValue.ZERO, True),
        (LogicValue.ONE, False),
        (LogicValue.X, False),
        (LogicValue.Z, False),
    ],
)
def test_pmos_conduction_rules(gate_value: LogicValue, expected: bool):
    """PMOS must conduct only when gate is LogicValue.ZERO."""
    g = Node(1, kind=NodeKind.GATE)
    s = Node(2)
    d = Node(3)
    t = PMOS(1, g, s, d)
    t.gate.resolved_value = gate_value
    assert t.is_conducting() is expected


# ------------------------------------------------------------------------------
# Polymorphism Tests
# ------------------------------------------------------------------------------


@pytest.mark.parametrize(
    "transistor_class, transistor_id, gate_id, source_id, drain_id, expected_kind",
    TRANSISTORS,
)
# pylint: disable=too-many-arguments, too-many-positional-arguments
def test_nmos_and_pmos_share_same_interface(
    transistor_class: TransistorConstructor,
    transistor_id: int,
    gate_id: int,
    source_id: int,
    drain_id: int,
    expected_kind: TransistorKind,
):
    """NMOS and PMOS must both be Transistor subclasses."""
    g = Node(gate_id, kind=NodeKind.GATE)
    s = Node(source_id)
    d = Node(drain_id)
    t = transistor_class(transistor_id, g, s, d)
    assert isinstance(t, Transistor)
    assert t.kind is expected_kind


# ------------------------------------------------------------------------------
# Debug Representation Tests
# ------------------------------------------------------------------------------


@pytest.mark.parametrize(
    "transistor_class, transistor_id, gate_id, source_id, drain_id, expected_kind",
    TRANSISTORS,
)
# pylint: disable=too-many-arguments, too-many-positional-arguments
def test_transistor_repr_format(
    transistor_class: TransistorConstructor,
    transistor_id: int,
    gate_id: int,
    source_id: int,
    drain_id: int,
    expected_kind: TransistorKind,
):
    """Transistor __repr__ must return the expected debug representation."""
    g = Node(gate_id, kind=NodeKind.GATE)
    s = Node(source_id)
    d = Node(drain_id)
    t = transistor_class(transistor_id, g, s, d)
    assert repr(t) == (
        f"<{type(t).__name__} id={transistor_id} kind={expected_kind!r} "
        f"gate={g!r} source={s!r} drain={d!r}>"
    )
