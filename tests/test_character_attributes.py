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


def test_effective_value_at_baseline_is_zero():
    attributes = CharacterAttributes(intellect=0)
    assert attributes.effective_value("intellect") == 0


def test_effective_value_positive_raw_is_positive():
    attributes = CharacterAttributes(might=16)
    assert attributes.effective_value("might") > 0


def test_effective_value_diminishing_returns():
    small = CharacterAttributes(might=4)
    large = CharacterAttributes(might=8)

    small_effective = small.effective_value("might")
    large_effective = large.effective_value("might")

    assert large_effective > small_effective
    assert large_effective < small_effective * 2


def test_effective_value_symmetric_for_negative():
    positive = CharacterAttributes(ego=9)
    negative = CharacterAttributes(ego=-9)

    assert negative.effective_value("ego") == -positive.effective_value("ego")


def test_effective_value_coefficient_is_per_attribute():
    assert set(CharacterAttributes.DEFAULT_COEFFICIENTS.keys()) == set(
        CharacterAttributes.ATTRIBUTE_NAMES
    )

    doubled = CharacterAttributes(might=9)
    doubled.coefficients["might"] *= 2
    unchanged = CharacterAttributes(might=9)

    assert doubled.effective_value("might") == pytest.approx(
        unchanged.effective_value("might") * 2
    )
    assert unchanged.coefficients["might"] == CharacterAttributes.DEFAULT_COEFFICIENT


def test_effective_value_does_not_change_format_attribute(attributes):
    attributes.effective_value("might")
    assert attributes.format_attribute("might") == "Might 16"
