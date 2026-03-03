"""Unit tests for LogicValue module."""

from itertools import product
import pytest
from sirc.core import LogicValue

VALUES = tuple(LogicValue)


def expected_resolution(values: tuple[LogicValue, ...]) -> LogicValue:
    """Compute the expected resolution."""
    mask = 0b000
    for value in values:
        mask |= value
    return LogicValue.resolve_mask(mask)


# ------------------------------------------------------------------------------
# Driver Resolution Tests
# ------------------------------------------------------------------------------


def test_resolve_all_empty_returns_z():
    """Test that resolving an empty list returns Z."""
    assert LogicValue.resolve_all([]) is LogicValue.Z


@pytest.mark.parametrize("value", VALUES)
def test_resolve_all_single_value(value: LogicValue):
    """Test that resolving a single value returns that value."""
    assert LogicValue.resolve_all([value]) is value


@pytest.mark.parametrize("values", product(VALUES, repeat=3))
def test_resolve_all_matches_resolve_mask(values: tuple[LogicValue, ...]):
    """Test that resolve_all matches resolve_mask for 3-driver combinations."""
    expected = expected_resolution(values)
    assert LogicValue.resolve_all(values) is expected


@pytest.mark.parametrize(
    "mask, expected",
    [
        (0b000, LogicValue.Z),
        (0b001, LogicValue.ZERO),
        (0b010, LogicValue.ONE),
        (0b011, LogicValue.X),
        (0b100, LogicValue.X),
        (0b101, LogicValue.X),
        (0b110, LogicValue.X),
        (0b111, LogicValue.X),
    ],
)
def test_resolve_mask_table(mask: int, expected: LogicValue):
    """Test direct resolution of all valid driver masks."""
    assert LogicValue.resolve_mask(mask) is expected


# -----------------------------------------------------------------------------
# Display Helpers Tests
# -----------------------------------------------------------------------------


def test_str():
    """Test the __str__ method of LogicValue."""
    assert str(LogicValue.ZERO) == "0"
    assert str(LogicValue.ONE) == "1"
    assert str(LogicValue.X) == "X"
    assert str(LogicValue.Z) == "Z"


def test_repr():
    """Test the __repr__ method of LogicValue."""
    assert repr(LogicValue.ZERO) == "LogicValue.ZERO"
    assert repr(LogicValue.ONE) == "LogicValue.ONE"
    assert repr(LogicValue.X) == "LogicValue.X"
    assert repr(LogicValue.Z) == "LogicValue.Z"
