class CharacterAttributes:
    ATTRIBUTE_NAMES = (
        "might",
        "toughness",
        "agility",
        "perception",
        "intellect",
        "ego",
    )


    def __init__(
        self,
        might: int = 0,
        toughness: int = 0,
        agility: int = 0,
        perception: int = 0,
        intellect: int = 0,
        ego: int = 0,
    ):
        self.might = might
        self.toughness = toughness
        self.agility = agility
        self.perception = perception
        self.intellect = intellect
        self.ego = ego


    def format_attribute(self, attribute_name) -> str:
        score = getattr(self, attribute_name)

        return f"{attribute_name.capitalize()} {score}"


    def __str__(self) -> str:
        attribute_lines = []

        for attribute_name in self.ATTRIBUTE_NAMES:
            attribute_lines.append(self.format_attribute(attribute_name))

        return "\n".join(attribute_lines)


if __name__ == "__main__":
    character_attributes = CharacterAttributes()
    print(character_attributes, "\n")
    character_attributes_2 = CharacterAttributes(
        might=18,
        toughness=16,
        agility=8,
        perception=12,
        intellect=8,
        ego=10,
    )
    print(character_attributes_2)
