"""Unit tests for LogicValue module."""

import pytest
from sirc.core import LogicValue, Z, ZERO, ONE, X, RESOLVE_TABLE

MASK_CASES = (
    (0b000, Z, LogicValue.Z),
    (0b001, ZERO, LogicValue.ZERO),
    (0b010, ONE, LogicValue.ONE),
    (0b011, X, LogicValue.X),
    (0b100, X, LogicValue.X),
    (0b101, X, LogicValue.X),
    (0b110, X, LogicValue.X),
    (0b111, X, LogicValue.X),
)

MASKS = tuple(mask for mask, _, _ in MASK_CASES)
EXPECTED_RESOLVE_TABLE = (Z, ZERO, ONE, X, X, X, X, X)


def test_resolve_table_contract() -> None:
    """Test full raw resolution table contract."""
    assert RESOLVE_TABLE == EXPECTED_RESOLVE_TABLE


def test_raw_logic_constants() -> None:
    """Test canonical raw logic constants."""
    assert Z == 0b000
    assert ZERO == 0b001
    assert ONE == 0b010
    assert X == 0b100


def test_logic_value_members() -> None:
    """Test LogicValue members match canonical raw values."""
    assert LogicValue.Z == Z
    assert LogicValue.ZERO == ZERO
    assert LogicValue.ONE == ONE
    assert LogicValue.X == X


@pytest.mark.parametrize(("mask", "expected_raw", "_"), MASK_CASES)
def test_resolve_table(mask: int, expected_raw: int, _: LogicValue) -> None:
    """Test raw mask resolution through RESOLVE_TABLE."""
    assert RESOLVE_TABLE[mask] == expected_raw


def test_logic_value_resolve_empty_returns_z() -> None:
    """Test empty semantic resolution."""
    assert LogicValue.resolve([]) is LogicValue.Z


@pytest.mark.parametrize(("mask", "_", "expected_logic"), MASK_CASES)
def test_logic_value_resolve_mask(
    mask: int, _: int, expected_logic: LogicValue
) -> None:
    """Test semantic resolution of valid masks."""
    assert LogicValue.resolve([mask]) is expected_logic


@pytest.mark.parametrize("left", MASKS)
@pytest.mark.parametrize("right", MASKS)
def test_logic_value_resolve_mixed_masks(left: int, right: int) -> None:
    """Test semantic resolution of mixed valid masks."""
    assert LogicValue.resolve([left, right]) is LogicValue(RESOLVE_TABLE[left | right])


def test_logic_value_str() -> None:
    """Test compact display symbols."""
    assert str(LogicValue.Z) == "Z"
    assert str(LogicValue.ZERO) == "0"
    assert str(LogicValue.ONE) == "1"
    assert str(LogicValue.X) == "X"


def test_logic_value_repr() -> None:
    """Test debug representations."""
    assert repr(LogicValue.Z) == "LogicValue.Z"
    assert repr(LogicValue.ZERO) == "LogicValue.ZERO"
    assert repr(LogicValue.ONE) == "LogicValue.ONE"
    assert repr(LogicValue.X) == "LogicValue.X"
