import pytest

from character import Character
from character_attributes import CharacterAttributes
from skill import Skill


@pytest.fixture
def character():
    attributes = CharacterAttributes(might=16, perception=4)
    return Character("Aveline", attributes)


def test_skill_stores_name_and_governing_attribute():
    skill = Skill("Power Strike", "might", minimum_requirement=1)

    assert skill.name == "Power Strike"
    assert skill.governing_attribute == "might"
    assert skill.minimum_requirement == 1


def test_skill_rejects_unknown_governing_attribute():
    with pytest.raises(ValueError):
        Skill("Power Strike", "luck", minimum_requirement=1)


def test_is_usable_by_true_when_effective_value_meets_minimum(character):
    skill = Skill("Power Strike", "might", minimum_requirement=1)

    assert skill.is_usable_by(character) is True


def test_is_usable_by_false_when_effective_value_below_minimum(character):
    skill = Skill("Mind Spike", "perception", minimum_requirement=10)

    assert skill.is_usable_by(character) is False


def test_is_usable_by_compares_effective_value_not_raw(character):
    # raw perception (4) clears a minimum_requirement of 3, but its
    # effective_value (sqrt(4) == 2.0) does not - the gate must fail here.
    skill = Skill("Mind Spike", "perception", minimum_requirement=3)

    assert character.attributes.perception == 4
    assert skill.is_usable_by(character) is False


def test_scaled_output_reads_effective_value(character):
    skill = Skill("Power Strike", "might", minimum_requirement=1)

    assert skill.scaled_output(character) == character.attributes.effective_value(
        "might"
    )


def test_scaled_output_applies_magnitude_coefficient(character):
    skill = Skill(
        "Power Strike", "might", minimum_requirement=1, magnitude_coefficient=2.0
    )

    assert skill.scaled_output(character) == pytest.approx(
        character.attributes.effective_value("might") * 2.0
    )


def test_scaled_output_uses_override_when_present(character):
    def flat_bonus(skill, character):
        return 42

    skill = Skill("Scripted Strike", "might", minimum_requirement=1, override=flat_bonus)

    assert skill.scaled_output(character) == 42
