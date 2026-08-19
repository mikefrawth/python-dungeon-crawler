import pytest

from character import Character
from character_attributes import CharacterAttributes
from investment_allocation import InvestmentAllocation


@pytest.fixture
def attributes():
    return CharacterAttributes(
        might=16, toughness=14, agility=12, perception=10, intellect=8, ego=6
    )


def test_character_stores_name_attributes_and_level(attributes):
    character = Character("Aveline", attributes, level=3)

    assert character.name == "Aveline"
    assert character.attributes is attributes
    assert character.level == 3


def test_character_level_defaults_to_default_level(attributes):
    character = Character("Aveline", attributes)

    assert character.level == Character.DEFAULT_LEVEL
    assert character.level == 0


def test_character_level_zero_is_valid(attributes):
    character = Character("Generic Guard", attributes, level=0)

    assert character.level == 0


def test_character_level_has_no_enforced_maximum(attributes):
    character = Character("Ancient One", attributes, level=9999)

    assert character.level == 9999


def test_character_exposes_raw_and_effective_attribute_values(attributes):
    character = Character("Aveline", attributes)

    assert character.attributes.might == 16
    assert character.attributes.effective_value("might") > 0


def test_character_starts_with_no_skills_or_feats(attributes):
    character = Character("Aveline", attributes)

    assert character.skills == []
    assert character.feats == []


def test_create_player_builds_character_from_fully_spent_allocation():
    allocation = InvestmentAllocation.for_player_creation()
    allocation.spend("might", 10)
    allocation.spend("toughness", 10)

    character = Character.create_player("Aveline", allocation)

    assert character.name == "Aveline"
    assert character.level == 1
    assert character.attributes is allocation.attributes
    assert character.attributes.might == 10
    assert character.attributes.toughness == 10


def test_create_player_rejects_unspent_points():
    allocation = InvestmentAllocation.for_player_creation()
    allocation.spend("might", 10)

    with pytest.raises(ValueError):
        Character.create_player("Aveline", allocation)


def test_create_player_rejects_a_fresh_unspent_allocation():
    allocation = InvestmentAllocation.for_player_creation()

    with pytest.raises(ValueError):
        Character.create_player("Aveline", allocation)
