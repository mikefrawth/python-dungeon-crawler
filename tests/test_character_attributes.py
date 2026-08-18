import pytest

from character_attributes import CharacterAttributes


@pytest.fixture
def attributes():
    return CharacterAttributes(
        might=16, toughness=14, agility=12, perception=10, intellect=8, ego=6
    )


def test_character_attributes_stores_scores(attributes):
    assert attributes.might == 16
    assert attributes.toughness == 14
    assert attributes.agility == 12
    assert attributes.perception == 10
    assert attributes.intellect == 8
    assert attributes.ego == 6


def test_format_positive_attribute(attributes):
    assert attributes.format_attribute("might") == "Might 16"


def test_format_zero_attribute():
    attributes = CharacterAttributes(intellect=0)
    assert attributes.format_attribute("intellect") == "Intellect 0"


def test_format_negative_attribute():
    attributes = CharacterAttributes(ego=-4)
    assert attributes.format_attribute("ego") == "Ego -4"
