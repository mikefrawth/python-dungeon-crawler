import math


class CharacterAttributes:
    ATTRIBUTE_NAMES = (
        "might",
        "toughness",
        "agility",
        "perception",
        "intellect",
        "ego",
    )

    BASELINE = 0
    DEFAULT_COEFFICIENT = 1.0
    DEFAULT_COEFFICIENTS = dict.fromkeys(ATTRIBUTE_NAMES, DEFAULT_COEFFICIENT)


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
        self.coefficients = dict(self.DEFAULT_COEFFICIENTS)


    def format_attribute(self, attribute_name) -> str:
        score = getattr(self, attribute_name)

        return f"{attribute_name.capitalize()} {score}"


    def effective_value(self, attribute_name) -> float:
        raw = getattr(self, attribute_name)
        delta = raw - self.BASELINE
        coefficient = self.coefficients[attribute_name]

        return math.copysign(coefficient * math.sqrt(abs(delta)), delta)


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
