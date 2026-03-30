"""Unit tests for LogicValue module."""

import pytest
from sirc.core import LogicValue, ZERO, ONE, X, Z, RESOLVE_TABLE

MASKS = (0b000, 0b001, 0b010, 0b011, 0b100, 0b101, 0b110, 0b111)
RAW_VALUES = (Z, ZERO, ONE, X, X, X, X, X)
LOGIC_VALUES = (
    LogicValue.Z,
    LogicValue.ZERO,
    LogicValue.ONE,
    LogicValue.X,
    LogicValue.X,
    LogicValue.X,
    LogicValue.X,
    LogicValue.X,
)

# ------------------------------------------------------------------------------
# Simulator Driver Resolution Tests
# ------------------------------------------------------------------------------


@pytest.mark.parametrize(("mask", "expected"), tuple(zip(MASKS, RAW_VALUES)))
def test_resolve_table(mask: int, expected: int):
    """Test direct resolution of all valid driver masks."""
    assert RESOLVE_TABLE[mask] == expected


# ------------------------------------------------------------------------------
# LogicValue Resolution Tests
# ------------------------------------------------------------------------------


def test_resolve_all_empty_returns_z():
    """Test that resolving an empty list returns Z."""
    assert LogicValue.resolve_all([]) is LogicValue.Z


@pytest.mark.parametrize(("mask", "expected"), tuple(zip(MASKS, LOGIC_VALUES)))
def test_resolve_all(mask: int, expected: LogicValue):
    """Test logic resolution of all valid driver masks."""
    assert LogicValue.resolve_all([mask]) is expected


@pytest.mark.parametrize(("mask", "expected"), tuple(zip(MASKS, LOGIC_VALUES)))
def test_resolve_mask(mask: int, expected: LogicValue):
    """Test logic resolution of all valid driver masks."""
    assert LogicValue.resolve_mask(mask) is expected


# ------------------------------------------------------------------------------
# Equivalence Tests
# ------------------------------------------------------------------------------


@pytest.mark.parametrize("mask", MASKS)
def test_simulator_equivalent_logic_value(mask: int):
    """Test direct resolution is equivalent to logic resolution."""
    assert RESOLVE_TABLE[mask] == LogicValue.resolve_mask(mask)


# -----------------------------------------------------------------------------
# Display Helpers Tests
# -----------------------------------------------------------------------------


def test_str():
    """Test LogicValue string conversion."""
    assert str(LogicValue.ZERO) == "0"
    assert str(LogicValue.ONE) == "1"
    assert str(LogicValue.X) == "X"
    assert str(LogicValue.Z) == "Z"


def test_repr():
    """Test LogicValue debug representation."""
    assert repr(LogicValue.ZERO) == "LogicValue.ZERO"
    assert repr(LogicValue.ONE) == "LogicValue.ONE"
    assert repr(LogicValue.X) == "LogicValue.X"
    assert repr(LogicValue.Z) == "LogicValue.Z"
