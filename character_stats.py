class CharacterStats:
    STAT_NAMES = (
        "strength",
        "dexterity",
        "constitution",
        "intelligence",
        "wisdom",
        "ego",
    )

    def __init__(
        self,
        strength: int = 10,
        dexterity: int = 10,
        constitution: int = 10,
        intelligence: int = 10,
        wisdom: int = 10,
        ego: int = 10,
    ):
        self.strength = strength
        self.dexterity = dexterity
        self.constitution = constitution
        self.intelligence = intelligence
        self.wisdom = wisdom
        self.ego = ego

    @staticmethod
    def get_modifier(ability_score: int):
        return (ability_score - 10) // 2

    def format_stat(self, stat_name):
        score = getattr(self, stat_name)
        modifier = self.get_modifier(score)

        return f"{stat_name.capitalize()} {score} ({modifier:+})"

    def __str__(self):
        stat_lines = []

        for stat_name in self.STAT_NAMES:
            stat_lines.append(self.format_stat(stat_name))

        return "\n".join(stat_lines)


if __name__ == "__main__":
    character_stats = CharacterStats()
    print(character_stats, "\n")
    character_stats_2 = CharacterStats(
        strength=18,
        dexterity=8,
        constitution=16,
        intelligence=8,
        wisdom=12,
        ego=10,
    )
    print(character_stats_2)
