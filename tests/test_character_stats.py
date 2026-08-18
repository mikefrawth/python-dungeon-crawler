import pytest

from character_stats import CharacterStats

@pytest.fixture
def stats():
    return CharacterStats(
        strength=16, dexterity=14, constitution=12, intelligence=10, wisdom=8, ego=6
    )


def test_character_stats_stores_scores(stats):
    assert stats.strength == 16
    assert stats.dexterity == 14
    assert stats.constitution == 12
    assert stats.intelligence == 10
    assert stats.wisdom == 8
    assert stats.ego == 6


def test_positive_modifier(stats):
    assert stats.get_modifier(stats.strength) == 3


def test_zero_modifier(stats):
    assert stats.get_modifier(stats.intelligence) == 0


def test_negative_modifier():
    stats = CharacterStats(strength=6)
    assert stats.get_modifier(stats.strength) == -2

def test_odd_score_modifier_rounds_down():
    stats = CharacterStats(strength=9)
    assert stats.get_modifier(stats.strength) == -1

def test_format_positive_stat(stats):
    assert stats.format_stat("strength") == "Strength 16 (+3)"


def test_format_zero_stat(stats):
    assert stats.format_stat("intelligence") == "Intelligence 10 (+0)"


def test_format_negative_stat(stats):
    assert stats.format_stat("wisdom") == "Wisdom 8 (-1)"
