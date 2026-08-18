import pytest

from character_attributes import CharacterAttributes
from investment_allocation import InvestmentAllocation


def test_for_player_creation_starts_at_baseline():
    allocation = InvestmentAllocation.for_player_creation()

    for name in CharacterAttributes.ATTRIBUTE_NAMES:
        assert getattr(allocation.attributes, name) == CharacterAttributes.BASELINE


def test_for_player_creation_uses_player_pool_and_cap():
    allocation = InvestmentAllocation.for_player_creation()

    assert allocation.investment_pool == InvestmentAllocation.PLAYER_INVESTMENT_POOL
    assert allocation.investment_cap == InvestmentAllocation.PLAYER_INVESTMENT_CAP


def test_points_spent_starts_at_zero():
    allocation = InvestmentAllocation.for_player_creation()

    assert allocation.points_spent == 0
    assert allocation.points_remaining == allocation.investment_pool


def test_spend_raises_attribute_and_lowers_remaining():
    allocation = InvestmentAllocation.for_player_creation()

    allocation.spend("might", 3)

    assert allocation.attributes.might == 3
    assert allocation.points_spent == 3
    assert allocation.points_remaining == allocation.investment_pool - 3


def test_spend_rejects_exceeding_the_cap():
    allocation = InvestmentAllocation(
        CharacterAttributes(), investment_pool=20, investment_cap=10
    )
    allocation.spend("might", 10)

    with pytest.raises(ValueError):
        allocation.spend("might", 1)


def test_spend_rejects_exceeding_the_pool():
    allocation = InvestmentAllocation(
        CharacterAttributes(), investment_pool=5, investment_cap=10
    )

    with pytest.raises(ValueError):
        allocation.spend("might", 6)


def test_undo_lowers_attribute_and_restores_remaining():
    allocation = InvestmentAllocation.for_player_creation()
    allocation.spend("might", 3)

    allocation.undo("might", 1)

    assert allocation.attributes.might == 2
    assert allocation.points_spent == 2
    assert allocation.points_remaining == allocation.investment_pool - 2


def test_undo_rejects_going_below_the_creation_snapshot():
    allocation = InvestmentAllocation.for_player_creation()

    with pytest.raises(ValueError):
        allocation.undo("might", 1)


def test_leveling_pass_measures_spend_relative_to_its_own_snapshot():
    leveled_up_character = CharacterAttributes(might=8, toughness=6)

    allocation = InvestmentAllocation(
        leveled_up_character, investment_pool=5, investment_cap=100
    )

    assert allocation.points_spent == 0
    assert allocation.points_remaining == 5

    allocation.spend("might", 2)

    assert allocation.attributes.might == 10
    assert allocation.points_spent == 2
    assert allocation.points_remaining == 3


def test_leveling_pass_undo_floor_is_the_pass_snapshot_not_zero():
    leveled_up_character = CharacterAttributes(might=8)
    allocation = InvestmentAllocation(
        leveled_up_character, investment_pool=5, investment_cap=100
    )

    with pytest.raises(ValueError):
        allocation.undo("might", 1)


def test_spend_rejects_a_negative_amount():
    allocation = InvestmentAllocation.for_player_creation()

    with pytest.raises(ValueError):
        allocation.spend("might", -50)

    assert allocation.attributes.might == CharacterAttributes.BASELINE


def test_spend_rejects_a_zero_amount():
    allocation = InvestmentAllocation.for_player_creation()

    with pytest.raises(ValueError):
        allocation.spend("might", 0)


def test_undo_rejects_a_negative_amount():
    allocation = InvestmentAllocation(
        CharacterAttributes(might=10), investment_pool=20, investment_cap=100
    )

    with pytest.raises(ValueError):
        allocation.undo("might", -5)

    assert allocation.attributes.might == 10


def test_undo_rejects_a_zero_amount():
    allocation = InvestmentAllocation.for_player_creation()
    allocation.spend("might", 3)

    with pytest.raises(ValueError):
        allocation.undo("might", 0)


def test_spend_rejects_an_unknown_attribute_name():
    allocation = InvestmentAllocation.for_player_creation()

    with pytest.raises(ValueError):
        allocation.spend("coefficients", 1)


def test_undo_rejects_an_unknown_attribute_name():
    allocation = InvestmentAllocation.for_player_creation()

    with pytest.raises(ValueError):
        allocation.undo("not_a_real_attribute", 1)
