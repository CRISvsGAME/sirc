"""Unit tests for sirc.core.logic module."""

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
