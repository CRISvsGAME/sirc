"""Unit tests for sirc.core.logic module."""

import pytest
from sirc.core.logic import LogicValue

# ------------------------------------------------------------------------------
# State Property Tests
# ------------------------------------------------------------------------------


def test_logicvalue_properties():
    """Test the is_zero, is_one, is_x, is_z properties of LogicValue."""
    assert LogicValue.ZERO.is_zero
    assert not LogicValue.ZERO.is_one
    assert not LogicValue.ZERO.is_x
    assert not LogicValue.ZERO.is_z

    assert LogicValue.ONE.is_one
    assert not LogicValue.ONE.is_zero
    assert not LogicValue.ONE.is_x
    assert not LogicValue.ONE.is_z

    assert LogicValue.X.is_x
    assert not LogicValue.X.is_zero
    assert not LogicValue.X.is_one
    assert not LogicValue.X.is_z

    assert LogicValue.Z.is_z
    assert not LogicValue.Z.is_zero
    assert not LogicValue.Z.is_one
    assert not LogicValue.Z.is_x


# ------------------------------------------------------------------------------
# Two-Driver Resolution Tests
# ------------------------------------------------------------------------------


@pytest.mark.parametrize(
    "a, b, expected",
    [
        # Row: 0
        (LogicValue.ZERO, LogicValue.ZERO, LogicValue.ZERO),
        (LogicValue.ZERO, LogicValue.ONE, LogicValue.X),
        (LogicValue.ZERO, LogicValue.X, LogicValue.X),
        (LogicValue.ZERO, LogicValue.Z, LogicValue.ZERO),
        # Row: 1
        (LogicValue.ONE, LogicValue.ZERO, LogicValue.X),
        (LogicValue.ONE, LogicValue.ONE, LogicValue.ONE),
        (LogicValue.ONE, LogicValue.X, LogicValue.X),
        (LogicValue.ONE, LogicValue.Z, LogicValue.ONE),
        # Row: X
        (LogicValue.X, LogicValue.ZERO, LogicValue.X),
        (LogicValue.X, LogicValue.ONE, LogicValue.X),
        (LogicValue.X, LogicValue.X, LogicValue.X),
        (LogicValue.X, LogicValue.Z, LogicValue.X),
        # Row: Z
        (LogicValue.Z, LogicValue.ZERO, LogicValue.ZERO),
        (LogicValue.Z, LogicValue.ONE, LogicValue.ONE),
        (LogicValue.Z, LogicValue.X, LogicValue.X),
        (LogicValue.Z, LogicValue.Z, LogicValue.Z),
    ],
)
def test_two_driver_resolution(a: LogicValue, b: LogicValue, expected: LogicValue):
    """Test two-driver resolution of LogicValue."""
    assert a.resolve(b) is expected
    assert b.resolve(a) is expected


# ------------------------------------------------------------------------------
# Multi-Driver Resolution Tests
# ------------------------------------------------------------------------------


def test_resolve_all_empty_raises():
    """Test that resolving an empty list raises ValueError."""
    with pytest.raises(ValueError):
        LogicValue.resolve_all([])
