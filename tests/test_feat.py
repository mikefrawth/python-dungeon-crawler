import pytest

from character import Character
from character_attributes import CharacterAttributes
from feat import Feat


@pytest.fixture
def character():
    attributes = CharacterAttributes(might=16)
    return Character("Aveline", attributes)


def test_feat_stores_name_and_governing_attribute():
    feat = Feat("Brutal Momentum", "might")

    assert feat.name == "Brutal Momentum"
    assert feat.governing_attribute == "might"


def test_feat_rejects_unknown_governing_attribute():
    with pytest.raises(ValueError):
        Feat("Brutal Momentum", "luck")


def test_feat_has_no_gating_method():
    feat = Feat("Brutal Momentum", "might")

    assert not hasattr(feat, "is_usable_by")
    assert not hasattr(feat, "minimum_requirement")


def test_scaled_output_reads_effective_value(character):
    feat = Feat("Brutal Momentum", "might")

    assert feat.scaled_output(character) == character.attributes.effective_value(
        "might"
    )


def test_scaled_output_applies_magnitude_coefficient(character):
    feat = Feat("Brutal Momentum", "might", magnitude_coefficient=1.5)

    assert feat.scaled_output(character) == pytest.approx(
        character.attributes.effective_value("might") * 1.5
    )


def test_scaled_output_uses_override_when_present(character):
    def scripted_effect(feat, character):
        return 7

    feat = Feat("Scripted Feat", "might", override=scripted_effect)

    assert feat.scaled_output(character) == 7
